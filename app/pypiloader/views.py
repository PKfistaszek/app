from django.conf import settings
from django.http import HttpResponse
from django.views.generic import ListView

from elasticsearch_dsl.query import Q

from .documents import AppPackageDocument
from .tasks import download_data


class MainView(ListView):
    template_name = "pypiloader/search.html"
    paginate_by = settings.PAGE_NUMBER

    def get_queryset(self, *args, **kwargs):
        search = AppPackageDocument.search()
        q = self.request.GET.get("q")
        if q:
            packages = search.filter(
                Q("match", name=q)
                | Q("match", description=q)
                | Q("match", current_version=q)
                | Q("match", author__first_name=q)
                | Q("match", author__last_name=q)
                | Q("match", author__email=q)
                | Q("match", maintainers__email=q)
                | Q("match", maintainers__first_name=q)
                | Q("match", maintainers__last_name=q)
            )
        else:
            packages = search

        return packages
