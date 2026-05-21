import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Products , Orders
from .webhook import send_webhook  


@csrf_exempt
def create_product(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    body = json.loads(request.body)
    product = Products.objects.create(name=body['name'])

    send_webhook('product.created', {   
        'product_id': product.id,
        'name': product.name,
    })

    return JsonResponse({'product_id': product.id, 'name': product.name})


@csrf_exempt
def create_order(request):
    if request.method != "POST":
        return JsonResponse({'error': 'POST required'}, status=405)

    body = json.loads(request.body)

    product = Products.objects.get(name=body['name'])

    order = Orders.objects.create(
        product=product,
        quantity=body['quantity']
    )

    send_webhook('order.created', {
        'order_id': order.id,
        'product': product.name,
        'quantity': order.quantity,
    })

    return JsonResponse({
        'order_id': order.id,'product': product.name,'quantity': order.quantity,
    })