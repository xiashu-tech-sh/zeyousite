<template>
  <div class="main">
    <div class="datatext" >
      <span class="line"></span>
      <span class="text">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;筛选条件&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
      <span class="line"></span>
    </div>
    <el-form style="width:100%" :inline="true" :rules="rules" :model="screeninginfor" ref="screeninginfor" class="screeninginfor">
      <el-form-item label="转咨询开始时间" id="stop_consulting_div" prop="start_consulting_time">
        <el-date-picker v-model="screeninginfor.start_consulting_time" type="date" @change="startDate()" value-format="yyyy-MM-dd" placeholder="转咨询开始时间">
        </el-date-picker>
      </el-form-item>
      <el-form-item label="转咨询结束时间" id="stop_consulting_div" prop="stop_consulting_time">
        <el-date-picker v-model="screeninginfor.stop_consulting_time" type="date" @change="stopDate()" value-format="yyyy-MM-dd" placeholder="转咨询结束时间">
        </el-date-picker>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" id="resourceanalysis" @click="customerconversion()">查询</el-button>
      </el-form-item>
    </el-form>
    <div class="datatext">
      <span class="line"></span>
      <span class="text">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;统计结果&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
      <span class="line"></span>
    </div>
    <div class="billstyle">
      <span class="area_class">地区占比</span>
    </div>
    <div class="download" v-show="areaData.listkey.length>0" @click="downloadexls(areaData,'地区占比分布')">
      <span >导出exls</span>
    </div>
    <el-table :data="areaData.result"     
      max-height="300"
      border
      class="tableClass">
      <el-table-column v-for="key in areaData.listkey" :key="key" :prop="key"
          :label="key"></el-table-column>
    </el-table>
    <div class="billstyle">
      <span class="area_class">学校类型占比</span>
    </div>
    <div class="download" v-show="schooltypeData.listkey.length>0" @click="downloadexls(schooltypeData,'学校类型占比分布')">
      <span >导出exls</span>
    </div>
    <el-table :data="schooltypeData.result"     
      max-height="300"
      border
      class="tableClass">
      <el-table-column v-for="key in schooltypeData.listkey" :key="key" :prop="key"
          :label="key"></el-table-column>
    </el-table>
    <div class="billstyle">
      <span class="area_class">学校名占比</span>
    </div>
    <div class="download" v-show="schoolnameData.listkey.length>0" @click="downloadexls(schoolnameData,'学校名占比分布')">
      <span >导出exls</span>
    </div>
    <el-table :data="schoolnameData.result"     
      max-height="300"
      border
      class="tableClass">
      <el-table-column v-for="key in schoolnameData.listkey" :key="key" :prop="key"
          :label="key"></el-table-column>
    </el-table>
    <div class="billstyle">
      <span class="area_class">年级占比</span>
    </div>
    <div class="download" v-show="gradeData.listkey.length>0" @click="downloadexls(gradeData,'年级占比分布')">
      <span >导出exls</span>
    </div>
    <el-table :data="gradeData.result"     
      max-height="300"
      border
      class="tableClass">
      <el-table-column v-for="key in gradeData.listkey" :key="key" :prop="key"
          :label="key"></el-table-column>
    </el-table>
    <div class="billstyle">
      <span class="area_class">课程体系占比</span>
    </div>
    <div class="download" v-show="curriculumData.listkey.length>0" @click="downloadexls(curriculumData,'课程体系占比分布')">
      <span >导出exls</span>
    </div>
    <el-table :data="curriculumData.result"     
      max-height="300"
      border
      class="tableClass">
      <el-table-column v-for="key in curriculumData.listkey" :key="key" :prop="key"
          :label="key"></el-table-column>
    </el-table>
    <div class="billstyle">
      <span class="area_class">所属顾问占比</span>
    </div>
    <div class="download" v-show="consultantData.listkey.length>0" @click="downloadexls(consultantData,'所属顾问占比分布')">
      <span >导出exls</span>
    </div>
    <el-table :data="consultantData.result"     
      max-height="300"
      border
      class="tableClass">
      <el-table-column v-for="key in consultantData.listkey" :key="key" :prop="key"
          :label="key"></el-table-column>
    </el-table>
    <div class="billstyle">
      <span class="area_class">转咨询平均时长</span>
    </div>
    <div class="download" v-show="transfertimeData.listkey.length>0" @click="downloadexls(transfertimeData,'转咨询平均时长')">
      <span >导出exls</span>
    </div>
    <el-table :data="transfertimeData.result"     
      max-height="300"
      border
      class="tableClass">
      <el-table-column v-for="key in transfertimeData.listkey" :key="key" :prop="key"
          :label="key"></el-table-column>
    </el-table>
    <div class="billstyle">
      <span class="area_class">转换率</span>
    </div>
    <div class="download" v-show="conversionrateData.listkey.length>0" @click="downloadexls(conversionrateData,'转换率')">
      <span >导出exls</span>
    </div>
    <el-table :data="conversionrateData.result"     
      max-height="300"
      border
      class="tableClass">
      <el-table-column v-for="key in conversionrateData.listkey" :key="key" :prop="key"
          :label="key"></el-table-column>
    </el-table>
    <div class="billstyle" > 
      <span class="area_class" >签约率</span>
    </div>
    <div class="download" v-show="csigningData.listkey.length>0" @click="downloadexls(csigningData,'签约率')">
      <span >导出exls</span>
    </div>
    <el-table :data="csigningData.result"     
      max-height="300"
      border
      class="tableClass">
      <el-table-column v-for="key in csigningData.listkey" :key="key" :prop="key"
          :label="key"></el-table-column>
    </el-table>

  </div>
</template>
<script>
export default {
  data() {
      return{
        csigningData:{
        result: [],
        listkey:[],
      },
        conversionrateData:{
        result: [],
        listkey:[],
      },
        transfertimeData:{
        result: [],
        listkey:[],
      },
        consultantData: {
        result: [],
        listkey:[],
      },
      curriculumData: {
        result: [],
        listkey:[],
      },
      gradeData: {
        result: [],
        listkey:[],
      },
      areaData: {
        result: [],
        listkey:[],
      },
      schooltypeData: {
        result: [],
        listkey:[],
      },
      schoolnameData: {
        result: [],
        listkey:[],
      },
      rules: {
      start_consulting_time:[{
        required: true,
        message: "转咨询开始时间不能为空",
        trigger: "blur"
      }],
      stop_consulting_time: [{
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
      screeninginfor:{
          stop_consulting_time:"", //转咨询开始时间
          start_consulting_time:"" //转咨询结束时间
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
    var stop_consulting_time = JSON.parse(window.sessionStorage.getItem("stop_consulting_time"))
    var start_consulting_time = JSON.parse(window.sessionStorage.getItem("start_consulting_time"))
    if (start_consulting_time){
      this.screeninginfor.start_consulting_time = start_consulting_time
      this.screeninginfor.stop_consulting_time = stop_consulting_time
      this.areaData= JSON.parse(window.sessionStorage.getItem("areaData"))
      this.schooltypeData= JSON.parse(window.sessionStorage.getItem("schooltypeData"))
      this.schoolnameData= JSON.parse(window.sessionStorage.getItem("schoolnameData"))
      this.gradeData= JSON.parse(window.sessionStorage.getItem("gradeData"))
      this.curriculumData= JSON.parse(window.sessionStorage.getItem("curriculumData"))
      this.consultantData= JSON.parse(window.sessionStorage.getItem("consultantData"))
      this.conversionrateData = JSON.parse(window.sessionStorage.getItem("conversionrateData"))
      this.transfertimeData= JSON.parse(window.sessionStorage.getItem("transfertimeData"))
      this.csigningData= JSON.parse(window.sessionStorage.getItem("csigningData"))
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
      this.rules.start_consulting_time[0].required = false
    },
    stopDate(){
      this.rules.stop_consulting_time[0].required = false
    },
    async customerconversion(){
      if (this.screeninginfor.start_consulting_time == "" | this.screeninginfor.start_consulting_time == null){
        this.$message({
        type: "warning",
        message: "请选择转咨询开始日期"
        },)
        return
      }
      if (this.screeninginfor.stop_consulting_time== "" | this.screeninginfor.stop_consulting_time == null){
        this.$message({
        type: "warning",
        message: "请选择转咨询结束日期"
        },)
        return
      }
      if (this.start_consulting_time>this.stop_consulting_time){
        this.$message({
        type: "warning",
        message: "结束日期不能大于开始日期"
        },)
        return
      }
        this.csigningData={result:[],listkey:[],}
        this.conversionrateData={result: [],listkey:[],}
        this.transfertimeData={result: [],listkey:[],}
        this.consultantData={result: [],listkey:[],}
        this.curriculumData={result: [],listkey:[],}
        this.gradeData={result: [],listkey:[],}
        this.areaData={result: [],listkey:[],}
        this.schooltypeData={result: [],listkey:[],}
        this.schoolnameData={result: [],listkey:[],}
        const res = await this.$ajax.post(`/customerconversion/`,this.screeninginfor);
        let obj = JSON.parse(res.data)
        //提取地区表头字段
        this.areaData.result = obj.area_data
        for (let i = 0, l = this.areaData.result.length; i < l; i++) {
          for (let key in this.areaData.result[i]) {
            if (this.areaData.listkey.indexOf(key)==-1){
                this.areaData.listkey.push(key)
            }
          }
        }

        window.sessionStorage.setItem("areaData", JSON.stringify(this.areaData))
        //提取学校类型表头字段
        this.schooltypeData.result = obj.set_school_type
        for (let i = 0, l = this.schooltypeData.result.length; i < l; i++) {
          for (let key in this.schooltypeData.result[i]) {
            if (this.schooltypeData.listkey.indexOf(key)==-1){
                this.schooltypeData.listkey.push(key)
            }
          }
        }
        window.sessionStorage.setItem("schooltypeData", JSON.stringify(this.schooltypeData))
        //提取学校名表头字段
        this.schoolnameData.result = obj.school
        for (let i = 0, l = this.schoolnameData.result.length; i < l; i++) {
          for (let key in this.schoolnameData.result[i]) {
            if (this.schoolnameData.listkey.indexOf(key)==-1){
                this.schoolnameData.listkey.push(key)
            }
          }
        }
        window.sessionStorage.setItem("schoolnameData", JSON.stringify(this.schoolnameData))
        //提取年级表头字段
        this.gradeData.result = obj.grade
        for (let i = 0, l = this.gradeData.result.length; i < l; i++) {
          for (let key in this.gradeData.result[i]) {
            if (this.gradeData.listkey.indexOf(key)==-1){
                this.gradeData.listkey.push(key)
            }
          }
        }
        window.sessionStorage.setItem("gradeData", JSON.stringify(this.gradeData))
        //提取课程体系表头字段
        this.curriculumData.result = obj.curriculum_system
        for (let i = 0, l = this.curriculumData.result.length; i < l; i++) {
          for (let key in this.curriculumData.result[i]) {
            if (this.curriculumData.listkey.indexOf(key)==-1){
                this.curriculumData.listkey.push(key)
            }
          }
        }
        window.sessionStorage.setItem("curriculumData", JSON.stringify(this.curriculumData))
        //提取课程体系表头字段
        this.consultantData.result = obj.consultant
        for (let i = 0, l = this.consultantData.result.length; i < l; i++) {
          for (let key in this.consultantData.result[i]) {
            if (this.consultantData.listkey.indexOf(key)==-1){
                this.consultantData.listkey.push(key)
            }
          }
        }
        window.sessionStorage.setItem("consultantData", JSON.stringify(this.consultantData))
        //提取转咨询平均表头字段
        this.transfertimeData.result = obj.transfer_time
        for (let i = 0, l = this.transfertimeData.result.length; i < l; i++) {
          for (let key in this.transfertimeData.result[i]) {
            if (this.transfertimeData.listkey.indexOf(key)==-1){
                this.transfertimeData.listkey.push(key)
            }
          }
        }
        window.sessionStorage.setItem("transfertimeData", JSON.stringify(this.transfertimeData))
        //提取转换率表头字段
        this.conversionrateData.result = obj.conversion_rate
        for (let i = 0, l = this.conversionrateData.result.length; i < l; i++) {
          for (let key in this.conversionrateData.result[i]) {
            if (this.conversionrateData.listkey.indexOf(key)==-1){
                this.conversionrateData.listkey.push(key)
            }
          }
        }
        window.sessionStorage.setItem("conversionrateData", JSON.stringify(this.conversionrateData))
        //提取签约率表头字段
        this.csigningData.result = obj.signing
        for (let i = 0, l = this.csigningData.result.length; i < l; i++) {
          for (let key in this.csigningData.result[i]) {
            if (this.csigningData.listkey.indexOf(key)==-1){
                this.csigningData.listkey.push(key)
            }
          }
        }
        window.sessionStorage.setItem("csigningData", JSON.stringify(this.csigningData))
      // 保存数据‘
      window.sessionStorage.setItem("start_consulting_time", JSON.stringify(this.screeninginfor.start_consulting_time))
      window.sessionStorage.setItem("stop_consulting_time", JSON.stringify(this.screeninginfor.stop_consulting_time))

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
.screeninginfor{
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
#stop_consulting_div{
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