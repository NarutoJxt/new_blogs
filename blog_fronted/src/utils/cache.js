import storage from 'good-storage'
const token_prefix = "token"
const user_info_prefix = "user_info"

export function setToken(token){
  return storage.set(token_prefix,token)
}
export function getToken(){
  return storage.get(token_prefix)
}
export function  setUserInfo(user_info){
  return storage.set(user_info_prefix,user_info)
}
export function  getUserInfo(){
  return storage.get(user_info_prefix,{})
}