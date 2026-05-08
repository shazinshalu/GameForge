from django.db import models
class User(models.Model):
    name = models.CharField(max_length=100)
    email=models.EmailField()
    password = models.CharField(max_length=10)
    address = models.CharField(max_length=200)
    phone=models.IntegerField()
    def __str__(self):
        return f"{self.name}"
# Create a model named Product.
class products(models.Model):
    name =models.CharField(max_length=150)  
    description =models.TextField() 
    price =models.DecimalField (max_digits=10,decimal_places=2)  
    quantity =models.IntegerField()  
    category =models.CharField (max_length=100)  
    image = models.ImageField(upload_to='products/') 
    created_at = models.DateTimeField (auto_now_add=True)
    def __str__(self):
        return f"{self.name}"
#create a product cart
class Cart(models.Model): 
    user=models.ForeignKey(User,on_delete=models.CASCADE) 
    product=models.ForeignKey(products,on_delete=models.CASCADE) 
    quantity = models.PositiveIntegerField(default=1) 
    created_at = models.DateTimeField(auto_now_add=True) 
    def __str__(self):
        return f"{self.user.name} - {self.product.name} (x{self.quantity})"
        
class wishlist(models.Model): 
    user=models.ForeignKey(User,on_delete=models.CASCADE) 
    product=models.ForeignKey(products,on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True) 
 
    def __str__(self): 
        return f"wishlist of {self.user.name}"
class Feedback(models.Model):
    RATING_CHOICES=[
        (1,'1'),
        (2,'2'),
        (3,'3'),
        (4,'4'),
        (5,'5'),
    ]
    feedback_text=models.TextField()
    rating=models.IntegerField(choices=RATING_CHOICES)
    created_at=models.DateTimeField(auto_now_add=True)
    email=models.EmailField()
    def __str__(self):
        return str(self.email)
        
