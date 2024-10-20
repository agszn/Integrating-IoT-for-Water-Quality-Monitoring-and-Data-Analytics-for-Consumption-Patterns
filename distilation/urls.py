from unicodedata import name
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('predict_potability/',views.predict_potability, name='potential'),
    path('predict_potability_json/',views.predict_potability_json, name='predict_potability_json'),
    path('upload_json/',views.upload_json, name='upload_json'),
    path('read_sensor_data/',views.read_sensor_data, name='read_sensor_data'),
    
    

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
