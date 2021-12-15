# from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'academies'
urlpatterns = [
    url(r'^academyupdate/$', views.AcademyUpdateView.as_view(), name='academyupdate'),
    url(r'^academyadd/$', views.AcademyView.as_view(), name='academyadd'),
    # 获取学术信息
    # url(r'^getacademicinfor/$', views.getacademicInforView.as_view(), name='academyadd'),
    # 获取学术信息列表
    url(r'^makeinfor/$', views.makeInforView.as_view(), name='academyadd'),

    url(r'^makeinfor/(?P<user_id>\d+)/$', views.makeInforView.as_view()),
    # 获取订单号
    url(r'^ordernum/$', views.OrderNumView.as_view(), name='studentadd'),
    # 下载
    url(r'^downloadacadinfor/$', views.AcadeinforView.as_view(), name='downloadacadinfor'),
    # 跟进
    url(r'^followupdate/$', views.FollowUpdateView.as_view(), name='followupdate'),


]