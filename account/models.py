from django.contrib import auth
from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from account.manager import UserManager
from .validators import national_code_validator
from exercise.models import Exercise


class Grade(models.Model):
    name = models.CharField(max_length=10, verbose_name="grade name")

    class Meta:
        verbose_name = "grade"
        verbose_name_plural = "grades"

    def __str__(self):
        return self.name


class Major(models.Model):
    name = models.CharField(max_length=200, verbose_name="major name")

    class Meta:
        verbose_name = "major"
        verbose_name_plural = "majors"

    def __str__(self):
        return self.name


def _user_get_permissions(user, obj, from_name):
    permissions = set()
    name = "get_%s_permissions" % from_name
    for backend in auth.get_backends():
        if hasattr(backend, name):
            permissions.update(getattr(backend, name)(user, obj))
    return permissions


class User(AbstractUser):
    username = models.CharField(max_length=150, null=True, blank=True)
    is_student = models.BooleanField(default=False, verbose_name="student")
    is_teacher = models.BooleanField(default=False, verbose_name="Teacher")
    is_staff = models.BooleanField(default=False)
    email = models.EmailField(verbose_name="Email", max_length=255, unique=True)
    national_code = models.CharField(max_length=10, null=True, unique=True, validators=[national_code_validator],
                                     verbose_name="national code")
    profile_picture = models.ImageField(upload_to="account/", verbose_name="profile picture", blank=True)
    address = models.TextField(verbose_name="address", blank=True)
    father_name = models.CharField(max_length=200, null=True, blank=True, verbose_name="father name")
    grade = models.ForeignKey(Grade, null=True, blank=True, on_delete=models.SET_NULL, related_name="students",
                              verbose_name="grade")
    major = models.ForeignKey(Major, null=True, blank=True, on_delete=models.SET_NULL, related_name="students",
                              verbose_name="major")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name", "password"]

    def __str__(self):
        if self.get_full_name() == None:
            return self.get_username()
        return self.get_full_name()

    def get_full_name(self):
        if not self.first_name and not self.last_name:
            return self.username
        else:
            return "%s %s" % (self.first_name, self.last_name)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_all_permissions(self, obj=None):
        return _user_get_permissions(self, obj, "all")

    def get_superuser(self):
        return self.is_admin


class Teacher(User):
    school_name = models.CharField(max_length=255, verbose_name="School name", blank=True)
    biography = models.TextField(verbose_name="biography", blank=True)
    courses = models.ForeignKey('Course', verbose_name="Teacher's courses", on_delete=models.CASCADE,
                                related_name="teachers", blank=True, null=True)
    assigned_student = models.ForeignKey('Student', on_delete=models.CASCADE, verbose_name="Teacher's students",
                                         blank=True,
                                         null=True, related_name="teachers")

    class Meta:
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"


class Student(User):
    teacher_user = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='students', null=True, blank=True)
    course = models.ForeignKey('Course', verbose_name="course", on_delete=models.CASCADE,
                               related_name="enrolled_students",
                               blank=True, null=True)  # Changed related_name to 'enrolled_students'

    class Meta:
        verbose_name = "student"
        verbose_name_plural = "students"


class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name="Course name", blank=True)
    description = models.TextField(verbose_name="description", blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='taught_courses', null=True,
                                blank=True)  # Changed related_name to 'taught_courses'
    students = models.ManyToManyField(Student, related_name='enrolled_courses', null=True,
                                      blank=True)

    def __str__(self):
        return self.name
