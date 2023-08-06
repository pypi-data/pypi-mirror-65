import unittest
import numpy as np
import pandas as pd

from azureml.automl.runtime.featurizer.transformer.timeseries.numericalize_transformer import NumericalizeTransformer
from azureml.automl.core.shared.time_series_data_frame import TimeSeriesDataFrame
from azureml.automl.core.shared.exceptions import ClientException, TransformException

from ... import utilities


def _get_transform_mapping(domain_array, target_array):
    """
    Private utility for extracting a dict/mapping from
    domain to target values.
    Domain and target are assumed to be the same length
    """
    mapping = {}
    for lvl, val in zip(domain_array, target_array):
        if lvl not in mapping:
            mapping[lvl] = val

    return mapping


class TestFTKMLNumericalizeTransformer(unittest.TestCase):
    """
    Unit tests for the Numericalize transform.

    Test NumericalizeTransformer using the transform method and also as
    part of a forecast pipeline
    """

    def setUp(self):
        train_df = pd.DataFrame({'date': pd.date_range('2012', periods=3, freq='YS'),
                                 'type': [1, 1, 2],
                                 'cat_val': ['a', 'b', 'c'],
                                 'value': np.arange(3)})

        self.train_tsdf = TimeSeriesDataFrame(data=train_df,
                                              grain_colnames=['type'],
                                              time_colname='date',
                                              ts_value_colname='value')

    def test_numericalize_consistency(self):
        """
        Test that the Numericalize transform makes consistent encodings
        when some levels are missing that were in a training set
        """
        encoder = NumericalizeTransformer()
        out_tsdf = encoder.fit_transform(self.train_tsdf)

        # Construct transform mapping for the training set
        train_cat_mapping = _get_transform_mapping(self.train_tsdf.cat_val.values,
                                                   out_tsdf.cat_val.values)

        # Test that the categorical column has been numerically encoded
        train_num_cols = (out_tsdf.select_dtypes(include=[np.number]).columns)
        self.assertTrue('cat_val' in train_num_cols)

        # Transform the test set and get the categorical mapping
        test_df = pd.DataFrame({'date': pd.date_range('2015', periods=2, freq='YS'),
                                'type': [1, 1],
                                'cat_val': ['b', 'c'],
                                'value': np.arange(2)})
        test_tsdf = TimeSeriesDataFrame(data=test_df,
                                        grain_colnames=['type'],
                                        time_colname='date',
                                        ts_value_colname='value')
        test_out = encoder.transform(test_tsdf)
        test_cat_mapping = _get_transform_mapping(test_df.cat_val.values,
                                                  test_out.cat_val.values)

        # Compare the mappings on the intersection of train and test map keys
        common_keys = train_cat_mapping.keys() & test_cat_mapping.keys()
        train_cat_mapping_sub = {lvl: val
                                 for lvl, val in train_cat_mapping.items()
                                 if lvl in common_keys}
        test_cat_mapping_sub = {lvl: val
                                for lvl, val in test_cat_mapping.items()
                                if lvl in common_keys}
        self.assertDictEqual(train_cat_mapping_sub, test_cat_mapping_sub)

    def test_numericalize_missing_level(self):
        """
        Test that the Numericalize transform makes consistent encodings
        when some levels are missing that were in a training set
        """
        train_df = pd.DataFrame({'date': pd.date_range('2012', periods=3, freq='YS'),
                                 'type': [1, 1, 2],
                                 'cat_val': ['a', 'a', 'c'],
                                 'value': np.arange(3)})
        train_tsdf = TimeSeriesDataFrame(data=train_df,
                                         grain_colnames=['type'],
                                         time_colname='date',
                                         ts_value_colname='value')

        test_df = pd.DataFrame({'date': pd.date_range('2015', periods=3, freq='YS'),
                                'type': [1, 1, 2],
                                'cat_val': ['a', 'c', 'b'],
                                'value': np.arange(3)})
        test_tsdf = TimeSeriesDataFrame(data=test_df,
                                        grain_colnames=['type'],
                                        time_colname='date',
                                        ts_value_colname='value')

        encoder = NumericalizeTransformer()
        train_out = encoder.fit_transform(train_tsdf)

        # Construct transform mapping for the training set
        train_cat_mapping = _get_transform_mapping(train_df.cat_val.values,
                                                   train_out.cat_val.values)

        # Transform the test set and get the categorical mapping
        test_out = encoder.transform(test_tsdf)
        test_cat_mapping = _get_transform_mapping(test_df.cat_val.values,
                                                  test_out.cat_val.values)

        # Test that levels present in train are encoded consistently and
        #  that the "missing level" has the integer code for NA (missing value)
        missing_level_map = {lvl: NumericalizeTransformer.NA_CODE
                             for lvl in test_cat_mapping
                             if lvl not in train_cat_mapping}
        expected_cat_mapping = train_cat_mapping.copy()
        expected_cat_mapping.update(missing_level_map)
        self.assertDictEqual(expected_cat_mapping, test_cat_mapping)

    def test_raises(self):
        """Test that transform without fit raises exception."""
        encoder = NumericalizeTransformer()
        test_df = TimeSeriesDataFrame(
            {'date': pd.date_range('2015', periods=3, freq='YS'),
             'type': [1, 1, 2],
             'cat_val': ['a', 'c', 'b'],
             'value': np.arange(3)},
            grain_colnames=['type'],
            time_colname='date',
            ts_value_colname='value')
        with self.assertRaises(ClientException):
            encoder.transform(test_df)

    def test_fit_and_transform_logged(self):
        """Test fit and transform are being logged."""
        transform = NumericalizeTransformer()
        utilities.assert_timeseries_fun_logged(transform, False, self.train_tsdf, self.train_tsdf)

    def test_include_exclude_exception(self):
        include_cols = set(["col1", "col2"])
        exclude_cols = set(["col2", "col3"])
        with self.assertRaises(TransformException) as te:
            NumericalizeTransformer(include_cols, exclude_cols)
        utilities.assert_automl_exception_fields(
            te.exception,
            "The include and exclude columns contain the same columns.",
            target="customized_columns",
            has_pii=False,
            reference_code='ef41c6ed-7187-4304-93b9-383809b73fe4'
        )

    def test_data_transformation_with_include_and_exclude_columns(self):
        include_cols = set(["int1", "date1"])
        exclude_cols = set(["cat1"])
        train_df = pd.DataFrame({'date': pd.date_range('2012', periods=3, freq='YS'),
                                 'date1': [pd.to_datetime('2000-01-01') for i in range(3)],
                                 'type': [1, 1, 2],
                                 'int1': [1, 1, 1],
                                 'int2': [1, 1, 1],
                                 'cat_val': ['a', 'a', 'c'],
                                 'cat1': ['a', 'a', 'a'],
                                 'cat2': ['a', 'a', 'a'],
                                 'value': np.arange(3)})
        train_tsdf = TimeSeriesDataFrame(data=train_df,
                                         grain_colnames=['type'],
                                         time_colname='date',
                                         ts_value_colname='value')
        encoder = NumericalizeTransformer(include_columns=include_cols, exclude_columns=exclude_cols)
        train_out = encoder.fit_transform(train_tsdf)
        assert all(val == 0 for val in train_out['int1'])
        assert all(val == 0 for val in train_out['date1'])
        assert all(val == 1 for val in train_out['int2'])
        assert all(val == 'a' for val in train_out['cat1'])
        assert all(val == 0 for val in train_out['cat2'])

        encoder = NumericalizeTransformer(include_columns=include_cols)
        train_out = encoder.fit_transform(train_tsdf)
        assert all(val == 0 for val in train_out['int1'])
        assert all(val == 0 for val in train_out['date1'])
        assert all(val == 1 for val in train_out['int2'])
        assert all(val == 0 for val in train_out['cat1'])
        assert all(val == 0 for val in train_out['cat2'])

        encoder = NumericalizeTransformer(exclude_columns=exclude_cols)
        train_out = encoder.fit_transform(train_tsdf)
        assert all(val == 1 for val in train_out['int1'])
        assert all(val == pd.to_datetime('2000-01-01') for val in train_out['date1'])
        assert all(val == 1 for val in train_out['int2'])
        assert all(val == 'a' for val in train_out['cat1'])
        assert all(val == 0 for val in train_out['cat2'])


if __name__ == '__main__':
    unittest.main()
