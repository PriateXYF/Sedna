# Sedna

基于 Leancloud 的自动化签到工具。

* [浏览器拓展](https://github.com/PriateXYF/Sedna-Extension)
* [说明文档](https://sedna.virts.app/)

## 本地调试

* 前往 https://console.leancloud.app 创建应用

* 创建项目

```bash
git clone 'https://github.com/PriateXYF/Sedna.git' && cd Sedna && touch .env
```

* 编辑 `.env` 文件

```bash
LEANCLOUD_APP_ID=xxxxxx
LEANCLOUD_APP_KEY=xxxxxx
LEANCLOUD_APP_MASTER_KEY=xxxxxx
LEANCLOUD_APP_PORT=80
LEANCLOUD_APP_ENV=development
WEB_PASSWORD=123456
BARK_URL=https://api.day.app/yourkey/
```

* 安装依赖

```bash
pip install -r requirements.txt
```

* 运行项目

```bash
export $(cat .env | xargs) && python3 wsgi.py --
```

## 在线部署

* 前往 https://console.leancloud.app 创建应用

* 选择 云引擎 -> WEB -> 设置 ，添加环境变量 `WEB_PASSWORD` ，变量值即为网站登录密码；设置访问域名，如 `checkin.avosapps.us` ，或绑定其他域名。

* 选择 云引擎 -> WEB -> 部署，选择 Git部署 ，填入本仓库地址 https://github.com/PriateXYF/Sedna.git ，分支或提交设定为 `main` 。