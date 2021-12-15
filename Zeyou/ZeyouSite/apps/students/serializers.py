from rest_framework import serializers
from .models import Student
from rest_framework.response import Response
from datetime import date, datetime


class CreateStudentSerializer(serializers.ModelSerializer):

    # 客户状态（categorical) 1
    customer_state = serializers.CharField(write_only=True,default="",allow_blank=True)

    # 来源（categorical) 2
    source = serializers.CharField(write_only=True,default="",allow_blank=True)

    # 加好友日期 3
    date_to_add = serializers.CharField(write_only=True,default="",allow_blank=True)

    # 姓名 4
    name = serializers.CharField(write_only=True,default="",allow_blank=True)

    # 转咨询时间
    transfer_time = serializers.CharField(write_only=True,default="",allow_blank=True)

    # 签约时间 5
    signing_time = serializers.CharField(write_only=True,default="",allow_blank=True)

    # 性别 6
    gender = serializers.CharField(write_only=True,default="",allow_blank=True)

    # 微信号 7
    wechat_num = serializers.CharField(write_only=True,default="",allow_blank=True)

    # 地区 8
    area = serializers.CharField(write_only=True,default="",allow_blank=True)

    # 手机号 9
    phone = serializers.CharField(write_only=True,default="",allow_blank=True)

    # 所属小助手 10
    little_assistant = serializers.CharField(write_only=True,default="",allow_blank=True)

    # 所属顾问 11
    consultant = serializers.CharField(write_only=True,default="",allow_blank=True)

    # 所属服务顾问 12
    service_consultant = serializers.CharField(write_only=True,default="",allow_blank=True)

    # 所属文案 13
    paper_writer = serializers.CharField(write_only=True,default="",allow_blank=True)

    # 战略顾问
    strategy_consultant = serializers.CharField(write_only=True,default="",allow_blank=True)

    # 客户身份 家长or学生 14
    identity = serializers.CharField(write_only=True,default="",allow_blank=True)

    # 学校类型 15
    school_type = serializers.CharField(write_only=True,default="",allow_blank=True)

    # 学校名 16
    school = serializers.CharField(write_only=True,default="",allow_blank=True)

    # 课程体系 17
    curriculum_system = serializers.CharField(write_only=True,default="",allow_blank=True)

    # 课程体系备注 18
    curriculum_system_note = serializers.CharField(write_only=True,default="",allow_blank=True)

    # 申请层级入学时间 19
    graduation_date = serializers.CharField(write_only=True,default="",allow_blank=True)

    # 申请层级 20
    application_level = serializers.CharField(write_only=True,default="",allow_blank=True)

    # 专业方向 21
    major = serializers.CharField(write_only=True,default="",allow_blank=True)

    # 目标国家 22
    target_country = serializers.CharField(write_only=True,default="",allow_blank=True)

    # 托福 23
    TOEFL = serializers.CharField(write_only=True,default="",allow_blank=True)
    # 雅思 24
    IELTS = serializers.CharField(write_only=True,default="",allow_blank=True)
    # SAT 25
    SAT = serializers.CharField(write_only=True,default="",allow_blank=True)
    # ACT 26
    ACT = serializers.CharField(write_only=True,default="",allow_blank=True)
    # GRE 27
    GRE = serializers.CharField(write_only=True,default="",allow_blank=True)
    # 客户信息备注
    customer_remarks = serializers.CharField(write_only=True,default="",allow_blank=True)
    class Meta:
        model = Student
        fields = "__all__"
    def to_representation(self, instance):
        return (instance)
    def create(self, validated_data):
        try:

            student = super().create(validated_data)
            student.save()
        except:
            return {'message': "当前输入姓名已存在已存在，请检查", 'status': 201}
        return {'message': '添加成功','status':200}
