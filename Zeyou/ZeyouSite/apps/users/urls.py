# from django.urls import path
from django.conf.urls import url
from . import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'^createuser/$', views.UserView.as_view(), name='createUser'),
    url(r'^authorizations/$', obtain_jwt_token, name='authorization'),
    # 旧密码改新密码
    url(r'^pwdupdate/$', views.UpdatePwdView.as_view(), name='pwdUpdate'),
    # 修改个人信息
    url(r'^personupdate/$', views.UpdatePerdView.as_view(), name='pwdUpdate'),
    url(r'^parseexcel/$', views.ParseExcelView.as_view(), name='parseexcel'),
    # 获取学生信息
    url(r'^filterdepartment/$', views.FilterDepartmentView.as_view(), name='filterDepartment'),
    # 获取学生详细信息
    url(r"^filterdepartment/(?P<studentns_id>\d+)/$", views.FilterDepartmentView.as_view(), name='filterDepartment'),
    url(r'^personalinfo/$', views.PersonalInfoView.as_view(), name='personalInfo'),
    url(r'^lookupuser/$', views.LookupUser.as_view(), name='userLookup'),
    url(r'^deleteuser/$', views.DeleteUser.as_view(), name='userdelete'),
    # 查询邮箱个数
    url(r'^email_number/$', views.EmailCountView.as_view()),
    # 查询用户名个数
    url(r'^username_number/$', views.UsernameCountView.as_view()),
    # 获取所有小助手
    url(r'^getassistant/$', views.GetassistantView.as_view()),
    # 获取所有顾问
    url(r'^consultant/$', views.ConsultantView.as_view()),
    # 获取所有顾问服务
    url(r'^serviceadvisor/$', views.ServiceadvisorView.as_view()),
    # 获取所有文案
    url(r'^copywriting/$', views.CopywritingView.as_view()),
    # 获取所有助教
    url(r'^teachingassistant/$', views.TeachingassistantView.as_view()),
    # 获取所有战略顾问
    url(r'^strategy/$', views.StrategyView.as_view()),
    # 个人中心
    url(r'^user/(?P<user_id>\d+)/$', views.UserDetailView.as_view()),
    # 更新用户数据
    url(r'^user/$', views.UserDetailView.as_view()),
    # 查询员工
    url(r'^getuserinfo/$', views.GetUserInfoView.as_view()),
    # 发送邮箱验证码
    url(r'^sms_code/$', views.EmailCodeView.as_view()),
    # 通过邮箱验证码修改密码
    url(r'^email_password/$', views.EmailPasswordView.as_view()),

]
