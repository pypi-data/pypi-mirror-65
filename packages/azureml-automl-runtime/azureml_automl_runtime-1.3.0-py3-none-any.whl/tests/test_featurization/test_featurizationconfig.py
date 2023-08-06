import unittest
import copy

from azureml.automl.core.shared.exceptions import (ConfigException,
                                                   MissingValueException,
                                                   InvalidValueException)
from azureml.automl.core.featurization.featurizationconfig import FeaturizationConfig
from azureml.automl.core.constants import SupportedTransformers, FeatureType

from ..utilities import assert_automl_exception_fields


class TestFeaturizationConfig(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestFeaturizationConfig, self).__init__(*args, **kwargs)
        self.column_purposes = {
            'column1': FeatureType.Numeric,
            'column2': FeatureType.Categorical,
            'column3': FeatureType.Numeric}
        self.transformer_param = {
            'Imputer': [(['column1', 'column2'], {"strategy": "median"}),
                        (['column3'], {"strategy": "mean"}),
                        (['column4'], {"strategy": "median"})]}
        self.blocked_transformers = [SupportedTransformers.CatTargetEncoder]

        self.config = FeaturizationConfig(
            column_purposes=self.column_purposes,
            transformer_params=self.transformer_param,
            blocked_transformers=self.blocked_transformers)

    def test_initialize_by_param(self):
        self.assertEqual(self.config.column_purposes, self.column_purposes)
        self.assertEqual(self.config.transformer_params, self.transformer_param)
        self.assertEqual(self.config.blocked_transformers, self.blocked_transformers)

    def test_column_purpose(self):
        # test empty
        config = FeaturizationConfig()
        self.assertIsNone(config.column_purposes)

        column_purposes = {'column1': FeatureType.Numeric, 'column2': FeatureType.Categorical}

        # set test
        config.column_purposes = column_purposes
        self.assertEqual(config.column_purposes, column_purposes)
        config.column_purposes = None
        self.assertIsNone(config.column_purposes)

        # add test
        config.add_column_purpose('column1', FeatureType.Numeric)
        config.add_column_purpose('column2', FeatureType.Categorical)
        self.assertEqual(config.column_purposes, column_purposes)

        with self.assertRaises(ConfigException):
            config.add_column_purpose('column1', 'SomeFeature')
        self.assertEqual(config.column_purposes, column_purposes)

        # remove test
        config.remove_column_purpose('column1')
        column_purposes.pop('column1')
        self.assertEqual(config.column_purposes, column_purposes)

    def test_transformer_param(self):
        config = FeaturizationConfig()
        transformer_params = {
            SupportedTransformers.Imputer: [
                (['column1', 'column2'], {"strategy": "median"}),
                (['column3'], {"strategy": "mean"})
            ]
        }

        # set test
        config.transformer_params = transformer_params
        self.assertEqual(config.transformer_params, transformer_params)
        config.transformer_params = None
        self.assertIsNone(config.transformer_params)

        # add test
        config.add_transformer_params(SupportedTransformers.Imputer,
                                      ['column1', 'column2'],
                                      {"strategy": "median"})
        config.add_transformer_params(SupportedTransformers.Imputer,
                                      ['column3'],
                                      {"strategy": "mean"})
        self.assertEqual(config.transformer_params, transformer_params)

        config.remove_transformer_params(SupportedTransformers.Imputer)
        self.assertTrue(len(config.transformer_params) == 0)

        with self.assertRaises(ConfigException):
            # Transformer name is wrong
            config.add_transformer_params('WrongTransformerName', ['column1', 'column2'], {"strategy": "median"})

        with self.assertRaises(ConfigException):
            # Transformer not allowed to be customizable
            config.add_transformer_params(
                SupportedTransformers.StringCast, ['column1', 'column2'], {"strategy": "median"})

    def test_get_transformer_param(self):
        config = FeaturizationConfig()
        transformer_params = {
            SupportedTransformers.Imputer: [
                (['column1', 'column2'], {"strategy": "median"}),
                (['column3'], {"strategy": "mean"})
            ]
        }
        config.transformer_params = transformer_params
        test = config.get_transformer_params(SupportedTransformers.Imputer, ['column1', 'column2'])
        self.assertEqual(test, {"strategy": "median"})

        test = config.get_transformer_params(SupportedTransformers.Imputer, ['othercolumn'])
        self.assertEqual(test, {})

    def test_blocked_transformers(self):
        config = FeaturizationConfig()
        self.assertIsNone(config.blocked_transformers)
        blocked_transformers = [SupportedTransformers.TfIdf, SupportedTransformers.WoETargetEncoder]

        # set test
        config.blocked_transformers = blocked_transformers
        self.assertEqual(config.blocked_transformers, blocked_transformers)
        config.blocked_transformers = None
        self.assertIsNone(config.blocked_transformers)

        # add test
        config.add_blocked_transformers(blocked_transformers)
        self.assertEqual(config.blocked_transformers, blocked_transformers)

        blocked_transformers.append(SupportedTransformers.CatTargetEncoder)
        config.add_blocked_transformers(SupportedTransformers.CatTargetEncoder)
        self.assertEqual(config.blocked_transformers, blocked_transformers)

        with self.assertRaises(ConfigException):
            config.add_blocked_transformers(SupportedTransformers.CatImputer)

    def test_drop_columns(self):
        config = FeaturizationConfig()
        self.assertIsNone(config.drop_columns)
        drop_columns = ['C1', 'C2']

        # set test
        config.drop_columns = drop_columns
        self.assertEqual(config.drop_columns, drop_columns)
        config.drop_columns = None
        self.assertIsNone(config.drop_columns)

        config.add_drop_columns(drop_columns)
        config.add_drop_columns(['C3'])
        drop_columns.append('C3')
        self.assertEqual(drop_columns, config.drop_columns)

    def test_convert_timeseries_target_column_name(self):
        featurization_config = FeaturizationConfig()
        featurization_config.add_transformer_params(
            'Imputer', ['someval', 'y'], {"strategy": "constant", "fill_value": 0})
        featurization_config._convert_timeseries_target_column_name("not_exit_column")
        self.assertNotIn(
            '_automl_target_col',
            featurization_config.transformer_params['Imputer'][0][0])

        featurization_config._convert_timeseries_target_column_name("y")
        self.assertIn(
            '_automl_target_col',
            featurization_config.transformer_params['Imputer'][0][0])

    def test_invalid_transformer_strategy(self):
        transformer_param = {'Imputer': [(['someval', 'y'], {"strategy": "constant"})]}
        with self.assertRaises(MissingValueException) as ex:
            _ = FeaturizationConfig(
                column_purposes=self.column_purposes,
                transformer_params=transformer_param,
                blocked_transformers=self.blocked_transformers)
        assert_automl_exception_fields(
            ex.exception, "Fill value cannot be None for constant value imputation.",
            target="fill_value", reference_code='aef9782e-8d2f-4a4a-973f-9929e437f051', has_pii=False)

        config = copy.deepcopy(self.config)
        with self.assertRaises(MissingValueException) as ex:
            config.add_transformer_params(
                'Imputer', ['someval', 'y'], {"strategy": "constant"})
        assert_automl_exception_fields(
            ex.exception, "Fill value cannot be None for constant value imputation.",
            target="fill_value", reference_code='aef9782e-8d2f-4a4a-973f-9929e437f051', has_pii=False)

    def test_drop_column_names(self):
        drop_columns = ['column1']
        with self.assertRaises(InvalidValueException) as ex:
            _ = FeaturizationConfig(
                column_purposes=self.column_purposes,
                transformer_params=self.transformer_param,
                blocked_transformers=self.blocked_transformers,
                drop_columns=drop_columns)
        assert_automl_exception_fields(
            ex.exception, "Featurization column_purposes customization contains column1 which is in drop columns.",
            target="featurization_config.column_purposes",
            reference_code='4d2ee336-2a77-4ba2-808b-2f29dbcb546c',
            has_pii=True,
            generic_message="column_purposes configuration was provided for a column configured to be dropped.")

        config = copy.deepcopy(self.config)
        with self.assertRaises(InvalidValueException) as ex:
            config.add_drop_columns(drop_columns)
        assert_automl_exception_fields(
            ex.exception, "Featurization column_purposes customization contains column1 which is in drop columns.",
            target="featurization_config.column_purposes",
            reference_code='4d2ee336-2a77-4ba2-808b-2f29dbcb546c',
            has_pii=True,
            generic_message="column_purposes configuration was provided for a column configured to be dropped.")

        drop_columns = ['column4']
        with self.assertRaises(InvalidValueException) as ex:
            _ = FeaturizationConfig(
                column_purposes=self.column_purposes,
                transformer_params=self.transformer_param,
                blocked_transformers=self.blocked_transformers,
                drop_columns=drop_columns)
        assert_automl_exception_fields(
            ex.exception, "Featurization transformer_params customization contains column4 which is in drop columns.",
            target="featurization_config.transformer_params",
            reference_code='5b6999a3-81db-47db-b29d-1b5c43ed22aa',
            has_pii=True,
            generic_message="transformer_params configuration was provided for a column configured to be dropped.")

        config = copy.deepcopy(self.config)
        with self.assertRaises(InvalidValueException) as ex:
            config.add_drop_columns(drop_columns)
        assert_automl_exception_fields(
            ex.exception, "Featurization transformer_params customization contains column4 which is in drop columns.",
            target="featurization_config.transformer_params",
            reference_code='5b6999a3-81db-47db-b29d-1b5c43ed22aa',
            has_pii=True,
            generic_message="transformer_params configuration was provided for a column configured to be dropped.")


if __name__ == "__main__":
    unittest.main()
