from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.urls import reverse


class User(AbstractUser):
    pass

class List(models.Model):
    title = models.CharField(max_length=23)
    #list_id = models.AutoField(primary_key=True)
    description = models.TextField(max_length=300)
    starting_bid = models.IntegerField(default=0)
    #final_bid = models.IntegerField(default=0, blank=True)
    category = models.CharField(max_length=23)
    image = models.ImageField(upload_to='auction_pics', default='default.jpeg', blank=True)
    user = models.CharField(max_length=23, default="user")
    date_created = models.DateTimeField(default=timezone.now)
    final_buyer = models.CharField(max_length=23, blank=True)
    available = models.BooleanField(default=True,null=True)
    
    
    def __str__(self):
        return f"{self.title}"
    
class WatchList(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE, blank=True)
    #id = models.AutoField(primary_key=True)
    buyer = models.CharField(max_length=23, default="hello")
    taken = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.list.title}"
    
class Bid(models.Model):
    bid_item = models.ForeignKey(List, on_delete=models.CASCADE)
    starting_bid = models.IntegerField(default=0)
    current_bid = models.IntegerField(default=0)
    bidder = models.CharField(max_length=23, default="user")
    
    def __str__(self):
        return f"Bid for {self.bid_item.title}"
    
class Comment(models.Model):
    comment_item = models.ForeignKey(List, on_delete=models.CASCADE)
    the_comment = models.TextField(max_length=100)
    author = models.CharField(max_length=23, default="user")

    def __str__(self):
        return f"Comment for {self.comment_item.title}"