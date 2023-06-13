from django.contrib import admin


def delete_and_remove_file_on_disk(modeladmin, request, queryset):
    for obj in queryset:
        obj.delete()


delete_and_remove_file_on_disk.short_description = (
    "Delete selected objects and their files on disk"
)


class FilesifyAdmin(admin.ModelAdmin):
    list_display = ["file_path", "comment"]
    fields = [
        "file_path",
        "file_content",
        "comment",
    ]
    actions = [delete_and_remove_file_on_disk]
