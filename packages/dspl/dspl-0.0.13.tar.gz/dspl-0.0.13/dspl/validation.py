"""
# validation.py

# Team: DS.Platform
# Author: Nikita Varganov
# e-mail: nikita.varganov.ml@gmail.com

=============================================================================

A module with a transformer for data-splitting.

Available Classes:
- DataSplitter: data-splitting into train / valid / test.

=============================================================================

"""

from typing import Optional, List, Dict, Tuple, Callable

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import train_test_split


class DataSplitter(BaseEstimator, TransformerMixin):
    """
    Data-splitting into train / valid / [test].

    Parameters
    ----------
    split_fractions: List[float|int]
        Parameters for splitting sample.
        The list may be in the form of fractions of
        a split: [0.6, 0.3, 0.1] or as the number of
        observations: [200000, 100000, 50000].

    split_column: string, optional, default = None
        The name of the feature in the sample by which to split.
        Optional parameter, default = None.

    """
    def __init__(self, split_fractions, split_column = None):
        self.split_fractions = split_fractions
        self.n_samples = len(split_fractions)
        self.split_column = split_column

    def transform(self, data: pd.DataFrame, target: pd.Series) -> dict:
        """
        Spilitting data into train / valid / [test].

        Parameters
        ----------
        data: pandas.DataFrame, shape = [n_samples, n_features]
            The training input samples.

        target: pandas.Series, shape = [n_samples, ]
            The target values (class labels in classification,
            real numbers in regression).

        Returns
        -------
        eval_set: Dict[string, Tuple[pd.DataFrame, pd.Series]]
            Dict, where the key is the name of the sample
            (train / valid / [test]), value is the tuple of
            input samples and target values pairs.

        """
        splitter = self.get_splitter(data, target)
        return splitter(data, target)

    def get_splitter(self, data: pd.DataFrame, target: pd.Series) -> callable:
        """
        Choosing a method for data-splitting.

        Parameters
        ----------
        data: pandas.DataFrame, shape = [n_samples, n_features]
            The training input samples.

        target: pandas.Series, shape = [n_samples, ]
            The target values (class labels in classification,
            real numbers in regression).

        Returns
        -------
        splitter: callable
            The method of data-splitting.

        """
        if target.nunique() == 2:
            return self._random_stratify_split
        if self.split_column:
            return self._column_split
        else:
            return self._random_split

    def _random_stratify_split(self, data: pd.DataFrame, target: pd.Series):
        """
        Random and stratified (by target values) data-splitting.
        It's using when target values is binary.

        Parameters
        ----------
        data: pandas.DataFrame, shape = [n_samples, n_features]
            The training input samples.

        target: pandas.Series, shape = [n_samples, ]
            The target values (class labels in classification).

        Returns
        -------
        eval_set: Dict[string, Tuple[pd.DataFrame, pd.Series]]
            Dict, where the key is the name of the sample
            (train / valid / [test]), value is the tuple of
            input samples and target values pairs.

        """
        train_idx, *valid_idx = self._calculate_split_idx(data.index, target)
        return self._to_evalset(data, target, train_idx, *valid_idx)

    def _random_split(self, data: pd.DataFrame, target: pd.Series):
        """
        Random data-splitting.
        It's using when target values is real numbers.

        Parameters
        ----------
        data: pandas.DataFrame, shape = [n_samples, n_features]
            The training input samples.

        target: pandas.Series, shape = [n_samples, ]
            The target values (real numbers in regression).

        Returns
        -------
        eval_set: Dict[string, Tuple[pd.DataFrame, pd.Series]]
            Dict, where the key is the name of the sample
            (train / valid / [test]), value is the tuple of
            input samples and target values pairs.

        """
        train_idx, *valid_idx = self._calculate_split_idx(data.index)
        return self._to_evalset(data, target, train_idx, *valid_idx)

    def _column_split(self, data: pd.DataFrame, target: pd.Series):
        """
        Data-splitting with non-overlapping groups.
        The same group will not appear in two different folds

        Parameters
        ----------
        data: pandas.DataFrame, shape = [n_samples, n_features]
            The training input samples.

        target: pandas.Series, shape = [n_samples, ]
            The target values (real numbers in regression).

        Returns
        -------
        eval_set: Dict[string, Tuple[pd.DataFrame, pd.Series]]
            Dict, where the key is the name of the sample
            (train / valid / [test]), value is the tuple of
            input samples and target values pairs.

        """
        values = data[self.split_column].unique()
        train_idx, *valid_idx = self._calculate_split_idx(values)

        train_mask = data[self.split_column].isin(train_idx)
        train_idx = data.loc[train_mask].index

        valid_mask = [data[self.split_column].isin(idx) for idx in valid_idx]
        valid_idx = [data.loc[mask].index for mask in valid_mask]

        return self._to_evalset(data, target, train_idx, *valid_idx)

    def _calculate_split_idx(self, idx_array, target=None):
        """
        Computing indices for train / valid / [test] samples.

        Parameters
        ----------
        idx_array: numpy.array
            Indexes to split.

        target: pd.Series, optional, default = None
            The target values (class labels in classification,
            real numbers in regression). Optional, default = None.

        Returns
        -------
        idx: Tuple[np.array]
            Index tuple for train / valid / [test] parts.

        """
        train_idx, valid_idx = train_test_split(
            idx_array, train_size=self.split_fractions[0], stratify=target
        )

        if self.n_samples == 3:
            if isinstance(self.split_fractions[0], float):
                size = int(idx_array.shape[0] * self.split_fractions[1])
            else:
                size = self.split_fractions[1]

            if isinstance(target, pd.Series):
                target = target.loc[valid_idx]

            valid_idx, test_idx = train_test_split(
                valid_idx, train_size=size, stratify=target, random_state=10
            )
            return train_idx, valid_idx, test_idx

        return train_idx, valid_idx

    @staticmethod
    def _to_evalset(data, target, train_idx, *valid_idx):
        """
        Creating an eval_set dictionary, where key is the name
        of the sample, value is a tuple with the input samples
        and the target values.
        """
        eval_set = {
            "train": (data.loc[train_idx], target.loc[train_idx]),
            "valid": (data.loc[valid_idx[0]], target.loc[valid_idx[0]])
        }

        if len(valid_idx) == 2:
            eval_set["test"] = (
                data.loc[valid_idx[1]], target.loc[valid_idx[1]]
            )
        return eval_set
