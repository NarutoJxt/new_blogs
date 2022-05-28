<template>
      <el-collapse-transition>

  <div class="comment-form">
      <div>
        <div class="input" @click="show=true">
          <textarea placeholder="请输入" class="input-textarea" v-model="commentContent">
          </textarea>
        </div>
        <div style="position: relative;left: 75%">
            <button class="circle-button-black-border-fill" @click="createComment">发布</button>
            <button class="circle-button-black-border" @click="showCommentForm(false)">取消</button>
          </div>
      </div>
  </div>
      </el-collapse-transition>

</template>

<script>
import {createComment} from "../../../../api/blog";

export default {
  name: "comment-form",
  props: {
    commentId: {
      type: Number,
      detail: null
    },
    articleId: {
      type: Number,
      detail: null
    }
  },

  data() {
    return {
      commentContent: "",
    }
  },
  methods: {
    createComment() {
      if(this.commentContent === ""){
        this.$message.info({
          type:"info",
          message:"评论内容不能为空"
        })
      }else{
            var params = {
        body: this.commentContent,
        article: this.articleId,
        parent_comment: this.commentId
      }
      createComment(params).then(() => {
        this.commentContent = ""
        this.showCommentForm(false,true)
        this.$message.success({
          type:"success",
          message:"评论发布成功"
        })
      }).catch(()=>{
        this.$message.error({
          tyoe:"error",
          message:"服务器异常，请稍后再试"
        }
      )
      })
      }
    },
    showCommentForm(res,type=false) {
      this.$emit("showCommentForm",this.commentId,res,type)
    }
  },

}
</script>

<style scoped>
.input {
  width: 90%;
  margin-bottom: 20px;
  position: relative;
  left: 20px;
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
}

.input-textarea {
  background-color: #f9f9f9;
  width: 100%;
  padding-left: 10px;
  border-width: 1px;
  border-color: lightgray;
  border-style: solid;
  outline: none;
  padding-top: 10px;
  height: 80px;
}

.circle-button-black-border-fill {
  color: white;
  background-color: #ef826d;
  border-color: #ef826d;
}

.circle-button-black-border, .circle-button-black-border-fill {
  border-radius: 50px;
  padding: 2px 9px;
  height: 40px;
  width: 70px;
  border-width: 1px;
  border-style: double;
}

.comment-form {
  margin-bottom: 30px;
}
</style>