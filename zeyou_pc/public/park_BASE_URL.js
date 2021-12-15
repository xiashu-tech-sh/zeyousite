
let BASE_URL = ""; //这里是一个默认的url，可以没有

if (process.env.NODE_ENV === "production") {
    // console.log("设置生产环境api接口url");
    BASE_URL = "www.bwshutters.com"; //生产环境url
} else if (process.env.NODE_ENV === "test") {
    // BASE_URL = "http://mg.test.yuanquwuyou.com/park/"; //测试环境url
} else {
    //dev 开发环境
    // console.log("开发环境api接口url");
    // BASE_URL = "http://localhost:8380/park/"; //开发环境url
    // BASE_URL = "http://47.100.79.150:8000/"; //开发环境url
    BASE_URL = "http://45.76.246.90:8000/"; //开发环境url
}
export default { BASE_URL };
