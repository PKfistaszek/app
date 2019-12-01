import logging

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

import yarg
from celery import shared_task
from celery.decorators import periodic_task
from celery.schedules import crontab
from celery.task import task

from .models import AppAuthor, AppPackage
from .serializers import AppAuthorSerializer, AppPackageSerializer
from .utils import PyPiDataDownloader


logger = logging.getLogger(__name__)


@periodic_task(run_every=(crontab(minute="*/1")), name="hello", ignore_result=True)
def download_data():
    logger.info("Process is started")
    for package in yarg.newest_packages():
        download_package.delay(package.name)
    logger.info("Process is finished")


@task()
def download_package(package_name):
    downloader = PyPiDataDownloader(package_name)
    downloader.start_process()
