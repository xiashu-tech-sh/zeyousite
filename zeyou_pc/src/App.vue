<template>
  <div id="app">
    <router-view />
  </div>
</template>

<style lang="less">
.el-message--warning {
    background-color: #fff;
    border-color: #094572;
}
.el-message--warning .el-message__content {
    color: #094572;
    background-color: #fff;
}
.el-icon-success:before,
.el-icon-warning:before{
color: #094572;
}
.el-message--success .el-message__content {
    color: #094572;
    border-color: #094572;
}
* {
  padding: 0;
  margin: 0;
}

.el-button {
  background: #094572;
  color: #fff;
}
.el-button:focus,
.el-button:hover {
  background: #094572;
  border-color: #271849;
  color: #fff;
}
.el-button + .el-button {
  margin-left: 139px;
}
/* 灰色背景容器 */
.styinfor {
  margin-top: 40px;
  margin-bottom: 40px;
}
.one_label {
  margin-top: 50px;
  color: rgb(141, 138, 138);
}
/* 文本框 */
.el-form-item__label {
  width: 135px;
  height: 30px;
  color: rgb(141, 138, 138);
}
.el-input__inner {
  width: 220px;
  border-radius: 10px;
  margin-left: 30px;
}
.one_a {
  color: rgb(141, 138, 138);
  cursor: pointer;
}
.two_a {
  color: #fff;
  text-decoration: none;
  margin-left: 11px;
  line-height: 40px;
}
/* 设置显示栏容器 */
.datashow {
  width: 1200px;
  margin: 0 auto;
  border: solid #094572 1px;
  border-radius: 10px;
}
.el-input__icon {
  margin-left: 30px;
}
/* 头标签 */
.datahead {
  height: 40px;
  background-color: #094572;
  border-radius: 10px;
  border: none;
}
/* 部分标签位置调整 */
.el-select__tags {
  margin-left: 30px;
}
.el-form-item__error {
  margin-left: 30px;
}

.el-pagination.is-background .el-pager li:not(.disabled).active {
  background-color: #094572;
}
.el-dialog__body {
  word-break: break-word;
}
video {
  width: auto;
  max-height: 100%;
}

.el-link.el-link--default:hover {
  color: #094572;
}

.el-link.is-underline:hover:after {
  border-bottom: 1px solid #094572;
}
.el-checkbox__input.is-checked .el-checkbox__inner,
.el-checkbox__input.is-indeterminate .el-checkbox__inner {
  background-color: #094572;
  border-color: #094572;
}

.addBtnBox {
  display: flex;

  /deep/ .el-form-item__content {
    margin-left: 0 !important;
    justify-content: space-between;
  }

  .addCartBtn {
    width: 238px !important;
    height: 78px !important;
    margin-left: 0 !important;
    margin-right: 38px;
  }

  .editCartBtn.addCartBtn {
    width: auto !important;
    height: 78px !important;
    margin-left: 0 !important;
    margin-right: 38px;
  }

  .addCartBtn:first-child {
    margin-right: 0;
  }
}

.el-textarea .el-textarea__inner {
  // 然后找到对应的类名，在这里将拉伸去掉即可
  resize: none;
}

.el-dropdown-menu {
  .el-button--text {
    width: 100% !important;
    text-align: left !important;
  }
}

.install_class.colors {
  background-color: #fff !important;
}

.main {
  flex-grow: 1;
}

.el-tooltip__popper {
  width: 400px;
  // height: 200px;
  font-size: 13px;
  font-family: "Microsoft YaHei";
  // text-indent: 2em;
  line-height: 22px;
}

.el-icon-diy-Success123 {
  color: #094572 !important;
  font-size: 26px !important;
  margin-right: 8px;
}

.el-icon-diy-warning123 {
  color: #094572 !important;
  font-size: 30px !important;
  margin-right: 8px;
}

.el-message {
  p {
    font-size: 18px !important;
    color: #094572;
  }
}

#app {
  // min-width: 1900px;
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  // text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}

.el-textarea {
  // border: 4px solid #cdcdcd;
  .el-textarea__inner {
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #ffffff;
    border-radius: 10px;
    font-size: 12px;
    font-family: Microsoft YaHei;
    font-weight: 400;
    border: 4px solid #094572;
    color: #094572;
    width: 338px;
  }
}

.el-textarea__inner:focus {
  border: 4px solid #094572;
}

.el-radio-button__orig-radio:checked + .el-radio-button__inner {
  box-shadow: none !important;
}
</style>