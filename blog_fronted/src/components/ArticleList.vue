<template>
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
</template>

<script>
	export default {
		name: 'articleList',
		data() {
			return {

			}
		},
		props: {
			blogs: Array
		},
		methods: {
			toArticleDetail() {
				this.$router.push({
					path: '/articleDetail'
				})
			},
			toPersonalHome() {
				this.$router.push({
					path: '/personalHome'
				})
			}
		},
		mounted() {

		}
	}
</script>

<style lang="scss">
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
  padding: 40px 0;
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
  width: 40%;
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
</style>
