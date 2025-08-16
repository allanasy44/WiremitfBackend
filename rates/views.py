from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .models import Rate
from .serializers import RateSerializer
from .tasks import refresh_rates_task
from rest_framework.pagination import PageNumberPagination
class LatestRatesView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get(self, request):
        qs = Rate.objects.order_by('pair','-timestamp').distinct('pair').order_by('-timestamp')
        serializer = RateSerializer(qs, many=True)
        return Response(serializer.data)
class RateDetailView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get(self, request, currency):
        qs = Rate.objects.filter(pair__icontains=currency.upper()).order_by('-timestamp')[:10]
        serializer = RateSerializer(qs, many=True)
        return Response(serializer.data)
class HistoricalRatesView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get(self, request):
        pair = request.query_params.get('pair')
        qs = Rate.objects.all()
        if pair: qs=qs.filter(pair=pair)
        qs=qs.order_by('-timestamp')
        paginator=PageNumberPagination(); page=paginator.paginate_queryset(qs, request, view=self)
        serializer=RateSerializer(page, many=True); return paginator.get_paginated_response(serializer.data)
class AdminRefreshView(APIView):
    permission_classes=[permissions.IsAdminUser]
    def post(self, request):
        task = refresh_rates_task.delay(); return Response({'task_id':task.id,'status':'scheduled'})
