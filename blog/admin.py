# Register your models here.
from django.contrib import admin

from blog.models import Post


@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "published_at")
    prepopulated_fields = {
        "slug": ("title",),
    }
    list_filter = ["status", "created_at", "published_at", "author"]
    search_fields = ["title", "body"]
    raw_id_fields = ["author"]
    date_hierarchy = "published_at"
    ordering = ["status", "published_at"]
