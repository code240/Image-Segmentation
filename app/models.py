from pyexpat import model
from django.db import models

# Create your models here.
class Admindata(models.Model):
    id = models.AutoField
    useremail = models.CharField(max_length=100)
    userps = models.CharField(max_length=100)

class Article(models.Model):
    data_id = models.AutoField
    heading = models.CharField(max_length=200)
    source = models.CharField(max_length=50)
    content = models.TextField()
    date = models.CharField(max_length=50)
    article_id = models.CharField(max_length=100)

class Media(models.Model):
    data_id = models.AutoField
    img1 = models.ImageField(upload_to = "./Templates/ArticleImages")
    article_id = models.CharField(max_length=100)
    img_count = models.IntegerField()
    
class Segment(models.Model):
    data_id = models.AutoField
    img = models.ImageField(upload_to = "./Templates/Segment/input")
    img_id = models.CharField(max_length=100)
    