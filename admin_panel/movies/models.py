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

    class Meta:
        db_table = 'content"."filmwork'
        verbose_name = _("film")
        verbose_name_plural = _("films")


class NotificationGroup(UUIDMixin):
    name = models.CharField(verbose_name=_("notification_group_name"), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'content"."notificationgroup'
        verbose_name = _("notification_group")
        verbose_name_plural = _("notification_groups")


class User(UUIDMixin, TimeStampedMixin):
    fullname = models.CharField(verbose_name=_("fullname"), max_length=255, null=True)
    login = models.CharField(verbose_name=_("login"), max_length=63)
    password = models.TextField(verbose_name=_("password"), blank=True, null=True)
    email = models.CharField(verbose_name=_("user_email"), max_length=255, blank=True, null=True)
    phone = models.CharField(verbose_name=_("user_phone"), max_length=12, blank=True, null=True)
    allow_send_email = models.BooleanField(verbose_name=_("allow_send_email"), default=False)
    confirmed_email = models.BooleanField(verbose_name=_("confirmed_email"), default=False)
    notification_group = models.ManyToManyField(
        to=NotificationGroup, verbose_name=_("notification_group_name"), through="UserNotificationGroup"
    )
    timezone = models.IntegerField(verbose_name=_("timezone"), default=0)

    def __str__(self):
        return self.fullname

    class Meta:
        db_table = 'content"."user'
        verbose_name = _("user")
        verbose_name_plural = _("users")


class UserNotificationGroup(UUIDMixin, TimeStampedCreateMixin):
    user = models.ForeignKey(to=User, verbose_name=_("user"), on_delete=models.CASCADE)
    notification_user_group = models.ForeignKey(
        to=NotificationGroup, verbose_name=_("notification_group"), on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'content"."UserNotificationUserGroup'
        constraints = [
            models.UniqueConstraint(
                fields=["user", "notification_user_group"], name="user_notification_user_group_idx"
            ),
        ]
        verbose_name = _("user_notification_group")
        verbose_name_plural = _("user_notification_groups")


class Template(UUIDMixin):
    class TemplateType(models.TextChoices):
        EMAIL = "email", _("email")
        PUSH = "push", _("push")
        SMS = "sms", _("sms")

    class TemplatePriority(models.TextChoices):
        LOW = "low", _("low")
        MEDIUM = "medium", _("medium")
        HIGH = "high", _("high")

    name = models.CharField(verbose_name=_("template_name"), max_length=255)
    template = models.TextField(verbose_name=_("template"), blank=True, null=True)
    type = models.CharField(
        verbose_name=_("type"), max_length=5, choices=TemplateType.choices, default=TemplateType.EMAIL
    )
    priority = models.CharField(
        verbose_name=_("priority"), max_length=6, choices=TemplatePriority.choices, default=TemplatePriority.MEDIUM
    )

    class Meta:
        db_table = 'content"."template'
        verbose_name = _("template")
        verbose_name_plural = _("templates")
