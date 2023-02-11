import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedUpdateMixin(models.Model):
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TimeStampedCreateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class TimeStampedMixin(TimeStampedUpdateMixin, TimeStampedCreateMixin):
    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Filmwork(UUIDMixin, TimeStampedMixin):
    class TypeChoice(models.TextChoices):
        movie = "movie", _("movie")
        tv_show = "tv_show", _("tv_show")

    title = models.CharField(verbose_name=_("title"), max_length=255)
    description = models.TextField(verbose_name=_("description"), blank=True, null=True)
    creation_date = models.DateField(verbose_name=_("created_date"), blank=True, null=True)
    rating = models.FloatField(
        verbose_name=_("rating"),
        blank=True,
        null=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
    )
    type = models.CharField(verbose_name=_("types"), max_length=7, choices=TypeChoice.choices, default=TypeChoice.movie)


class User(UUIDMixin, TimeStampedMixin):
    login = models.CharField(verbose_name=_("login"), max_length=63)
    password = models.TextField(verbose_name=_("password"), blank=True, null=True)
    fullname = models.CharField(verbose_name=_("fullname"), max_length=127, null=True)
    email = models.CharField(verbose_name=_("email"), max_length=63, null=True)
    phone = models.CharField(verbose_name=_("phone"), max_length=31, null=True)
    subscribed = models.BooleanField(verbose_name=_("subscribed"), default=False)
    confirmed = models.BooleanField(verbose_name=_("confirmed"), default=False)


class Template(UUIDMixin, TimeStampedMixin):
    template = models.TextField(verbose_name=_("template"), blank=True, null=True)
