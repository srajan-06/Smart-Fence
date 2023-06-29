from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "stream_control"

urlpatterns = [
    path(" ",views.detect,name="detect"),
    path("detect_person/",views.detect_person,name="detect_person"),
    path("gotodetect/",views.gotodetect,name="gotodetect"),
    path("take_actions/",views.take_actions,name="take_actions")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)