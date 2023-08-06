from django.contrib import admin

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    search_fields = ('id', 'user__username', 'sso_id')
    list_display = ('sso_id', 'sso_rev', 'created_at')

admin.site.register(Profile, ProfileAdmin)
