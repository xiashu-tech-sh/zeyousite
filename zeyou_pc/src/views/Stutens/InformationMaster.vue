<template>
  <div class="datashow">
    <div class="datahead">
      <a class="one_a" @click="customerpath()">客户信息 ></a>
      <a class="two_a">用户信息主表 </a>
    </div>
    <el-form :inline="true" :rules="rules" :model="statusinfor" ref="statusinfor" class="styinfor">
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
      <el-form-item label="加好友日期">
        <el-date-picker v-model="date_to_add" value-format="yyyy-MM-dd" type="date" placeholder="选择日期">
        </el-date-picker>
      </el-form-item>

      <el-form-item label="姓名">
        <el-input v-model="statusinfor.name" placeholder="请输入姓名"></el-input>
      </el-form-item>
      <el-form-item label="转咨询时间">
          <el-date-picker v-model="transfer_time" type="date" value-format="yyyy-MM-dd" placeholder="选择日期">
          </el-date-picker>
      </el-form-item>
      <el-form-item label="签约时间" id="signing_time">
        <el-date-picker v-model="signing_time" type="date" value-format="yyyy-MM-dd" placeholder="选择日期">
          </el-date-picker>
      </el-form-item>
      <el-form-item label="性别">
        <el-select v-model="gender" placeholder="请选择">
          <el-option v-for="item in genders" :key="item.value" :label="item.label" :value="item.value">
          </el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="微信号" >
        <el-input v-model="statusinfor.wechat_num" placeholder="请输入微信号"></el-input>
      </el-form-item>
      <el-form-item label="地区">
        <el-input v-model="statusinfor.area" placeholder="请输入地区"></el-input>
      </el-form-item>
      <el-form-item label="手机号">
        <el-input v-model="statusinfor.phone" placeholder="请输入手机号"></el-input>
      </el-form-item>
      <el-form-item label="小助手">
        <el-select v-model="assvalue" placeholder="请选择">
          <el-option v-for="item in assistant" :key="item.id" :label="item.name" :value="item.name">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="顾问">
        <el-select v-model="convalue" placeholder="请选择">
          <el-option v-for="item in consultant" :key="item.id" :label="item.name" :value="item.name">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="服务顾问">
        <el-select v-model="servalue" placeholder="请选择">
          <el-option v-for="item in service_advisor" :key="item.id" :label="item.name" :value="item.name">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="文案">
        <el-select v-model="copvalue" placeholder="请选择">
          <el-option v-for="item in copywriting" :key="item.id" :label="item.name" :value="item.name">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="战略顾问">
        <el-select v-model="strategy_consultant" placeholder="请选择">
          <el-option v-for="item in strategy_consultants" :key="item.id" :label="item.name" :value="item.name">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="客户身份">
        <el-select v-model="identity" placeholder="请选择">
          <el-option v-for="item in identitys" :key="item.value" :label="item.label" :value="item.value">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="学校类型">
          <el-select v-model="school_type" placeholder="请选择学校类型">
            <el-option v-for="item in school_types" :key="item.value" :label="item.label" :value="item.value">
            </el-option>
          </el-select>
      </el-form-item>
      <el-form-item label="学校名">
        <el-input v-model="statusinfor.school" placeholder="请输入学校名"></el-input>
      </el-form-item>
      <el-form-item label="课程体系">
        <el-select v-model="curriculum_system" placeholder="请选择课程体系">
          <el-option v-for="item in curriculum_systems" :key="item.value" :label="item.label" :value="item.value">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="体系专业">
        <el-input v-model="statusinfor.curriculum_system_note" placeholder="请输入体系专业"></el-input>
      </el-form-item>
      <el-form-item label="申请层级">
        <el-select v-model="application_level" placeholder="请选择申请层级">
          <el-option v-for="item in application_levels" :key="item.value" :label="item.label" :value="item.value">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="申请层级入学时间">
        <el-input v-model="statusinfor.graduation_date" placeholder="请输入申请层级入学时间"></el-input>
      </el-form-item>
      <el-form-item label="专业方向">
        <el-input v-model="statusinfor.major" placeholder="请输入专业方向"></el-input>
      </el-form-item>
      <el-form-item label="目标国家">
        <el-select v-model="target_country" placeholder="请选择目标国家">
          <el-option v-for="item in target_countrys" :key="item.value" :label="item.label" :value="item.value">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="托福">
        <el-input v-model="statusinfor.TOEFL" placeholder="请输入托福"></el-input>
      </el-form-item>
      <el-form-item label="雅思">
        <el-input v-model="statusinfor.IELTS" placeholder="请输入雅思"></el-input>
      </el-form-item>
      <el-form-item label="SAT">
        <el-input v-model="statusinfor.SAT" placeholder="请输入SAT"></el-input>
      </el-form-item>
      <el-form-item label="ACT">
        <el-input v-model="statusinfor.ACT" placeholder="请输入ACT"></el-input>
      </el-form-item>
      <el-form-item label="GRE/GMAT">
        <el-input v-model="statusinfor.GRE" placeholder="请输入GRE/GMAT"></el-input>
      </el-form-item>
      <el-form-item label="客户信息备注">
        <el-input v-model="statusinfor.customer_remarks" placeholder="请输入客户信息备注"></el-input>
      </el-form-item>
      <br>
      <el-form-item>
        <el-button type="primary" @click="updatastudent()">更新信息</el-button>
        <el-button type="primary" @click="lookacademic()">营销信息</el-button>
        <el-button type="primary" @click="handleDownload()">推荐产品</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script > 
export default {
  data() {
    return {
      mapHeader: [
        "客户状态",
        "资源来源",
        "加好友日期",
        "姓名",
        "签约时间",
        "性别",
        "微信号",
        "地区",
        "手机号",
        "所属小助手",
        "所属顾问",
        "所属服务顾问",
        "所属文案",
        "客户身份",
        "学校类型",
        "学校名",
        "课程体系",
        "体系专业",
        "申请层级入学时间",
        "申请层级",
        "专业方向",
        "目标国家",
        "托福",
        "雅思",
        "SAT",
        "ACT",
        "GRE/GMAT",
        "客户信息备注"
      ],
      children: [
        "customer_state",
        "source",
        "date_to_add",
        "name",
        "signing_time",
        "gender",
        "wechat_num",
        "area",
        "phone",
        "little_assistant",
        "consultant",
        "service_consultant",
        "paper_writer",
        "identity",
        "school_type",
        "school",
        "curriculum_system",
        "curriculum_system_note",
        "graduation_date",
        "application_level",
        "major",
        "target_country",
        "TOEFL",
        "IELTS",
        "SAT",
        "ACT",
        "GRE"
      ],
      // statusinfor : this.$route.query.information,
      school_types:[{
        value: '体制内',
        label: '体制内'
      }, {
        value: '公立国际部',
        label: '公立国际部'
      }, {
        value: '民办双语',
        label: '民办双语'
      }, {
        value: '国际学校',
        label: '国际学校'
      }, {
        value: '陆本',
        label: '陆本'
      }, {
        value: '海本',
        label: '海本'
      }, {
        value: '海高',
        label: '海高'
      }],
      school_type:'',
      target_countrys:[{
        value: '美国',
        label: '美国'
      }, {
        value: '英国',
        label: '英国'
      }, {
        value: '加拿大',
        label: '加拿大'
      }, {
        value: '法国',
        label: '法国'
      }, {
        value: '美欧混申',
        label: '美欧混申'
      }, {
        value: '美亚混申',
        label: '美亚混申'
      }, {
        value: '其他',
        label: '其他'
      }],
      target_country:'',
      application_levels:[{
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
      application_level:'',
      curriculum_systems:[{
        value: 'IB',
        label: 'IB'
      }, {
        value: 'AP',
        label: 'AP'
      }, {
        value: 'IG',
        label: 'IG'
      }, {
        value: 'MYP',
        label: 'MYP'
      }, {
        value: 'A-Level',
        label: 'A-Level'
      },{
        value: '陆本',
        label: '陆本'
      }, {
        value: '海本',
        label: '海本'
      },{
        value: '体制内',
        label: '体制内'
      }, {
        value: '其他',
        label: '其他'
      }],
      curriculum_system:'',
      transfer_time:'',
      signing_time:"",
      statusinfor: {
        name: '',
        wechat_num: '',
        area: '',
        phone: '',
        school: '',
        curriculum_system_note: '',
        major: '',
        signing_time: '',
        TOEFL: '',
        IELTS: '',
        SAT: '',
        ACT: '',
        GRE: '',
        application_level:'',
        target_country:'',
        curriculum_system:'',
        school_type:'',
        customer_remarks:''
      },
      customer: [{
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
      }],
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
      genders: [{
        value: '男',
        label: '男'
      }, {
        value: '女',
        label: '女'
      }],
      gender: '',
      identitys: [{
        value: '家长',
        label: '家长'
      }, {
        value: '学生',
        label: '学生'
      }],
      identity: '',
      assistant: [],
      assvalue: '',
      consultant: [],
      convalue: '',
      service_advisor: [],
      servalue: '',
      strategy_consultants:[],
      strategy_consultant:'',
      copywriting: [],
      copvalue: '',
      pickerOptions: {
        disabledDate(time) {
          return time.getTime() > Date.now();
        },
      },
      date_to_add: '',
      graduation_date: '',
    }
  },
  created() {
    window.sessionStorage.removeItem("makeList")
    var infor = window.sessionStorage.getItem('information')
    if (infor) {
      this.statusinfor = JSON.parse(infor);
      this.assistant = JSON.parse(window.sessionStorage.getItem('assistant'))
      this.consultant = JSON.parse(window.sessionStorage.getItem('consultant'))
      this.copywriting = JSON.parse(window.sessionStorage.getItem('copywriting'))
      this.strategy_consultants = JSON.parse(window.sessionStorage.getItem('strategy_consultants'))
      this.service_advisor = JSON.parse(window.sessionStorage.getItem('service_advisor'))
          // 客户状态
          this.customer_state = this.statusinfor.customer_state
          // 来源
          this.source = this.statusinfor.source 
          // 性别
          this.gender = this.statusinfor.gender 
          // 转咨询时间
          this.transfer_time = this.statusinfor.transfer_time
          // 签约时间
          this.signing_time = this.statusinfor.signing_time
          //所属小助手
          this.assvalue = this.statusinfor.little_assistant 
          //所属顾问
          this.convalue = this.statusinfor.consultant 
          //所属服务顾问
          this.servalue = this.statusinfor.service_consultant 
          //所属文案
          this.copvalue = this.statusinfor.paper_writer 
          // 所属战略顾问
          this.strategy_consultant = this.statusinfor.strategy_consultant
          // 客户身份
          this.identity = this.statusinfor.identity 
          // 学校类型
          this.school_type = this.statusinfor.school_type 
          // 课程体系
          this.curriculum_system = this.statusinfor.curriculum_system 
          // 目标国家
          this.target_country = this.statusinfor.target_country 
          // 申请层级
          this.application_level = this.statusinfor.application_level 
          // 加好友日期
          this.date_to_add = this.statusinfor.date_to_add 
    } else {
      this.assistant = JSON.parse(window.sessionStorage.getItem('assistant'))
      this.consultant = JSON.parse(window.sessionStorage.getItem('consultant'))
      this.service_advisor = JSON.parse(window.sessionStorage.getItem('service_advisor'))
      this.copywriting = JSON.parse(window.sessionStorage.getItem('copywriting'))
      this.strategy_consultants = JSON.parse(window.sessionStorage.getItem('strategy_consultants'))
    }},

  methods: {
    async updatastudent() {
          // 客户状态
          this.statusinfor.customer_state = this.customer_state
          // 来源
          this.statusinfor.source = this.source
          // 性别
          this.statusinfor.gender = this.gender
          // 转咨询时间
          this.statusinfor.transfer_time = this.transfer_time
          // 签约时间
          this.statusinfor.signing_time = this.signing_time
          //所属小助手
          this.statusinfor.little_assistant = this.assvalue
          //所属顾问
          this.statusinfor.consultant = this.convalue
          //所属服务顾问
          this.statusinfor.service_consultant = this.servalue
          //所属文案
          this.statusinfor.paper_writer = this.copvalue
          //战略顾问
          this.statusinfor.strategy_consultant = this.strategy_consultant
          // 客户身份
          this.statusinfor.identity = this.identity
          // 学校类型
          this.statusinfor.school_type = this.school_type
          // 课程体系
          this.statusinfor.curriculum_system = this.curriculum_system
          // 目标国家
          this.statusinfor.target_country = this.target_country
          // 申请层级
          this.statusinfor.application_level = this.application_level
          // 加好友日期
          this.statusinfor.date_to_add = this.date_to_add
          const studetnres = await this.$ajax.post(`studentupdate/`, this.statusinfor);
          if (studetnres.data.status == 201) {
            window.sessionStorage.setItem("information", JSON.stringify(this.statusinfor))
            this.$message({
              type: "success",
              message: studetnres.data.message
            })
          } else {
            this.$message({
              type: 'warning',
              message: studetnres.data.message
            })}
    },
    async handleDownload() {
      var data = {
        graduation_date:this.statusinfor.graduation_date,
        application_level:this.statusinfor.application_level,
        major:this.statusinfor.major,
        school_type:this.statusinfor.school_type,
        curriculum_system:this.statusinfor.curriculum_system,
      }
      const res = await this.$ajax.post(`/studentanalysis/`, data);
          let obj = JSON.parse(res.data)
          if (obj.status == 200){
            if (obj.data.length ==1){
              this.$alert('一对一独立研究', '推荐产品',{
              dangerouslyUseHTMLString:true,
              confirmButtonText: '确定',})
            }if (obj.data.length ==2){
              this.$alert(obj.data[0]+'</br>'+'</br>'+obj.data[1], '推荐产品',{
              dangerouslyUseHTMLString:true,
              confirmButtonText: '确定',})
            }if (obj.data.length ==3){
              this.$alert(obj.data[0]+'</br>'+'</br>'+obj.data[1]+'</br>'+'</br>'+obj.data[2]+'</br>'+'</br>'+obj.data[3]+'</br>'+'</br>', '推荐产品',{
              dangerouslyUseHTMLString:true,
              confirmButtonText: '确定',})
            }if (obj.data.length >3){
              this.$alert(obj.data[0]+'</br>'+'</br>'+obj.data[1]+'</br>'+'</br>'+obj.data[2]+'</br>'+'</br>'+obj.data[3]+'</br>'+'</br>'+'一对一独立研究', '推荐产品',{
              dangerouslyUseHTMLString:true,
              confirmButtonText: '确定',})
              }
          }else{
            this.$message({
            type: 'warning',
            message: obj.message
          })}

    },
    lookacademic() {
      this.$router.push({
        path: '/markeinform/',
        query: {
          username: this.statusinfor.name
        }
      }
      );
    },
    customerpath() {
      this.$router.push("/customer")
    }
  }
}
</script>

<style scoped>
#signing_time{
  margin-left: 30px;
}
.el-button:focus,
.el-button:hover {
  background: #094572;
  border-color: #271849;
  color: #fff;
}
.el-message-box__title{
  color: #094572;
}
.el-button--primary {
  margin-left: 51px;
  width: 268px;
  height: 40px;
  font-size: 18px;
  background-color: #094572;
  border: none;
  border-radius: 10px;
  color: #ffffff;
}
.el-button + .el-button {
  margin-left: 139px;
}
/* 灰色背景容器 */
.styinfor {
  margin-top: 40px;
  margin-bottom: 40px;
}
.one_label {
  margin-top: 50px;
  color: rgb(141, 138, 138);
}
/* 文本框 */
.el-form-item__label {
  width: 135px;
  height: 30px;
  color: rgb(141, 138, 138);
}
.el-input__inner {
  width: 220px;
  border-radius: 10px;
  margin-left: 30px;
}
.one_a {
  color: rgb(141, 138, 138);
  cursor: pointer;
}
.two_a {
  color: #fff;
  text-decoration: none;
  margin-left: 11px;
  line-height: 40px;
}
/* 设置显示栏容器 */
.datashow {
  width: 1200px;
  margin: 0 auto;
  border: solid #094572 1px;
  border-radius: 10px;
}
.el-input__icon {
  margin-left: 30px;
}
/* 头标签 */
.datahead {
  height: 40px;
  background-color: #094572;
  border-radius: 10px;
  border: none;
}
/* 部分标签位置调整 */
.el-select__tags {
  margin-left: 30px;
}
.el-form-item__error {
  margin-left: 30px;
}
</style>
