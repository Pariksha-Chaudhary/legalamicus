from django.contrib import admin
from django.db.models import Sum
from .models import State, City, LegalCategory, SubCategory, Lawyer, LawyerCategory
from consultations.models import Consultation


admin.site.register(State)
admin.site.register(City)
admin.site.register(LegalCategory)
admin.site.register(SubCategory)


class LawyerCategoryInline(admin.TabularInline):
    model = LawyerCategory
    extra = 1


@admin.register(Lawyer)
class LawyerAdmin(admin.ModelAdmin):
    list_display = ('user', 'state', 'city', 'total_earnings')
    inlines = [LawyerCategoryInline]

    def total_earnings(self, obj):
        total = Consultation.objects.filter(
            lawyer=obj,
            is_paid=True
        ).aggregate(Sum('amount'))['amount__sum']

        return total or 0

    total_earnings.short_description = "Total Earnings (₹)"