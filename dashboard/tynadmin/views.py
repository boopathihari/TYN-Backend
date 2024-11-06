from django.db.models import Count, Q,Avg,Sum
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import EnterpriseUser,UserPersona , Startup
from .serializers import IndustryAcceptedInvitedCountSerializer, StatusCountSerializer, UserPersonaCountSerializer,StartupCategorySerializer
from django.db import connection
from rest_framework import status

class IndustryAcceptedInvitedCountView(APIView):
    def get(self, request):
        data = (
            EnterpriseUser.objects
            .values('industry')
            .annotate(
                accepted_count=Count('enterprise_user_id', filter=Q(accepted=True)),
                invited_count=Count('enterprise_user_id', filter=Q(invited=True))
            )
            .order_by('industry')
        )
        
        serializer = IndustryAcceptedInvitedCountSerializer(data, many=True)
        return Response(serializer.data)
    

class StatusCountView(APIView):
    def get(self, request):
        # Aggregate data by status (e.g., Active, Inactive)
        data = (
            EnterpriseUser.objects
            .values('status')
            .annotate(count=Count('enterprise_user_id'))
            .order_by('status')
        )
        
        # Serialize the data
        serializer = StatusCountSerializer(data, many=True)
        return Response(serializer.data)


class UserPersonaCountView(APIView):
    def get(self, request):
        data = UserPersona.objects.values('user_type', 'count')
        
        serializer = UserPersonaCountSerializer(data, many=True)
        return Response(serializer.data)



class SessionCountAPI(APIView):
    def get(self, request):
        # Define the SQL query
        query = """
            SELECT 
                CASE
                    WHEN EXTRACT(QUARTER FROM s.session_date) = 1 THEN 'Q1'
                    WHEN EXTRACT(QUARTER FROM s.session_date) = 2 THEN 'Q2'
                    WHEN EXTRACT(QUARTER FROM s.session_date) = 3 THEN 'Q3'
                    WHEN EXTRACT(QUARTER FROM s.session_date) = 4 THEN 'Q4'
                END AS quadrant,
                CASE
                    WHEN s.enterpriseuser_id IS NOT NULL THEN 'Enterprise'
                    ELSE 'Startup'
                END AS user_type,
                COUNT(s.session_id) AS session_count
            FROM session s
            LEFT JOIN enterpriseuser eu ON s.enterpriseuser_id = eu.enterprise_user_id
            LEFT JOIN startup st ON s.startup_id = st.startup_id
            GROUP BY 
                CASE
                    WHEN EXTRACT(QUARTER FROM s.session_date) = 1 THEN 'Q1'
                    WHEN EXTRACT(QUARTER FROM s.session_date) = 2 THEN 'Q2'
                    WHEN EXTRACT(QUARTER FROM s.session_date) = 3 THEN 'Q3'
                    WHEN EXTRACT(QUARTER FROM s.session_date) = 4 THEN 'Q4'
                END,
                CASE
                    WHEN s.enterpriseuser_id IS NOT NULL THEN 'Enterprise'
                    ELSE 'Startup'
                END
            ORDER BY quadrant, user_type;
        """
        
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

        response_data = []
        for row in results:
            response_data.append({
                'quadrant': row[0],
                'user_type': row[1],
                'session_count': row[2],
            })

        return Response(response_data, status=status.HTTP_200_OK)


class AverageResponseTimeView(APIView):
    def get(self, request, *args, **kwargs):
        # Calculate the average response time and round to 2 decimal places
        overall_avg_response_time = Startup.objects.aggregate(
            avg_response_time=Avg('average_response_time')
        )['avg_response_time']

        # Round to 2 decimal places
        overall_avg_response_time_rounded = round(overall_avg_response_time, 2) if overall_avg_response_time else 0

        return Response({
            "overall_avg_response_time": overall_avg_response_time_rounded
        })


class StartupCategoryStatsAPIView(APIView):
    def get(self, request):
        categories = Startup.objects.values('category').distinct()

        result = []
        for category in categories:
            total_startups = Startup.objects.filter(category=category['category']).count()
            verified_startups = Startup.objects.filter(
                category=category['category'], is_verified=True).count()

            result.append({
                'category': category['category'],
                'total_startups': total_startups,
                'verified_startups': verified_startups
            })

        # Serialize the data
        serializer = StartupCategorySerializer(result, many=True)

        # Return the response
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class TotalConversionRateView(APIView):
    def get(self, request, *args, **kwargs):
        # Aggregate the total values
        total_queries = Startup.objects.aggregate(Sum('query_count'))['query_count__sum'] or 0
        total_poc_accepted = Startup.objects.aggregate(Sum('poc_accepted'))['poc_accepted__sum'] or 0
        total_poc_delivered = Startup.objects.aggregate(Sum('poc_delivered'))['poc_delivered__sum'] or 0

      
        return Response({
            "total_queries": total_queries,
            "total_poc_accepted": total_poc_accepted,
            "total_poc_delivered": total_poc_delivered,
        }, status=status.HTTP_200_OK)

    