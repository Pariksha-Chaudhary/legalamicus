from django.shortcuts import render
from .models import PracticeArea, SubPracticeArea
from lawyers.models import Lawyer   # adjust if model name differs



def practice_area_detail(request, slug):
    area = get_object_or_404(PracticeArea, slug=slug)
    return render(request, "practice/practice_area_detail.html", {
        "area": area
    })


def sub_practice_detail(request, area_slug, sub_slug):
    sub = get_object_or_404(
        SubPracticeArea,
        slug=sub_slug,
        practice_area__slug=area_slug
    )
    return render(request, "practice/sub_practice_detail.html", {
        "sub": sub
    })
from django.shortcuts import render

def civil_law(request):
    return render(request, "practice/civil_law.html")



def criminal_law(request):
    return render(request, 'practice/criminal_law.html')
def family_law(request):
    return render(request, 'practice/family_law.html')

def corporate_law(request):
    return render(request, 'practice/corporate_law.html')

def property_law(request):
    return render(request, 'practice/property_law.html')

def taxation_gst(request):
    return render(request, 'practice/taxation_gst.html')
def services_employment(request):
    return render(request, 'practice/services_employment.html')
def documentation(request):
    return render(request, 'practice/documentation.html')
