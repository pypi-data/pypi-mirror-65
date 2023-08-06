import unittest

from azureml.automl.core.shared.exceptions import ConfigException
from azureml.automl.runtime.featurizer.transformer.data import DataProviders
from azureml.automl.runtime.featurizer.transformer.data.automl_wordembeddings_provider import AutoMLEmbeddingsProvider
from azureml.automl.runtime.featurizer.transformer.data.automl_textdnn_provider import AutoMLPretrainedDNNProvider


class TestDataProviders(unittest.TestCase):
    def test_wiki_news_300d_1M_subword(self):
        embeddings = DataProviders.wiki_news_300d_1M_subword()
        assert isinstance(embeddings, AutoMLEmbeddingsProvider)
        self.assertEqual(embeddings._embeddings_name, 'wiki_news_300d_1M_subword')

    def test_glove_6B_300d_word2vec(self):
        embeddings = DataProviders.glove_6B_300d_word2vec()
        assert isinstance(embeddings, AutoMLEmbeddingsProvider)
        self.assertEqual(embeddings._embeddings_name, 'glove_6B_300d_word2vec')

    def test_pretrained_text_dnn(self):
        embeddings = DataProviders.pretrained_text_dnn()
        assert isinstance(embeddings, AutoMLPretrainedDNNProvider)
        self.assertEqual(embeddings._embedding_info._embedding_name, "bert-base-uncased")

        with self.assertRaisesRegex(ConfigException, 'Unsupported pretrained dnn type '):
            DataProviders.pretrained_text_dnn(model_name=None)

    def test_get(self):
        embeddings = DataProviders.get('non_existent')
        self.assertEqual(embeddings, None)


if __name__ == '__main__':
    unittest.main()
