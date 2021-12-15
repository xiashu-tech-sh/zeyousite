from django.db import models
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Academy(models.Model):
    # 订单号
    order_number = models.CharField(max_length=64, db_index=True, unique=True)

    # 姓名
    name = models.CharField(max_length=64, db_index=True, null=True)

    # 客户来源
    source = models.CharField(max_length=64, db_index=True, null=True)

    # 产品类型
    product_type = models.CharField(max_length=64, db_index=True, null=True)

    # 产品名称
    product_name = models.CharField(max_length=64, db_index=True, null=True)

    # 课程体系分类
    calss_course = models.CharField(max_length=64, db_index=True, null=True)

    # 难度级别
    difficulty_level = models.CharField(max_length=64, db_index=True,null=True)

    # 内容方向
    content_direction = models.CharField(max_length=64, db_index=True, null=True)

    # 班型大小
    class_size = models.CharField(max_length=64, db_index=True, null=True)

    # 分配助教
    teaching_assistant = models.CharField(max_length=64, db_index=True, null=True)

    # 所属销售人员
    sales = models.CharField(max_length=64, db_index=True, null=True)

    # 授课老师
    teacher = models.CharField(max_length=64, db_index=True, null=True)

    # 购买时间
    date_of_purchasing = models.CharField(max_length=64, db_index=True, null=True)

    # 产品内容
    product = models.CharField(max_length=64, db_index=True, null=True)

    # 上课日期
    date_of_lecture = models.CharField(max_length=64, db_index=True, null=True)

    # 预计课时
    hours_of_lecture = models.CharField(max_length=64, db_index=True,null=True)

    # 已用课时
    has_been_lecture = models.CharField(max_length=64, db_index=True, null=True)

    # 剩余课时
    the_remaining_lecture = models.CharField(max_length=64, db_index=True,null=True)

    # 导师报价
    price_per_hour = models.CharField(max_length=64, db_index=True,null=True)

    # 总价
    price_overall = models.CharField(max_length=64, db_index=True,null=True)

    # 推进状态
    cur_state = models.CharField(max_length=64, db_index=True , null=True)

    # 跟进周期
    follow_period = models.CharField(max_length=64, db_index=True , null=True)

    # 跟进次数
    follow_number = models.CharField(max_length=64, db_index=True , null=True)

    #图片显示
    warning_show = models.CharField(max_length=64, db_index=True, default="true")


    def __str__(self):
        return '<Academy {}>'.format(self.name)