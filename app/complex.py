import imp
import sys
from django.http import HttpResponse
from .models import *
from markupsafe import Markup


def decodeMytags(Article_Heading,x,src,Article_date,articleId):
    Article_date = decodeDate(Article_date)
    Article_Heading = """<h1 class="main-content-heading">"""+Article_Heading+"</h1>"
    labelText = '<span class="content-label">Last edit : '+Article_date+' | Source : '+src+'</span>'
    x = x.replace("<p>","""<p class="main-content-para">""")
    x = x.replace("</p>","</p>")
    x = x.replace("<ht>","""<span class="highlight-docs">""")
    x = x.replace("</ht>","</span>")
    x = x.replace("<sh1>","""<h2 class="sub-heading-1">""")
    x = x.replace("</sh1>","</h2>")
    x = x.replace("<sh2>","""<h3 class="sub-heading-2">""")
    x = x.replace("</sh2>","</h3>")
    x = x.replace("<pt>","""<span class="points-1">""")
    x = x.replace("</pt>","</span>")
    x = x.replace("<al>","""<div class="algo-container">""")
    x = x.replace("</al>","</div>")
    articleBody = Article_Heading+labelText+x
    current_dict = {"noData":False,"Content":articleBody}
    articledict = decodeImages(articleBody,articleId,current_dict)
    if 'error' in articledict.keys():
        return {"error":True}
    articledict["Content"] = Markup(articledict["Content"])
    return articledict 

def decodeDate(d):
    li = list(d.split("-"))
    monthNumber = int(li[1])
    monthList = ["January","February","March","April","May","June","July","August","September","October","November","December"]
    month = monthList[monthNumber-1]
    date = li[0]+" "+month+" "+li[2]
    return date

def decodeImages(article,articleId,mydict):
    # print("Hello")
    if "<img1>" in article:
        getImage = Media.objects.values("img1").filter(article_id = articleId,img_count = 1)
        getImage = list(getImage)
        list_len = len(getImage)
        if list_len == 0:
            return {"error":True}
        img1 = getImage[-1]["img1"]
        img1 = img1.split("/")
        img1 = img1[2]
        # print(img1)
        article = article.replace("<img1>","""<span class="for-article-img"><img src="/static/"""+img1+"""" class="article-img" alt="article-related-img" /></span>""")
        mydict["Content"] = article
        # mydict["img1"] = Markup("""{% static """+"'"+img1+"'"+" %}")
        mydict["img1"] = img1

        if "<img2>" in article:
            getImage = Media.objects.values("img1").filter(article_id = articleId,img_count = 2)
            getImage = list(getImage)
            list_len = len(getImage)
            if list_len == 0:
                return {"error":True}
            img1 = getImage[-1]["img1"]
            img1 = img1.split("/")
            img1 = img1[2]
            article = article.replace("<img2>","""<span class="for-article-img"><img src="/static/"""+img1+"""" class="article-img" alt="article-related-img" /></span>""")
            mydict["Content"] = article
            mydict["img2"] = img1

            if "<img3>" in article:
                getImage = Media.objects.values("img1").filter(article_id = articleId,img_count = 3)
                getImage = list(getImage)
                list_len = len(getImage)
                if list_len == 0:
                    return {"error":True}
                img1 = getImage[-1]["img1"]
                img1 = img1.split("/")
                img1 = img1[2]
                article = article.replace("<img3>","""<span class="for-article-img"><img src="/static/"""+img1+"""" class="article-img" alt="article-related-img" /></span>""")
                mydict["Content"] = article
                mydict["img3"] = img1
    return mydict
        



def getPanelPara(content):
    r1 = content.find("<p>")
    r2 = content.find("</p>")
    mypara = content[r1:r2+4]
    mypara = mypara.replace("<p>","""<p class="article-short-body">""")
    mypara = Markup(mypara)
    return mypara




def imgcounts(content):
    count = 0
    if "<img1>" in content:
        count = 1
        if "<img2>" in content:
            count = 2
            if "<img3>" in content:
                count = 3
    return count