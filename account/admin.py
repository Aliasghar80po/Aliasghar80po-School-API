from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User, Grade, Major
from django import forms
from django.core.exceptions import ValidationError


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["email"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = forms.CharField(label="Password", widget=forms.HiddenInput)

    class Meta:
        model = User
        fields = ["email", "password", "is_active", "is_admin"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # Add your new fields here to the 'fieldsets' tuple
    # fieldsets = (
    #     *BaseUserAdmin.fieldsets,
    #     (None, {"fields": ("national_code", "profile_picture", "address", "father_name", "grade")}),
    #     ("اطلاعات عمومی", {"fields": ("data_of_birth", "major")}),
    # )

    # Extend list_display with your new fields
    # list_display = (*BaseUserAdmin.list_display, "is_student", "is_teacher", "grade", "major", "father_name")

    # Extend list_filter with your new fields
    # list_filter = (*BaseUserAdmin.list_filter, "is_teacher", "is_student", "data_of_birth", "major", "grade")

    # Extend search_fields with your new fields
    # search_fields = (*BaseUserAdmin.search_fields, "national_code", "father_name")

    # Extend add_fieldsets with your new fields
    add_fieldsets = (
        *BaseUserAdmin.add_fieldsets,
        (None, {
            "classes": ["wide"],
            "fields": ["is_student", "is_teacher", "national_code", "profile_picture", "address", "father_name", "grade", "major"]
        }),
    )


UserAdmin.fieldsets[2][1]["fields"] += ("is_teacher", "is_student")
UserAdmin.fieldsets += ("اطلاعات عمومی", {"fields": ("national_code", "profile_picture", "address", "father_name", "grade", "major")}),
UserAdmin.list_display += ("is_student", "is_teacher", "grade", "major", "father_name")
UserAdmin.list_filter += ("is_teacher", "is_student", "is_staff")
UserAdmin.search_fields += ("national_code", "father_name")

admin.site.register(User, UserAdmin)


# Register your models and admin classes here

admin.site.register(Grade)
admin.site.register(Major)

# Unregister the Group model from admin since we're not using Django's built-in permissions
admin.site.unregister(Group)
