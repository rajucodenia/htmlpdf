from django.urls import path
from export import views

urlpatterns =[
    path('', views.index, name='index'),
    path('pdf/', views.export_to_pdf, name='pdf'),
    path('create/', views.create, name='create'),
    path('excel/', views.export_to_excel, name='excel'),
    path('create_razorpay_order/', views.create_razorpay_order, name='create_razorpay_order'),
    path('payment/', views.payment_view, name='payment_view'),
    path('payment/callback/', views.payment_callback, name='payment_callback'),
]