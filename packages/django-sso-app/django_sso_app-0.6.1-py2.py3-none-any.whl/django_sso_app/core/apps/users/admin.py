from django.contrib.admin import StackedInline
from django.contrib.auth import admin as auth_admin

from .forms import UserChangeForm, UserCreationForm
from ..profiles.models import Profile

_list_display = ['username', 'email', 'is_superuser', 'last_login']
_search_fields = ['username', 'email']


class ProfileInline(StackedInline):
    model = Profile
    max_num = 1
    can_delete = False

    def get_readonly_fields(self, request, obj=None):
        # if obj is None:
        return ['sso_id', 'sso_rev']


class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    # pai
    # fieldsets = (('User', {'fields': ('name',)}),) + auth_admin.UserAdmin.fieldsets
    fieldsets = auth_admin.UserAdmin.fieldsets
    list_display = _list_display
    search_fields = _search_fields

    # pai
    inlines = [ProfileInline]
