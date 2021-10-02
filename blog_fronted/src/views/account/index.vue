<template>
<div class="body">
  <div class="login_box">

      <ul class="form-header">
        <li @click="formName = 'login'">
          <h1 :class="[formName=='login'?'form-active-h1':'form-inactive-h1']">登录</h1>
        </li>
        <li  @click="formName = 'register'">
          <h1 :class="[formName=='register'?'form-active-h1':'form-inactive-h1']">注册</h1>
        </li>
      </ul>
    <component :is="component" ></component>
    </div>
</div>
</template>

<script>
import LoginForm from "./loginForm";
import RegisterForm from "./registerForm";
export default {
name: "login",
  components:{LoginForm,RegisterForm},
data(){
  return {
    formName:"login",
    component:LoginForm
  }
},
  watch:{
    formName(val){
      this.component = val === "login"?LoginForm:RegisterForm
    }
  }
}
</script>

<style scoped>
.body{
  background-image: url("../../assets/img/login/background1.jpg");
  width: 100%;
  height: 100%;
  position:absolute;
 top:0;
  left:0;
  background-size:cover;
  background-attachment:fixed;
  background-repeat: no-repeat;
   -webkit-background-size: cover;/* 兼容Webkit内核浏览器如Chrome和Safari */
   -o-background-size: cover;/* 兼容Opera */
    zoom: 1;
  padding: 0;
  margin: 0;
    opacity: 1;
}
.login_box {
  width: 350px;
  height: 500px;
  background: #fff;
  border-radius: 3px;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}
.login_form {
  position: relative;
  bottom: 0;
  width: 100%;
  padding: 0 20px;
  box-sizing: border-box;
}
.btns {
  display: flex;
  justify-content: flex-end;
}


.third-party{
  position: relative;
  top: -20px;
}
.third-party-link{
  margin-left: 10px;
}
.form-header{
  position: relative;
  right: 20px;
}
.form-header>li{
  display: inline-block;
}
.form-active-h1{
  border-bottom: coral;
  border-bottom-style: solid;
  color: coral;
}
.form-inactive-h1{
  border: none;
}
.form-header>li:first-child{
  margin-right: 20px;
}
</style>