<template>
  <div class="body">
    <div class="body-left">
      <div class="header">
        <el-avatar :size="70" style="margin-right: 20px" class="avatar" :src="author.avatar">
        </el-avatar>
        <div class="header-middle">
          <div id="username">
            {{ author.username }}
          </div>
          <div id="info-list">
            <ul>
              <li>
                <ul class="info-item">
                  <li>
                    {{ attentionCount }}
                  </li>
                  <li>
                    <a>关注</a>
                  </li>
                </ul>
              </li>
              <li>
                <ul class="info-item">
                  <li>
                    {{ followerCount }}
                  </li>
                  <li>
                    <a>粉丝</a>
                  </li>
                </ul>
              </li>
              <li>
                <ul class="info-item">
                  <li>
                    {{ articles?articles.length:0 }}
                  </li>
                  <li>
                    <a>文章</a>
                  </li>
                </ul>
              </li>
              <li>
                <ul class="info-item">
                  <li>
                    {{ characterCount }}
                  </li>
                  <li>
                    <a>字数</a>
                  </li>
                </ul>
              </li>
              <li>
                <ul class="info-item">
                  <li>
                    {{ collectionCount }}
                  </li>
                  <li>
                    <a>收藏</a>
                  </li>
                </ul>
              </li>
            </ul>
          </div>

        </div>
     <div v-if="user.id !== author.id">
       <el-button v-if="isConcerned" round icon="el-icon-check">已关注</el-button>
       <el-button v-else type="success" icon="el-icon-plus" round>关注</el-button>
     </div>
      </div>
    </div>
    <div class="body-right">
      b
    </div>
  </div>
</template>

<script>
import {getPersonArticles} from "../../../api/person";
import {base_url} from "../../../api/settings";
import {mapGetters} from "vuex";

export default {
  name: "index",
  props: {
    id: {
      type: [Number, String],
      detail: -1
    }
  },
  data() {
    return {
      user: this.getUserInfo(),
      articles: [],
      followerCount: 0,
      attentionCount: 0,
      author: {},
      collectionCount: 0,
      characterCount: 0,
      isConcerned:false,
    }
  },
  mounted() {
    this.$nextTick(this.getPersonArticles)
  },
  methods: {
    getPersonArticles() {
      var params = {
        author_id: this.id
      }
      console.log(params)
      getPersonArticles(params).then((response) => {
        let data = JSON.parse(response.data)
        this.author = data.author
        this.author.avatar = base_url.substring(0, base_url.length - 1) + this.author.avatar
        this.articles = data.articles
        this.isConcerned = data.isConcerned
        this.characterCount = this.articles.reduce(
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
        this.collectionCount = data.collectionCount
        this.categories = data.categories
        this.followerCount = data.followerCount
        this.attentionCount = data.attentionCount
      })
    },
    ...mapGetters("login", {
      "getUserInfo": "GET_USER_INFO",
    })  }
}
</script>

<style scoped>
.body {
  display: flex;
  flex-direction: row;
  justify-content: center;
  padding-top: 20px;
  margin-top: 20px;
  height: 100%;
}

.header {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
}

.body-left, .body-right {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  padding-left: 10px;
  padding-right: 10px;
}

.body-left {
  width: 40%;
  text-align: left;
}

.body-right {
  width: 15%;
}

.info-item {
  list-style: none;
  text-align: center;
  padding-left: 0;
}

#username {
  font-size: 24px;
  font-weight: 700;
  vertical-align: middle;
  padding-top: 5px;
}

.header-middle {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}

#info-list {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
}

#info-list > ul {
  margin-left: 0;
  padding-left: 0;
}

#info-list > ul > li {
  list-style: none;
  float: left;
  padding: 0 20px;
}

#info-list > ul > li:first-child {
  padding-left: 0px;
}
</style>