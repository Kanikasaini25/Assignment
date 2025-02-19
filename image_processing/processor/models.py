from django.db import models

class Request(models.Model):
    request_id= models.CharField(max_length=50, primary_key=True)
    status = models.CharField(max_length=20, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.request_id

class Product(models.Model):
    serial_number = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=100)
    input_image_urls = models.TextField()
    output_image_urls = models.TextField(blank=True, null=True)
    request = models.ForeignKey(Request, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name