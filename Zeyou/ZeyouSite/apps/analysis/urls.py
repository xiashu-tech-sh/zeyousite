# from django.urls import path
from django.conf.urls import url
from . import views
from rest_framework_jwt.views import obtain_jwt_token

app_name = 'analysis'
urlpatterns = [
    # 资源普遍状态分析
    url(r'^resourceanalysis/$', views.ResourceanAlysisView.as_view(), name='resourceanalysis'),
    # 客户转换状态分析
    url(r'^customerconversion/$', views.CustomerConversionaView.as_view(), name='customerconversion'),
    # 客户签约状态分析
    url(r'^customercontract/$', views.CustomerContractView.as_view(), name='customercontract'),
    # 产品购买情况分析
    url(r'^productstobuy/$', views.ProductsToBuyView.as_view(), name='productstobuy'),

    # 销售人员统计  # 获取销售人员名单
    url(r'^salesstatistics/$', views.SalesstatiSticsView.as_view(), name='salesstatistics'),
    # 顾问在办统计
    url(r'^consultantoffice/$', views.ConsultantOfficeView.as_view(), name='consultantoffice'),
    # 促签人数
    url(r'^promotenum/$', views.PromoteNumView.as_view(), name='promotenum'),
    # 销售分部
    url(r'^alesdistribution/$', views.AlesDistributionView.as_view(), name='alesdistribution'),

    # 复购率分析  /  下载
    url(r'^afterbuy/$', views.AfterBuyView.as_view(), name='afterbuy'),
    # 复购率下载
    #url(r'^afterbuydownload/', views.AfterBuyDownloadView.as_view(), name='afterbuydownload'),

]