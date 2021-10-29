from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def _create(self, email, password, name,  **extra_fields):
        if not email:
            raise ValueError('Введите Email')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, name, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', False)
        return self._create(email, password, name, **extra_fields)

    def create_superuser(self, email, password, name, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        return self._create(email, password, name, **extra_fields)


class User(AbstractBaseUser):
    email = models.EmailField('Электронная почта', primary_key=True)
    name = models.CharField('Имя', max_length=50)
    avatar = models.ImageField('Аватарка', upload_to='avatar', blank=True)
    last_name = models.CharField('Фамилия', max_length=50, blank=True)
    is_active = models.BooleanField('Активный', default=False)
    is_staff = models.BooleanField('Права администратора', default=False)
    activation_code = models.CharField('Код активации', max_length=8, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.name

    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, obj=None):
        return self.is_staff

    def create_activation_code(self):
        from django.utils.crypto import get_random_string
        self.activation_code = get_random_string(8)
        self.save()
