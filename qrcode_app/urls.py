from django.urls import path
from qrcode_app import views

app_name = 'qrcode_app'

urlpatterns = [
    # QR Code from Field Page
    path('child_<int:child_id>/qr', views.show_qrcode, name="show_qrcode"),
]