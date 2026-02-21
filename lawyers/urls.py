from django.urls import path
from . import views

urlpatterns = [
    path('', views.lawyer_list, name='lawyer_list'),
    path('book/<int:lawyer_id>/<int:category_id>/',
     views.book_consultation,
     name='book_consultation'),


    path(
        'payment/<int:lawyer_id>/<int:category_id>/',
        views.payment_page,
        name='payment_page'   # ⚠️ THIS LINE MUST EXIST
    ),

    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
    path('ajax/load-subcategories/', views.load_subcategories, name='ajax_load_subcategories'),
]