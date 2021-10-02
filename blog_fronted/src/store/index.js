import Vue from 'vue'
import Vuex from 'vuex'
import * as getters from "./getters"
import login from "./modules/login";
Vue.use(Vuex)
export default new Vuex.Store({
  modules: {
    login:login,
  },
getters
})