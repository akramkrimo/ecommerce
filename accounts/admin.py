from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserCreationForm, UserAdminChangeForm
from .models import User, EmailToken

class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'is_admin', 'is_active')
    list_filter = ('is_admin',)
    fieldsets = (
        ('User Authentication Info', {'fields':('email', 'password')}),
        ('More Info', {'fields': ('first_name', 'last_name')}),
        ('User Status', {'fields': ('is_active', 'is_admin')}),
        ('Stripe', {'fields': ('customer_id',)})
    )

    # django will automatically display the above fieldsets when you visit
    # the UserAdminChangeForm page, there's no need to tell it that it should display 
    # those fieldsets when the admin visits the UserAdminChangeForm

    # but if we want to have a custom fieldset when creating a user
    # we need to use the attribute add_fieldsets

    add_fieldsets = (
        ('Create A New User', {
            'classes': ('wide', ),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
            # all the fields specified above must be included in the UserCreateForm
        }),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(EmailToken)