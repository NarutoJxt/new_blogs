import axios from "@/utils/axios";
import {base_url} from "./settings";


export const register = (params)=>{
    return axios.post(
        base_url + "api/users/",
        params
    )
}
export const login = (params)=>{
    return axios.post(
        base_url + "login/",
        params
    )
}

export const logout = (params)=>{
    return axios.get(
        base_url + "api/users/logout/",
        params
    )
}

export const refreshToken = (params)=>{
    return axios.post(
        base_url + "refresh_token",
        params
    )
}
export const getIndexAttentions = (params)=>{
       return axios.get(
        base_url + "api/attention/index/",
           {
               params
           }
    )
}
export const cancelConcerned = (params)=>{
    return axios.post(
        base_url + "api/attention/",
        params
    )
}

export const getFriendLoopData = (params)=>{
    return axios.get(
        base_url + "api/attention/",
        {
            params:params
        }
    )
}

export const updateUser = (params)=>{
    return axios.put(
        base_url + "api/users/",
        params
    )
}