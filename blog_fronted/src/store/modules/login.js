import {setToken, setUserInfo} from "../../utils/cache";

import * as types from '../mutation-types.js'
const state = {
    token:"",
  user_info:""
}
const mutations = {
  [types.SET_TOKEN](state,token){
    state.token = token
    setToken(token)
  },
  [types.SET_USER_INFO](state,user_info){
    state.user_info = user_info
    setUserInfo(user_info)
  }

}

export default {
  namespaced: true,
  state,
  mutations,
}