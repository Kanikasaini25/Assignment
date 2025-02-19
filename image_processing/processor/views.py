from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import csv
import uuid
from .models import Request, Product
from .tasks import process_images

@csrf_exempt
def upload_csv(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        reader = csv.DictReader(file.read().decode('utf-8').splitlines())
        request_id = str(uuid.uuid4())
        Request.objects.create(request_id=request_id)
        for row in reader:
            Product.objects.create(
                serial_number=row['Serial Number'],
                product_name=row['Product Name'],
                input_image_urls=row['Input Image Urls'],
                request_id=request_id
            )
        process_images.delay(request_id)
        return JsonResponse({"request_id": request_id})
    return JsonResponse({"error": "Invalid request"}, status=400)

def check_status(request, request_id):
    request_obj = get_object_or_404(Request, request_id=request_id)
    products = Product.objects.filter(request=request_obj)
    output = {
        "status": request_obj.status,
        "products": [
            {
                "product_name": product.product_name,
                "output_image_urls": product.output_image_urls
            }
            for product in products
        ]
    }
    return JsonResponse(output)