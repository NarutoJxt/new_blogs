import axios from "../utils/axios";
import {base_url} from "./settings";

export const getPersonArticles = (params)=>{
    return axios.get(
        base_url + "blog/person/articles/",
        {
            params
        }
    )
}