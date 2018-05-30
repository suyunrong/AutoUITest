"""AutoUITest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('add_project/', views.add_project, name='add_project'),
    path('project_list/<int:id>/', views.project_list, name='project_list'),
    path('add_module/', views.add_module, name='add_module'),
    path('module_list/<int:id>/', views.module_list, name='module_list'),
    path('add_case/', views.add_case, name='add_case'),
    path('choose/', views.choose, name='choose'),
    path('case_list/<int:id>/', views.case_list, name='case_list'),
    path('edit_case/<int:id>/', views.edit_case, name='edit_case_list'),
    path('edit_case/', views.edit_case, name='edit_case'),
    path('add_env/', views.add_env, name='add_env'),
    path('env_list/<int:id>', views.env_list, name='env_list'),
]
