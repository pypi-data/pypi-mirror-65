#! /usr/bin/env python3

import numpy as np
from sklearn.metrics import normalized_mutual_info_score
import warnings

from . import stat_utils

METRICS = ["NMI", "precision_at_1", "r_precision", "mean_average_precision_at_r"]

def get_relevance_mask(shape, gt_labels, embeddings_come_from_same_source=False, label_counts=None):
    # This assumes that k was set to at least the max number of relevant items 
    if label_counts is None:
        label_counts = {k:v for k,v in zip(*np.unique(gt_labels, return_counts=True))}
    relevance_mask = np.zeros(shape=shape, dtype=np.int)
    for k,v in label_counts.items():
        matching_rows = np.where(gt_labels==k)[0]
        max_column = v-1 if embeddings_come_from_same_source else v
        relevance_mask[matching_rows, :max_column] = 1
    return relevance_mask

def r_precision(knn_labels, gt_labels, embeddings_come_from_same_source=False, label_counts=None):
    relevance_mask = get_relevance_mask(knn_labels.shape, gt_labels, embeddings_come_from_same_source, label_counts)
    matches_per_row = np.sum((knn_labels == gt_labels) * relevance_mask.astype(bool), axis=1) 
    max_possible_matches_per_row = np.sum(relevance_mask, axis=1)
    return np.mean(matches_per_row / max_possible_matches_per_row)

def mean_average_precision_at_r(knn_labels, gt_labels, embeddings_come_from_same_source=False, label_counts=None):
    relevance_mask = get_relevance_mask(knn_labels.shape, gt_labels, embeddings_come_from_same_source, label_counts)
    num_samples, num_k = knn_labels.shape
    equality = (knn_labels == gt_labels) * relevance_mask.astype(bool)
    cumulative_correct = np.cumsum(equality, axis=1)
    k_idx = np.tile(np.arange(1, num_k + 1), (num_samples, 1))
    precision_at_ks = (cumulative_correct * equality) / k_idx
    summed_precision_per_row = np.sum(precision_at_ks * relevance_mask, axis=1)
    max_possible_matches_per_row = np.sum(relevance_mask, axis=1)
    return np.mean(summed_precision_per_row / max_possible_matches_per_row)

def precision_at_k(knn_labels, gt_labels, k):
    """
    Precision at k is the percentage of k nearest neighbors that have the correct
    label.
    Args:
        knn_labels: numpy array of size (num_samples, k)
        gt_labels: numpy array of size (num_samples, 1)
    """
    curr_knn_labels = knn_labels[:, :k]
    precision = np.mean(np.sum(curr_knn_labels == gt_labels, axis=1) / k)
    return precision


def NMI(input_embeddings, gt_labels):
    """
    Returns NMI and also the predicted labels from k-means
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        num_clusters = len(set(gt_labels.flatten()))
        pred_labels = stat_utils.run_kmeans(input_embeddings, num_clusters)
        nmi = normalized_mutual_info_score(gt_labels, pred_labels)
    return nmi, pred_labels


def compute_accuracies(query_embeddings, knn_labels, query_labels, embeddings_come_from_same_source, label_counts):
    """
    Computes clustering quality of query_embeddings.
    Computes various retrieval scores given knn_labels (labels of nearest neighbors)
    and the ground-truth labels of the query embeddings.
    Returns the results in a dictionary.
    """
    accuracies = {}
    accuracies["NMI"] = NMI(query_embeddings, query_labels)[0]
    accuracies["precision_at_1"] = precision_at_k(knn_labels, query_labels[:, None], 1)
    accuracies["r_precision"] = r_precision(knn_labels, query_labels[:, None], embeddings_come_from_same_source, label_counts)
    accuracies["mean_average_precision_at_r"] = mean_average_precision_at_r(knn_labels, query_labels[:, None], embeddings_come_from_same_source, label_counts)
    return accuracies


def get_label_counts(reference_labels):
    unique_labels, label_counts = np.unique(reference_labels, return_counts=True)
    num_k = min(1023, int(np.max(label_counts))) # faiss can only do a max of k=1024, and we have to do k+1
    return {k:v for k,v in zip(unique_labels, label_counts)}, num_k


def calculate_accuracy(
    query,
    reference,
    query_labels,
    reference_labels,
    embeddings_come_from_same_source,
):
    """
    Gets k nearest reference embeddings for each element of query.
    Then computes various accuracy metrics.
    """
    embeddings_come_from_same_source = embeddings_come_from_same_source or (query is reference)
    label_counts, num_k = get_label_counts(reference_labels)

    knn_indices = stat_utils.get_knn(
        reference,
        query,
        num_k,
        embeddings_come_from_same_source
    )
    knn_labels = reference_labels[knn_indices]
    return compute_accuracies(query, knn_labels, query_labels, embeddings_come_from_same_source, label_counts)
