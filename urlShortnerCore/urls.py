from django.contrib import admin
from django.urls import path
from .views import loginView
from .views import signupView
from .views import urlShortnerView
from .views import shortToOriginalView
from .views import urlsHistoryView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', loginView, name='login'),
    path('signup/',signupView, name='signup'),
    path('shorten/', urlShortnerView, name='urlShortner'),
    path('s/<str:path>/',shortToOriginalView, name='shortToOriginal'),
    path('urlsHistory/<int:userId>/',urlsHistoryView, name='urlsHistory')
]