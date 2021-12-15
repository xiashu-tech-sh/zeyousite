<template>
  <div class="datashow">
    <div class="datahead">
      <a>客户信息</a>
    </div>
    <div class="datatext">
      <span class="line"></span>
      <span class="text">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;筛选条件&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
      <span class="line"></span>
    </div>
    <div class="filter">
      <el-form :inline="true" :model="customerObj" class="customerObj">
        <el-form-item label="客户状态">
          <el-select v-model="customer_state" placeholder="请选择">
            <el-option v-for="item in customer" :key="item.value" :label="item.label" :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="资源来源">
          <el-select v-model="source" placeholder="请选择">
            <el-option v-for="item in sources" :key="item.value" :label="item.label" :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="地区">
          <el-input v-model="customerObj.area" placeholder="请输入地区"></el-input>
        </el-form-item>
        <el-form-item label="申请层级">
          <el-select v-model="application_level" placeholder="请选择">
            <el-option v-for="item in application_levels" :key="item.value" :label="item.label" :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
          <el-form-item label="申请层级入学时间">
          <el-input v-model="customerObj.graduation_date" placeholder="请输入申请层级入学时间"></el-input>
        </el-form-item>
        <el-form-item label="学校名" class="school_item">
          <el-input v-model="customerObj.school" placeholder="请输入学校名"></el-input>
        </el-form-item>
        <el-form-item label="专业方向">
          <el-input v-model="customerObj.major" placeholder="请输入专业方向"></el-input>
        </el-form-item>
        <el-form-item label="小助手" class="school_item">
          <el-select v-model="assvalue" :disabled="assistantdisabled"  placeholder="请选择">
            <el-option v-for="item in assistant" :key="item.id" :label="item.name" :value="item.name" >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item class="btns" id="elbutset">
          <el-button type="primary" @click="tofindthe()">查找</el-button>
          <el-button type="info" @click="resetLoginForm()">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div class="selectdiv">
          <el-input v-model="selectinput" placeholder="请输入姓名或微信号"></el-input>
          <button class="select_btn" type='button' @click="fuzzyselect()">查找</button>
    </div>
    <div id="select_btn">
      <label class="checkedlabel" @click="checkedAll"> 全选/反选</label>
      <label class="checkednolabel" @click="nocheckedAll"> 全不选</label>
      <label v-show="itemshow" class="droplabel" @click="deletestudent">刪除选中部分</label>     
    </div>
    <div class="pinfo">
      <div class="personnel_info" v-for="(item,make_index) in studetnList" :key="item.id">
        <div class="per_line">
          <div class="checkboxdiv">
            <input type="checkbox" :checked="fruitIds.indexOf(item.id)>=0" name="checkboxinput" class="input-checkbox" @click="checkedOne(item.id)">
          </div>
          <div class="usernamediv" @click="detailedinfor(item.id,make_index)">
            <img src="../../assets/username.png" alt="">
            <span> {{item.name}}</span>
          </div>
          <div class="imageshow">
          <div v-show="image_div" class="imageshowdiv">
            <img v-show="item.warning_show=='true'" src="../../assets/warning.png" id="imgshow">
          </div>
          </div>
          <div class="schooldiv" @click="detailedinfor(item.id,make_index)">
            <span>学校名：{{item.school}}</span>
          </div>
          <div class="graduationdiv" @click="detailedinfor(item.id,make_index)">
            <span>申请层级入学时间：{{item.graduation_date}} >>></span>
          </div>
        </div>
      </div>
    </div>
    <el-pagination background layout="prev, pager, next" :current-page="customerpage" :total="custtotal" @current-change="cutleCurentChange">
    </el-pagination>
    <div class="btnBox">
      <el-button class="selectedDownload" type="primary" @click="handleDownload(fruitIds)">导出xlsx(选中部分)</el-button>
      <el-button class="allDownload" type="primary" @click="handleDownload('all')">导出xlsx(所有学生)</el-button>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      assistantdisabled:true,
      assvalue:'',
      assistant:[],
    little_helper:false,
    all_students : [],
    judge_cust : false, // 是否条件查询
    judge_sele : false, // 是否姓名查询
    image_div: false,
      selectinput:'',
      selectpag:1,
     mapHeader:[
        "客户状态",
        "资源来源",
        "加好友日期",
        "姓名",
        "转咨询时间",
        "签约时间",
        "性别",
        "微信号",
        "地区",
        "手机号",
        "所属小助手",
        "所属顾问",
        "所属服务顾问",
        "所属文案",
        "战略顾问",
        "客户身份",
        "学校类型",
        "学校名",
        "课程体系",
        "体系专业",
        "申请层级",
        "申请层级入学时间",
        "专业方向",
        "目标国家",
        "托福",
        "雅思",
        "SAT",
        "ACT",
        "GRE/GMAT",
        "客户信息备注"
      ],
      children:[
        "customer_state",
        "source",
        "date_to_add",
        "name",
        "transfer_time",
        "signing_time",
        "gender",
        "wechat_num",
        "area",
        "phone",
        "little_assistant",
        "consultant",
        "service_consultant",
        "paper_writer",
        "strategy_consultants",
        "identity",
        "school_type",
        "school",
        "curriculum_system",
        "curriculum_system_note",
        "application_level",
        "graduation_date",
        "major",
        "target_country",
        "TOEFL",
        "IELTS",
        "SAT",
        "ACT",
        "GRE",
        "customer_remarks"


      ],
      model: [],
      custtotal: 100,
      customerpage: 1,//页码(查询所有)
      studetnList: [],
      // 初始化全选按钮, 默认不选
      fruitIds: [],
      isCheckedAll: false,
      customer: [],
      customer_state: '',
      sources: [{
        value: '知乎',
        label: '知乎'
      }, {
        value: '群裂变',
        label: '群裂变'
      }, {
        value: '前台电话',
        label: '前台电话'
      }, {
        value: '自有平台',
        label: '自有平台'
      }, {
        value: '线下活动',
        label: '线下活动'
      }, {
        value: '网络搜索',
        label: '网络搜索'
      }, {
        value: '公众号投放',
        label: '公众号投放'
      }, {
        value: '老客户介绍',
        label: '老客户介绍'
      }, {
        value: '其他',
        label: '其他'
      }],
      source: '',
      application_levels: [{
        value: '国内国际学校',
        label: '国内国际学校'
      }, {
        value: '美国高中',
        label: '美国高中'
      }, {
        value: '海本',
        label: '海本'
      }, {
        value: '海本转学',
        label: '海本转学'
      }, {
        value: '海研',
        label: '海研'
      }, {
        value: '海博',
        label: '海博'
      }],
      application_level: '',
      pickerOptions: {
        disabledDate(time) {
          return time.getTime();
        },
      },
      conditionselect:false,//是否条件查询
      customerObj: {
        area: '',
        school: '',
        major: '',
        customerpage: '',
        all: [],
        identity: false,
        filter_search :false,
        graduation_date:"",
        customer_state:"",
        application_level:"",
        source:''
      },
    }
  },
  created() {
      let identity = window.sessionStorage.getItem('department')
      if (identity == "学术成长学院" || identity == "数据管理员" || identity == "超级用户") {
        this.itemshow = true
        }else{
          this.itemshow = false
        }
       var reg = RegExp(/助教/)
       if (reg.test(identity)){
         this.image_div = true
       }else{
         this.image_div = false
       }
       var reg = RegExp(/小助手/)
       if (reg.test(identity)){
         this.assistantdisabled=false
         this.little_helper = true
         this.customer = [{
          value: '未分配未购买',
          label: '未分配未购买'
        },{
          value: '未分配已购买',
          label: '未分配已购买'
        }, ]
       }else{
         this.assistantdisabled= true
         this.little_helper = false
         this.customer = [{
          value: '未分配未购买',
          label: '未分配未购买'
        }, {
          value: '已分配未购买',
          label: '已分配未购买'
        },{
          value: '已流失未购买',
          label: '已流失未购买'
        },{
          value: '再签约未购买',
          label: '再签约未购买'
        }, {
          value: '已签约未购买',
          label: '已签约未购买'
        }, {
          value: '已完成未购买',
          label: '已完成未购买'
        }, {
          value: '未分配已购买',
          label: '未分配已购买'
        }, {
          value: '已分配已购买',
          label: '已分配已购买'
        }, {
          value: '已流失已购买',
          label: '已流失已购买'
        },{
          value: '再签约已购买',
          label: '再签约已购买'
        },{
          value: '已签约已购买',
          label: '已签约已购买'
        }, {
          value: '已完成已购买',
          label: '已完成已购买'
        }]
       }
       this.assistant = JSON.parse(window.sessionStorage.getItem('assistant'))

    this.getstudents();
  },
  methods: {
    // 单选
    checkedOne(fruitId) {
      let idIndex = this.fruitIds.indexOf(fruitId)
      if (idIndex >= 0) {//如果已经包含就去除
        this.fruitIds.splice(idIndex, 1)
      } else {//如果没有包含就添加
        this.fruitIds.push(fruitId)
      }
    },
    // 全选/反选
    checkedAll() {
      if (this.fruitIds.length == 0) {
        this.fruitIds = []
        this.studetnList.forEach(item => {
          this.fruitIds.push(item.id)
        })
      } else {
        this.studetnList.forEach(item => {
          let idIndex = this.fruitIds.indexOf(item.id)
          if (idIndex >= 0) {//如果已经包含就去除
            this.fruitIds.splice(idIndex, 1)
          } else {
            this.fruitIds.push(item.id)
          }
        })
      }
    },
    nocheckedAll() {
      this.fruitIds = []
    },
    async deletestudent(){
      if (this.fruitIds.length>0){
        const res = await this.$ajax.delete(`/selectquery/`, {
          data: this.fruitIds
        });
        if (res.data.status == 200) {
            this.$message({
              type: 'success',
              message: res.data.message
            })
            this.fuzzyselect()
        } else {
          this.$message({
            type: 'warning',
            message: '服务器连接失败'
          })
        }}else{
          this.$message({
          type: 'warning',
          message: "请选择需要删除项"});
          return
      }
      },
    async fuzzyselect(){
      this.judge_cust=false
      window.sessionStorage.setItem("judge_cust", JSON.stringify(this.judge_cust))
      this.judge_sele = true
      window.sessionStorage.setItem("judge_sele",JSON.stringify(this.judge_sele))
      this.customerpage = 1
      this.customerObj.area = ''
      this.customerObj.customer_state = ''
      this.customerObj.graduation_date = ''
      this.customerObj.major = ''
      this.customerObj.school = ''
      this.customerObj.source = ''
      this.customerObj.application_level = ''
      this.customer_state = ''
      this.source = ''
      this.application_level=''
      this.studetnList = []
      if (this.selectinput){
      this.filter_search = true
      // 保存数据
      window.sessionStorage.setItem("selectinput", JSON.stringify(this.selectinput))
      }else{
        window.sessionStorage.removeItem("selectinput")
        this.filter_search = false
        this.customerpage = JSON.parse(new Number(window.sessionStorage.getItem('customerpage')))
        if (this.customerpage){
        }else{
          this.customerpage=1
        }
        this.tofindthe()
        return
      }
      let identity = window.sessionStorage.getItem('department')
      if (identity == "学术成长学院" || identity == "数据管理员" || identity == "超级用户") {
        var data = {
          little_helper:this.little_helper,
          name:this.selectinput,
          username:window.sessionStorage.getItem("username"),
          pag:this.customerpage,
          identity:true
        }
      }else{
          var data = {
          little_helper:this.little_helper,
          name:this.selectinput,
          username:window.sessionStorage.getItem("username"),
          pag:this.customerpage,
          identity:false
        }
      }
      const res = await this.$ajax.post(`/selectquery/`, data);
      let obj = JSON.parse(res.data);
      if (obj.status==200){
          // 保存总数据
          window.sessionStorage.setItem("all_students", JSON.stringify(obj.data_infor))
          // 总数量
          window.sessionStorage.setItem("custtotal", obj.custpag)
          // 当前
          window.sessionStorage.setItem("customerpage", this.customerpage)
          this.custtotal = obj.custpag
          if (this.custtotal>10){
          this.studetnList = obj.data_infor.slice(0,10)
          }else{
            this.studetnList = obj.data_infor.slice(0,this.custtotal)
          }
          // 保存当前数据
          window.sessionStorage.setItem("studetnList", JSON.stringify(this.studetnList))
      }else{
            this.$message({
            type: 'warning',
            message: obj.message
          });
          this.studetnList = []
      }
      this.custtotal = obj.custpag
    },
    async getstudents() {
      var sessiondata = JSON.parse(window.sessionStorage.getItem('studetnList'))
      if (sessiondata && sessiondata.length>0) {
        this.studetnList = []
        this.studetnList = sessiondata
        this.customerpage = JSON.parse(new Number(window.sessionStorage.getItem('customerpage')))
        this.custtotal = JSON.parse(new Number(window.sessionStorage.getItem('custtotal')))
        var judge_ = JSON.parse(window.sessionStorage.getItem('judge_sele'))
        if (judge_){
          this.selectinput = JSON.parse(window.sessionStorage.getItem('selectinput'))
        }
        var cust = JSON.parse(window.sessionStorage.getItem('judge_cust'))
        if(cust){
          this.customerObj = JSON.parse(window.sessionStorage.getItem('customerObj'))
          this.customer_state = this.customerObj.customer_state
          this.source = this.customerObj.source
          this.application_level = this.customerObj.application_level
        }
        
      } else {
        let username = window.sessionStorage.getItem("username")
        let identity = window.sessionStorage.getItem('department')
        if (identity == "学术成长学院" || identity == "数据管理员" || identity == "超级用户") {
          this.customerObj.little_helper = this.little_helper
          this.customerObj.username = username
          this.customerObj.identity = true
          const superstudetns = await this.$ajax.post(`filterdepartment/`, this.customerObj)
          let obj = JSON.parse(superstudetns.data);
          // 保存总数据
          window.sessionStorage.setItem("all_students", JSON.stringify(obj.data_infor))
          // 总数量
          window.sessionStorage.setItem("custtotal", obj.custpag)
          // 当前
          window.sessionStorage.setItem("customerpage", this.customerpage)
          this.custtotal = obj.custpag
          if (this.custtotal>10){
          this.studetnList = obj.data_infor.slice(0,10)
          }else{
            this.studetnList = obj.data_infor.slice(0,this.custtotal)
          }
          // 保存当前数据
          window.sessionStorage.setItem("studetnList", JSON.stringify(this.studetnList))
        } else {
          this.customerObj.little_helper = this.little_helper
          let username = window.sessionStorage.getItem("username") 
          this.customerObj.username = username
          this.customerObj.customerpage = this.customerpage
          const studetns = await this.$ajax.post(`filterdepartment/`, this.customerObj)
          let obj = JSON.parse(studetns.data);
          // 保存总数据
          window.sessionStorage.setItem("all_students", JSON.stringify(obj.data_infor))
          // 总数量
          window.sessionStorage.setItem("custtotal", obj.custpag)
          // 当前
          window.sessionStorage.setItem("customerpage", this.customerpage)
          this.custtotal = obj.custpag
          if (this.custtotal>10){
          this.studetnList = obj.data_infor.slice(0,10)
          }else{
            this.studetnList = obj.data_infor.slice(0,this.custtotal)
          }
          // 保存当前数据
          window.sessionStorage.setItem("studetnList", JSON.stringify(this.studetnList))
        }
      }  },
    async detailedinfor(studentns_id,student_index) {
      window.sessionStorage.setItem("student_index",student_index)
      const studetninfor = await this.$ajax.get(`filterdepartment/${studentns_id}/`);
      const information = JSON.parse(studetninfor.data)
      window.sessionStorage.setItem("information", JSON.stringify(information))

      this.$router.push(
        {
          path: '/informationmaster/',
        });
    },
    async cutleCurentChange(pageValue) {
      var all_students = JSON.parse(window.sessionStorage.getItem('all_students'))
        this.studetnList = []
        this.studetnList = all_students.slice(10*pageValue-10,10*pageValue)
        // 保存当前数据
          window.sessionStorage.setItem("studetnList", JSON.stringify(this.studetnList))
      },
    async tofindthe() {
      this.judge_sele =false
      this.selectinput = ''
      window.sessionStorage.setItem("judge_sele", JSON.stringify(this.judge_sele))
      this.customerpage = 1
      this.judge_cust = true
      window.sessionStorage.setItem("judge_cust",JSON.stringify(this.judge_cust))
      let identity = window.sessionStorage.getItem('department')
      if (identity == "学术成长学院" || identity == "数据管理员" || identity == "超级用户") {
        this.customerObj.identity = true
      }
      this.customerObj.assvalue = this.assvalue
      this.customerObj.little_helper = this.little_helper
      this.conditionselect = true
      this.selectinput = ''
      this.studetnList = []
      this.customerObj.customer_state = this.customer_state
      this.customerObj.customerpage = this.customerpage
      this.customerObj.source = this.source
      let department = window.sessionStorage.getItem("department")
      this.customerObj.department = department
      this.customerObj.application_level = this.application_level
      this.customerObj.username = window.sessionStorage.getItem("username") 
      const res = await this.$ajax.post(`/studentquery/`, this.customerObj);
      let obj = JSON.parse(res.data);
      if (obj.status==200){
      // 保存总数据
      window.sessionStorage.setItem("all_students", JSON.stringify(obj.data_infor))
      window.sessionStorage.setItem("customerObj", JSON.stringify(this.customerObj))
      // 总数量
      window.sessionStorage.setItem("custtotal", obj.custpag)
      // 当前
      window.sessionStorage.setItem("customerpage", this.customerpage)
      // 当前
      window.sessionStorage.setItem("conditionselect", this.conditionselect)
      this.custtotal = obj.custpag
      if (this.custtotal>10){
          this.studetnList = obj.data_infor.slice(0,10)
      }else{
          this.studetnList = obj.data_infor.slice(0,this.custtotal)
        }
      // 保存当前数据
      window.sessionStorage.setItem("studetnList", JSON.stringify(this.studetnList))
      }
      else{
        this.$message({
          type: 'warning',
          message: "未找到满足条件学生"})
      }
    },
    async resetLoginForm(){
        this.customerObj.area = ''
        this.customerObj.customer_state = ''
        this.customerObj.graduation_date = ''
        this.customerObj.major = ''
        this.customerObj.school = ''
        this.customerObj.source = ''
        this.customerObj.application_level = ''
        this.customer_state = ''
        this.source = ''
        this.application_level=''
        this.customerpage = 1
        window.sessionStorage.setItem("customerObj", JSON.stringify(this.customerObj))
        window.sessionStorage.removeItem("studetnList")
        this.judge_cust=false
        window.sessionStorage.setItem("judge_cust", JSON.stringify(this.judge_cust))
        this.judge_sele =false
        this.selectinput = ''
        window.sessionStorage.setItem("judge_sele", JSON.stringify(this.judge_sele))
        this.getstudents()
    },
    async handleDownload(opints) {
      if(this.little_helper){
        this.$message({
          type: 'warning',
          message: "权限不足，无法下载"});
          return
      }
      var judge_cust = window.sessionStorage.getItem("judge_cust")
      var judge_sele = window.sessionStorage.getItem("judge_sele")
      let identity = window.sessionStorage.getItem('department')
      if (identity == "学术成长学院" || identity == "数据管理员" || identity == "超级用户") {
          this.customerObj.identity = true
        }
      if (opints == 'all') {
        this.customerObj.all = []
        this.customerObj.all.push(opints)
      } else {
        if (opints.length>0){
          const res = await this.$ajax.post(`/downloadid/`, opints);
          var shuju = JSON.parse(res.data)
          var data = {
          tableData: shuju.data_info,
          children: this.children
          }
          this.comExportToExcel(data, this.mapHeader,"用户信息主表")
          return
        }else{
          this.$message({
          type: 'warning',
          message: "请选择需要下载项"});
          return
          }
      }
      if (judge_cust=="true"){
        this.customerObj.customer_state = this.customer_state
        this.customerObj.source = this.source
        let department = window.sessionStorage.getItem("department")
        this.customerObj.department = department
        this.customerObj.application_level = this.application_level
        this.customerObj.username = window.sessionStorage.getItem("username") 
        const res = await this.$ajax.post(`/downloadstudent/`, this.customerObj);
        var student_ = JSON.parse(res.data)
        if (student_.message==200){
            var data = {
            tableData: student_.data_info,
            children: this.children
            }
            this.comExportToExcel(data, this.mapHeader,"用户信息主表");
            return
        }else{
          this.$message({
          type: 'warning',
          message: select_name.message});
          return
          }
      }
      if (judge_sele=="true"){
        this.customerObj.customer_state = this.customer_state
        this.customerObj.source = this.source
        let department = window.sessionStorage.getItem("department")
        this.customerObj.department = department
        this.customerObj.name = this.selectinput
        this.customerObj.application_level = this.application_level
        this.customerObj.username = window.sessionStorage.getItem("username") 
        const res = await this.$ajax.post(`/downloadselect/`, this.customerObj);
        var select_name = JSON.parse(res.data)
        if (select_name.status==200){
          var data = {
          tableData: select_name.data_infor,
          children: this.children
          }
          this.comExportToExcel(data, this.mapHeader,"用户信息主表");
          return
        }else{
          this.$message({
          type: 'warning',
          message: select_name.message});
          return
          }
      }else{
        this.customerObj.customer_state = this.customer_state
        this.customerObj.source = this.source
        let department = window.sessionStorage.getItem("department")
        this.customerObj.department = department
        this.customerObj.application_level = this.application_level
        this.customerObj.username = window.sessionStorage.getItem("username") 
        const res = await this.$ajax.post(`/downloadstudent/`, this.customerObj);
        var student_ = JSON.parse(res.data)
        if (student_.message==200){
            var data = {
            tableData: student_.data_info,
            children: this.children
            }
            this.comExportToExcel(data, this.mapHeader,"用户信息主表");
            return
        }else{
          this.$message({
          type: 'warning',
          message: select_name.message});
          return
          }
      }

    },
  },
}
</script>

<style scoped>
.checkedlabel{
  cursor: pointer;
}
.checkednolabel{
  cursor: pointer;
  margin-left: 20px;
}
.droplabel{
  cursor: pointer;
  margin-left: 560px;
}
.btnBox {
  display: flex;
  justify-content: center;
  align-items: center;
}
.customerObj {
  margin-top: 30px;
}
#select_btn {
  /* width: 100px; */
  height: 25px;
  margin-left: 200px;
  color: #094572;
  margin-right: 20px;
  margin-top: 30px;
  cursor: pointer;
  /* outline:none; */
}
.personnel_info input {
  margin-left: 15px;
}
.usernamediv {
  width: 130px;
  float: left;
  cursor: pointer;
  overflow:hidden;
  text-overflow:ellipsis;
  white-space:nowrap;
}
.checkboxdiv {
  float: left;
}
.schooldiv {
  width: 280px;
  float: left;
  cursor: pointer;
  overflow:hidden;
  text-overflow:ellipsis;
  white-space:nowrap;
}
.imageshowdiv{
  overflow:hidden;
  text-overflow:ellipsis;
  white-space:nowrap;
  display: block;
}
.imageshow{
  width: 40px;
  height: 40px;
  float: left;
  cursor: pointer;
  overflow:hidden;
  text-overflow:ellipsis;
  white-space:nowrap;
  display: block;
}
.graduationdiv {
  width: 280px;
  float: right;
  cursor: pointer;
  overflow:hidden;
  text-overflow:ellipsis;
  white-space:nowrap;
}
.personnel_info img {
  margin-left: 5px;
  margin-top: 8px;
}
.personnel_info {
  overflow: hidden;
  margin-left: 200px;
  font-size: 16px;
  margin-bottom: 30px;
  /* float: left; */
}
.pinfo {
  width: 1200px;
  min-height: 450px;
  margin-top: 10px;
}
.per2_line {
  width: 500px;
  height: 30px;
  float: left;
  background-color: #e1e5e9;
  color: #094572;
  margin-left: 70px;
  border-radius: 10px;
}
.per_line {
  height: 45px;
  width: 800px;
  /* float:left; */
  background-color: #e1e5e9;
  color: #094572;
  border-radius: 10px;
  cursor: pointer;
  line-height: 45px;
  /* display: inline-block; */
}

/* 绘制虚线 style="display:none; 显示不显示*/
.filter {
  height: 190px;
  border-bottom: 1px dashed #094572;
}
.selectdiv{
  margin-left: 170px;
  margin-top: 30px;
}
.reset_btn {
  height: 50px;
  width: 100px;
  margin-left: 200px;
  background-color: #094572;
  color: #fff;
  font-size: 20px;
  border-radius: 10px;
  outline: none;
}
#my_find {
  height: 120px;
  width: 80px;
  margin-left: 158px;
  background-color: #094572;
  color: #fff;
  font-size: 14px;
  border-radius: 10px;
  outline: none;
}
select {
  width: 160px;
  height: 30px;
  color: #094572;
  margin-left: 10px;
  text-align: center;
  text-align-last: center;
  border-radius: 10px;
  background-color: #f2f4fb;
}
.each_line input {
  width: 160px;
  height: 30px;
  color: #094572;
  margin-left: 10px;
  text-align: center;
  text-align-last: center;
  border-radius: 10px;
  background-color: #f2f4fb;
  outline: none;
}
.each_line {
  height: 30px;
  font-size: 14px;
  margin-left: 33px;
  color: #094572;
  margin-top: 30px;
}
.prompt1 {
  margin-left: 80px;
}
.prompt2 {
  margin-left: 42px;
}
/* 筛选条件 */
.datatext {
  height: 36px;
  line-height: 36px;
  text-align: center;
  color: #094572;
  margin-left: 10px;
}
.line {
  display: inline-block;
  width: 544px;
  border-top: 1px solid #cccccc;
  vertical-align: 5px;
  margin-top: 30px;
  font-weight: bold;
}
/* 头标签 */
.datahead {
  height: 40px;
  background-color: #094572;
  border-radius: 10px;
  border: none;
}
.datahead a {
  color: #fff;
  text-decoration: none;
  margin-left: 11px;
  line-height: 40px;
}
.find_btn {
  height: 50px;
  width: 100px;
  margin-left: 296px;
  background-color: #094572;
  color: #fff;
  font-size: 20px;
  border-radius: 10px;
  outline: none;
}
.el-pagination {
  text-align: center;
}
.selectedDownload {
  width: 200px;
  height: 50px;
  font-size: 18px;
  margin-top: 30px;
  margin-bottom: 30px;
  border-radius: 10px;
}
.allDownload{
  width: 200px;
  height: 50px;
  font-size: 18px;
  margin-top: 30px;
  margin-bottom: 30px;
  border-radius: 10px;
}
.el-input{
  width: 100px;
}
.select_btn{
  width: 55px;
  height: 40px;
  margin-left: 165px;
  color: #fff;
  background-color: #094572;
  border-radius: 15px;
  outline: none;
}
.school_item{
  margin-left: 150px;
}
#elbutset{
  margin-left: 100px;
}
</style>
