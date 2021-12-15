import openpyxl
import os
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse, QueryDict, HttpResponse
from academies.models import Academy
from users.models import User
from .models import Student
from .serializers import CreateStudentSerializer
from datetime import date, datetime,timedelta
import xlrd
import json
from django.forms.models import model_to_dict
from django.db.models import Q
class StudentView(CreateAPIView):
    """
    学生注册
    """
    serializer_class = CreateStudentSerializer


class UploadView(APIView):

    def post(self,request):
        file_bytes = request.FILES.get('file')
        excel_type = file_bytes.name.split('.')[1]
        if excel_type in ['xlsx', 'xls']:
            # 开始解析上传的excel表格
            allfolders = xlrd.open_workbook(filename=None, file_contents=file_bytes.read())
            res = []
            for i,table in enumerate(allfolders.sheets()):
                rows = table.ncols
                nrows = table.nrows
                if allfolders.sheet_names()[i] =="用户信息主表" or rows==30:
                    student_res,updete_data_list = self.uploadstudent(table,allfolders,nrows)
                    if student_res:
                        if len(updete_data_list)>0:
                            res.append({"message": "导入用户信息主表成功，总覆盖%s条，请点击查看覆盖数据查看详情"%len(updete_data_list), "status": 200, "updeta_data": updete_data_list})
                        else:
                            res.append({"message": "导入用户信息主表成功","status":200,"updeta_data":updete_data_list})
                    else:
                        res.append({"message": "导入用户信息主表失败","status": 201})
                elif allfolders.sheet_names()[i]=="学术成长学院营销信息表" or rows==22:
                    academy_res = self.uploadacademic(table,allfolders,nrows)
                    if academy_res:
                        res.append({"message": "导入学术成长学院营销信息表成功", "status": 200})
                    else:
                        res.append({"message": "导入学术成长学院营销信息表失败", "status": 201})
            jsonArr = json.dumps(res, ensure_ascii=False)
            return JsonResponse(jsonArr, safe=False)
        else:
            res = [{"message": "上传文件类型错误", "status": 400}]
            jsonArr = json.dumps(res, ensure_ascii=False)
            return JsonResponse(jsonArr, safe=False)

    def uploadacademic(self,table,allfolders,rows):
        # try:
            order_number = Academy.objects.filter().order_by('-order_number')[0].order_number # 倒序
            num = 1
            for i in range(1, rows):
                count_name = "CFC" + str(int(order_number[3:]) + num)
                rowVlaues = table.row_values(i)
                issudate = table.cell(i, 3).value
                # 日期格式转换
                try:
                    data_value = xlrd.xldate_as_tuple(rowVlaues[14], 0)
                    lecture_y_m_d = date(*data_value[:3]).strftime('%Y-%m-%d')
                except TypeError as e:
                    lecture_y_m_d = rowVlaues[14]
                now_time = datetime.now()
                now_time_str = now_time.strftime('%Y-%m-%d')
                warning_show = "true"
                try:
                    data_value = xlrd.xldate_as_tuple(rowVlaues[12], 0)
                    buy_y_m_d = date(*data_value[:3]).strftime('%Y-%m-%d')
                except TypeError as e:
                    buy_y_m_d = rowVlaues[12]
                if rowVlaues[6]:
                    try:
                        difficulty_level = str(int(rowVlaues[6]))
                    except:
                        difficulty_level = rowVlaues[6]
                else:
                    difficulty_level =rowVlaues[6]
                try:

                    student_ = Academy.objects.create(	order_number=count_name,
                                                    name=rowVlaues[1],
                                                    source=rowVlaues[2],
                                                    product_type=rowVlaues[3],
                                                    product_name=rowVlaues[4],
                                                    calss_course=rowVlaues[5],
                                                    difficulty_level=difficulty_level,
                                                    content_direction=rowVlaues[7],
                                                    class_size=rowVlaues[8],
                                                    teaching_assistant=rowVlaues[9],
                                                    sales=rowVlaues[10],
                                                    teacher=rowVlaues[11],
                                                    date_of_purchasing=buy_y_m_d,
                                                    product=rowVlaues[13],
                                                    date_of_lecture=lecture_y_m_d,
                                                    hours_of_lecture=rowVlaues[15],
                                                    has_been_lecture = rowVlaues[16],
                                                    the_remaining_lecture = rowVlaues[17],
                                                    price_per_hour=rowVlaues[18],
                                                    price_overall=rowVlaues[19],
                                                    cur_state=rowVlaues[20],
                                                    follow_period=rowVlaues[21],
                                                    follow_number = now_time_str,
                                                    warning_show = warning_show
                                                    )
                    student_.save()
                    Student.objects.filter(name=rowVlaues[1]).update(warning_show=warning_show)
                except:
                    continue
                num+=1
            return True
        # except:
        #     return False

    def uploadstudent(self,table,allfolders,rows):
        # try:
            updete_data_list = []
            for i in range(1, rows):
                update_data_dist = {}
                rowVlaues = table.row_values(i)
                issudate = table.cell(i, 2).value
                # 日期格式转换
                try:
                    data_value = xlrd.xldate_as_tuple(rowVlaues[2], 0)
                    y_m_d = date(*data_value[:3]).strftime('%Y-%m-%d')
                except TypeError as e:
                    y_m_d = rowVlaues[2]
                try:
                    transfer_value = xlrd.xldate_as_tuple(rowVlaues[4], 0)
                    transfer_time = date(*transfer_value[:3]).strftime('%Y-%m-%d')
                except TypeError as e:
                    transfer_time = rowVlaues[4]

                try:
                    signing_time_value = xlrd.xldate_as_tuple(rowVlaues[5], 0)
                    signing_time = date(*signing_time_value[:3]).strftime('%Y-%m-%d')
                except TypeError as e:
                    signing_time = rowVlaues[5]
                if rowVlaues[9]:
                    try:
                        phone = str(int(rowVlaues[9]))
                    except:
                        phone = rowVlaues[9]
                else:
                    phone = rowVlaues[9]
                if rowVlaues[7]:
                    try:
                        wechat_num = str(int(rowVlaues[7]))
                    except:
                        wechat_num = rowVlaues[7]
                else:
                    wechat_num = rowVlaues[7]
                try:
                    if rowVlaues[13] == "海本" and int(rowVlaues[18][:4]) == datetime.now().year:
                        customer_state = "未分配"+rowVlaues[0][3:]
                    else:
                        customer_state = rowVlaues[0]
                except:
                    customer_state = rowVlaues[0]
                try:
                    student_ = Student.objects.create(customer_state=customer_state, source=rowVlaues[1],date_to_add = y_m_d,transfer_time = transfer_time,
                                                    signing_time=signing_time,
                                                      name=rowVlaues[3], gender=rowVlaues[6], wechat_num=wechat_num,
                                                      area=rowVlaues[8],
                                                      phone=phone, little_assistant=rowVlaues[10],
                                                      consultant=rowVlaues[11], service_consultant=rowVlaues[12],
                                                      paper_writer=rowVlaues[13], strategy_consultant=rowVlaues[14],identity=rowVlaues[15],
                                                      school_type=rowVlaues[16], school=rowVlaues[17],
                                                      curriculum_system=rowVlaues[18], curriculum_system_note=rowVlaues[19],
                                                      application_level=rowVlaues[20],
                                                      graduation_date=rowVlaues[21], major=rowVlaues[22],
                                                      target_country=rowVlaues[23],
                                                      TOEFL=rowVlaues[24], IELTS=rowVlaues[25], SAT=rowVlaues[26],
                                                      ACT=rowVlaues[27], GRE=rowVlaues[28],customer_remarks=rowVlaues[29]
                                                      )
                    student_.save()
                except:
                    update_data_dist["name"] = rowVlaues[3]
                    update_data_dist["wechat_num"] = rowVlaues[7]
                    update_data_dist['little_assistant']=rowVlaues[10]
                    updete_data_list.append(update_data_dist)
                    Student.objects.filter(name=rowVlaues[3]).update(customer_state=customer_state, source=rowVlaues[1], date_to_add=y_m_d,
                                                      name=rowVlaues[3],transfer_time = transfer_time,signing_time=signing_time, gender=rowVlaues[6], wechat_num=wechat_num,
                                                      area=rowVlaues[8],
                                                      phone=rowVlaues[9], little_assistant=rowVlaues[10],
                                                      consultant=rowVlaues[11], service_consultant=rowVlaues[12],
                                                      paper_writer=rowVlaues[13], strategy_consultant=rowVlaues[14],identity=rowVlaues[15],
                                                      school_type=rowVlaues[16], school=rowVlaues[17],
                                                      curriculum_system=rowVlaues[18], curriculum_system_note=rowVlaues[19],
                                                      application_level=rowVlaues[20],
                                                      graduation_date=rowVlaues[21], major=rowVlaues[22],
                                                      target_country=rowVlaues[23],
                                                      TOEFL=rowVlaues[24], IELTS=rowVlaues[25], SAT=rowVlaues[26],
                                                      ACT=rowVlaues[27], GRE=rowVlaues[28],customer_remarks=rowVlaues[29]
                                                      )
                    continue
            return True,updete_data_list
        # except:
        #     return False,updete_data_list
class UpdateStudent(APIView):

    def post(self, request):
        data = request.data
        source = data['source']
        date_to_add = data['date_to_add']
        name = data['name']
        signing_time= data['signing_time']
        gender = data['gender']
        wechat_num = data['wechat_num']
        area = data['area']
        phone = data['phone']
        little_assistant = data["little_assistant"]
        consultant = data["consultant"]
        service_consultant = data["service_consultant"]
        paper_writer = data["paper_writer"]
        identity = data['identity']
        school_type = data["school_type"]
        school = data["school"]
        curriculum_system = data["curriculum_system"]
        curriculum_system_note = data["curriculum_system_note"]
        graduation_date = data['graduation_date']
        application_level = data["application_level"]
        major = data["major"]
        target_country = data["target_country"]
        TOEFL = data["TOEFL"]
        IELTS = data["IELTS"]
        SAT = data["SAT"]
        ACT = data["ACT"]
        GRE = data["GRE"]
        transfer_time=data["transfer_time"]
        customer_remarks = data["customer_remarks"]

        try:
            if application_level == "海本" and int(graduation_date[:4]) == datetime.now().year:
                customer_state = "未分配" + data["customer_state"][3:]
            else:
                customer_state = data["customer_state"]
        except:
            customer_state = data["customer_state"]
        if "已流失" in customer_state:
            transfer_to_beenlost = datetime.now()
        else:
            transfer_to_beenlost = ''

        # try:
        Student.objects.filter(id=data["id"]).update(customer_state=customer_state, date_to_add=date_to_add, graduation_date=graduation_date,
                              source=source, name=name, wechat_num=wechat_num,signing_time=signing_time, area=area, phone=phone, gender=gender, identity=identity,transfer_time=transfer_time,
                              little_assistant=little_assistant, consultant=consultant, service_consultant=service_consultant,
                              paper_writer=paper_writer, school=school, school_type=school_type,
                              curriculum_system=curriculum_system, curriculum_system_note=curriculum_system_note,
                              application_level=application_level, major=major, target_country=target_country,
                              TOEFL=TOEFL, IELTS=IELTS, SAT=SAT, ACT=ACT, GRE=GRE,customer_remarks=customer_remarks,transfer_to_beenlost=transfer_to_beenlost)
        return Response({"message": "更新成功", "status": 201})
        # except:
        #     return Response({"message": "参数格式错误，更新失败", "status": 400})

class StudentQueryView(APIView):

    def post(self, request):
        data = request.data
        name = data['username']
        little_helper = data['little_helper']
        dict_infor = {}
        identity = data['identity']
        if identity:
            info = Student.objects.filter().all()
        elif little_helper:
            info = Student.objects.filter(Q(customer_state="未分配已购买") | Q(customer_state="未分配未购买")).all()
        else:
            department = User.objects.get(username=name).department
            if "助教" in department:
                ty_data = Academy.objects.filter(Q(teaching_assistant=name)).values_list('name',flat = "true")
                list_ty_name = list(ty_data)
                if len(list_ty_name)==0:
                    info = Student.objects.filter(Q(little_assistant=name) | Q(consultant=name) |
                                                  Q(service_consultant=name) | Q(paper_writer=name)).all()

                else:
                    stu_name = Student.objects.filter(Q(little_assistant=name) | Q(consultant=name) |
                                                  Q(service_consultant=name) | Q(paper_writer=name)).values_list('name',flat = "true")
                    all_name = list(stu_name)
                    for ty_ in list_ty_name:
                        if ty_ not in all_name:
                            all_name.append(ty_)
                    info = Student.objects.filter(name=all_name[0]).all()
                    for _name in range(1,len(all_name)):
                        info = info | Student.objects.filter(name=all_name[_name]).all()
            else:
                info = Student.objects.filter(Q(little_assistant=name) | Q(consultant=name) |
                                              Q(service_consultant=name) | Q(paper_writer=name)).all()
        ret = []
        for i in range(info.count()):
            data1 = model_to_dict(info[i])
            if data['area']:
                if data1['area']!= data['area']:
                    continue
            if data['customer_state']:
                if data1['customer_state']!= data['customer_state']:
                    continue
            if data['graduation_date']:
                if data1['graduation_date']!= data['graduation_date']:
                    continue
            if data['major']:
                if data1['major']!= data['major']:
                    continue
            if data['school']:
                if data1['school']!= data['school']:
                    continue
            if data['source']:
                if data1['source']!= data['source']:
                    continue
            if data['application_level']:
                if data1['application_level']!= data['application_level']:
                    continue
            if data['assvalue']:
                if data1['assvalue']!= data['assvalue']:
                    continue
            data2 = dict()
            data2["id"] = data1["id"]
            data2["name"] = data1["name"]
            data2["graduation_date"] = data1["graduation_date"]
            data2["school"] = data1["school"]
            data2["warning_show"] = data1["warning_show"]
            ret.append(data2)
        dict_infor['custpag'] = len(ret)
        dict_infor['data_infor'] = ret
        if len(ret)>0:
            dict_infor['status']=200
        else:
            dict_infor['status'] = 202
        jsonArr = json.dumps(dict_infor, ensure_ascii=False)
        return JsonResponse(jsonArr, safe=False)


class LittleGetStudentsView(APIView):
    def post(self, request):
        customerpage = request.data['customerpage']
        info = Student.objects.filter().all()
        data_value = ["未分配已购买","未分配未购买"]
        ret = []
        dict_infor = {}
        for i in range(info.count()):
            data1 = model_to_dict(info[i])
            if data1['customer_state'] in data_value:
                data2 = dict()
                data2["id"] = data1["id"]
                data2["name"] = data1["name"]
                data2["graduation_date"] = data1["graduation_date"]
                data2["school"] = data1["school"]
                data2["warning_show"] = data1["warning_show"]
                ret.append(data2)
        if customerpage==1:
            if info.count()>10:
                the_end = 10
            else:
                the_end = info.count()
        elif 10*customerpage+10 < info.count():
            the_end =10*customerpage
        else:
            the_end = info.count()
        dict_infor['custpag'] = len(ret)
        dict_infor['data_infor'] = ret[10*customerpage-10:the_end]
        jsonArr = json.dumps(dict_infor, ensure_ascii=False)
        return JsonResponse(jsonArr, safe=False)


class StudentinforView(APIView):

    def post(self, request):
        data = request.data
        name = data['username']
        dict_infor = {}
        identity = data['identity']
        department = data["department"]
        if identity:
            info = Student.objects.filter().all()
        else:
            if "助教" in department:
                ty_data = Academy.objects.filter(Q(teaching_assistant=name)).values_list('name',flat = "true")
                list_ty_name = list(ty_data)
                if len(list_ty_name)==0:
                    info = Student.objects.filter(Q(little_assistant=name) | Q(consultant=name) |
                                                  Q(service_consultant=name) | Q(paper_writer=name)).all()

                else:
                    stu_name = Student.objects.filter(Q(little_assistant=name) | Q(consultant=name) |
                                                  Q(service_consultant=name) | Q(paper_writer=name)).values_list('name',flat = "true")
                    all_name = list(stu_name)
                    for ty_ in list_ty_name:
                        if ty_ not in all_name:
                            all_name.append(ty_)
                    info = Student.objects.filter(name=all_name[0]).all()
                    for _name in range(1,len(all_name)):
                        info = info | Student.objects.filter(name=all_name[_name]).all()

            else:
                info = Student.objects.filter(Q(little_assistant=name) | Q(consultant=name) |
                                          Q(service_consultant=name)| Q(paper_writer=name)).all()
        ret = []
        if info.count():
            for i in range(info.count()):
                data1 = model_to_dict(info[i])
                if data['area']:
                    if data1['area']!= data['area']:
                        continue
                if data['customer_state']:
                    if data1['customer_state']!= data['customer_state']:
                        continue
                if data['graduation_date']:
                    if data1['graduation_date']!= data['graduation_date']:
                        continue
                if data['major']:
                    if data1['major']!= data['major']:
                        continue
                if data['school']:
                    if data1['school']!= data['school']:
                        continue
                if data['source']:
                    if data1['source']!= data['source']:
                        continue
                if data['application_level']:
                    if data1['application_level']!= data['application_level']:
                        continue
                ret.append(data1)
            dict_infor["data_info"] = ret
            dict_infor["message"] = 200
            jsonArr = json.dumps(dict_infor, ensure_ascii=False)
            return JsonResponse(jsonArr, safe=False)
        else:
            dict_infor['status'] = 202
            dict_infor['message'] = "为匹配到学生"
            jsonArr = json.dumps(dict_infor, ensure_ascii=False)
            return JsonResponse(jsonArr, safe=False)
class StudentIdView(APIView):

    def post(self, request):
        data = request.data
        dict_infor = {}
        ret = []
        for id in data:
            info = Student.objects.filter(id=id).all()
            data1 = model_to_dict(info[0])
            ret.append(data1)
        dict_infor["data_info"] = ret
        dict_infor["message"] = 200
        jsonArr = json.dumps(dict_infor, ensure_ascii=False)
        return JsonResponse(jsonArr, safe=False)

class AcademicDownloadView(APIView):

    def post(self,request):
        info = Academy.objects.filter().all()
        ret = []
        for i in range(info.count()):
            data1 = model_to_dict(info[i])
            ret.append(data1)
        jsonArr = json.dumps(ret, ensure_ascii=False)
        return JsonResponse(jsonArr, safe=False)


class SelectNameQueryView(APIView):

    def post(self,request):
        data = request.data
        name = data["username"]
        identity = data['identity']
        select_name = data['name']
        dist_info = {}
        little_helper=data['little_helper'],
        if identity :
            info = Student.objects.filter(Q(name__icontains=select_name) | Q(wechat_num__icontains=select_name)).all()
        elif little_helper:
            info = Student.objects.filter(Q(name__icontains=select_name) | Q(wechat_num__icontains=select_name)).all()
        else:
            department = User.objects.get(username=name).department
            if  "助教" in department:
                ty_data = Academy.objects.filter(Q(teaching_assistant=name)&Q(name__icontains=name)).values_list('name',flat = "true")
                list_ty_name = list(ty_data)
                if len(list_ty_name)==0:
                    info = Student.objects.filter(
                        (Q(name__icontains=select_name) | Q(wechat_num__icontains=select_name)) & (
                        Q(little_assistant=name) | Q(consultant=name) |
                        Q(service_consultant=name) | Q(paper_writer=name))).all()
                else:
                    stu_name = Student.objects.filter(
                        (Q(name__icontains=select_name) | Q(wechat_num__icontains=select_name)) & (
                            Q(little_assistant=name) | Q(consultant=name) |
                            Q(service_consultant=name) | Q(paper_writer=name))).values_list('name', flat="true")
                    all_name = list(stu_name)
                    for ty_ in list_ty_name:
                        if ty_ not in all_name:
                            all_name.append(ty_)
                    info = Student.objects.filter(name=all_name[0]).all()
                    for _name in range(1,len(all_name)):
                        info = info | Student.objects.filter(name=all_name[_name]).all()
            else:
                info = Student.objects.filter( (Q(name__icontains=select_name) |Q(wechat_num__icontains=select_name))& (Q(little_assistant=name) | Q(consultant=name) |
                                          Q(service_consultant=name)| Q(paper_writer=name))).all()
        if info.count():
            ret = []
            for i in range(info.count()):
                data1 = model_to_dict(info[i])
                ret.append(data1)
            dist_info['status'] = 200
            dist_info['data_infor'] = ret
            dist_info['custpag']= info.count()
            jsonArr = json.dumps(dist_info, ensure_ascii=False)
            return JsonResponse(jsonArr, safe=False)
        else:
            dist_info['status'] = 202
            dist_info['message'] = "未找到含有关键字 %s 学生"%select_name
            jsonArr = json.dumps(dist_info, ensure_ascii=False)
            return JsonResponse(jsonArr, safe=False)

    def delete(self, request):
        data = request.data
        for id in data:
            Student.objects.filter(id=id).delete()
        # 删除成功
        return Response({"message": "删除成功","status":200})

class StudentSelectView(APIView):

    def post(self,request):
        data = request.data
        name = data["username"]
        open_all = data['all']
        select_name = data['name']
        dist_info = {}
        if open_all == "all":
            info = Student.objects.filter(name__icontains=select_name).all()
        else:
            department = User.objects.get(username=name).department
            if  "助教" in department:
                ty_data = Academy.objects.filter(Q(teaching_assistant=name)&Q(name__icontains=name)).values_list('name',flat = "true")
                list_ty_name = list(ty_data)
                if len(list_ty_name)==0:
                    info = Student.objects.filter(
                        (Q(name__icontains=select_name) | Q(wechat_num__icontains=select_name)) & (
                        Q(little_assistant=name) | Q(consultant=name) |
                        Q(service_consultant=name) | Q(paper_writer=name))).all()
                else:
                    stu_name = Student.objects.filter(
                        (Q(name__icontains=select_name) | Q(wechat_num__icontains=select_name)) & (
                            Q(little_assistant=name) | Q(consultant=name) |
                            Q(service_consultant=name) | Q(paper_writer=name))).values_list('name', flat="true")
                    all_name = list(stu_name)
                    for ty_ in list_ty_name:
                        if ty_ not in all_name:
                            all_name.append(ty_)
                    info = Student.objects.filter(name=all_name[0]).all()
                    for _name in range(1,len(all_name)):
                        info = info | Student.objects.filter(name=all_name[_name]).all()
            else:
                info = Student.objects.filter( (Q(name__icontains=select_name) |Q(wechat_num__icontains=select_name))& (Q(little_assistant=name) | Q(consultant=name) |
                                          Q(service_consultant=name)| Q(paper_writer=name))).all()
        if info.count():
            ret = []
            for i in range(info.count()):
                data1 = model_to_dict(info[i])
                ret.append(data1)
            dist_info['status'] = 200
            dist_info['data_infor'] = ret
            jsonArr = json.dumps(dist_info, ensure_ascii=False)
            return JsonResponse(jsonArr, safe=False)
        else:
            dist_info['status'] = 202
            dist_info['message'] = "未找到含有关键字 %s 学生"%select_name
            jsonArr = json.dumps(dist_info, ensure_ascii=False)
            return JsonResponse(jsonArr, safe=False)
class StudentCountView(APIView):

    def get(self, *args, **kwargs):
        # Articlelist1 = Student.objects.filter(**kwargs).order_by('customer_number')
        Articlelist2 = Student.objects.filter(**kwargs).order_by('-customer_number')[0].customer_number # 倒序
        count_name = "CFC" + str(int(Articlelist2[3:])+1 )
        return Response({ 'count_name': count_name})
