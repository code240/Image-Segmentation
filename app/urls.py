import imp
from django.urls import path
from . import views
from . import panel
# from django.urls import path
from xml.etree.ElementInclude import include

urlpatterns = [
    path('',views.home,name='home'),
    path('Home',views.home,name='home'),
    path('Documentation',views.documentation,name='documentation'),
    path('Segmentation',views.segmentation,name='segmentation'),
    path('Uploadimg',views.Uploadimg,name='Uploadimg'),
    path('Segmenting',views.segmenting,name='segmenting'),
    path('Output',views.output,name='output'),
    path('Test',views.test,name='test'),

    path('Panel',panel.panel,name='panel'),
    path('Verify',panel.verify,name='verify'),
    path('Panel/Add',panel.addpage,name='addpage'),
    path('Panel/SaveArticle',panel.SaveArticle,name='SaveArticle'),
    path('Panel/Edit',panel.EditArticle,name='EditArticle'),
    path('Panel/SaveEditedArticle',panel.SaveEditedArticle,name='SaveEditedArticle'),
    path('Panel/UpdateImageSettings',panel.renderUpdateImagePage,name='renderUpdateImagePage'),
    path('Panel/AddNewImages',panel.AddNewImages,name="AddNewImages"),
    path('Panel/replaceImage',panel.replaceImage,name="replaceImage"),
    path('Panel/DeleteImage',panel.DeleteImage,name="DeleteImage"),
    path('Panel/DeleteArticle',panel.DeleteArticle,name="DeleteArticle"),
]

