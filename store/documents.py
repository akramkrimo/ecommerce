from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import Product

@registry.register_document
class ProductDocument(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'products'

        # I don't fully understand this !!!!!
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = Product # the model you want to index

        # the fields of the model you want to be indexed in Elasticsearch
        fields = [
            'name',
            'description',
            'price',
        ]
