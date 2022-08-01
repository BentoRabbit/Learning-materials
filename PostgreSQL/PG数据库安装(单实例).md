## PG数据库安装

### 软件准备

| 软件名称                     | 下载地址                                                     |
| ---------------------------- | ------------------------------------------------------------ |
| PostgreSQL  下载地址（总览） | https://yum.postgresql.org/rpmchart/                         |
| PG 13.4 client               | https://yum.postgresql.org/13/redhat/rhel-7-x86_64/repoview/postgresql13.html |
| PG 13.4 lib                  | https://yum.postgresql.org/13/redhat/rhel-7-x86_64/repoview/postgresql13-libs.html |
| PG 13.4 server               | https://yum.postgresql.org/13/redhat/rhel-7-x86_64/repoview/postgresql13-server.html |

### 基础环境说明

| 内容                         | 说明           |
| ---------------------------- | -------------- |
| 操作系统                     | Oracle Linux 7 |
| 主机名                       | pgsingle       |
| 公有IP地址（对外访问）       |                |
| 私有IP地址（虚拟机内部访问） | 192.168.56.133 |
| 软件共享目录                 | /software      |

## 一、系统准备

#### 1）通过Vagrant 先创建Oracle Linux 7虚拟机（具体创建见Vagrant使用）

```
#查看现有的vagrant虚拟机库
vagrant box list
```

```
#生成Oracle Linux7 虚拟机vagrantfile
vagrant init oraclelinux/7

#在目录下，找到vagrantfile文件
#增加私有IP配置
config.vm.network "private_network", ip: "192.168.56.133"
#增加公有IP配置 
config.vm.network "public_network", ip: "192.168.3.130"
#共享目录配置，用于读取数据库软件
config.vm.synced_folder "/software", "/software"
```

#### 2）以root用户进入系统，进行初始化设置

```
#启动虚拟机
vagrant up
vagrant ssh

#切换到root用户需改系统基础信息
sudo -s

#设置主机名称
hostnamectl set-hostname pgsingle

#设置时区
timedatectl set-timezone Asia/Shanghai

#修改root用户密码
echo "Mema_1234" | passwd root --stdin > /dev/null 2>&1

#删除欢迎信息
mv /etc/motd /etc/motd.orgn

#修改sshd配置
sed -i -e "s\PasswordAuthentication no\PasswordAuthentication yes\g" /etc/ssh/sshd_config
systemctl restart sshd

#关闭selinux
sed -i 's/SELINUX=enforcing/\SELINUX=disabled/' /etc/selinux/config

#关闭防火墙
systemctl stop firewalld
systemctl disable firewalld

#配置主机名列表
cat >> /etc/hosts <<EOF
192.168.56.133 pgsingle
EOF
```

## 二、数据库安装

#### 1）通过RPM包的形式，安装PG13版本数据库

```
#安装pg所需的依赖包
yum install -y libicu

#安装pg所需的lib,client以及Server包
cd /software
rpm -ivh postgresql13-libs-13.4-1PGDG.rhel7.x86_64.rpm
rpm -ivh postgresql13-13.4-1PGDG.rhel7.x86_64.rpm
rpm -ivh postgresql13-server-13.4-1PGDG.rhel7.x86_64.rpm

#安装包会自动创建postgres操作系统用户
```

![image-20211117154114892](PG数据库安装(单实例).assets/image-20211117154114892.png)

![image-20211117154017646](PG数据库安装(单实例).assets/image-20211117154017646.png)

#### 2）初始化PG数据库

```
#通过PG自带脚本，初始化数据库
#如果需要更改数据库默认存储位置，需要修改配置文件，后续测试中修改验证
/usr/pgsql-13/bin/postgresql-13-setup initdb
#该脚本会对数据库进行初始化配置，主要生成/var/lib/pgsql/13目录及相关文件
```

![image-20211117154406852](PG数据库安装(单实例).assets/image-20211117154406852.png)

#### 3）启动PG并配置自动启动

```
#启动PG数据库
systemctl restart postgresql-13
#配置服务自动启动
systemctl enable postgresql-13

#通过postgres用户连接数据库验证
su - postgres
#使用psql命令连接数据库并查看默认数据库及用户权限$为用户提示符
psql
#进入postgres-# 提示符，查看本用户下的数据库
\du
#查看所有默认数据库
\l
#查看当前用户及数据库
\c
#退出
\q
```

![image-20211117154659462](PG数据库安装(单实例).assets/image-20211117154659462.png)

#### 4）修改监听支持远程登陆访问

```
#创建测试用户，用户之后连接测试,继续上一步portgres命令行下
#创建超级管理员mema，此步骤为测试使用，真实环境无需创建
create role mema superuser encrypted password 'mema' login replication createdb createrole;

#创建测试数据库，隶属于mema用户
create database mema owner mema;

#检查是否创建成功
\du
\l
```

![image-20211117155402305](PG数据库安装(单实例).assets/image-20211117155402305.png)

```
#测试连接
#通过psql -h(ip地址) -U(用户名)进行连接尝试
psql -h 192.168.56.133 -Umema
```

![image-20211117155525426](PG数据库安装(单实例).assets/image-20211117155525426.png)

```
#通过网络状态命令检查，目前默认监听127.0.0.1，也就是只监听本地连接
netstat -nltpa
```

![image-20211117160243839](PG数据库安装(单实例).assets/image-20211117160243839.png)

```
#修改配置文件，设置监听
vi /var/lib/pgsql/13/data/postgresql.conf

#将listen_address参数去掉注释，同时从'localhost'改成'0.0.0.0',保存并退出
listen_address = '0.0.0.0'

#重启数据库使配置生效
systemctl restart postgresql-13

#检查监听是否启动
netstat -nltpa
```

![image-20211117160854022](PG数据库安装(单实例).assets/image-20211117160854022.png)

![image-20211118111514738](PG数据库安装(单实例).assets/image-20211118111514738.png)

```
# 有了监听，也不是直接可以通过用户可以连接的
# 还需要修订pg_hba.conf文件，增加访问规则
vi /var/lib/pgsql/13/data/pg_hba.conf

# 增加访问配置，让所有用户可以通过网络以密码的方式访问数据库
# 第一位host表示通过网络连接
# 第二位all表示所有数据库
# 第三位all表示所有用户
# 第四位192.168.3.0/24表示192.168.3网段中的IP都可以连接
# 第五位md5 表示通过密码验证
host all all 192.168.56.0/24 md5

#重启数据库使配置生效
systemctl restart postgresql-13

# 此时用户可以正常连接数据库
psql -h 192.168.56.133 -Umema 
```

![image-20211118141542400](PG数据库安装(单实例).assets/image-20211118141542400.png)
