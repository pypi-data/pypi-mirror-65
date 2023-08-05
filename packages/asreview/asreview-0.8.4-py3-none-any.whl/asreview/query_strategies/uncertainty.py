# Copyright 2019 The ASReview Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Uncertainty sampling while saving probabilities."""

# from typing import Tuple

import numpy as np


from asreview.query_strategies.base import ProbaQueryStrategy


class UncertaintyQuery(ProbaQueryStrategy):
    """Maximum uncertainty query strategy."""

    name = "uncertainty"

    def __init__(self):
        """Initialize the maximum uncertainty query strategy.

        Arguments:
        ----------
        random_tie_break: bool
            If true randomly decide which ones to include by tie-break.
        """
        super(UncertaintyQuery, self).__init__()

    def _query(self, X, pool_idx, n_instances=1, proba=None):
        uncertainty = 1 - np.max(proba[pool_idx], axis=1)
        query_idx = np.argsort(-uncertainty)[:n_instances]
        return pool_idx[query_idx], X[pool_idx[query_idx]]
