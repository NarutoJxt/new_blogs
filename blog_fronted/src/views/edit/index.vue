<template>
  <div class="editor-main">
    <div class="editor-container">
      <div class="back-index">
        <a href="/">回首页</a>
      </div>
      <div class="category-addition">
        <div @click="switchBlog" class="category-addition-btn">
          <i class="el-icon-plus"></i>
          <a>新建文章</a>
        </div>
        <transition name="el-zoom-in-top">
          <div v-if="switchNewBlog" class="category-addition-form">
            <el-form :model="categoryForm" ref="categoryForm" label-width="100px" class="demo-ruleForm">
              <el-form-item
                  prop="category"
                  :rules="[
                  { required: true, message: '文集名称不能为空'},
                ]"
              >
                <el-input type="text" placeholder="新建文集" v-model.number="categoryForm.category"
                          autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item class="category-addition-form-footer">
                <el-button type="success" @click="addCategory">提交</el-button>
                <el-button @click="switchBlog">取消</el-button>
              </el-form-item>
            </el-form>
          </div>
        </transition>
      </div>
      <ul class="editor-menu">
        <li v-for="(item,i) in categories" :key="i" :class="item.pk === category?'active':'inactive'"
            @click="chooseCategory(item.pk)">
          {{ item.category }}
          <el-dropdown @command="handleCommand" v-if="item.pk === category" style="float: right">
            <span class="el-dropdown-link">
              <i style="font-size: 20px" class="el-icon-setting el-icon--left"></i>
            </span>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item :command="{command:'updateCategory',data:item}">修改文集</el-dropdown-item>
              <el-dropdown-item :command="{command:'deleteCategory',data:item}">删除文集</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </li>
      </ul>
    </div>
    <el-dialog
        :title="dialogTitle"
        :visible="dialogVisible"
        width="25%"
        :show-close="false"
    >
      <span>{{ dialogMessage }}</span>
      <span slot="footer" class="dialog-foter">
    <el-button @click="dialogVisible = null">取 消</el-button>
    <el-button type="primary" @click="dialogFunc">确 定</el-button>
  </span>
    </el-dialog>
    <div class="editor-container-child">
      <div class="blog-addition">
        <div @click="addBlog" class="blog-addition-btn">
          <i class="el-icon-plus"></i>
          <a>新建文章</a>
        </div>
      </div>
      <ul class="child-editor-menu">
        <li v-for="(item,i) in articleList" :key="i" :class="item.id === article.id?'child-active':'child-inactive'"
            @click="updateBlog(item)">
          {{ item.title }}
          <el-dropdown @command="handleCommand" v-if="item.id === article.id" style="float: right">
            <span class="el-dropdown-link">
              <i style="font-size: 20px" class="el-icon-setting el-icon--left"></i>
            </span>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item :disabled="item.status==='e'|| item.status === null?true:false" :command="{command:'publishArticle',data:item}">发布文章</el-dropdown-item>
              <el-dropdown-item :command="{command:'deleteArticle',data:item}">删除文章</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </li>
      </ul>
    </div>
    <div class="editor-view">
      <editor @update="updateArticleList" @save="saveBlog" ref="editor" :article="article"></editor>
    </div>
    <el-dialog width="600px" height="200px" title="修改文集" :visible="dialogFormVisible">
      <el-form :model="form">
        <el-form-item label="文集名称" :label-width="formLabelWidth">
          <el-input v-model="form.category" autocomplete="off"></el-input>
          <el-input type="hidden" v-model="form.pk"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = null">取 消</el-button>
        <el-button type="primary" @click="updateCategory">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import {
  createCategory,
  deleteBlog,
  deleteCategory,
  get_blogs,
  getCategories,
  updateBlog,
  updateCategory
} from "../../api/blog";
import Editor from "./components/edit"

export default {
  name: "backendLayout",
  components: {Editor},
  data() {
    return {
      height: '800px',
      width: "20%",
      index: -1,
      childIndex: -1,
      switchNewBlog: false,
      curType:null,
      article: null,
      dialogTitle:"",
      dialogMessage:"",
      dialogVisible: false,
      dialogFormVisible:false,
      form: {
        pk: null,
        category: "",
      },
      formLabelWidth: '120px',
      categoryForm: {
        category: ''
      },
      editable: null,
      category: "",
      categories: [],
      categoryBlogsDict: {},
    }
  },
  created() {
    this.getCategories()
    this.getCategoryAndBlogs()
  },
  methods: {
    switchBlog() {
      this.switchNewBlog = !this.switchNewBlog
    },
    handleCommand(item) {
      var command = item.command
      var data = item.data
      this.curType = command
      if(command === "deleteCategory"){
        this.form.category = data.category
        this.form.pk = data.pk
        this.dialogTitle = "删除文集"
        this.dialogMessage = "删除文集则将该文集下的所有文章一并删除，确认继续？"
        if(this.editable && (this.form.pk == this.editable.category)){
        this.$message.error(
            {
              type: "error",
              message: "该类目下还有文章未保存，请编辑该文章"
            }
        )
      }else {
          this.dialogVisible = true
        }
      }else if(command === "deleteArticle"){
        this.dialogTitle = "删除文章"
        this.dialogMessage = "确认删除该文章？"
        this.dialogVisible = true
      }else if(command === "publishArticle"){
        this.dialogTitle = "发表文章"
        this.dialogMessage = "确认发表文章？"
        this.dialogVisible = true
        this.form.category = data.category
        this.form.id = data.id
        this.form.status = 'e'
      }else if(command === "updateCategory"){
        this.dialogFormVisible = true
        this.form.category = data.category
        this.form.pk = data.pk
      }
    },
    publishArticle(){
      updateBlog(this.form).then((response)=>{
          var article = response.data
        var index = -1
        for(let i=0;i<this.categoryBlogsDict[this.category].length;i++){
          if(this.categoryBlogsDict[this.category][i].id == article.id){
            index = i
          }
        }
        this.dialogVisible = null
        this.categoryBlogsDict[this.category][index].status = 'e'
        this.$message.success(
            {
              type: "success",
              message: "发布成功"
            }
        )
      }).catch((error)=>{
        console.log(error)
        this.$message.success(
            {
              type: "success",
              message: "发布失败"
            }
        )
        this.dialogVisible = null

      })
    },
    dialogFunc(){
      var dealFuncDict = {
        deleteCategory:this.deleteCategory,
        deleteArticle:this.deleteArticle,
        updateCategory:this.updateCategory,
        publishArticle:this.publishArticle
      }
      var func = dealFuncDict[this.curType]
      func()
    },
    deleteArticle() {
      if(this.article.id === undefined){
        this.categoryBlogsDict[this.category].splice(0,1)
        this.article = this.articleList.length > 0?this.articleList[0]:null
        this.dialogVisible = null
        this.editable = null
      }else{
      deleteBlog(this.article).then(() => {
        var index = -1
        for (let i = 0; i < this.categoryBlogsDict[this.category].length; i++) {
          if (this.article.id == this.categoryBlogsDict[this.category][i].id) {
            index = i
            break
          }
        }
        this.categoryBlogsDict[this.category].splice(index, 1)
        this.dialogVisible = null
        this.article = this.articleList.length > 0?this.articleList[0]:null
        this.$message.success(
            {
              type: "success",
              message: "删除成功"
            }
        )
      })}
    },
    deleteCategory() {
        deleteCategory(this.form).then(() => {
          let index = -1
          for (let i = 0; i < this.categories.length; i++) {
            if (this.categories[i].pk === this.form.pk) {
              index = i
              break
            }
          }
          this.categories.splice(index, 1)
          this.category = this.categories.length > 0 ? this.categories[0].pk : null
          this.article = this.articleList[0]
          this.$message.success(
              {
                type: "success",
                message: "删除成功"
              }
          )
          this.dialogVisible = null
        }).catch((error) => {
          this.$message.error(
              {
                type: "error",
                message: "删除失败"
              }
          )
          console.log(error)
        })
    },
    updateCategory() {
      updateCategory(this.form).then((response) => {
        this.dialogFormVisible = false
        for (let i = 0; i < this.categories.length; i++) {
          if (this.categories[i].pk === response.data.pk) {
            this.categories[i].category = response.data.category
          }
        }
        this.$message.success(
            {
              type: "success",
              message: "修改成功"
            }
        )
      }).catch(() => {
        this.$message.error(
            {
              type: "error",
              message: "修改失败"
            }
        )
      })
    },
    addCategory() {
      createCategory(this.categoryForm).then((response) => {
        let category = response.data
        this.categories.push(category)
        this.switchBlog()
        this.category = category.pk
        this.categoryBlogsDict[category.pk] = []
        this.$message.success(
            {
              type: "success",
              message: "创建文集成功"
            }
        )
      }).catch(() => {
        this.$message.success(
            {
              type: "success",
              message: "创建文集失败"
            }
        )
      })
    },
    getCategoryAndBlogs() {
      get_blogs().then((response) => {
        this.categoryBlogsDict = JSON.parse(response.data)
        let temp = this.categoryBlogsDict[this.category]
        if (temp) {
          if (temp.length > 0) {
            this.article = temp[0]
          }
        }
      })
    },
    getCategories() {
      getCategories().then((response) => {
        this.categories = response.data
        if (this.categories.length > 0) {
          this.category = this.categories[0].pk
        }
      })
    },
    saveBlog(val,data) {
      this.editable = val
      this.categoryBlogsDict[this.category].splice(0,1,data)
      this.article = data
    },
    chooseCategory(key) {
      this.category = key
    },
    updateBlog(article) {
      this.article = article
    },
    updateArticleList(article) {
      for (let i = 0; i < this.categoryBlogsDict[this.category].length; i++) {
        if (this.categoryBlogsDict[this.category][i].id === article.id) {
          this.categoryBlogsDict[this.category][i] = article
        }
      }
    },
    addBlog() {
      if (!this.editable) {
        this.article = {
          title: "标题",
          body: "",
          status: null,
          category: this.category,
        }
        this.categoryBlogsDict[this.category].unshift(
            this.article
        )
        this.editable = this.article
      } else {
        this.$message.error(
            {
              type: "error",
              message: "您有文章未保存，请编辑该文章"
            }
        )
      }
    }
  },
  computed: {
    articleList() {
      if (this.categoryBlogsDict[this.category]) {
        return this.categoryBlogsDict[this.category].length > 0 ? this.categoryBlogsDict[this.category] : []
      } else {
        return []
      }
    }
  },
  watch: {
    article(val) {
      this.$refs.editor.changeArticle(val)
    },
    category() {
      var temp = this.categoryBlogsDict[this.category]
      this.article = temp && temp.length > 0 ? temp[0] : null
    }
  }
}
</script>

<style scoped>
.editor-container, .editor-container-child {
  height: 110%;
  flex-grow: 2;
  flex-shrink: 1;
  width: 20%;
  margin: 0;
  background-color: #2c3e50;
}

.editor-container-child {
  background-color: white;
}

.category-addition, .blog-addition {
  color: white;
  font-size: 20px;
  font-weight: bolder;
  position: relative;
  right: 35%;
  width: 110%;
}

.category-addition-form {
  position: relative;
  left: 8%;
  width: 100%;
}

.category-addition-form-footer {
  position: relative;
  right: 11%;
}

.dialog {
  width: 600px;
  height: 200px;
}

.category-addition-btn, .blog-addition-btn {
  padding: 10px 0;
}

.blog-addition {
  margin-top: 30px;
  color: black;
  font-size: 18px;
}

.back-index {
  border-radius: 50px;
  width: 210px;
  height: 20px;
  border-color: grey;
  border-style: solid;
  padding-top: 5px;
  padding-bottom: 10px;
  position: relative;
  left: 10%;
  margin-top: 40px;
  margin-bottom: 20px;
}

.back-index > a {
  text-decoration: none;
  color: grey;
  text-align: center;
}

.editor-main {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  justify-content: space-between;
  align-items: flex-start;
  height: 100%;
  width: 100%;
  overflow: hidden;
}

.editor-view {
  flex-grow: 2;
  flex-shrink: 1;
  flex-basis: 80%;
  padding-left: 20px;
}

.editor-menu, .child-editor-menu {
  height: 100%;
  width: 100%;
  margin: 0;
  padding: 0;
  overflow: auto;
}

.editor-container-child {
  background-color: white;
  border-width: 1px;
  border-color: lightgrey;
  border-style: solid;
  border-top: none;
  margin-right: 10px;
}

.editor-menu li, .child-editor-menu li {
  list-style: none;
  padding: 20px 10px;
  margin: 10px 10px;
  text-align: left;
  text-wrap: normal;
}

.editor-menu li:hover, .active, .child-active, .child-editor-menu li:hover {
  border-width: 1px;
  border-style: dotted;
  background-color: lightgrey;
}

.editor-menu li:hover, .child-editor-menu li:hover {
  color: white;
}

.active {
  color: black;
}

.inactive, child-inactive, .child-active {
  color: white;
}
</style>