<template>
  <div class="recomshow">
    <div class="datahead">
      <a class="recommended" >推荐系统 ></a>
      <a class="analysis " @click="analysispath()">数据分析</a>
    </div>
    <el-form style="width:100%" :inline="true" :rules="rules" :model="stupushinfor" ref="stupushinfor" class="masterinfor">
        <el-form-item>
            <el-button type="primary" class="quantity" @click="productpush()">产品信息推荐学生</el-button>
            <el-button type="primary" @click="studentpush()">学生信息推荐产品</el-button>
        </el-form-item>
        <el-form-item label="学生课程体系" prop="curriculum_system">
            <el-select v-model="curriculum_system" placeholder="请选择课程体系">
            <el-option v-for="item in curriculum_systems" :key="item.value" :label="item.label" :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <!-- <el-form-item label="学校类型" prop="school_type" >
          <el-select v-model="school_type" placeholder="请选择学校类型">
            <el-option v-for="item in school_types" :key="item.value" :label="item.label" :value="item.value">
            </el-option>
          </el-select>
        </el-form-item> -->
        <el-form-item label="专业方向" prop="major">
            <el-input v-model="stupushinfor.major"  placeholder="请输入专业方向"></el-input>
        </el-form-item>
        <el-form-item label="申请层级" prop="application_level">
          <el-select v-model="application_level" placeholder="请选择申请层级">
            <el-option v-for="item in application_levels" :key="item.value" :label="item.label" :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="申请层级入学时间" prop="graduation_date">
            <el-input v-model="stupushinfor.graduation_date"  placeholder="请输入申请层级入学时间"></el-input>
        </el-form-item>
        <div class="ai_recom"  @click="StudentAnalysis()" >
        <spen class="ai_spen" >智能分析</spen>
        </div>
    </el-form>
    <div v-for="item in productList" :key="item" class="sturespush">
      <span class="sturesprodut"> {{item}}</span>
    </div>

  </div>
</template>
<script>
export default {
  data() {
      return{
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
      //   school_types:[{
      //   value: '体制内',
      //   label: '体制内'
      // }, {
      //   value: '公立国际部',
      //   label: '公立国际部'
      // }, {
      //   value: '民办双语',
      //   label: '民办双语'
      // }, {
      //   value: '国际学校',
      //   label: '国际学校'
      // }, {
      //   value: '陆本',
      //   label: '陆本'
      // }, {
      //   value: '海本',
      //   label: '海本'
      // }, {
      //   value: '海高',
      //   label: '海高'
      // }],
      // school_type:'',
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
        productList:[],
        rules: {
        curriculum_system: [{
          required: true,
          message: "课程体系不能为空",
          trigger: "blur"
        }
        ],
        school_type: [{
          required: true,
          message: "学校类型不能为空",
          trigger: "blur"
        }
        ],
        major: [{
          required: true,
          message: "专业方向不能为空",
          trigger: "blur"
        }
        ],
        application_level: [{
          required: true,
          message: "申请层级不能为空",
          trigger: "blur"
        }],
        graduation_date: [{
          required: true,
          message: "毕业时间不能为空",
          trigger: "blur"
        }],
      },
      stupushinfor:{
          curriculum_system:"",
          major:"",
          application_level:"",
          graduation_date:""
      },
    }
  },
    created() {
    var stupushinfor = window.sessionStorage.getItem("stupushinfor")
    var productlist = window.sessionStorage.getItem("productlist")
    if (stupushinfor ){
      this.stupushinfor = JSON.parse(stupushinfor)
      this.curriculum_system =  this.stupushinfor.curriculum_system
      this.application_level = this.stupushinfor.application_level
      this.productList = JSON.parse(productlist)
    }
   
  },
  methods:{
    productpush(){
      if (this.$route.name != 'productpush') {
        this.$router.push("/productpush")}
    },
    studentpush(){
      if (this.$route.name != 'studentpush') {
        this.$router.push("/studentpush")}
    },
    async StudentAnalysis(){
      this.stupushinfor.curriculum_system = this.curriculum_system
      this.stupushinfor.application_level = this.application_level
      this.$refs.stupushinfor.validate(async (valid) => {
        if (valid) {
          const res = await this.$ajax.post(`/studentanalysis/`, this.stupushinfor);
          let obj = JSON.parse(res.data)
          if (obj.status == 200){
            this.productList = obj.data
            window.sessionStorage.setItem("stupushinfor",JSON.stringify(this.stupushinfor))
            window.sessionStorage.setItem("productlist",JSON.stringify(obj.data))
          }else {
            this.$message({
              type: "warning",
              message: obj.message
              },
            window.sessionStorage.removeItem("stupushinfor"),
            this.productList=[]
            )
          }
          } else {
          this.$message({
            type: 'warning',
            message: "请填写带*号必填项"
          });
        }
      })
    },
    analysispath () {
      let identity = window.sessionStorage.getItem('department')
      var identity_list = ["学术成长学院" ,"数据管理员", "超级用户"]
      if (identity_list.findIndex(item => item=== identity)<0){
        this.$message({
        type: "warning",
        message: "权限不足，无法查看"
        },)
      return        
      }else{
        this.$router.push("/resourceanalysis")}
    },
  }
}
</script>

<style scoped lang="less">
.recommended{
    color: #fff;
    text-decoration: none;
    margin-left: 11px;
    line-height: 40px;
}
.analysis {
    color: rgb(141, 138, 138);
    cursor: pointer;
    text-decoration: none;
    margin-left: 11px;
    line-height: 40px;
}
.ai_recom{
  width: 220px;
  height: 40px;
  // display: block;
  background-color: #094572;
  color: #fff;
  margin-left: 4%;
  text-align: center;
  line-height: 40px;
  font-size: 18px;
  margin-bottom: 30px;
  border-radius: 10px;
  cursor: pointer;
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
.sturespush{
  width: 300px;
  height: 66px;
  margin-left: 4%;
  color: #094572;
}
.quantity{
  color: rgb(194, 187, 187)
}

</style>