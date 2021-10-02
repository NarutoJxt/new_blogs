import {getToken as getTokenCache}  from "../utils/cache"
export function getToken(state){
    var token = state.login.token
    if(!token){
        token = getTokenCache()
    }
    return token
}