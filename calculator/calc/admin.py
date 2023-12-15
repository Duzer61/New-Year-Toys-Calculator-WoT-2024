from django.contrib import admin

from .models import UserAlbums


class UserAlbumsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserAlbums._meta.fields]
    search_fields = ['user']


admin.site.register(UserAlbums, UserAlbumsAdmin)
