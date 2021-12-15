<template>
    <div>
        <div class="datashow">
            <div class="datahead">
                <a class="one_a" @click="customer()">客户信息 ></a>
                <a class="two_a" @click="informationmaster()">用户信息主表 ></a>
                <a class="there_a"  @click="lookacademic()">营销信息表> </a>
                <a class="foru_a">学术成长学院营销信息表 </a>
            </div>
            <el-form :inline="true" :rules="rules" :model="acadeinfor" ref="acadeinfor" class="masterinfor">
                <el-form-item label="订单号" class="one_label" id="amend" >
                    <el-input placeholder="" v-model="acadeinfor.order_number" :disabled="true"></el-input>
                </el-form-item>
                <el-form-item label="姓名" class="one_label" id="amend">
                    <el-input v-model="acadeinfor.name" :disabled="true" ></el-input>
                </el-form-item>
                <el-form-item label="客户来源" id="amend" >
                    <el-input v-model="acadeinfor.source"  placeholder="请输入客户来源" ></el-input>
                </el-form-item>
                <el-form-item label="产品类型" id="amend" >
                    <el-input v-model="acadeinfor.product_type" placeholder="请输入产品类型"></el-input>
                </el-form-item>
                <el-form-item label="产品名称" id="amend" >
                    <el-input v-model="acadeinfor.product_name" placeholder="请输入产品名称"></el-input>
                </el-form-item>
                <el-form-item label="课程体系分类" id="amend" >
                    <el-input v-model="acadeinfor.calss_course" placeholder="请输入课程体系分类"></el-input>
                </el-form-item>
                <el-form-item label="难度级别" id="amend" >
                    <el-input v-model="acadeinfor.difficulty_level" placeholder="请输入难度级别"></el-input>
                </el-form-item>
                <el-form-item label="内容方向" id="amend" >
                    <el-input v-model="acadeinfor.content_direction" placeholder="请输入内容方向"></el-input>
                </el-form-item>
                <el-form-item label="班型大小" id="amend" >
                    <el-input v-model="acadeinfor.class_size" placeholder="请输入班型大小"></el-input>
                </el-form-item>
                <el-form-item label="分配助教" id="amend">
                <el-select v-model="teachvalue" placeholder="请选择" style="display:block">
                    <el-option v-for="item in teaching_assistant" :key="item.id" :label="item.name" :value="item.name">
                    </el-option>
                </el-select>
                </el-form-item>
                <el-form-item label="所属销售人员" id="amend">
                    <el-input v-model="acadeinfor.sales" placeholder="请输入销售人员"></el-input>
                </el-form-item>
                <el-form-item label="授课老师" id="amend" >
                    <el-input v-model="acadeinfor.teacher" placeholder="请输入授课老师"></el-input>
                </el-form-item>
                <el-form-item label="购买时间" id="amend" prop="date_of_purchasing">
                    <el-date-picker value-format="yyyy-MM-dd" v-model="acadeinfor.date_of_purchasing" type="date" placeholder="请选择购买时间">
                    </el-date-picker>
                </el-form-item>
                <el-form-item label="产品内容" id="acadeid">
                    <el-input v-model="acadeinfor.product" placeholder="请输入产品内容"></el-input>
                </el-form-item>
                <el-form-item label="上课日期" id="amend" >
                    <el-date-picker value-format="yyyy-MM-dd" v-model="acadeinfor.date_of_lecture" type="date" placeholder="请选择上课日期">
                    </el-date-picker>
                </el-form-item>
                <el-form-item label="预计课时" id="special" >
                    <el-input v-model="acadeinfor.hours_of_lecture" placeholder="请输入预计课时"></el-input>
                </el-form-item>
                <el-form-item label="已用课时" id="amend" >
                    <el-input v-model="acadeinfor.has_been_lecture" placeholder="请输入已用课时"></el-input>
                </el-form-item>
                <el-form-item label="剩余课时" id="amend">
                    <el-input v-model="acadeinfor.the_remaining_lecture" placeholder="请输入剩余课时"></el-input>
                </el-form-item>
                <el-form-item label="导师报价元/时" id="amend">
                    <el-input v-model="acadeinfor.price_per_hour" placeholder="导师报价（元/时）"></el-input>
                </el-form-item>
                <el-form-item label="总价" id="amend">
                    <el-input v-model="acadeinfor.price_overall" placeholder="请输入总价"></el-input>
                </el-form-item>
                <el-form-item label="推进状态" id="amend">
                    <el-input v-model="acadeinfor.cur_state" placeholder="推进状态"></el-input>
                </el-form-item>
                <el-form-item label="跟进周期" id="amend">
                <el-select v-model="follow_period" placeholder="请选择">
                    <el-option v-for="item in follow_periods" :key="item.value" :label="item.label" :value="item.value">
                    </el-option>
                </el-select>
                </el-form-item>
                <br>
              <el-form-item>
                <el-button type="primary" @click="AddAcademic()">{{ update_add }}</el-button>
                <el-button type="primary" @click="handleDownload(false)">导出生成xlsx</el-button>
            </el-form-item>
            </el-form>
        </div>
    </div>
</template>
<script>
export default {
  data () {
    return {
    follow_periods: [{
        value: '每周',
        label: '每周'
      }, {
        value: '每两周',
        label: '每两周'
      }, {
        value: '每月',
        label: '每月'
      }],
      follow_period: '',
        rules: {
            date_of_purchasing: [{
            required: true,
            message: "购买时间不能为空",
            trigger: "blur"
            }],
        },
      update_add :"更新信息",
      url_update_add :true, // false 更新数据  true 添加数据
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
      addtype:"",
      teaching_assistant:'',
      teachvalue:"",
      academicintotal:'',
      acadeinfor:{
        id:'',
        order_number:"",
        name:"",
        source:"",
        product_type:"",
        product_name:"",
        difficulty_level:"",
        content_direction:"",
        class_size:"",
        sales:"",
        teacher:"",
        date_of_purchasing:"",
        product:"",
        date_of_lecture:"",
        hours_of_lecture:"",
        has_been_lecture:"",
        the_remaining_lecture:"",
        price_per_hour:"",
        price_overall:"",
        cur_state:"",
        calss_course:""
        },
    }
  },
  created () {
    this.getmakedata()
  },
  methods: {
    async getmakedata(){
    if (JSON.parse(this.$route.query.url_update_add)){
        // 获取用户编号
        const acadenumber = await this.$ajax.get(`ordernum/`);
        this.acadeinfor.order_number = acadenumber.data.ordernumber
        this.acadeinfor.name = this.$route.query.username
        this.update_add = "添加数据"
        if (this.$route.query.addtype){
            this.addtype = this.$route.query.addtype
        }else{
        this.$message({
        type: "warning",
        message: "用户营销信息不存在，请添加"
        })}

    }else{
        var makeinfor_id = this.$route.query.makeinfor_id;
        var makeifor = await this.$ajax.get(`makeinfor/${makeinfor_id}/`);
        this.acadeinfor = JSON.parse(makeifor.data)
        this.teachvalue = this.acadeinfor.teaching_assistant
        this.follow_period = this.acadeinfor.follow_period
        this.update_add = "更新信息"
        this.url_update_add = false

    }
    this.AllEmployees()
    },
    async AllEmployees() {
      // 获取所有助教
      var teachin = window.sessionStorage.getItem('teachingassistant')
      if (teachin) {
        this.teaching_assistant = JSON.parse(teachin);
      } else {
        const teachingassistant = await this.$ajax.get(`teachingassistant/`);
        var obj = JSON.parse(teachingassistant.data);
        this.teaching_assistant = obj
        window.sessionStorage.setItem("teachingassistant", JSON.stringify(obj))
      } 
      },
    lookacademic() {
        this.$router.push({
        path: '/markeinform/',
        query: {
        username: this.acadeinfor.name
        }
      }
      );
    },
    async AddAcademic () {
        this.$refs.acadeinfor.validate(async (valid) => {
        if (valid) {
            this.acadeinfor.teaching_assistant = this.teachvalue
            this.acadeinfor.follow_period = this.follow_period
            if (this.url_update_add){
                const aca_res = await this.$ajax.post(`academyadd/`, this.acadeinfor);
                if (aca_res.data.status == 200) {
                    this.$message({
                    showClose: true,
                    message: aca_res.data.message,
                    type: 'success'
                })
                this.acadeinfor.id = aca_res.data.id
                this.update_add ="更新信息"
                this.url_update_add = false
                
                this.academicintotal+=1
                window.sessionStorage.removeItem("makeList")
                var index = window.sessionStorage.getItem('student_index')
                var studetnList = JSON.parse(window.sessionStorage.getItem('studetnList'))
                studetnList[index].warning_show='true'
                window.sessionStorage.setItem("studetnList", JSON.stringify(studetnList))
                } else {
                    this.$message({showClose: true,
                        type: "warning",
                        message: aca_res.data.message
                        })
                    }
            }else{
                this.acadeinfor.teaching_assistant = this.teachvalue
                const aca_res = await this.$ajax.post(`academyupdate/`, this.acadeinfor)
                if (aca_res.data.status == 200) {
                    window.sessionStorage.removeItem("makeList")
                    this.$message({
                    showClose: true,
                    message: aca_res.data.message,
                    type: 'success'
                    })
                this.update_add ="更新信息"
                this.url_update_add = false
                } else {
                    this.$message({
                        type: "warning",
                        message: aca_res.data.message
                        })
                    }
                if (aca_res.data.student_update == 200) {
                    var index = window.sessionStorage.getItem('student_index')
                    var studetnList = JSON.parse(window.sessionStorage.getItem('studetnList'))
                    studetnList[index].warning_show='true'
                    window.sessionStorage.setItem("studetnList", JSON.stringify(studetnList))
                }
                }

        } else {
            this.$message({
            type: 'warning',
            message: "请填写带*号必填项"
            });
            }
      })
    },
    async handleDownload(options) {
        if (options){
            var getgetacademic = {
                username :this.$route.query.username,
                academicinpage : this.academicinpage,
                options:options
                }
            const ademicinfor = await this.$ajax.post(`downloadacadinfor/`, getgetacademic );
            var data = {
                tableData: JSON.parse(ademicinfor.data),
                children: this.children
                }
            }
        else{
        var data = {
            tableData: [this.acadeinfor,],
            children: this.children
            }
        }
        this.comExportToExcel(data, this.mapHeader,"学术成长学院营销信息表");
    },
    informationmaster (){
        this.$router.push("/informationmaster");
    },
    customer(){
        this.$router.push("/customer");
    }
  },
}
</script>

<style scoped lang="less">

.el-button:focus,.el-button:hover {
  background: #094572;
  border-color: #271849;
  color: #fff;
}
.el-button--primary{
    margin-left: 250px;
    width: 220px;
    height: 40px;
    font-size: 18px;
    background-color: #094572;
    border: none;
    border-radius: 10px;
    color: #FFFFFF;
}
.el-button+.el-button{
    margin-left: 260px;
}
/* 灰色背景容器 */
.masterinfor{
    width: 1120px;
    min-height: 300px;
    margin-left: 40px;
    margin-top: 40px;
    margin-bottom: 40px;
    background-color: #F2F4FB;
    border-radius: 15px;
}
#amend{
    margin-left: 100px;
}
.one_label{
    margin-top: 50px;
    color: rgb(141, 138, 138);
}
/* 文本框 */
.el-form-item__label{
    width: 200px;
    height: 30px;
    color: rgb(141, 138, 138);
    margin-left: 130px;
}
.el-input__inner{
    width: 80px;
    border-radius: 10px;
     margin-left: 30px;
}

.one_a,.two_a{
    color: rgb(141, 138, 138);
    cursor: pointer;
}
.there_a{
    color: rgb(141, 138, 138);
    text-decoration: none;
    cursor: pointer;
    margin-left: 11px;
    line-height: 40px;
}
.foru_a{
    color: #fff;
    margin-left: 10px;
    line-height: 40px;
}

#special{
    margin-left: 130px;
}
.el-pagination {
    text-align: center; 
    margin-bottom: 30px;
}
/deep/.el-form-item__error{
    left: 0px;
}
.el-form-item__error{
    margin-left: 0px;
}
#acadeid{
    margin-left: 130px;
}
</style>
