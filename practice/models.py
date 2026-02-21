from django.db import models
from django.utils.text import slugify


class PracticeArea(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Practice Areas"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SubPracticeArea(models.Model):
    practice_area = models.ForeignKey(
        PracticeArea,
        on_delete=models.CASCADE,
        related_name="sub_areas"
    )
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)  # ✅ ADD THIS
    acts = models.TextField(blank=True)         # ✅ OPTIONAL (for acts)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.practice_area.name} → {self.name}"
