<template>
  <el-container>
    <el-header>
      <div class="header">
        <ul class="header-title">
          <li>
            <a class="logo">笔映</a>
          </li>
          <li>
            <a href="/index" class="header-link">
            首页
          </a>
          </li>
          <li>发现</li>
          <li>
            <a href="/attention" class="header-link">
              关注
            </a>
          </li>
          <li>消息</li>
          <li>
            <input
                placeholder="搜索"
                suffix-icon="el-icon-search"
                class="search-input"
            />
          </li>
          <li>
            <el-dropdown class="dropdown" >
              <img width="60px" height="60px" style="border-radius: 50%;position: relative;bottom: 20px" src="../assets/header/avatar.jpeg">
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item split-button icon="el-icon-plus" @click="getUserPage()">
                  我的主页 </el-dropdown-item>
                <el-dropdown-item icon="el-icon-circle-plus">狮子头</el-dropdown-item>
                <el-dropdown-item icon="el-icon-circle-plus-outline">螺蛳粉</el-dropdown-item>
                <el-dropdown-item icon="el-icon-check">双皮奶</el-dropdown-item>
                <el-dropdown-item icon="el-icon-circle-check" ><a @click="logout">注销</a></el-dropdown-item>
              </el-dropdown-menu>
    </el-dropdown>
          </li>
          <li>
            <a class="write-btn" href="/edit">
                写文档
            </a>
          </li>
        </ul>
      </div>
    </el-header>
    <el-main style="margin-top: 10px">
      <router-view/>
      <router-view style="background-color: #f9f9f9;" name="detail"/>
    </el-main>
  </el-container>
</template>

<script>
// @ is an alias to /src

import {mapMutations} from "vuex";
import {logout} from "../api/account";
import { base_url } from '../api/settings';

export default {
  name: 'Home',
  data(){
   return { user:{} }
  },
  mounted(){
    this.$nextTick(this.getUserInfo())
  },
  methods:{
    logout(){
      logout().then((response)=>{
        console.log(response)
        this.setToken("")
        this.$router.push("login")
      }).catch((error)=>{
        console.log(error)
        this.$message.error("注销失败")
      })
    },
    ...mapMutations("login",{
        "setToken":"SET_TOKEN",
        "getUserInfo": "GET_USER_INFO",
      })
  },
  watch:{
    user:function(newVal){
      this.userUrl = base_url + "person/" + newVal.id
    }
  }
}
</script>
<style scoped>
.header {
  position: fixed;
  top: 0;
  display: block;
  height: 10%;
  width: 100%;
  background: white;
  border-bottom: black;
  border-bottom-width: 1px;
  border-bottom-style: dotted;
  z-index: 3;
}

.write-btn{
  width:150px;
  height: 40px;
  font-size: 18px;
  background-color: coral;
  color: white;
  border-radius: 50px;
  padding: 5px 5px 0 5px;
  position: absolute;
}
.header-title li {
  list-style: none;
  width: 100px;
  float: left;
  font-size: 25px;
  margin: 0 20px;
  padding: 10px;
}

.header-title li:first-child {
  padding: 0;
}
.header-link{
  color: black;
  text-decoration-line: none;
}
.dropdown{
  position: absolute;right: 5%;top: 20px
}
.logo {
  color: coral;
  font-size: 40px;
  margin: 0;
}

.search-input {
  width: 300px;
  border-radius: 20px;
  height: 40px;
  padding-left: 15px;
  border-style: dotted;
  border: none;
  background-color: #F5F5F5;
  outline: none;
}

</style>
