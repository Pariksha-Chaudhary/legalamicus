from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:lawyer_id>/', views.book_lawyer, name='book_lawyer'),
    path('payment-success/<int:lawyer_id>/', views.payment_success, name='payment_success'),
    path("my-consultations/", views.my_consultations, name="my_consultations"),
    path("platform/revenue/", views.admin_revenue, name="admin_revenue"),

]
