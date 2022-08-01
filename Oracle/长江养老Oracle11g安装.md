

| 服务器   | 12.4.70.113 |
| -------- | ----------- |
| 执行人   |             |
| 审核人   |             |
| 服务时间 |             |

## 1：安装前准备

### 1.1：安装环境

| OS version     | centos linux release 7.4.1808 |
| -------------- | ----------------------------- |
| IP             | 12.4.70.113                   |
| Oracle账号密码 | oracle/oracle                 |
| Oracle version | Oracle 11g                    |
| CDB数据库名    |                               |
| 字符集         |                               |

### 1.2：安装包准备

安装包放置路径：

```
/cpic/oarsoft
```



## 2：安装数据库软件

### 2.1：编辑内核参数

#### 2.1.1 详细代码

```
vi /etc/sysctl.conf

fs.file-max = 6815744
kernel.sem = 250 32000 100 128
kernel.shmmni = 4096
kernel.shmall = 4194304
kernel.shmmax = 17179869183
kernel.panic_on_oops = 1
net.core.rmem_default = 262144
net.core.rmem_max = 4194304
net.core.wmem_default = 262144
net.core.wmem_max = 1048576
net.ipv4.conf.all.rp_filter = 2
net.ipv4.conf.default.rp_filter = 2
fs.aio-max-nr = 1048576
net.ipv4.ip_local_port_range = 9000 65500


# 重新载入
[root@dump-oracle ~]# sysctl -p
```



### 2.2：修改访问限制

#### 2.2.1 详细代码

```
vi /etc/security/limits.d/oracle-database-preinstall-11g.conf

oracle   soft   nofile    1024
oracle   hard   nofile    65536
oracle   soft   nproc    16384
oracle   hard   nproc    16384
oracle   soft   stack    10240
oracle   hard   stack    32768
oracle   hard   memlock    134217728
oracle   soft   memlock    134217728
```



#### 2.3.1 详细代码

```
yum install -y bc    
yum install -y binutils
yum install -y compat-libcap1
yum install -y compat-libstdc++-33
#yum install -y dtrace-modules
#yum install -y dtrace-modules-headers
#yum install -y dtrace-modules-provider-headers
yum install -y dtrace-utils
yum install -y elfutils-libelf
yum install -y elfutils-libelf-devel
yum install -y fontconfig-devel
yum install -y glibc
yum install -y glibc-devel
yum install -y ksh
yum install -y libaio
yum install -y libaio-devel
yum install -y libdtrace-ctf-devel
yum install -y libXrender
yum install -y libXrender-devel
yum install -y libX11
yum install -y libXau
yum install -y libXi
yum install -y libXtst
yum install -y libgcc
yum install -y librdmacm-devel
yum install -y libstdc++
yum install -y libstdc++-devel
yum install -y libxcb
yum install -y make
yum install -y net-tools # Clusterware
yum install -y nfs-utils # ACFS
yum install -y python # ACFS
yum install -y python-configshell # ACFS
yum install -y python-rtslib # ACFS
yum install -y python-six # ACFS
yum install -y targetcli # ACFS
yum install -y smartmontools
yum install -y sysstat


yum install -y unixODBC
```

### 2.4：创建用户组和用户及目录

#### 2.4.1 详细代码

```
groupadd -g 54321 oinstall
groupadd -g 54322 dba
groupadd -g 54323 oper
groupadd -g 54324 backupdba
groupadd -g 54325 dgdba
groupadd -g 54326 kmdba
groupadd -g 54330 racdba
useradd -u 54321 -g oinstall -G dba,oper,backupdba,dgdba,kmdba,racdba oracle
echo "oracle" | passwd --stdin oracle
mkdir -p /app/u01/oracle/product/11.2.0/db_1
mkdir -p /app/u01/oraInventory
chown -R oracle:oinstall /u01 
chmod -R 775 /u01 
```



### 2.5：修改firewall和selinux

#### 2.5.1 详细代码

```
vim /etc/selinux/config

SELINUX=disabled

systemctl stop firewalld
systemctl disable firewalld
```



### 2.6：编辑bash_profile

#### 2.6.1 详细代码

```
vi /home/oracle/.bash_profile

# Oracle Settings
export TMP=/tmp
export TMPDIR=$TMP

export ORACLE_BASE=/app/u01/oracle
export ORACLE_HOME=$ORACLE_BASE/product/11.2.0/db_1
export ORACLE_SID=cjzx

export PATH=/usr/sbin:/usr/local/bin:$PATH
export PATH=$ORACLE_HOME/bin:$PATH

export LD_LIBRARY_PATH=$ORACLE_HOME/lib:/lib:/usr/lib
export CLASSPATH=$ORACLE_HOME/jlib:$ORACLE_HOME/rdbms/jlib
```

#### 

### 2.7：解压oracle安装包

#### 2.7.1 详细代码

```
cd /cpic/orasoft
unzip /cpic/oradata/p13390677_112040_Linux-x86-64_1of7.zip
unzip /cpic/oradata/p13390677_112040_Linux-x86-64_2of7.zip
```





```

# vi /cpic/oradata/database/response/db_install.rsp
//需要修改的参数
oracle.install.option=INSTALL_DB_SWONLY

ORACLE_HOSTNAME=localhost

UNIX_GROUP_NAME=oinstall

INVENTORY_LOCATION=/app/u01/oraInventory

SELECTED_LANGUAGES=en,zh_CN

ORACLE_HOME=/app/u01/oracle/product/11.2.0/db_1

ORACLE_BASE=/app/u01/oracle

oracle.install.db.InstallEdition=EE

oracle.install.db.DBA_GROUP=dba

oracle.install.db.OPER_GROUP=oper

oracle.install.db.config.starterdb.characterSet=AL32UTF8

DECLINE_SECURITY_UPDATES=true

```





```
cd /cpic/orasoft/databse

./runInstaller -silent -responseFile /cpic/oradata/database/response/db_install.rsp


dbca -silent -createDatabase -responseFile
/app/u01/oracle/product/11.2.0/db_1/assistants/dbca/dbca.rsp

```

