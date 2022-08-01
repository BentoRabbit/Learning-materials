## MySQL数据库安装

#### 1. 所需工具

- Oracle VM VirtualBox
- Vagrant
- MobaXterm 
- Git Bash 

#### 2. 下载安装包

mysql80-community-release-el7-3.noarch.rpm

安装包存放目录：/opt/software

![image-20210715132046875](MySQL.assets/image-20210715132046875.png)

#### 3. 安装安装mysql8的yum源

root用户

```shell
yum install mysql80-community-release-el7-3.noarch.rpm 
```

#### 4. 查看yum源

```shell
yum repolist
```

![image-20210715132539452](MySQL.assets/image-20210715132539452.png)

#### 5.安装MySQL

```shell
yum install mysql-community-server
```

![image-20210715132627405](MySQL.assets/image-20210715132627405.png)

```shell
systemctl start mysqld
ps -ef|grep mysql
```

![image-20210715132903710](MySQL.assets/image-20210715132903710.png)

```shell
--修改数据库root用户密码
grep 'temporary password' /var/log/mysqld.log
#临时密码：ppWSktlh*8OK


```

![image-20210715133408895](MySQL.assets/image-20210715133408895.png)

```shell
#修改密码
mysql -uroot -p
输入找到的密码
mysql>ALTER USER 'root'@'localhost' IDENTIFIED BY 'Mema_1234';

#密码修改为Mema_1234
```

![image-20210715133501084](MySQL.assets/image-20210715133501084.png)

![image-20210715133328485](MySQL.assets/image-20210715133328485.png)

```shell
#查看数据库
mysql>show databases;
```

![image-20210715133520121](MySQL.assets/image-20210715133520121.png)

```shell
#查看端口
netstat -antp
ss -nltp
```

![image-20210715134233145](MySQL.assets/image-20210715134233145.png)

![image-20210715134105301](MySQL.assets/image-20210715134105301.png)