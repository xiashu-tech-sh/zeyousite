<template>
  <div class="datashow">
    <div class="datahead">
        <a class="one_a" @click="customerpath()">客户信息 ></a>
        <a class="two_a" @click="informationmaster()">用户信息主表 ></a>
        <a class="there_a">营销信息 </a>
    </div>
    <div id="select_btn">
      <label class="checkedlabel" @click="checkedAll"> 全选/反选</label>
      <label class="checkednolabel" @click="nocheckedAll"> 全不选</label>
      <label v-show="itemshow" class="droplabel" @click="deletestudent()">刪除选中部分</label>   
    </div>
    <div class="pinfo">
      <div class="personnel_info" v-for="(item,make_index) in makeList" :key="item.id"
      @contextmenu.prevent="contextmenu($event,make_index)">
        <div class="per_line">
          <div class="checkboxdiv">
            <input type="checkbox" :checked="fruitIds.indexOf(item.id)>=0" name="checkboxinput" class="input-checkbox" @click="checkedOne(item.id)">
          </div>
          <div class="usernamediv" @click="detailedinfor(item.id)">
            <img src="../../assets/username.png" alt="">
            <span> {{item.name}}</span>
          </div>
          <div class="imageshow">
          <div v-show="image_div" class="imageshowdiv">
            <img v-show="item.warning_show=='true'" src="../../assets/warning.png" id="imgshow">
          </div>
          </div>
          <div class="teachdiv" @click="detailedinfor(item.id)">
            <span>助教：{{item.teaching_assistant}}</span>
          </div>
          <div class="schooldiv" @click="detailedinfor(item.id)">
            <span>产品内容：{{item.product}}</span>
          </div>
          <div class="graduationdiv" @click="detailedinfor(item.id)">
            <span>推进状态：{{item.cur_state}}</span>
          </div>
          <div class="flot_is">
            <span>>>></span>
          </div>
          <div class="popover" v-if="isShowPopover" :style="computedStyle">
            <div class="li" v-for="(item_name,index) in popoverList" :key="index" @click="follow_up(item)">{{item_name.name}}</div>
          </div>
        </div>
      </div>
    </div>
    <el-pagination background layout="prev, pager, next" :current-page="makecustomerpage" :total="maketotal" @current-change="cutleCurentChange">
    </el-pagination>
    <div class="btnBox">
      <el-button class="allDownload" type="primary" @click="adddata()">添加数据</el-button>
      <el-button class="selectedDownload" type="primary" @click="handleDownload(fruitIds)">导出xlsx(选中部分)</el-button>
      <el-button class="allDownload" type="primary" @click="handleDownload('all')">{{ThirdColumn}}</el-button>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      image_div: false,
      diff : 0,
      make_index :0,
      isShowPopover: false,
      popoverLeft: 0,
      popoverTop: 0,
      popoverList:[
        {
          name:"跟进",
          prop:"follow_up"
        }
      ],
      academic :false,
      ThirdColumn :"",
      itemshow:true,
      selectinput:'',
      selectpag:1,
     mapHeader:[
        "订单号",
        "姓名",
        "客户来源",
        "产品类型",
        "产品名称",
        "课程体系分类",
        "难度级别",
        "内容方向",
        "班型大小",
        "分配助教",
        "所属销售人员",
        "授课老师",
        "购买时间",
        "产品内容",
        "上课日期",
        "预计课时",
        "已用课时",
        "剩余课时",
        "导师报价/时",
        "总价",
        "推进状态",
        "跟进周期"
      ],
      children:[
        "order_number",
        "name",
        "source",
        "product_type",
        "product_name",
        "calss_course",
        "difficulty_level",
        "content_direction",
        "class_size",
        "teaching_assistant",
        "sales",
        "teacher",
        "date_of_purchasing",
        "product",
        "date_of_lecture",
        "hours_of_lecture",
        "has_been_lecture",
        "the_remaining_lecture",
        "price_per_hour",
        "price_overall",
        "cur_state",
        "follow_period"
      ],
      model: [],
      maketotal: 10,
      makecustomerpage: 1,//页码(查询所有)
      makeList: [],
      // 初始化全选按钮, 默认不选
      fruitIds: [],
      url_update_add: true,
      customer: [{
        value: '未分配未购买',
        label: '未分配未购买'
      }, {
        value: '已分配未购买',
        label: '已分配未购买'
      }, {
        value: '未分配已购买',
        label: '未分配已购买'
      }, {
        value: '已分配已购买',
        label: '已分配已购买'
      }, {
        value: '已签约未购买',
        label: '已签约未购买'
      }, {
        value: '已签约已购买',
        label: '已签约已购买'
      }, {
        value: '已完成未购买',
        label: '已完成未购买'
      }, {
        value: '已完成已购买',
        label: '已完成已购买'
      }],
      customer_state: '',
      sources: [{
        value: '知乎',
        label: '知乎'
      }, {
        value: '群裂变',
        label: '群裂变'
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
        value: '海研',
        label: '海研'
      }, {
        value: '海本',
        label: '海本'
      }, {
        value: '海博',
        label: '海博'
      }, {
        value: '国内国际学校',
        label: '国内国际学校'
      }],
      application_level: '',
      pickerOptions: {
        disabledDate(time) {
          return time.getTime();
        },
      },
      _name :'',
      graduation_date: '',
      makeObj: {
        username:'',
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
    if (identity == "学术成长学院"){
      this.academic = true
      this.ThirdColumn = "导出xlsx(已购买)"
    }else{
        this.academic = false
        this.ThirdColumn = "导出xlsx(全部信息)"
        }
    this.makeinfor();
  },
    computed: {
    computedStyle() {
      return {
        left: `${this.popoverLeft + 5}px`,
        top: `${this.popoverTop  + 15}px`
      };
    }
  },
  mounted() {
      window.addEventListener('scroll', this.handleScroll);
    },
  methods: {
    handleScroll() {
      this.diff= document.documentElement.scrollTop
      },
    async follow_up(item){
      if(this.makeList[this.make_index].follow_period){
        this.isShowPopover = false
        this.makeList[this.make_index].warning_show = "false"
        window.sessionStorage.setItem("makeList", JSON.stringify(this.makeList))
        var item ={
        "item_id":this.makeList[this.make_index].id,
        "item_name":this.makeList[this.make_index].name
        }
        const studetns = await this.$ajax.post(`followupdate/`, item)
        if (studetns.data.status == 200) {
            this.$message({
            showClose: true,
            message: studetns.data.message,
            type: 'success'
            })
            if (studetns.data.upstatus ==200){
              var index = window.sessionStorage.getItem('student_index')
              var studetnList = JSON.parse(window.sessionStorage.getItem('studetnList'))
              studetnList[index].warning_show='false'
              window.sessionStorage.setItem("studetnList", JSON.stringify(studetnList))
            }
          }else {
            this.$message({
                type: "warning",
                message: aca_res.data.message
                })
          }
      }else{
        this.$message({
        type: "warning",
        message: "请选择跟进周期"
        })
      }

    },
    contextmenu(e,id) {
      this.make_index = id
      this.isShowPopover = true;
      this.popoverLeft = e.clientX;
      this.popoverTop = e.clientY + this.diff;
    },
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
        this.makeList.forEach(item => {
          this.fruitIds.push(item.id)
        })
      } else {
        this.makeList.forEach(item => {
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
      const res = await this.$ajax.delete(`/makeinfor/`, {
          data: this.fruitIds
        });
        if (res.data.status == 200) {
            this.$message({
              type: 'success',
              message: res.data.message
            })
      const studetns = await this.$ajax.post(`makeinfor/`, this.makeObj)
      let obj = JSON.parse(studetns.data);
        if (obj.status == 200) {
          
          this.url_update_add = false
          window.sessionStorage.setItem("makeList", JSON.stringify(obj.data_infor))
          // 总数量
          window.sessionStorage.setItem("makecusttotal", obj.custpag)
          // 当前
          window.sessionStorage.setItem("makecustomerpage", this.makecustomerpage)
          this.maketotal = obj.custpag
          this.makeList = obj.data_infor
          }else{
            window.sessionStorage.setItem("makeList", [])
            this.url_update_add = true
            this.$router.push({
            path: '/academicinfor/',
            query: {
            username:this._name,
            url_update_add:this.url_update_add,
            addtype:false
        }
      }
      );
          }
        } else {
          this.$message({
            type: 'warning',
            message: '服务器连接失败'
          })
        }

    },
    async makeinfor() {
      var data = window.sessionStorage.getItem("makeList")
      if (data){
        this.makeList = JSON.parse(data);
        this.maketotal = JSON.parse(new Number(window.sessionStorage.getItem('makecusttotal')))
        this.makecustomerpage = JSON.parse(new Number(window.sessionStorage.getItem('makecustomerpage')))
        this.url_update_add = false
      }
      else{
      this.makeObj.username = this.$route.query.username,
      this._name = this.$route.query.username,
      this.makeObj.makecustomerpage = this.makecustomerpage
      const studetns = await this.$ajax.post(`makeinfor/`, this.makeObj)
      let obj = JSON.parse(studetns.data);
        if (obj.status == 200) {
          this.url_update_add = false
          window.sessionStorage.setItem("makeList", JSON.stringify(obj.data_infor))
          // 总数量
          window.sessionStorage.setItem("makecusttotal", obj.custpag)
          // 当前
          window.sessionStorage.setItem("makecustomerpage", this.makecustomerpage)
          this.maketotal = obj.custpag
          this.makeList = obj.data_infor
          }else{
            this.url_update_add = true
            this.$router.push({
            path: '/academicinfor/',
            query: {
            username:this.makeObj.username,
            url_update_add:this.url_update_add,
            addtype:false
        }
      }
      );
          }
        }}
      ,
    async detailedinfor(makeinfor_id) {
      // const makeifor = await this.$ajax.get(`makeinfor/${makeinfor_id}/`);
      // const information = JSON.parse(makeifor.data)
      this.$router.push({
        path: '/academicinfor/',
        query: {
          makeinfor_id: makeinfor_id,
          url_update_add:this.url_update_add,
          addtype:false
        }
      }
      );
    },
    async cutleCurentChange(pageValue) {
        this.makeObj.username = this.$route.query.username,
        this.makeObj.makecustomerpage = pageValue
        const studetns = await this.$ajax.post(`makeinfor/`, this.makeObj)
        let obj = JSON.parse(studetns.data);
        window.sessionStorage.setItem("makeList", JSON.stringify(obj.data_infor))
        // 总数量
        window.sessionStorage.setItem("makecusttotal", obj.custpag)
        // 当前
        window.sessionStorage.setItem("makecustomerpage", this.makecustomerpage)
        this.custtotal = obj.custpag
        this.makeList = obj.data_infor;
    },
    informationmaster (){
      this.$router.push("/informationmaster");
    },
    customerpath(){
        this.$router.push("/customer");
    },
    async adddata(){
            this.url_update_add = true
            this.$router.push({
            path: '/academicinfor/',
            query: {
            username:this.$route.query.username,
            url_update_add:this.url_update_add,
            addtype:true
            }
      }
      )},
    async handleDownload(opints) {
      // 先清空数据
      this.makeObj.all = []
      // let username = window.sessionStorage.getItem("username") 
      if (opints == 'all') {
        this.makeObj.all.push(opints)
      } else {
        this.makeObj.all = opints
      }
      if (opints.length>0){
        if (this.academic){
        const res = await this.$ajax.post(`/academicdownloadacad/`, this.makeObj);
        let data = {
        tableData: JSON.parse(res.data),
        children: this.children
        }
        this.comExportToExcel(data, this.mapHeader,"学术成长学院营销信息表");
        }else{
        const res = await this.$ajax.post(`/downloadacadinfor/`, this.makeObj);
        let data = {
          tableData: JSON.parse(res.data),
          children: this.children
        }
        this.comExportToExcel(data, this.mapHeader,"学术成长学院营销信息表");
      }

      }else{
          this.$message({
          type: 'warning',
          message: "请选择需要下载项"});
          return
          }

    }
  },
      destroyed() {
      window.removeEventListener('scroll', this.handleScroll);
    }
}
</script>

<style scoped lang="less">
.btnBox {
  display: flex;
  justify-content: center;
  align-items: center;
}
#select_btn {
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
  width: 150px;
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
  width: 240px;
  float: left;
  cursor: pointer;
  overflow:hidden;
  text-overflow:ellipsis;
  white-space:nowrap;
}
.flot_is{
  width: 50px;
  float: right;
  cursor: pointer;
}
.teachdiv{
  width: 130px;
  float: left;
  cursor: pointer;
  overflow:hidden;
  text-overflow:ellipsis;
  white-space:nowrap;
}
.graduationdiv {
  width: 160px;
  float: left;
  cursor: pointer;
  overflow:hidden;
  text-overflow:ellipsis;
  white-space:nowrap;
}
.personnel_info img {
  margin-left: 5px;
  margin-top: 8px;
}
// .personnel_info {
//   overflow: hidden;
//   margin-left: 200px;
//   font-size: 16px;
//   margin-bottom: 30px;
// }
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
  background-color: #e1e5e9;
  color: #094572;
  border-radius: 10px;
  cursor: pointer;
  line-height: 45px;
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
/* 头标签 */
.datahead {
  height: 40px;
  background-color: #094572;
  border-radius: 10px;
  border: none;
}
.el-pagination {
  text-align: center;
}
.checkedlabel {
  cursor: pointer;
}
.checkednolabel {
  margin-left: 30px;
  cursor: pointer;
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
.one_a, .two_a{
    color: rgb(141, 138, 138);
    cursor: pointer;
}
.there_a{
    color: #fff;
    text-decoration: none;
    margin-left: 11px;
    line-height: 40px;
}
.droplabel{
  cursor: pointer;
  margin-left: 560px;
}

.personnel_info {
  overflow: hidden;
  margin-left: 200px;
  font-size: 16px;
  margin-bottom: 30px;
  overflow: hidden;
  padding-right: 30px;
  max-width: calc(100vw - 64px);
  .tag {
    font-family: PingFangSC-Regular;
    font-size: 10px;
    color: #ffffff;
    letter-spacing: 0.3px;
    height: 18px;
    line-height: 18px;
    cursor: pointer;
    padding: 0 10px;
    border-right: 1px solid #4b5058;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    .name {
      display: inline-block;
      margin-right: 6px;
    }
  }
  .popover {
    position: fixed;
    background: #fff;
    border-radius: 4px;
    box-shadow: 2px 2px 3px 0 rgba(0, 0, 0, 0.3);
    color: #333;
    font-size: 14px;
    font-weight: 400;
    list-style-type: none;
    margin: 0;
    padding: 5px 0;
    position: absolute;
    z-index: 100;
    width: 80px;
    // height: 118px;
    .li {
      height: 27px;
      line-height: 27px;
      cursor: pointer;
      padding-left: 16px;
      &:hover{
        background: #cccccc;
      }
    }
  }
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
</style>
