<template>
      <ul class="editor-menu">
        <li v-for="i in data" :key="i" :class="i === index?'active':'inactive'" @click="index = i">
          <slit></slit>
        </li>
      </ul>
</template>

<script>
export default {
name: "menu",
  props:{
    data:{
      type:Array,
      default:[]
    }
  }
}
</script>

<style scoped>
.editor-menu{
  height: 100%;
  width: 100%;
  background-color: #2c3e50;
  margin: 0;
  padding: 0;
}
.editor-menu li{
  list-style: none;
  padding: 20px 0;
}
.editor-menu li:hover,.active{
  border-width: 1px;
  border-style: dotted;
  background-color: white;
  color: black;
}
.active{
  color: black;
}
.inactive{
  color: white;
}
</style>