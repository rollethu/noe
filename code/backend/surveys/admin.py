from django.contrib import admin

from . import models as m


admin.site.register(m.SurveyQuestion)
admin.site.register(m.SurveyAnswer)