<template>
	<div class="atten-box">
		<div class="atten-left-wrap">
			<div class="atten-left-title">
				<span class="all-atten">全部关注</span>
				<span class="add-btn"><i class="iconfont iconjiahaob"></i>添加关注</span>
			</div>
			<ul class="atten-left-nav">
				<li 
				  :class="{'active': currentIndex == index}" 
					v-for="(item, index) in navList" 
					:key="index"
					@click="changeRight(index, item)">
					<img :src="join_img_url(item.pic)">
					<span class="name">{{item.username}}</span>
					<span class="count">{{item.count}}</span>
				</li>
			</ul>
		</div>
		<div class="atten-right-wrap">
			<div class="atten-right-top">
				<img @click="toSpecialSubject" src="https://upload.jianshu.io/collections/images/83/1.jpg?imageMogr2/auto-orient/strip|imageView2/1/w/240/h/240/format/webp"
				 alt="">
				<div class="name">
					<div class="name-theme" @click="toSpecialSubject">{{title}}</div>
					<div class="name-info">
						<span class="user">简书</span>编 · 收录了<span>{{articleCount}}</span>篇文章 · <span>{{likeCount}}</span>人关注
					</div>
				</div>
				<div class="btns">
					<el-button type="primary" round>投稿</el-button>
					<el-button type="primary" round @click="toSpecialSubject">专题主页 > </el-button>
				</div>
			</div>
			<el-tabs v-model="activeName" @tab-click="handleClick">
				<el-tab-pane label="最新收录" name="first">
					<span slot="label"><i class="iconfont iconwenzhang2"></i> 最新收录</span>
					<ArticleList :blogs="list"/>
				</el-tab-pane>
				<el-tab-pane label="最新评论" name="second">
					<span slot="label"><i class="iconfont iconpinglunzu"></i> 最新评论</span>
					<ArticleList :blogs="list"/>
				</el-tab-pane>
				<el-tab-pane label="热门" name="third">
					<span slot="label"><i class="iconfont iconremen"></i> 热门</span>
					<ArticleList :blogs="list"/>
				</el-tab-pane>
			</el-tabs>
		</div>
	</div>
</template>

<script>
	import ArticleList from '@/components/ArticleList.vue';
	import 
		{ getFriendLoopData }
	 from "../../api/account";
	import {base_url} from "../../api/settings";

	export default {
		name: 'attention',
		components: {
			ArticleList
		},
		data() {
			return {
				activeName: 'first',
				navList: [],
				currentIndex: 0,
				list: [],
				title: '摄影',
				articleCount: 100,
				likeCount: 1098760,
				page:1,
				hasNext:true
			}
		},
		mounted() {
			// this.getLeftList()
			console.log("ssss")
			this.getArticleList({
				page: 1,
			})
		},
		methods: {
			join_img_url(url){
				console.log(url)
 				return base_url + "media/" + url
			},
			getArticleList(params) {
				getFriendLoopData(params).then(res => {
					let data = JSON.parse(res.data)
					this.list = data.data
					this.navList = JSON.parse(data.followers)
					console.log(this.navList)
				}).catch(err => {
					console.log(err)
				})
			},
			changeRight(index, item) {
				this.currentIndex = index
				this.title = item.name
				this.articleCount = item.article_count
				this.likeCount = item.like_count
				//console.log(item.id)
				//切换右侧内容
				this.getArticleList({
					page: 1,
				})
			},
			// getLeftList() {
			// 	this.$axios.attenList().then(res => {
			// 		//console.log(res.data)
			// 		const arr = res.data.subscriptions
					
			// 		//es6数组去重（去除重复对象）
			// 		var hash = {};
			// 		this.navList = arr.reduce(function(item, next) {
			// 		    hash[next.name] ? '' : hash[next.name] = true && item.push(next);
			// 		    return item
			// 		}, [])
					
			// 	}).catch(err => {
			// 		console.log(err)
			// 	})
			// },
			handleClick(tab, event) {
				console.log(tab, event);
				this.getArticleList({
					page: 1,
				})
			},
			toSpecialSubject() {
				this.$router.push({
					path: '/attention/specialSubject'
				})
			}
		}
	}
</script>

<style scoped lang="scss">
	@import '@/assets/scss/common.scss';
	.atten-box {
		width: 100%;
		margin: 0 auto;
		display: flex;
		.atten-left-wrap {
			width: 20%;
			margin-right: 40px;
			padding-top: 30px;
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
						background-color: rgba(240, 240, 240, .7);
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
			flex: 2;
			padding-top: 30px;
		}
	}
</style>
