<template>
  <div class="datashow">
    <div class="datahead">
      <router-link class="two_a" :to="{path:'/superPersona'}">个人中心 &gt;</router-link>
      <router-link class="one_a" :to="{path:'/employeeinfor'}"> 员工信息 &gt;</router-link>
      <router-link class="three_a" :to="{path:'/superregiste'}">注册账户</router-link>
    </div>
    <div class="infor">
      <div v-for="item in userInfoList" :key="item.id">
        <div class="employeeinfor">
          <div class="userclass">
            <img src="../../assets/username.png" class="idenimg">
            <span class="employeespan">{{item.username}}</span>
          </div>
          <!-- <div class="phoneclass">
            <img src="../../assets/cellphone.png" class="idenimg">
            <span class="employeespan">{{item.phone}}</span>
          </div> -->
          <div class="emailclass">
            <img src="../../assets/email.png" class="idenimg">
            <span class="employeespan" white-space:nowrap>{{item.email}}</span>
          </div>
        </div>
        <div class="employeeframe">
          <el-checkbox-group v-model="item.newUsertype" @change="handleCheckedCitiesChange" class="identity">
            <el-checkbox v-for="city in item.cities" :label="city" :key="city">{{city}}</el-checkbox>
          </el-checkbox-group>
        </div>
        <div class="deletebut">
        <span type="text" @click="updateuser(item.id)" class="updateinfo">更新信息</span>
        <br>
        <span type="text" @click="deleteuser(item.id)" class="updateinfo">删除用户</span>
        </div>
      </div>
      <el-pagination background layout="prev, pager, next" :total="employeepag">
      </el-pagination>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      userdepartment:'',
      employeepag: '',
      checkAll: false,
      cities: [],
      isIndeterminate: true,
      userInfoList: []
    }
  },
  created() {
    this.getuserinfo();
    // this.userdepartment = 
  },
  methods: {
    async  getuserinfo() {
      const res = await this.$ajax.get(`getuserinfo/`);
      let obj = JSON.parse(res.data);
      obj.forEach(item => {
        item.newUsertype = item.usertype.split(",");
        if (item.newUsertype =="学术成长学院" || item.newUsertype == "数据管理员"|| item.newUsertype == "超级用户" ){
          item.cities=["学术成长学院","数据管理员","超级用户"]
        }
        else{
          item.cities=[ '顾问', '文案', '助教','小助手','服务顾问', '战略顾问']
        }
      });
      this.userInfoList = obj;
      this.employeepag = obj.length
    },
    handleCheckedCitiesChange(value) {
      this.userdepartment = value
      let checkedCount = value.length
      this.checkAll = checkedCount === this.cities.length
      this.isIndeterminate = checkedCount > 0 && checkedCount < this.cities.length
      
    },
    deleteuser(item) {
      this.$confirm(`此操作将永久删除用户<${item.userName}>, 是否继续?`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
      .then(async () => {
        let paramObj = {
          user_id: item,
        }
        const res = await this.$ajax.delete(`/getuserinfo/`, {
          data: paramObj
        });
        if (res.data.status == 200) {
          this.userInfoList.some((it, i) => {
            if (it.id == item) {
              this.userInfoList.splice(i, 1)
            }
          }),
            this.$message({
              type: 'success',
              message: '删除成功!'
            })
        } else {
          this.$message({
            type: 'warning',
            message: '服务器连接失败'
          })
        }
      })
      .catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    },
    async  updateuser(item) {
      if (this.userdepartment){
        var update = {
        id:item,
        usertype:this.userdepartment.join(',')
      }
        const res = await this.$ajax.post(`/getuserinfo/`,update);
        if (res.data.status == 200) {
          this.$message({
            type: 'success',
            message: res.data.message
          })
        } else {
          this.$message({
            type: 'warning',
            message: res.data.message
          })
        }
      }else{
            this.$message({
            type: 'warning',
            message: "未检测到变化"
          })
      }

      }
    }
}
</script>

<style scoped lang="less">
/* 样式图片 */
.idenimg {
  margin-top: 18px;
  margin-left: 20px;
}
.updateinfo{
    width: 85px;
    height: 20px;
    color: #fff;
    text-align: center;
    display: inline-block;
    background-color: #094572;
    cursor: pointer;
}
/* 删除按钮 */
.deletebut {

  margin-top: 40px;
  margin-left: 10px;
  // border-radius: 20px;
  display: inline-block;
  // border-radius: 15px;
}
/* 删除按钮点击效果 */
.el-button:focus,
.el-button:hover {
  background: #094572;
  border-color: #271849;
  color: #fff;
}
.identity {
  width: 550px;
  margin-top: 25px;
  margin-left: 30px;
}

.employeeframe {
  width: 585px;
  height: 50px;
  background-color: #f2f4fb;
  margin-top: 40px;
  display: inline-block;
  margin-left: 30px;
  border-radius: 15px;
}
/* 设置显示栏容器 */
.datashow {
  width: 1200px;
  min-height: 450px;
  margin: 0 auto;
  border: solid #094572 1px;
  border-radius: 10px;


}
.employeeinfor {
  width: 430px;
  height: 50px;
  margin-top: 50px;
  background-color: #f2f4fb;
  margin-top: 40px;
  display: inline-block;
  border-radius: 15px;
}
.infor {
  width: 1140px;
  margin-left: 30px;
  padding-bottom: 20px;
}
.employeespan {
  margin-left: 10px;

}
// 翻页样式
.el-pagination {
  margin-top: 30px;
  text-align: center;
}
.userclass {
  width: 200px;
  display: inline-block;
  overflow:hidden;
  text-overflow:ellipsis;
  white-space:nowrap;
}
.phoneclass {
  width: 150px;
  display: inline-block;
  overflow:hidden;
  text-overflow:ellipsis;
  white-space:nowrap;
}
.emailclass {
  width: 200px;
  display: inline-block;
  overflow:hidden;
  text-overflow:ellipsis;
  white-space:nowrap;

}
/* 头标签 */
.datahead {
  height: 40px;
  background-color: #094572;
  border-radius: 10px;
  border: none;
}
.one_a {
  color: #fff;
  cursor: pointer;
  margin-left: 10px;
}
.three_a {
  color: rgb(168, 168, 168);
  cursor: pointer;
  margin-left: 10px;
}
.two_a {
  color: rgb(141, 138, 138);
  text-decoration: none;
  line-height: 40px;
}
</style>
