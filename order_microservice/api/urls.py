from django.urls import path
from api.views import OrderView

urlpatterns = [path("", OrderView.as_view())]
