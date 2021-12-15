import Vue from "vue";
import ElementUI from "element-ui";
import "element-ui/lib/theme-chalk/index.css";
import { Loading } from "element-ui";
import router from "./router";
import store from "./store";
import axios from "axios";
import BaiduMap from "vue-baidu-map";
import App from "./App.vue";
// import BASE_URL from "../public/park_BASE_URL"; //配置全局URL
import Viewer from "v-viewer";
import "viewerjs/dist/viewer.css";
import scroll from "vue-seamless-scroll";
//mian.js中：
import "vue-googlemaps/dist/vue-googlemaps.css";
//导入表格
// import vueXlsxTable from 'vue-xlsx-table'
// Vue.use(vueXlsxTable, {rABS: false})
//导出表格
import JsonExcel from "vue-json-excel";

Vue.component("downloadExcel", JsonExcel);

Vue.use(Viewer);
Vue.use(scroll);

Viewer.setDefaults({
  Options: {
    inline: true,
    button: true,
    navbar: true,
    title: true,
    toolbar: true,
    tooltip: true,
    movable: true,
    zoomable: true,
    rotatable: true,
    scalable: true,
    transition: true,
    fullscreen: true,
    keyboard: true,
    url: "data-source",
  },
});
Vue.prototype.$ajax = axios;

Vue.prototype.comExportToExcel = (ref, mapHeader, excelTitle) => {
  let res = ref.tableData;
  let tHeader = mapHeader;
  let filterVal = ref.children;
  require.ensure([], () => {
    const { export_json_to_excel } = require("./utils/Export2Excel");
    const list = res;
    const data = formatJson(filterVal, list);
    export_json_to_excel(tHeader, data, excelTitle);
  });
  function getNowDateTime() {
    let now = new Date();
    var Y = now.getFullYear() + "";
    var M =
      (now.getMonth() + 1 < 10
        ? "0" + (now.getMonth() + 1)
        : now.getMonth() + 1) + "";
    var D = (now.getDate() < 10 ? "0" + now.getDate() : now.getDate()) + "";
    var h = (now.getHours() < 10 ? "0" + now.getHours() : now.getHours()) + "";
    var m =
      (now.getMinutes() < 10 ? "0" + now.getMinutes() : now.getMinutes()) + "";
    var s = now.getSeconds() < 10 ? "0" + now.getSeconds() : now.getSeconds();
    var newDate = Y + M + D + h + m + s;
    return newDate;
  }
  function formatJson(filterVal, jsonData) {
    return jsonData.map((v) => filterVal.map((j) => v[j]));
  }
};

axios.defaults.baseURL = "http://47.100.79.150:8000"; //设置全局URL
// axios.defaults.baseURL = "http://127.0.0.1:8000"; //设置全局URL

axios.defaults.headers.post["Content-Type"] = "application/json";
import acc from "./App"; //引用文件
Vue.prototype.GLOBAL = acc;

Vue.filter("splitName", function(value) {
  if (value) {
    // return value.split("\n")[0];
    var toFixedNum = Number(value).toFixed(3);
    var realVal = toFixedNum.substring(0, toFixedNum.toString().length - 1);
    return realVal;
  }
});

// router.beforeEach((to, from, next) => {
//   let token = window.sessionStorage.getItem("authentication");
//   if (token || to.path === "/login") {
//     next();
//   } else {
//     next("/login");
//   }
// });

Vue.use(ElementUI);

Vue.use(BaiduMap, {
  ak: "5HDI034i4pHKSRVLkbXWBHe6PahxcfnV", //这个地方是官方提供的ak密钥
});

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount("#app");
