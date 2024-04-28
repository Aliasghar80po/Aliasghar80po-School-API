from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User, Grade, Major, Teacher, Student, Course
from new.models import New
from exercise.models import Exercise, ExerciseResponse
from django import forms


class UserModelAdmin(BaseUserAdmin):
    # Add your new fields here to the 'fieldsets' tuple

    list_display = BaseUserAdmin.list_display + ("is_student", "is_teacher", "grade", "major", "father_name")
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Personal Info", {
            "fields": ("national_code", "profile_picture", "address", "father_name", "grade", "major")
        }),
        ("Permissions", {"fields": ("is_admin",)})
    )

    # Extend list_display with your new fields
    ordering = BaseUserAdmin.ordering + ("is_admin", "id")

    # Extend search_fields with your new fields
    search_fields = BaseUserAdmin.search_fields + ("national_code", "father_name")

    # Extend add_fieldsets with your new fields
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {
            "classes": ["wide"],
            "fields": ["is_student", "is_teacher", "profile_picture", "address", "father_name", "grade", "major"]
        }),
    )


class StudentInline(admin.TabularInline):
    model = Student
    fk_name = 'teacher_user'
    fields = ('first_name', 'last_name', 'national_code')


class NewInline(admin.TabularInline):
    model = New
    fields = ('title',)


class ExerciseInline(admin.TabularInline):
    model = Exercise
    fields = ('title', 'deadline')


class ExerciseResponseInline(admin.TabularInline):
    model = ExerciseResponse
    fields = ('student', 'response_text', 'attached_file')


class TeacherAdmin(BaseUserAdmin):
    # Add your new fields here to the 'fieldsets' tuple
    fieldsets = BaseUserAdmin.fieldsets + (
        ("personal info", {
            "fields": ("profile_picture", "address", "father_name", "grade", "major", "courses")
        }),
        ("permission", {'fields': ("is_admin",)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {
            "classes": ["wide"],
            "fields": ["national_code", "profile_picture", "address", "father_name", "grade", "major", "courses"]
        }),
    )

    # Extend list_display with your new fields
    list_display = BaseUserAdmin.list_display + (
        "email", "is_admin", "is_student", "is_teacher", "grade", "major", "father_name")

    inlines = [StudentInline, NewInline, ExerciseInline, ExerciseResponseInline]


class StudentAdmin(BaseUserAdmin):
    # Add your new fields here to the 'fieldsets' tuple
    fieldsets = BaseUserAdmin.fieldsets + (
        ("personal info", {
            "fields": ("profile_picture", "address", "father_name", "grade", "major", "course")
        }),
        ("permission", {'fields': ("is_admin",)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {
            "classes": ["wide"],
            "fields": ["national_code", "profile_picture", "address", "father_name", "grade", "major", "course"]
        }),
    )

    # Extend list_display with your new fields
    list_display = BaseUserAdmin.list_display + (
        "email", "is_admin", "is_student", "is_teacher", "grade", "major", "father_name")


admin.site.register(User, UserModelAdmin)
admin.site.register(Grade)
admin.site.register(Major)

admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
# Unregister the Group model from admin since we're not using Django's built-in permissions
admin.site.unregister(Group)
admin.site.register(Course)
