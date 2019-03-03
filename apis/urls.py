from django.urls import path, include, re_path
from rest_framework.authtoken.views import obtain_auth_token

from .views import *

urlpatterns = [
    path('login/', obtain_auth_token),
    path('getreports/', GetReportGen.as_view()),
    path('getallmigrants/', GetAllMigrants.as_view()),
    path('getallhelpers/', GetAllHelpers.as_view()),
    path('getredflagquestions/', GetRedflagQuestions.as_view()),
    re_path(r'^getresponses/(?P<migrant>\d+)$', GetUserResponses.as_view()),
    re_path(r'^getredflagusers/(?P<question>\d+)$', GetRedflagUsers.as_view()),
    re_path(r'^getusersbypercent/$', GetUsersByPercent.as_view()),
    re_path(r'^getusersbycountry/$', GetUsersByCountry.as_view()),
]
