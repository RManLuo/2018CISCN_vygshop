# H1TerHub CISCN A&D Web

## 打包步骤

1. 将`sshop, *.py` 移动到`ciscn_deploy/www`里
2. 向`sshop/captcha`填充验证码数据集
3. 向`ciscn_deploy`填充`dumb-init.deb`（下载地址`https://github.com/Yelp/dumb-init/releases/`）和`phantomjs`（下载地址`https://bitbucket.org/ariya/phantomjs/downloads/`，解压其中的bin）（辣鸡网络只能这么加速了……）
4. 现在有`ciscn_*`三个文件夹，将这三个文件夹打包即可。
5. 打包完将源码撤回移动到根目录

## 部署

1. 切换到`ciscn_deploy`
2. 运行`docker-compose build` （build过程中`phantomjs`可能会因权限问题无法运行，添加运行权限重新构建即可）
3. 运行`docker-compose up -d`，程序将在后台运行
4. 宿主使用`docker ps`查看容器ID后可用`docker exec -it ID /bin/sh`连接到容器

## 需要的环境变量

`product` 存在该参数时Tornado内`debug=False`，docker内存在

`FLAAAAAG`你懂的，可通过docker运行参数修改

`api_url`（模拟）短信接口地址，docker内为`http://127.0.0.1:8200/api/send_sms`