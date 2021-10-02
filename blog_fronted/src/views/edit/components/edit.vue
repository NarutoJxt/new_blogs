<template>
  <div id="editor">
    <el-form v-if="article" class="editor-form" :rules="rules" :model="blogForm" ref="blogForm">
      <el-form-item prop="title">
        <el-input type="text" placeholder="请输入文章标题" v-model="blogForm.title">
        </el-input>
      </el-form-item>
      <el-form-item prop="content">
        <div class="mavonEditor">
          <mavon-editor
              @save="submitForm"
              style="height: 700px"
              toolbarsBackground="lightgrey"
              v-model="blogForm.body"/>
        </div>
      </el-form-item>
      <el-input type="hidden" v-model="blogForm.category"></el-input>
    </el-form>
    >
  </div>
</template>

<script>
import {createBlog, updateBlog} from "../../../api/blog";

export default {
  name: "Editor",
  props:{
    article:{
      type:Object,
      default:()=>{return {}},
    }
  },
  data() {
    return {
      text: "ahahh",
      height: 1000,
      blogForm: {
        id:"",
        title: "",
        body: "",
        status: "d",
        category:""
      },
      rules: {
        title: [
          {required: true, message: '请输入文章标题', trigger: 'blur'},
          {min: 1, max: 255, message: '长度在 1 到 255 个字符', trigger: 'blur'}
        ]
      }
    }
  },
  mounted() {
    if(this.article){
          this.blogForm.title = this.article.title
    this.blogForm.body = this.article.body
    this.blogForm.status = this.article.status
    this.blogForm.category = this.article.category
    this.blogForm.id = this.article.id
    }

  },
  methods: {
    changeArticle(article){
      if(article){
        this.blogForm.title = article.title
        this.blogForm.body = article.body
        this.blogForm.status = article.status
        this.blogForm.category = article.category
          this.blogForm.id = article.id
      }
    },
    submitForm() {
      this.$refs["blogForm"].validate((valid) => {
        if (valid) {
          if(this.blogForm.id){
            updateBlog(this.blogForm).then((response)=>{
            this.$message.success(
                {
                  type:"success",
                  message:"修改成功"
                }
            )
            this.$emit("update",response.data)
            }).catch((error)=>{
              console.log(error)
              this.$message.error(
                {
                  type:"error",
                  message:"修改失败"
                }
            )
            })
          }else{
            this.blogForm.status = "d"
          createBlog(this.blogForm).then((response)=>{
            this.$message.success(
                {
                  type:"success",
                  message:"保存成功"
                }
            )
            this.$emit("save",null,response.data)
          }).catch(()=>{
            this.$message.error(
                {
                  type:"error",
                  message:"保存失败"
                }
            )
          })}

        } else {
          return false;
        }
      });
    }
  },
}
</script>

<style scoped>
#editor {
  width: 100%;
  margin-top: 30px;
}

.mavonEditor {
  width: 100%;
  height: 100%;
}
</style>