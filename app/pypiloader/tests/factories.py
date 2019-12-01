import factory
import factory.fuzzy
from pypiloader.models import AppAuthor, AppPackage


class AppAuthorFactory(factory.DjangoModelFactory):
    email = factory.Sequence(lambda n: "email_{}@test.pl".format(n))
    first_name = factory.Sequence(lambda n: "name {}".format(n))
    last_name = factory.Sequence(lambda n: "last name {}".format(n))

    class Meta:
        model = AppAuthor


class AppPackageFactory(factory.DjangoModelFactory):
    author = factory.SubFactory(AppAuthorFactory)
    description = factory.Sequence(lambda n: "description {}".format(n))
    name = factory.Sequence(lambda n: "name {}".format(n))
    current_version = factory.Sequence(lambda n: "1.{}".format(n))

    class Meta:
        model = AppPackage

    @factory.post_generation
    def maintainers(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            for maintainer in extracted:
                self.maintainers.add(maintainer)
