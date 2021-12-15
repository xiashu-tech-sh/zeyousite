# from django.urls import path
from django.conf.urls import url
from . import views
from rest_framework_jwt.views import obtain_jwt_token

app_name = 'recommended'
urlpatterns = [
    # 学生信息推荐产品
    url(r'^studentanalysis/$', views.StudentAnalysisView.as_view(), name='studentupdate'),
    # 产品信息推荐学生
    url(r'^productanalysis/$', views.ProductAnalysisView.as_view(), name='studentupdate'),

]