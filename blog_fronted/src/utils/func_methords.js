import {base_url} from "../api/settings";

export function  transImageUrl(url) {
      return base_url.substring(0, base_url.length - 1) + url
    }
export function transDatetime(datetime) {
  return datetime.split(".")[0].replace("T", " ")
}
export function trnasUsername(username,start,end){
  if(username){
    return username.substring(start,end)
  }
  return username
}

export function extractContent(body) {
  if (!body) {
    return '';
  } else {
    var text = body.replace(/(\\*\\*|__)(.*?)(\\*\\*|__)/g, '')          //全局匹配内粗体
        .replace(/!\[[\s\S]*?\]\([\s\S]*?\)/g, '')                  //全局匹配图片
        .replace(/\[[\s\S]*?\]\([\s\S]*?\)/g, '')                    //全局匹配连接
        .replace(/<\/?.+?\/?>/g, '')                                 //全局匹配内html标签
        .replace(/(\*)(.*?)(\*)/g, '')                               //全局匹配内联代码块
        .replace(/`{1,2}[^`](.*?)`{1,2}/g, '')                       //全局匹配内联代码块
        .replace(/```([\s\S]*?)```[\s]*/g, '')                       //全局匹配代码块
        .replace(/\\~\\~(.*?)\\~\\~/g, '')                               //全局匹配删除线
        .replace(/[\s]*[0-9]+\.(.*)/g, '')                           //全局匹配有序列表
        .replace(/(#+)(.*)/g, '')                                    //全局匹配标题
        .replace(/(>+)(.*)/g, '')                                    //全局匹配摘要
        .replace(/\r\n/g, "")                                        //全局匹配换行
        .replace(/\n/g, "")                                          //全局匹配换行
        .replace(/\s/g, "")                                          //全局匹配空字符;
    return text
  }
}
export function extractImageUrl(body) {
  let imgRegx = /!.*?\((?<url>.*?)\)/mg
  let img = imgRegx.exec(body)
  let url = null
  if (img) {
    url = img.groups.url
  }
  return url
}