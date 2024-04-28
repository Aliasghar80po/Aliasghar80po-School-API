from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, national_code, password=None, password2=None):
        """
        Creates and saves a User with the given email,username, firstname, lastname and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            national_code=national_code
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, national_code=None, password=None):
        """
        Creates and saves a Superuser with the given email,username, firstname, lastname and password.
        """
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            national_code=national_code,
        )
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user
