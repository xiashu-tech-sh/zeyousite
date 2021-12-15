from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
import json
import pandas as pd
import numpy as np
# Create your views here.
import warnings
from students.models import Student
from academies.models import Academy
from django_pandas.io import read_frame
from django.forms.models import model_to_dict
from django.db.models import Q
import re
import datetime


class ProductAnalysisView(APIView):
    # 产品信息推荐学生
    def post(self, request):
        data = request.data
        # 申请层级
        app_level = data['application_level']
        # 专业方向
        app_major = data['major']
        # 学校类型
        difficulty = int(data['difficulty_level'])
        # 课程体系
        school_structure = data['curriculum_system']

        username = data['username']
        res = self.courses_for_students(app_level, app_major, school_structure, difficulty)
        res_dist = {}
        res_list = []
        for name in res:
            if data['identity']:
                info = Student.objects.filter(Q(name=name)).all()
                if info:
                    data_res = model_to_dict(info[0])
                    aca = Academy.objects.filter(name=name).all()
                    if aca:
                        for academies in aca:
                            infor_copy = data_res.copy()
                            acade = model_to_dict(academies)
                            try:
                                if res_list[-1]['product_name'] == acade["product_name"]:
                                    continue
                            except IndexError:
                                pass
                            infor_copy["product_name"] = acade["product_name"]
                            res_list.append(infor_copy)
                    else:
                        data_res["product_name"] = ''
                        res_list.append(data_res)
            else:
                info = Student.objects.filter(Q(name=name) & (Q(little_assistant=username) | Q(consultant=username) |
                                                              Q(service_consultant=username) | Q(
                    paper_writer=username))).all()
                if info:
                    data_res = model_to_dict(info[0])
                    aca = Academy.objects.filter(name=name).all()
                    if aca:
                        for academies in aca:
                            infor_copy = data_res.copy()
                            acade = model_to_dict(academies)
                            try:
                                if res_list[-1]['product_name'] == acade["product_name"]:
                                    continue
                            except IndexError:
                                pass
                            infor_copy["product_name"] = acade["product_name"]
                            res_list.append(infor_copy)
                    else:
                        data_res["product_name"] = ''
                        res_list.append(data_res)
        if res_list:
            res_dist["status"] = 200
        else:
            res_dist["status"] = 202
            res_dist["message"] = "未找到符合学生，请核对信息"
        res_dist["res_data"] = res_list
        jsonArr = json.dumps(res_dist, ensure_ascii=False)
        return JsonResponse(jsonArr, safe=False)

    def courses_for_students(self,app_level, app_major, school_structure, difficulty):
        data = Student.objects.all()
        cus = read_frame(qs=data, index_col="id")
        # %% 产品部分：产品编号
        data = Academy.objects.all()
        sales = read_frame(qs=data, index_col="id")
        # %% 产品部分：产品编号
        id = sales['product_name']
        id = set(id)
        id = dict(zip(id, range(sales.index[0], sales.index[-1])))
        sales['id'] = sales['product_name'].apply(lambda x: id[x])
        # %% 客户购买状态
        cus['df'] = cus['customer_state'].apply(lambda x: 1 if x == '已签约已购买' else 0)

        # %%
        customers = cus.loc[:,
                    ['name', 'wechat_num', 'school_type', 'curriculum_system', 'graduation_date', 'application_level',
                     'major', 'df']]
        customers.columns = ['name', 'wechat', 'school_type', 'structure', 'enter_time_raw', 'app_level', 'major','purchased_before']
        # %%
        customers['major1'] = customers['major'].apply(
            lambda x: str(x).split('+')[0] if str(x).split('+')[0] else np.nan)
        customers['major2'] = customers['major'].apply(
            lambda x: str(x).split('+')[1] if len(str(x).split('+')) > 1 else np.nan)
        customers['major3'] = customers['major'].apply(
            lambda x: str(x).split('+')[2] if len(str(x).split('+')) > 2 else np.nan)
        customers['major4'] = customers['major'].apply(
            lambda x: str(x).split('+')[3] if len(str(x).split('+')) > 3 else np.nan)
        del customers['major']
        customers["enter_time_raw"] = customers["enter_time_raw"].fillna("")
        curr_year = datetime.datetime.today().year
        customers['enter_time'] = customers['enter_time_raw'].apply(
            lambda x: int(x[:4]) if x[:4].isdigit() else curr_year)
        del customers['enter_time_raw']
        self.customers = customers

        self.qiepian = pd.read_excel(r"/home/Zeyou/ZeyouSite/apps/recommended/qiepianchanpin.xlsx", sheet_name="Sheet1")
        # self.qiepian = pd.read_excel(r"C:\Users\hhpba\Desktop\Zeyou\ZeyouSite\apps\recommended\qiepianchanpin.xlsx", sheet_name="Sheet1")

        potential_customers = self.customers[self.customers.structure == school_structure]
        stu = list(potential_customers['wechat'])
        score = [0] * len(stu)
        dic = dict(zip(stu, score))
        potential_customers["score"] = score
        potential_customers["score"][potential_customers.major1 == app_major] += 3
        potential_customers["score"][potential_customers.major2 == app_major] += 3
        potential_customers["score"][potential_customers.major3 == app_major] += 3
        potential_customers["score"][potential_customers.major4 == app_major] += 3
        self.app_level_mapping = {
            "国内国际学校": "国内国际学校",
            "美国高中": "国内国际学校",
            "美高": "国内国际学校",
            "海本转学": "海本",
            "本科转学": "海本",
            "海研": "海研",
            "海博": "海博",
            "海本": "海本",
        }
        # 申请层级
        if app_level in self.app_level_mapping:
            mapped_app_level = self.app_level_mapping[app_level]
        else:
            mapped_app_level = ""
        potential_customers["score"][
            (potential_customers.app_level == app_level) | (potential_customers.app_level == mapped_app_level)] += 2
        # 用难度系数估算入学时间
        curr_year = datetime.datetime.today().year
        if mapped_app_level == "海本":
            if 2 < difficulty <= 3:
                potential_customers["score"][(potential_customers.app_level == mapped_app_level) & (
                    potential_customers.enter_time < curr_year + 2) & (potential_customers.enter_time > curr_year)] += 1
            elif difficulty < 3:
                potential_customers["score"][(potential_customers.app_level == mapped_app_level) & (
                    potential_customers.enter_time >= curr_year + 2)] += 1
        elif mapped_app_level == "海研":
            if difficulty >= 3:
                potential_customers["score"][potential_customers.app_level == mapped_app_level] += 1
        potential_customers = potential_customers.sort_values(by="score", ascending=False)
        return potential_customers.name


class StudentAnalysisView(APIView):
    # 学生信息推荐产品
    def post(self, request):
        warnings.filterwarnings("ignore")
        data = request.data
        app_time = data['graduation_date']
        app_level = data['application_level']
        app_major = data['major']
        school_structure = data['curriculum_system']  # 课程体系
        res = self.students_for_course(app_time, app_level, app_major, school_structure)
        res_dist = {}
        if res:
            res_dist["status"] = 200
            res_dist["message"] = "获取成功"
            res_dist["data"] = res
            jsonArr = json.dumps(res_dist, ensure_ascii=False)
            return JsonResponse(jsonArr, safe=False)
        else:
            res_dist["status"] = 202
            res_dist["message"] = "未找到符合产品，请核对信息"
            res_dist["data"] = res
            jsonArr = json.dumps(res_dist, ensure_ascii=False)
            return JsonResponse(jsonArr, safe=False)

    def students_for_course(self, app_time, app_level, app_major, school_structure):
        '''
        :param app_time: 入学时间
        :param app_level: 申请层级: 应为国内国际学校，海本，海研之一
        :param app_major: 专业方向
        :param school_structure: 课程体系
        :param count: 返回前多少个推荐课程
        :return: 课程推荐
        '''
        data = Student.objects.all()
        cus = read_frame(qs=data, index_col="id")
        # %% 产品部分：产品编号
        data = Academy.objects.all()
        sales = read_frame(qs=data, index_col="id")
        # %% 产品部分：产品编号
        id = sales['product_name']
        id = set(id)
        id = dict(zip(id, range(sales.index[0], sales.index[-1])))
        sales['id'] = sales['product_name'].apply(lambda x: id[x])
        # %% 客户购买状态
        cus['df'] = cus['customer_state'].apply(lambda x: 1 if x == '已签约已购买' else 0)

        # %%
        customers = cus.loc[:,
                    ['name', 'wechat_num', 'school_type', 'curriculum_system', 'graduation_date', 'application_level',
                     'major', 'df']]
        customers.columns = ['name', 'wechat', 'school_type', 'structure', 'enter_time', 'app_level', 'major',
                             'purchased_before']
        # %%
        customers['major1'] = customers['major'].apply(
            lambda x: str(x).split('+')[0] if str(x).split('+')[0] else np.nan)
        customers['major2'] = customers['major'].apply(
            lambda x: str(x).split('+')[1] if len(str(x).split('+')) > 1 else np.nan)
        customers['major3'] = customers['major'].apply(
            lambda x: str(x).split('+')[2] if len(str(x).split('+')) > 2 else np.nan)
        customers['major4'] = customers['major'].apply(
            lambda x: str(x).split('+')[3] if len(str(x).split('+')) > 3 else np.nan)
        del customers['major']
        self.customers = customers

        self.qiepian = pd.read_excel(r"/home/Zeyou/ZeyouSite/apps/recommended/qiepianchanpin.xlsx", sheet_name="Sheet1")
        # self.qiepian = pd.read_excel(r"C:\Users\hhpba\Desktop\Zeyou\ZeyouSite\apps\recommended\qiepianchanpin.xlsx", sheet_name="Sheet1")
        self.qiepian["申请层级"] = self.qiepian["申请层级"].fillna("")
        self.qiepian["专业方向"] = self.qiepian["专业方向"].fillna("")
        self.app_level_mapping = {
            "国内国际学校": "国内国际学校",
            "美国高中": "国内国际学校",
            "美高": "国内国际学校",
            "海本转学": "海本",
            "本科转学": "海本",
            "海研": "海研",
            "海博": "海博",
            "海本": "海本",
        }
        self.school_structure_mapping = {
            "IB": "IB",
            "AP": "AP",
            "IG": "AP&IB",
            "MYP": "AP&IB",
            "A-Level": "AP&IB",
            "陆本": "本科",
            "海本": "本科",
            "本科": "本科",
        }
        if app_level in self.app_level_mapping:
            mapped_app_level = self.app_level_mapping[app_level]
        else:
            mapped_app_level = ""

        result = self.qiepian[
            (self.qiepian["申请层级"].str.contains(app_level)) | (self.qiepian["申请层级"].str.contains(mapped_app_level))]
        if app_level == "海研":
            school_structure = "本科"
        mapped_school_struct = self.school_structure_mapping[school_structure]
        if mapped_school_struct != "AP&IB":
            result = result[result["产品课程体系"].str.contains(mapped_school_struct)]
        else:
            result = result[(result["产品课程体系"].str.contains("AP")) & (result["产品课程体系"].str.contains("IB"))]
        if app_major and app_major != np.nan:
            result = result[result["专业方向"].str.contains(app_major)]

        app_year = re.search("\d{4}", app_time)
        if app_year:
            app_year = int(app_year.group(0))
            current_year = datetime.datetime.today().year
            diff = abs(app_year - current_year)
            if app_level == "海研" and diff >= 2:
                result = result[result["产品难度分级"] >= 3]
                result.sort_values(by="产品难度分级", ascending=True)
            elif app_level == "海本":
                if diff >= 2:
                    result = result[result["产品难度分级"] < 3]
                else:
                    result = result[(result["产品难度分级"] <= 3) & (result["产品难度分级"] > 1)]
                result.sort_values(by="产品难度分级", ascending=True)

        names = list(result["切片产品名称"])

        names.append("一对一独立研究")
        return names
