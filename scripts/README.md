# 下载
curl -k https://bootstrap.pypa.io/get-pip.py -o get-pip.py

# 安装
python get-pip.py

# 设置国内镜像
mkdir  ~/.pip/
echo '[global]' >>  ~/.pip/pip.conf
echo 'index-url = https://pypi.tuna.tsinghua.edu.cn/simple' >>  ~/.pip/pip.conf

# 安装依赖
pip install -r requirements.txt


# 设置环境变量
echo 'export FLASKR_SETTINGS=/opt/RBAC/admin/setting.py' >> /ect/profile
source /etc/profile


# 数据库安装并初始化
    # 1 创建数据库并授权用户
	CREATE DATABASE `rbac` DEFAULT CHARACTER SET utf8;
	grant all on rbac.* to rbac_user@'%' identified by 'rbac_password';
	flush privileges;
    # 2 建表

        db.create_all()
    
    # 3 导入初始数据 

# 运行
python runserver.py

