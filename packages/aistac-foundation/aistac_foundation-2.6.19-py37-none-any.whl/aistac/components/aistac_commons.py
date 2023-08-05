import collections
import re
import threading
from abc import abstractmethod
from copy import deepcopy
from datetime import datetime
from typing import Any

__author__ = 'Darryl Oatridge'


class AistacCommons(object):

    @staticmethod
    def list_formatter(value: Any) -> list:
        """ Useful utility method to convert any type of str, list, tuple or pd.Series into a list"""
        if isinstance(value, (int, float, str, datetime)):
            return [value]
        if isinstance(value, (list, tuple, set)):
            return list(value)
        if isinstance(value, (collections.abc.KeysView, collections.abc.ValuesView, collections.abc.ItemsView)):
            return list(value)
        if isinstance(value, dict):
            return list(value.keys())
        return list()

    @staticmethod
    def label_gen(limit: int=None) -> str:
        """generates a sequential headers. if limit is set will return at that limit"""
        headers = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        counter = 0
        for n in range(0, 100):
            for i in range(len(headers)):
                rtn_str = f"{headers[i]}" if n == 0 else f"{headers[i]}{n}"
                if isinstance(limit, int) and counter >= limit:
                    return rtn_str
                counter += 1
                yield rtn_str

    @staticmethod
    def unique_list(seq: list) -> list:
        """ Useful utility method to retain the order of a list but removes duplicates"""
        seen = set()
        # Note: assign seen add to a local variable as local variable are less costly to resolve than dynamic call
        seen_add = seen.add
        # Note: seen.add() always returns None, the 'or' is only there to attempt to set update
        return [x for x in seq if not (x in seen or seen_add(x))]

    @staticmethod
    def filter_headers(data: dict, headers: [str, list]=None, drop: bool=None, dtype: [str, list]=None,
                       exclude: bool=None, regex: [str, list]=None, re_ignore_case: bool=None) -> list:
        """ returns a list of headers based on the filter criteria

        :param data: the Canonical data to get the column headers from
        :param headers: a list of headers to drop or filter on type
        :param drop: to drop or not drop the headers
        :param dtype: the column types to include or excluse. Default None else int, float, bool, object, 'number'
        :param exclude: to exclude or include the dtypes. Default is False
        :param regex: a regiar expression to seach the headers
        :param re_ignore_case: true if the regex should ignore case. Default is False
        :return: a filtered list of headers

        :raise: TypeError if any of the types are not as expected
        """
        if drop is None or not isinstance(drop, bool):
            drop = False
        if exclude is None or not isinstance(exclude, bool):
            exclude = False
        if re_ignore_case is None or not isinstance(re_ignore_case, bool):
            re_ignore_case = False

        if not isinstance(data, dict):
            raise TypeError("The first function attribute must be a dictionary")
        _headers = AistacCommons.list_formatter(headers)
        dtype = AistacCommons.list_formatter(dtype)
        regex = AistacCommons.list_formatter(regex)
        _obj_cols = list(data.keys())
        _rtn_cols = set()
        unmodified = True

        if _headers is not None and _headers:
            _rtn_cols = set(_obj_cols).difference(_headers) if drop else set(_obj_cols).intersection(_headers)
            unmodified = False

        if regex is not None and regex:
            re_ignore_case = re.I if re_ignore_case else 0
            _regex_cols = list()
            for exp in regex:
                _regex_cols += [s for s in _obj_cols if re.search(exp, s, re_ignore_case)]
            _rtn_cols = _rtn_cols.union(set(_regex_cols))
            unmodified = False

        if unmodified:
            _rtn_cols = set(_obj_cols)

        if dtype is not None and dtype:
            type_header = []
            for col in _rtn_cols:
                if any((isinstance(x, tuple(dtype)) for x in col)):
                    type_header.append(col)
            _rtn_cols = set(_rtn_cols).difference(type_header) if exclude else set(_rtn_cols).intersection(type_header)

        return [c for c in _rtn_cols]

    @staticmethod
    def filter_columns(data: dict, headers=None, drop=False, dtype=None, exclude=False, regex=None,
                       re_ignore_case=None, inplace=False) -> dict:
        """ Returns a subset of columns based on the filter criteria

        :param data: the Canonical data to get the column headers from
        :param headers: a list of headers to drop or filter on type
        :param drop: to drop or not drop the headers
        :param dtype: the column types to include or excluse. Default None else int, float, bool, object, 'number'
        :param exclude: to exclude or include the dtypes
        :param regex: a regiar expression to seach the headers
        :param re_ignore_case: true if the regex should ignore case. Default is False
        :param inplace: if the passed pandas.DataFrame should be used or a deep copy
        :return:
        """
        if not inplace:
            with threading.Lock():
                data = deepcopy(data)
        obj_cols = AistacCommons.filter_headers(data=data, headers=headers, drop=drop, dtype=dtype, exclude=exclude,
                                                regex=regex, re_ignore_case=re_ignore_case)
        for col in data.keys():
            if col not in obj_cols:
                data.pop(col)
        return data


class AnalyticsCommons(object):
    label: str
    associate: str
    dtype: str
    selection: list
    granularity: [int, float, list]
    lower: [int, float]
    upper: [int, float]
    top: int
    precision: int
    year_first: bool
    day_first: bool
    data_format: str
    weighting_precision: int
    exclude_dominant: bool
    weight_pattern: list
    weight_mean: list
    weight_std: list
    sample_distribution: list
    dominant_values: list
    dominance_weighting: list
    dominant_percent: float
    nulls_percent: float
    sample: int
    outlier_percent: float
    mean: [int, float]
    var: float
    skew: float
    kurtosis: float

    def __init__(self, analysis: dict, label: str = None):
        self._analysis = analysis
        self.label = label if isinstance(label, str) else 'unnamed'
        self.dtype = analysis.get('intent', {}).get('dtype', 'object')
        self.selection = analysis.get('intent', {}).get('selection', list())
        self.granularity = analysis.get('intent', {}).get('granularity', 1)
        self.lower = analysis.get('intent', {}).get('lower', 0.0)
        self.upper = analysis.get('intent', {}).get('upper', 1.0)
        self.top = analysis.get('intent', {}).get('top', None)
        self.precision = analysis.get('intent', {}).get('precision', 3)
        self.year_first = analysis.get('intent', {}).get('year_first', False)
        self.day_first = analysis.get('intent', {}).get('day_first', False)
        self.data_format = analysis.get('intent', {}).get('data_format', None)
        self.weighting_precision = analysis.get('intent', {}).get('weighting_precision', None)

        self.weight_pattern = analysis.get('patterns', {}).get('weight_pattern', list())
        self.weight_mean = analysis.get('patterns', {}).get('weight_mean', list())
        self.weight_std = analysis.get('patterns', {}).get('weight_std', list())
        self.sample_distribution = analysis.get('patterns', {}).get('sample_distribution', list())
        self.dominant_values = analysis.get('patterns', {}).get('dominant_values', list())
        self.dominance_weighting = analysis.get('patterns', {}).get('dominance_weighting', list())
        self.dominant_percent = analysis.get('patterns', {}).get('dominant_percent', 0)

        self.nulls_percent = analysis.get('stats', {}).get('nulls_percent', 0)
        self.sample = analysis.get('stats', {}).get('sample', 0)
        self.outlier_percent = analysis.get('stats', {}).get('outlier_percent', 0)
        self.mean = analysis.get('stats', {}).get('mean', 0)
        self.var = analysis.get('stats', {}).get('var', 0)
        self.skew = analysis.get('stats', {}).get('skew', 0)
        self.kurtosis = analysis.get('stats', {}).get('kurtosis', 0)

    def __str__(self):
        return self._analysis.__str__()

    def __repr__(self):
        return f"<{self.__class__.__name__} {str(self._analysis)}"

