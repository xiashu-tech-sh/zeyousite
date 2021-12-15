<template>

  <div     v-loading="loading"
    element-loading-text="拼命上传中"
    element-loading-spinner="el-icon-loading"
    element-loading-background='#094572'>
    <div class="datashow">
      <div class="files">
        <div id="files">
          <div class="fileinput-button">
            <input type="file" id="File" @change="handleFileChange()" ref="inputer" accept=".csv,.xls,.xlsx">
            <span class="filestyle">一键导入exls信息</span>
            <img src="../../assets/addexls.png" alt="">
          </div>
        </div>
        <div id="popover_div">
          <el-popover
            width="300"
            height='500'
            trigger="click"
            id="popover_id"
            v-show="popovershow"
            >
            <el-table
    :data="updateData"
    max-height="250"
    border
    style="width: 100%">
    <el-table-column
      prop="name"
      label="姓名"
      width="150">
    </el-table-column>
    <el-table-column
      prop="wechat_num"
      label="微信号"
      width="150">
    </el-table-column>
        <el-table-column
      prop="little_assistant"
      label="所属小助手"
      width="150">
    </el-table-column>
  </el-table>
            <el-button slot="reference">查看覆盖数据</el-button>
        </el-popover>
        </div>
      </div>
      <div class="tabletext">
        <span id="tatext">人工录入</span>
      </div>
      <el-form :inline="true" :rules="rules" :model="inforObj" ref="inforObj" class="styinfor">
        <!-- <el-form-item label="客户编号">
          <el-input placeholder="" v-model="inforObj.customer_number" :disabled="true"></el-input>
        </el-form-item> -->
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
          <el-date-picker v-model="date_to_add" type="date" value-format="yyyy-MM-dd" placeholder="选择日期">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input v-model="inforObj.name" placeholder="请输入姓名"></el-input>
        </el-form-item>
        <el-form-item label="转咨询时间">
          <el-date-picker v-model="transfer_time" type="date" value-format="yyyy-MM-dd" placeholder="选择日期">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="签约时间" id="signing_time_id">
          <el-date-picker v-model="signing_time" type="date" value-format="yyyy-MM-dd" placeholder="选择日期">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="性别">
          <el-select v-model="gender" placeholder="请选择">
            <el-option v-for="item in genders" :key="item.value" :label="item.label" :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="微信号">
          <el-input v-model="inforObj.wechat_num" placeholder="请输入微信号"></el-input>
        </el-form-item>
        <el-form-item label="地区">
          <el-input v-model="inforObj.area" placeholder="请输入地区"></el-input>
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="inforObj.phone" placeholder="请输入手机号"></el-input>
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
          <el-input v-model="inforObj.school" placeholder="请输入学校名"></el-input>
        </el-form-item>
        <el-form-item label="课程体系">
          <el-select v-model="curriculum_system" placeholder="请选择课程体系">
            <el-option v-for="item in curriculum_systems" :key="item.value" :label="item.label" :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="体系专业">
          <el-input v-model="inforObj.curriculum_system_note" placeholder="请输入体系专业"></el-input>
        </el-form-item>
        <el-form-item label="申请层级">
          <el-select v-model="application_level" placeholder="请选择申请层级">
            <el-option v-for="item in application_levels" :key="item.value" :label="item.label" :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="申请层级入学时间">
          <el-input v-model="inforObj.graduation_date" placeholder="请输入申请层级入学时间"></el-input>
        </el-form-item>
        <el-form-item label="专业方向">
          <el-input v-model="inforObj.major" placeholder="请输入专业方向"></el-input>
        </el-form-item>
        <el-form-item label="目标国家">
          <el-select v-model="target_country" placeholder="请选择目标国家">
            <el-option v-for="item in target_countrys" :key="item.value" :label="item.label" :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="托福">
          <el-input v-model="inforObj.TOEFL" placeholder="请输入托福"></el-input>
        </el-form-item>
        <el-form-item label="雅思">
          <el-input v-model="inforObj.IELTS" placeholder="请输入雅思"></el-input>
        </el-form-item>
        <el-form-item label="SAT">
          <el-input v-model="inforObj.SAT" placeholder="请输入SAT"></el-input>
        </el-form-item>
        <el-form-item label="ACT">
          <el-input v-model="inforObj.ACT" placeholder="请输入ACT"></el-input>
        </el-form-item>
        <el-form-item label="GRE/GMAT">
          <el-input v-model="inforObj.GRE" placeholder="请输入GRE/GMAT"></el-input>
        </el-form-item>
        <el-form-item label="客户信息备注">
          <el-input v-model="inforObj.customer_remarks"  placeholder="请输入客户信息备注"></el-input>
        </el-form-item>
        <br>
        <div class="layui-form-item">
          <button class="submit_btn" type='button' @click="lookacademic()">提交</button>
          <button type="reset" class="reset_btn">重置</button>
        </div>
      </el-form>
    </div>
  </div>
</template>
<script > 
export default {
  data() {
    return {
      popovershow:false,//更新数据按钮显示，不显示
      updateData:[],//更新数据
      rules: {
        name: [{
          required: true,
          message: "姓名不能为空",
          trigger: "blur"
        }]
      },
      loading: false,
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
      application_levels:[{
        value: '国内国际学校',
        label: '国内国际学校'
      }, {
        value: '美国高中',
        label: '美国高中'
      },{
        value: '海本转学',
        label: '海本转学'
      }, {
        value: '海研',
        label: '海研'
      }, {
        value: '海博',
        label: '海博'
      }, {
        value: '海本',
        label: '海本'
      }],
      application_level:'',
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
      identitys: [{
        value: '家长',
        label: '家长'
      }, {
        value: '学生',
        label: '学生'
      }],
      identity: '',
      // 小助手
      assistant: [],
      assvalue: '',
      // 顾问
      consultant: [],
      convalue: '',
      // 服务顾问
      service_advisor: [],
      servalue: '',
      // 文案
      copywriting: [],
      copvalue: '',
      strategy_consultants:[],
      strategy_consultant:'',
      date_to_add: '',
      transfer_time:'',
      signing_time:"",
      inforObj: {
        graduation_date:'',
        signing_time:'',
        name: '',
        curriculum_system:'',
        school_type:'',
        wechat_num: '',
        area: '',
        phone: '',
        school: '',
        curriculum_system_note: '',
        major: '',
        TOEFL: '',
        IELTS: '',
        SAT: '',
        ACT: '',
        GRE: '',
        application_level: '',
        customer_remarks:''

      },
    }
  },
  created() {
    var popovershow = window.sessionStorage.getItem('popovershow')
    var updateData = window.sessionStorage.getItem('updateData')
    if (popovershow=='true'){
      this.popovershow = true
      this.updateData = JSON.parse(updateData)
    }
    this.AllEmployees();
  },
  methods: {
    // 获取所有员工
    async AllEmployees() {
      // 获取所有小助手
      const getassisall = await this.$ajax.get(`getassistant/`);
      var obj = JSON.parse(getassisall.data);
      this.assistant = obj
      window.sessionStorage.setItem('assistant', JSON.stringify(obj));
      // 获取所有顾问
      const consultantall = await this.$ajax.get(`consultant/`);
      var obj = JSON.parse(consultantall.data);
      this.consultant = obj
      window.sessionStorage.setItem('consultant', JSON.stringify(obj));
      // 获取所有服务顾问
      const serviceadvisorall = await this.$ajax.get(`serviceadvisor/`);
      var obj = JSON.parse(serviceadvisorall.data);
      this.service_advisor = obj
      window.sessionStorage.setItem('service_advisor', JSON.stringify(obj));
      // 获取所有文案
      const copywritingall = await this.$ajax.get(`copywriting/`);
      var obj = JSON.parse(copywritingall.data);
      this.copywriting = obj
      window.sessionStorage.setItem('copywriting', JSON.stringify(obj));
      // 获取所有战略顾问
      const strategyall = await this.$ajax.get(`strategy/`);
      var obj = JSON.parse(strategyall.data);
      this.strategy_consultants = obj
      window.sessionStorage.setItem('strategy_consultants', JSON.stringify(obj));
      // 获取用户编号
      // const studentcount = await this.$ajax.get(`studentcount/`);
      // this.inforObj.customer_number = studentcount.data.count_name
    },
    async lookacademic() {
      
      this.$refs.inforObj.validate(async (valid) => {
        if (valid) {
            this.inforObj.date_to_add = this.date_to_add
            this.inforObj.transfer_time = this.transfer_time
            this.inforObj.signing_time = this.signing_time
            this.inforObj.source = this.source
            this.inforObj.customer_state = this.customer_state
            this.inforObj.gender = this.gender
            this.inforObj.school_type = this.school_type
            this.inforObj.application_level = this.application_level
            this.inforObj.curriculum_system = this.curriculum_system
            this.inforObj.target_country = this.target_country
            //所属小助手
            this.inforObj.little_assistant = this.assvalue
            //所属顾问
            this.inforObj.consultant = this.convalue
            //所属服务顾问
            this.inforObj.service_consultant = this.servalue
            //所属文案
            this.inforObj.paper_writer = this.copvalue
            this.inforObj.strategy_consultants = this.strategy_consultant
            this.inforObj.identity = this.identity
            const res = await this.$ajax.post(`/studentadd/`, this.inforObj);
            if (res.data.status == 200) {
              // 更新用户编号
              // const studentcount = await this.$ajax.get(`studentcount/`);
              // this.inforObj.customer_number = studentcount.data.count_name
              this.$message({
                type: "success",
                message: res.data.message
              })
            } else {
              this.$message({
                type: "warning",
                message: res.data.message
              })}
          } else {
          this.$message({
            type: 'warning',
            message: "请填写带*号必填项"
          });
        }
      })
    },
    async handleFileChange() {
      let inputDOM = this.$refs.inputer;
      this.file = inputDOM.files[0];// 通过DOM取文件数据
      this.formData = new FormData();//new一个formData事件
      this.formData.append("file", this.file); //将file属性添加到formData里
      let config = {
        headers: {
          'Content-Type': 'multipart/form-data',
        }
      };
      this.loading= true
      const res = await this.$ajax.post('/upload/', this.formData)
      let obj = JSON.parse(res.data);
      this.loading=false
        if (obj[0].status == 200){
          if(obj[0].updeta_data.length>0) {
            this.popovershow = true
          }else{
            this.popovershow = false
          }
          this.popovershow = true
          this.updateData = obj[0].updeta_data
          window.sessionStorage.setItem("popovershow", JSON.stringify(this.popovershow))
          window.sessionStorage.setItem("updateData", JSON.stringify(obj[0].updeta_data))
        this.$message({
          type: 'success',
          message: obj[0].message
        })}else{
          window.sessionStorage.setItem("popovershow", JSON.stringify(false))
          window.sessionStorage.setItem("updateData", JSON.stringify(obj[0].updeta_data))
          this.$message({
          type: 'warning',
          message: obj[0].message})
        }
        setTimeout(() => {
          if (obj[1].status == 200) {
            this.$message({
              type: "success",
              message: obj[1].message
            })
          } else {
            this.$message({
              type: 'warning',
              message: obj[1].message
            })
          };
        }, 0.1);
        this.$router.push({
        path: '/adddata/',
      }
      );
    },
  },
}
</script>

<style scoped lang="less">
#signing_time_id{
  margin-left: 30px;
}
.submit_btn {
  width: 200px;
  height: 50px;
  margin-left: 300px;
  background-color: #094572;
  color: #fff;
  font-size: 20px;
  border-radius: 10px;
  margin-top: 50px;
  outline: none;
}
.reset_btn {
  width: 200px;
  height: 50px;
  background-color: #094572;
  color: #fff;
  font-size: 20px;
  border-radius: 10px;
  outline: none;
  display: inline-block;
  margin: auto 12px auto 120px;
}
.prompt1 {
  margin-left: 80px;
}
.prompt2 {
  margin-left: 80px;
}
.each_line input {
  width: 250px;
  height: 30px;
  color: #094572;
  margin-left: 10px;
  text-align: center;
  text-align-last: center;
  border-radius: 10px;
  background-color: #f2f4fb;
  outline: none;
}
select {
  width: 250px;
  height: 30px;
  color: #094572;
  margin-left: 10px;
  text-align: center;
  text-align-last: center;
  border-radius: 10px;
  background-color: #f2f4fb;
}
.each_line {
  height: 30px;
  font-size: 14px;
  margin-left: 33px;
  color: #094572;
  margin-top: 30px;
}
#tatext {
  margin-left: 550px;
}
/* 人工录入文字样式 */
.tabletext {
  margin-top: 30px;
  height: 30px;
  font-weight: bold;
  font-size: 20px;
  color: #094572;
}
#popover_div{
  display: inline-block;
  margin-left: 1005px;
}
/* 导入exle样式 */
.fileinput-button {
  height: 30px;
  background-color: #e3e6e9;
  color: #094572;
  font-size: 20px;
  position: relative;
  display: inline-block;
  margin: 0 auto;
  margin-top: 15px;
  overflow: hidden;
  margin-left: 30px;
  border-radius: 10px;
}
/* 导入exle选择框隐藏样式 */
.fileinput-button input {
  position: absolute;
  right: 0px;
  top: 0px;
  opacity: 0;
  -ms-filter: "alpha(opacity=0)";
  cursor: pointer;
}
/* 导入exle文字样式 */
.filesimport {
  line-height: 48px;
  margin-left: 30px;
}
/* 导入exle下划线样式 */
.files {
  width: 1130px;
  height: 90px;
  margin-left: 20px;
  margin: 0 auto;
  border-bottom: 1px solid #b9bbbd;
}
#files {
  height: 50px;
  width: 240px;
  margin: 0 auto;
  border-radius: 20px;
  margin-top: 20px;
  font-size: 18px;
  background-color: #e3e6e9;
}
.filesimge {
  margin-left: 10px;
}
/* 设置显示栏容器 */
.datashow {
  width: 1200px;
  margin: 0 auto;
  border: solid #094572 1px;
  border-radius: 10px;
}
.el-select-dropdown__item.selected {
  color: #094572;
}
/deep/.el-form-item__error {
  margin-left: 30px;
}
</style>
