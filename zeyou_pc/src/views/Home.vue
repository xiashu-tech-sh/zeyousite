<template>
  <div>
    <div class="header">
      <div class="headcontent">
        <div class="headerleft"><img src="../assets/logo.png" alt="" class="headlog">
          <span class="headtitle">择由智能客群管理系统</span>
        </div>
        <div class="headerright" @click="logout()">
          <span class="headexit">退出</span>
        </div>
      </div>
    </div>
    <div class="navigationcontainer">
      <div id="Navi-one" @click="oneHigh()">
        <div class="round" id="onevolume"></div>
        <span class="nav_span">导入数据</span>
        <img src="../assets/dataimg.png" class="nav_img" alt="">
      </div>
      <div id="Navi-box" @click="twoHigh()">
        <!-- <a href="login.html" class="jump"></a> -->
        <div class="round" id="twovolume"></div>
        <span class="nav_span">客户信息</span>
        <img src="../assets/customerinfor.png" class="nav_img" alt="">
      </div>
      <div id="Navi-box" @click="threeHigh()">
        <!-- <a href="register_success.html" class="jump"></a> -->
        <div class="round" id="threevolume"></div>
        <span class="nav_span">{{ThirdColumn}}</span>
        <img src="../assets/personal.png" class="nav_img" alt="">
      </div>
      <div id="Navi-box" @click="fourHigh()">
        <div class="round" id="fourvolume"></div>
        <span class="nav_span">推荐系统</span>
        <img src="../assets/recommended.png" class="nav_img" alt="">
      </div>
    </div>
    <div class="main">
      <router-view></router-view>
    </div>
    <div class="footer">
      <div class="footer_text"> Copyright 2015－2020 choicefree ALL Rights Reserved 沪ICP备1502547</div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      ThirdColumn: '',
      SuperUser: false
    }
  },
  mounted() {
    if (window.sessionStorage.getItem("department") == '超级用户') {
      this.ThirdColumn = "员工/个人中心"
      this.SuperUser = true
    } else {
      this.ThirdColumn = "个人中心"
      this.SuperUser = false
    }
    
    var div_hight = window.sessionStorage.getItem("div_hight")
    if (div_hight == 1) {
      var oDiv = document.getElementById('onevolume')
      var oDiv2 = document.getElementById('twovolume')
      var oDiv3 = document.getElementById('threevolume')
      var oDiv4 = document.getElementById('fourvolume')
      oDiv.style.backgroundColor = "#094572"
      oDiv2.style.backgroundColor = "#fff"
      oDiv3.style.backgroundColor = "#fff"
      oDiv4.style.backgroundColor = "#fff"
      window.sessionStorage.setItem("div_hight", 1)
    }
    if (div_hight == 2) {
      var oDiv = document.getElementById('onevolume')
      var oDiv2 = document.getElementById('twovolume')
      var oDiv3 = document.getElementById('threevolume')
      var oDiv4 = document.getElementById('fourvolume')
      oDiv.style.backgroundColor = "#fff"
      oDiv2.style.backgroundColor = "#094572"
      oDiv3.style.backgroundColor = "#fff"
      oDiv4.style.backgroundColor = "#fff"
      window.sessionStorage.setItem("div_hight", 2)
    }
    if (div_hight == 3) {
      var oDiv = document.getElementById('onevolume')
      var oDiv2 = document.getElementById('twovolume')
      var oDiv3 = document.getElementById('threevolume')
      var oDiv4 = document.getElementById('fourvolume')
      oDiv.style.backgroundColor = "#fff"
      oDiv2.style.backgroundColor = "#fff"
      oDiv3.style.backgroundColor = "#094572"
      oDiv4.style.backgroundColor = "#fff"
      window.sessionStorage.setItem("div_hight", 3)
    }
    if (div_hight == 4) {
      var oDiv = document.getElementById('onevolume')
      var oDiv2 = document.getElementById('twovolume')
      var oDiv3 = document.getElementById('threevolume')
      var oDiv4 = document.getElementById('fourvolume')
      oDiv.style.backgroundColor = "#fff"
      oDiv2.style.backgroundColor = "#fff"
      oDiv3.style.backgroundColor = "#fff"
      oDiv4.style.backgroundColor = "#094572"
      window.sessionStorage.setItem("div_hight", 4)
    }
  },
  methods: {
    oneHigh() {
      var oDiv = document.getElementById('onevolume')
      var oDiv2 = document.getElementById('twovolume')
      var oDiv3 = document.getElementById('threevolume')
      var oDiv4 = document.getElementById('fourvolume')
      oDiv.style.backgroundColor = "#094572"
      oDiv2.style.backgroundColor = "#fff"
      oDiv3.style.backgroundColor = "#fff"
      oDiv4.style.backgroundColor = "#fff"
      if (this.$route.name != 'AddData') {
        this.$router.push("/adddata")
      }
      window.sessionStorage.setItem("div_hight", 1)
    },
    twoHigh() {
      var oDiv = document.getElementById('onevolume')
      var oDiv2 = document.getElementById('twovolume')
      var oDiv3 = document.getElementById('threevolume')
      var oDiv4 = document.getElementById('fourvolume')
      oDiv.style.backgroundColor = "#fff"
      oDiv2.style.backgroundColor = "#094572"
      oDiv3.style.backgroundColor = "#fff"
      oDiv4.style.backgroundColor = "#fff"
      if (this.$route.name != 'customer') {
        this.$router.push("/customer")
      }
      window.sessionStorage.setItem("div_hight", 2)
    },
    threeHigh() {
      var oDiv = document.getElementById('onevolume')
      var oDiv2 = document.getElementById('twovolume')
      var oDiv3 = document.getElementById('threevolume')
      var oDiv4 = document.getElementById('fourvolume')
      oDiv.style.backgroundColor = "#fff"
      oDiv2.style.backgroundColor = "#fff"
      oDiv3.style.backgroundColor = "#094572"
      oDiv4.style.backgroundColor = "#fff"
      if (this.SuperUser) {
        this.$router.push("/superPersona")
      } else {
        this.$router.push("/personalcenter")
      }
      window.sessionStorage.setItem("div_hight", 3)

    },
    fourHigh() {
      var oDiv = document.getElementById('onevolume')
      var oDiv2 = document.getElementById('twovolume')
      var oDiv3 = document.getElementById('threevolume')
      var oDiv4 = document.getElementById('fourvolume')
      oDiv.style.backgroundColor = "#fff"
      oDiv2.style.backgroundColor = "#fff"
      oDiv3.style.backgroundColor = "#fff"
      oDiv4.style.backgroundColor = "#094572"
      if (this.$route.name != 'productpush') {
        this.$router.push("/productpush")
      }
      window.sessionStorage.setItem("div_hight", 4)
    },
    // 退出登录
    logout() {
      var _this = this
      _this
        .$confirm('确认退出吗?', '提示', {
        })
        .then(() => {
          window.sessionStorage.clear()
          window.location.href = '/login'
        })
        .catch(() => {
          this.$message({
            showClose: true,
            message: '已取消',
            type: 'warning'
          });
        })
    },
  },
  computed: {

  },
  watch: {

  }
}

</script>

<style scoped lang="less">
.showtaaa{
  width: 100px;
}
.spandivshow{
  width: 100px;
}
* {
  margin: 0;
  padding: 0;
}
.main {
  min-height: calc(100vh - 100px - 136px - 101px);
  padding-top: 50px;
  box-sizing: border-box;
}
/* 设置显示栏容器 */
.datashow {
  width: 1200px;
  // min-height: 600px;
  margin: 0 auto;
  border: solid #094572 1px;
  border-radius: 10px;
}
/* 图标样式 */
.round {
  width: 27px;
  height: 16px;
  background-color: #fff;
  border-radius: 0 8px 8px 0;
  position: absolute;
  top: 32px;
}
/* 页脚 */
.footer {
  width: 100%;
  background: #094572;
  margin-top: 50px;
  text-align: center;
}
.footer_text {
  // height: 51px;
  color: aliceblue;
  line-height: 53px;
}
/* 首个导航栏去除margin */
#Navi-one {
  overflow: hidden;
  display: inline-block;
  position: relative;
  color: #094572;
  width: 255px;
  height: 80px;
  border: solid #094572 1px;
  border-radius: 10px;
  margin: 0px;
  cursor: pointer;
}
/* 其次导航栏存在margin */
#Navi-box {
  overflow: hidden;
  display: inline-block;
  position: relative;
  color: #094572;
  width: 255px;
  height: 80px;
  border: solid #094572 1px;
  border-radius: 10px;
  margin-left: 52px;
  cursor: pointer;
}
/* 导航栏文字样式 */
.nav_span {
  font-weight: bold;
  position: absolute;
  top: 30px;
  left: 45px;
  font-size: 20px;
}
/* 导航栏图片样式 */
.nav_img {
  position: absolute;
  top: 16px;
  right: 31px;
}
/* 设置导航栏容器 */
.navigationcontainer {
  width: 1200px;
  margin: 0 auto;
  margin-top: 50px;
}
/* 设置头背景颜色 */
.header {
  height: 100px;
  background-color: #094572;
}
/* 设置头位置 */
.headcontent {
  width: 1200px;
  margin: 0 auto;
  // display: block;
}
/* log图片位置调整 */
.headlog {
  margin-top: 30px;
  margin-left: 0px;
}
/* 文字样式 */
.headtitle {
  position: absolute;
  line-height: 97px;
  color: #fff;
  font-weight: bold;
  font-size: 24px;
  margin-left: 20px;
}
.headexit {
  color: #094572;
  top: 10px;
  width: 100px;
  height: 30px;
  border: none;
  border-radius: 15px;
  text-align: left;
  background-color: #fff;
  background-image: url("../assets/exit.png");
  background-repeat: no-repeat;
  background-position: 91% 50%;
  margin-left: 10px;
  margin-top: 37px;
  cursor: pointer;
  outline: none;
  display: flex;
  align-items: center;
  justify-content: center;
}
.headerright {
  width: 200px;
  float: right;
  margin-top: -70px;
}

</style>