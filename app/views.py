from atexit import register
from random import random
from xml.etree.ElementTree import register_namespace
from django.http import HttpResponse
from django.shortcuts import render 
from markupsafe import Markup
import mysql.connector
from time import gmtime, strftime

import numpy as np
from numpy import append
from app.models import Admindata
from .models import *
from .complex import *
# Image editing
import os
from PIL import Image,ImageEnhance

import cv2
from skimage import data
from skimage.color import rgb2gray, rgb2hsv
import matplotlib.pyplot as plt 
# Create your views here.


    
def home(request):
    getData = list(Article.objects.values("heading","article_id"))
    # print(getData)
    allData = []
    topData = []
    # print(topData)
    
    if len(getData)<4:
        topData = getData
    else:
        for i in range(0,3):
            topData.append(getData[i])

    if len(getData)>6:
        for i in range(0,len(getData)):
            allData.append(getData[i])
        return render(request,"index.html",{"articles":allData, "topData":topData})
    return render(request,"index.html",{"articles":getData, "topData":topData})

def documentation(request):
    getData = list(Article.objects.values("heading","article_id"))
    if "a" in request.GET:
        articleNeed = request.GET["a"]
        getArticle = list(Article.objects.filter(article_id = articleNeed))
        if len(getArticle) == 0:
            return HttpResponse("There is no such article exist")
        getArticle = getArticle[0]
        Article_Heading = getArticle.heading
        x = getArticle.content
        src = getArticle.source
        Article_date = getArticle.date
        articleBody = decodeMytags(Article_Heading,x,src,Article_date,articleNeed)
        if "error" in articleBody.keys():
            return HttpResponse("There is some error in this article")
        articleBody["sideData"] = getData
        # print(articleBody)
        return render(request,"Documentation.html",articleBody)
    else:
        getArticle = list(Article.objects.values())
        if len(getArticle) == 0:
            return HttpResponse("There is no article exist on website")
        getArticle = getArticle[0]
        Article_Heading = getArticle["heading"]
        x = getArticle["content"]
        articleNeed = getArticle["article_id"]
        src = getArticle["source"]
        Article_date = getArticle["date"]
        articleBody = decodeMytags(Article_Heading,x,src,Article_date,articleNeed)
        if "error" in articleBody.keys():
            return HttpResponse("There is some error in this article")
        articleBody["sideData"] = getData
        return render(request,"Documentation.html",articleBody)





def Uploadimg(request):
    if "yes" not in request.POST.keys():
        return HttpResponse("Invalid Access")
    code = "img"+strftime("%Y%m%d%H%M%S", gmtime())
    myImg = request.FILES["segment"]
    x = Segment(img = myImg, img_id = code)
    x.save()
    return render(request,"verify.html",{"segment_upload":True,"code":code})











def segmentation(request):
    if "img" not in request.GET.keys():
        return HttpResponse("Invalid inputs")
    code = request.GET["img"]
    img = list(Segment.objects.filter(img_id = code).values())
    myimg = img[0]["img"]
    myimg = myimg.split("/")
    myimg = myimg[-1]
    return render(request,"Segmentation.html",{"img":myimg,"code":code})

def segmenting(request):
    if "img" not in request.GET.keys():
            return HttpResponse("Invalid inputs")
    code = request.GET["img"]
    img = list(Segment.objects.filter(img_id = code).values())
    myimg = img[0]["img"]   
    imgName = myimg.split("/")
    imgName = imgName[-1]
    path = "./Templates/Segment/output/"
    newImg = path+imgName
    image = plt.imread(myimg)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pixel_vals = image.reshape((-1,3))
    pixel_vals = np.float32(pixel_vals)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.85)
    k = 3
    retval, labels, centers = cv2.kmeans(pixel_vals, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    segmented_data = centers[labels.flatten()]
    segmented_image = segmented_data.reshape((image.shape))
    plt.imsave(newImg,segmented_image)
    return render(request,"verify.html",{"img":code,"imgYes":True})

def output(request):
    if "img" not in request.GET.keys():
        return HttpResponse("Invalid inputs")
    code = request.GET["img"]
    img = list(Segment.objects.filter(img_id = code).values())
    myimg = img[0]["img"]
    myimg = myimg.split("/")
    myimg = myimg[-1]
    return render(request,"output.html",{"img":myimg,"code":code})







def test(request):
    x = "There is no data right now"
    # x = Admindata.objects.all()
    # print(type(x[0].userps))
    # registered_email = x
    datetime = "Article_"+strftime("%Y%m%d%H%M%S", gmtime())
    # print(datetime)
    arc = Media.objects.filter(article_id = "Article20220510091448I k").values()
    # print(arc)
    # print(showtime)
    # x = """<img src="{% static 'is1.png' %}" id="i1" alt="image">"""
    x = Markup(x)
    # Media.objects.filter(article_id = "Article20220508044730Whn").delete()
    if 'text' in request.GET:
        text = request.GET["text"]
        return render(request,"TestPage.html",{"data":text})
    return render(request,"TestPage.html",{"data":True,"img":"/static/segments.png"})



 # enhance processing
    # xx = ImageEnhance.Brightness(img1)
    # xx.enhance(1.1)
    # en2 = ImageEnhance.Color(img1)
    # en2.enhance(1.1)