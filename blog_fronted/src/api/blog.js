import {base_url} from "./settings";
import axios from "../utils/axios";

export const register = (params)=>{
    return axios.post(
        base_url + "api/blog/category/",
        params
    )
}
export const get_blogs = (params)=>{
    return axios.get(
        base_url + "blog/category/blogs/",
        params
    )
}
export const getCategories = (params)=>{
    return axios.get(
        base_url + "blog/category/",
        params
    )
}
export const createCategory = (params)=>{
    return axios.post(
        base_url + "blog/category/",
        params
    )
}
export const updateCategory = (params)=>{
    return axios.patch(
        base_url + "blog/category/"+params.pk+"/",
        params
    )
}
export const deleteCategory = (params)=>{
    return axios.delete(
        base_url + "blog/category/"+params.pk+"/",
        params
    )
}
export const createBlog = (params)=>{
    return axios.post(
        base_url + "blog/article/",
        params
    )
}
export const updateBlog = (params)=>{
    return axios.patch(
        base_url + "blog/article/"+params.id+"/",
        params
    )
}
export const getArticleDetail = (params)=>{
      return axios.get(
        base_url + "blog/article/",
          {params}
    )
}
export const getArticles = (params)=>{
    return axios.get(
        base_url + "blog/index/",
        {
            params
        }
    )
}
export const deleteBlog = (params)=>{
    return axios.delete(
        base_url + "blog/article/"+params.id+"/",
        params
    )
}
export const uploadImage = (params)=>{
    return axios.post(
        base_url + "blog/upload_file/",
        params,
        { headers:{'Content-Type': 'multipart/form-data' }},
    )
}
export const createCompliment = (params)=>{
    return axios.post(
        base_url + "compliment/article/",
        params
    )
}
export const deleteCompliment = (params)=>{
    return axios.delete(
        base_url + "compliment/article/cancel/",
        {
            params
        }
    )
}
export const createCollection = (params)=>{
    return axios.post(
        base_url + "collection/",
        params
    )
}
export const deleteCollection = (params)=>{
    return axios.delete(
        base_url + "collection/cancel/",
        {params}
    )
}

export const createComment = (params)=>{
    return axios.post(
        base_url + "comment/",
        params
    )
}
export const deleteComment = (params)=>{
    return axios.delete(
        base_url + "comment/"+params.id+"/",
        {params}
    )
}
export const createComplimentForComment = (data)=>{
    return axios.post(
        base_url + "compliment/comment/",
        data
    )
}
export const deleteComplimentForComment = (params)=>{
    return axios.delete(
        base_url + "compliment/comment/cancel/",
        {
            params
        }
    )
}
