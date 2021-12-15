<template>
  <div>
    <div class="persdatashow">
      <div class="datahead">
        <router-link class="two_a" :to="{path:'/superPersona'}">个人中心 &gt;</router-link>
        <router-link class="one_a" :to="{path:'/employeeinfor'}"> 员工信息 &gt;</router-link>
        <router-link class="three_a" :to="{path:'/superregiste'}">注册账户</router-link>
      </div>
      <div class="app-container">
        <el-form :model="loginObj" :rules="rules" ref="loginObj" label-width="100px" class="loginObj">
          <img src="../../assets/username.png" alt="" class="superone">
          <div class="ipt_item">
            <el-form-item label="用户名" prop="username">
              <el-input placeholder="请输入用户名" v-model="loginObj.username"></el-input>
            </el-form-item>
          </div>
          <img src="../../assets/cellphone.png" alt="" class="superimg">
          <div class="ipt_item">
            <el-form-item label="手机号" prop="iphone">
              <el-input placeholder="请输入手机号" v-model="loginObj.iphone"></el-input>
            </el-form-item>
          </div>
          <img src="../../assets/email.png" alt="" class="superimg">
          <div class="ipt_item">
            <el-form-item label="邮箱" prop="email">
              <el-input placeholder="请输入邮箱" @blur="hasEmailFn()" v-model="loginObj.email"></el-input>
            </el-form-item>
          </div>
          <img src="../../assets/pawd.png" alt="" class="superimg">
          <div class="ipt_item">
            <el-form-item label="密码" prop="password">
              <el-input type="password" autocomplete="new-password" placeholder="请输入密码" v-model="loginObj.password"></el-input>
            </el-form-item>
          </div>
          <img src="../../assets/pawd.png" alt="" class="superimg">
          <div class="ipt_item">
            <el-form-item label="确认密码" prop="password2">
              <el-input type="password" placeholder="请再次输入密码" v-model="loginObj.password2"></el-input>
            </el-form-item>
          </div>
          <br>
          <img src="../../assets/username.png" alt="" class="superimg">
          <div class="ipt_item">
            <el-form-item label="用户身份">
              <el-radio v-model="checkedCities" fill="#094572" text-color="#094572" label="学术成长学院">学术成长学院</el-radio>
              <el-radio v-model="checkedCities" fill="#094572" text-color="#094572" label="数据管理员">数据管理员</el-radio>
            </el-form-item>
          </div>
          <div class="btns">
            <el-form-item>
              <el-button @click="loginSys('loginObj')">注册</el-button>
            </el-form-item>
          </div>
        </el-form>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      checkedCities: '',
      isIndeterminate: true,
      loginObj: {
        username: '',
        firstName: '',
        lastName: '',
        email: '',
        iphone: '',
        password: '',
        password2: '',
        gouxuanValue: false
      },
      allow: false,
      rules: {
        username: [
          {
            required: true,
            message: "用户名不能为空",
            trigger: "blur"
          }
        ],
        email: [
          {
            required: true,
            message: '邮箱不能为空',
            trigger: 'blur'
          }
        ],
        iphone: [
          {
            required: true,
            message: "手机号不能为空",
            trigger: "blur",
          },
        ],
        password: [
          {
            required: true,
            message: "密码不能为空",
            trigger: "blur"
          },
          {
            min: 8,
            max: 20,
            message: '密码长度为8-20位',
            trigger: 'change'
          }
        ],
        password2: [
          {
            required: true,
            message: "确认密码不能为空",
            trigger: "blur"
          },
          {
            min: 8,
            max: 20,
            message: '密码长度为8-20位',
            trigger: 'change'
          }
        ],
      },
      iszhuceFn: false,
    }
  },
  mounted() {
    document.body.scrollTop = document.documentElement.scrollTop = 0;

  },
  methods: {
    async hasEmailFn() {
      var reg = /^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
      if (!reg.test(this.loginObj.email)) {
        this.$message({
          type: 'warning',
          message: "邮箱格式错误"
        });
        return;
        
      }
      let email = this.loginObj.email;
      const res = await this.$ajax.post(`/email_number/`, {
        email: email
      })
      if (res.data.count == 0) {
        this.$message({
          type: 'success',
          message: "当前邮箱可注册"
        })
        this.iszhuceFn = false;
        return;
      } else {
        this.$message({
          type: 'warning',
          message: "当前邮箱已注册"
        });
        this.iszhuceFn = true;
        return;
      }

    },

    loginSys(loginObj) {
      this.$refs.loginObj.validate(async (valid) => {
        if (valid) {
          if (this.iszhuceFn) {
            this.$message({
              type: 'warning',
              message: "当前邮箱已注册"
            })
            return;
          }
          if (!this.checkedCities) {
            this.$message({
              type: 'warning',
              message: "请选择用户身份"
            })
            return;
          }
          if (this.loginObj.password != this.loginObj.password2) {
            this.$message({
              type: 'warning',
              message: "两个密码不一致"
            })
            return;
          }
          if (!this.loginObj.email) {
            this.$message({
              type: 'warning',
              message: "邮箱不能为空"
            });
            return;
          }
          var reg = /^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
          if (!reg.test(this.loginObj.email)) {
            this.$message({
              type: 'warning',
              message: "邮箱格式错误"
            });
            return;
          }
          var registerObj = {
            password: this.loginObj.password,
            password2: this.loginObj.password2,
            username: this.loginObj.username,
            email: this.loginObj.email,
            phone: this.loginObj.iphone,
            department: this.checkedCities,
          }
          const res = await this.$ajax.post(`/createuser/`, registerObj);
          if (res.data.token) {
            this.$message({
              type: "success",
              message: "注册成功"
            })
            window.sessionStorage.setItem("username", res.data.username);
          } else {
            this.$message({
              type: "warning",
              message: "登录失败"
            })
          }
        } else {
          this.$message({
            type: 'warning',
            message: "请核对填写信息",
            // duration: 1000000
          });
        }
      })
    },
  },
}
</script>
<style scoped lang="less">
/deep/ .el-radio__input.is-checked .el-radio__inner {
  color: #094572;
  background-color: #094572;
}
/deep/ .el-radio__input.is-checked + .el-radio__label {
  color: #094572;
}
.el-radio {
  color: #094572;
}

.preo_select {
  margin-left: 426px;
}
.superimg {
  margin-left: 386px;
}
.ipt_item {
  display: inline-block;
}
/* 第一个往下移 */
.superone {
  margin-left: 386px;
  margin-top: 100px;
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
  margin-left: 40px;
  margin-top: 40px;
  margin-bottom: 40px;
  background-color: #f2f4fb;
  border-radius: 15px;
}
/* 设置显示栏容器 */
.persdatashow {
  width: 1200px;
  margin: 0 auto;
  border: solid #094572 1px;
  border-radius: 10px;
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
  color: rgb(141, 138, 138);
  text-decoration: none;
  line-height: 40px;
}
.three_a {
  color: #fff;
  cursor: pointer;
  margin-left: 10px;
}
.el-checkbox {
  margin-left: -20px;
}

.el-checkbox__inner {
  background-color: #094572;
  border-color: #094572;
}
.loginObj {
  position: relative;
  z-index: 2001;
  margin-top: 40px;
}
.el-button {
  letter-spacing: 10px;
  width: 220px;
  height: 36px;
  font-size: 18px;
  background-color: #094572;
  border: none;
  border-radius: 10px;
  color: #ffffff;
  margin-left: 380px;
  margin-bottom: 30px;
  margin-top: 30px;
}
</style>
