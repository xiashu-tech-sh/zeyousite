<template>
  <div class="recomshow">
    <div class="analysishead">
      <a class="recommended" @click="customerpath()">推荐系统 ></a>
      <a class="analysis">数据分析</a>
    </div>
    <div class="datatext">
      <span class="line"></span>
      <span class="text">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;筛选条件&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
      <span class="line"></span>
    </div>
    <el-form style="width:100%" :inline="true" :rules="rules" :model="screeninginfor" ref="screeninginfor" class="screeninginfor">
        <el-form-item label="资源录入时间跨度">
        <el-input v-model="screeninginfor.time_span" placeholder="请输入资源录入时间跨度"></el-input>
      </el-form-item>
        <el-form-item label="客户状态">
          <el-select v-model="customer_state" placeholder="请选择">
            <el-option v-for="item in customer_states" :key="item.value" :label="item.label" :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="资源来源">
          <el-select v-model="source" placeholder="请选择">
            <el-option v-for="item in sources" :key="item.value" :label="item.label" :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="性别">
        <el-select v-model="gender" placeholder="请选择">
          <el-option v-for="item in genders" :key="item.value" :label="item.label" :value="item.value">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="签约时间">
        <el-input v-model="screeninginfor.signing_time" placeholder="请输入签约时间"></el-input>
      </el-form-item>
      <el-form-item label="地区">
        <el-input v-model="screeninginfor.area" placeholder="请输入地区"></el-input>
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
      <el-form-item label="文案">
        <el-select v-model="copvalue" placeholder="请选择">
          <el-option v-for="item in copywriting" :key="item.id" :label="item.name" :value="item.name">
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
        <el-input v-model="screeninginfor.school" placeholder="请输入学校名"></el-input>
      </el-form-item>
      <el-form-item label="课程体系">
        <el-select v-model="curriculum_system" placeholder="请选择课程体系">
          <el-option v-for="item in curriculum_systems" :key="item.value" :label="item.label" :value="item.value">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="申请层级">
        <el-select v-model="application_level" placeholder="请选择申请层级">
          <el-option v-for="item in application_levels" :key="item.value" :label="item.label" :value="item.value">
          </el-option>
        </el-select>
      </el-form-item>
    </el-form>
    <div class="datatext">
      <span class="line"></span>
      <span class="text">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;查询内容&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
      <span class="line"></span>
    </div>
    <div class="conditionshead">
      <div class="contentdiv_one" id="contentdiv_one" @click="common_age('contentdiv_one')" >
        <span >客户状态</span>
      </div>
      <div class="contentdiv">
        <span @click="common_age()">资源来源</span>
      </div>
      <div class="contentdiv">
        <span @click="common_age()">性别</span >
      </div>
      <div class="contentdiv">
        <span @click="common_age()">申请层级</span>
      </div>
      <div class="contentdiv">
        <span @click="common_age()">申请层级入学时间</span>
      </div>
    </div>
    <div class="conditionshead">
      <div class="contentdiv">
        <span @click="common_age()">地区</span>
      </div>
      <div class="contentdiv">
        <span @click="common_age()">所属小助手</span>
      </div>
      <div class="contentdiv">
        <span @click="common_age()">所属顾问</span>
      </div>
      <div class="contentdiv">
        <span @click="common_age()">所属文案</span>
      </div>
      <div class="contentdiv">
        <span @click="common_age()">学校类型</span>
      </div>
    </div>
    <div class="conditionshead">
      <div class="contentdiv">
        <span @click="common_age()">学校名</span>
      </div>
      <div class="contentdiv">
        <span @click="common_age()">课程体系</span>
      </div>
      <div class="contentdiv">
        <span @click="common_age()">专业方向</span>
      </div>
      <div class="contentdiv">
        <span @click="common_age()">目标国家</span>
      </div>
    </div>
    <div class="datatext">
      <span class="line"></span>
      <span class="text">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;统计结果&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
      <span class="line"></span>
    </div>
  <!-- <div class="imagevolume"> -->
      <div id="imageshow" ></div>
  <!-- </div> -->
  </div>
</template>
<script>
import echarts from 'echarts'
export default {
  data() {
      return{
      high_quantity:[],
      imageshow: '',
      opinion: [], //x 轴显示内容
      opinionData: [], // 显示数据
      copywriting:[], //文案
      consultant:[], //顾问
      assistant:[], //小助手
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
      genders: [{
        value: '男',
        label: '男'
      }, {
        value: '女',
        label: '女'
      }],
      gender: '',
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
      customer_states: [{
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
      screeninginfor:{
          gender:"",
          source:"",
          customer_state:"",
          signing_time:"",
          area:"",
          convalue:"",
          assvalue:"",
          copvalue:"",
          school_type:"",
          school:"",
          curriculum_system:"",
          application_level:"",
          time_span:""
      },

    }
  },
  created() {
    var pro_data = window.sessionStorage.getItem("analysisinfor")
    var tab_data = window.sessionStorage.getItem("tabledata")
    if (pro_data ){
      this.analysisinfor = JSON.parse(pro_data)
      this.tableData = JSON.parse(tab_data)
    }
   
  },

  methods:{
    async common_age(heght){
      if (this.high_quantity.indexOf(heght)==-1){
        var oDiv = document.getElementById(heght)
        oDiv.style.backgroundColor = "#094572"
        oDiv.style.color = "#fff"
        this.high_quantity.push(heght)
      }
      else{
        var oDiv = document.getElementById(heght)
        oDiv.style.backgroundColor = "#fff"
        oDiv.style.color = "#094572"
        this.high_quantity.splice(this.high_quantity.indexOf(heght),1)
      }

      this.screeninginfor.customer_state = this.customer_state
      const res = await this.$ajax.post(`/commonage/`, this.screeninginfor);
      let obj = JSON.parse(res.data)
      if (obj.status==200){
        this.opinion =  obj.x_data
        this.opinionData = obj.value_list
      }else{
          this.$message({
            type: "warning",
            message: obj.message
            },)
          this.opinion =  []
          this.opinionData = []
          return
          }
      this.imageshow = echarts.init(document.getElementById('imageshow'))
      this.imageshow.setOption({
        title: {
          text: '人数'
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c}'
        },
        // legend: {
        //   orient: 'vertical',
        //   x: 'right',
        //   y: 'top',
        //   data: ['评估概率']
        // },
        xAxis: {
          data: this.opinion
        },
        yAxis: {},
        series: [{
          name: '人数',
          type: 'bar',
          data: this.opinionData,
          itemStyle: {
            emphasis: {
              shadowBlur: 2,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            },
            color: function (params) {
              // 自定义颜色
              var colorList = ['#1ab394', "#094572"]
              return colorList[params.dataIndex]
            }
          }
        }]
      })
    }
  }
}
</script>

<style scoped lang="less">

.contentdiv:hover{
  background-color: #094572;
  color: #fff;
}
.contentdiv_one:hover{
  background-color: #094572;
  color: #fff;
}
.conditionsspan{
  width: 200px;
  height: 100px;
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

}
.el-button{
  margin-left: 70px;
  border-radius: 20px;
}
.conditionshead{
  padding: 0px 0px;
  margin-top: 30px;
}
.imagevolume{
  margin-top: 60px;
  width:1000px;
  margin-left: 400px;
  margin-bottom: 120px;
}
#imageshow{
  width:600px;
  height:250px;
  // float:left
  
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
}
.analysishead{
  // margin-bottom: 100px;
  height: 40px;
  background-color: #094572;
  border-radius: 10px;
  border: none;
}
.recommended{
    color: rgb(141, 138, 138);
    text-decoration: none;
    margin-left: 11px;
    line-height: 40px;
}
.analysis {
    color: #fff;
    cursor: pointer;
    text-decoration: none;
    margin-left: 11px;
    line-height: 40px;
}
/* 设置显示栏容器 */
.recomshow {
  width: 1200px;
  min-height: 600px;
  margin: 0 auto;
  border: solid #094572 1px;
  border-radius: 10px;
}
.el-button:focus,.el-button:hover {
  background: #094572;
  border-color: #271849;
  color: #fff;
}
.el-button--primary{
    margin-left: 310px;
    width: 220px;
    height: 40px;
    font-size: 18px;
    background-color: #094572;
    border: none;
    border-radius: 10px;
    color: #FFFFFF;
    margin-bottom: 50px;
    margin-top: 30px;
}
.el-table--border{
  margin-left: 4%;
}
.quantity{
  color: rgb(194, 187, 187)
}
</style>