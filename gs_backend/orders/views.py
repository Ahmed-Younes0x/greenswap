from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Order
from .serializers import OrderSerializer
from django.utils.timezone import now

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_orders(request):
    user = request.user

    received = Order.objects.filter(seller=user).order_by('-created_at')
    sent = Order.objects.filter(buyer=user).order_by('-created_at')
    completed = Order.objects.filter(status='completed', buyer=user) | Order.objects.filter(status='completed', seller=user)

    data = {
        'received': OrderSerializer(received, many=True).data,
        'sent': OrderSerializer(sent, many=True).data,
        'completed': OrderSerializer(completed.distinct(), many=True).data
    }

    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_order_status(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=404)

    if order.seller != request.user:
        return Response({'error': 'Permission denied'}, status=403)

    status_value = request.data.get('status')
    if status_value not in ['accepted', 'rejected', 'completed']:
        return Response({'error': 'Invalid status'}, status=400)

    order.status = status_value
    if status_value == 'completed':
        order.completed_at = now()

    order.save()
    return Response(OrderSerializer(order).data)
