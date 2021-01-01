from django.urls import path
from . import views as portfolio_views

urlpatterns = [
    path('', portfolio_views.about, name='about'),
    path('mypage/', portfolio_views.mypage, name='mypage'),
]
