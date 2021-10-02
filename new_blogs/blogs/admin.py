from django.contrib import admin

# Register your models here.
from blogs.models import Article


@admin.register(Article)
class ArticalAdmin(admin.ModelAdmin):
    list_display = ["id","title","body","pub_time","status","views"]
    list_display_links = ["id","title"]
    list_filter = ["status"]
    fields =  ["title","body","pub_time","status","views"]
    show_full_result_count = True
    search_fields = ["title","status"]
    date_hierarchy = "pub_time"
