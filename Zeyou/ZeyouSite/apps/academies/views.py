from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Academy
from .serializers import CreateAcademySerializer
from datetime import date, datetime
from django.forms.models import model_to_dict
from django.http import JsonResponse
import json
from students.models import Student

class AcademyView(CreateAPIView):
    """
    学生注册
    """
    serializer_class = CreateAcademySerializer


class AcademyUpdateView(APIView):
    def post(self, request):
        data = request.data
        name = data['name']
        source = data['source']
        product_name=data['product_name']
        difficulty_level = data['difficulty_level']
        content_direction = data['content_direction']
        class_size = data['class_size']
        date_of_purchasing = data['date_of_purchasing']
        hours_of_lecture = data['hours_of_lecture']
        price_overall = data["price_overall"]
        date_of_lecture = data['date_of_lecture']
        product_type = data['product_type']
        product = data['product']
        price_per_hour = data['price_per_hour']
        cur_state = data['cur_state']
        teacher = data['teacher']
        teaching_assistant = data['teaching_assistant']
        sales = data['sales']
        has_been_lecture = data['has_been_lecture']
        the_remaining_lecture = data['the_remaining_lecture']
        follow_period = data['follow_period']
        calss_course=data['calss_course']
        follow = Academy.objects.filter(order_number=data["order_number"]).all()
        if follow[0].follow_period == follow_period:
            warning_show = follow[0].warning_show
            student_update = 201
        else:
            warning_show = "true"
            Student.objects.filter(name=name).update(warning_show="true")
            student_update = 200

        try:
            Academy.objects.filter(order_number=data["order_number"]).update(name=name, source=source, price_overall=price_overall, date_of_purchasing=date_of_purchasing,
                                  date_of_lecture=date_of_lecture, hours_of_lecture=hours_of_lecture, product=product,
                                  product_type=product_type, price_per_hour=price_per_hour, cur_state=cur_state, teacher=teacher,
                                  teaching_assistant=teaching_assistant, sales=sales,the_remaining_lecture=the_remaining_lecture,
                                  has_been_lecture=has_been_lecture,class_size=class_size,content_direction=content_direction,
                                  difficulty_level=difficulty_level,product_name=product_name,follow_period=follow_period,calss_course=calss_course,
                                  warning_show=warning_show)

            return Response({"message": "更新成功", "status": 200,"student_update":student_update})
        except:
            return Response({"message": "参数校验失败", "status": 400})

class FollowUpdateView(APIView):

    def post(self, request):
        try:
            data = request.data
            now_time = datetime.now()
            now_time_str = now_time.strftime('%Y-%m-%d')
            Academy.objects.filter(id=data['item_id']).update(follow_number=now_time_str,warning_show="false")

            info = Academy.objects.filter(name=data['item_name']).all()
            the_end = info.count()
            for i in range(0,the_end):
                data1 = model_to_dict(info[i])
                if data1["warning_show"] == "true":
                    return Response({"message": "跟进成功", "status": 200, "upstatus":400})
            Student.objects.filter(name=data['item_name']).update(warning_show="false")
            return Response({"message": "跟进成功", "status": 200, "upstatus":200})
        except:
            return Response({"message": "校验失败", "status": 400})
class getacademicInforView(APIView):

    def post(self,request):
        dict_infor = {}
        data = request.data
        if data['options']:
            all_infor = []
            infors = Academy.objects.filter(name=data['username']).all()
            for infor in range(infors.count()):
                data_infor = model_to_dict(infors[infor])
                all_infor.append(data_infor)
            jsonArr = json.dumps(all_infor, ensure_ascii=False)
            return JsonResponse(jsonArr, safe=False)
        else:
            ret = []
            info = Academy.objects.filter(name=data['username']).all()
            try:
                if len(info) > 0:
                    for i in range(info.count()):
                        data_dist = {}
                        data_infor = model_to_dict(info[i])
                        data_dist['name']= data_infor['name']
                        data_dist['name'] = data_infor['name']
                        data_dist['name'] = data_infor['name']
                        data_dist['name'] = data_infor['name']
                    jsonArr = json.dumps(dict_infor, ensure_ascii=False)
                    return JsonResponse(jsonArr, safe=False)
            except IndexError as e:
                dict_infor['status'] = 203
                dict_infor['message'] = "请添加数据"
                jsonArr = json.dumps(dict_infor, ensure_ascii=False)
                return JsonResponse(jsonArr, safe=False)
            else:
                dict_infor['status'] = 202
                jsonArr = json.dumps(dict_infor, ensure_ascii=False)
                return JsonResponse(jsonArr, safe=False)

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)
class makeInforView(APIView):

    def post(self, request):
        data = request.data
        name = data['username']
        if name:
            customerpage = int(data['makecustomerpage'])
            dict_infor = {}
            info = Academy.objects.filter(name=name).all()
            dict_infor['custpag'] = info.count()
            if info.count() == 0:
                dict_infor['status'] = "202"
                jsonArr = json.dumps(dict_infor, ensure_ascii=False)
                return JsonResponse(jsonArr, safe=False)
            if customerpage==1:
                if info.count()<10:
                    the_end = info.count()
                else:
                    the_end = 10
            elif 10< 10*customerpage < info.count():
                the_end =10*customerpage
            elif 10*customerpage > info.count():
                the_end = info.count()
            ret = []
            for i in range(10*(customerpage-1),the_end):
                data1 = model_to_dict(info[i])
                data2 = dict()
                data2["id"] = data1["id"]
                data2["name"] = data1["name"]
                data2["product"] = data1["product"]
                data2["cur_state"] = data1["cur_state"]
                data2["teaching_assistant"] = data1["teaching_assistant"]
                data2["warning_show"] = data1["warning_show"]
                data2["follow_period"] = data1['follow_period']
                ret.append(data2)
            dict_infor['data_infor'] = ret
            dict_infor['status'] = "200"
            jsonArr = json.dumps(dict_infor, ensure_ascii=False)
            return JsonResponse(jsonArr, safe=False)
        else:
            dict_infor = {}
            dict_infor['status'] = "202"
            jsonArr = json.dumps(dict_infor, ensure_ascii=False)
            return JsonResponse(jsonArr, safe=False)


    def get(self,request,user_id):
        infors = Academy.objects.filter(id=user_id).all()
        data_infor = model_to_dict(infors[0])
        jsonArr = json.dumps(data_infor, cls = DateEncoder,ensure_ascii=False)
        return JsonResponse(jsonArr, safe=False)
    def delete(self, request):
        data = request.data
        for id in data:
            Academy.objects.filter(id=id).delete()
        # 删除成功
        return Response({"message": "删除成功","status":200})

class OrderNumView(APIView):

    def get(self, *args, **kwargs):

        Articlelist2 = Academy.objects.filter(**kwargs).order_by('-order_number')[0].order_number # 倒序
        count_name = "CFC" + str(int(Articlelist2[3:])+1 )

        return Response({ 'ordernumber': count_name})


class AcadeinforView(APIView):

    def post(self,request):
        data = request.data
        name = data["username"]
        open_all = data['all']
        if open_all[0] == "all":
            info = Academy.objects.filter(name=name).all()
            the_end = info.count()
            ret = []
            for i in range(0, the_end):
                data1 = model_to_dict(info[i])
                ret.append(data1)
            jsonArr = json.dumps(ret, ensure_ascii=False)
            return JsonResponse(jsonArr, safe=False)
        else:
            ret = []
            for id in data["all"]:
                info = Academy.objects.get(id=id)
                data1 = model_to_dict(info)
                ret.append(data1)
            jsonArr = json.dumps(ret, ensure_ascii=False)
            return JsonResponse(jsonArr, safe=False)