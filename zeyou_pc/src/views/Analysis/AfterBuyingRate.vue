<template>
  <div class="main">
    <div class="datatext">
      <span class="line"></span>
      <span class="text">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;筛选条件&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
      <span class="line"></span>
    </div>
        <el-form style="width:100%" :inline="true" :rules="rules" :model="afterinfor" ref="afterinfor" class="screeninginfor">
      <el-form-item label="购买开始时间" id="stop_buy_div">
        <el-date-picker v-model="afterinfor.start_after_time" type="date" value-format="yyyy-MM-dd" placeholder="购买开始时间">
        </el-date-picker>
      </el-form-item>
      <el-form-item label="购买结束时间" id="stop_buy_div">
        <el-date-picker v-model="afterinfor.stop_after_time" type="date" value-format="yyyy-MM-dd" placeholder="购买结束时间">
        </el-date-picker>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" id="resourceanalysis" @click="afterbuy()">查询</el-button>
      </el-form-item>
    </el-form>

    <div class="datatext">
      <span class="line"></span>
      <span class="text">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;统计结果&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
      <span class="line"></span>
    </div>
    <template v-if="afterbuyList.length > 0">
      <el-button type="primary" id="resourceanalysis" @click="downloadFile()">导出生成exls</el-button>
      <div id="printTest1" style="overflow:scroll;">
        <table>
          <tbody >
            <tr>
            <td colspan="4" id="styletd">复购率统计</td>
            </tr>
            <tr style="height:40px">
              <td colspan="1" id="styletd">产品复购率</td>
              <td></td>
              <td></td>
              <td></td>
            </tr>
            <tr>
              <td></td>
              <td>复购触发次数</td>
              <td>时间范围内总购买数</td>
              <td>复购触发率</td>
            </tr>
            <tr style="height:40px"   v-for="products in afterbuyList" :key="products.id">
              <td >{{products.product_name}}</td>
              <td >{{products.repurchase_trigger}}</td>
              <td >{{products.total_number}}</td>
              <td >{{products.after_buy_rate}}</td>
            </tr>
            <tr>
              <td></td>
              <td></td>
              <td></td>
              <td></td>
            </tr>
            <tr>
              <td></td>
              <td></td>
              <td></td>
              <td></td>
            </tr>
            <tr>
            <td id="styletd">销售人员复购率</td>
            </tr>
            <tr>
              <td></td>
              <td>复购出现次数</td>
              <td>总销售计数</td>
              <td>复购率</td>
            </tr>
            <tr style="height:40px"   v-for="after in afterList" :key="after.id">
              <td >{{after.sales_staff}}</td>
              <td >{{after.purchase_num}}</td>
              <td >{{after.total_num}}</td>
              <td >{{after.after_buying_rate}}</td>
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
        afterbuyList:'',
        afterList:'',
      afterinfor:{
          start_after_time:"",
          stop_after_time:"",
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
    var start_after_time = JSON.parse(window.sessionStorage.getItem("start_after_time"))
    var stop_after_time = JSON.parse(window.sessionStorage.getItem("stop_after_time"))
    if (start_after_time){
      this.afterinfor.start_after_time = start_after_time
      this.afterinfor.stop_after_time = stop_after_time
      }
    var afterList = JSON.parse(window.sessionStorage.getItem("afterList"))
    if(afterList){
    this.afterList = afterList
    }
    var afterbuyList = JSON.parse(window.sessionStorage.getItem("afterbuyList"))
    if(afterbuyList){
    this.afterbuyList = afterbuyList
    }
  },

  methods:{
        async downloadFile(){
        const res = await this.$ajax.get(`/afterbuy/`,{responseType: 'blob'});
        var blob = new Blob([res.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=UTF-8'})
        let fileName = "复购率分析.xlsx"
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
    async afterbuy(){
    if (this.afterinfor.start_after_time == "" | this.afterinfor.start_after_time == null){
      this.$message({
      type: "warning",
      message: "请选择购买开始日期"
      },)
      return
    }
    if (this.afterinfor.stop_after_time == "" | this.afterinfor.stop_after_time  == null){
      this.$message({
      type: "warning",
      message: "请选择购买结束日期"
      },)
      return
    }
    if (this.afterinfor.start_after_time>this.afterinfor.stop_after_time ){
      this.$message({
      type: "warning",
      message: "结束日期不能大于开始日期"
      },)
      return
    }
    const res = await this.$ajax.post(`/afterbuy/`,this.afterinfor);
    let obj = JSON.parse(res.data)

    if (obj.status == 200){
      this.afterbuyList = obj.purchase_res
      this.afterList = obj.sales_res
      window.sessionStorage.setItem("start_after_time", JSON.stringify(this.afterinfor.start_after_time))
      window.sessionStorage.setItem("stop_after_time", JSON.stringify(this.afterinfor.stop_after_time))
      window.sessionStorage.setItem("afterbuyList", JSON.stringify(this.afterbuyList))
      window.sessionStorage.setItem("afterList", JSON.stringify(this.afterList))
    }else{
      this.afterbuyList = []
      this.afterList = []
      window.sessionStorage.setItem("afterbuyList", JSON.stringify(this.afterbuyList))
      window.sessionStorage.setItem("afterList", JSON.stringify(this.afterList))
      this.alesList = []
      window.sessionStorage.setItem("alesList", JSON.stringify(this.alesList))
      this.$message({
      type: 'warning',
      message: "数据错误，请联系开发人员"
      });
    }
    },
  }
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
#stop_buy_div{
  margin-left: 45px;
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
  // margin-bottom: 50px;
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
</style>