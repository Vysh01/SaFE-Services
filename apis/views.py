import csv
from datetime import datetime

from django.db.models import Count, F, Q
# Create your views here.
from django.db.models.functions import Length
from django.http import HttpResponse

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from apis.models import *
from apis.serializers import *


class GetReportGen(APIView):
    def get(self, request):
        detail_query_set = UserSafeTbl.objects.filter(user_type='migrant')
        response_query_set = ResponseTbl.objects.all()
        # age_groups = UsersSerializer(detail_query_set.annotate(age_groups=Count('user_age')).values('age_groups'), many=True)
        age_groups = detail_query_set.exclude(user_age__contains=0).values('user_age').annotate(
            count=Count('user_age')).order_by('user_age')
        gender_groups = detail_query_set.exclude(user_sex__exact='').values('user_sex').annotate(
            count=Count('user_sex'))
        user_types = detail_query_set.exclude(user_type=None).values('user_type').annotate(count=Count('user_type'))
        location_group = detail_query_set.values('current_country').annotate(count=Count('current_country'))
        percentages = detail_query_set.exclude(percent_comp=None).values('percent_comp').annotate(
            count=Count('percent_comp'))
        reg_dates = detail_query_set.values('percent_comp').annotate(count=Count('percent_comp'))
        redflags = response_query_set.values('question_id').annotate(
            question__question_step=F('question__question_step_en')).filter(
            is_error='true').annotate(count=Count('question_id'))
        return Response(
            {'genders': gender_groups, 'ages': age_groups, 'user_types': user_types, 'locations': location_group,
             'percentages': percentages, 'regflags': redflags},
            status.HTTP_200_OK)


class GetAllMigrants(ListAPIView):
    pagination_class = LimitOffsetPagination

    def get(self, request):
        # queryset = ResponseTbl.objects.filter(user__user_type='migrant').annotate(
        #     registered_country=F('user__registered_country'))
        users = UserSafeTbl.objects.filter(user_type='migrant')
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(users, request)
        for user in page:
            registered_country = 'Not Selected'
            try:
                registered_country = user.responses.get(response_variable='mg_destination').response
                registered_country = CountriesTbl.objects.get(country_id=registered_country).country_name_en
            except:
                pass
            user.registered_country = registered_country
        serializer = UsersSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


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
                'id',
                'question_title',
                'response',
                'is_error',
                'query_followback',
                'question_query',
                'response_time').filter(
                user_id=mig['user_id']).exclude(question_query__exact='').order_by('tile_id')
            mig_dict['queries'] = queryset
            mig_dict['user_details'] = mig
            all_data.append(mig_dict)
        return Response({'data': all_data})


class GetAllHelpers(ListAPIView):
    serializer_class = UsersSerializer
    queryset = UserSafeTbl.objects.filter(user_type='helper')
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
            user_id=self.request.GET['migrant']).exclude(response_variable__contains='percent_comp').order_by('tile_id')
        for index, dict in enumerate(queryset):
            try:
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
            except:
                pass
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
        queryset = ResponseTbl.objects.filter(question_id=self.kwargs['question'], is_error='true').values(
            'user_id').annotate(
            user_name=F('user__user_name'), user_sex=F('user__user_sex'), user_phone=F('user__user_phone'),
            user_age=F('user__user_age'), percent_comp=F('user__percent_comp'), user_type=F('user__user_type'),
            current_country=F('user__current_country'), registered_country=F('user__registered_country'),
            last_active=F('user__last_active'), parent_id=F('user__parent_id'),
            counts=Count('user_id'))
        return Response({'data': queryset})


class ExportRedflagUsers(APIView):
    def get(self, request):
        queryset = ResponseTbl.objects.filter(is_error='true').values(
            'question', 'response', 'question_query').annotate(
            user_name=F('user__user_name'), user_sex=F('user__user_sex'), user_phone=F('user__user_phone'),
            user_age=F('user__user_age'), percent_comp=F('user__percent_comp'),
            current_country=F('user__current_country'), registered_country=F('user__registered_country'))

        serializer = ExportRedflagMigrantSerializer(queryset, many=True)

        headers = ['question', 'response', 'question_query', 'user_name', 'user_sex', 'user_phone', 'user_age',
                   'percent_comp', 'current_country',
                   'registered_country']
        today = datetime.today()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="SaFE-Migrants-Redflags-{}.csv"'.format(today)

        writer = csv.DictWriter(response, fieldnames=headers)
        writer.writeheader()
        for row in serializer.data:
            writer.writerow(row)
        return response


class ExportMigrants(ListAPIView):
    def get(self, request):
        users = UserSafeTbl.objects.filter(user_type='migrant')
        users.update(exported=2)
        for user in users:
            user.save()

        serializer = ExportMigrantSerializer(users.values('user_name', 'user_phone', 'user_sex',
                                                          'user_age',
                                                          'percent_comp', 'current_country',
                                                          'registered_country'), many=True)

        headers = ['user_name', 'user_phone', 'user_sex', 'user_age', 'percent_comp', 'current_country',
                   'registered_country']
        today = datetime.today()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="SaFE-Migrants-{}.csv"'.format(today)

        writer = csv.DictWriter(response, fieldnames=headers)
        writer.writeheader()
        for row in serializer.data:
            writer.writerow(row)
        return response


class ExportUnexportedMigrants(ListAPIView):
    def get(self, request):
        users = UserSafeTbl.objects.filter(user_type='migrant', exported=1)
        serializer = ExportMigrantSerializer(users.values('user_name', 'user_phone', 'user_sex',
                                                          'user_age',
                                                          'percent_comp', 'current_country',
                                                          'registered_country'), many=True)

        headers = ['user_name', 'user_phone', 'user_sex', 'user_age', 'percent_comp', 'current_country',
                   'registered_country']
        today = datetime.today()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="SaFE-Migrants-{}.csv"'.format(today)

        writer = csv.DictWriter(response, fieldnames=headers)
        writer.writeheader()
        for row in serializer.data:
            writer.writerow(row)
        users.update(exported=2)
        for user in users:
            user.save()
        return response


class ExportUserQueries(APIView):
    def get(self, request):
        queryset = ResponseTbl.objects.values(
            'user_id', 'question', 'response', 'question_query').annotate(query_len=Length('question_query'),
                                                                          user_name=F('user__user_name'),
                                                                          user_sex=F('user__user_sex'),
                                                                          user_phone=F('user__user_phone'),
                                                                          user_age=F(
                                                                              'user__user_age'),
                                                                          percent_comp=F('user__percent_comp'),
                                                                          current_country=F('user__current_country'),
                                                                          registered_country=F(
                                                                              'user__registered_country')).filter(
            query_len__gte=5)

        serializer = ExportRedflagMigrantSerializer(queryset, many=True)

        headers = ['question', 'response', 'question_query', 'user_name', 'user_sex', 'user_phone', 'user_age',
                   'percent_comp', 'current_country',
                   'registered_country']
        today = datetime.today()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="SaFE-Migrants-Queries-{}.csv"'.format(today)

        writer = csv.DictWriter(response, fieldnames=headers)
        writer.writeheader()
        for row in serializer.data:
            writer.writerow(row)
        return response


class ExportMigrantResponses(APIView):
    def get(self, request):
        queryset = ResponseTbl.objects.values(
            'user_id', 'question', 'response', 'question_query').annotate(query_len=Length('question_query'),
                                                                          user_name=F('user__user_name'),
                                                                          user_sex=F('user__user_sex'),
                                                                          user_phone=F('user__user_phone'),
                                                                          user_age=F(
                                                                              'user__user_age'),
                                                                          percent_comp=F('user__percent_comp'),
                                                                          current_country=F('user__current_country'),
                                                                          registered_country=F(
                                                                              'user__registered_country'))

        serializer = ExportRedflagMigrantSerializer(queryset, many=True)

        headers = ['question', 'response', 'question_query', 'user_name', 'user_sex', 'user_phone', 'user_age',
                   'percent_comp', 'current_country',
                   'registered_country']
        today = datetime.today()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="SaFE-Migrants-Queries-{}.csv"'.format(today)

        writer = csv.DictWriter(response, fieldnames=headers)
        writer.writeheader()
        for row in serializer.data:
            writer.writerow(row)
        return response


class FollowedQuery(APIView):
    serializer_class = TestSerializer

    def get(self, request, *args, **kwargs):
        response = ResponseTbl.objects.get(id=self.kwargs['queryid'])
        response.query_followback = 'yes'
        response.save()
        return Response({'data': 'Status Saved'})


# Get Migrants By Percent
class GetUsersByPercent(ListAPIView):
    serializer_class = UsersSerializer

    def get_queryset(self):
        return UserSafeTbl.objects.filter(percent_comp__gte=self.request.GET['percent_min'],
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
        return UserSafeTbl.objects.filter(
            Q(user_name__icontains=self.request.GET['query']) | Q(user_phone__icontains=self.request.GET['query']))
