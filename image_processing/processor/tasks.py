import requests
from PIL import Image
from io import BytesIO
import boto3
from django.conf import settings
from .models import Product, Request
from celery import Celery

app = Celery('image_processing')


def process_image(image_url):
    # Download image
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    # Compress image
    img = img.convert('RGB')
    img.thumbnail((img.width // 2, img.height // 2))
    # Save to storage (e.g., AWS S3)
    s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY)
    buffer = BytesIO()
    img.save(buffer, format="JPEG", quality=50)
    buffer.seek(0)
    output_key = f"processed/{image_url.split('/')[-1]}"
    s3.upload_fileobj(buffer, settings.AWS_STORAGE_BUCKET_NAME, output_key)
    return f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{output_key}"

@app.task
def process_images(request_id):
    request = Request.objects.get(request_id=request_id)
    products = Product.objects.filter(request=request)
    for product in products:
        input_urls = product.input_image_urls.split(',')
        output_urls = []
        for url in input_urls:
            output_url = process_image(url.strip())
            output_urls.append(output_url)
        product.output_image_urls = ','.join(output_urls)
        product.save()
    request.status = "Completed"
    request.save()
    if settings.WEBHOOK_URL:
        requests.post(settings.WEBHOOK_URL, json={"request_id": request_id, "status": "Completed"})