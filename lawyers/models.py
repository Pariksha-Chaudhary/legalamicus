from django.db import models
from django.conf import settings
from smart_selects.db_fields import ChainedForeignKey


class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="cities")
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}, {self.state.name}"


class LegalCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(
        LegalCategory,
        on_delete=models.CASCADE,
        related_name="subcategories"
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class Lawyer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    # city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    city = ChainedForeignKey(
        City,
        chained_field="state",              # field in Lawyer model
        chained_model_field="state",       # field in City model
        show_all=False,
        auto_choose=True,
        sort=True,
        on_delete=models.SET_NULL,
        null=True
    )


    experience = models.IntegerField()
    bio = models.TextField()
    profile_image = models.ImageField(upload_to='lawyers/', null=True, blank=True)

    whatsapp_number = models.CharField(max_length=15, null=True, blank=True)

    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # 👈 ADD THIS

    is_free_consultation = models.BooleanField(default=False)  # 👈 OPTIONAL

    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


class LawyerCategory(models.Model):
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE)
    category = models.ForeignKey(LegalCategory, on_delete=models.CASCADE)
    sub_category = ChainedForeignKey(
        SubCategory,
        chained_field="category",            # field in this model
        chained_model_field="category",      # field in SubCategory model
        show_all=False,
        auto_choose=True,
        sort=True,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_free_consultation = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.lawyer.user.username} - {self.category.name}"