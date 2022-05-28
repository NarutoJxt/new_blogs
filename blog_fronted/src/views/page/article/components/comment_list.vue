<template>
  <div class="items">
      <ul style="padding-left: 0">
        <li v-for="(item,index) in headers" :key="index">
          <div class="item">
            <div class="item-header">
              <el-avatar :size="50" class="avatar" :src="transImageUrl(item.author.avatar)">
              </el-avatar>
              <div class="comment-author-info">
                <a style="font-size: 20px">{{ trnasUsername(item.author.username,0,30) }}</a>
                <div style="margin-top: 10px">
                  {{ transDatetime(item.pub_time) }}
                </div>
              </div>
            </div>
            <div class="item-body">
              <p>{{item.body}}</p>
            </div>
            <div class="item-footer">
              <div @click="item.showComment = true">
                <img class="comment-compliment-icon" :src="require('@/assets/img/detail/bigcomment.png')">
                <span>
                  回复
                </span>
              </div>

              <div class="delete-button" v-if="item.autho.idr === user.id" >
                    <el-popconfirm
                        title="确认删除？？"
                        @confirm="deleteComment(item.id)"
                    >
                      <el-button style="border: none;" :plain="true"
                                 icon="el-icon-delete-solid" slot="reference"
                      >删除</el-button>
                    </el-popconfirm>
                  </div>
            </div>
          </div>
          <div class="line-wider">
          </div>
          <comment-form :article-id="articleId" @showCommentForm="showCommentForm" v-show="item.showComment"
                            style="margin-bottom: 30px"  :commentId="item.id">
          </comment-form>
          <comment-list :user="user" @refreshData="refreshData" :headers="comments[item.id]" :article-id="articleId" :comments="comments">
          </comment-list>
        </li>
      </ul>
    </div>

</template>

<script>
import {transDatetime, transImageUrl, trnasUsername} from "../../../../utils/func_methords";
import CommentForm from "./comment_form";
import {createComplimentForComment, deleteComment, deleteComplimentForComment} from "../../../../api/blog";

export default {
  name: "comment-list",
  components:{CommentForm},
  props:{
    headers:{
      type:Array,
      default:()=>{
        return []
      }
    },
    user:{
      type:Object,
      default:()=>{
        return {}
      }
    },
    articleId:{
      type:Number,
      default:-1
    },
    comments:{
      type:Object,
      default: ()=>{
        return {}
      }
    }
  },

  methods:{
    transImageUrl(url) {
      return transImageUrl(url)
    },
    transDatetime(datetime) {
      return transDatetime(datetime)
    },
    trnasUsername(username,start,end){
    return trnasUsername(username,start,end)
    },
    refreshData(){
      this.$emit("refreshData")
    },
        deleteComment(comment_id=null){
      let params = {
        id:comment_id
      }
      deleteComment(params).then(()=>{
        this.$message.success(
            {
              type:"success",
              message:"评论删除成功"
            }
        )
        this.$emit("refreshData")

      }).catch((error)=>{
        console.log(error)
        this.$message.error(
            {
              type:"error",
              message:"评论删除失败"
            }
        )
      })
    },
    createComplimentForComment(id){
      var params = {
        comment:id
      }
      createComplimentForComment(params).then((response)=>{
        console.log(response)
      })
    },
    deleteComplimentForComment(id){
      var params = {
             comment:id
      }
      deleteComplimentForComment(params).then((response)=>{
        console.log(response)
      })
    },
    showCommentForm(id,res){
      for(let i=0;i<this.headers.length;i++){
        if(this.headers[i].id == id){
          this.headers[i].showComment = res
        }
        this.$emit("refreshData")
      }
    },
  }
}
</script>

<style scoped>
.comment-author-info {
  display: flex;
  flex-direction: column;
  margin-left: 10px;
  justify-content: flex-start;
}
.item ul{
  padding-left: 0;
}
.item-footer{
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}
.line-wider {
  width: 100%;
  margin-top: 20px;
  margin-bottom: 20px;
  height: 1px;
  background-color: #eee;
}
.el-button{
  height: 28px;
  font-size: 18px;
}
.delete-button{
  position: relative;
  bottom: 4px;
}
.item {
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
}
.comment-compliment-icon{
  position: relative;
  top: 4px;
}
.item-header {
  position: relative;
  right: 10%;
  display: flex;
  flex-direction: row;
  width: 90%;
}
.item-header,.item-body,.item-footer{
    margin-bottom: 5px;
}
.item-body{
  font-size: 20px;
  line-height: 1.5;
  color: gray;
  font-family: -apple-system,BlinkMacSystemFont,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei","Helvetica Neue",Helvetica,Arial,sans-serif;
}
</style>