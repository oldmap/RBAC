# 项目简介
    
    RBAC(Role-Based Access Control,基于角色的访问控制)，本项目是我基于restfull思想（一切皆资源），对权限管理的实现设计的一个demo。
    时间有限，bug不断，主要看设计理念和思想。

## 安装步骤

### 0. 环境准备
    python2.7 mysql-5.6对环境不敏感，基于python3.6 coding然后再2.7上做的调试。

### 1. 安装pip
```shell
# 安装其他依赖等
yum install python-setuptools -y

# 下载pip
curl -k https://bootstrap.pypa.io/get-pip.py -o get-pip.py

# 安装pip
python get-pip.py

# 设置国内镜像
mkdir  ~/.pip/
echo '[global]' >>  ~/.pip/pip.conf
echo 'index-url = https://pypi.tuna.tsinghua.edu.cn/simple' >>  ~/.pip/pip.conf

# 安装依赖模块
pip install -r requirements.txt
```

### 2. 数据库安装

```shell
# 1 创建数据库并授权用户
CREATE DATABASE `rbac` DEFAULT CHARACTER SET utf8;
grant all on rbac.* to rbac_user@'%' identified by 'rbac_password';
flush privileges;
# 2 数据库连接设置 setting.py 配置文件
SQLALCHEMY_DATABASE_URI = "mysql://rbac_user:rbac_password@127.0.0.1:3306/rbac"
```

### 3. nginx配置
```shell
[root@VM_19_9_centos ~]# cat /etc/nginx/conf.d/rbac.conf 
server {
    listen 8000;
    server_name 127.0.0.1
    charset utf-8;
    client_max_body_size 75M;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/opt/RBAC/uwsgi.sock;
        uwsgi_param UWSGI_CHDIR /opt/RBAC;
    }
}
```

### 4. 启动uwsgi和nginx

```shell
uwsgi --ini uwsgi.ini
/etc/init.d/nginx start
```

### 5. 导入demo数据
```shell
mysql -urbac -p rbac < rbac.sql

```
