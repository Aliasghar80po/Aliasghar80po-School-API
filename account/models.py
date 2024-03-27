from django.db import models
from django.contrib.auth.models import AbstractUser
from account.manager import UserManager
from .validators import national_code_validator


class Grade(models.Model):
    name = models.CharField(max_length=10, verbose_name="نام مقطع")

    class Meta:
        verbose_name = "مقطع تحصیلی"
        verbose_name_plural = "مقاطع تحصیلی"

    def __str__(self):
        return self.name


class Major(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام رشته تحصیلی")

    class Meta:
        verbose_name = "رشته تحصیلی"
        verbose_name_plural = "رشته های تحصیلی"

    def __str__(self):
        return self.name


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    is_student=models.BooleanField(default=False, verbose_name="دانش آموز")
    is_teacher = models.BooleanField(default=False, verbose_name="معلم")
    email = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    national_code = models.CharField(max_length=10, blank=True, validators=[national_code_validator], verbose_name="کد ملی")
    profile_picture = models.ImageField(upload_to="account/", verbose_name="عکس پروفایل", blank=True)
    address = models.TextField(verbose_name="آدرس", blank=True)
    father_name = models.CharField(max_length=200, null=True, blank=True, verbose_name="نام پدر")
    grade = models.ForeignKey(Grade, null=True, blank=True, on_delete=models.SET_NULL, related_name="students", verbose_name="مقطع تحصیلی")
    major = models.ForeignKey(Major, null=True, blank=True, on_delete=models.SET_NULL, related_name="students", verbose_name="رشته تحصیلی")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        if not self.first_name and not self.last_name:
            return self.username
        else:
            return "%s %s" % (self.first_name, self.last_name)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
