<template>
    <el-form  :show-message="true" ref="register" :model="registerForm" class="login_form" :rules="registerRules" label-width="0px">
      <el-form-item prop="username" :error="registerError.usernameError">
        <el-input  v-model="registerForm.username" placeholder="用户名" type="text"></el-input>
      </el-form-item>
      <el-form-item prop="email" :error="registerError.emailError">
        <el-input  v-model="registerForm.email" placeholder="邮箱" type="email" style="width: 100%;"></el-input>
      </el-form-item>
      <el-form-item prop="password" :error="registerError.passwordError">
        <el-input  v-model="registerForm.password" placeholder="邮箱" type="password" style="width: 100%;"></el-input>
      </el-form-item>
          <el-form-item prop="password1" :error="registerError.password11Error">
        <el-input v-model="registerForm.password1" type="password" placeholder="请再次输入密码" style="width: 100%;"></el-input>
      </el-form-item>
        <el-form-item class="btns">
          <el-button class="login-btn" type="primary" @click="submitForm">注册</el-button>
        </el-form-item>
      </el-form>

</template>

<script>
import {register} from "@/api/account/"
export default {
  name: "registerForm",
  data(){
  var validateEmail = (rule,value,callback) => {
    var regex = /^([0-9A-Za-z\-_.]+)@([0-9a-z]+\.[a-z]{2,3}(\.[a-z]{2})?)$/g;
    var res = regex.test( value )
    if(!res){
      callback(new Error("邮箱格式不合法"))
    }else {
      callback()
    }
  }
      var validatePass2 = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请再次输入密码'));
        } else if (value !== this.registerForm.password) {
          callback(new Error('两次输入密码不一致!'));
        } else {
          callback();
        }
      };
  return {
      // 登录表单的数据绑定对象
    registerForm:{
      username:"",
      email:"",
      password:"",
      password1:"",
    },
        registerError:{
      usernameError:"",
      emailError:"",
      passwordError:"",
      password11Error:"",
    },
    registerRules:{
      email:[
        {required:true,message:"邮箱是必选项",trigger:'blur'},
        {validator:validateEmail,trigger: 'blur'}
      ],
      username:[
        {required:true,message:"用户名是必须的",trigger:'blur'},
        {min:8,max:62,message: "用户名长度为8-64个字符",trigger: "blur"}
      ],
   password:[
        {required:true,message:"密码是必须的",trigger:'blur'},
        {min:8,max:62,message: "密码长度为8-64个字符",trigger: "blur"},
      ],
   password1:[
        {required:true,message:"密码是必须的",trigger:'blur'},
        {min:8,max:62,message: "密码长度为8-64个字符",trigger: "blur"},
     {validator:validatePass2,trigger: 'blur'}

      ],
    },
    formName:"login"
  }
 },

  methods:{
    submitForm(){
        this.$refs["register"].validate((valid) => {
          if (valid) {
            register(this.registerForm).then((response)=>{
              if(response) {
                this.$parent.formName = "login"
                this.$message.success("注册成功")
              }
            }).catch((errors)=>{
              var error = errors.response.data
              this.registerError.usernameError = error.username ? error.username[0]:""
              this.registerError.emailError = error.email ? error.email[0]:""
              this.registerError.passwordError = error.password ? error.password[0]:""
              this.registerError.password11Error = error.password1 ? error.password1[0]:""

            })
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },

  }
}
</script>

<style scoped>
.login-btn{
  width: 310px;
  border-radius: 20px;
  border-style: dotted;
}
</style>