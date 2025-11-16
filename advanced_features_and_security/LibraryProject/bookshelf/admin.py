    
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # shows these columns
    list_filter = ('publication_year', 'author')  # adds filter sidebar

# ----------------------------
# Custom User Admin
# ----------------------------
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Add the extra fields to both edit and create forms in admin
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('date_of_birth', 'profile_photo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('date_of_birth', 'profile_photo')}),
    )

# Register CustomUser with custom admin
admin.site.register(CustomUser, CustomUserAdmin)




