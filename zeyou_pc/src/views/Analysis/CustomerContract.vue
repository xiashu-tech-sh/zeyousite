<template>
  <div class="main">
    <div class="datatext">
      <span class="line"></span>
      <span class="text">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;筛选条件&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
      <span class="line"></span>
    </div>
    <el-form style="width:100%" :inline="true" :rules="rules" :model="screeninginfor" ref="screeninginfor" class="screeninginfor">
      <el-form-item label="签约开始时间" id="stop_signing_div" prop="start_signing_time">
        <el-date-picker v-model="start_signing_time" type="date" @change="startDate()" value-format="yyyy-MM-dd" placeholder="签约开始时间" >
        </el-date-picker>
      </el-form-item>
      <el-form-item label="签约结束时间" id="stop_signing_div" prop="stop_signing_time">
        <el-date-picker v-model="stop_signing_time" type="date" @change="stopDate()" value-format="yyyy-MM-dd" placeholder="签约结束时间"  >
        </el-date-picker>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" id="resourceanalysis" @click="customercontract()">查询</el-button>
      </el-form-item>
    </el-form>
    <div class="datatext">
      <span class="line"></span>
      <span class="text">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;统计结果&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
      <span class="line"></span>
    </div>
    <template v-if="consultantList.length > 0">
      <el-button type="primary" id="resourceanaly" @click="consultandownload()">导出生成xlsx</el-button>
      <div id="printTest1" v-for="consultan in consultantList" :key="consultan.id">
        <table width="100%" style="margin: auto!important;">
          <tbody>
            <tr style="height:40px">
              <td >顾问名字</td>
              <td id="styletd">{{consultan.name}}</td>
              <!-- <td v-for="num in 3" :key="num" :value="0">{{num != 2 ? num : ''}}</td> -->
            </tr>
            <tr style="height:40px" >
              <td>资源类型分布</td>
              <td v-for="(value, name) in consultan.source" :key="value">{{name}}</td>
            </tr>
            <tr style="height:40px" >
              <td></td>
              <td v-for="(value, name) in consultan.source" :key="name">{{value}}</td>
            </tr>
            <tr style="height:40px" >
              <td >签约时间</td>
              <td >平均签约时间</td>
            </tr>
            <tr style="height:40px" >
              <td></td>
              <td >{{consultan.average_signing}}</td>
            </tr>
            <tr style="height:40px" >
              <td>学校类型分布</td>
              <td v-for="(value, name) in consultan.school_type" :key="value">{{name}}</td>
            </tr>
            <tr style="height:40px" >
              <td></td>
              <td v-for="(value, name) in consultan.school_type" :key="name">{{value}}</td>
            </tr>
            <tr style="height:40px" >
              <td>学校名分布</td>
              <td v-for="(value, name) in consultan.school" :key="value">{{name}}</td>
            </tr>
            <tr style="height:40px" >
              <td></td>
              <td v-for="(value, name) in consultan.school" :key="name">{{value}}</td>
            </tr>
            <tr style="height:40px" >
              <td>当前年级分布</td>
              <td v-for="(value, name) in consultan.current_grade" :key="value">{{name}}</td>
            </tr>
            <tr style="height:40px" >
              <td></td>
              <td v-for="(value, name) in consultan.current_grade" :key="name">{{value}}</td>
            </tr>
            <tr style="height:40px" >
              <td>课程体系分布</td>
              <td v-for="(value, name) in consultan.curriculum_system" :key="value">{{name}}</td>
            </tr>
            <tr style="height:40px" >
              <td></td>
              <td v-for="(value, name) in consultan.curriculum_system" :key="name">{{value}}</td>
            </tr>
            <tr style="height:40px" >
              <td >签约率</td>
              <td >签约率</td>
            </tr>
            <tr style="height:40px" >
              <td></td>
              <td >{{consultan.contract_rate}}</td>
            </tr>
            <tr style="height:40px" >
              <td >流失率</td>
              <td >流失率</td>
            </tr>
            <tr style="height:40px" >
              <td></td>
              <td >{{consultan.turnover_rate}}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>

  </div>
</template>
<script>
export default {
  data() {
    return {
      consultantList: {
        id: '',
        name: '',
        school: ""
      },
      rules:{
      start_signing_time: [{
          required: true,
          message: "签约开始时间不能为空",
          trigger: "blur"
        }],
      stop_signing_time: [{
        required: true,
        message: "签约结束时间不能为空",
        trigger: "blur"
      }]
      },
      screeninginfor: {},
      start_signing_time: '',
      stop_signing_time: '',
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
    var stop_signing_time = JSON.parse(window.sessionStorage.getItem("stop_signing_time"))
    var start_signing_time = JSON.parse(window.sessionStorage.getItem("start_signing_time"))
    if (start_signing_time){
      this.start_signing_time = start_signing_time
      this.stop_signing_time = stop_signing_time
      this.consultantList= JSON.parse(window.sessionStorage.getItem("consultantList"))
      }
    },
  methods: {
    async consultandownload(){
      const res = await this.$ajax.get(`customercontract/`,{responseType: 'blob'});
      var blob = new Blob([res.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=UTF-8'})
      let fileName = "客户签约状态分析.xlsx"
      if (window.navigator.msSaveOrOpenBlob) {
        navigator.msSaveBlob(blob, fileName)
      } else {
        var link = document.createElement('a')
        link.href = window.URL.createObjectURL(blob)
        link.download = fileName
        link.click()
        //释放内存
        window.URL.createObjectURL(link.href)
        }

    },
    startDate(){
      this.rules.start_signing_time[0].required = false
    },
    stopDate(){
      this.rules.stop_signing_time[0].required = false
    },
    async customercontract() {
      if (this.start_signing_time == "" | this.start_signing_time == null){
        this.$message({
        type: "warning",
        message: "请选择签约开始日期"
        },)
        return
      }
      if (this.stop_signing_time== "" | this.stop_signing_time == null){
        this.$message({
        type: "warning",
        message: "请选择签约结束日期"
        },)
        return
      }
      if (this.start_signing_time>this.stop_signing_time){
        this.$message({
        type: "warning",
        message: "结束日期不能大于开始日期"
        },)
        return
      }
        this.screeninginfor.start_signing_time = this.start_signing_time
        this.screeninginfor.stop_signing_time = this.stop_signing_time
        const res = await this.$ajax.post(`/customercontract/`, this.screeninginfor);
        let obj = JSON.parse(res.data)
        if (obj.status == 200){
          if (obj.res.length>0){
            this.consultantList = obj.res
            window.sessionStorage.setItem("start_signing_time", JSON.stringify(this.screeninginfor.start_signing_time))
            window.sessionStorage.setItem("stop_signing_time", JSON.stringify(this.screeninginfor.stop_signing_time))
            window.sessionStorage.setItem("consultantList", JSON.stringify(this.consultantList))
          }else{
            this.consultantList = []
            window.sessionStorage.setItem("consultantList", JSON.stringify(this.consultantList))
            this.$message({
            type: 'warning',
            message: "该时间段内没有顾问人员信息"
        });
          }
        }else{
          this.consultantList = []
          window.sessionStorage.setItem("consultantList", JSON.stringify(this.consultantList))
          this.$message({
          type: 'warning',
          message: "数据错误，请联系开发人员"
        });
        }
    // }},)
    }
  }
}


</script>
<style scoped lang="less" >
#styletd{
  font-weight :bold;
}
//表格样式
#printTest1 .right .top .leader {
  float: left;
  margin-left: 30px !important;
}
#printTest1 .right .top {
  margin-top: 100px !important;
}
#printTest1 .right .top .official_seal {
  margin-right: 30px !important;
}
#printTest1 .bottom {
  margin-top: 10px !important;
}
#printTest1 .bottom .year,
#printTest1 .bottom .month {
  margin-right: 40px !important;
}
#printTest1 #title {
  padding-top: 50px !important;
  padding-bottom: 30px !important;
}
#printTest1 {
  width: 70%;
  margin: auto;
  margin-bottom: 50px;
  border: 2px solid black;
  // padding-bottom: 30px!important;
}
#printTest1 table {
  border-collapse: collapse;
}
#printTest1 table thead th {
  font-size: 20px;
  padding: 10px;
}
#printTest1 table tbody tr {
  height: 30px;
  font-size: 14px;
}
#printTest1 table tbody td {
  width: 25%;
  border: 1px solid black;
  text-align: center !important;
}
#printTest1 table tbody td span {
  margin-right: 20px;
}
//截至
.contents /deep/ .el-dialog__title {
  font-size: 15px !important;
}
.contents /deep/ .el-form {
  /*width: 410px!important;*/
  margin: auto !important;
}
.contents /deep/ .el-dialog__body {
  padding: 20px 10px !important;
}
.contents .ml {
  margin-bottom: 15px !important;
  border-left: 3px solid #447fc1;
  padding-left: 10px !important;
  font-size: 18px !important;
  font-weight: 500;
  font-size: 15px !important;
  margin-left: 15px !important;
}
.style /deep/ .el-input__inner {
  margin-bottom: 15px !important;
}
.contentdiv:hover {
  background-color: #094572;
  color: #fff;
}
.contentdiv_one:hover {
  background-color: #094572;
  color: #fff;
}

.contentdiv_one {
  width: 130px;
  display: inline-block;
  border: 1px solid #dcdfe6;
  background: #fff;
  color: #094572;
  padding: 10px 20px;
  border-radius: 15px;
  text-align: center;
  cursor: pointer;
  margin-left: 55px;
  margin-top: 30px;
}
.contentdiv {
  width: 130px;
  display: inline-block;
  border: 1px solid #dcdfe6;
  background: #fff;
  color: #094572;
  padding: 10px 20px;
  border-radius: 15px;
  margin-left: 60px;
  text-align: center;
  cursor: pointer;
  margin-top: 30px;
}
.el-button {
  margin-left: 70px;
  border-radius: 20px;
}
#imageshow {
  width: 600px;
  height: 250px;
  margin-left: 300px;
}
.el-button.is-round {
  margin-left: 70px;
}
.el-button {
  background: #fff;
  color: #094572;
}
.screeninginfor {
  margin-top: 30px;
}
.line {
  display: inline-block;
  width: 530px;
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
.el-button:focus,
.el-button:hover {
  background: #094572;
  border-color: #271849;
  color: #fff;
}
.el-button--primary {
  margin-left: 100px;
  width: 220px;
  height: 40px;
  font-size: 18px;
  background-color: #094572;
  border: none;
  border-radius: 10px;
  color: #ffffff;
  // margin-bottom: 50px;
  margin-top: 30px;
}
.el-table--border {
  margin-left: 4%;
}
.quantity {
  color: rgb(194, 187, 187);
}

#stop_signing_div {
  margin-left: 45px;
}
.screeninginfor {
  margin-top: 30px;
}
#resourceanalysis {
  margin-top: 0px;
  width: 200px;
}
#resourceanaly{
  margin-top: 0px;
  width: 181px;
  margin-left: 840px;
}
.area_class {
  top: 30px;
  left: 45px;
  font-size: 18px;
}
.billstyle {
  text-align: center;
  display: block;
  width: 200px;
  height: 30px;
  background-color: #094572;
  color: #fff;
  margin-left: 155px;
  border-radius: 10px;
}
.tableClass {
  margin-left: 155px;
  width: 900px;
  // height: 300px;
  margin-bottom: 30px;
}
.table_class {
  width: 100%;
  margin: auto !important;
}
</style>
