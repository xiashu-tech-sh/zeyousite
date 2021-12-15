from django.db import models
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Student(models.Model):

    # 客户状态（categorical) 1
    customer_state = models.CharField(max_length=500, db_index=True, null=True)

    # 来源（categorical) 2
    source = models.CharField(max_length=64, db_index=True, null=True)

    # 加好友日期 3
    date_to_add = models.CharField(max_length=64, db_index=True, null=True)

    # 姓名 4
    name = models.CharField(max_length=64, db_index=True, unique=True)

    # 转咨询时间
    transfer_time = models.CharField(max_length=64, db_index=True, null=True)

    # 签约时间 5
    signing_time = models.CharField(max_length=64, db_index=True, null=True)

    # 性别 6
    gender = models.CharField(max_length=20, db_index=True,null=True)

    # 微信号 7
    wechat_num = models.CharField(max_length=64, db_index=True,null=True )

    # 地区 8
    area = models.CharField(max_length=64, db_index=True, null=True)

    # 手机号 9
    phone = models.CharField(max_length=64, db_index=True,null=True)

    # 所属小助手 10
    little_assistant = models.CharField(max_length=64, db_index=True,null=True)

    # 所属顾问 11
    consultant = models.CharField(max_length=64, db_index=True, null=True)

    # 所属服务顾问 12
    service_consultant = models.CharField(max_length=64, db_index=True, null=True)

    # 所属文案 13
    paper_writer = models.CharField(max_length=64, db_index=True, null=True)

    # 战略顾问
    strategy_consultant = models.CharField(max_length=64, db_index=True, null=True)

    # 客户身份 家长or学生 14
    identity = models.CharField(max_length=64, null=True)

    # 学校类型 15
    school_type = models.CharField(max_length=64, db_index=True, null=True)

    # 学校名 16
    school = models.CharField(max_length=64, db_index=True, null=True)

    # 课程体系 17
    curriculum_system = models.CharField(max_length=64, db_index=True, null=True)

    # 课程体系备注 18
    curriculum_system_note = models.CharField(max_length=64, db_index=True, null=True)

    # 申请层级入学时间 19
    graduation_date = models.CharField(max_length=64, null=True)

    # 申请层级 20
    application_level = models.CharField(max_length=64, db_index=True, null=True)

    # 专业方向 21
    major = models.CharField(max_length=64, null=True)

    # 目标国家 22
    target_country = models.CharField(max_length=64, null=True)

    # 托福 23
    TOEFL = models.CharField(max_length=64, default="")
    # 雅思 24
    IELTS = models.CharField(max_length=64, default="")
    # SAT 25
    SAT = models.CharField(max_length=64, default="")
    # ACT 26
    ACT = models.CharField(max_length=64, default="")
    # GRE 27
    GRE = models.CharField(max_length=64, default="")

    # 客户信息备注
    customer_remarks = models.CharField(max_length=64, default="")

    #图片实现
    warning_show =  models.CharField(max_length=64, db_index=True ,default="false")
    # 转咨询 转为 已流失
    transfer_to_beenlost = models.CharField(max_length=64, default="",null=True)


    def __str__(self):
        return '<Student {}>'.format(self.name)