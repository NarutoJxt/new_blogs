import {getToken} from "../store/getters";
import store from "../store/index.js"
import {refreshToken} from "../api/account";

const axios = require("axios");
const service = axios.create({
    timeout: 10000,
    withCredentials: true
})
service.interceptors.request.use(
    config => {
        // 每次发送请求之前判断vuex中是否存在token
        // 如果存在，则统一在http请求的header都加上token，这样后台根据token判断你的登录情况
        // 即使本地存在token，也有可能token是过期的，所以在响应拦截器中要对返回状态进行判断
        const token = getToken(store.state)
        token && (config.headers.Authorization = "JWT " + token);
        return config;
    },

    error => {
        return Promise.error(error);
    }
);
let isRefreshing = false
// 重试队列，每一项将是一个待执行的函数形式
let requests = []
service.interceptors.response.use(response => {
    const {code} = response.data
    if (code === 1234) {
        const config = response.config
        if (!isRefreshing) {
            isRefreshing = true
            return refreshToken().then(res => {
                const {token} = res.data
                store.setToken(token)
                config.headers['X-Token'] = token
                config.baseURL = ''
                // 已经刷新了token，将所有队列中的请求进行重试
                requests.forEach(cb => cb(token))
                // 重试完了别忘了清空这个队列（掘金评论区同学指点）
                requests = []
                return service(config)
            }).catch(res => {
                console.error('refreshtoken error =>', res)
                window.location.href = '/'
            }).finally(() => {
                isRefreshing = false
            })
        } else {
            // 正在刷新token，返回一个未执行resolve的promise
            return new Promise((resolve) => {
                // 将resolve放进队列，用一个函数形式来保存，等token刷新后直接执行
                requests.push((token) => {
                    config.baseURL = ''
                    config.headers['X-Token'] = token
                    resolve(service(config))
                })
            })
        }
    }
    return response
}, error => {
    try {
        if (error.response) {
            switch (error.response.status) {
                case 401://token过期，清除它,清除token信息并跳转到登录页面
                    store.commit('login/SET_TOKEN', "");
                    return;
                case 403://权限
                    store.commit('SET_TOKEN', "");
                    return;
            }
        }
        return Promise.reject(error.response.data)
    } catch (e) {
      console.log("ssss")
    }
})

export default service