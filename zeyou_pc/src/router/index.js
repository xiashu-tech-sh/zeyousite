import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home";
import Login from "../views/Users/Login";
import Register from "../views/Users/Register";
import EditPassword from "../views/Users/EditPassword";
import PersonalCenter from "../views/Users/PersonalCenter";
import EmployeeInfor from "../views/Users/EmployeeInfor";
import SuperPersona from "../views/Users/SuperPersona";
import SuperRegiste from "../views/Users/SuperRegiste";
import MarkeInform from "../views/Academies/MarkeInform"
import AcademicInfor from "../views/Academies/AcademicInfor";
import InformationMaster from "../views/Stutens/InformationMaster";
import Customer from "../views/Stutens/Customer";
import AddData from "../views/Stutens/AddData";
import ProductPush from "../views/Recommended/ProductPush";
import StudentPush from "../views/Recommended/StudentPush"
import DataAnalysis from "../views/Analysis/DataAnalysis"
import ResourceAnalysis from "../views/Analysis/ResourceAnalysis"
import AfterBuyingRate from "../views/Analysis/AfterBuyingRate"
import PersonnelSales from "../views/Analysis/PersonnelSales"
import CustomerContract from "../views/Analysis/CustomerContract"
import CustomerConversion from "../views/Analysis/CustomerConversion"
import ProductsToBuy from "../views/Analysis/ProductsToBuy"
Vue.use(VueRouter)

const routes = [
  {
    path: "/",
    redirect: "/login",
    // alias: '/111',
    // name: "index",
    // component: index
  },
  {
    path: "/login",
    name: "login",
    component: Login,
  },
  {
    path: "/register",
    name: "register",
    component: Register,
  },
  {
    path: "/importdata",
    name: "home",
    component: Home,
    // redirect: '/',
    children: [
      {
        path: "/editPassword",
        name: "editPassword",
        component: EditPassword,
      },
      {
        path: "/academicinfor",
        name: "academicinfor",
        component: AcademicInfor,
      },
      {
        path: "/informationmaster",
        name: "informationmaster",
        component: InformationMaster,
      },
      {
        path: "/customer",
        name: "customer",
        component: Customer,
      },
      {
        path: "/adddata",
        name: "AddData",
        component: AddData,
      },
      {
        path: "/personalcenter",
        name: "personalcenter",
        component: PersonalCenter,
      },
      {
        path: "/employeeinfor",
        name: "employeeinfor",
        component: EmployeeInfor,
      },
      {
        path: "/superPersona",
        name: "superPersona",
        component: SuperPersona,
      },
      {
        path: "/superregiste",
        name: "superregiste",
        component: SuperRegiste,
      },
      {
        path: "/markeinform",
        name: "markeinform",
        component: MarkeInform,
      },
      {
        path: "/studentpush",
        name: "studentpush",
        component: StudentPush,
      },
      {
        path: "/productpush",
        name: "productpush",
        component: ProductPush,
      },
      {
        path: "/dataanalysis",
        name: "dataanalysis",
        component: DataAnalysis,
        children:[
          {
            path: "/resourceanalysis",
            name: "resourceanalysis",
            component: ResourceAnalysis,
          },
          {
            path: "/afterbuyingrate",
            name: "afterbuyingrate",
            component: AfterBuyingRate,
          },
          {
            path: "/personnelsales",
            name: "personnelsales",
            component: PersonnelSales,
          },
          {
            path: "/customercontract",
            name: "customercontract",
            component: CustomerContract,
          },
          {
            path: "/customerconversion",
            name: "customerconversion",
            component: CustomerConversion,
          },
          {
            path: "/productstobuy",
            name: "productstobuy",
            component: ProductsToBuy,
          },
        ]
      },
    ],
  },
];

const router = new VueRouter({
  mode: "history",
  routes,
});

export default router;
