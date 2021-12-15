import csv
from urllib import parse

import xlwt
from django.shortcuts import render
from io import BytesIO

from django.utils.encoding import escape_uri_path
from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse, FileResponse
import json
import pandas as pd
import numpy as np
# Create your views here.
import warnings
from django_pandas.io import read_frame
from django.forms.models import model_to_dict
from students.models import Student
from academies.models import Academy

from django.db.models import Q
from rest_framework.response import Response
import datetime
import os
from xlwt import Workbook


class AlesDistributionView(APIView):

    def post(self,request):
        infor = {}
        set_ales = []
        # try:
        strat_time = datetime.date(*map(int, request.data['start_personnelsales_time'].split('-')))
        stop_time = datetime.date(*map(int, request.data['stop_personnelsales_time'].split('-')))
        qutset_data = Academy.objects.filter(date_of_purchasing__range=(strat_time, stop_time))

        for acade in qutset_data:
            stu_set = Student.objects.filter(name=acade.name).all()[0]
            to_follow_up = 0
            in_the_office = 0
            if "已分配" in stu_set.customer_state:
                to_follow_up = 1
            elif "已签约" in stu_set.customer_state:
                in_the_office = 1
            else:
                continue
            name_in = False
            name_location = 0
            for i, produvt_set in enumerate(set_ales):
                if produvt_set["name"] == stu_set.consultant:  # 顾问名字
                    name_in = True
                    name_location = i
            if name_in:
                set_ales[name_location]["to_follow_up"] += to_follow_up
                set_ales[name_location]["in_the_office"] += in_the_office
            else:
                tofollowup = 0
                produvt_dict = {
                    "name":stu_set.consultant,
                    "to_follow_up":tofollowup,
                    "in_the_office": in_the_office,
                }
                set_ales.append(produvt_dict)
        infor["status"] = 200
        infor["ales"] = set_ales
        # except:
        #     infor["res"] = []
        #     infor["status"] = 202
        self.read_xls(set_ales)
        jsonArr = json.dumps(infor, ensure_ascii=False)
        return JsonResponse(jsonArr, safe=False)
    def get(self,request):
        response = StreamingHttpResponse(self.readFile("顾问切片产品销售分布.xlsx"))
        response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format("1.xlsx")

        return response
    def readFile(self, filename, chunk_size=512):
        with open(filename, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    def read_xls(self,set_produvt):
        table_name = "销售分布"
        workbook = xlwt.Workbook(encoding="UTF-8")
        worksheet = workbook.add_sheet(table_name)
        # 样式设置(可选)
        style = xlwt.XFStyle()  # 初始化样式（居中+加粗）
        style2 = xlwt.XFStyle() # 初始化样式（居中）
        font = xlwt.Font()  # 为样式创建字体
        font.bold = True  # 加粗
        # 水平居中
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        alignment.vert = xlwt.Alignment.VERT_CENTER
        style.alignment = alignment  # Add Alignment to Style
        style2.alignment = alignment # Add Alignment to Style
        style.font = font
        worksheet.col(0).width = 6110
        worksheet.col(1).width = 8110
        worksheet.write_merge(0, 0, 0, 1, '顾问切片产品销售分布', style)
        __num = 0
        for i,peopre in enumerate(set_produvt):
            worksheet.write(i+1+__num, 0, peopre['name'], style)
            worksheet.write(i + 1 + __num, 1, "跟进客户购买计数", style2)
            __num += 1
            worksheet.write(__num+i+1, 1, peopre['to_follow_up'], style2)
            __num += 1
            worksheet.write(i + 1 + __num, 1, "在办客户购买计数", style2)
            __num += 1
            worksheet.write(__num + i + 1, 1, peopre['in_the_office'], style2)
            __num += 1

        exist_file = os.path.exists("顾问切片产品销售分布.xlsx")
        if exist_file:
            os.remove(r"顾问切片产品销售分布.xlsx")
        workbook.save("顾问切片产品销售分布.xlsx")
class PromoteNumView(APIView):

    def post(self,request):
        infor = {}
        set_promote = []
        try:
            strat_time = datetime.date(*map(int, request.data['start_personnelsales_time'].split('-')))
            stop_time = datetime.date(*map(int, request.data['stop_personnelsales_time'].split('-')))
            qutset_data = Student.objects.filter(Q(customer_state__icontains="已签约"))

            for student in qutset_data:
                name_in = False
                name_location = 0
                for i, produvt_set in enumerate(set_promote):
                    if produvt_set["name"] == student.consultant:  # 顾问名字
                        name_in = True
                        name_location = i
                if name_in:
                    try:
                        current_time = student.signing_time.date()
                    except:
                        set_promote[name_location]["all_num"] += 1
                        continue

                    if strat_time <= current_time <= stop_time:
                        set_promote[name_location]["all_num"] += 1
                        set_promote[name_location]["the_current"] += 1
                    else:
                        set_promote[name_location]["all_num"] += 1
                else:
                    try:
                        current_time = student.signing_time.date()
                    except:
                        produvt_dict = {
                            "name": student.consultant,
                            "all_num": 1,
                            "the_current": 0,
                        }
                        set_promote.append(produvt_dict)
                        continue
                    if strat_time <= current_time <= stop_time:
                        the_current = 1
                    else:
                        the_current = 0
                    produvt_dict = {
                        "name":student.name,
                        "all_num":1,
                        "the_current": the_current,
                        "rate ":0,
                    }
                    set_promote.append(produvt_dict)
            for item,set_o in enumerate(set_promote):
                if set_o["the_current"] ==0 or set_o["all_num"] ==0:
                    set_promote[item]["rate"] = 0
                else:
                    set_promote[item]["rate"] = '{:.2f}%'.format(set_o["the_current"]/set_o["all_num"] * 100)
            infor["status"] = 200
            infor["promote"] = set_promote
        except:
            infor["res"] = []
            infor["status"] = 202
        self.read_xls(set_promote)
        jsonArr = json.dumps(infor, ensure_ascii=False)
        return JsonResponse(jsonArr, safe=False)
    def get(self,request):
        response = StreamingHttpResponse(self.readFile("顾问产品促签.xlsx"))
        response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format("1.xlsx")

        return response
    def readFile(self, filename, chunk_size=512):
        with open(filename, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    def read_xls(self,set_produvt):
        table_name = "产品促签"
        workbook = xlwt.Workbook(encoding="UTF-8")
        worksheet = workbook.add_sheet(table_name)
        # 样式设置(可选)
        style = xlwt.XFStyle()  # 初始化样式（居中+加粗）
        style2 = xlwt.XFStyle() # 初始化样式（居中）
        font = xlwt.Font()  # 为样式创建字体
        font.bold = True  # 加粗
        # 水平居中
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        alignment.vert = xlwt.Alignment.VERT_CENTER
        style.alignment = alignment  # Add Alignment to Style
        style2.alignment = alignment # Add Alignment to Style
        style.font = font
        worksheet.col(0).width = 6110
        worksheet.col(1).width = 8110
        worksheet.write_merge(0, 0, 0, 1, '顾问产品促签统计', style)
        __num = 0
        for i,peopre in enumerate(set_produvt):
            worksheet.write(i+1+__num, 0, peopre['name'], style)
            worksheet.write(i + 1 + __num, 1, "促签人数", style2)
            __num += 1
            worksheet.write(__num+i+1, 1, peopre['all_num'], style2)
            __num += 1
            worksheet.write(i + 1 + __num, 1, "选定时间内总签约人数", style2)
            __num += 1
            worksheet.write(__num + i + 1, 1, peopre['the_current'], style2)
            __num += 1
            worksheet.write(i + 1 + __num, 1, "切片产品促签率", style2)
            __num += 1
            worksheet.write(__num + i + 1, 1, peopre['rate'], style2)
            __num += 1

        exist_file = os.path.exists("顾问产品促签.xlsx")
        if exist_file:
            os.remove(r"顾问产品促签.xlsx")
        workbook.save("顾问产品促签.xlsx")

class ConsultantOfficeView(APIView):

    def post(self,request):
        infor = {}
        set_office = []
        # try:
        strat_time = datetime.date(*map(int, request.data['start_personnelsales_time'].split('-')))
        stop_time = datetime.date(*map(int, request.data['stop_personnelsales_time'].split('-')))
        qutset_data = Academy.objects.filter(date_of_purchasing__range=(strat_time, stop_time))
        set_grade= ["8年级", "9年级", "10年级", "11年级", "12年级", "大一", "大二", "大三", "大四"]
        grade_classification = {"海本": {"1": 4, "2": 3, "3": 2, "4": 1, "5": 0},
                                "海研": {"1": 8, "2": 7, "3": 6, "4": 5}}
        for academies in qutset_data:

            student = Student.objects.filter(name=academies.name).all()[0]
            # 年级计算
            try:
                grade_num = grade_classification[student.application_level][
                    str(datetime.datetime.now().year - int(student.graduation_date[:4]))]
            except KeyError:
                grade_num = 8
            name_in = False
            name_location = 0
            for i, produvt_set in enumerate(set_office):
                if produvt_set["name"] == student.consultant:  # 顾问名字
                    name_in = True
                    name_location = i
            if name_in:
                try:
                    if student.customer_state == "已签约已购买":
                        set_office[name_location]["product_name"][academies.product_name][0] += 1
                    if "已签约" in student.customer_state:
                        set_office[name_location]["product_name"][academies.product_name][1] += 1
                except:
                    if student.customer_state == "已签约已购买":
                        da_ = [[1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1]]
                        da_[grade_num][0] +=1
                        set_office[name_location]["product_name"][academies.product_name] = da_
                    if "已签约" in student.customer_state:
                        da_ = [[1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1]]
                        da_[grade_num][1] +=1
                        set_office[name_location]["product_name"][academies.product_name] = da_
            else:
                if "已签约" in student.customer_state:
                    produvt_dict = {
                        "name":student.consultant,
                        "grade":set_grade,
                        "product_name": {academies.product_name:[[1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1]]},
                    }
                    if student.customer_state == "已签约已购买":
                        produvt_dict["product_name"][academies.product_name][grade_num][0] +=1
                    if "已签约" in student.customer_state:
                        produvt_dict["product_name"][academies.product_name][grade_num][1] += 1
                    set_office.append(produvt_dict)
        for set_o in set_office:
            for key,values in set_o["product_name"].items():
                for it,value in enumerate(values):
                    if value[0] == 1 and value[1] ==1:
                        set_o["product_name"][key][it] = 0
                    else:
                        # set_o["product_name"][key][it] = '{:.2f}%'.format(value[0] / value[1] * 100)
                        set_o["product_name"][key][it] = value[0]
        infor["status"] = 200

        infor["office"] = set_office
        # except:
        #     infor["res"] = []
        #     infor["status"] = 202
        self.read_xls(set_office)
        jsonArr = json.dumps(infor, ensure_ascii=False)
        return JsonResponse(jsonArr, safe=False)
    def get(self,request):
        response = StreamingHttpResponse(self.readFile("顾问在办.xlsx"))
        response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format("1.xlsx")

        return response
    def readFile(self, filename, chunk_size=512):
        with open(filename, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    def read_xls(self,set_produvt):
        table_name = "顾问在办购买"
        workbook = xlwt.Workbook(encoding="UTF-8")
        worksheet = workbook.add_sheet(table_name)
        # 样式设置(可选)
        style = xlwt.XFStyle()  # 初始化样式（居中+加粗）
        style2 = xlwt.XFStyle() # 初始化样式（居中）
        font = xlwt.Font()  # 为样式创建字体
        font.bold = True  # 加粗
        # 水平居中
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        alignment.vert = xlwt.Alignment.VERT_CENTER
        style.alignment = alignment  # Add Alignment to Style
        style2.alignment = alignment # Add Alignment to Style
        style.font = font
        worksheet.col(0).width = 8110
        worksheet.write_merge(0, 0, 0, 12, '顾问在办购买统计', style)
        __num = 0
        for i,peopre in enumerate(set_produvt):
            worksheet.write(i+1+__num, 0, peopre['name'], style)
            for num,grade in enumerate(peopre['grade']):
                worksheet.write(__num+i+1, num+1, grade, style2)

            for key,value in peopre['product_name'].items():
                worksheet.write(__num+i+2, 0, key, style2)
                for month_num, month in enumerate(value):
                    if month !=0:
                        worksheet.write(__num+i+2, month_num + 1, str(month), style2)
                __num+=1
            __num+=2
        exist_file = os.path.exists("顾问在办.xlsx")
        if exist_file:
            os.remove(r"顾问在办.xlsx")
        workbook.save("顾问在办.xlsx")
class SalesstatiSticsView(APIView):
    def post(self,request):
        infor = {}
        set_produvt = []
        set_month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                     "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        try:
            strat_time = datetime.date(*map(int, request.data['start_personnelsales_time'].split('-')))
            stop_time = datetime.date(*map(int, request.data['stop_personnelsales_time'].split('-')))
            qutset_data = Academy.objects.filter(date_of_purchasing__range=(strat_time, stop_time))
            for academies in qutset_data:
                name_in = False
                name_location = 0
                academies.date_of_purchasing = datetime.datetime.strptime(academies.date_of_purchasing, '%Y-%m-%d')
                _month = academies.date_of_purchasing.month
                for i, produvt_set in enumerate(set_produvt):
                    if produvt_set["name"] == academies.sales:  # 顾问名字
                        name_in = True
                        name_location = i
                if name_in:
                    try:
                        set_produvt[name_location]["product_name"][academies.product_name][_month] += 1
                    except:
                        set_produvt[name_location]["product_name"][academies.product_name] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                        set_produvt[name_location]["product_name"][academies.product_name][_month] += 1
                else:
                    produvt_dict = {
                        "name":academies.sales,
                        "set_month":set_month,
                        "product_name": {academies.product_name:[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
                    }
                    produvt_dict["product_name"][academies.product_name][_month] = 1
                    set_produvt.append(produvt_dict)

            infor["status"] = 200
            infor["produvt"] = set_produvt
        except:
            infor["res"] = []
            infor["status"] = 202
        self.read_xls(set_produvt)
        jsonArr = json.dumps(infor, ensure_ascii=False)
        return JsonResponse(jsonArr, safe=False)
    def get(self,request):
        response = StreamingHttpResponse(self.readFile("销售人员.xlsx"))
        response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format("1.xlsx")

        return response
    def readFile(self, filename, chunk_size=512):
        with open(filename, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    def read_xls(self,set_produvt):
        table_name = "销售人员统计"
        workbook = xlwt.Workbook(encoding="UTF-8")
        worksheet = workbook.add_sheet(table_name)
        # 样式设置(可选)
        style = xlwt.XFStyle()  # 初始化样式（居中+加粗）
        style2 = xlwt.XFStyle() # 初始化样式（居中）
        font = xlwt.Font()  # 为样式创建字体
        font.bold = True  # 加粗
        # 水平居中
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        alignment.vert = xlwt.Alignment.VERT_CENTER
        style.alignment = alignment  # Add Alignment to Style
        style2.alignment = alignment # Add Alignment to Style
        style.font = font
        worksheet.col(0).width = 8110
        worksheet.write_merge(0, 0, 0, 12, '销售人员统计', style)
        __num = 0
        for i,peopre in enumerate(set_produvt):
            worksheet.write(i+1+__num, 0, peopre['name'], style)
        # exist_file = os.path.exists("销售人员.xlsx")
        # if exist_file:
        #     os.remove(r"销售人员.xlsx")
        # workbook.save("销售人员.xlsx")
            for num,month in enumerate(peopre['set_month']):
                worksheet.write(__num+i+1, num+1, month, style2)

            for key,value in peopre['product_name'].items():
                worksheet.write(__num+i+2, 0, key, style2)
                for month_num, month in enumerate(value):
                    if month >0:
                        worksheet.write(__num+i+2, month_num + 1, month, style2)
                __num+=1
            __num+=2
        exist_file = os.path.exists("销售人员.xlsx")
        if exist_file:
            os.remove(r"销售人员.xlsx")
        workbook.save("销售人员.xlsx")



class AfterBuyView(APIView):


    def post(self,request):
        infor = {}
        # try:
        set_products_after = []
        set_sales_after = []
        strat_time = datetime.date(*map(int, request.data['start_after_time'].split('-')))
        stop_time = datetime.date(*map(int, request.data['stop_after_time'].split('-')))
        purchasings = Academy.objects.filter(date_of_purchasing__range=(strat_time, stop_time)).order_by("date_of_purchasing")
        for purchasing in purchasings:
            product_name_in = False
            sales_name_in = False
            for i,sales_set in enumerate(set_sales_after):
                if sales_set["sales_staff"] == purchasing.sales:
                    sales_name_in = True
                    sales_name_location = i
            for i, product_set in enumerate(set_products_after):
                if product_set["product_name"] == purchasing.product_name:
                    product_name_in = True
                    product_name_location = i
            if product_name_in:
                if 0 < set_products_after[product_name_location]["customer_name"].count(purchasing.name) < 2:
                    set_products_after[product_name_location]["repurchase_trigger"]+=1
                set_products_after[product_name_location]["customer_name"].append(purchasing.name)
                set_products_after[product_name_location]["total_number"] += 1
            else:
                product_after_dict = {
                    "product_name":purchasing.product_name,
                    "repurchase_trigger":0,
                    "total_number": 1,
                    "after_buy_rate": 0,
                    "customer_name":[purchasing.name],
                }
                set_products_after.append(product_after_dict)
            if sales_name_in:
                if 0 < set_sales_after[sales_name_location]["user_name"].count(purchasing.name) < 2:
                    set_sales_after[sales_name_location]["purchase_num"]+=1

                set_sales_after[sales_name_location]["user_name"].append(purchasing.name)
                set_sales_after[sales_name_location]["total_num"] += 1
            else:
                sales_after_dict = {
                                "sales_staff": purchasing.sales,
                                "purchase_num": 0,
                                "total_num": 1,
                                "after_buying_rate": 0,
                                "user_name":[purchasing.name]
                            }
                set_sales_after.append(sales_after_dict)
        for set_data in set_products_after:
            set_data["after_buy_rate"] = '{:.2f}%'.format(set_data["repurchase_trigger"]/set_data["total_number"]* 100)
        for sales_data in set_sales_after:
            sales_data["after_buying_rate"] = '{:.2f}%'.format(sales_data["purchase_num"]/sales_data["total_num"]* 100)
        infor["purchase_res"] = set_products_after
        infor["sales_res"] = set_sales_after
        infor["status"] = 200

        table_name = "复购率"
        workbook = xlwt.Workbook(encoding="UTF-8")
        worksheet = workbook.add_sheet(table_name)
        # 样式设置(可选)
        style = xlwt.XFStyle()  # 初始化样式（居中+加粗）
        style2 = xlwt.XFStyle() # 初始化样式（居中）
        font = xlwt.Font()  # 为样式创建字体
        font.bold = True  # 加粗
        # 水平居中
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        alignment.vert = xlwt.Alignment.VERT_CENTER
        style.alignment = alignment  # Add Alignment to Style
        style2.alignment = alignment # Add Alignment to Style
        style.font = font
        worksheet.col(0).width = 6110
        worksheet.col(1).width = 4110
        worksheet.col(2).width = 6110
        worksheet.col(3).width = 4110
        worksheet.write_merge(0, 0, 0, 3, '复购率统计', style)
        worksheet.write(1, 0, '产品复购率', style)
        worksheet.write(2, 1, "复购触发次数", style2)
        worksheet.write(2, 2, "时间范围内总购买数", style2)
        worksheet.write(2, 3, "复购触发率", style2)
        for i, data_dist in enumerate(set_products_after):
            worksheet.write(3+i, 0, data_dist["product_name"], style2)
            worksheet.write(3+i, 1, data_dist["repurchase_trigger"], style2)
            worksheet.write(3+i, 2, data_dist["total_number"], style2)
            worksheet.write(3+i, 3, data_dist["after_buy_rate"], style2)
        _num = len(set_products_after)
        worksheet.write(5 + _num, 0, "销售人员复购率", style)
        worksheet.write(6 + _num, 1, "复购出现次数", style)
        worksheet.write(6 + _num, 2, "总销售计数", style)
        worksheet.write(6 + _num, 3, "复购率", style)
        for i, data_dist in enumerate(set_sales_after):
            worksheet.write(7+_num+i, 0, data_dist["sales_staff"], style2)
            worksheet.write(7+_num+i, 1, data_dist["purchase_num"], style2)
            worksheet.write(7+_num+i, 2, data_dist["total_num"], style2)
            worksheet.write(7+_num+i, 3, data_dist["after_buying_rate"], style2)
        exist_file = os.path.exists("复购率.xlsx")
        if exist_file:
            os.remove(r"复购率.xlsx")
        workbook.save("复购率.xlsx")
        jsonArr = json.dumps(infor, ensure_ascii=False)
        return JsonResponse(jsonArr, safe=False)

    def get(self,request):
        response = StreamingHttpResponse(self.readFile("复购率.xlsx"))
        response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format("1.xlsx")

        return response

    def readFile(self, filename, chunk_size=512):
        with open(filename, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

class ProductsToBuyView(APIView):

    def post(self,request):
        infor = {}
        # try:
        set_products_buy = []
        strat_time = datetime.date(*map(int, request.data['start_buy_time'].split('-')))
        stop_time = datetime.date(*map(int, request.data['stop_buy_time'].split('-')))
        purchasings = Academy.objects.filter(date_of_purchasing__range=(strat_time, stop_time))
        # 单个顾问统计
        grade_classification = {"海本":{"1":"12年级","2":"11年级","3":"10年级","4":"9年级","5":"8年级"},
                                "海研": {"1": "大四", "2": "大三", "3": "大二", "4": "大一"}}
        id_num = 1
        for purchasing in purchasings:
            student = Student.objects.filter(name=purchasing.name).all()[0]
            name_in = False
            name_location = 0
            # 年级计算
            try:
                current_grade = grade_classification[student.application_level][str(datetime.datetime.now().year - int(student.graduation_date[:4]))]
            except KeyError :
                current_grade = "大四"
            for i,product_set in enumerate(set_products_buy):
                if product_set["name"] == purchasing.product_name:
                    name_in = True
                    name_location = i
            if name_in:
                if student.customer_state in set_products_buy[name_location]["customer_state"].keys():
                    set_products_buy[name_location]["customer_state"][student.customer_state]+=1
                else:
                    set_products_buy[name_location]["source"][purchasing.source] = 1
                if purchasing.source in set_products_buy[name_location]["source"].keys():
                    set_products_buy[name_location]["source"][purchasing.source]+=1
                else:
                    set_products_buy[name_location]["source"][purchasing.source] = 1
                if current_grade in set_products_buy[name_location]["current_grade"].keys():
                    set_products_buy[name_location]["current_grade"][current_grade] += 1
                else:
                    set_products_buy[name_location]["current_grade"][current_grade] = 1
                if student.area in set_products_buy[name_location]["area"].keys():
                    set_products_buy[name_location]["area"][student.area] += 1
                else:
                    set_products_buy[name_location]["area"][student.area] = 1
                set_products_buy[name_location]["sales"][purchasing.sales + purchasing.date_of_purchasing]  = 1
                if student.major in set_products_buy[name_location]["major"].keys():
                    set_products_buy[name_location]["major"][student.major] += 1
                else:
                    set_products_buy[name_location]["major"][student.major] = 1
                if student.school_type in set_products_buy[name_location]["school_type"].keys():
                    set_products_buy[name_location]["school_type"][student.school_type] += 1
                else:
                    set_products_buy[name_location]["school_type"][student.school_type] = 1
                if student.curriculum_system in set_products_buy[name_location]["curriculum_system"].keys():
                    set_products_buy[name_location]["curriculum_system"][student.curriculum_system] += 1
                else:
                    set_products_buy[name_location]["curriculum_system"][student.curriculum_system] = 1

            else:
                student_dict = {
                    "id":id_num,
                    "name":purchasing.product_name,
                    "customer_state":{student.customer_state:1},
                    "source": {purchasing.source:1},
                    "current_grade": {current_grade: 1},
                    "area": {student.area: 1},
                    "sales": {purchasing.sales+ purchasing.date_of_purchasing: 1},
                    "major": {student.major: 1},
                    "school_type": {student.school_type: 1},
                    "curriculum_system": {student.curriculum_system: 1}
                }
                id_num+=1
                set_products_buy.append(student_dict)
        for set_data in set_products_buy:
            for set_key,set_value in set_data["customer_state"].items():
                # customer_num = Student.objects.filter(Q(customer_state=set_key)&Q(date_of_purchasing__range=(strat_time, stop_time))).count()
                customer_num = Student.objects.filter(customer_state=set_key).count()
                set_data["customer_state"][set_key] = '{:.2f}%'.format(set_value/customer_num* 100)
        infor["res"] = set_products_buy
        infor["status"] = 200
        # except:
        #     infor["res"] = []
        #     infor["status"] = 202
        self.read_xls(set_products_buy)
        jsonArr = json.dumps(infor, ensure_ascii=False)
        return JsonResponse(jsonArr, safe=False)
    def get(self,request):
        response = StreamingHttpResponse(self.readFile("产品购买情况.xlsx"))
        response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format("1.xlsx")

        return response
    def readFile(self, filename, chunk_size=512):
        with open(filename, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    def read_xls(self,set_produvt):
        table_name = "产品购买情况"
        workbook = xlwt.Workbook(encoding="UTF-8")
        worksheet = workbook.add_sheet(table_name)
        # 样式设置(可选)
        style = xlwt.XFStyle()  # 初始化样式（居中+加粗）
        style2 = xlwt.XFStyle() # 初始化样式（居中）
        font = xlwt.Font()  # 为样式创建字体
        font.bold = True  # 加粗
        # 水平居中
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        alignment.vert = xlwt.Alignment.VERT_CENTER
        style.alignment = alignment  # Add Alignment to Style
        style2.alignment = alignment # Add Alignment to Style
        style.font = font
        worksheet.col(0).width = 8110
        worksheet.col(1).width = 8110
        worksheet.col(2).width = 8110
        worksheet.col(3).width = 8110
        worksheet.col(4).width = 8110
        worksheet.col(5).width = 8110
        worksheet.col(6).width = 8110
        worksheet.col(7).width = 8110
        worksheet.col(8).width = 8110
        worksheet.col(9).width = 8110
        worksheet.col(10).width = 8110
        worksheet.col(11).width = 8110
        worksheet.col(12).width = 8110
        worksheet.col(13).width = 8110
        worksheet.col(14).width = 8110
        worksheet.col(15).width = 8110
        # worksheet.write_merge(0, 0, 0, 12, '销售人员统计', style)
        __num = 0
        for i,peopre in enumerate(set_produvt):
            worksheet.write(i + __num, 0, "产品名称", style2)
            worksheet.write(i+__num, 1, peopre['name'], style)
            __num+=1
            worksheet.write(i + __num, 0, "客户状态分布", style2)
            num = 0
            for key, value in peopre['customer_state'].items():
                worksheet.write(__num + i, 1 + num, key, style2)
                worksheet.write(__num+1 + i, 1 + num, value, style2)
                num+=1
            __num += 2
            worksheet.write(i + __num, 0, "客户来源分布", style2)
            num = 0
            for key, value in peopre['source'].items():
                worksheet.write(__num + i, 1 + num, key, style2)
                worksheet.write(__num+1 + i, 1 + num, value, style2)
                num+=1
            __num += 2
            worksheet.write(i + __num, 0, "当前年级分布", style2)
            num = 0
            for key, value in peopre['current_grade'].items():
                worksheet.write(__num + i, 1 + num, key, style2)
                worksheet.write(__num+1 + i, 1 + num, value, style2)
                num+=1
            __num += 2
            worksheet.write(i + __num, 0, "地区分布", style2)
            num = 0
            for key, value in peopre['area'].items():
                worksheet.write(__num + i, 1 + num, key, style2)
                worksheet.write(__num+1 + i, 1 + num, value, style2)
                num+=1
            __num += 2
            worksheet.write(i + __num, 0, "销售人员分布", style2)
            num = 0
            for key, value in peopre['sales'].items():
                worksheet.write(__num + i, 1 + num, key, style2)
                worksheet.write(__num+1 + i, 1 + num, value, style2)
                num+=1
            __num += 2
            worksheet.write(i + __num, 0, "专业方向分布", style2)
            num = 0
            for key, value in peopre['major'].items():
                worksheet.write(__num + i, 1 + num, key, style2)
                worksheet.write(__num+1 + i, 1 + num, value, style2)
                num+=1
            __num += 2
            worksheet.write(i + __num, 0, "学校类型分布", style2)
            num = 0
            for key, value in peopre['school_type'].items():
                worksheet.write(__num + i, 1 + num, key, style2)
                worksheet.write(__num+1 + i, 1 + num, value, style2)
                num+=1
            __num += 2
            worksheet.write(i + __num, 0, "课程体系分布", style2)
            num = 0
            for key, value in peopre['curriculum_system'].items():
                worksheet.write(__num + i, 1 + num, key, style2)
                worksheet.write(__num+1 + i, 1 + num, value, style2)
                num+=1
            __num += 2
        exist_file = os.path.exists("产品购买情况.xlsx")
        if exist_file:
            os.remove(r"产品购买情况.xlsx")
        workbook.save("产品购买情况.xlsx")
class CustomerConversionaView(APIView):

    def post(self,request):
        infor = {}
        strat_time = datetime.date(*map(int, request.data['start_consulting_time'].split('-')))
        stop_time = datetime.date(*map(int, request.data['stop_consulting_time'].split('-')))
        little_assistant = Student.objects.filter((Q(customer_state="已分配未购买") | Q(customer_state="已分配已购买"))&Q(transfer_time__range=(strat_time, stop_time)))
        little_assistant_list = list(set(Student.objects.values_list('little_assistant', flat=True)))

        set_area = []  # 地区统计
        set_school_type = [] # 学校类型统计
        set_school_name = [] # 学校名统计
        set_grade = []  # 年级统计
        set_curriculum_system = [] # 课程体系占比统计
        set_consultant = [] # 所属顾问占比统计
        set_transfer_time = [] # 转咨询平均时长
        set_conversion_rate = [] # 转化率
        for student in little_assistant:
            area_name_in = True
            for i,area in enumerate(set_area):
                if area["小助手"] == student.little_assistant:
                    area_name_in = False
                    try:
                        set_area[i][student.area] +=1
                    except:
                        set_area[i][student.area] = 1
                    break
            if area_name_in:
                dict_area = {}  # 地区统计
                dict_area["小助手"] = "未知" if student.little_assistant=="" else student.little_assistant
                try:
                    dict_area[student.area] +=1
                except:
                    dict_area[student.area] = 1
                set_area.append(dict_area)
            school_type_name_in = True
            for i,school_type in enumerate(set_school_type):
                if school_type["小助手"] == student.little_assistant:
                    school_type_name_in = False
                    try:
                        set_school_type[i][student.school_type] +=1
                    except:
                        set_school_type[i][student.school_type] = 1
                    break
            if school_type_name_in:
                dict_school_type = {}
                dict_school_type["小助手"] = "未知" if student.little_assistant == "" else student.little_assistant
                try:
                    dict_school_type[student.school_type] += 1
                except:
                    dict_school_type[student.school_type] = 1
                set_school_type.append(dict_school_type)
            school_name_in = True
            for i,school_name in enumerate(set_school_name):
                if school_name["小助手"] == student.little_assistant:
                    school_name_in = False
                    try:
                        set_school_name[i][student.school] +=1
                    except:
                        set_school_name[i][student.school] = 1
                    break
            if school_name_in:
                dict_school_name = {}
                dict_school_name["小助手"] = "未知" if student.little_assistant == "" else student.little_assistant
                try:
                    dict_school_name[student.school] += 1
                except:
                    dict_school_name[student.school] = 1
                set_school_name.append(dict_school_name)
            grade_in = True
            # grade_list = ["小助手", "12年级", "11年级", "10年级", "9年级", "8年级", "大四", "大三", "大二", "大一"]
            grade_classification = {"海本": {"1": "12年级", "2": "11年级", "3": "10年级", "4": "9年级", "5": "8年级"},
                                    "海研": {"1": "大四", "2": "大三", "3": "大二", "4": "大一"}}
            try:
                diff_year = int(student.graduation_date[:4]) - datetime.datetime.now().year
                current_grade = grade_classification[student.application_level][str(diff_year)] if diff_year>0 else "大四"
            except:
                current_grade = "大四"

            for i,grade in enumerate(set_grade):
                if grade["小助手"] == student.little_assistant:
                    grade_in = False
                    try:
                        set_grade[i][current_grade] +=1
                    except:
                        set_grade[i][current_grade] = 1
                    break
            if grade_in:
                dict_application_level = {}
                dict_application_level["小助手"] = "未知" if student.little_assistant == "" else student.little_assistant
                try:
                    dict_application_level[current_grade] += 1
                except:
                    dict_application_level[current_grade] = 1
                set_grade.append(dict_application_level)

            curriculum_system_name_in = True
            for i,curriculum_system in enumerate(set_curriculum_system):
                if curriculum_system["小助手"] == student.little_assistant:
                    curriculum_system_name_in = False
                    try:
                        set_curriculum_system[i][student.curriculum_system] +=1
                    except:
                        set_curriculum_system[i][student.curriculum_system] = 1
                    break

            if curriculum_system_name_in:
                dict_curriculum_system = {}
                dict_curriculum_system["小助手"] = "未知" if student.little_assistant == "" else student.little_assistant
                try:
                    dict_curriculum_system[student.curriculum_system] += 1
                except:
                    dict_curriculum_system[student.curriculum_system] = 1
                set_curriculum_system.append(dict_curriculum_system)

            consultant_name_in = True
            for i,consultant in enumerate(set_consultant):
                if consultant["小助手"] == student.little_assistant:
                    consultant_name_in = False
                    try:
                        set_consultant[i][student.consultant] +=1
                    except:
                        set_consultant[i][student.consultant] = 1
                    break

            if consultant_name_in:
                dict_consultant = {}
                dict_consultant["小助手"] = "未知" if student.little_assistant == "" else student.little_assistant
                try:
                    dict_consultant[student.consultant] += 1
                except:
                    dict_consultant[student.consultant] = 1
                set_consultant.append(dict_consultant)


            try:
                current_time = datetime.date(*map(int, student.transfer_time.split('-')))
            except:
                continue
            transfer_time = 0
            if student.transfer_time:
                add_time = datetime.date(*map(int, student.date_to_add.split('-')))
                transfer_time = (current_time - add_time).days
            transfer_name_in = True
            for i,consultant in enumerate(set_transfer_time):
                if consultant["小助手"] == student.little_assistant:
                    transfer_name_in = False
                    set_transfer_time[i]["总数量"] +=1
                    set_transfer_time[i]["总时间"] += transfer_time
                    break

            if transfer_name_in:
                transfer_time_list = ['小助手', "总数量", "总时间", "转咨询平均时长(/天)"]
                dict_transfer_time = dict.fromkeys(transfer_time_list, 0)
                dict_transfer_time["小助手"] = "未知" if student.little_assistant == "" else student.little_assistant
                dict_transfer_time["总数量"] += 1
                dict_transfer_time["总时间"] = transfer_time
                set_transfer_time.append(dict_transfer_time)


        # 转化率
        grade_classification = {"海本":{"1":"12年级","2":"11年级","3":"10年级","4":"9年级","5":"8年级"},
                                "海研": {"1": "大四", "2": "大三", "3": "大二", "4": "大一"}}
        conversion_rate_list = ["小助手","12年级","11年级","10年级","9年级","8年级","大四", "大三", "大二", "大一","总转咨询率"]
        for assistant in little_assistant_list:
            if assistant=="":
                assistant = "未知"
            dict_conversion_rate = {}
            dict_conversion_rate["小助手"] = assistant
            dict_conversion_rate["总转咨询率"] = [0,0]
            all_studetn = Student.objects.filter( Q(little_assistant=assistant))
            for student in all_studetn:
                try:
                    diff_year = int(student.graduation_date[:4])- datetime.datetime.now().year
                    current_grade = grade_classification[student.application_level][str(diff_year)]
                    try:
                        dict_conversion_rate["总转咨询率"][1] += 1
                        dict_conversion_rate[current_grade][1] +=1
                        if student.transfer_time:
                            dict_conversion_rate[current_grade][0] += 1
                            dict_conversion_rate["总转咨询率"][0] += 1
                    except:
                        dict_conversion_rate[current_grade] = [0,1]
                        if student.transfer_time:
                            dict_conversion_rate[current_grade][0] += 1
                            dict_conversion_rate["总转咨询率"][0] += 1
                except:
                    try:
                        dict_conversion_rate["总转咨询率"][1] += 1
                        dict_conversion_rate["大四"][1] += 1
                        if student.transfer_time:
                            dict_conversion_rate["大四"][0] += 1
                            dict_conversion_rate["总转咨询率"][0] += 1
                    except:
                        dict_conversion_rate["大四"] = [0,1]
                        if student.transfer_time:
                            dict_conversion_rate["大四"][0] += 1
                            dict_conversion_rate["总转咨询率"][0] += 1

            for _gread  in dict_conversion_rate.keys():
                if _gread =="小助手":
                    continue
                if dict_conversion_rate[_gread][1]>0:
                    dict_conversion_rate[_gread] = '{:.2f}%'.format((dict_conversion_rate[_gread][0]/dict_conversion_rate[_gread][1])*100)
                else:
                    dict_conversion_rate[_gread] = 0
            set_conversion_rate.append(dict_conversion_rate)

        # 签约率
        set_signing = []
        transfer_time_list = ['小助手', "签约率"]
        for assistant in little_assistant_list:
            total_number = 0
            signing_number = 0
            if assistant=="":
                assistant = "未知"
            dict_transfer_time = dict.fromkeys(transfer_time_list, 0)
            dict_transfer_time["小助手"] = assistant
            all_studetn = Student.objects.filter(little_assistant=assistant)
            for student in all_studetn:
                try:
                    current_time = datetime.date(*map(int, student.transfer_time.split('-')))
                except:
                    continue
                if strat_time <= current_time <= stop_time:
                    total_number+=1
                    if "已签约" in student.customer_state:
                        signing_number+=1

            if signing_number>0:
                dict_transfer_time["签约率"] = '{:.2f}%'.format(signing_number/total_number*100)
            else:
                continue
            set_signing.append(dict_transfer_time)
        for tran_num, trans_data in enumerate(set_transfer_time):
            trans_data['转咨询平均时长(/天)'] = round(trans_data['总时间']/trans_data['总数量'],2)
        infor["area_data"] = set_area
        infor["set_school_type"] = set_school_type
        infor["school"] = set_school_name
        infor["grade"] = set_grade
        infor["curriculum_system"] = set_curriculum_system
        infor["consultant"] = set_consultant
        infor["transfer_time"] = set_transfer_time
        infor["conversion_rate"] = set_conversion_rate
        infor["signing"] = set_signing
        jsonArr = json.dumps(infor, ensure_ascii=False)
        return JsonResponse(jsonArr, safe=False)
class ResourceanAlysisView(APIView):

    def post(self,request):
        infor = {}
        strat_time = datetime.date(*map(int, request.data['start_resource_time'].split('-')))
        stop_time = datetime.date(*map(int, request.data['stop_resource_time'].split('-')))
        little_assistant = Student.objects.filter((Q(customer_state="未分配未购买") | Q(customer_state="未分配已购买"))&Q(date_to_add__range=(strat_time, stop_time)))
        set_source = [] # 资源来源
        ser_gender = [] # 性别
        ser_application_level = [] # 申请层级
        set_graduation_date = [] # 申请层级入学时间
        set_area = []  # 地区统计
        set_identity = [] # 客户身份占比
        set_school_type = [] # 学校类型统计
        set_school_name = [] # 学校名统计
        set_curriculum_system = [] # 课程体系占比统计
        set_major = [] # 专业方向
        set_target_country= []  # 专业方向
        for student in little_assistant:
            source_name_in = True
            source = "未知" if student.source=="" else student.source
            for i,source_data in enumerate(set_source):
                if source_data["小助手"] == student.little_assistant:
                    source_name_in = False
                    try:
                        set_source[i][source] +=1
                    except:
                        set_source[i][source] = 1
                    break
            if source_name_in:
                dict_source = {}
                dict_source["小助手"] = "未知" if student.little_assistant=="" else student.little_assistant
                try:
                    dict_source[source] +=1
                except:
                    dict_source[source] = 1
                set_source.append(dict_source)
            gender_name_in = True
            gender = "未知" if student.gender == "" else student.gender
            for i,genderdata in enumerate(ser_gender):
                if genderdata["小助手"] == student.little_assistant:
                    gender_name_in = False
                    try:
                        ser_gender[i][gender] +=1
                    except:
                        ser_gender[i][gender] = 1
                    break
            if gender_name_in:
                dict_gender = {}  #资源来源
                dict_gender["小助手"] = "未知" if student.little_assistant=="" else student.little_assistant
                try:
                    dict_gender[gender] +=1
                except:
                    dict_gender[gender] = 1
                ser_gender.append(dict_gender)
            application_level_name_in = True
            application_level = "未知" if student.application_level == "" else student.application_level
            for i,application_leveldata in enumerate(ser_application_level):
                if application_leveldata["小助手"] == student.little_assistant:
                    application_level_name_in = False
                    try:
                        ser_application_level[i][application_level] +=1
                    except:
                        ser_application_level[i][application_level] = 1
                    break
            if application_level_name_in:
                dict_application_level = {}  #申请层级
                dict_application_level["小助手"] = "未知" if student.little_assistant=="" else student.little_assistant
                try:
                    dict_application_level[application_level] +=1
                except:
                    dict_application_level[application_level] = 1
                ser_application_level.append(dict_application_level)
            graduation_date_name_in = True
            for i,graduation_date in enumerate(set_graduation_date):
                if graduation_date["小助手"] == student.little_assistant:
                    graduation_date_name_in = False
                    try:
                        set_graduation_date[i][student.graduation_date] +=1
                    except:
                        set_graduation_date[i][student.graduation_date] = 1
                    break
            if graduation_date_name_in:
                dict_graduation_date = {}  # 申请层级入学时间
                dict_graduation_date["小助手"] = "未知" if student.little_assistant=="" else student.little_assistant
                try:
                    dict_graduation_date[student.graduation_date] +=1
                except:
                    dict_graduation_date[student.graduation_date] = 1
                    set_graduation_date.append(dict_graduation_date)
            area_name_in = True
            for i,area in enumerate(set_area):
                if area["小助手"] == student.little_assistant:
                    area_name_in = False
                    try:
                        set_area[i][student.area] +=1
                    except:
                        set_area[i][student.area] = 1
                    break
            if area_name_in:
                dict_area = {}  # 地区统计
                dict_area["小助手"] = "未知" if student.little_assistant=="" else student.little_assistant
                try:
                    dict_area[student.area] +=1
                except:
                    dict_area[student.area] = 1
                set_area.append(dict_area)

            identity_name_in = True
            identity = "未知" if student.identity == "" else student.identity
            for i, area in enumerate(set_identity):
                if area["小助手"] == student.little_assistant:
                    identity_name_in = False
                    try:
                        set_identity[i][identity] += 1
                    except:
                        set_identity[i][identity] = 1
                    break
            if identity_name_in:
                dict_identity = {} # 客户身份
                dict_identity["小助手"] = "未知" if student.little_assistant == "" else student.little_assistant
                try:
                    dict_identity[identity] += 1
                except:
                    dict_identity[identity] = 1
                set_identity.append(dict_identity)


            school_type_name_in = True
            for i,school_type in enumerate(set_school_type):
                if school_type["小助手"] == student.little_assistant:
                    school_type_name_in = False
                    try:
                        set_school_type[i][student.school_type] +=1
                    except:
                        set_school_type[i][student.school_type] = 1
                    break
            if school_type_name_in:
                dict_school_type = {}
                dict_school_type["小助手"] = "未知" if student.little_assistant == "" else student.little_assistant
                try:
                    dict_school_type[student.school_type] += 1
                except:
                    dict_school_type[student.school_type] = 1
                set_school_type.append(dict_school_type)
            school_name_in = True
            for i,school_name in enumerate(set_school_name):
                if school_name["小助手"] == student.little_assistant:
                    school_name_in = False
                    try:
                        set_school_name[i][student.school] +=1
                    except:
                        set_school_name[i][student.school] = 1
                    break
            if school_name_in:
                dict_school_name = {}
                dict_school_name["小助手"] = "未知" if student.little_assistant == "" else student.little_assistant
                try:
                    dict_school_name[student.school] += 1
                except:
                    dict_school_name[student.school] = 1
                set_school_name.append(dict_school_name)

            curriculum_system_name_in = True
            for i,curriculum_system in enumerate(set_curriculum_system):
                if curriculum_system["小助手"] == student.little_assistant:
                    curriculum_system_name_in = False
                    try:
                        set_curriculum_system[i][student.curriculum_system] +=1
                    except:
                        set_curriculum_system[i][student.curriculum_system] = 1
                    break

            if curriculum_system_name_in:
                dict_curriculum_system = {}
                dict_curriculum_system["小助手"] = "未知" if student.little_assistant == "" else student.little_assistant
                try:
                    dict_curriculum_system[student.curriculum_system] += 1
                except:
                    dict_curriculum_system[student.curriculum_system] = 1
                set_curriculum_system.append(dict_curriculum_system)

            major_name_in = True
            major = "未知" if student.major == "" else student.major
            for i,ma in enumerate(set_major):
                if ma["小助手"] == student.little_assistant:
                    major_name_in = False
                    try:
                        set_major[i][major] +=1
                    except:
                        set_major[i][major] = 1
                    break
            if major_name_in:
                dict_major = {}
                dict_major["小助手"] = "未知" if student.little_assistant == "" else student.little_assistant
                try:
                    dict_major[major] += 1
                except:
                    dict_major[major] = 1
                set_major.append(dict_major)

            target_country_name_in = True
            country = "未知" if student.target_country == "" else student.target_country
            for i, target_country in enumerate(set_target_country):
                if target_country["小助手"] == student.little_assistant:
                    target_country_name_in = False
                    try:
                        set_target_country[i][country] += 1
                    except:
                        set_target_country[i][country] = 1
                    break
            if target_country_name_in:
                dict_target_country = {}
                dict_target_country["小助手"] = "未知" if student.little_assistant == "" else student.little_assistant
                try:
                    dict_target_country[country] += 1
                except:
                    dict_target_country[country] = 1
                set_target_country.append(dict_target_country)
        infor['source_data'] = set_source
        infor['gender_data'] = ser_gender
        infor['application_level_data'] = ser_application_level
        infor['graduation_date'] = set_graduation_date
        infor["area_data"] = set_area
        infor["identity"] = set_identity
        infor["school_type"] = set_school_type
        infor["school"] = set_school_name
        infor["curriculum_system"] = set_curriculum_system
        infor['major'] = set_major
        infor['target_country'] = set_target_country
        jsonArr = json.dumps(infor, ensure_ascii=False)
        return JsonResponse(jsonArr, safe=False)

class CustomerContractView(APIView):

    def post(self,request):
        infor = {}
        set_signing_state = []
        strat_time = datetime.date(*map(int, request.data['start_signing_time'].split('-')))
        stop_time = datetime.date(*map(int, request.data['stop_signing_time'].split('-')))
        students = Student.objects.filter(
            (Q(customer_state="已签约未购买") | Q(customer_state="已签约已购买")| Q(customer_state="已分配未购买")| Q(customer_state="已分配已购买")| Q(customer_state="已流失未购买")| Q(customer_state="已流失已购买")) & Q(signing_time__range=(strat_time, stop_time)))
        # 单个顾问统计
        grade_classification = {"海本":{"1":"12年级","2":"11年级","3":"10年级","4":"9年级","5":"8年级"},
                                "海研": {"1": "大四", "2": "大三", "3": "大二", "4": "大一"}}
        buy_list = list(set(students.values_list('consultant', flat=True)))
        buy_dict = dict.fromkeys(buy_list, 0)
        lose_dict = dict.fromkeys(buy_list, 0)
        for student in students:
            student.signing_time = datetime.datetime.strptime(student.signing_time, '%Y-%m-%d')
            student.transfer_time = datetime.datetime.strptime(student.transfer_time, '%Y-%m-%d')
            if student.customer_state in ["已分配已购买","已分配未购买"]:
                buy_dict[student.consultant] +=1
                continue
            if student.customer_state in ["已流失未购买","已流失已购买"]:
                lose_dict[student.consultant] +=1
                continue
            if student.source not in ["老客户介绍", "前台电话"]:
                student.source = "市场部"
            name_in = False
            name_location = 0
            # 年级计算
            try:
                current_grade = grade_classification[student.application_level][str(datetime.datetime.now().year - int(student.graduation_date[:4]))]
            except KeyError :
                current_grade = "大四"
            for i,student_set in enumerate(set_signing_state):
                if student_set["name"] == student.consultant:
                    name_in = True
                    name_location = i
            if name_in:

                if student.source in set_signing_state[name_location]["source"].keys():
                    set_signing_state[name_location]["source"][student.source]+=1
                else:
                    set_signing_state[name_location]["source"][student.source] = 1
                if student.school_type in set_signing_state[name_location]["school_type"].keys():
                    set_signing_state[name_location]["school_type"][student.school_type] += 1
                else:
                    set_signing_state[name_location]["school_type"][student.school_type] = 1

                if student.school in set_signing_state[name_location]["school"].keys():
                    set_signing_state[name_location]["school"][student.school] += 1
                else:
                    set_signing_state[name_location]["school"][student.school] = 1

                if current_grade in set_signing_state[name_location]["current_grade"].keys():
                    set_signing_state[name_location]["current_grade"][current_grade] += 1
                else:
                    set_signing_state[name_location]["current_grade"][current_grade] = 1

                if student.curriculum_system in set_signing_state[name_location]["curriculum_system"].keys():
                    set_signing_state[name_location]["curriculum_system"][student.curriculum_system] += 1
                else:
                    set_signing_state[name_location]["curriculum_system"][student.curriculum_system] = 1

                set_signing_state[name_location]["average_signing"] += (student.signing_time - student.transfer_time).days
                set_signing_state[name_location]["all_number"] += 1

            else:
                student_dict = {
                    "name":student.consultant,
                    "source": {student.source:1},
                    "average_signing": (student.signing_time - student.transfer_time).days,
                    "school_type": {student.school_type:1},
                    "school": {student.school:1},
                    "current_grade": {current_grade:1},
                    "curriculum_system": {student.curriculum_system:1},
                    "contract_rate":0,
                    "turnover_rate":0,
                    "all_number":1
                }
                set_signing_state.append(student_dict)
        for set_data in set_signing_state:
            set_data["average_signing"] = set_data["average_signing"]/set_data["all_number"]
            set_data["contract_rate"] = '{:.2f}%'.format(set_data["all_number"]/(set_data["all_number"]+buy_dict[set_data["name"]])*100)
            set_data["turnover_rate"] = '{:.2f}%'.format(lose_dict[set_data["name"]]/(set_data["all_number"]+buy_dict[set_data["name"]])*100)
        infor["res"] = set_signing_state
        infor["status"] = 200
        # except:
        #     infor["res"] = []
        #     infor["status"] = 202
        self.read_xls(set_signing_state)
        jsonArr = json.dumps(infor, ensure_ascii=False)
        return JsonResponse(jsonArr, safe=False)

    def get(self,request):
        response = StreamingHttpResponse(self.readFile("签约状态.xlsx"))
        response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format("1.xlsx")

        return response
    def readFile(self, filename, chunk_size=512):
        with open(filename, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    def read_xls(self,set_signing_state):
        table_name = "签约状态"
        workbook = xlwt.Workbook(encoding="UTF-8")
        worksheet = workbook.add_sheet(table_name)
        # 样式设置(可选)
        style = xlwt.XFStyle()  # 初始化样式（居中+加粗）
        style2 = xlwt.XFStyle() # 初始化样式（居中）
        font = xlwt.Font()  # 为样式创建字体
        font.bold = True  # 加粗
        # 水平居中
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        alignment.vert = xlwt.Alignment.VERT_CENTER
        style.alignment = alignment  # Add Alignment to Style
        style2.alignment = alignment # Add Alignment to Style
        style.font = font
        worksheet.col(0).width = 8110
        worksheet.col(1).width = 8110
        worksheet.col(2).width = 8110
        worksheet.col(3).width = 8110
        worksheet.col(4).width = 8110
        worksheet.col(5).width = 8110
        worksheet.col(6).width = 8110
        worksheet.col(7).width = 8110
        worksheet.col(8).width = 8110
        worksheet.col(9).width = 8110
        worksheet.col(10).width = 8110
        worksheet.col(11).width = 8110
        worksheet.col(12).width = 8110
        worksheet.col(13).width = 8110
        worksheet.col(14).width = 8110
        worksheet.col(15).width = 8110
        # worksheet.write_merge(0, 0, 0, 12, '销售人员统计', style)
        __num = 0
        for i,peopre in enumerate(set_signing_state):
            worksheet.write(i + __num, 0, "顾问名字", style2)
            worksheet.write(i+__num, 1, peopre['name'], style)
            __num+=1
            worksheet.write(i + __num, 0, "资源类型分布", style2)
            num = 0
            for key, value in peopre['source'].items():
                worksheet.write(__num + i, 1 + num, key, style2)
                worksheet.write(__num+1 + i, 1 + num, value, style2)
                num+=1
            __num += 2
            worksheet.write(i + __num, 0, "客户来源分布", style2)
            num = 0
            for key, value in peopre['source'].items():
                worksheet.write(__num + i, 1 + num, key, style2)
                worksheet.write(__num+1 + i, 1 + num, value, style2)
                num+=1
            __num += 2
            worksheet.write(i + __num, 0, "签约时间", style2)
            worksheet.write(i + __num, 1, "平均签约时间", style2)
            num = 0
            # for key, value in peopre['current_grade'].items():
            #     worksheet.write(__num + i, 1 + num, key, style2)
            worksheet.write(__num+1 + i, 1 + num, peopre['average_signing'], style2)
            #     num+=1
            __num += 2
            worksheet.write(i + __num, 0, "学校类型分布", style2)
            num = 0
            for key, value in peopre['school_type'].items():
                worksheet.write(__num + i, 1 + num, key, style2)
                worksheet.write(__num+1 + i, 1 + num, value, style2)
                num+=1
            __num += 2
            worksheet.write(i + __num, 0, "学校名分布", style2)
            num = 0
            for key, value in peopre['school'].items():
                worksheet.write(__num + i, 1 + num, key, style2)
                worksheet.write(__num+1 + i, 1 + num, value, style2)
                num+=1
            __num += 2
            worksheet.write(i + __num, 0, "当前年级分布", style2)
            num = 0
            for key, value in peopre['current_grade'].items():
                worksheet.write(__num + i, 1 + num, key, style2)
                worksheet.write(__num+1 + i, 1 + num, value, style2)
                num+=1
            __num += 2
            worksheet.write(i + __num, 0, "课程体系分布", style2)
            num = 0
            for key, value in peopre['curriculum_system'].items():
                worksheet.write(__num + i, 1 + num, key, style2)
                worksheet.write(__num+1 + i, 1 + num, value, style2)
                num+=1
            __num += 2
            num = 0
            worksheet.write(i + __num, 0, "签约率", style2)
            worksheet.write(i + __num, 1, "签约率", style2)
            worksheet.write(__num + 1 + i, 1 + num, peopre['contract_rate'], style2)
            __num += 2
            num = 0
            worksheet.write(i + __num, 0, "流失率", style2)
            worksheet.write(i + __num, 1, "流失率", style2)
            worksheet.write(__num + 1 + i, 1 + num, peopre['turnover_rate'], style2)
            __num += 2
        exist_file = os.path.exists("签约状态.xlsx")
        if exist_file:
            os.remove(r"签约状态.xlsx")
        workbook.save("签约状态.xlsx")
class CommonAgeView(APIView):

    def post(self,request):
        datainfor = request.data
        studatas = Student.objects.filter(Q(customer_state=datainfor['customer_state'])).all()
        if studatas:
            stu_dist = {}
            sti_list = []
            for studata in studatas:
                if studata.gender is "":
                    studata.gender = "空"
                if studata.gender in stu_dist.keys():
                    stu_dist[studata.gender] +=1
                else:
                    stu_dist[studata.gender] = 1
                    sti_list.append(studata.gender)

            value_list = []
            for value in stu_dist.values():
                value_dist = {"value":value,"itemStyle":"yellow"}
                value_list.append(value_dist)

            infor = {
                "x_data":sti_list,
                "value_list":value_list,
                "status":200
            }
        else:
            infor = {
                "message":"未找到匹配用户",
                "status":202
            }

        jsonArr = json.dumps(infor, ensure_ascii=False)
        return JsonResponse(jsonArr, safe=False)


