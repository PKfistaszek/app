from django_elasticsearch_dsl import DocType, Index, fields

from .models import AppAuthor, AppPackage


package_index = Index("packages")

package_index.settings(number_of_shards=1, number_of_replicas=0)


@package_index.doc_type
class AppPackageDocument(DocType):

    author = fields.ObjectField(
        properties={
            "first_name": fields.TextField(),
            "last_name": fields.TextField(),
            "email": fields.TextField(),
        }
    )

    maintainers = fields.NestedField(
        properties={
            "first_name": fields.TextField(),
            "last_name": fields.TextField(),
            "email": fields.TextField(),
        }
    )

    class Django:
        model = AppPackage

        fields = [
            "name",
            "description",
            "current_version",
            "tags",
        ]

        related_models = [AppAuthor]

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, AppAuthor):
            return related_instance.apppackage_set.all()
