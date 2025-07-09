from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.conf import settings

# ユーザー用マネージャー
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


# カスタムユーザーモデル
class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    # 追加のフィールド
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)  # ←これを追加
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
    
class MenuItem(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='menu_images/')
    
    def __str__(self):
        return self.name

class Reservation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        null=True, blank=True  # ← これを追加 
    )  # `default`に指定したユーザーIDがデフォルトで設定される
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    date_time = models.DateTimeField()
    number_of_people = models.IntegerField()
    inquiry = models.TextField(blank=True, null=True)  # ← 忘れず追加
    created_at = models.DateTimeField(auto_now_add=True)  # ← 追加！

    # 新しく追加
    is_confirmed = models.BooleanField(default=False, verbose_name="本予約済み")
    follow_up_note = models.TextField(blank=True, null=True, verbose_name="問い合わせ対応メモ")
    confirmation_email_sent = models.BooleanField(default=False)  # ←追加

    def __str__(self):
        user_email = self.user.email if self.user else "Anonymous"
        return f"Reservation for {user_email} on {self.date_time}"
    
class SpecialOffer(models.Model):
    title = models.CharField(max_length=100, default="ご予約の方へ一品プレゼント！")
    description = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='special_offers/')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title