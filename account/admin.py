from django.contrib import admin
from .models import Main, User
from django.contrib.auth.models import Permission

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    model = User
    list_display = ['username', 'email', 'first_name', 'last_name', 'role']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'mobile', 'personal_address', 'city', 'user_photo', 'user_stripe_id')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Other Info', {'fields': ('is_delete', 'role')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'role'),
        }),
    )
    list_filter = ('role', 'is_superuser','is_delete')
    filter_horizontal = ('groups', 'user_permissions',)
    # list_editable = ('role',)


class MainAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'tell', 'email', 'set_name', 'last_modified')
    list_display_links = ('id', 'name', 'set_name')
    # list_editable = ('is_featured',)
    # search_fields = ('id', 'name', 'description', 'create_date')
    # list_filter = ('create_date',)



admin.site.register(User, CustomUserAdmin)
admin.site.register(Main, MainAdmin)
admin.site.register(Permission)