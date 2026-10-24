from django.contrib import admin
from .models import GalleryItem, ContactMessage
@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ("title", "kind", "is_public", "created_at")
    list_filter = ("kind", "is_public")
    search_fields = ("title", "description")
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at")
    search_fields = ("name", "email", "subject")
    readonly_fields = ("name", "email", "subject", "message", "created_at")
