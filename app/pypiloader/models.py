from django.db import models


class AppAuthor(models.Model):
    email = models.EmailField("Email", unique=True)
    first_name = models.CharField("First Name", max_length=255, null=True, blank=True)
    last_name = models.CharField("Last Name", max_length=255, null=True, blank=True)

    def __str__(self):
        return "{pk} {email}".format(pk=self.pk, email=self.email,)


class AppPackage(models.Model):
    maintainers = models.ManyToManyField(
        AppAuthor, blank=True, related_name="Maintainers",
    )
    author = models.ForeignKey(
        AppAuthor,
        on_delete=models.SET_NULL,
        verbose_name="Author",
        null=True,
        blank=True,
    )
    description = models.TextField("Description", null=True, blank=True)
    name = models.CharField("Name", unique=True, max_length=255)
    current_version = models.CharField("Current Version", max_length=255)
    tags = models.TextField("tags", null=True, blank=True)

    def __str__(self):
        return "{pk} {name}".format(pk=self.pk, name=self.name,)
