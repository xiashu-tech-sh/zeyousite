<template>
  <div class="main">
    <div class="datatext" >
      <span class="line"></span>
      <span class="text">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;筛选条件&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
      <span class="line"></span>
    </div>
    <el-form style="width:100%" :inline="true" :rules="rules" :model="screeninginfor" ref="screeninginfor" class="screeninginfor">
      <el-form-item label="购买开始时间" id="stop_buy_div">
        <el-date-picker v-model="start_buy_time" type="date" value-format="yyyy-MM-dd" placeholder="购买开始时间">
        </el-date-picker>
      </el-form-item>
      <el-form-item label="购买结束时间" id="stop_buy_div">
        <el-date-picker v-model="stop_buy_time" type="date" value-format="yyyy-MM-dd" placeholder="购买结束时间">
        </el-date-picker>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" id="resourceanalysis" @click="productstobuy()">查询</el-button>
      </el-form-item>
    </el-form>
    <div class="datatext">
      <span class="line"></span>
      <span class="text">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;统计结果&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
      <span class="line"></span>
    </div>
    <template v-if="productsList.length > 0">
      <el-button type="primary" id="resourceanaly" @click="productsdownload()">导出生成xlsx</el-button>
      <div id="printTest1" v-for="products in productsList" :key="products.id" style="overflow:scroll;">
        <table>
          <tbody>
            <tr style="height:40px">
              <td >产品名称</td>
              <td colspan="2" id="styletd">{{products.name}}</td>
            </tr>
            <tr style="height:40px" >
              <td>客户状态分布</td>
              <td v-for="(value, name) in products.customer_state" :key="value">{{name}}</td>
              <td v-for="num in products.sales.length" :key="num">{{num}}</td>
            </tr>
            <tr style="height:40px" >
              <td></td>
              <td v-for="(value, name) in products.customer_state" :key="name">{{value}}</td>
            </tr>
            <tr style="height:40px" >
              <td>客户来源分布</td>
              <td v-for="(value, name) in products.source" :key="value">{{name}}</td>
            </tr>
            <tr style="height:40px" >
              <td></td>
              <td v-for="(value, name) in products.source" :key="name">{{value}}</td>
            </tr>
            <tr style="height:40px" >
              <td>当前年级分布</td>
              <td v-for="(value, name) in products.current_grade" :key="value">{{name}}</td>
            </tr>
            <tr style="height:40px" >
              <td></td>
              <td v-for="(value, name) in products.current_grade" :key="name">{{value}}</td>
            </tr>
            <tr style="height:40px" >
              <td>地区分布</td>
              <td v-for="(value, name) in products.area" :key="value">{{name}}</td>
            </tr>
            <tr style="height:40px" >
              <td></td>
              <td v-for="(value, name) in products.area" :key="name">{{value}}</td>
            </tr>
            <tr style="height:40px" >
              <td>销售人员分布</td>
              <td v-for="(value, name) in products.sales" :key="value">{{name}}</td>
            </tr>
            <tr style="height:40px" >
              <td></td>
              <td v-for="(value, name) in products.sales" :key="name">{{value}}</td>
            </tr>
            <tr style="height:40px" >
              <td>专业方向分布</td>
              <td v-for="(value, name) in products.major" :key="value">{{name}}</td>
            </tr>
            <tr style="height:40px" >
              <td></td>
              <td v-for="(value, name) in products.major" :key="name">{{value}}</td>
            </tr>
            <tr style="height:40px" >
              <td>学校类型分布</td>
              <td v-for="(value, name) in products.school_type" :key="value">{{name}}</td>
            </tr>
            <tr style="height:40px" >
              <td></td>
              <td v-for="(value, name) in products.school_type" :key="name">{{value}}</td>
            </tr>
            <tr style="height:40px" >
              <td>课程体系分布</td>
              <td v-for="(value, name) in products.curriculum_system" :key="value">{{name}}</td>
            </tr>
            <tr style="height:40px" >
              <td></td>
              <td v-for="(value, name) in products.curriculum_system" :key="name">{{value}}</td>
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
      return{
      start_buy_time:"",
      stop_buy_time:"", 
      productsList:[],
      productsinfor:{
          start_buy_time:"",
          stop_buy_time:""
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
    var start_buy_time = JSON.parse(window.sessionStorage.getItem("start_buy_time"))
    var stop_buy_time = JSON.parse(window.sessionStorage.getItem("stop_buy_time"))
    if (start_buy_time){
      this.start_buy_time = start_buy_time
      this.stop_buy_time = stop_buy_time
      this.productsList= JSON.parse(window.sessionStorage.getItem("productsList"))
      }
  },

  methods:{
    async productstobuy(){
      if (this.start_buy_time == "" | this.start_buy_time == null){
      this.$message({
      type: "warning",
      message: "请选择购买开始日期"
      },)
      return
    }
    if (this.stop_buy_time== "" | this.stop_buy_time == null){
      this.$message({
      type: "warning",
      message: "请选择购买结束日期"
      },)
      return
    }
    if (this.start_buy_time>this.stop_buy_time){
      this.$message({
      type: "warning",
      message: "结束日期不能大于开始日期"
      },)
      return
    }
        this.productsinfor.start_buy_time = this.start_buy_time
        this.productsinfor.stop_buy_time = this.stop_buy_time
        const res = await this.$ajax.post(`/productstobuy/`,this.productsinfor);
        let obj = JSON.parse(res.data)
        this.productsList = obj.res
        if (obj.status == 200){
          if (obj.res.length>0){
            this.productsList = obj.res
            window.sessionStorage.setItem("start_buy_time", JSON.stringify(this.start_buy_time))
            window.sessionStorage.setItem("stop_buy_time", JSON.stringify(this.stop_buy_time))
            window.sessionStorage.setItem("productsList", JSON.stringify(this.productsList))
          }else{
            this.productsList = []
            window.sessionStorage.setItem("productsList", JSON.stringify(this.productsList))
            this.$message({
            type: 'warning',
            message: "该时间段内没有顾问人员信息"
        });
          }
        }else{
          this.productsList = []
          window.sessionStorage.setItem("productsList", JSON.stringify(this.productsList))
          this.$message({
          type: 'warning',
          message: "数据错误，请联系开发人员"
        });
        }
    },
    async productsdownload(){
      const res = await this.$ajax.get(`productstobuy/`,{responseType: 'blob'});
      var blob = new Blob([res.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=UTF-8'})
      let fileName = "产品购买情况分析.xlsx"
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
    this.rules.start_personnelsales_time[0].required = false
  },
  stopDate(){
    this.rules.stop_personnelsales_time[0].required = false
  },

  },

}
</script>

<style scoped lang="less">
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
  width: 85%;
  margin: auto;
  margin-bottom: 50px;
  border: 2px solid black;
  // padding-bottom: 30px!important;
}
#printTest1 table {
  border-collapse: collapse;
  width: 1000px;
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
  border: 1px solid black;
  text-align: center !important;
}
#printTest1 table tbody td span {
  margin-right: 20px;
}
#resourceanalysis{
  margin-top: 0px;
  width: 200px;
}
#resourceanaly{
  margin-top: 0px;
  width: 181px;
  margin-left: 930px;
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

#stop_buy_div{
  margin-left: 45px;
}
</style>