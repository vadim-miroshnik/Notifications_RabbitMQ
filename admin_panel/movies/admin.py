from django.contrib import admin

from movies.models import Filmwork


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
    list_filter = (
        "type",
    )
    search_fields = ("title", "description", "id")
