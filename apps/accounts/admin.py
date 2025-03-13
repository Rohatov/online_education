from django.contrib import admin
from apps.accounts.models import User
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'username', 'is_active', 'is_staff', 'is_superuser']
    list_display_links = ['id', 'email', 'username']
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    search_fields = ['email', 'username']
    readonly_fields = ['id', 'last_login', 'date_joined']
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Personal', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')
        }),
    )
    ordering = ['id']
    filter_horizontal = []
    actions = ['activate_users', 'deactivate_users']

    def activate_users(self, request, queryset):
        queryset.update(is_active=True)

    activate_users.short_description = 'Activate selected users'

    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)

    deactivate_users.short_description = 'Deactivate selected users'
