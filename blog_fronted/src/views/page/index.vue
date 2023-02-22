<template>
  <div class="layout">
    <div class="left-container">
      <ul class="main-list">
        <li v-for="(item,index) in blogs" :key="index" class="item">
          <div class="blog">
            <a class="item-title" :href="'/article/detail/'+item.id+'/'">{{ item.title }}</a>
            <p :class="item.imgUrl?'item-body-img-existing':'item-body-img-not-found'">
              {{ item.body ? item.body.substr(0, 140) : "空" }}
            </p>
            <ul class="item-footer">
              <li>{{ item.username }}</li>
              <li>
                <img class="icon-position" :src="require('@/assets/img/index/heart.png')">
                <span>
                {{ item.compliment_count }}
              </span>
              </li>
              <li>
                <img class="icon-position" :src="require('@/assets/img/index/comment.png')">
                <span>
              {{ item.comment_count }}
            </span>
              </li>

            </ul>
          </div>
          <div style="width: 200px">
            <img v-if="item.imgUrl" class="item-img" :src="item.imgUrl" width="100%" height="100%"/>
          </div>
        </li>
      </ul>
      <button v-if="hasNext" class="load-btn" type="button"
              style="background-color: darkorange;width: 90%;height: 50px;
                                border-radius: 40px;margin-left: 30px;color: white;border: none"
              @click="this.getBlogs">
        加载更多
      </button>
    </div>
    <div class="right-container">
      <div style="padding-left: 40px">
        <span>推荐作者</span>
        <a style="float: right" @click="getIndexAttentions">
          <i class="el-icon-refresh"></i>
          <span>换一批</span>
        </a>
      </div>
      <ul class="recommend-list">
        <li v-for="(item,index) in recommendedUsers" :key="index">
          <div class="recommend-item">
            <el-avatar class="avatar" :src="item.avatar">
            </el-avatar>
            <a style="float: right;" v-if="item.isConcerned === true" @click="concernUser(index,false)">
              <i class="el-icon-check">
              </i>
              已关注
            </a>
            <a v-else style="float: right;color: lightgreen" @click="concernUser(index,true)">
              <i class="el-icon-plus">
              </i>
              关注
            </a>
            <a>{{ item.username.substring(0, 30) }}</a>
            <div class="annotation">写了{{ item.article_count }}篇文章,有{{ item.attention_count }}人喜欢</div>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import {getArticles} from "../../api/blog";
import {base_url} from "../../api/settings";
import {cancelConcerned, getIndexAttentions} from "../../api/account";
import {extractImageUrl,extractContent} from "../../utils/func_methords"
export default {
  name: "index",
  data() {
    return {
      blogs: [],
      blogsPage: 1,
      hasNext: true,
      recommendedUsers: [],
    }
  },
  created() {
    this.getBlogs()
    this.getIndexAttentions()
  },
  mounted() {
    this.$nextTick()
  },
  methods: {
    getBlogs() {
      var params = {
        page: this.blogsPage
      }
      getArticles(params).then((response) => {
        let data = JSON.parse(response.data)
        this.blogsPage++
        this.hasNext = data.hasNext
        let blogs = data.data
        for (let i = 0; i < blogs.length; i++) {
          blogs[i].imgUrl = extractImageUrl(blogs[i].body)
          blogs[i].body = extractContent(blogs[i].body)
        }
        this.blogs = this.blogs.concat(blogs)
      })
    },
    getIndexAttentions() {
      getIndexAttentions().then((response) => {
        let data = JSON.parse(response.data)
        this.recommendedUsers = data.recommendedUsers
        for (let i = 0; i < this.recommendedUsers.length; i++) {
          this.recommendedUsers[i].avatar = base_url.substring(0, base_url.length - 1) + this.recommendedUsers[i].avatar
        }
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
    concernUser(index, type) {
      let param = {
        "type": type,
        "follower": this.recommendedUsers[index].user_id
      }
      cancelConcerned(param).then(() => {
        this.recommendedUsers[index].isConcerned = type
      })
    },

  }
}
</script>

<style scoped>
.main-list, .recommend-list {
  list-style: none;
}

.avatar {
  float: left;
}

.layout {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  justify-content: center;
}

.recommend-list > li {
  padding: 10px 0;
  padding: 8px 0;
}

.main-list > li {
  padding: 40px 20px;
  border-bottom-color: lightgray;
  border-bottom-style: dotted;
  border-bottom-width: 1px;
}

.annotation {
  font-size: 12px;
  line-height: 20px;
  color: dimgrey;
}

.item {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

p img {
  width: 30%;
}

.recommend-item {
  margin: 0;
}

.icon-position {
  position: relative;
  top: 4px
}

.left-container {
  width: 54%;
}

.right-container {
  width: 25%;
  margin-top: 80px;
  text-align: left;
}

.blog {
  display: flex;
  flex-direction: column;
  width: 70%;
}

.item-title {
  text-align: left;
  margin: -7px 0 4px;
  display: inherit;
  font-size: 18px;
  font-weight: 700;
  line-height: 1.5;
  text-decoration: none;
  color: black;
}

.item-body-img-existing, .item-body-img-not-found {
  text-align: left;
  font-family: "Roboto", "Lucida Grande", "DejaVu Sans", "Bitstream Vera Sans", Verdana, Arial, sans-serif;
  font-size: 16px;
  color: dimgrey;
  line-height: 1.4;
}

.item-body-img-existing {
  width: 80%;
}

.item-body-img-not-found {
  width: 100%;
}

.item-footer {
  list-style: none;
  padding: 0;

}

.item-footer li {
  float: left;
  margin-left: 10px;
  align-content: center;
}
</style>d