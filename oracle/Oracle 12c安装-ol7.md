## 安装Oracle 12c

### 1 主机设置

```
#修改主机名
hostnamectl set-hostname oraclesi
bash

#修改时区
timedatectl set-timezone 'Asia/Shanghai'
date

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
192.168.56.148    oraclesi.dbtest.mema.com   oraclesi  
EOF

#格式化第二块硬盘/dev/sdb,自动挂载到/u01	
if [ ! -e /dev/sdb1 ]; then
  echo -e "n\np\n1\n\n\nw" | fdisk /dev/sdb
fi

mkfs.xfs -f /dev/sdb1

UUID=`blkid -o value /dev/sdb1 | grep -v xfs`
mkdir /u01
cat >> /etc/fstab <<EOF
UUID=${UUID}  /u01    xfs    defaults 1 2
EOF

mount /u01

# 关闭透明大页THP
cat >> /etc/rc.local << EOF
if test -f /sys/kernel/mm/transparent_hugepage/enabled; then
 echo never > /sys/kernel/mm/transparent_hugepage/enabled
fi
if test -f /sys/kernel/mm/transparent_hugepage/defrag; then
 echo never > /sys/kernel/mm/transparent_hugepage/defrag
fi
EOF

#安装必要软件
yum install -y unzip 	
yum -y install oracle-database-server-12cR2-preinstall
yum -y install oracleasm*
yum -y install kmod-oracleasm*
yum -y install rlwrap
```

修改配置文件

```
[root@localhost ~]# vi /etc/sysctl.conf

# oracle-database-server-12cR2-preinstall setting for fs.file-max is 6815744
fs.file-max = 6815744

# oracle-database-server-12cR2-preinstall setting for kernel.sem is '250 32000 100 128'
kernel.sem = 250 32000 100 128

# oracle-database-server-12cR2-preinstall setting for kernel.shmmni is 4096
kernel.shmmni = 4096

# oracle-database-server-12cR2-preinstall setting for kernel.shmall is 1073741824 on x86_64
kernel.shmall = 1073741824

# oracle-database-server-12cR2-preinstall setting for kernel.shmmax is 4398046511104 on x86_64
kernel.shmmax = 4398046511104

# oracle-database-server-12cR2-preinstall setting for kernel.panic_on_oops is 1 per Orabug 19212317
kernel.panic_on_oops = 1

# oracle-database-server-12cR2-preinstall setting for net.core.rmem_default is 262144
net.core.rmem_default = 262144

# oracle-database-server-12cR2-preinstall setting for net.core.rmem_max is 4194304
net.core.rmem_max = 4194304

# oracle-database-server-12cR2-preinstall setting for net.core.wmem_default is 262144
net.core.wmem_default = 262144

# oracle-database-server-12cR2-preinstall setting for net.core.wmem_max is 1048576
net.core.wmem_max = 1048576

# oracle-database-server-12cR2-preinstall setting for net.ipv4.conf.all.rp_filter is 2
net.ipv4.conf.all.rp_filter = 2

# oracle-database-server-12cR2-preinstall setting for net.ipv4.conf.default.rp_filter is 2
net.ipv4.conf.default.rp_filter = 2

# oracle-database-server-12cR2-preinstall setting for fs.aio-max-nr is 1048576
fs.aio-max-nr = 1048576

# oracle-database-server-12cR2-preinstall setting for net.ipv4.ip_local_port_range is 9000 65500
net.ipv4.ip_local_port_range = 9000 65500

```

![image-20211013161713425](Oracle 12c安装-ol7.assets/image-20211013161713425.png)

修改配置文件

```
[root@localhost ~]# vi /etc/security/limits.d/oracle-database-server-12cR2-preinstall.conf


# oracle-database-server-12cR2-preinstall setting for nofile soft limit is 1024
oracle   soft   nofile    1024

# oracle-database-server-12cR2-preinstall setting for nofile hard limit is 65536
oracle   hard   nofile    65536

# oracle-database-server-12cR2-preinstall setting for nproc soft limit is 16384
# refer orabug15971421 for more info.
oracle   soft   nproc    16384

# oracle-database-server-12cR2-preinstall setting for nproc hard limit is 16384
oracle   hard   nproc    16384

# oracle-database-server-12cR2-preinstall setting for stack soft limit is 10240KB
oracle   soft   stack    10240

# oracle-database-server-12cR2-preinstall setting for stack hard limit is 32768KB
oracle   hard   stack    32768

# oracle-database-server-12cR2-preinstall setting for memlock hard limit is maximum of 128GB on x86_64 or 3GB
 on x86 OR 90 % of RAM
oracle   hard   memlock    134217728

# oracle-database-server-12cR2-preinstall setting for memlock soft limit is maximum of 128GB on x86_64 or 3GB
 on x86 OR 90% of RAM
oracle   soft   memlock    134217728

```

![image-20211013161851550](Oracle 12c安装-ol7.assets/image-20211013161851550.png)



### 2 数据库安装准备

#### 2.1创建所需要的用户，组，目录

```
#创建所需要的用户，组，目录
groupadd -g 54321 oinstall
groupadd -g 54322 dba
groupadd -g 54323 oper
useradd -u 54321 -g oinstall -G dba,oper oracle

echo "oracle" | passwd --stdin oracle

mkdir -p /u01/app/oracle
mkdir -p /u01/app/oracle/product/12.2.0/db_home
chown -R oracle:oinstall /u01

```

#### 2.2 准备oracle用户的环境变量

setEnv12c.sh

```
su - oracle

cat > /home/oracle/.setEnv12c.sh <<EOF
# Oracle Settings
export TMP=/tmp
export TMPDIR=\$TMP

export ORACLE_UNQNAME=orcl
export ORACLE_BASE=/u01/app/oracle
export ORACLE_HOME=/u01/app/oracle/product/12.2.0/db_home
export ORACLE_SID=orcl

export PATH=/usr/sbin:/usr/local/bin:\$PATH
export PATH=\$ORACLE_HOME/bin:\$PATH

export LD_LIBRARY_PATH=\$ORACLE_HOME/lib:/lib:/usr/lib
export CLASSPATH=\$ORACLE_HOME/jlib:\$ORACLE_HOME/rdbms/jlib
EOF

echo ". /home/oracle/.setEnv12c.sh" >> /home/oracle/.bash_profile
```

#### 2.3 解压oracle安装包

```
su - oracle
export DISPLAY=192.168.56.1:0.0
cd $ORACLE_HOME
unzip /software/

```



### 3 安装Oracle数据库

```
cd database/
./runInstaller
```

![image-20211014152151070](Oracle 12c安装-ol7.assets/image-20211014152151070.png)

![image-20211014152207118](Oracle 12c安装-ol7.assets/image-20211014152207118.png)

![image-20211014152221566](Oracle 12c安装-ol7.assets/image-20211014152221566.png)

![image-20211014152235694](Oracle 12c安装-ol7.assets/image-20211014152235694.png)

![image-20211014152249052](Oracle 12c安装-ol7.assets/image-20211014152249052.png)

![image-20211014152315950](Oracle 12c安装-ol7.assets/image-20211014152315950.png)

![image-20211014152330460](Oracle 12c安装-ol7.assets/image-20211014152330460.png)

![image-20211014152403455](Oracle 12c安装-ol7.assets/image-20211014152403455.png)

![image-20211014152424770](Oracle 12c安装-ol7.assets/image-20211014152424770.png)



### 4 创建监听

```
cd $ORACLE_HOME
cd bin
./netca
```

![image-20211014154036171](Oracle 12c安装-ol7.assets/image-20211014154036171.png)

![image-20211014154048717](Oracle 12c安装-ol7.assets/image-20211014154048717.png)

![image-20211014154056536](Oracle 12c安装-ol7.assets/image-20211014154056536.png)

![image-20211014154108377](Oracle 12c安装-ol7.assets/image-20211014154108377.png)

![image-20211014154119859](Oracle 12c安装-ol7.assets/image-20211014154119859.png)

![image-20211014154130546](Oracle 12c安装-ol7.assets/image-20211014154130546.png)



### 5 创建数据库实例

```
cd $ORACLE_HOME
cd bin
./dbca
```

![image-20211014154302449](Oracle 12c安装-ol7.assets/image-20211014154302449.png)

![image-20211014154316895](Oracle 12c安装-ol7.assets/image-20211014154316895.png)

![image-20211014154328217](Oracle 12c安装-ol7.assets/image-20211014154328217.png)

![image-20211014154349080](Oracle 12c安装-ol7.assets/image-20211014154349080.png)

![image-20211014154446873](Oracle 12c安装-ol7.assets/image-20211014154446873.png)

![image-20211014154505382](Oracle 12c安装-ol7.assets/image-20211014154505382.png)

![image-20211014154515914](Oracle 12c安装-ol7.assets/image-20211014154515914.png)

password：oracle

![image-20211014154745515](Oracle 12c安装-ol7.assets/image-20211014154745515.png)

创建PDB

```
sqlplus / as sysdba

create pluggable database pdb admin user pdbadmin identified by pdbadmin file_name_convert=('/u01/app/oracle/oradata/orcl/pdbseed','/u01/app/oracle/oradata/orcl/pdb');

--打开pdb
alter pluggable database pdb open instances=all;

--进入pdb
alter session set container=pdb;
```

![image-20211015153806391](Oracle 12c安装-ol7.assets/image-20211015153806391.png)



### 6 数据库的启动关闭

环境变量$ORACLE_SID来决定启动哪个实例

启动数据库需要数据库参数文件：

1. spfile<SID>.ora
2. spfile.ora
3. init<SID>.ora
4. init.ora

```
echo $ORACLE_SID
sqlplus /nolog
connect / as sysdba
startup pfile='...'
```

通过参数文件的control_files来找到控制文件

控制文件里面：（mount）：

- 数据文件的位置
- 在线日志文件的位置
- 数据库的同步信息SCN
- 备份信息 
- 等

当数据库处于实例恢复完毕后，可以open数据库。

```
su - oracle
# 查看环境变量
env
env|grep ORACLE
echo $ORACLE_SID

# 查看实例是否启动
ps -ef|grep ora_
ps -ef|grep smon

# 查看Listener
lsnrctl status
ps -ef|grep tns
```



三种关闭方式：

```sql 
shutdown; -- shutdown normal
shutdown transactional;
shutdown immediate;
shutdown abort;
```



运行日志：数据库运行的log跟踪文件

```
/u01/app/oracle/diag/rdbms/orcl/orcl/trace/alert_<SID>.log
```



### 7 监听进程

文件位置：$ORACLE_HOME/network/admin/listener.ora (如果没有，停止监听，通过netca创建一个)

```
## 添加再lisnener.ora文件末尾

SID_LIST_LISTENER =
(SID_LIST =
   (SID_DESC =
     (GLOBAL_DBNAME = orcl)
     (ORACLE_HOME = /u01/app/oracle/product/12.2.0/db_home)
     (SID_NAME = orcl)
   )
)
```

启动listener

```
lsnrctl start
lsnrctl status
```

修改缺省的1521端口

修改监听端口：

```
LISTENER =
  (DESCRIPTION_LIST =
    (DESCRIPTION =
      (ADDRESS = (PROTOCOL = TCP)(HOST = oraclesi)(PORT = 1522))
      (ADDRESS = (PROTOCOL = IPC)(KEY = EXTPROC1521))
    )
  )

## 添加再lisnener.ora文件末尾

SID_LIST_LISTENER =
(SID_LIST =
   (SID_DESC =
     (GLOBAL_DBNAME = orcl)
     (ORACLE_HOME = /u01/app/oracle/product/12.2.0/db_home)
     (SID_NAME = orcl)
   )
)
```

数据库参数修改：

```
 alter system set local_listener='(ADDRESS = (PROTOCOL = TCP)(HOST = 192.168.56.148)(PORT = 1522))';
```



查看监听：

```
cd $ORACLE_HOME/bin
./lsnrctl
LSNRCTL> status LISTENER
LSNRCTL> status LISTENER2
```

