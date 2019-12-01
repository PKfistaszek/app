import logging

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

import requests
import yarg

from .models import AppAuthor, AppPackage
from .serializers import AppAuthorSerializer, AppPackageSerializer


logger = logging.getLogger(__name__)


class PyPiDataDownloader:
    def __init__(self, package_name):
        self._api_url = settings.PYPI_API_URL.format(package_name)

    def start_process(self):
        response = requests.get(self._api_url)
        info = response.json()["info"]
        author_data = {
            "email": info["author_email"],
            "first_name": info["author"],
        }
        author = self._prepare_author(author_data)
        if author:
            author_pk = author.pk
        else:
            author_pk = None

        maintainers = info["maintainer"].split(",")
        maintainers_emails = info["maintainer_email"].split(",")

        maintainer_authors = self._prepare_maintainers(maintainers, maintainers_emails)

        package_data = {
            "name": info["name"],
            "current_version": info["version"],
            "description": info["description"],
            "maintainers": maintainer_authors,
            "tags": info["keywords"],
            "author": author_pk,
        }
        self._prepare_package(package_data)

    def _prepare_maintainers(self, maintainers, maintainers_emails):
        maintainers_list = []
        for m_name, m_email in zip(maintainers, maintainers_emails):
            maintainer_dict = {
                "email": m_email.replace(" ", ""),
                "first_name": m_name.replace(" ", ""),
            }
            maintainers_list.append(maintainer_dict)

        maintainer_authors = []
        for maintainer in maintainers_list:
            maintainer_author = self._prepare_author(maintainer)
            if maintainer_author:
                maintainer_authors.append(maintainer_author.pk)
        return maintainer_authors

    def _prepare_author(self, author_data):
        author_serializer = AppAuthorSerializer(data=author_data)
        if author_serializer.is_valid():
            author = author_serializer.save()
            logger.info("New Author <%s> is saved.", author.email)
            return author

        try:
            author = AppAuthor.objects.get(email=author_data["email"])
        except ObjectDoesNotExist:
            if author_serializer.errors:
                logger.error(author_serializer.errors)
            return
        author_serializer.update(author, author_data)
        logger.info("Author <%s> is updated.", author.email)
        return author

    def _prepare_package(self, package_data):
        package_serializer = AppPackageSerializer(data=package_data)
        package = None
        if package_serializer.is_valid():
            package = package_serializer.save()
            logger.info("New Application <%s> is saved.", package.name)
            return
        try:
            package = AppPackage.objects.get(name=package_data["name"])
        except ObjectDoesNotExist:
            return
        package_data["author"] = package.author
        package_serializer.update(package, package_data)
        logger.info("Application <%s> is uptaded.", package.name)
        return
