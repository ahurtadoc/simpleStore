from django.db import models


# Create your models here.

class Orders(models.Model):
    customer_name = models.CharField(max_length=80)
    customer_email = models.CharField(max_length=120)
    customer_mobile = models.CharField(max_length=40)
    status = models.CharField(max_length=20)
    process_url = models.CharField(max_length=150, null=True)
    session_id = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
