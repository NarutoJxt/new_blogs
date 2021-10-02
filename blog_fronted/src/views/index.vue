<template>
  <el-container>
    <el-header>
      <div class="header">
        <ul class="header-title">
          <li>
            <a class="logo">笔映</a>
          </li>
          <li>首页</li>
          <li>发现</li>
          <li>关注</li>
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
              <img width="60px" height="60px" style="border-radius: 50%;margin: 0px 24px 0px 16px" src="../assets/header/avatar.jpeg">
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item icon="el-icon-plus">黄金糕</el-dropdown-item>
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
    <el-main>
      <router-view/>
    </el-main>
    <el-footer>
    </el-footer>
  </el-container>
</template>

<script>
// @ is an alias to /src

import {mapMutations} from "vuex";
import {logout} from "../api/account";

export default {
  name: 'Home',
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
      })
  }
}
</script>
<style scoped>
.header {
  position: fixed;
  display: block;
  top: 0;
  height: 20%;
  width: 100%;
}

.header-title {
  position: relative;
  bottom: 20px;
  height: 60px;
  border-bottom: black;
  border-bottom-width: 1px;
  border-bottom-style: dotted;
  padding: 10px 0 20px 0;
  vertical-align: middle;
}
.write-btn{
  width:150px;
  height: 50px;
  font-size: 20px;
  background-color: coral;
  color: white;
  border-radius: 50px;
  padding: 5px 5px 0 5px;
  position: absolute;
  right: 13%;
  bottom: 10%;
}
.header-title li {
  list-style: none;
  width: 100px;
  float: left;
  font-size: 30px;
  margin: 0 20px;
  padding: 10px;
}

.header-title li:first-child {
  padding: 0;
}
.dropdown{
  position: absolute;right: 5%;top: 20px
}
.logo {
  color: coral;
  font-size: 50px;
  margin: 0;
}

.search-input {
  width: 300px;
  border-radius: 20px;
  height: 60px;
  padding-left: 15px;
  border-style: dotted;
  border: none;
  background-color: #F5F5F5;
  outline: none;
}

</style>
