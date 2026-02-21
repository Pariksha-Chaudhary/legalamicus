from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('consultation/', views.consultation, name='consultation'),

    path('practice-areas/', views.practice_areas, name='practice_areas'),
    path('appointment/', views.appointment, name='appointment'),
    path('blog/', views.blog, name='blog'),

    path('casestudy/', views.casestudy, name='casestudy'),
    path('faq/', views.faq, name='faq'),
     path('term_conditions/', views.term_conditions, name='term_conditions'),


    # path('practice/<slug:area_slug>/', views.practice_detail, name='practice_detail'),
    # path('practice/<slug:area_slug>/<slug:sub_slug>/', views.sub_practice_detail, name='sub_practice_detail'),



]
