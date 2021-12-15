from django.http import JsonResponse
from rest_framework import serializers
from .models import Academy
from rest_framework.response import Response
from datetime import date, datetime

from students.models import Student

class CreateAcademySerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(write_only=True)
    name = serializers.CharField(write_only=True, default="", allow_blank=True)
    source = serializers.CharField(write_only=True, default="", allow_blank=True)
    product_type = serializers.CharField(write_only=True, default="", allow_blank=True)

    product_name = serializers.CharField(write_only=True, default="", allow_blank=True)
    difficulty_level = serializers.CharField(write_only=True, default="", allow_blank=True)
    content_direction = serializers.CharField(write_only=True, default="", allow_blank=True)
    class_size = serializers.CharField(write_only=True, default="", allow_blank=True)
    calss_course = serializers.CharField(write_only=True, default="", allow_blank=True)

    teaching_assistant = serializers.CharField(write_only=True, default="", allow_blank=True)
    sales = serializers.CharField(write_only=True, default="", allow_blank=True)
    teacher = serializers.CharField(write_only=True, default="", allow_blank=True)
    date_of_purchasing = serializers.CharField(write_only=True,default="")
    product = serializers.CharField(write_only=True, default="", allow_blank=True)
    date_of_lecture = serializers.CharField(write_only=True, default="", allow_blank=True)
    hours_of_lecture = serializers.CharField(write_only=True, default="", allow_blank=True)
    has_been_lecture = serializers.CharField(write_only=True, default="", allow_blank=True)
    the_remaining_lecture = serializers.CharField(write_only=True, default="", allow_blank=True)
    price_per_hour = serializers.CharField(write_only=True, default="", allow_blank=True)
    price_overall = serializers.CharField(write_only=True, default="", allow_blank=True)
    cur_state = serializers.CharField(write_only=True, default="", allow_blank=True)
    follow_period = serializers.CharField(write_only=True, default="", allow_blank=True)

    class Meta:
        model = Academy
        fields = "__all__"

    def to_representation(self, instance):
        return (instance)

    def create(self, validated_data):
        try:
            student = super().create(validated_data)
            student.save()
            Student.objects.filter(name=validated_data['name']).update(warning_show="true")
        except:
            return {'message': "参数效验失败", 'status': 201}
        return {'message': '添加成功', 'status': 200}
