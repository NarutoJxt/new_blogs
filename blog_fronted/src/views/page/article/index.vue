<template>
  <div class="detail-body">
    <div class="detail-left">
      <div v-if="isComplimented===1" class="compliment-icon" style="position: center" @click="praise(2)">
        <img src="../../../assets/img/detail/compliented.png" class="detail-icon"/>
      </div>
      <div v-else class="compliment-icon" style="position: center" @click="praise(1)">
        <img src="../../../assets/img/detail/uncompliment.png" class="detail-icon"/>
      </div>
      <div v-if="!isCollected" class="compliment-icon" @click="collectArticle(true)">
        <img src="../../../assets/img/detail/discollected.png" class="detail-icon"/>
      </div>
      <div v-else class="compliment-icon" @click="collectArticle(false)">
        <img src="../../../assets/img/detail/collected.png" class="detail-icon"/>
      </div>
    </div>
    <div class="detail-middle">
      <div class="article">
        <h1 class="article-title">{{ article.title }}</h1>
        <div class="article-header" style="position:relative;right: 50px">
          <el-avatar :size="60" style="margin-right: 20px" class="avatar" :src="author.avatar">
          </el-avatar>
          <div style="text-align: left">
            <a :href="'/person/'+author.id+'/'" style="font-size: 20px;font-weight: 2;line-height: 2;margin-right: 10px;color: black;text-decoration-line: none">{{
                author.username| slice(0,30)
              }}</a>
            <div class="annotation">
              {{ article.pub_time }} &nbsp;&nbsp; 字数：{{ article.body ? article.body.length : 0 }},&nbsp;&nbsp;
              阅读：{{ article.views }}
            </div>pkl
          </div>
          <div v-if="author.id !== user.id" style="position: relative;right: 170px">
              <button v-if="!isConcerned" class="circle-button" @click="concernedUser(true)">
              关注
            </button>
            <button v-else class="circle-button-fill" @click="concernedUser(false)"
                    @mouseover="text = '取消关注'"
                    @mouseleave="text = '已关注'"
            >
              <span style="width: 200px">{{ text }}</span>
            </button>
            </div>
        </div>
        <div class="article-body" v-html="convertMarkdownToHtml(article.body)" style="height: 100%">
        </div>
        <div class="article-footer">
          <div style="display: flex;flex-direction: row;justify-content: flex-start">
            <div v-if="isComplimented===1" class="footer-compliment-icon" style="position: center" @click="praise(2)">
              <img src="../../../assets/img/detail/compliented.png" class="detail-icon"/>
            </div>
            <div v-else class="footer-compliment-icon" @click="praise(1)">
              <img src="../../../assets/img/detail/uncompliment.png" class="detail-icon"/>
            </div>
            <div style="text-align: left;padding-top: 10px">
              有{{ complimentCount }}人点赞
            </div>
            <div v-if="isComplimented!==0" class="footer-compliment-icon" style="margin-left: 4px" @click="praise(0)">
              <img src="../../../assets/img/detail/undis.png" class="detail-icon"/>
            </div>
            <div v-else class="footer-compliment-icon" style="margin-left: 4px" @click="praise(2)">
              <img src="../../../assets/img/detail/dis.png" class="detail-icon"/>
            </div>
          </div>
          <div class="article-footer-right">
            <i class="el-icon-s-fold" style="font-size: 22px;"></i>
            <span style="font-size: 22px;padding-left: 5px">{{ category }}</span>
          </div>
        </div>
      </div>
      <div class="comment">
        <div class="comment-form">
          <div class="input" @click="show=true">
            <el-avatar :size='50' style="margin-right: 10px" :src="author.avatar">
            </el-avatar>
            <textarea placeholder="请输入" class="input-textarea" v-model="commentContent">
            </textarea>
          </div>
          <div style="float: right;margin-right: 30px">
            <el-collapse-transition>
              <div v-show="show">
                <button class="circle-button-black-border-fill" @click="createComment(null)">发布</button>
                <button class="circle-button-black-border" @click="show=false">取消</button>
              </div>
            </el-collapse-transition>
          </div>
        </div>
        <div class="comment-header">
          <span style="padding-left: 20px;font-size: 25px">全部评论</span>
        </div>
        <div class="comments">
          <ul style="padding-left: 40px">
            <li v-for="(item,index) in header" :key="index">
              <div class="comment-item">
                <div class="comment-item-header">
                  <el-avatar :size="50" class="avatar" :src="transImageUrl(item.author.avatar)">
                  </el-avatar>
                  <div class="comment-author-info">
                    <a style="font-size: 20px">{{ trnasUsername(item.author.username, 0, 30) }}</a>
                    <div style="margin-top: 10px">
                      {{ transDatetime(item.pub_time) }}
                    </div>
                  </div>
                </div>
                <div class="comment-item-body">
                  <p>{{ item.body }}</p>
                </div>
                <div class="comment-item-footer">
                  <diV class="comment-item-footer-left">
                    <div style="margin-right: 20px">
                      <img v-if="!checkCommentPraised(item)"
                           class="comment-compliment-icon"
                           :src="require('@/assets/img/detail/bigunpraise.png')"
                           @click="praiseForComment(true,item.id)">
                      <img v-else class="comment-compliment-icon"
                           :src="require('@/assets/img/detail/bigpraise.png')"
                           @click="praiseForComment(false,item.id)">
                      <span>
                {{ item.compliment_comments != 0 ? item.compliment_comments.length : "赞" }}
                  </span>
                    </div>
                    <div @click="item.showComment = true">
                      <img class="comment-compliment-icon" :src="require('@/assets/img/detail/bigcomment.png')">
                      <span>
                      回复
                    </span>
                    </div>
                  </diV>
                  <div class="delete-button" v-if="item.author.id === user.id" style="float: right">
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
              <comment-form :article-id="article.id" @showCommentForm="showCommentForm" v-show="item.showComment"
                            style="margin-bottom: 30px" :commentId="item.id">
              </comment-form>
              <comment-list :user="user" @refreshData="refreshData" style="margin-left: 80px" :headers="comments[item.id]"
                            :article-id="article.id" :comments="comments">
              </comment-list>
            </li>
          </ul>
        </div>
      </div>
    </div>
    <div style="float: right;margin-top: 11px;">
      <div class="author">
        <div class="author-header">
          <el-avatar :size='50' class="avatar" :src="author.avatar">
          </el-avatar>
          <div style="display: flex;flex-direction: column;justify-content: flex-start">
            <a style="text-align: left;padding-left: 10px;margin-top: 5px">{{ author.username | slice(0,30) }}</a>
            <div style="padding-left: 10px;padding-top: 5px">写55篇文章,有1人喜欢</div>
          </div>
          <div v-if="author.id !== user.id" style="float: right">
            <button v-if="!isConcerned" class="circle-button" @click="concernedUser(true)">
            关注
          </button>
          <button v-else class="circle-button-fill" @click="concernedUser(!false)"
                  @mouseover="text = '取消关注'"
                  @mouseleave="text = '已关注'"
          >
            <span style="width: 200px">{{ text }}</span>
          </button>
          </div>
        </div>
        <div class="line">
        </div>
        <div class="author-body">
          <ul class="article-list">
            <li v-for="(item,index) in authorArticle" :key="index" class="article-item">
              <a :href="'/article/detail/'+item.id+'/'" class="author-article-title">
                {{ item.title.length > 20 ? item.title.substring(0, 20) + "......" : item.title }}
              </a>
              <span class="article-reading-count">
                  阅读：{{ item.views }}
                </span>
            </li>
          </ul>
        </div>
      </div>
      <div class="recommended-article">
        <div class="recommended-article-header">
          <span style="padding-left: 10px;font-weight: 500;font-size: 25px">推荐阅读</span>
        </div>
        <ul class="article-list">
          <li v-for="(item,index) in authorArticle" :key="index" class="article-item">
            <a :href="'/article/detail/'+item.id+'/'" class="author-article-title">
              {{ item.title.length > 20 ? item.title.substring(1, 20) + "......" : item.title }}
            </a>
            <span class="article-reading-count">
                  阅读：{{ item.views }}
                </span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import {
  createCollection, createComment,
  createCompliment, createComplimentForComment,
  deleteCollection, deleteComment,
  deleteCompliment, deleteComplimentForComment,
  getArticleDetail
} from "../../../api/blog";
import {base_url} from "../../../api/settings";
import marked from 'marked';
import {cancelConcerned} from "../../../api/account";
import {transDatetime, transImageUrl, trnasUsername} from "../../../utils/func_methords";
import CommentList from "./components/comment_list";
import CommentForm from "./components/comment_form"
import {mapGetters} from "vuex";

export default {
  name: "index",
  components: {CommentForm, CommentList},
  props: {
    id: {
      type: [Number, String],
      default: 0
    }
  },
  data() {
    return {
      article: {},
      author: {},
      header: [],
      comments: [],
      complimentCount: 0,
      category: "",
      text: "已关注",
      commentContent: "",
      authorArticle: [],
      isConcerned: false,
      isComplimented: false,
      isCollected: false,
      show: false,
      user: {}
    }
  },
  created() {
    this.getArticleDetail()
    this.user = this.getUserInfo()
  },
  methods: {
    transImageUrl(url) {
      return transImageUrl(url)
    },
    transDatetime(datetime) {
      return transDatetime(datetime)
    },
    trnasUsername(username, start, end) {
      return trnasUsername(username, start, end)
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
        this.getArticleDetail()
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
    checkCommentPraised(item) {
      var that = this
      if (item.compliment_comments) {
        for (let i = 0; i < item.compliment_comments.length; i++)
          if (item.compliment_comments[i].blog_user == that.user.id) {
            return true
          }
      }
      return false
    },
    showCommentForm(id, res, type) {
      for (let i = 0; i < this.header.length; i++) {
        if (this.header[i].id == id) {
          this.header[i].showComment = res
        }
      }
      if (type) {
        this.getArticleDetail()
      }
    },
    refreshData() {
      this.getArticleDetail()
    },
    getArticleDetail() {
      var param = {
        "id": this.id
      }
      var that = this
      getArticleDetail(param).then((response) => {
        let data = JSON.parse(response.data)
        that.article = data.article
        that.author = data.author
        that.author.avatar = base_url.substring(0, base_url.length - 1) + that.author.avatar
        if (data.header) {
          for (let i = 0; i < data.header.length; i++) {
            data.header[i].showComment = false
          }
        }
        that.header = data.header
        that.comments = data.comments
        that.complimentCount = data.complimentCount
        that.article.pub_time = that.article.pub_time.split(".")[0].replace("T", " ")
        that.category = data.category
        that.authorArticle = data.authorArticle
        that.isConcerned = data.isConcerned
        that.isComplimented = data.isComplimented
        that.isCollected = data.isCollected
      })
    },
    createComment(parentComment = null, content = null) {
      if (!content) {
        content = this.commentContent
      }
      var params = {
        body: content,
        article: this.article.id,
        parent_comment: parentComment
      }
      console.log(params)
      createComment(params).then(() => {
        this.getArticleDetail()
        this.commentContent = ""
        this.show = false
        this.$message.success({
          type: "success",
          message: "评论发布成功"
        })
      }).catch(() => {
        this.$message.error({
              tyoe: "error",
              message: "服务器异常，请稍后再试"
            }
        )
      })
    },
    praise(value) {
      var params = {
        "article": this.article.id,
      }
      if (value !== 2) {
        params.praise_type = value
      }
      let func = value === 2 ? deleteCompliment : createCompliment
      func(params).then(() => {
        this.isComplimented = value
      }).catch((error) => {
        console.log(error)
        this.$message.error(
            {
              type: "error",
              message: "服务器异常"
            }
        )
      })
    },
    praiseForComment(type, commentId) {
      var params = {
        "comment": commentId,
      }
      let func = type ? createComplimentForComment : deleteComplimentForComment
      func(params).then((response) => {
        console.log(response)
        this.getArticleDetail()
      }).catch((error) => {
        console.log(error)
        this.$message.error(
            {
              type: "error",
              message: "服务器异常"
            }
        )
      })
    },
    collectArticle(type) {
      var params = {
        collected_article: this.article.id,
      }
      let func = type ? createCollection : deleteCollection
      func(params).then((response) => {
        console.log(response)
        this.isCollected = type
      })
    },
    concernedUser(type) {
      let param = {
        "type": type,
        "follower": this.author.id
      }
      var that = this
      cancelConcerned(param).then(() => {
        that.isConcerned = type ? true : false
      })
    },
    convertMarkdownToHtml(body) {
      if (body) {
        body = marked(body);
        body = body.replace(/<img/g, "<br/><img style='width:600px;height:auto;position:relative'");
      }
      return body;
    },
    ...mapGetters("login", {
      "getUserInfo": "GET_USER_INFO",
    })
  },
  filters: {
    slice: function (value, start, end) {
      if (value) {
        return value.substring(start, end)
      } else {
        return value
      }
    }
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

.comment-item-body, .comment-item-footer {
  padding-left: 20px;
}

.comment-item-footer {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.comment-item-footer-left {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
}
.el-button{
  height: 28px;
  font-size: 18px;
}
.delete-button{
  position: relative;
  bottom: 4px;
}
.detail-body {
  display: flex;
  flex-direction: row;
  justify-content: center;
}

.line-wider {
  width: 90%;
  margin-top: 20px;
  margin-bottom: 20px;
}

.comment-item {
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
}

.comment-compliment-icon {
  position: relative;
  top: 4px;
}

.comment-item-header {
  position: relative;
  right: 10%;
  display: flex;
  flex-direction: row;
  width: 60%;
}

.comment-item-header, .comment-item-body, .comment-item-footer {
  margin-bottom: 5px;
}

.comment-item-body {
  font-size: 20px;
  line-height: 1.5;
  color: black;
  font-family: -apple-system, BlinkMacSystemFont, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Helvetica Neue", Helvetica, Arial, sans-serif;
}

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

.line {
  width: 70%;
  margin-left: 50px;
  margin-top: 16px;
  margin-bottom: 10px;
}

.line, .line-wider {
  height: 1px;
  background-color: #eee;
}

.comment-body > ul, .comments > ul {
  list-style: none;
  text-align: left;
}

.comment-body ul > li {
  padding: 5px 0;
  font-size: 24px;
}

.article-item {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}

.article-reading-count {
  color: #969696;
}

.author, .recommended-article {
  background-color: white;
  padding: 40px 20px 10px 10px;
  margin-left: 5px;
}

.recommended-article {
  margin-top: 10px;
  text-align: left;
  position: sticky;
  top: -1000px;
}

.recommended-article-header, .comment-header {
  font-weight: 500;
  border-left: 4px solid #ec7259;
  margin-left: 30px;
}

.comment-header {
  text-align: left;
  font-size: 25px;
  margin-bottom: 20px;
}

.author-article-title {
  font-size: 18px;
  color: lightgray;
}

.author-body {
  text-align: left;
}

.author-article-title {
  color: black;
  font-size: 20px;
  text-decoration-line: none;
  padding: 5px 0;
  width: auto;
}

.author-header {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  position: relative;
  right: 30px;
}

.article, .comment {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  margin-top: 10px;
  background-color: white;
  padding-left: 50px;
  padding-top: 40px;
  padding-right: 50px;
  padding-bottom: 50px;
  border-width: 0.5px;
  border-style: dotted;
  border-color: lightgray;
}

.article-footer {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.article-list {
  list-style: none;
}

.article-list li {
  padding: 10px 0px;
}

.article-footer-right {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  padding-top: 10px;
}

.compliment-icon, .footer-compliment-icon {
  justify-content: center;
  width: 48px;
  height: 48px;
  font-size: 18px;
  border-radius: 50%;
  box-shadow: 0 2px 10px rgb(0 0 0 / 5%);
  background-color: #fff;
}

.compliment-icon {
  margin-top: 10px;
}

.avatar {
  margin-left: 50px;
}

.detail-left {
  display: block;
  width: 20%;
  position: fixed;
  left: 100px;
  top: 40%;
}

.detail-icon {
  position: relative;
  top: 10px;
}

.detail-middle {
  width: 50%;
  height: auto;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}

.article-body {
  margin-top: 20px;
}

.article-title {
  text-align: left;
  font-size: 30px;
  font-weight: 700;
  word-break: break-word;
}

.article-header {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
}

.circle-button {
  color: #ec7259;
  background-color: #fff;
  border-color: #ec7259;
}

.circle-button-fill {
  color: #ec7259;
  background-color: #ffebeb;
  border-color: #ffebeb;
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
  border-width: 2px;
  border-style: double;
}

.circle-button-black-border {
  background-color: white;
  border-color: lightgray;
  color: #999;
}

.circle-button, .circle-button-fill {
  border-radius: 50px;
  border: 1px solid;
  padding: 2px 9px;
  height: 30px;
  width: 70px;
  font-size: 12px;
}
</style>