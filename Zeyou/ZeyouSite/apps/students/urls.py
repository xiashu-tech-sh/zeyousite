# from django.urls import path
from django.conf.urls import url
from . import views
from rest_framework_jwt.views import obtain_jwt_token

app_name = 'students'
urlpatterns = [
    url(r'^studentupdate/$', views.UpdateStudent.as_view(), name='studentupdate'),
    url(r'^studentadd/$', views.StudentView.as_view(), name='studentadd'),
    # 上传文件
    url(r'^upload/$', views.UploadView.as_view(), name='upload'),
    # 条件过滤查询学生
    url(r'^studentquery/$', views.StudentQueryView.as_view(), name='studentquery'),
    # 下载 (条件过滤查询学生)
    url(r'^downloadstudent/$', views.StudentinforView.as_view(), name='downloadstudent'),
    # 下载 (选项)
    url(r'^downloadid/$', views.StudentIdView.as_view(), name='downloadid'),
    # 下载 (关键字过滤)
    url(r'^downloadselect/$', views.StudentSelectView.as_view(), name='downloadid'),
    # 姓名过滤查询
    url(r'^selectquery/$', views.SelectNameQueryView.as_view(), name='selectquery'),
    # 获取用户编号
    url(r'^studentcount/$', views.StudentCountView.as_view(), name='studentcount'),
    # 学术账户下载营销表
    url(r'^academicdownloadacad/$', views.AcademicDownloadView.as_view(), name='academicdownloadacad'),
    # 小助手查询
    url(r'^littlegetstudents/$', views.LittleGetStudentsView.as_view(), name='littlegetstudents'),

]