from django.contrib import admin

from . import models as m


class SurveyQuestionAdmin(admin.ModelAdmin):
    list_display = ["question", "answer_datatype", "is_required", "is_active"]


admin.site.register(m.SurveyQuestion, SurveyQuestionAdmin)
admin.site.register(m.SurveyAnswer)
