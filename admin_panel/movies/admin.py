from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from movies.models import Filmwork, UserNotificationGroup, NotificationGroup, EmailTemplate
from movies.models import User


# Register your models here.
@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)
    list_display = (
        "title",
        "type",
        "creation_date",
        "rating",
    )
    list_filter = ("type",)
    search_fields = ("title", "description", "id")


class UserNotificationGroupInline(admin.TabularInline):
    model = UserNotificationGroup
    extra = 3
    verbose_name = _("user_notification_group_inline")
    verbose_name_plural = _("user_notification_group_inline")


@admin.register(NotificationGroup)
class NotificationUserGroupAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = (UserNotificationGroupInline,)
    list_display = (
        "fio",
        "email",
        "phone",
        "allow_send_email",
        "get_notification_group",
    )

    def get_notification_group(self, obj):
        return "\n".join([n.name for n in obj.notification_group.all()])

@admin.register(EmailTemplate)
class NotificationUserGroupAdmin(admin.ModelAdmin):
    list_display = ("name",)