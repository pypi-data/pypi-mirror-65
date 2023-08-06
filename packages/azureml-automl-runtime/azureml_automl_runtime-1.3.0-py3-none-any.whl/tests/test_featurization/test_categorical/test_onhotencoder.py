import unittest

import numpy as np
from sklearn.preprocessing import OneHotEncoder
import pandas as pd

from azureml.automl.runtime.featurizer.transformer import OneHotEncoderTransformer


class OneHotEncoderTransformerTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(OneHotEncoderTransformerTests, self).__init__(*args, **kwargs)
        self.onehot_encoder_transformer = OneHotEncoderTransformer(handle_unknown='ignore')

    def test_onehot_encoding_unique_values(self):
        # Test if training data is correctly one hot encoded
        train_set_category_array = np.array(
            ['Red', 'Blue', 'Green', 'Yellow'])
        expected_train_set_label_array = np.array([[0., 0., 1., 0.],
                                                   [1., 0., 0., 0.],
                                                   [0., 1., 0., 0.],
                                                   [0., 0., 0., 1.]])
        actual_train_set_label_array = self.onehot_encoder_transformer \
            .fit_transform(train_set_category_array).toarray()
        self.assertEquals(type(self.onehot_encoder_transformer.get_model()), OneHotEncoder)
        self.assertListEqual(self.onehot_encoder_transformer.get_feature_names(), ['Blue', 'Green', 'Red', 'Yellow'])
        self.assertTrue(np.all(expected_train_set_label_array ==
                               actual_train_set_label_array))

        # Test if test data is correctly one hot encoded
        test_set_category_array = np.array(['Blue', 'Yellow'])
        expected_test_set_label_array = np.array([[1., 0., 0., 0.],
                                                  [0., 0., 0., 1.]])
        actual_test_set_label_array = self.onehot_encoder_transformer.transform(test_set_category_array)
        self.assertTrue(np.all(expected_test_set_label_array ==
                               actual_test_set_label_array))

    def test_onehot_encoding_datatypes(self):
        # ndarray with len(shape) > 1
        train_set_category_array = np.array(
            [['Red'], ['Blue'], ['Red'], ['Blue']])
        expected_train_set_label_array = np.array([[0., 1.],
                                                   [1., 0.],
                                                   [0., 1.],
                                                   [1., 0.]])
        actual_train_set_label_array = self.onehot_encoder_transformer \
            .fit_transform(train_set_category_array).toarray()
        self.assertTrue(np.all(expected_train_set_label_array ==
                               actual_train_set_label_array))

        # pandas Series
        train_set_category_series = pd.Series(
            ['Red', 'Blue', 'Green', 'Yellow'])
        expected_train_set_label_array = np.array([[0., 0., 1., 0.],
                                                   [1., 0., 0., 0.],
                                                   [0., 1., 0., 0.],
                                                   [0., 0., 0., 1.]])
        actual_train_set_label_array = self.onehot_encoder_transformer \
            .fit_transform(train_set_category_series).toarray()
        self.assertTrue(np.all(expected_train_set_label_array ==
                               actual_train_set_label_array))

    def test_get_transformer_name(self):
        self.assertEquals(self.onehot_encoder_transformer._get_transformer_name(), 'OneHotEncoder')


if __name__ == "__main__":
    unittest.main()
