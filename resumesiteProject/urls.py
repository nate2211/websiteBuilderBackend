"""
URL configuration for resumesiteProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter


from accounts.views import AccountListView, AccountDetailView, AccountCreateView, LoginView, AccountImageViewSet, \
    AccountUpdateView
from layouts.views import create_layout


urlpatterns = [
    path('api/create_layout/', create_layout, name='create_layout'),
    path('account/update/<int:pk>/', AccountUpdateView.as_view(), name='account-update'),
    path('api/account-images-view/', AccountImageViewSet.as_view({'get': 'list', 'post': 'create'}),
                       name='account-image-view'),
    path('api/account-images-view/<int:pk>/', AccountImageViewSet.as_view({
      'get': 'retrieve',  # To retrieve a single account image
      'delete': 'destroy'  # To delete a single account image
    }), name='account-image-detail'),
    path('api/signup/', AccountCreateView.as_view(), name='signup'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('accounts/', AccountListView.as_view(), name='account-list'),
    path('accounts/<int:pk>/', AccountDetailView.as_view(), name='account-detail'),
    path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
