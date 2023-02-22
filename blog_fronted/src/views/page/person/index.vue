<template>
  <div class="personal-home">
    <div class="ph-left-wrap">
      <div class="ph-left-top">
        <div class="ph-user-img">
          <img
            :src="join_avatar_url(author.avatar)"
          />
        </div>
        <div class="ph-user-info">
          <div>{{author.username}}</div>
          <ul>
            <li>
              <span class="num">{{attentionCount}}</span>
              <span class="name">关注 ></span>
            </li>
            <li>
              <span class="num">{{followerCount}}</span>
              <span class="name">粉丝 ></span>
            </li>
            <li>
              <span class="num">{{articles.length}}</span>
              <span class="name">文章 ></span>
            </li>
            <li>
              <span class="num">{{characterCount}}</span>
              <span class="name">字数</span>
            </li>
            <li>
              <span class="num">{{collectionCount}}</span>
              <span class="name">收获喜欢</span>
            </li>
            <li>
              <span class="num">100</span>
              <span class="name">总资产</span>
            </li>
          </ul>
        </div>
        <div class="ph-top-btns">
          <el-button round plain>发简信</el-button>
        <span v-if="author.id != user.id">
            <el-button v-if="!isConcerned" type="success" @click="concernUser(true,author.id)" round
            ><i class="iconfont iconjiahaob"></i>关注</el-button
            >
            <el-button v-else round @click="concernUser(false,author.id)"
             ><i class="iconfont iconjiahaob"></i>已关注</el-button
            >
        </span>
        </div>
      </div>
      <el-tabs v-model="activeName" @tab-click="handleClick">
        <el-tab-pane label="文章" name="first">
          <span slot="label"><i class="iconfont iconwenzhang2"></i> 文章</span>
          <ArticleList :blogs="articles" />
        </el-tab-pane>
        <el-tab-pane label="动态" name="second">
          <span slot="label"><i class="iconfont iconwenzhang2"></i> 动态</span>
          <ArticleList :blogs="articles" />
        </el-tab-pane>
        <el-tab-pane label="最新评论" name="third">
          <span slot="label"
            ><i class="iconfont iconpinglunzu"></i> 最新评论</span
          >
          <ArticleList :blogs="articles" />
        </el-tab-pane>
        <el-tab-pane label="热门" name="four">
          <span slot="label"><i class="iconfont iconremen"></i> 热门</span>
          <ArticleList :blogs="articles" />
        </el-tab-pane>
      </el-tabs>
    </div>
    <div class="ph-right-wrap">
      <div class="personal-info">
      
        <div class="title">
        <span>个性签名：{{ author.person_instruction != "" ? author.person_instruction : "暂无个性签名"}}</span>
          <span @click="handleEadit" v-if="author.id === user.id"
            ><i class="iconfont iconshiwu-huabi"></i>编辑</span
          >
        </div>
        <div class="textarea-box" v-show="isEadit">
          <el-input type="textarea" v-model="author.person_instruction"></el-input>
          <el-button type="success" round @click="save">保存</el-button>
          <el-button type="info" round plain @click="cancel">取消</el-button>
        </div>
        <div class="textarea-show" v-show="!isEadit">{{ author.person_instruction }}</div>
      </div>
      <div class="my-like">
        <div><i class="iconfont iconcaidan"></i>我关注的专题/文集/连载</div>
        <div><i class="iconfont iconxihuan"></i>我喜欢的文章</div>
      </div>
      <div class="my-theme">
        <div class="title">我创建的专题</div>
        <ul>
          <li @click="toSpecialSubject">
            <i class="iconfont iconwenzhang2"></i> 旅游
          </li>
          <li><i class="iconfont iconwenzhang2"></i> 工作</li>
          <li><i class="iconfont iconwenzhang2"></i> 风景</li>
        </ul>
        <div class="btn">
          <i class="iconfont iconjiahaob"></i>
          创建一个新专题
        </div>
      </div>
      <div class="my-articles">
        <div class="title">我的文集</div>
        <div class="my-articles-list">
          <a href="#"> <i class="iconfont iconwenzhang2"></i> gulp </a>
          <a href="#"> <i class="iconfont iconwenzhang2"></i> vue </a>
          <a href="#"> <i class="iconfont iconwenzhang2"></i> layui </a>
          <a href="#"> <i class="iconfont iconwenzhang2"></i> h5 </a>
          <a href="#">
            <i class="iconfont iconwenzhang2"></i> 一张照片一个故事
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ArticleList from '@/components/ArticleList.vue'
import {getPersonArticles} from "../../../api/person";
import {base_url} from "../../../api/settings";
import {mapGetters} from "vuex";
import { extractImageUrl, extractContent } from "../../../utils/func_methords";
import {cancelConcerned,updateUser} from "../../../api/account";

export default {
		  name: 'personalHome',
      props: {
      id: {
        type: [Number, String],
        detail: -1
      }
  },
		components: {
			ArticleList
		},
		data() {
			return {
				intiroduction: '分享生活趣事与工作的日志',
				isEadit: false,
				activeName: 'first',
				list: [],
        categories:[],
        articles: [],
        followerCount: 0,
        attentionCount: 0,
        author: {},
        user:this.getUserInfo(),
        collectionCount: 0,
        characterCount: 0,
        isConcerned:false,
			}
		},
		mounted() {
        this.getArticleList({
            author_id: this.id
        })
		},
		methods:{
      judgeEmpty(intiroduction){
        if(intiroduction != undefined && intiroduction != null && intiroduction != ""){    
         return true
        }else{
          return false
        }
      },
      join_avatar_url(url) {
        return base_url.substring(0, base_url.length - 1) + url;
      },
      transformBlogs(blogs) {
          for (let i = 0; i < blogs.length; i++) {
            blogs[i].imgUrl = extractImageUrl(blogs[i].body);
            blogs[i].body = extractContent(blogs[i].body);
          }
          return blogs;
        },
			getArticleList(params) {
        getPersonArticles(params)
          .then((res) => {
            let data = JSON.parse(res.data);
            let articles = data.articles;
            this.articles = this.transformBlogs(articles)
            this.followerCount = data.followerCount;
            this.collectionCount = data.collectionCount;
            this.attentionCount = data.attentionCount;
            this.author = data.author;
            this.isConcerned = data.isConcerned;
            this.categories = data.categories;
          })
          .catch((err) => {
            console.log(err);
          });
			},
			handleEadit() {
				this.isEadit = true
			},
      updateUserIntroduction(param){
        updateUser(param).then((res) => {
          console.log(res)
          }
        )
     },
			save() {
				this.isEadit = false
        let params = {
          "id":this.author.id,
          "person_introduction":this.author.person_introduction
        }
        this.updateUserIntroduction(params)
			},
			cancel() {
				this.isEadit = false
			},
			handleClick(tab) {
        this.page = 0;
        let params = {
          "author_id":this.id,
          "page":this.page,
          "condition":tab.index
        }
        this.getArticleList(params)
			},
			toSpecialSubject() {
				this.$router.push({
					path: '/specialSubject'
				})
			},
      concernUser(type,id) {
        let param = {
          "type": type,
          "follower": id
        }
        cancelConcerned(param).then(() => {
          this.isConcerned = type
        })
      },
        getPersonArticles() {
        var params = {
          author_id: this.id
        }
      getPersonArticles(params).then((response) => {
        let data = JSON.parse(response.data)
        this.author = data.author
        this.author.avatar = base_url.substring(0, base_url.length - 1) + this.author.avatar
        this.articles = data.articles
        this.isConcerned = data.isConcerned
        let articles = this.articles
        if(articles.length > 0){
          this.characterCount = articles.reduce(
              (total, item) => {
                console.log("total",total,item)
                let base = 0
                if(total.body){
                  base = total.body.length
                }else {
                  base = Number(total)
                }
                if (item.body) {
                  return base + item.body.length
                } else {
                  return base + 0
                }
              }
          )
        }else{
          this.characterCount = 0
        }
        this.collectionCount = data.collectionCount
        this.categories = data.categories
        this.followerCount = data.followerCount
        this.attentionCount = data.attentionCount
      })
    },

    ...mapGetters("login", {
      "getUserInfo": "GET_USER_INFO",
    })
		}
	}
</script>

<style lang="scss">
.personal-home {
  width: 1000px;
  margin: 0 auto;
  display: flex;
  .ph-left-wrap {
    flex: 1;
    padding-top: 30px;
    margin-right: 40px;
    .ph-left-top {
      display: flex;
      margin-bottom: 20px;
      .ph-user-img {
        width: 80px;
        height: 80px;
        margin-left: -2px;
        margin-right: 20px;
        img {
          width: 100%;
          height: 100%;
          border: 1px solid #ddd;
          border-radius: 50%;
        }
      }
      .ph-user-info {
        flex: 1;
        div {
          font-size: 22px;
          font-weight: 700;
          margin-top: 6px;
          margin-bottom: 4px;
        }
        ul {
          li {
            display: inline-block;
            border-left: 1px solid #f0f0f0;
            font-size: 12px;
            margin: 0 7px 6px 0;
            padding: 0 0 0 8px;
            color: #969696;
            &:first-child {
              border-left: 0;
              padding-left: 0;
            }
            .num {
              display: block;
              font-size: 16px;
              color: #333;
            }
            .name {
              display: block;
            }
          }
        }
      }
      .ph-top-btns {
        margin-left: 20px;
        button {
          margin-top: 30px;
          padding: 11px 23px;
        }
      }
    }
  }
  .ph-right-wrap {
    width: 262px;
    padding-top: 30px;
    .personal-info {
      margin-bottom: 16px;
      padding-bottom: 16px;
      border-bottom: 1px solid #f0f0f0;
      .title {
        color: #969696;
        margin-bottom: 14px;
        span {
          float: right;
          text-align: right;
          cursor: pointer;
        }
      }
      .textarea-box {
        textarea {
          margin-bottom: 14px;
          width: 100%;
          height: 125px;
          padding: 5px 10px;
          font-size: 14px;
          background-color: hsla(0, 0%, 71%, 0.1);
          border: 1px solid #c8c8c8;
          border-radius: 4px;
          resize: none;
          outline: none;
        }
        button {
          padding: 7px 20px;
        }
      }
      .textarea-show {
        width: 100%;
        padding: 5px 10px;
        font-size: 14px;
      }
    }
    .my-like {
      margin-bottom: 16px;
      padding-bottom: 16px;
      border-bottom: 1px solid #f0f0f0;
      line-height: 30px;
      div {
        cursor: pointer;
        i {
          margin-right: 8px;
          font-size: 20px;
          vertical-align: middle;
        }
      }
    }
    .my-theme {
      margin-bottom: 16px;
      padding-bottom: 16px;
      border-bottom: 1px solid #f0f0f0;
      .title {
        color: #969696;
        margin-bottom: 14px;
      }
      ul {
        margin-bottom: 14px;
        li {
          margin: 10px 0;
          line-height: 22px;
          cursor: pointer;
        }
      }
      .btn {
        color: #3db922;
        cursor: pointer;
      }
    }
    .my-articles {
      margin-bottom: 16px;
      padding-bottom: 16px;
      border-bottom: 1px solid #f0f0f0;
      .title {
        color: #969696;
        margin-bottom: 14px;
      }
      .my-articles-list {
        a {
          line-height: 20px;
          display: block;
          margin: 12px 0;
          color: #2f2f2f;
          i {
            vertical-align: middle;
            margin-right: 2px;
          }
        }
      }
    }
  }
}
.el-tabs__item {
  font-size: 16px;
  i {
    font-size: 18px;
    &.iconpinglunzu {
      font-size: 20px;
    }
  }
}
</style>
