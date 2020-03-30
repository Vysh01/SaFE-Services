from django.urls import path, include, re_path
from rest_framework.authtoken.views import obtain_auth_token

from .views import *

urlpatterns = [
    path('login/', obtain_auth_token),
    path('getreports/', GetReportGen.as_view()),
    path('getqueries/', GetQueries.as_view()),
    path('getallmigrants/', GetAllMigrants.as_view()),
    path('getallhelpers/', GetAllHelpers.as_view()),
    path('getredflagquestions/', GetRedflagQuestions.as_view()),
    path('exportmigrants/', ExportMigrants.as_view()),
    path('exporthelpers/', ExportHelpers.as_view()),
    path('exportunexportedmigrants/', ExportUnexportedMigrants.as_view()),
    path('exportunexportedhelpers/', ExportUnexportedHelpers.as_view()),
    path('exportredflaggmigrants/', ExportRedflagUsers.as_view()),
    path('exportmigqueries/', ExportUserQueries.as_view()),
    path('exportunansweredqueries/', ExportUnansweredUserQueries.as_view()),
    path('exportmigresponses/', ExportMigrantResponses.as_view()),
    re_path(r'^getresponses/$', GetUserResponses.as_view()),
    re_path(r'^getredflagusers/(?P<question>\d+)$', GetRedflagUsers.as_view()),
    re_path(r'^followedback/(?P<queryid>\d+)$', FollowedQuery.as_view()),
    path('followedmigrant/', FollowedMigrant.as_view()),
    path('getallresponses/', GetAllResponses.as_view()),
    re_path(r'^search/$', GetUserByQuery.as_view()),
    re_path(r'^getusersbypercent/$', GetUsersByPercent.as_view()),
    re_path(r'^getusersbycountry/$', GetUsersByCountry.as_view()),
]
