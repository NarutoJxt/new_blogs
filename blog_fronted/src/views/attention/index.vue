<template>
  <div class="atten-box">
    <div class="atten-left-wrap">
      <div class="atten-left-title">
        <span class="all-atten">全部关注</span>
        <span class="add-btn"
          ><i class="iconfont iconjiahaob"></i>添加关注</span
        >
      </div>
      <ul class="atten-left-nav">
        <li :class="{ active: currentIndex == 0 }" @click="changeRight(0)">
          <img
            style="border: none"
            src="../../assets/img/attention/朋友圈.png"
          />
          <span class="name">朋友圈</span>
        </li>
        <li
          :class="{ active: currentIndex == index + 1 }"
          v-for="(item, index) in navList"
          :key="index + 1"
          @click="changeRight(index + 1, item)"
        >
          <img :src="join_img_url(item.pic)" />
          <span class="name">{{ item.username }}</span>
          <span class="count">{{ item.count }}</span>
        </li>
      </ul>
    </div>
    <div class="atten-right-wrap">
      <div v-if="currentIndex == 0">
        <ArticleList :blogs="list" />
      </div>
      <div v-else>
        <div class="atten-right-top">
          <img
            @click="toSpecialSubject"
            :src="join_avatar_url(author.avatar)"
            alt=""
          />
          <div class="name">
            <div class="name-theme" @click="toSpecialSubject">
              {{ author.username }}
            </div>
            <div class="name-info">
              <span class="user">简书</span>编 · 收录了<span>{{
                articleCount
              }}</span
              >篇文章 · <span>{{ followerCount }}</span
              >人关注
            </div>
          </div>
          <div class="btns">
            <el-button type="primary" round>投稿</el-button>
            <el-button type="primary" round @click="toSpecialSubject"
              >专题主页 >
            </el-button>
          </div>
        </div>
        <el-tabs v-model="activeName" @tab-click="handleClick">
          <el-tab-pane label="最新收录" name="first">
            <span slot="label"
              ><i class="iconfont iconwenzhang2"></i> 最新收录</span
            >
            <ArticleList :blogs="list" />
          </el-tab-pane>
          <el-tab-pane label="最新评论" name="second">
            <span slot="label"
              ><i class="iconfont iconpinglunzu"></i> 最新评论</span
            >
            <ArticleList :blogs="list" />
          </el-tab-pane>
          <el-tab-pane label="热门" name="third">
            <span slot="label"><i class="iconfont iconremen"></i> 热门</span>
            <ArticleList :blogs="list" />
          </el-tab-pane>
        </el-tabs>
      </div>
    </div>
  </div>
</template>

<script>
import ArticleList from "@/components/ArticleList.vue";
import { getFriendLoopData } from "../../api/account";
import { getExtraBlogInfo } from "../../api/blog";
import { extractImageUrl, extractContent } from "../../utils/func_methords";

import { base_url } from "../../api/settings";

export default {
  name: "attention",
  components: {
    ArticleList,
  },
  data() {
    return {
      activeName: "first",
      navList: [],
      currentIndex: 0,
      list: [],
      author: {},
      articleCount: 0,
      followerCount: 0,
      page: 1,
      hasNext: true,
    };
  },
  mounted() {
    this.getArticleList({
      page: 1,
    });
  },
  methods: {
    join_img_url(url) {
      return base_url + "media/" + url;
    },
    join_avatar_url(url) {
      return base_url.substring(0, base_url.length - 1) + url;
    },
    getArticleList(params) {
      getFriendLoopData(params)
        .then((res) => {
          let data = JSON.parse(res.data);
          this.list = this.transformBlogs(data.data);
          this.navList = JSON.parse(data.followers);
        })
        .catch((err) => {
          console.log(err);
        });
    },
    transformBlogs(blogs) {
      for (let i = 0; i < blogs.length; i++) {
        blogs[i].imgUrl = extractImageUrl(blogs[i].body);
        blogs[i].body = extractContent(blogs[i].body);
      }
      return blogs;
    },
    getRightUserAndArticles(params) {
      getExtraBlogInfo(params)
        .then((res) => {
          let data = JSON.parse(res.data);
          this.list = this.transformBlogs(data.articles);
          this.articleCount = data.articles.length;
          this.author = data.author;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    changeRight(index, item) {
      this.currentIndex = index;
      this.activeName = "first";
      if (item) {
        let params = {
          id: item.id,
          page: this.page,
        };
        this.getRightUserAndArticles(params);
      } else {
        this.getArticleList({
          page: 1,
        });
      }
    },
    handleClick(tab) {
      this.page = 0;
      let params = {
        id: this.author.id,
        page: this.page,
        condition: tab.index,
      };
      this.getRightUserAndArticles(params);
    },
    toSpecialSubject() {
      this.$router.push({
        path: "/attention/specialSubject",
      });
    },
  },
};
</script>

<style scoped lang="scss">
@import "@/assets/scss/common.scss";
.atten-box {
  width: 100%;
  margin: 0 auto;
  display: flex;
  .atten-left-wrap {
    width: 20%;
    margin-right: 40px;
    padding-top: 30px;
    position: fixed;
    left: 0;
    overflow-y: scroll;
    height: 100%;
    .atten-left-title {
      overflow: hidden;
      padding: 0 13px 10px;
      border-bottom: 1px solid #f0f0f0;

      .all-atten {
        float: left;
        font-size: 16px;
      }

      .add-btn {
        float: right;
        cursor: pointer;

        i {
          font-weight: 600;
        }
      }
    }
    .atten-left-nav {
      li {
        display: flex;
        padding: 10px 13px;
        line-height: 40px;
        cursor: pointer;

        &:hover,
        &.active {
          background-color: rgba(240, 240, 240, 0.7);
          border-radius: 5px 0 0 5px;
        }

        img {
          width: 40px;
          height: 40px;
          margin-right: 8px;
          display: block;
          border: 1px solid #ddd;
          border-radius: 10%;
        }

        .name {
          flex: 1;
          vertical-align: middle;
          display: block;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
        }

        .count {
          color: #969696;
        }
      }
    }
  }

  .atten-right-wrap {
    flex: 1;
    padding-top: 30px;
    height: 100%;
    width: 75%;
    position: fixed;
    right: 10px;
    overflow-y: scroll;
  }
}
</style>
