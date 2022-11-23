from atexit import register
from platform import architecture
from random import random
from xml.etree.ElementTree import register_namespace
from django.http import HttpResponse
from django.shortcuts import render 
from markupsafe import Markup
import mysql.connector
from time import gmtime, strftime
from app.models import Admindata
from .models import *
from .complex import *
import os
from django.shortcuts import redirect
# Create your views here.





#    PANEL CODING
"""PANEL CODES HERE"""



def panel(request):
    if request.session.has_key('admin'):
        data = request.session['admin']
        getArticles = list(Article.objects.values())
        # getArticles = getArticles[0]
        dictionary = {}
        mylist = []
        for item in getArticles:
            dictionary["heading"] = item["heading"]
            # print(dictionary)
            dictionary["article_id"] = item["article_id"] 
            dictionary["para"] = getPanelPara(item["content"])
            mylist.append(dictionary.copy())
        # print(mylist)
        return render(request,"PanelHome.html",{"data":mylist,"user":data})
    return render(request,"Login.html")



def verify(request):
    email = request.POST["useremail"].lower()
    psw = request.POST["userps"]
    getRow = Admindata.objects.all()
    registered_email = (getRow[0].useremail).lower()
    registered_password = getRow[0].userps
    if email == registered_email:
        if psw == registered_password:
            request.session['admin'] = registered_email
            return render(request,"verify.html",{"success":True})
        else:
            return render(request,"verify.html",{"ps":True})
    else:
        return render(request,"verify.html",{"em":True})


def addpage(request):
    if not request.session.has_key('admin'):
        return redirect("/Panel")
    return render(request,"addarticle.html")

def getArticleId(x):
    code = "Article"+strftime("%Y%m%d%H%M%S", gmtime())
    code += x[0]+x[-3]+x[-2]
    return code


def SaveArticle(request):
    if not request.session.has_key('admin'):
        return redirect("/Panel")
    if 'formsubmit' not in request.POST.keys():
        return render(request,"addarticle.html")
    ArticleCode = getArticleId(request.POST["heading"])
    imageCount = 1 
    allkeys =  request.FILES.keys()
    allkeys = list(allkeys)
    for key in allkeys:
        myImage = request.FILES[key]
        AddImage = Media(img1 = myImage,article_id = ArticleCode,img_count = imageCount)
        AddImage.save()
        imageCount = imageCount+1
    ArticleHeading = request.POST["heading"]
    ArticleBody = request.POST["article"]
    Current_date = strftime("%d-%m-%Y", gmtime())
    AddArticle = Article(heading = ArticleHeading,source = "Google",content = ArticleBody,date = Current_date,article_id= ArticleCode)
    AddArticle.save()
    return render(request,"verify.html",{"DataSaved":True})






def EditArticle(request):
    if not request.session.has_key('admin'):
        return redirect("/Panel")
    if "a" not in request.GET.keys():
        return HttpResponse("Invalid input")
        # panel(request)
    else:
        article_id = request.GET["a"]
        # print(article_id)
        getArticle_details = list(Article.objects.filter(article_id = article_id).values())  
        if len(getArticle_details) == 0:
            return HttpResponse("There is no such article exist by this article code")
        getArticle_details = getArticle_details[0]
        return render(request,"editData.html",{"article_data":getArticle_details,"article_id":article_id})


def SaveEditedArticle(request):
    if not request.session.has_key('admin'):
        return redirect("/Panel")
    if 'formsubmit' not in request.POST.keys():
        return HttpResponse("Bad Request")
    article_id = request.POST["article_id"]
    html = """
            <title>
                Error
            </title>
            <h1>You cannot delete or update the from here.</h1>
            <h2> If you want to perform Delete, Update operations on image then you <br>
            have to use <a href="/Panel/UpdateImageSettings?a="""+article_id+"""">update images</a> button </h2>
            <button onclick="window.history.back();">Go back</button>
        """
    today = strftime("%d-%m-%Y", gmtime())
    article_heading = request.POST["heading"]
    article_content = request.POST["article"]
    # article_img_count = int(request.POST["imgcount"])
    all_images = list(Media.objects.filter(article_id=article_id).values())
    article_img_count = len(all_images)
    current_image_status = imgcounts(article_content)
    if article_img_count == current_image_status:
        Article.objects.filter(article_id=article_id).update(heading = article_heading,content = article_content,date = today)
        return render(request,"verify.html",{"updationTrue":True})
    if article_img_count > current_image_status:
        return HttpResponse(html)
    if article_img_count < current_image_status:
        bool = {"img1":False,"img2":False,"img3":False}
        old_article = Article.objects.filter(article_id = article_id).values()
        old_article = old_article[0]
        my_old_article = old_article["content"]

        if ("<img1>" not in my_old_article) and ("<img2>" not in my_old_article) and ("<img3>" not in my_old_article):
            if("<img1>" in article_content):
                bool["img1"] = True
                if("<img2>" in article_content):
                    bool["img2"] = True
                    if("<img3>" in article_content):
                        bool["img3"] = True
        if  ("<img1>" in my_old_article) and ("<img2>" not in my_old_article) and ("<img3>" not in my_old_article):
            if("<img1>" in article_content):
                bool["img1"] = False
                if("<img2>" in article_content):
                    bool["img2"] = True
                    if("<img3>" in article_content):
                        bool["img3"] = True

        if  ("<img1>" in my_old_article) and ("<img2>" in my_old_article) and ("<img3>" not in my_old_article):
            if("<img1>" in article_content):
                bool["img1"] = False
                if("<img2>" in article_content):
                    bool["img2"] = False
                    if("<img3>" in article_content):
                        bool["img3"] = True


        bool["article_heading"] = article_heading
        bool["article_content"] = article_content
        bool["article_id"] = article_id
        return render(request,"askNewImage.html",bool)
 

def renderUpdateImagePage(request):
    if not request.session.has_key('admin'):
        return redirect("/Panel")
    if "a" not in request.GET.keys():
        return HttpResponse("Bad Request")
    article_code = request.GET["a"]
    getImages = []
    getImages = list(Media.objects.filter(article_id = article_code).values())
    for items in getImages:
        s = items["img1"].split("/")
        items["img1"] = s[-1]
    dataDict = {"data":getImages}
    dataDict["isData"] = True
    if len(getImages) == 0:
        dataDict["isData"] = False
    return render(request,"updateImages.html",dataDict)


def AddNewImages(request):
    if not request.session.has_key('admin'):
        return redirect("/Panel")
    if "newImagesSave" not in request.POST.keys():
        return HttpResponse("Bad request")
    ArticleCode = request.POST["article_id"]
    article_heading = request.POST["article_heading"]
    article_content = request.POST["article_content"]
    today = strftime("%d-%m-%Y", gmtime())
    if "img1" in request.FILES.keys():
        img1 = request.FILES["img1"]
        AddImage = Media(img1 = img1,article_id = ArticleCode,img_count = 1)
        AddImage.save()
    if "img2" in request.FILES.keys():
        img2 = request.FILES["img2"]
        AddImage = Media(img1 = img2,article_id = ArticleCode,img_count = 2)
        AddImage.save()
    if "img3" in request.FILES.keys():
        img3 = request.FILES["img3"]
        AddImage = Media(img1 = img3,article_id = ArticleCode,img_count = 3)
        AddImage.save()
    Article.objects.filter(article_id=ArticleCode).update(heading = article_heading,content = article_content,date = today)
    return render(request,"verify.html",{"NewImageUpload":True,"article": ArticleCode })

def replaceImage(request):
    if not request.session.has_key('admin'):
        return redirect("/Panel")
    if "submit_replacement" not in request.POST.keys():
        return HttpResponse("Bad Request")
    article = request.POST["article_id"]
    imgNumber = int(request.POST["image_count"])
    myImg = request.FILES["replacement"]
    old_img = list(Media.objects.filter(article_id=article,img_count = imgNumber).values())
    old_img = old_img[0]["img1"]
    os.remove("./"+old_img)
    Media.objects.filter(article_id=article,img_count = imgNumber).delete()
    AddImage = Media(img1 = myImg,article_id = article,img_count = imgNumber)
    AddImage.save()
    # print(old_img)
    return render(request,"verify.html",{"replacementImg":True,"article":article})

def DeleteImage(request):
    if not request.session.has_key('admin'):
        return redirect("/Panel")
    if "article_number" not in request.POST.keys():
        return HttpResponse("Bad request")
    article = request.POST["article_number"]
    imgCount = int(request.POST["image_number"])
    if imgCount == 1:
        old_img = list(Media.objects.filter(article_id=article,img_count = imgCount).values())
        old_img = old_img[0]["img1"]
        os.remove("./"+old_img)
        Media.objects.filter(article_id=article,img_count = imgCount).delete()
        Media.objects.filter(article_id=article,img_count = 2).update(img_count = 1)
        Media.objects.filter(article_id=article,img_count = 3).update(img_count = 2)
        article_body = list(Article.objects.filter(article_id = article).values())
        article_body = article_body[0]["content"]
        article_body = article_body.replace("<img1>","")
        article_body = article_body.replace("<img2>","<img1>")
        article_body = article_body.replace("<img3>","<img2>")
        Article.objects.filter(article_id = article).update(content = article_body)
    if imgCount == 2:
        old_img = list(Media.objects.filter(article_id=article,img_count = imgCount).values())
        old_img = old_img[0]["img1"]
        os.remove("./"+old_img)
        Media.objects.filter(article_id=article,img_count = imgCount).delete()
        Media.objects.filter(article_id=article,img_count = 3).update(img_count = 2)
        article_body = list(Article.objects.filter(article_id = article).values())
        article_body = article_body[0]["content"]
        article_body = article_body.replace("<img2>","")
        article_body = article_body.replace("<img3>","<img2>")
        Article.objects.filter(article_id = article).update(content = article_body)
    if imgCount == 3:
        old_img = list(Media.objects.filter(article_id=article,img_count = imgCount).values())
        old_img = old_img[0]["img1"]
        os.remove("./"+old_img)
        Media.objects.filter(article_id=article,img_count = imgCount).delete()
        article_body = list(Article.objects.filter(article_id = article).values())
        article_body = article_body[0]["content"]
        article_body = article_body.replace("<img3>","")
        Article.objects.filter(article_id = article).update(content = article_body)
    
    return render(request,"verify.html",{"imageDeleted":True,"article":article})


def DeleteArticle(request):
    if not request.session.has_key('admin'):
        return redirect("/Panel")
    if "article_code" not in request.POST.keys():
        return HttpResponse("Bad Request")
    article = request.POST["article_code"]
    Article.objects.filter(article_id = article).delete()
    getImages = list(Media.objects.filter(article_id = article).values())
    for item in getImages:
        toDlt = item["img1"]
        os.remove("./"+toDlt)
        # print(toDlt)
    return render(request,"verify.html",{"artDelete":True})

