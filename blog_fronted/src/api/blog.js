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

export const deleteBlog = (params)=>{
    return axios.delete(
        base_url + "blog/article/"+params.id+"/",
        params
    )
}
