from django.contrib import admin
from .models import ImageCaption

class ImageCaptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'caption', 'count_likes', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('caption',)
    readonly_fields = ('created_at',)

    def count_likes(self, obj):
        return obj.likes.count()

    count_likes.short_description = 'Number of Likes'

admin.site.register(ImageCaption, ImageCaptionAdmin)