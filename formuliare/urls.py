"""
URL configuration for formuliare project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from formulaire_app.views import after_submit, submit_recharge

urlpatterns = [
    path('', lambda request: redirect('formulaire/', permanent=False)),
    path('admin/', admin.site.urls),
    path('formulaire/',submit_recharge, name='submit-recharge'),
    path('after/', after_submit, name='after-submit'),
]
