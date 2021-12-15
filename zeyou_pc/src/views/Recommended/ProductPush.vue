<template>
  <div class="recomshow">
    <div class="datahead">
      <a class="recommended" >推荐系统 ></a>
      <a class="analysis " @click="analysispath()">数据分析</a>
    </div>
    <el-form style="width:100%" :inline="true" :rules="rules" :model="productinfor" ref="productinfor" class="masterinfor">
        <el-form-item>
            <el-button type="primary" @click="productpush()">产品信息推荐学生</el-button>
            <el-button type="primary" class="quantity" @click="studentpush()">学生信息推荐产品</el-button>
        </el-form-item>
        <el-form-item label="产品课程体系" prop="curriculum_system">
          <el-select v-model="curriculum_system" placeholder="请选择课程体系">
            <el-option v-for="item in curriculum_systems" :key="item.value" :label="item.label" :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="产品难度" prop="difficulty_level">
            <el-select v-model="difficulty_level" placeholder="请选择产品难度">
            <el-option v-for="item in difficulty_levels" :key="item.value" :label="item.label" :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="专业方向" prop="major">
            <el-input v-model="productinfor.major"  placeholder="请输入专业方向"></el-input>
        </el-form-item>
          <el-form-item label="班型大小" prop="difficulty_level">
            <el-select v-model="class_size" placeholder="请选择班型大小">
            <el-option v-for="item in class_sizes" :key="item.value" :label="item.label" :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="申请层级" prop="application_level">
          <el-select v-model="application_level" placeholder="请选择申请层级">
            <el-option v-for="item in application_levels" :key="item.value" :label="item.label" :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <div class="ai_recom"  @click="ProductAnalysis()" >
        <spen class="ai_spen">智能分析</spen>
        </div>
    </el-form>
    <el-table
    :data="tableData"
    style="width: 90%"
    border>
    <el-table-column
      prop="name"
      label="姓名"
      width="180">
    </el-table-column>
    <el-table-column
      prop="wechat_num"
      label="微信号"
      width="150">
    </el-table-column>
    <el-table-column
      prop="little_assistant"
      label="所属小助手"
      width="120">
    </el-table-column>
    <el-table-column
      prop="consultant"
      label="所属顾问"
      width="120">
    </el-table-column>
    <el-table-column
      prop="school"
      label="学校名"
      width="150">
    </el-table-column>
    <el-table-column
      prop="major"
      label="专业方向"
      width="150">
    </el-table-column>
    <el-table-column
      prop="application_level"
      label="申请层级"
      width="150">
    </el-table-column>
    <el-table-column
      prop="graduation_date"
      label="入学时间"
      width="150">
    </el-table-column>
    <el-table-column
      prop="customer_state"
      label="客户状态"
      width="150">
    </el-table-column>
    <el-table-column
      prop="product_name"
      label="产品名称"
      width="150">
    </el-table-column>
  </el-table>
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
      class_sizes:[{
        value: '小班',
        label: '小班'
      }, {
        value: '中班',
        label: '中班'
      }, {
        value: '大班',
        label: '大班'
      }],
      class_size:'',
      difficulty_levels:[{
        value: '1',
        label: '1'
      }, {
        value: '2',
        label: '2'
      }, {
        value: '3',
        label: '3'
      }, {
        value: '4',
        label: '4'
      }, {
        value: '5',
        label: '5'
      }],
      difficulty_level:'',
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
        rules: {
        curriculum_system: [{
          required: true,
          message: "课程体系不能为空",
          trigger: "blur"
        }
        ],
        difficulty_level: [{
          required: true,
          message: "产品难度不能为空",
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
      },
      productinfor:{
          curriculum_system:"",
          difficulty_level:"",
          major:"",
          class_size:"",
          application_level:"",
      },
    tableData: [],
    }
  },
  created() {
    var pro_data = window.sessionStorage.getItem("productinfor")
    var tab_data = window.sessionStorage.getItem("tabledata")
    if (pro_data ){
      this.productinfor = JSON.parse(pro_data)
      this.curriculum_system = this.productinfor.curriculum_system
      this.difficulty_level = this.productinfor.difficulty_level
      this.application_level = this.productinfor.application_level
      this.class_size = this.productinfor.class_size
      this.tableData = JSON.parse(tab_data)
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
    async ProductAnalysis(){
      this.productinfor.curriculum_system = this.curriculum_system
      this.productinfor.difficulty_level = this.difficulty_level
      this.productinfor.application_level = this.application_level
      this.productinfor.class_size = this.class_size
      this.$refs.productinfor.validate(async (valid) => {
        if (valid) {
          let identity = window.sessionStorage.getItem('department')
          if (identity == "学术成长学院" || identity == "数据管理员" || identity == "超级用户") {
            var tity = true
            }else{
              var tity = false
            }
          this.productinfor.identity = tity
          let username = window.sessionStorage.getItem("username")
          this.productinfor.username = username
          const res = await this.$ajax.post(`/productanalysis/`, this.productinfor);
          var obj = JSON.parse(res.data)
          if (obj.status == 200){
            this.tableData = obj.res_data
            window.sessionStorage.setItem("productinfor",JSON.stringify(this.productinfor))
            window.sessionStorage.setItem("tabledata",JSON.stringify(obj.res_data))
          }else {
            this.$message({
              type: "warning",
              message: obj.message
              },
            window.sessionStorage.removeItem("tabledata"),
            this.tableData=[]
            )
          }
        } else {
          this.$message({
            type: 'warning',
            message: "请填写带*号必填项"
          });
          window.sessionStorage.removeItem("tabledata"),
          this.tableData=[]
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
.el-table--border{
  margin-left: 4%;
}
.quantity{
  color: rgb(194, 187, 187)
}
.el-table--border{
    margin-bottom: 50px;
}
</style>