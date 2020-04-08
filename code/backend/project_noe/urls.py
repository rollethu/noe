"""project_noe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import include, path
from django.http import HttpResponse
from rest_framework.routers import DefaultRouter

import surveys.views


api_router = DefaultRouter()
api_router.register("survey-questions", surveys.views.SurveyQuestionViewSet)
api_router.register("survey-answers", surveys.views.SurveyAnswerViewSet)


# Just added this quickly, feel free to redo it properly.
def healthcheck(req):
    msg = f"Ok!"
    return HttpResponse(msg, content_type="text/plain")


urlpatterns = [
    path("api", include(api_router.urls)),
    path("admin/", admin.site.urls),
    path("health/", healthcheck),
]
