from django.urls import path
from tale_app import views

app_name = 'tale_app'

urlpatterns = [
    path('child_<int:child_id>/tales', views.TalesList.as_view(), name="TalesList"),
    path('child_<int:child_id>/tales_<int:tale_id>/start', views.TaleStart.as_view(), name="TaleStart"),
    path('child_<int:child_id>/tales_<int:tale_id>/end', views.TaleEnd.as_view(), name="TaleEnd"),
    path('child_<int:child_id>/tales_<int:tale_id>/content_<int:content_id>', views.TaleContent.as_view(), name="TaleContent"),
    path('child_<int:child_id>/tales_<int:tale_id>/content_<int:content_id>/upload', views.TaleUpload.as_view(),
         name="TaleUpload"),
]