<template>
    <div class="app">
        <div class="login-box">
            <div class="title">
                <img src="../../assets/logo.png" alt="">
            </div>
            <el-form :model="formObj" :rules="rules" ref="formObj" class="formObj">
                <div class="form-in">
                    <img src="../../assets/email.png" class="email_img"><input type="text" placeholder="请输入邮箱" v-model="formObj.email">
                    <span class="veri" @click="sendCodeFn()" >获取验证码</span>
                </div>
                <div class="form-in">
                    <img src="../../assets/verificationcode.png" class="input_img"><input type="text" placeholder="请输入验证码" v-model="formObj.code">
                </div>
                <div class="form-in">
                    <img src="../../assets/pawd.png" class="input_img" ><input type="password" placeholder="请再次输入新密码" autocomplete="new-password" v-model="formObj.password1">
                </div>
                <div class="form-in">
                    <img src="../../assets/pawd.png" class="input_img"><input type="password" placeholder="请再次输入新密码" autocomplete="new-password" v-model="formObj.password2">
                </div>    
                <div class="btns">
                    <el-form-item>
                        <el-button @click="editPasswordFn('formObj')">确认修改 </el-button>
                    </el-form-item>
                </div>
                <div class="status clearfix">
                    <span class="editpaww" @click="tologinFn()">已有账户?去登录</span>
                </div>
            </el-form>
        </div>
    </div>
</template>

<script>
    import dragVerify from 'vue-drag-verify'

    export default {
        data() {
            return {
                rules: {

                },
                formObj: {
                    email: '',
                    code: '',
                    password1: '',
                    password2: '',
                },
            }
        },
        components: {
            dragVerify
        },
        mounted () {
            document.body.scrollTop = document.documentElement.scrollTop = 0;
        },
        methods: {
            tologinFn(){
            this.$router.push("/login")
                },
            editPasswordFn(formObj) {
                this.$refs[formObj].validate(async (valid) => {
                    if (valid) {
                        if (!this.formObj.email) {
                            this.$message({
                                type: 'warning',
                                message: "请输入邮箱"
                            })
                            return;
                        }
                        var reg=/^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
                        if(!reg.test(this.formObj.email)){
                            this.$message({
                                type: 'warning',
                                message: "邮箱格式错误"
                            });
                            return;
                        }
                        var reg_code=/^\d{6}$/
                        if (!reg_code.test(this.formObj.code)) {
                            this.$message({
                                type: 'warning',
                                message: "请输入6位数验证码"
                            })
                            return;
                        }
                        if (!this.formObj.password1) {
                            this.$message({
                                type: 'warning',
                                message: "新密码不能为空"
                            })
                            return;
                        }
                        if (!this.formObj.password2) {
                            this.$message({
                                type: 'warning',
                                message: "确认密码不能为空"
                            })
                            return;
                        }                        
                        if (this.formObj.password1 != this.formObj.password2) {
                            this.$message({
                                type: "warning",
                                message: "两次密码输入不一致"
                            })
                            return;
                        }
                        const res = await this.$ajax.post(`/email_password/`, {
                            email: this.formObj.email,
                            sms_code: this.formObj.code,
                            password: this.formObj.password1,
                            confirm_password: this.formObj.password2,
                        });
                        if (res.data.status == 200) {
                            this.$message({
                                type: "success",
                                message: res.data.message
                            })
                            window.sessionStorage.removeItem('_mainObj');
                            window.sessionStorage.removeItem('authentication');
                            window.sessionStorage.removeItem('user_id');
                            window.sessionStorage.removeItem('user_identity');
                            this.$router.push("/login");
                            location.reload();
                        } else {
                            this.$message({
                                type: "warning",
                                message: res.data.message
                            })
                        }
                    } else {
                        return false;
                    }
                });
            },
            async sendCodeFn() {
                var reg=/^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
                if(!reg.test(this.formObj.email)){
                    this.$message({
                        type: 'warning',
                        message: "邮箱格式错误"
                    });
                    return;
                }
                const res = await this.$ajax.post(`/sms_code/`, {
                    email: this.formObj.email,
                });
                console.log(res)
                if (res.data.status == 200) {
                    this.$message({
                        type: "success",
                        message: res.data.message
                    });
                } else {
                    this.$message({
                        type: "warning",
                        message: res.data.message
                    })
                }
            }
        },
    }
   
</script>

<style lang="less" scoped>
    .btns {
        padding-top: 40px;
        .el-button {
        letter-spacing: 10px;
        width:  220px;
        height: 36px;
        font-size: 18px;
        background-color: #094572;
        border: none;
        border-radius: 10px;
        color: #FFFFFF;
        margin-left: 90px;


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
        margin-top: -15px;

        .left {
            cursor: pointer;
        }

        .right {
            cursor: pointer;
        }
    }
/* 白色框样式 */
.login-box{
    float: right;
    width: 400px;
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
/* 输入框图标样式 */
.input_img{
    margin-top: 18px;
}
.email_img{
    margin-left: 0px;
    margin-top: 18px;
}
.formObj{
    margin-top: 30px;
}
/* 验证码样式 */
.form-in .veri{
    width: 20px;
    height: 20px;
    margin-top:30px;
    line-height: 20px;
    letter-spacing: 1px;
    cursor: pointer;
    font-size: 12px;
    margin-left: -50px;
    background-color: #fff;
    color: #76777e;
    border: solid 1px #7F92DA;
}
input::placeholder{
    color: #094572;
}
.form-in{
    width: 220px;
    border: solid 1px #094572;
    border-color: #656668;
    border-top-width: 0px;
    border-right-width: 0px;
    border-bottom-width: 1px;
    border-left-width: 0px;
    margin: 0 auto;
    margin-top: 10px;
}
/* 登录输入框样式 */
.form-in input{
    margin-left: 10px;
    margin-top: 4px;
    border-top-width: 0px;
    border-right-width: 0px;
    border-bottom-width: 1px;
    border-left-width: 0px;
    outline: none;
    color: #094572;
}
.editpaww{
    color: #094572;
    cursor: pointer;
}
</style>