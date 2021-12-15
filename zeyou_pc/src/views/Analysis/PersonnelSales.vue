<template>
  <div class="main">
    <div class="datatext">
      <span class="line"></span>
      <span class="text">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;筛选条件&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
      <span class="line"></span>
    </div>
    <el-form style="width:100%" :inline="true" :rules="rules" :model="salesinfor" ref="personnelsalesinfor" class="personnelsalesinfor">
      <el-form-item label="购买开始时间" prop="start_personnelsales_time">
        <el-date-picker v-model="salesinfor.start_personnelsales_time" type="date" @change="startDate()" value-format="yyyy-MM-dd" placeholder="转咨询开始时间">
        </el-date-picker>
      </el-form-item>
      <el-form-item label="购买结束时间" prop="stop_personnelsales_time">
        <el-date-picker v-model="salesinfor.stop_personnelsales_time" type="date" @change="stopDate()" value-format="yyyy-MM-dd" placeholder="转咨询结束时间">
        </el-date-picker>
      </el-form-item>
    </el-form>
    <div class="datatext">
      <span class="line"></span>
      <span class="text">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;统计结果&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
      <span class="line"></span>
    </div>
    <div id="tempstatistics">
      <el-button type="primary" id="statistics" @click="salesstaff()">销售人员</el-button>
      <template v-if="productsList.length > 0" id="tempstatistics">
      <el-button type="primary" id="resourceanalysis" @click="salesstaffdownload()">导出生成xlsx</el-button>
        <div id="printTest1"  style="overflow:scroll;">
          <table>
            <tbody>
            <tr>
            <td colspan="25" id="styletd">销售人员统计</td>
            </tr>
            </tbody>
            <tbody v-for="products in productsList" :key="products.id">
              <tr style="height:40px" >
                <td colspan="2" id="styletd">{{products.name}}</td>
                <td colspan="2" v-for=" name in products.set_month" :key="name">{{name}}</td>
                <tr style="height:40px" v-for=" (value,names) in products.product_name" :key="names">
                  <td colspan="2" >{{names}}</td>
                  <td colspan="2" v-for=" num in value" :key="num">{{num != 0 ? num : ''}}</td>
              </tr>
              <tr>
                <td colspan="2" v-for="vm in 13" :key="vm"></td>
              </tr>
            </tbody>
          </table>
        </div>
      </template>
    </div>
    <div id="tempstatistics">
      <el-button type="primary" id="statistics" @click="consultantoffice()">在办购买</el-button>
      <template v-if="officeList.length > 0" id="tempstatistics">
      <el-button type="primary" id="resourceanalysis" @click="consultantofficedownload()">导出生成xlsx</el-button>
        <div id="printTest1"  style="overflow:scroll;">
          <table>
            <tbody>
            <tr>
            <td colspan="20" id="styletd">顾问在办购买统计</td>
            </tr>
            </tbody>
            <tbody v-for="products in officeList" :key="products.id">
              <tr style="height:40px" >
                <td colspan="2" id="styletd">{{products.name}}</td>
                <td colspan="2" v-for=" name in products.grade" :key="name">{{name}}</td>
                <tr style="height:40px" v-for=" (value,names) in products.product_name" :key="names">
                  <td colspan="2" >{{names}}</td>
                  <td colspan="2" v-for=" num in value" :key="num">{{num != 0 ? num : ''}}</td>
              </tr>
              <tr>
                <td colspan="2" v-for="vm in 10" :key="vm"></td>
              </tr>
            </tbody>
          </table>
        </div>
      </template>
    </div>
      <div id="tempstatistics">
      <el-button type="primary" id="statistics" @click="promotenum()">产品促签</el-button>
      <template v-if="promoteList.length > 0" id="tempstatistics">
      <el-button type="primary" id="resourceanalysis" @click="promotenumdownload()">导出生成xlsx</el-button>
        <div id="printTest1"  style="overflow:scroll;">
          <table>
            <tbody>
            <tr>
            <td colspan="10" id="styletd">顾问产品促签统计</td>
            </tr>
            </tbody>
            <tbody v-for="promote in promoteList" :key="promote.id">
              <tr style="height:40px" >
                <td colspan="2" id="styletd">{{promote.name}}</td>
                <td>促签人数</td>
              </tr>
              <tr style="height:40px" >
                <td colspan="2"></td>
                <td colspan="2" >{{promote.the_current}}</td>
              </tr>
              <tr style="height:40px" >
                <td colspan="2"></td>
                <td colspan="2" >选定时间内总签约人数</td>
              </tr>
              <tr style="height:40px" >
                <td colspan="2"></td>
                <td colspan="2">{{promote.all_num}}</td>
              </tr>
              <tr style="height:40px" >
                <td colspan="2"></td>
                <td colspan="2">切片产品促签率</td>
              </tr>
              <tr style="height:40px" >
                <td colspan="2"></td>
                <td colspan="2">{{promote.rate}}</td>
              </tr>

              <tr>
                <td colspan="2" v-for="vm in 2" :key="vm"></td>
              </tr>
            </tbody>
          </table>
        </div>
      </template>
    </div>
    <div id="tempstatistics">
      <el-button type="primary" id="statistics" @click="alesdistribution()">销售分布</el-button>
      <template v-if="alesList.length > 0" id="tempstatistics">
      <el-button type="primary" id="resourceanalysis" @click="alesdistributiondownload()">导出生成xlsx</el-button>
        <div id="printTest1"  style="overflow:scroll;">
          <table>
            <tbody>
            <tr>
            <td colspan="8" id="styletd">顾问切片产品销售分布</td>
            </tr>
            </tbody>
            <tbody v-for="ales in alesList" :key="ales.id">
              <tr style="height:40px" >
                <td colspan="2" id="styletd">{{ales.name}}</td>
                <td>跟进客户购买计数</td>
              </tr>
              <tr style="height:40px" >
                <td colspan="2"></td>
                <td colspan="2" >{{ales.to_follow_up}}</td>
              </tr>
              <tr style="height:40px" >
                <td colspan="2"></td>
                <td colspan="2" >在办客户购买计数</td>
              </tr>
              <tr style="height:40px" >
                <td colspan="2"></td>
                <td colspan="2">{{ales.in_the_office}}</td>
              </tr>
            
              <tr>
                <td colspan="2" v-for="vm in 2" :key="vm"></td>
              </tr>
            </tbody>
          </table>
        </div>
      </template>
    </div>
    

  </div>
</template>
<script>
export default {
  data() {
      return{
        alesList : [],
      promoteList:[],
      productsList:[],
      officeList:[],
      rules: {
        stop_personnelsales_time: [{
          required: true,
          message: "购买结束时间不能为空",
          trigger: "blur"
        }],
      start_personnelsales_time: [{
        required: true,
        message: "购买开始时间不能为空",
        trigger: "blur"
      }]
      },
      salesinfor:{
          start_personnelsales_time:"",
          stop_personnelsales_time:"",
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
    var start_personnelsales_time = JSON.parse(window.sessionStorage.getItem("start_personnelsales_time"))
    var stop_personnelsales_time = JSON.parse(window.sessionStorage.getItem("stop_personnelsales_time"))
    if (start_personnelsales_time){
      this.salesinfor.start_personnelsales_time = start_personnelsales_time
      this.salesinfor.stop_personnelsales_time = stop_personnelsales_time
      }
    var sales_productsList = JSON.parse(window.sessionStorage.getItem("sales_productsList"))
    if(sales_productsList){
    this.productsList = sales_productsList
    }
    var officeList = JSON.parse(window.sessionStorage.getItem("officeList"))
    if(officeList){
    this.officeList = officeList
    }
    var promoteList = JSON.parse(window.sessionStorage.getItem("promoteList"))
    if(promoteList){
    this.promoteList = promoteList
    }
    var alesList = JSON.parse(window.sessionStorage.getItem("alesList"))
    if(alesList){
    this.alesList = alesList
    }
  },
  

  methods:{
      // 销售分布
        async alesdistribution(){
      if (this.salesinfor.start_personnelsales_time == "" | this.salesinfor.start_personnelsales_time == null){
      this.$message({
      type: "warning",
      message: "请选择购买开始日期"
      },)
      return
    }
    if (this.salesinfor.stop_personnelsales_time == "" | this.salesinfor.stop_personnelsales_time  == null){
      this.$message({
      type: "warning",
      message: "请选择购买结束日期"
      },)
      return
    }
    if (this.salesinfor.start_personnelsales_time>this.salesinfor.stop_personnelsales_time ){
      this.$message({
      type: "warning",
      message: "结束日期不能大于开始日期"
      },)
      return
    }
        const res = await this.$ajax.post(`/alesdistribution/`,this.salesinfor);
        let obj = JSON.parse(res.data)
        if (obj.status == 200){
          if (obj.ales.length>0){
            this.alesList = obj.ales
            window.sessionStorage.setItem("start_personnelsales_time", JSON.stringify(this.salesinfor.start_personnelsales_time))
            window.sessionStorage.setItem("stop_personnelsales_time", JSON.stringify(this.salesinfor.stop_personnelsales_time))
            window.sessionStorage.setItem("alesList", JSON.stringify(this.alesList))
          }else{
            this.alesList = []
            window.sessionStorage.setItem("alesList", JSON.stringify(this.alesList))
            this.$message({
            type: 'warning',
            message: "该时间段内没有销售人员信息"
            });
            }
        }else{
          this.alesList = []
          window.sessionStorage.setItem("alesList", JSON.stringify(this.alesList))
          this.$message({
          type: 'warning',
          message: "数据错误，请联系开发人员"
          });
        }

      },
    async alesdistributiondownload(){
      const res = await this.$ajax.get(`/alesdistribution/`,{responseType: 'blob'});
      var blob = new Blob([res.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=UTF-8'})
      let fileName = "销售分布统计.xlsx"
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
    // 产品促签
      async promotenum(){
      if (this.salesinfor.start_personnelsales_time == "" | this.salesinfor.start_personnelsales_time == null){
      this.$message({
      type: "warning",
      message: "请选择购买开始日期"
      },)
      return
    }
    if (this.salesinfor.stop_personnelsales_time == "" | this.salesinfor.stop_personnelsales_time  == null){
      this.$message({
      type: "warning",
      message: "请选择购买结束日期"
      },)
      return
    }
    if (this.salesinfor.start_personnelsales_time>this.salesinfor.stop_personnelsales_time ){
      this.$message({
      type: "warning",
      message: "结束日期不能大于开始日期"
      },)
      return
    }
      const res = await this.$ajax.post(`/promotenum/`,this.salesinfor);
      let obj = JSON.parse(res.data)
      if (obj.status == 200){
        if (obj.promote.length>0){
          this.promoteList = obj.promote
          window.sessionStorage.setItem("start_personnelsales_time", JSON.stringify(this.salesinfor.start_personnelsales_time))
          window.sessionStorage.setItem("stop_personnelsales_time", JSON.stringify(this.salesinfor.stop_personnelsales_time))
          window.sessionStorage.setItem("promoteList", JSON.stringify(this.promoteList))
        }else{
          this.promoteList = []
          window.sessionStorage.setItem("promoteList", JSON.stringify(this.promoteList))
          this.$message({
          type: 'warning',
          message: "该时间段内没有销售人员信息"
          });
          }
      }else{
        this.promoteList = []
        window.sessionStorage.setItem("promoteList", JSON.stringify(this.promoteList))
        this.$message({
        type: 'warning',
        message: "数据错误，请联系开发人员"
        });
      }

    },
    async promotenumdownload(){
      const res = await this.$ajax.get(`/promotenum/`,{responseType: 'blob'});
      var blob = new Blob([res.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=UTF-8'})
      let fileName = "产品促签分布统计.xlsx"
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
    // 在办购买
    async consultantoffice(){
      if (this.salesinfor.start_personnelsales_time == "" | this.salesinfor.start_personnelsales_time == null){
      this.$message({
      type: "warning",
      message: "请选择购买开始日期"
      },)
      return
    }
    if (this.salesinfor.stop_personnelsales_time == "" | this.salesinfor.stop_personnelsales_time  == null){
      this.$message({
      type: "warning",
      message: "请选择购买结束日期"
      },)
      return
    }
    if (this.salesinfor.start_personnelsales_time>this.salesinfor.stop_personnelsales_time ){
      this.$message({
      type: "warning",
      message: "结束日期不能大于开始日期"
      },)
      return
    }
      const res = await this.$ajax.post(`/consultantoffice/`,this.salesinfor);
      let obj = JSON.parse(res.data)
      if (obj.status == 200){
        if (obj.office.length>0){
          this.officeList = obj.office
          window.sessionStorage.setItem("start_personnelsales_time", JSON.stringify(this.salesinfor.start_personnelsales_time))
          window.sessionStorage.setItem("stop_personnelsales_time", JSON.stringify(this.salesinfor.stop_personnelsales_time))
          window.sessionStorage.setItem("officeList", JSON.stringify(this.officeList))
        }else{
          this.officeList = []
          window.sessionStorage.setItem("officeList", JSON.stringify(this.officeList))
          this.$message({
          type: 'warning',
          message: "该时间段内没有销售人员信息"
          });
          }
      }else{
        this.officeList = []
        window.sessionStorage.setItem("officeList", JSON.stringify(this.officeList))
        this.$message({
        type: 'warning',
        message: "数据错误，请联系开发人员"
        });
      }

    },
    async consultantofficedownload(){
      const res = await this.$ajax.get(`/consultantoffice/`,{responseType: 'blob'});
      var blob = new Blob([res.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=UTF-8'})
      let fileName = "在办购买分布统计.xlsx"
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
    // 销售人员统计
    async salesstaff(){
      if (this.salesinfor.start_personnelsales_time == "" | this.salesinfor.start_personnelsales_time == null){
      this.$message({
      type: "warning",
      message: "请选择购买开始日期"
      },)
      return
    }
    if (this.salesinfor.stop_personnelsales_time == "" | this.salesinfor.stop_personnelsales_time  == null){
      this.$message({
      type: "warning",
      message: "请选择购买结束日期"
      },)
      return
    }
    if (this.salesinfor.start_personnelsales_time>this.salesinfor.stop_personnelsales_time ){
      this.$message({
      type: "warning",
      message: "结束日期不能大于开始日期"
      },)
      return
    }
      const res = await this.$ajax.post(`/salesstatistics/`,this.salesinfor);
      let obj = JSON.parse(res.data)
      if (obj.status == 200){
        if (obj.produvt.length>0){
          this.productsList = obj.produvt
            window.sessionStorage.setItem("start_personnelsales_time", JSON.stringify(this.salesinfor.start_personnelsales_time))
            window.sessionStorage.setItem("stop_personnelsales_time", JSON.stringify(this.salesinfor.stop_personnelsales_time))
            window.sessionStorage.setItem("sales_productsList", JSON.stringify(this.productsList))
        }else{
          this.productsList = []
          window.sessionStorage.setItem("sales_productsList", JSON.stringify(this.productsList))
          this.$message({
          type: 'warning',
          message: "该时间段内没有销售人员信息"
          });
          }
      }else{
        this.productsList = []
        window.sessionStorage.setItem("sales_productsList", JSON.stringify(this.productsList))
        this.$message({
        type: 'warning',
        message: "数据错误，请联系开发人员"
        });
      }

    },
    async salesstaffdownload(){
      const res = await this.$ajax.get(`/salesstatistics/`,{responseType: 'blob'});
      var blob = new Blob([res.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=UTF-8'})
      let fileName = "销售人员分布统计.xlsx"
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
    
    }

  }

</script>

<style scoped lang="less">
#styletd{
  font-weight :bold;
}
/deep/.el-form-item__label{
  margin-left: 130px;
}
#tempstatistics{
  min-height: 300px;
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
  min-height: 200px;
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
  width: 181px;
  margin-left: 659px;
}
#statistics{
  margin-left: 90px;
  width: 181px;
}
.personnelsalesinfor{
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
}
.el-button:focus,.el-button:hover {
  background: #094572;
  border-color: #271849;
  color: #fff;
}
.el-button--primary{
    margin-left: 100px;
    width: 200px;
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
.tableClass{
  margin-left: 90px;
  width: 1050px;
  // height: 1000px;
  margin-bottom: 30px;
}
</style>