from typing import List

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

ROUND_TO = 3


def print_evaluation(y_true: List[bool], y_pred: List[bool]):
    print(f' F1 score: {f1_score(y_true=y_true, y_pred=y_pred):.{ROUND_TO}f}')
    print(f' Accuracy: {accuracy_score(y_true=y_true, y_pred=y_pred):.{ROUND_TO}f}')
    print(f'Precision: {precision_score(y_true=y_true, y_pred=y_pred):.{ROUND_TO}f}')
    print(f'   Recall: {recall_score(y_true=y_true, y_pred=y_pred):.{ROUND_TO}f}')
