import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views'
import {getToken} from "../utils/cache";
import backendLayout from "@/views/edit/index"
const WHITE_LIST = ["/register","/login"]
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'login',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/account/index')
  },
  {
    path:"/edit",
    name:"edit",
    component: backendLayout,
    redirect:"/edit",
    children:[
      {
        path:"/edit",
        name:"edit",
        component:() => import("../views/edit/components/edit")
      }
    ]
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})
router.beforeEach((to, from, next) => {
  var token = getToken()
  if(token){
    if (WHITE_LIST.indexOf(to.path) === -1) {
      next()
    } else {
      next("/")
    }
    next()
  }else {
    if (WHITE_LIST.indexOf(to.path) === -1) {
      next("/login")
    } else {
      next()
    }
  }
})
export default router