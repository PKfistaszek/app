from django.test import TestCase, tag

from .factories import AppAuthorFactory, AppPackageFactory


@tag("integration")
class AppAuthorTestCase(TestCase):
    def test_str_method(self):
        # Arrangement / Act
        author = AppAuthorFactory()

        # Assert
        self.assertEqual(
            "{pk} {email}".format(pk=author.pk, email=author.email,), str(author),
        )


@tag("integration")
class AppPackageTestCase(TestCase):
    def test_str_method(self):
        # Arrangement / Act
        package = AppPackageFactory()

        # Assert
        self.assertEqual(
            "{pk} {name}".format(pk=package.pk, name=package.name,), str(package),
        )
