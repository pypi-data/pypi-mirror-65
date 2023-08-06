import numpy as np
import pandas as pd
import unittest

from azureml.automl.runtime.featurizer.transformer.timeseries.missingdummies_transformer\
    import MissingDummiesTransformer
from azureml.automl.runtime.shared.time_series_data_frame import TimeSeriesDataFrame

from numpy.ma.testutils import assert_array_equal
from ... import utilities


class TestMissingDummiesTransformer(unittest.TestCase):
    """Tests for the MissingDummiesTransformer."""

    DATE = 'date'
    TGT = 'y'

    def setUp(self):
        """Create the data frame."""
        df = pd.DataFrame(
            {TestMissingDummiesTransformer.DATE: pd.date_range('2001-01-01',
                                                               freq='D', periods=12),
             'val': 42,
             TestMissingDummiesTransformer.TGT: np.arange(12),
             'missing_val': [np.nan, 2, 3, 4, 5, np.nan,
                             np.nan, 8, 9, 10, np.nan, np.NaN]
             })
        self.tsdf = TimeSeriesDataFrame(
            df,
            time_colname=TestMissingDummiesTransformer.DATE,
            ts_value_colname=TestMissingDummiesTransformer.TGT)

    def test_missing_dummies(self):
        """Test MissingDummiesTransformer."""
        target = 'missing_val'
        transform = MissingDummiesTransformer([target])
        x_transformed = transform.fit_transform(self.tsdf)
        new_col = MissingDummiesTransformer.get_column_name(target)
        self.assertNotEqual(new_col, target, 'New column shold not equal target column.')
        self.assertIn(
            new_col, x_transformed,
            "The data frame was not transformed.")
        expected = np.array([1, 0, 0, 0, 0, 1,
                             1, 0, 0, 0, 1, 1])
        assert_array_equal(expected, x_transformed[new_col].values)

    def test_fit_and_transform_logged(self):
        """Test fit and transform are being logged."""
        transform = MissingDummiesTransformer(['missing_val'])
        utilities.assert_timeseries_fun_logged(transform, False, self.tsdf, self.tsdf)


if __name__ == '__main__':
    unittest.main()
