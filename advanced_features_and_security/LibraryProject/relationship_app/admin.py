from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile, Author, Book, Library, Librarian

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

# ----------------------------
# UserProfile Admin
# ----------------------------
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')  # Show username and role in admin list

# ----------------------------
# Author Admin
# ----------------------------
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)

# ----------------------------
# Book Admin
# ----------------------------
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    # Optional: Add filters
    list_filter = ('author',)

# ----------------------------
# Library Admin
# ----------------------------
@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    filter_horizontal = ('books',)  # Makes ManyToMany easier in admin

# ----------------------------
# Librarian Admin
# ----------------------------
@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ('name', 'library')
