from django.db.models import Count, F, Q
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from apis.models import *
from apis.serializers import *


class GetReportGen(APIView):
    def get(self, request):
        detail_query_set = UserTbl.objects.all()
        response_query_set = ResponseTbl.objects.all()
        # age_groups = UsersSerializer(detail_query_set.annotate(age_groups=Count('user_age')).values('age_groups'), many=True)
        age_groups = detail_query_set.values('user_age').annotate(count=Count('user_age')).order_by('user_age')
        gender_groups = detail_query_set.values('user_sex').annotate(count=Count('user_sex'))
        user_types = detail_query_set.values('user_type').annotate(count=Count('user_type'))
        location_group = detail_query_set.values('current_country').annotate(count=Count('current_country'))
        percentages = detail_query_set.values('percent_comp').annotate(count=Count('percent_comp'))
        reg_dates = detail_query_set.values('percent_comp').annotate(count=Count('percent_comp'))
        redflags = response_query_set.values('question_id').annotate(
            question__question_step=F('question__question_step_en')).filter(
            is_error='true').annotate(count=Count('question_id'))
        return Response(
            {'genders': gender_groups, 'ages': age_groups, 'user_types': user_types, 'locations': location_group,
             'percentages': percentages, 'regflags': redflags},
            status.HTTP_200_OK)


class GetAllMigrants(ListAPIView):
    serializer_class = UsersSerializer
    queryset = UserTbl.objects.filter(user_type='migrant')
    pagination_class = LimitOffsetPagination


class GetQueries(ListAPIView):
    serializer_class = ResponseSerializer

    def get(self, request, *args, **kwargs):
        mig_list = ResponseTbl.objects.exclude(question_query__exact='').values('user_id').annotate(
            user_name=F('user__user_name'), user_sex=F('user__user_sex'), user_phone=F('user__user_phone'),
            user_age=F('user__user_age'), percent_comp=F('user__percent_comp'), user_type=F('user__user_type'),
            current_country=F('user__current_country'), registered_country=F('user__registered_country'),
            last_active=F('user__last_active'), parent_id=F('user__parent_id'),
            counts=Count('user_id'))
        all_data = []
        for mig in mig_list:
            mig_dict = {}
            queryset = ResponseTbl.objects.annotate(question_title=F('question__question_step_en')).values(
                'question_title',
                'response',
                'is_error',
                'question_query',
                'response_time').filter(
                user_id=mig['user_id']).exclude(question_query__exact='').order_by('tile_id')
            mig_dict['queries'] = queryset
            mig_dict['user_details'] = mig
            all_data.append(mig_dict)
        return Response({'data': all_data})


class GetAllHelpers(ListAPIView):
    serializer_class = UsersSerializer
    queryset = UserTbl.objects.filter(user_type='helper')
    pagination_class = LimitOffsetPagination


class GetAllHelpers(ListAPIView):
    serializer_class = UsersSerializer
    queryset = UserTbl.objects.filter(user_type='helper')
    pagination_class = LimitOffsetPagination


# Getting User Responses
class GetUserResponses(ListAPIView):
    serializer_class = ResponseSerializer

    def get(self, request):
        queryset = ResponseTbl.objects.annotate(question_title=F('question__question_step_en')).values('question',
                                                                                                       'question_title',
                                                                                                       'response',
                                                                                                       'is_error',
                                                                                                       'tile_id',
                                                                                                       'question__response_type',
                                                                                                       'tile__tile_title',
                                                                                                       'question_query',
                                                                                                       'response_time').filter(
            user_id=self.request.GET['migrant']).order_by('tile_id')
        for index, dict in enumerate(queryset):
            if dict['question__response_type'] == 0:
                queryset[index]['response'] = ''
            elif dict['response'] == 'true':
                options = OptionsTbl.objects.filter(questions_tbl_question__question_id=dict['question']).values(
                    'option_text')
                queryset[index]['response'] = options[0]['option_text']
            elif dict['response'] == 'false':
                options = OptionsTbl.objects.filter(questions_tbl_question__question_id=dict['question']).values(
                    'option_text')
                queryset[index]['response'] = options[1]['option_text']
        return Response({'data': queryset})


# Get Redflags
class GetRedflagQuestions(ListAPIView):
    serializer_class = QuestionsSerializer

    def get_queryset(self):
        return QuestionsTbl.objects.values('question_id').annotate(question_step=F('question_step_en'),
                                                                   question_description=F(
                                                                       'question_description_en')).filter(
            Q(question_condition__contains='error') | Q(response_type=4)).order_by('tiles_tbl_tile')


class GetRedflagUsers(ListAPIView):
    serializer_class = TestSerializer

    def get(self, request, *args, **kwargs):
        queryset = ResponseTbl.objects.filter(question_id=self.kwargs['question'], is_error = 'true ').values('user_id').annotate(
            user_name=F('user__user_name'), user_sex=F('user__user_sex'), user_phone=F('user__user_phone'),
            user_age=F('user__user_age'), percent_comp=F('user__percent_comp'), user_type=F('user__user_type'),
            current_country=F('user__current_country'), registered_country=F('user__registered_country'),
            last_active=F('user__last_active'), parent_id=F('user__parent_id'),
            counts=Count('user_id'))
        return Response({'data': queryset})


# Get Migrants By Percent
class GetUsersByPercent(ListAPIView):
    serializer_class = UsersSerializer

    def get_queryset(self):
        return UserTbl.objects.filter(percent_comp__gte=self.request.GET['percent_min'],
                                      percent_comp__lte=self.request.GET['percent_max'])


# Get Users by Dest & Current Country
class GetUsersByCountry(ListAPIView):
    serializer_class = UsersSerializer

    def get_queryset(self):
        destination = self.request.GET['destination']
        current = self.request.GET['current']
        if current == 'any':
            return ResponseTbl.objects.filter(response_variable='mg_destination',
                                              response__contains=destination).values('user_id').annotate(
                user_name=F('user__user_name'), user_sex=F('user__user_sex'), user_phone=F('user__user_phone'),
                user_age=F('user__user_age'), percent_comp=F('user__percent_comp'), user_type=F('user__user_type'),
                current_country=F('user__current_country'), registered_country=F('user__registered_country'),
                last_active=F('user__last_active'), parent_id=F('user__parent_id'))
        elif destination == 'any':
            return ResponseTbl.objects.filter(user__current_country__contains=current).values('user_id').annotate(
                user_name=F('user__user_name'), user_sex=F('user__user_sex'), user_phone=F('user__user_phone'),
                user_age=F('user__user_age'), percent_comp=F('user__percent_comp'), user_type=F('user__user_type'),
                current_country=F('user__current_country'), registered_country=F('user__registered_country'),
                last_active=F('user__last_active'), parent_id=F('user__parent_id'))
        else:
            return ResponseTbl.objects.filter(response_variable='mg_destination', response__contains=destination,
                                              user__current_country__contains=current)


# Searching by Name or Number
class GetUserByQuery(ListAPIView):
    serializer_class = UsersSerializer

    def get_queryset(self):
        return UserTbl.objects.filter(
            Q(user_name__icontains=self.request.GET['query']) | Q(user_phone__icontains=self.request.GET['query']))
