import json
import unittest

import numpy as np
import pandas as pd

from sklearn.cluster import MiniBatchKMeans
from sklearn.preprocessing import Imputer, MaxAbsScaler

from azureml.automl.core.constants import FeatureType, SupportedTransformersInternal
from azureml.automl.runtime.featurization import GenericTransformer
from azureml.automl.runtime._engineered_feature_names import _GenerateEngineeredFeatureNames


class TestGenericTransformer(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.engineered_feature_name_generator = _GenerateEngineeredFeatureNames()
        self.column_groups = {}
        self.column_groups.setdefault(FeatureType.Numeric, ["col1", "col2"])
        super(TestGenericTransformer, self).__init__(*args, **kwargs)

    def test_get_transforms(self):
        generic_transformer = GenericTransformer()
        transforms = generic_transformer.get_transforms(self.column_groups, self.engineered_feature_name_generator)
        assert(transforms is not None)
        assert(transforms[0][0][0] == 'col1')
        assert(transforms[0][0][1] == 'col2')
        assert(len(transforms) == 1)
        assert(isinstance(transforms[0][1][0], Imputer))
        assert(isinstance(transforms[0][1][1], MaxAbsScaler))
        assert(isinstance(transforms[0][1][2], MiniBatchKMeans))

    def test_get_transforms_onnx_compatible(self):
        generic_transformer = GenericTransformer(is_onnx_compatible=True)
        transforms = generic_transformer.get_transforms(self.column_groups, self.engineered_feature_name_generator)
        self.assertEqual(transforms, [])

    def test_get_transforms_numeric(self):
        self.column_groups[FeatureType.Numeric] = ["col1"]
        generic_transformer = GenericTransformer()
        transforms = generic_transformer.get_transforms(self.column_groups, self.engineered_feature_name_generator)
        self.assertEqual(transforms, [])

    def test_get_transforms_blocked_list(self):
        generic_transformer = GenericTransformer()
        transforms = generic_transformer.get_transforms(
            self.column_groups, self.engineered_feature_name_generator,
            blocked_list=[SupportedTransformersInternal.MiniBatchKMeans])
        self.assertEqual(transforms, [])


if __name__ == '__main__':
    unittest.main()
