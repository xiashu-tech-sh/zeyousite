<template>
  <div>
    <div class="persdatashow">
      <div class="datahead">
        <router-link class="two_a" :to="{path:'/superPersona'}">个人中心 &gt;</router-link>
        <router-link class="one_a" :to="{path:'/employeeinfor'}"> 员工信息 &gt;</router-link>
        <router-link class="three_a" :to="{path:'/superregiste'}">注册账户</router-link>
      </div>
      <div class="personal">
        <div class="personal-one">
          <img src="../../assets/username.png" alt=""><span class="persspen">姓名&nbsp;:&nbsp;&nbsp;</span>
          <input type="text" v-model="username" class="perinput_set">
        </div>
        <div class="personal-info">
          <img src="../../assets/cellphone.png" alt=""><span class="persspen">手机号&nbsp;:&nbsp;&nbsp;</span>
          <input type="text" v-model="phone" class="perinput">
        </div>
        <div class="personal-info">
          <img src="../../assets/email.png" alt=""><span class="persspen">邮箱&nbsp;:&nbsp;&nbsp;</span>
          <input type="text" v-model="email" class="perinput">
        </div>
        <div >
          <spen class="updatadiv" adjustsImageWhenHighlighted = NO @click="uppersonainfor()">更新信息</spen>
        </div>
      </div>
      <div class="app-container">
        <el-form :model="resetForm" :rules="resetFormRules" ref="resetForm" status-icon label-width="100px">
          <img src="../../assets/pawd.png" alt="" class="pwdimgone">
          <div class="pawtype">
            <el-form-item label="旧密码：" prop="old_password">
              <el-input type="password" v-model="resetForm.old_password" auto-complete="off" placeholder="请输入旧密码"></el-input>
            </el-form-item>
          </div>
          <img src="../../assets/pawd.png" alt="" class="pwdimg">
          <div class="pawtype">
            <el-form-item label="新密码：" prop="new_password">
              <el-input type="password" v-model="resetForm.new_password" auto-complete="off" placeholder="请输入新密码"></el-input>
            </el-form-item>
          </div>
          <img src="../../assets/pawd.png" alt="" class="pwdimg">
          <div class="pawtype">
            <el-form-item label="确认密码：" prop="confirm_password">
              <el-input type="password" v-model="resetForm.confirm_password" auto-complete="off" placeholder="请再次输入新密码"></el-input>
            </el-form-item>
          </div>
          <el-form-item>
            <el-button type="primary" @click.native.prevent="toAmend">确认修改</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    var validatePass = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入新密码'))
      } else if (value.toString().length < 6 || value.toString().length > 18) {
        callback(new Error('密码长度为6-18位'))
      } else {
        callback()
      }
    }
    var validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== this.resetForm.new_password) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    }
    return {
      username: '',
      email: '',
      phone: '',
      resetForm: {
        //   传给后台所需要的参数
        old_password: '',
        new_password: '',
        confirm_password: '',
        user_id: ''
      },
      resetFormRules: {
        old_password: [
          { required: true, message: '请输入旧密码', trigger: 'blur' }
        ],
        new_password: [
          { required: true, validator: validatePass, trigger: 'blur' }
        ],
        confirm_password: [
          { required: true, validator: validatePass2, trigger: 'blur' }
        ]
      },
      formInline: {
        user: '',
        region: '',
        source: '',
        protype: '',
        teacher: '',
        teaching_assistant: '',
        salesperson: '',
        purchase_time: '',
        product_content: '',
        class_date: '',
        school_hour: '',
        quotation: '',
        total_price: '',
        status: ''
      }
    }
  },
  created() {
    this.getuserinfor();
  },
  methods: {
    async getuserinfor() {
      let user_id = window.sessionStorage.getItem("user_id");
      // var user_id = 1  // 测试使用
      const res = await this.$ajax.get(`user/${user_id}/`);
      if (res.data.status == 200) {
        this.userForm = res.data;
        this.username = res.data.username;
        this.email = res.data.email;
        this.phone = res.data.phone;
      } else {
        this.$message({
          type: 'warning',
          message: res.data.message

        })
        // this.$router.push(`/login`) // 请求失败跳转到登录界面
      }
    },
    async uppersonainfor() {
          this.resetForm.user_id=window.sessionStorage.getItem("user_id")
          // this.resetForm.user_id = 1
          this.resetForm.phone = this.phone
          this.resetForm.email = this.email
          const res = await this.$ajax.post(`/personupdate/`, this.resetForm)
          if (res.data.status == 200) {
            this.$message({
              type: "success",
              iconClass: "el-icon-diy-Success123",
              message: res.data.message
            })
          } else {
            this.$message({
              type: 'warning',
              message: res.data.message

            })
          }
    },
    toAmend() {
      this.$refs.resetForm.validate(async valid => {
        if (valid) {
          this.resetForm.user_id=window.sessionStorage.getItem("user_id")
          // this.resetForm.user_id = 1
          this.resetForm.phone = this.phone
          this.resetForm.email = this.email
          this.resetForm.username = this.username
          const res = await this.$ajax.post(`/pwdupdate/`, this.resetForm)
          if (res.data.status == 200) {
            this.$message({
              type: "success",
              iconClass: "el-icon-diy-Success123",
              message: res.data.message
            })
          } else {
            this.$message({
              type: 'warning',
              message: res.data.message

            })
          }
        } else {
          this.$message({
            type: 'warning',
            message: "请填写带*号必填项"
          });
        }

      },
      )
    },
    //    这是修改成功后重新返回登陆页的方法，看个人需要自行调整
    async logout() {
      await this.$store.dispatch('user/logout')
      this.$router.push(`/login`)
    }
  }
}
</script>
<style scoped lang="less">
// 姓名栏文字
.persspen {
  margin-left: 16px;
}
/* 确认修改按钮样式 */
.el-button--primary {
  background-color: #094572;
  margin-left: 430px;
  margin-top: 40px;
}
.el-button:focus,
.el-button:hover {
  background: #094572;
  border-color: #271849;
  color: #fff;
}
.pawtype {
  display: inline-block;
}
.el-input__inner {
  width: 250px;
  height: 30px;
  margin-left: 20px;
  border-radius: 10px;
}
/* 灰色背景容器 */
.app-container {
  width: 1120px;
  height: 470px;
  margin-left: 40px;
  margin-top: 40px;
  margin-bottom: 40px;
  background-color: #f2f4fb;
  border-radius: 15px;
}
/* 第一个往下移 */
.pwdimgone {
  margin-left: 386px;
  margin-top: 100px;
}
.el-form-item__error {
  margin-left: 100px;
}
/* 右移 */
.pwdimg {
  margin-left: 386px;
}

.personal-info {
  width: 250px;
  border: solid 1px #094572;
  border-top-width: 0px;
  border-right-width: 0px;
  border-bottom-width: 1px;
  border-left-width: 0px;
  margin-left: 126px;
  display: inline-block;
  overflow:hidden;
  text-overflow:ellipsis;
  white-space:nowrap;
}
.personal {
  margin: 0 auto;
  width: 1120px;
}
/* 设置显示栏容器 */
.persdatashow {
  width: 1200px;
  margin: 0 auto;
  border: solid #094572 1px;
  border-radius: 10px;
}
.el-form-item__error {
  margin-left: 30px;
}
.perinput {
  width: 150px;
  outline: none;
  border: none;
}
.perinput_set{
  width: 150px;
  outline: none;
  border: none;
  color:#a5a2a2;
  background-color: #fff;

}
/* 头标签 */
.datahead {
  height: 40px;
  background-color: #094572;
  border-radius: 10px;
  border: none;
}
.one_a {
  color: rgb(141, 138, 138);
  cursor: pointer;
  margin-left: 10px;
}
.two_a {
  color: #fff;
  text-decoration: none;
  line-height: 40px;
}
.three_a {
  color: rgb(141, 138, 138);
  cursor: pointer;
  margin-left: 10px;
}
.updatadiv{
  margin-top: -26px;
  float:right;
  width: 95px;
  height: 23px;
  color: #fff;
  text-align: center;
  display: inline-block;
  background-color: #094572;
  cursor: pointer;
}
.personal-one {
  width: 250px;
  border: solid 1px #094572;
  border-top-width: 0px;
  border-right-width: 0px;
  border-bottom-width: 1px;
  border-left-width: 0px;
  display: inline-block;
  margin-top: 50px;
  overflow:hidden;
  text-overflow:ellipsis;
  white-space:nowrap;
}
</style>
