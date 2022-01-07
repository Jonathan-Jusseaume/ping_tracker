"""ping_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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

import ping.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ping.views.login_view),
    path('logout', ping.views.logout_view),
    path('check-connexion', ping.views.check_connexion),
    path('dashboard', ping.views.main),
    path('notes', ping.views.notes),
    path('match', ping.views.match),
    path('add-notes', ping.views.add_notes),
    path('submit-match', ping.views.submit_match),
    path('historique', ping.views.history),
]
