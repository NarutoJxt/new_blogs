<template>
    <el-form ref="login" :rules="rules" :model="loginForm" class="login_form" label-width="0px">
      <el-form-item prop="username">
        <el-input  v-model="loginForm.username" placeholder="用户名" type="text"></el-input>
      </el-form-item>
      <el-form-item prop="password">
        <el-input  v-model="loginForm.password" type="password" placeholder="选择时间" style="width: 100%;"></el-input>
      </el-form-item>
        <el-form-item class="btns">
          <el-button class="login-btn" type="primary" @click="submitForm">登录</el-button>
        </el-form-item>
        <el-form-item class="btns">
          <el-link :underline="false" class="register-link" href="/register">注册</el-link>
          <el-link :underline="false" class="forget-password-link" href="#">忘记密码</el-link>
        </el-form-item>
        <el-form-item class="third-party">

          <el-link :underline="false" class="third-party-link" :href="getOauthURL('github')" ><img src="../../assets/img/login/github.png"/></el-link>
          <el-link :underline="false" class="third-party-link" :href="getOauthURL('google')"><img src="../../assets/img/login/google.png" /></el-link>
        </el-form-item>
      </el-form>

</template>

<script>
import {login} from "@/api/account/";
import {mapMutations} from "vuex";
import {base_url} from "../../api/settings";

export default {
name: "loginForm",
  data(){
  return {
    loginForm: {
      username: '',
      password: ''
    },
    loginError:{
      usernameError:"",
      passwordError:"",
    },
    rules:{
      username:[
        {required:true,message:"用户名是必须的",trigger:'blur'},
        {min:8,max:62,message: "用户名长度为8-64个字符",trigger: "blur"}
      ],
      password:[
        {required:true,message:"密码是必须的",trigger:'blur'},
      ]
    }
  }
  },
  methods:{
    getOauthURL(type){
        return base_url + "login/"+type+"/"
    },
      submitForm(){
        this.$refs["login"].validate((valid) => {
          if (valid) {
            login(this.loginForm).then((response)=>{
              let  {data} = response
              var token = data.token
              var user_info = data.user
              this.setUserInfo(user_info)
              this.setToken(token)
              this.$router.push("/")
            }).catch((errors)=>{
              console.log(errors)
              var error = errors.response.data
              this.loginError.usernameError = error.username ? error.username[0]:""
              this.loginError.passwordError = error.password ? error.password[0]:""
            })
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
      ...mapMutations("login",{
        "setToken":"SET_TOKEN",
        "setUserInfo":"SET_USER_INFO"
      })
  }
}
</script>

<style scoped>
.login-btn{
  width: 310px;
  border-radius: 20px;
  border-style: dotted;
}
.register-link{
  position: relative;
  right: 100px;
  top: -20px;
}
.forget-password-link{
  position: relative;
  left: 100px;
  top: -20px;
}
</style>