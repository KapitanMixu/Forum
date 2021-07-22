from django.contrib import admin
from .models import UserProfile, Post, Comment
from .forms import CreateUserForm
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = UserProfile
    add_form = CreateUserForm

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'User role',
            {
                'fields':
                    (
                        'desc',
                        'role',
                    )
            }
        )
    )


admin.site.register(UserProfile, CustomUserAdmin)
admin.site.register(Post)
admin.site.register(Comment)
