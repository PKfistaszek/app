from django.test import TestCase, modify_settings, tag

from mock import Mock, patch
from pypiloader.models import AppAuthor, AppPackage
from pypiloader.tasks import download_data

from .factories import AppAuthorFactory, AppPackageFactory


@patch("pypiloader.utils.requests")
@patch("pypiloader.tasks.yarg")
class DownloadDataTestCase(TestCase):
    def setUp(self):
        super().setUp()

    def test_download_data_new_objects(self, yarg, requests):
        # Arrangement
        maintainers_number = 2
        author_obj = AppAuthorFactory.build()
        package_obj = AppPackageFactory.build()
        maintainers = AppAuthorFactory.build_batch(maintainers_number)
        maintainers_emails = ",".join([m.email for m in maintainers])
        maintainers_str = ",".join([m.first_name for m in maintainers])
        author_dict = author_obj.__dict__
        package_dict = package_obj.__dict__
        package = Mock()
        package.name = "test"

        response = Mock()
        requests.get.return_value = response
        response.json.return_value = {
            "info": {
                "author_email": author_dict["email"],
                "author": author_dict["first_name"],
                "name": package_dict["name"],
                "description": package_dict["description"],
                "keywords": "test_tag_1, test_tag_1",
                "maintainer": maintainers_str,
                "maintainer_email": maintainers_emails,
                "version": package_dict["current_version"],
            }
        }
        yarg.newest_packages.return_value = [package]

        # Act
        download_data()

        # Assert
        package = AppPackage.objects.get(name=package_obj.name)

        self.assertEqual(package.author.email, author_obj.email)
        self.assertEqual(package.author.first_name, author_obj.first_name)
        self.assertEqual(package.maintainers.count(), maintainers_number)
        self.assertEqual(package.description, package_obj.description)
        self.assertEqual(package.current_version, package_obj.current_version)
        self.assertEqual(package.name, package_obj.name)

    def test_download_data_update_objects(self, yarg, requests):
        # Arrangement
        maintainers_number = 2
        author_obj = AppAuthorFactory.create()
        package_obj = AppPackageFactory.create(author=author_obj)
        maintainers = AppAuthorFactory.create_batch(maintainers_number)
        maintainers_emails = ",".join([m.email for m in maintainers])
        maintainers_str = ",".join([m.first_name for m in maintainers])
        author_dict = author_obj.__dict__
        package_dict = package_obj.__dict__
        package = Mock()
        package.name = "test"
        new_description = "new_description"

        response = Mock()
        requests.get.return_value = response
        response.json.return_value = {
            "info": {
                "author_email": author_dict["email"],
                "author": author_dict["first_name"],
                "name": package_dict["name"],
                "description": new_description,
                "keywords": "test_tag_1, test_tag_1",
                "maintainer": maintainers_str,
                "maintainer_email": maintainers_emails,
                "version": package_dict["current_version"],
            }
        }
        yarg.newest_packages.return_value = [package]

        # Act
        download_data()

        # Assert
        package = AppPackage.objects.get(name=package_obj.name)

        self.assertEqual(package.author.email, author_obj.email)
        self.assertEqual(package.author.first_name, author_obj.first_name)
        self.assertEqual(package.maintainers.count(), maintainers_number)
        self.assertEqual(package.description, new_description)
        self.assertEqual(package.current_version, package_obj.current_version)
        self.assertEqual(package.name, package_obj.name)

    def test_download_data_save_no_user(self, yarg, requests):
        # Arrangement
        maintainers_number = 2
        package_obj = AppPackageFactory.build(author=None)
        maintainers = AppAuthorFactory.build_batch(maintainers_number)
        maintainers_emails = ",".join([m.email for m in maintainers])
        maintainers_str = ",".join([m.first_name for m in maintainers])
        package_dict = package_obj.__dict__
        package = Mock()
        package.name = "test"

        response = Mock()
        requests.get.return_value = response
        response.json.return_value = {
            "info": {
                "author_email": "",
                "author": "",
                "name": package_dict["name"],
                "description": package_dict["description"],
                "keywords": "test_tag_1, test_tag_1",
                "maintainer": maintainers_str,
                "maintainer_email": maintainers_emails,
                "version": package_dict["current_version"],
            }
        }
        yarg.newest_packages.return_value = [package]

        # Act
        download_data()

        # Assert
        package = AppPackage.objects.get(name=package_obj.name)

        self.assertEqual(package.maintainers.count(), maintainers_number)
        self.assertEqual(package.description, package_obj.description)
        self.assertEqual(package.current_version, package_obj.current_version)
        self.assertEqual(package.name, package_obj.name)

    def test_download_data_no_package_name(self, yarg, requests):
        # Arrangement
        maintainers_number = 2
        author_obj = AppAuthorFactory.build()
        package_obj = AppPackageFactory.build()
        maintainers = AppAuthorFactory.build_batch(maintainers_number)
        maintainers_emails = ",".join([m.email for m in maintainers])
        maintainers_str = ",".join([m.first_name for m in maintainers])
        author_dict = author_obj.__dict__
        package_dict = package_obj.__dict__
        package = Mock()
        package.name = "test"

        response = Mock()
        requests.get.return_value = response
        response.json.return_value = {
            "info": {
                "author_email": author_dict["email"],
                "author": author_dict["first_name"],
                "name": "",
                "description": package_dict["description"],
                "keywords": "test_tag_1, test_tag_1",
                "maintainer": maintainers_str,
                "maintainer_email": maintainers_emails,
                "version": package_dict["current_version"],
            }
        }
        yarg.newest_packages.return_value = [package]

        # Act
        download_data()

        # Assert
        package_count = AppPackage.objects.count()
        self.assertFalse(package_count)
