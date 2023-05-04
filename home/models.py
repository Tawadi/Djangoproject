from django.db import models
from django.contrib.auth.models import User
import uuid 


class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4 , editable=False,primary_key=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)

    class meta:
        abstract=True

class medicinecategory(BaseModel):
    category_name = models.CharField(max_length=100)

class medicines(BaseModel):
    category=models.ForeignKey(medicinecategory, on_delete=models.CASCADE,related_name="medicines")
    medicine_name=models.CharField(max_length=100)
    price=models.IntegerField(default=100)
    images=models.ImageField(upload_to='medicine')   

class Carts(BaseModel): 
    user=models.ForeignKey(User, null=True, blank=True , on_delete=models.SET_NULL, related_name="carts")
    is_paid=models.BooleanField(default=False)
    instamojo_id = models.CharField(max_length=1000)

    def get_cart_total(self):
        cart_items = CartItems.objects.filter(cart=self)
        total = sum([item.medicine.price for item in cart_items])
        return total

    # def get_cart_total(self ):
    #     return CartItems.objects.filter(carts = self).aggregate(Sum('medicine__price'))['medicine__price_sum']

class CartItems(BaseModel):
    cart=models.ForeignKey(Carts, on_delete=models.CASCADE ,related_name="cart_items") 
    medicine=models.ForeignKey(medicines, on_delete=models.CASCADE)  

 