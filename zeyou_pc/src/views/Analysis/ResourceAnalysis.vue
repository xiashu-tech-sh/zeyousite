<template>
  <div class="main">
    <div class="datatext" >
      <span class="line"></span>
      <span class="text">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;筛选条件&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
      <span class="line"></span>
    </div>
    <el-form style="width:100%" :inline="true" :rules="rules" :model="resourceinfor" ref="resourceinfor" class="resourceinfor">
      <el-form-item label="加好友开始时间" id="stop_resource_div" prop="stop_resource_time">
        <el-date-picker v-model="resourceinfor.start_resource_time" type="date" @change="startDate()" value-format="yyyy-MM-dd" placeholder="转咨询开始时间">
        </el-date-picker>
      </el-form-item>
      <el-form-item label="加好友结束时间" id="stop_resource_div" prop="stop_resource_time">
        <el-date-picker v-model="resourceinfor.stop_resource_time" type="date" @change="stopDate()" value-format="yyyy-MM-dd" placeholder="转咨询结束时间">
        </el-date-picker>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" id="resourceanalysis" @click="resourceanalysis()">查询</el-button>
      </el-form-item>
    </el-form>
    <div class="datatext">
      <span class="line"></span>
      <span class="text">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;统计结果&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
      <span class="line"></span>
    </div>
    <div class="billstyle">
      <span class="area_class">资源来源</span>
    </div>
    <div class="download" v-show="re_sourceData.listkey.length>0" @click="downloadexls(re_sourceData,'资源来源占比分布')">
      <span >导出exls</span>
    </div>
    <el-table :data="re_sourceData.result"     
      max-height="300"
      border
      class="tableClass">
      <el-table-column v-for="key in re_sourceData.listkey" :key="key" :prop="key"
          :label="key"></el-table-column>
    </el-table>
    <div class="billstyle">
      <span class="area_class">性别占比</span>
    </div>
    <div class="download" v-show="re_genderData.listkey.length>0" @click="downloadexls(re_genderData,'性别占比分布')">
      <span >导出exls</span>
    </div>
    <el-table :data="re_genderData.result"     
      max-height="300"
      border
      class="tableClass">
      <el-table-column v-for="key in re_genderData.listkey" :key="key" :prop="key"
          :label="key"></el-table-column>
    </el-table>
    <div class="billstyle">
      <span class="area_class">申请层级占比</span>
    </div>
    <div class="download" v-show="re_applicationlevelData.listkey.length>0" @click="downloadexls(re_applicationlevelData,'申请层级占比分布')">
      <span >导出exls</span>
    </div>
    <el-table :data="re_applicationlevelData.result"     
      max-height="300"
      border
      class="tableClass">
      <el-table-column v-for="key in re_applicationlevelData.listkey" :key="key" :prop="key"
          :label="key"></el-table-column>
    </el-table>
    <div class="billstyle">
      <span class="area_class">入学时间占比</span>
    </div>
    <div class="download" v-show="re_graduationData.listkey.length>0" @click="downloadexls(re_graduationData,'入学时间占比分布')">
      <span >导出exls</span>
    </div>
    <el-table :data="re_graduationData.result"     
      max-height="300"
      border
      class="tableClass">
      <el-table-column v-for="key in re_graduationData.listkey" :key="key" :prop="key"
          :label="key"></el-table-column>
    </el-table>
    <div class="billstyle">
      <span class="area_class">地区占比</span>
    </div>
    <div class="download" v-show="re_areaData.listkey.length>0" @click="downloadexls(re_areaData,'地区占比分布')">
      <span >导出exls</span>
    </div>
    <el-table :data="re_areaData.result"     
      max-height="300"
      border
      class="tableClass">
      <el-table-column v-for="key in re_areaData.listkey" :key="key" :prop="key"
          :label="key"></el-table-column>
    </el-table>
    <div class="billstyle">
      <span class="area_class">客户身份占比</span>
    </div>
    <div class="download" v-show="re_identityData.listkey.length>0" @click="downloadexls(re_identityData,'客户身份分布')">
      <span >导出exls</span>
    </div>
    <el-table :data="re_identityData.result"     
      max-height="300"
      border
      class="tableClass">
      <el-table-column v-for="key in re_identityData.listkey" :key="key" :prop="key"
          :label="key"></el-table-column>
    </el-table>
    <div class="billstyle">
      <span class="area_class">学校类型占比</span>
    </div>
    <div class="download" v-show="re_schooltypeData.listkey.length>0" @click="downloadexls(re_schooltypeData,'学校类型占比分布')">
      <span >导出exls</span>
    </div>
    <el-table :data="re_schooltypeData.result"     
      max-height="300"
      border
      class="tableClass">
      <el-table-column v-for="key in re_schooltypeData.listkey" :key="key" :prop="key"
          :label="key"></el-table-column>
    </el-table>
    <div class="billstyle">
      <span class="area_class">学校名占比</span>
    </div>
    <div class="download" v-show="re_schoolnameData.listkey.length>0" @click="downloadexls(re_schoolnameData,'学校名占比分布')">
      <span >导出exls</span>
    </div>
    <el-table :data="re_schoolnameData.result"     
      max-height="300"
      border
      class="tableClass">
      <el-table-column v-for="key in re_schoolnameData.listkey" :key="key" :prop="key"
          :label="key"></el-table-column>
    </el-table>
    <div class="billstyle">
      <span class="area_class">课程体系占比</span>
    </div>
    <div class="download" v-show="re_curriculumData.listkey.length>0" @click="downloadexls(re_curriculumData,'课程体系占比分布')">
      <span >导出exls</span>
    </div>
    <el-table :data="re_curriculumData.result"     
      max-height="300"
      border
      class="tableClass">
      <el-table-column v-for="key in re_curriculumData.listkey" :key="key" :prop="key"
          :label="key"></el-table-column>
    </el-table>
    <div class="billstyle">
      <span class="area_class">专业方向占比</span>
    </div>
    <div class="download" v-show="re_majorData.listkey.length>0" @click="downloadexls(re_majorData,'专业方向占比分布')">
      <span >导出exls</span>
    </div>
    <el-table :data="re_majorData.result"     
      max-height="300"
      border
      class="tableClass">
      <el-table-column v-for="key in re_majorData.listkey" :key="key" :prop="key"
          :label="key"></el-table-column>
    </el-table>
    <div class="billstyle">
      <span class="area_class">目标国家占比</span>
    </div>
    <div class="download" v-show="re_targetcountryData.listkey.length>0" @click="downloadexls(re_targetcountryData,'目标国家占比分布')">
      <span >导出exls</span>
    </div>
    <el-table :data="re_targetcountryData.result"     
      max-height="300"
      border
      class="tableClass">
      <el-table-column v-for="key in re_targetcountryData.listkey" :key="key" :prop="key"
          :label="key"></el-table-column>
    </el-table>
  </div>
</template>
<script>
export default {
  data() {
      return{
      re_identityData:{
        result: [],
        listkey:[],
      },
      re_graduationData:{
        result: [],
        listkey:[],
      },
      re_applicationlevelData:{
        result: [],
        listkey:[],
      },
      re_genderData:{
        result: [],
        listkey:[],
      },
      re_sourceData:{
        result: [],
        listkey:[],
      },
      re_targetcountryData:{
        result: [],
        listkey:[],
      },
      re_majorData: {
        result: [],
        listkey:[],
      },
      re_curriculumData: {
        result: [],
        listkey:[],
      },
      re_areaData: {
        result: [],
        listkey:[],
      },
      re_schooltypeData: {
        result: [],
        listkey:[],
      },
      re_schoolnameData: {
        result: [],
        listkey:[],
      },
      rules: {
      stop_resource_time:[{
        required: true,
        message: "转咨询开始时间不能为空",
        trigger: "blur"
      }],
      stop_resource_time: [{
        required: true,
        message: "转咨询结束时间不能为空",
        trigger: "blur"
      }],
      sales: [{
        required: true,
        message: "销售人员不能为空",
        trigger: "blur"
      }]
      },
      resourceinfor:{
          start_resource_time:"", //转咨询开始时间
          stop_resource_time:"" //转咨询结束时间
      },

    }
  },
  created() {
      let identity = window.sessionStorage.getItem('department')
      var identity_list = ["学术成长学院" ,"数据管理员", "超级用户"]
      if (identity_list.findIndex(item => item=== identity)<0){
        this.$message({
        type: "warning",
        message: "权限不足，无法查看"
        },)
      return        
      }     
    var start_resource_time = JSON.parse(window.sessionStorage.getItem("start_resource_time"))
    var stop_resource_time = JSON.parse(window.sessionStorage.getItem("stop_resource_time"))
    if (stop_resource_time){
      this.re_sourceData= JSON.parse(window.sessionStorage.getItem("re_sourceData"))
      this.re_genderData= JSON.parse(window.sessionStorage.getItem("re_genderData"))
      this.re_applicationlevelData= JSON.parse(window.sessionStorage.getItem("re_applicationlevelData"))
      this.re_graduationData= JSON.parse(window.sessionStorage.getItem("re_graduationData"))
      this.re_areaData= JSON.parse(window.sessionStorage.getItem("re_areaData"))
      this.re_identityData = JSON.parse(window.sessionStorage.getItem("re_identityData"))
      this.re_schooltypeData= JSON.parse(window.sessionStorage.getItem("re_schooltypeData"))
      this.re_schoolnameData= JSON.parse(window.sessionStorage.getItem("re_schoolnameData"))
      this.re_curriculumData= JSON.parse(window.sessionStorage.getItem("re_curriculumData"))
      this.re_majorData= JSON.parse(window.sessionStorage.getItem("re_majorData"))
      this.re_targetcountryData= JSON.parse(window.sessionStorage.getItem("re_targetcountryData"))
      this.resourceinfor.start_resource_time = start_resource_time
      this.resourceinfor.stop_resource_time = stop_resource_time
    }
   
  },

  methods:{
    async downloadexls(tableclass,tablename){
      var data = {
      tableData: tableclass.result,
      children: tableclass.listkey
      }
      this.comExportToExcel(data, tableclass.listkey,tablename);
    },
    startDate(){
      this.rules.stop_resource_time[0].required = false
    },
    stopDate(){
      this.rules.stop_resource_time[0].required = false
    },
    async resourceanalysis(){
      if (this.resourceinfor.stop_resource_time == "" | this.resourceinfor.stop_resource_time == null){
        this.$message({
        type: "warning",
        message: "请选择转咨询开始日期"
        },)
        return
      }
      if (this.resourceinfor.stop_resource_time== "" | this.resourceinfor.stop_resource_time == null){
        this.$message({
        type: "warning",
        message: "请选择转咨询结束日期"
        },)
        return
      }
      if (this.stop_resource_time>this.stop_resource_time){
        this.$message({
        type: "warning",
        message: "结束日期不能大于开始日期"
        },)
        return
      }
        this.re_sourceData={result: [],listkey:[],}
        this.re_genderData = {result: [],listkey:[],}
        this.re_applicationlevelData = {result: [],listkey:[],}
        this.re_graduationData = {result: [],listkey:[],}
        this.re_identityData = {result: [],listkey:[],}
        this.re_targetcountryData={result: [],listkey:[],}
        this.re_majorData={result: [],listkey:[],}
        this.re_curriculumData={result: [],listkey:[],}
        this.re_areaData={result: [],listkey:[],}
        this.re_schooltypeData={result: [],listkey:[],}
        this.re_schoolnameData={result: [],listkey:[],}
        const res = await this.$ajax.post(`/resourceanalysis/`,this.resourceinfor);
        let obj = JSON.parse(res.data)
        // 提取资源来源表头字段
        this.re_sourceData.result = obj.source_data
        for (let i = 0, l = this.re_sourceData.result.length; i < l; i++) {
          for (let key in this.re_sourceData.result[i]) {
            if (this.re_sourceData.listkey.indexOf(key)==-1){
                this.re_sourceData.listkey.push(key)
            }
          }
        }
        window.sessionStorage.setItem("re_sourceData", JSON.stringify(this.re_sourceData))
        // 提取性别表头字段
        this.re_genderData.result = obj.gender_data
        for (let i = 0, l = this.re_genderData.result.length; i < l; i++) {
          for (let key in this.re_genderData.result[i]) {
            if (this.re_genderData.listkey.indexOf(key)==-1){
                this.re_genderData.listkey.push(key)
            }
          }
        }
        window.sessionStorage.setItem("re_genderData", JSON.stringify(this.re_genderData))
        // 提取申请层级表头字段
        this.re_applicationlevelData.result = obj.application_level_data
        for (let i = 0, l = this.re_applicationlevelData.result.length; i < l; i++) {
          for (let key in this.re_applicationlevelData.result[i]) {
            if (this.re_applicationlevelData.listkey.indexOf(key)==-1){
                this.re_applicationlevelData.listkey.push(key)
            }
          }
        }
        window.sessionStorage.setItem("re_applicationlevelData", JSON.stringify(this.re_applicationlevelData))
        // 提取申请层级入学时间表头字段
        this.re_graduationData.result = obj.graduation_date
        for (let i = 0, l = this.re_graduationData.result.length; i < l; i++) {
          for (let key in this.re_graduationData.result[i]) {
            if (this.re_graduationData.listkey.indexOf(key)==-1){
                this.re_graduationData.listkey.push(key)
            }
          }
        }
        window.sessionStorage.setItem("re_graduationData", JSON.stringify(this.re_graduationData))
        //提取地区表头字段
        this.re_areaData.result = obj.area_data
        for (let i = 0, l = this.re_areaData.result.length; i < l; i++) {
          for (let key in this.re_areaData.result[i]) {
            if (this.re_areaData.listkey.indexOf(key)==-1){
                this.re_areaData.listkey.push(key)
            }
          }
        }
        window.sessionStorage.setItem("re_areaData", JSON.stringify(this.re_areaData))
        // 提取客户身份表头字段
        this.re_identityData.result = obj.identity
        for (let i = 0, l = this.re_identityData.result.length; i < l; i++) {
          for (let key in this.re_identityData.result[i]) {
            if (this.re_identityData.listkey.indexOf(key)==-1){
                this.re_identityData.listkey.push(key)
            }
          }
        }
        window.sessionStorage.setItem("re_identityData", JSON.stringify(this.re_identityData))
        //提取学校类型表头字段
        this.re_schooltypeData.result = obj.school_type
        for (let i = 0, l = this.re_schooltypeData.result.length; i < l; i++) {
          for (let key in this.re_schooltypeData.result[i]) {
            if (this.re_schooltypeData.listkey.indexOf(key)==-1){
                this.re_schooltypeData.listkey.push(key)
            }
          }
        }
        window.sessionStorage.setItem("re_schooltypeData", JSON.stringify(this.re_schooltypeData))
        //提取学校名表头字段
        this.re_schoolnameData.result = obj.school
        for (let i = 0, l = this.re_schoolnameData.result.length; i < l; i++) {
          for (let key in this.re_schoolnameData.result[i]) {
            if (this.re_schoolnameData.listkey.indexOf(key)==-1){
                this.re_schoolnameData.listkey.push(key)
            }
          }
        }
        window.sessionStorage.setItem("re_schoolnameData", JSON.stringify(this.re_schoolnameData))
        //提取课程体系表头字段
        this.re_curriculumData.result = obj.curriculum_system
        for (let i = 0, l = this.re_curriculumData.result.length; i < l; i++) {
          for (let key in this.re_curriculumData.result[i]) {
            if (this.re_curriculumData.listkey.indexOf(key)==-1){
                this.re_curriculumData.listkey.push(key)
            }
          }
        }
        window.sessionStorage.setItem("re_curriculumData", JSON.stringify(this.re_curriculumData))
        //提取专业方向表头字段
        this.re_majorData.result = obj.major
        for (let i = 0, l = this.re_majorData.result.length; i < l; i++) {
          for (let key in this.re_majorData.result[i]) {
            if (this.re_majorData.listkey.indexOf(key)==-1){
                this.re_majorData.listkey.push(key)
            }
          }
        }
        window.sessionStorage.setItem("re_majorData", JSON.stringify(this.re_majorData))
        //提取目标国家表头字段
        this.re_targetcountryData.result = obj.target_country
        for (let i = 0, l = this.re_targetcountryData.result.length; i < l; i++) {
          for (let key in this.re_targetcountryData.result[i]) {
            if (this.re_targetcountryData.listkey.indexOf(key)==-1){
                this.re_targetcountryData.listkey.push(key)
            }
          }
        }
        window.sessionStorage.setItem("re_targetcountryData", JSON.stringify(this.re_targetcountryData))
      // 保存数据‘
      window.sessionStorage.setItem("start_resource_time", JSON.stringify(this.resourceinfor.start_resource_time))
      window.sessionStorage.setItem("stop_resource_time", JSON.stringify(this.resourceinfor.stop_resource_time))

    }
  }
}
</script>

<style scoped lang="less">

#resourceanalysis{
  margin-top: 0px;
  width: 200px;
}
.contentdiv:hover{
  background-color: #094572;
  color: #fff;
}
.contentdiv_one:hover{
  background-color: #094572;
  color: #fff;
}

.contentdiv_one{
  width: 130px;
  display: inline-block;
  border:1px solid #DCDFE6;
  background: #fff;
  color: #094572;
  padding: 10px 20px;
  border-radius: 15px;
  text-align:center;
  cursor: pointer;
  margin-left: 55px;
  margin-top: 30px;
}
.contentdiv{
  width: 130px;
  display: inline-block;
  border:1px solid #DCDFE6;
  background: #fff;
  color: #094572;
  padding: 10px 20px;
  border-radius: 15px;
  margin-left: 60px;
  text-align:center;
  cursor: pointer;
  margin-top: 30px;

}
.el-button{
  margin-left: 70px;
  border-radius: 20px;
}
#imageshow{
  width:600px;
  height:250px;
  margin-left: 300px;
  
}
.el-button.is-round{
  margin-left: 70px;
}
.el-button{
  background:#fff;
  color:#094572
}
.resourceinfor{
  margin-top: 30px;
}
.line {
  display: inline-block;
  width:530px;
  border-top: 1px solid #cccccc;
  vertical-align: 5px;
  margin-top: 30px;
  font-weight: bold;
}
/* 筛选条件 */
.datatext {
  // margin-top: 50px;
  height: 30px;
  line-height: 36px;
  text-align: center;
  color: #094572;
  margin-left: 10px;
  margin-bottom: 50px;
}
.el-button:focus,.el-button:hover {
  background: #094572;
  border-color: #271849;
  color: #fff;
}
.el-button--primary{
    margin-left: 100px;
    width: 220px;
    height: 40px;
    font-size: 18px;
    background-color: #094572;
    border: none;
    border-radius: 10px;
    color: #FFFFFF;
    // margin-bottom: 50px;
    margin-top: 30px;
}
.el-table--border{
  margin-left: 4%;
}
.quantity{
  color: rgb(194, 187, 187)
}
#start_consulting_div{
  margin-left: 15px;
}
#stop_resource_div{
  margin-left: 45px;
}
.tableClass{
  margin-left: 155px;
  width: 900px;
  // height: 300px;
  margin-bottom: 30px;
}
.area_class{
    line-height: 30px;
    // left: 45px;
    font-size: 18px;
    display: inline-block;

}
.billstyle{
  display: inline-block;
  text-align: center;
  width: 170px;
  height: 30px;
  background-color: #094572;
  color: #fff;
  margin-left: 155px;
  border-radius: 10px;
}
.download{
  width: 130px;
  height: 30px;
  margin-left: 600px;
  font-size: 18px;
  display: inline-block;
  background-color: #094572;
  color: #fff;
  text-align: center;
  border-radius: 10px;
  font-size: 18px;
  line-height: 30px;
  cursor: pointer;
}
</style>