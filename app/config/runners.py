from django.conf import settings
from django.test.runner import DiscoverRunner


class CustomTestSuiteRunner(DiscoverRunner):
    "Local test suite runner."
    def setup_test_environment(self):
        "Create temp directory and update MEDIA_ROOT and default storage."
        super().setup_test_environment()
        settings.CELERY_TASK_ALWAYS_EAGER = True
