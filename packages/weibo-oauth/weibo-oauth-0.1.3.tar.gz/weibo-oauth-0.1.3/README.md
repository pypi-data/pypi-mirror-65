## Sina Weibo API

## 安装
```
pip install weibo-oauth
```

## 使用
```
from weibo_oauth import Weibo
import webbrowser

#APP_ID,SECRET_KEY,redirect_uri
weibo=Weibo("APP_ID","SECRET_KEY")

#打开浏览器获取request code
webbrowser.open(weibo.get_authorize_url())

#黏贴获取到的code
code=input("input request code:")

#获取access_token
weibo.get_access_token(code)

#请求API，获取所有的评论
_json = weibo.get("comments/by_me")
print(_json)

```

## API请求
```
weibo.get("comments/by_me",count=200,page=10)
返回一个 json 对象
```