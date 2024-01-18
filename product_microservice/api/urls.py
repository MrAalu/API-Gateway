from django.urls import path
from api.views import ProductView

urlpatterns = [path("", ProductView.as_view())]
