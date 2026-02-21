from django.contrib import admin
from .models import PracticeArea, SubPracticeArea


class SubPracticeInline(admin.TabularInline):
    model = SubPracticeArea
    extra = 1


@admin.register(PracticeArea)
class PracticeAreaAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    inlines = [SubPracticeInline]
    list_display = ("name",)

@admin.register(SubPracticeArea)
class SubPracticeAreaAdmin(admin.ModelAdmin):
    list_display = ("name", "practice_area")
    prepopulated_fields = {"slug": ("name",)}
