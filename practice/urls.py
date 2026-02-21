from django.urls import path
from . import views

app_name = "practice"

urlpatterns = [

    # ✅ STATIC ROUTE FIRST
    path("civil-law/", views.civil_law, name="civil_law"),
    path('criminal-law/', views.criminal_law, name='criminal_law'),
    path('family-law/', views.family_law, name='family_law'),
    path('corporate-law/', views.corporate_law, name='corporate_law'),
    path('propert-law/', views.property_law, name='property_law'),
    path('taxation-gst/', views.taxation_gst, name='taxation_gst'),
    path('services-employment-law/', views.services_employment, name='services_employment'),
    path('documentation/', views.documentation, name='documentation'),





    # dynamic routes AFTER
#     path("<slug:area_slug>/<slug:sub_slug>/",
#          views.sub_practice_detail,
#          name="sub_practice"),

#     path("<slug:slug>/",
#          views.practice_area_detail,
#          name="practice_area"),
#
# 
 ]
