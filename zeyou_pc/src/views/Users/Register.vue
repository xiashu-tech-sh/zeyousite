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
                    <el-form-item label="" prop="username">
                        <el-input placeholder="请输入账户" @blur="hasUsernameFn()" v-model="loginObj.username" ></el-input>
                    </el-form-item>
                </div>
                <div class="ipt_item">
                    <div class="label">
                        <img src="../../assets/cellphone.png" alt="">
                    </div>
                    <el-form-item label="" prop="iphone">
                        <el-input placeholder="请输入手机号" v-model="loginObj.iphone"></el-input>
                    </el-form-item>
                </div>
                <div class="ipt_item">
                    <div class="label">
                        <img src="../../assets/email.png" alt="">
                    </div>
                    <el-form-item prop="email">
                        <el-input placeholder="请输入邮箱" @blur="hasEmailFn()" v-model="loginObj.email"></el-input>
                    </el-form-item>
                </div>
                <div class="ipt_item">
                    <div class="label">
                        <img src="../../assets/pawd.png" alt="">
                    </div>
                    <el-form-item  prop="password">
                        <el-input type="password" autocomplete="new-password" placeholder="请输入密码" v-model="loginObj.password"></el-input>
                    </el-form-item>
                </div>
                <div class="ipt_item">
                    <div class="label">
                        <img src="../../assets/pawd.png" alt="">
                    </div>
                    <el-form-item prop="password2">
                        <el-input type="password" placeholder="请再次输入密码" v-model="loginObj.password2"></el-input>
                    </el-form-item>
                </div>
                <div class="ipt_item">
                    <el-checkbox-group v-model="checkedCities"  @change="handleCheckedCitiesChange" class="identity">
                        <el-checkbox label="顾问">顾问</el-checkbox>
                        <el-checkbox label="服务顾问">服务顾问</el-checkbox>
                        <el-checkbox label="小助手">小助手</el-checkbox>
                        <el-checkbox label="助教">助教</el-checkbox>
                        <el-checkbox label="战略顾问">战略顾问</el-checkbox>
                        <el-checkbox label="文案">文案</el-checkbox>
                    </el-checkbox-group>
                </div>
                <div class="btns">
                    <el-form-item>
                        <el-button @click="loginSys('loginObj')">注册</el-button>
                    </el-form-item>
                <div class="status clearfix">
                    <span class="rigisrispan" @click="tologinFn()">已有账户?去登录</span>
                    <span class="rigisright" @click="toPasswordFn()">忘记密码</span>
                </div>
                </div>
            </el-form>
        </div>
    </div>
</template>

<script>
export default {
    data () {
        return {
            checkedCities: [],
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
            isusernameFn:false
        }
    },
    mounted() {
        document.body.scrollTop = document.documentElement.scrollTop = 0;

    },
    methods: {
        toPasswordFn() {
            this.$router.push("/editPassword")
        },
        tologinFn(){
            this.$router.push("/login")
        },
        handleCheckedCitiesChange (value) {
            let checkedCount = value.length
            this.checkAll = checkedCount === this.cities.length
            this.isIndeterminate = checkedCount > 0 && checkedCount < this.cities.length
            },
        async hasEmailFn () {
            var reg=/^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
            if(!reg.test(this.loginObj.email)){
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
        async hasUsernameFn () {
            let username = this.loginObj.username;
            const res = await this.$ajax.post(`/username_number/`, {
                username: username
            })
            if (res.data.count == 0) {
                this.$message({
                    type: 'success',
                    message: "当前用户名可注册"
                })
                this.isusernameFn = false;
                return;
            } else {
                this.$message({
                    type: 'warning',
                    message: "当前用户名已注册"
                });
                this.isusernameFn = true;
                return;
            }
        },
        loginSys (loginObj) {
            this.$refs.loginObj.validate(async (valid) => {
                if (valid) {
                    if (this.iszhuceFn) {
                        this.$message({
                            type: 'warning',
                            message: "当前邮箱已注册"
                        })
                        return;
                    }
                    if (this.isusernameFn) {
                        this.$message({
                            type: 'warning',
                            message: "当前用户名已注册"
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
                    var reg=/^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
                    if(!reg.test(this.loginObj.email)){
                        this.$message({
                            type: 'warning',
                            message: "邮箱格式错误"
                        });
                        return;
                    }
                    var strchecke = this.checkedCities.join(',')
                    var registerObj = {
                        password: this.loginObj.password,
                        password2: this.loginObj.password2,
                        username: this.loginObj.username,
                        email: this.loginObj.email,
                        phone: this.loginObj.iphone,
                        department:strchecke,
                    }
                    const res = await this.$ajax.post(`/createuser/`, registerObj);
                    if (res.data.token) {
                        this.$message({
                            type: "success",
                            message: "注册成功"
                        })
                        window.sessionStorage.setItem("username", res.data.username);
                        this.$router.push("/login");
                    } else {
                        this.$message({
                            type: "warning",
                            message: "登录失败"
                        })
                    }
                } else { 
                    this.$message({
                        type: 'warning',
                        message: "请核对填写信息"
                    });
                }
            })
        },
    },
}
</script>

<style scoped lang="less">
.app {
        position:fixed;
        top:0;
        left:0;
        width:100%;
        height:100%;
        min-width: 1000px;
        background: url(../../assets/background.png) center 0 no-repeat;
        background-size: cover;
        -webkit-background-size: cover;
        -o-background-size: cover;
}
.identity{
    width: 250px;
    height: 30px;
    margin-top: 22px;
    margin-left:10px;
}

.el-checkbox{
    margin-left: -20px;
}
.login_view {
    float: right;
    width: 400px;
    // height: 360px;
    padding-bottom: 30px;
    background: rgba(255, 255, 255, 1);
    border-radius: 16px;
    margin:9% 12%;  

    .title {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 40px;
    }
}
.el-checkbox__inner{
    background-color: #094572;
    border-color:#094572;
}
.loginObj {
    position: relative;
    z-index: 2001;
    margin-top: 40px;
    .ipt_item {
        position: relative;
        width: 220px;
        height: 35px;
        margin: 0 auto;
        margin-bottom: 15px;
        border: solid 1px #094572;
        border-top-width: 0px;
        border-right-width: 0px;
        border-bottom-width: 1px;
        border-left-width: 0px;

        /deep/ .el-form-item__label {
            display: none;
        }

        /deep/ .el-input__inner {
            border: 0;
            height: 30px;
            margin-top: -2px;
            border-radius: 0;
            width: 150px;
            margin-left: -42px;
            color: #094572;
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
        /deep/

        .label {
            width: 26px;
            height: 26px;
            position: absolute;
            left: 10px;
            top: 70%;
            transform: translateY(-50%);
        }
    }

    .btns {
        padding-top: 20px;
        .el-button {
        letter-spacing: 10px;
        width:  220px;
        height: 36px;
        font-size: 18px;
        background-color: #094572;
        border: none;
        border-radius: 10px;
        color: #FFFFFF;
        margin-left: 87px;


        }

        /deep/ .el-form-item__content {
            margin-left: 0 !important;
            height: 100%;
            line-height: 37px;
        }
    }

    .status {
        width: 220px;
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
.rigisrispan{
    color: #094572;
    cursor: pointer;
}
.rigisright{
    margin-left: 63px;
    color: #094572;
    cursor: pointer;
}
/deep/.el-form-item__error{
    margin-left: -30px;
}
</style>