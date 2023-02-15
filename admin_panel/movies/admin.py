from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from movies.models import Filmwork, UserNotificationGroup, NotificationGroup, Template
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


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = (UserNotificationGroupInline,)
    list_display = (
        "fullname",
        "login",
        "email",
        "phone",
        "allow_send_email",
        "confirmed_email",
        "get_notification_group",
        "timezone",
    )

    readonly_fields = ["confirmed_email"]

    def get_notification_group(self, obj):
        return "\n".join([n.name for n in obj.notification_group.all()])


@admin.register(Template)
class NotificationUserGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "priority")
