from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from guardian.admin import GuardedModelAdmin

from core.accounts.models import Account
from core.accounts.utils import get_profile_model

class AccountInline(admin.StackedInline):
    model = Account
    max_num = 1

class AccountsAdmin(UserAdmin, GuardedModelAdmin):
    inlines = [AccountInline, ]
    list_display = ('username', 'email', 'first_name', 'last_name', 
                    'is_staff', 'date_joined')

admin.site.unregister(User)
admin.site.register(User, AccountsAdmin)
#admin.site.register(get_profile_model())
