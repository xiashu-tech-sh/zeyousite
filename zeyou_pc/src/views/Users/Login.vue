<template>
  <div class="app">
    <div class="login_view">
      <div class="title">
        <img src="../../assets/logo.png" alt="">
      </div>
      <el-form :model="loginObj" :rules="rules" ref="loginObj" label-width="100px" class="loginObj">
        <div class="ipt_item">
          <div class="label">
            <img src="../../assets/username.png" alt="">
          </div>
          <el-form-item label="" prop="keyword">
            <el-input placeholder="请输入账户" v-model="loginObj.keyword"></el-input>
          </el-form-item>
        </div>
        <div class="ipt_item">
          <div class="label">
            <img src="../../assets/pawd.png" alt="">
          </div>
          <el-form-item label="" prop="password">
            <el-input type="password" placeholder="请输入密码" @keyup.enter.native="loginSys('loginObj')" v-model="loginObj.password"></el-input>
          </el-form-item>
        </div>
        <div class="btns">
          <el-form-item>
            <el-button @click="loginSys('loginObj')">登陆</el-button>
          </el-form-item>
        </div>
        <div class="status clearfix">
          <span class="logbut" @click="toRegisterFn()">注册账户</span>
          <span class="logright" @click="toPasswordFn()">忘记密码</span>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      loginObj: {
        keyword: '',
        password: ''
      },
      rules: {
        keyword: [{
          required: true,
          message: '账户不能为空',
          trigger: 'blur'
        },
        ],
        password: [{
          required: true,
          message: '密码不能为空',
          trigger: 'blur'
        }],
      },
    }
  },
  created() {
    let username = window.sessionStorage.getItem("username");
    this.loginObj.keyword = username;
  },
  mounted() {
    document.body.scrollTop = document.documentElement.scrollTop = 0;
  },
  methods: {
    toPasswordFn() {
      this.$router.push("/editPassword");
    },
    toRegisterFn() {
      this.$router.push("/register");
    },
    loginSys(formName) {
      if (this.loginObj) {
        this.$refs[formName].validate(async (valid) => {
          if (valid) {
            console.log(this.loginObj)
            var loginObj = {
              username: this.loginObj.keyword,
              password: this.loginObj.password,
            }
            const res = await this.$ajax.post(`/authorizations/`, loginObj);
            if (res.data.status === 200) {
              var _mainObj = {
                'user_id': res.data.user_id,
                'token': res.data.token,
                'username': res.data.username
              }
              let token = _mainObj.token;
              _mainObj = JSON.stringify(_mainObj);
              window.sessionStorage.setItem('_mainObj', _mainObj);
              window.sessionStorage.setItem("username", res.data.username);
              window.sessionStorage.setItem("authentication", JSON.stringify(token));
              window.sessionStorage.setItem("department", res.data.department);
              window.sessionStorage.setItem("user_id", res.data.user_id);
              window.sessionStorage.setItem("div_hight", 1)
              this.$router.push('/adddata');
              location.reload();
            }
            else {
              this.$message({
                type: 'warning',
                message: '用户名或密码错误'
              })
            }
          } else {
            this.$message({
              type: 'warning',
              message: "Please complete the information"
            });
          }
        });
      }
    },
  },
}
</script>

<style scoped lang="less">
.app {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  min-width: 1000px;
  background: url(../../assets/background.png) center 0 no-repeat;
  background-size: cover;
  -webkit-background-size: cover;
  -o-background-size: cover;
}

.login_view {
  float: right;
  width: 400px;
  height: 360px;
  padding-bottom: 30px;
  background: rgba(255, 255, 255, 1);
  border-radius: 16px;
  margin: 9% 12%;

  .title {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 40px;
  }
}

.loginObj {
  position: relative;
  z-index: 2001;
  margin-top: 40px;
  .ipt_item {
    position: relative;
    width: 291px;
    height: 35px;
    margin: 0 auto;
    margin-bottom: 20px;
    border-radius: 15px;
    border: 1px solid #094572;

    /deep/ .el-form-item__label {
      display: none;
    }

    /deep/ .el-input__inner {
      border: 0;
      height: 30px;
      margin-top: -2px;
      border-radius: 0;
      width: 150px;
      margin-left: 3px;
    }

    /deep/ .el-form-item {
      display: inline-block;
      margin-left: 75px;
    }

    /deep/ .el-form-item__content {
      margin-left: 0 !important;
      line-height: 35px;
      background-color: #fff;
    }

    .label {
      width: 26px;
      height: 26px;
      position: absolute;
      left: 55px;
      top: 70%;
      transform: translateY(-50%);
    }
  }

  .btns {
    padding-top: 20px;
    .el-button {
      letter-spacing: 5px;
      width: 291px;
      height: 36px;
      font-size: 18px;
      background-color: #094572;
      border: none;
      border-radius: 10px;
      color: #ffffff;
      margin-left: 56px;
    }

    /deep/ .el-form-item__content {
      margin-left: 0 !important;
      height: 100%;
      line-height: 37px;
    }
  }

  .status {
    width: 291px;
    margin: 0 auto;
    // border-bottom: 1px solid #ccc;
    font-size: 13px;
    font-family: Source Han Sans CN;
    font-weight: 400;
    color: rgba(153, 153, 153, 1);
    padding-bottom: 18px;
    box-sizing: border-box;

    .left {
      cursor: pointer;
    }

    .right {
      cursor: pointer;
    }
  }

  .others {
    margin: 0 auto;
    margin-top: 25px;
    padding-right: 30px;

    .text {
      font-size: 13px;
      font-family: Source Han Sans CN;
      font-weight: 400;
      color: rgba(54, 62, 21, 1);
      text-align: right;
    }
  }
}
.logright {
  margin-left: 185px;
  color: #094572;
  cursor: pointer;
}
.logbut {
  color: #094572;
  cursor: pointer;
}
</style>