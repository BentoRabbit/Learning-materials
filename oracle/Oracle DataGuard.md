# Oracle DataGuard

| **操作系统**       | **oraclelinux7**   |
| ------------------ | ------------------ |
| **主机**           | **192.168.56.211** |
| **备机**           | **192.168.56.212** |
| **Oracle version** | 19.3               |

| 用户   | 密码      |
| ------ | --------- |
| root   | Mema_1234 |
| oracle | oracle    |

| 主库 | 备库   |
| ---- | ------ |
| mema | memaDG |

### linux系统的初始化设置，修改主机名，调整时区

```shell
#节点一
hostnamectl set-hostname DG1
bash

timedatectl set-timezone 'Asia/Shanghai'
date

yum install -y unzip
yum install -y rlwrap

#节点二
hostnamectl set-hostname DG2
bash

timedatectl set-timezone 'Asia/Shanghai'
date

yum install -y unzip
yum install -y rlwrap
```

### 1.安装Oracle

两个节点都要做

#### 1.1 编辑内核参数

```shell
vi /etc/sysctl.conf

fs.file-max = 6815744
kernel.sem = 250 32000 100 128
kernel.shmmni = 4096
kernel.shmall = 1073741824
kernel.shmmax = 4398046511104
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
sysctl -p
```

#### 1.2 修改访问限制

```shell
vi /etc/security/limits.d/oracle-database-preinstall-19c.conf

oracle   soft   nofile    1024
oracle   hard   nofile    65536
oracle   soft   nproc    16384
oracle   hard   nproc    16384
oracle   soft   stack    10240
oracle   hard   stack    32768
oracle   hard   memlock    134217728
oracle   soft   memlock    134217728
```

#### 1.3 安装rpm包

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

#为了使用xstart，需要安装
yum install -y xorg-x11-xauth
```

#### 1.4 创建用户组和用户及目录

```
groupadd -g 54321 oinstall
groupadd -g 54322 dba
groupadd -g 54323 oper
useradd -u 54321 -g oinstall -G dba,oper oracle
echo "oracle" | passwd --stdin oracle
mkdir -p /u01/app/oracle/product/19.0.0/dbhome_1
chown -R oracle:oinstall /u01 
chmod -R 775 /u01 
```

#### 1.5 修改firewall和selinux

```
vi /etc/selinux/config

SELINUX=disabled

systemctl stop firewalld
systemctl disable firewalld
```

#### 1.6 编辑bash_profile

```
vi /home/oracle/.bash_profile

# Oracle Settings
export TMP=/tmp
export TMPDIR=$TMP

export ORACLE_BASE=/u01/app/oracle
export ORACLE_HOME=$ORACLE_BASE/product/19.0.0/dbhome_1
export ORACLE_SID=orcl

export PATH=/usr/sbin:/usr/local/bin:$PATH
export PATH=$ORACLE_HOME/bin:$PATH

export LD_LIBRARY_PATH=$ORACLE_HOME/lib:/lib:/usr/lib
export CLASSPATH=$ORACLE_HOME/jlib:$ORACLE_HOME/rdbms/jlib
```

#### 1.7 解压oracle安装包

```
su - oracle
cd $ORACLE_HOME
ll
unzip /opt/software/LINUX.X64_193000_db_home.zip 
```

#### 1.8 图形化安装

```
#修改sshd_config
vi /etc/ssh/sshd_config
X11Forwarding yes
```

```
cd $ORACLE_HOME
./runInstaller
```

使用Xstart

![image-20210819110854665](Oracle DataGuard.assets/image-20210819110854665.png)

![image-20210819110917237](Oracle DataGuard.assets/image-20210819110917237.png)

![image-20210819110926129](Oracle DataGuard.assets/image-20210819110926129.png)

![image-20210819110949485](Oracle DataGuard.assets/image-20210819110949485.png)

![image-20210819111008571](Oracle DataGuard.assets/image-20210819111008571.png)

![image-20210819111057036](Oracle DataGuard.assets/image-20210819111057036.png)

![image-20210819111104263](Oracle DataGuard.assets/image-20210819111104263.png)

![image-20210819111122077](Oracle DataGuard.assets/image-20210819111122077.png)

![image-20210819111133528](Oracle DataGuard.assets/image-20210819111133528.png)

![image-20210819111231353](Oracle DataGuard.assets/image-20210819111231353.png)

![image-20210819112305524](Oracle DataGuard.assets/image-20210819112305524.png)

![image-20210819112246391](Oracle DataGuard.assets/image-20210819112246391.png)

#### 1.9 创建监听

![image-20210819112740064](Oracle DataGuard.assets/image-20210819112740064.png)

![image-20210819112823677](Oracle DataGuard.assets/image-20210819112823677.png)

![image-20210819112831234](Oracle DataGuard.assets/image-20210819112831234.png)

![image-20210819112837167](Oracle DataGuard.assets/image-20210819112837167.png)

![image-20210819112847074](Oracle DataGuard.assets/image-20210819112847074.png)

![image-20210819112855095](Oracle DataGuard.assets/image-20210819112855095.png)

![image-20210819112914388](Oracle DataGuard.assets/image-20210819112914388.png)

![image-20210819112920689](Oracle DataGuard.assets/image-20210819112920689.png)

#### 1.10 创建数据库

![image-20210819113005700](Oracle DataGuard.assets/image-20210819113005700.png)

![image-20210819113014790](Oracle DataGuard.assets/image-20210819113014790.png)

![image-20210819113023200](Oracle DataGuard.assets/image-20210819113023200.png)

![image-20210819133843396](Oracle DataGuard.assets/image-20210819133843396.png)

实例名：orcl

![image-20210819134131398](Oracle DataGuard.assets/image-20210819134131398.png)

![image-20210819134552808](Oracle DataGuard.assets/image-20210819134552808.png)

![image-20210819134716703](Oracle DataGuard.assets/image-20210819134716703.png)

passwd：oracle

![image-20210819135716308](Oracle DataGuard.assets/image-20210819135716308.png)

![image-20210819135830454](Oracle DataGuard.assets/image-20210819135830454.png)

![image-20210819135839664](Oracle DataGuard.assets/image-20210819135839664.png)

![image-20210819135847275](Oracle DataGuard.assets/image-20210819135847275.png)

![image-20210819141201055](Oracle DataGuard.assets/image-20210819141201055.png)



### 2.主库配置

#### 2.1归档模式开启

```sql 
sqlplus / as sysdba
#查看数据是否是归档模式
SQL> archive log list;
#关停数据库
SQL> shutdown immediate
#开到mount模式下
SQL> startup mount; 
#给数据库开归档模式
SQL> alter database archivelog;
#开启数据库
SQL> alter database open;
#修改归档路径
SQL> alter system set log_archive_dest_1='location=/u01/archivelog';
#验证归档模式是否成功
SQL> archive log list;
```

![image-20210819142643253](Oracle DataGuard.assets/image-20210819142643253.png)

![image-20210819142817239](Oracle DataGuard.assets/image-20210819142817239.png)

#### 2.2设置数据库闪回

```SQL
#查看是否开启闪回
SQL> select flashback_on from v$database;

#设置大小
SQL> alter system set db_recovery_file_dest_size='2G'; 
#设置存放路径
SQL> alter system set db_recovery_file_dest='/u01/db_recovery_file_dest';
#开启闪回
SQL> alter database flashback on;

SQL> show parameter db_recovery
```

![image-20210819145634255](Oracle DataGuard.assets/image-20210819145634255.png)

![image-20210819145650166](Oracle DataGuard.assets/image-20210819145650166.png)

![image-20210819145713140](Oracle DataGuard.assets/image-20210819145713140.png)

![image-20210819145747650](Oracle DataGuard.assets/image-20210819145747650.png)

#### 2.3强制记录日志

```SQL
#查看是否打开强制记录日志
SQL> select force_logging from v$database;
#打来强制记录日志
SQL> alter database force logging;
```

![image-20210819150410476](Oracle DataGuard.assets/image-20210819150410476.png)

#### 2.4添加standby日志

```
SQL> select group#,bytes/1024/1024 from v$log;
```

standby日志添加：比主库在线日志组数多1个，大小相同。

```sql
alter database add standby logfile group 4 '/u01/app/oracle/fast_recovery_area/MEMA/onlinelog/standby4_redo_01.log' size 200M;

alter database add standby logfile group 5 '/u01/app/oracle/fast_recovery_area/MEMA/onlinelog/standby5_redo_02.log' size 200M;

alter database add standby logfile group 6 '/u01/app/oracle/fast_recovery_area/MEMA/onlinelog/standby6_redo_03.log' size 200M;

alter database add standby logfile group 7 '/u01/app/oracle/fast_recovery_area/MEMA/onlinelog/standby7_redo_04.log' size 200M;

SQL> select group#,bytes/1024/1024 from v$standby_log;
```

![image-20210819153325681](Oracle DataGuard.assets/image-20210819153325681.png)

#### 2.5 修改参数文件

```
alter system set log_archive_config='DG_CONFIG=(mema,memaDG)';

alter system set log_archive_dest_1='location=/u01/archivelog';

alter system set log_archive_dest_2='SERVICE=memaDG VALID_FOR=(ONLINE_LOGFILES,PRIMARY_ROLE) DB_UNIQUE_NAME=memaDG' scope=spfile;

alter system set log_archive_dest_state_1='enable';

alter system set log_archive_dest_state_2='enable';

alter system set db_file_name_convert='/u01/app/oracle/oradata/MEMADG/datafile','/u01/app/oracle/oradata/MEMA/datafile' scope=spfile;

alter system set log_file_name_convert='/u01/app/oracle/oradata/MEMADG/onlinelog','/u01/app/oracle/oradata/MEMA/onlinelog' scope=spfile;

alter system set db_unique_name='mema' scope=spfile;

alter system set fal_server='memaDG';

alter system set fal_client='mema';

alter system set standby_file_management='AUTO';

alter system set log_archive_format='%t_%s_%r.arc' scope=spfile;

shutdown immediate

startup
```



#### 2.6配置监听文件参数

```
cd $ORACLE_HOME/network/admin

vi listener.ora

SID_LIST_LISTENER =
 (SID_LIST =
 (SID_DESC =
 (GLOBAL_DBNAME = mema)
 (ORACLE_HOME = /u01/app/oracle/product/19.0.0/dbhome_1)
 (SID_NAME = mema)
 )
)

LISTENER =
  (DESCRIPTION_LIST =
    (DESCRIPTION =
      (ADDRESS = (PROTOCOL = TCP)(HOST = 192.168.56.211)(PORT = 1521))
      (ADDRESS = (PROTOCOL = IPC)(KEY = EXTPROC1521))
    )
  )

ADR_BASE_LISTENER = /u01/app/oracle
```

![image-20210831100220610](Oracle DataGuard.assets/image-20210831100220610.png)

#### 2.7配置tns配置文件

```
mema =
 (DESCRIPTION =
 (ADDRESS_LIST =
 (ADDRESS = (PROTOCOL = TCP)(HOST = 192.168.56.211)(PORT = 1521))
 )
 (CONNECT_DATA =
 (SERVICE_NAME = mema)
 )
 )

memaDG =
 (DESCRIPTION =
 (ADDRESS_LIST =
 (ADDRESS = (PROTOCOL = TCP)(HOST = 192.168.56.212)(PORT = 1521))
 )
 (CONNECT_DATA =
 (SERVICE_NAME = memaDG)
 )
 )
```

![image-20210831100249150](Oracle DataGuard.assets/image-20210831100249150.png)

#### 2.8重启监听

```
lsnrctl stop

lsnrctl start

lsnrctl status
```



#### 2.9拷贝参数文件

```shell
cd $ORACLE_HOME/dbs
#在该目录下进去sql
SQL> create pfile from spfile;

#退出sql，进入$ORACLE_HOME/dbs目录下
mv initmema.ora initmemaDG.ora

cp orapwmema orapwmemaDG

#将对应文件传输到备库
scp initmemaDG.ora orapwmemaDG oracle@192.168.56.212:/u01/app/oracle/product/19.0.0/dbhome_1/dbs

#在主库上删除传送到备库的文件
rm -f initmemaDG.ora

rm -f orapwmemaDG
```

(截图中的实例名有误)

![image-20210819163448389](Oracle DataGuard.assets/image-20210819163448389.png)

![image-20210819163537200](Oracle DataGuard.assets/image-20210819163537200.png)

![image-20210819164138995](Oracle DataGuard.assets/image-20210819164138995.png)

![image-20210819164148683](Oracle DataGuard.assets/image-20210819164148683.png)



### 3.备库配置

#### 3.1修改参数文件

```shell
#root用户下
cd $ORACLE_HOME/dbs
chown oracle:oinstall initmemaDG.ora
chown oracle:oinstall orapwmemaDG

#oracle用户下
#修改initmemaDG.ora文件
vi initmemaDG.ora
```

*.audit_file_dest='/u01/app/oracle/admin/==memaDG==/adump'

*.audit_trail='db'

*.compatible='19.0.0'

*.control_files='/u01/app/oracle/oradata/==MEMADG==/control01.ctl','/u01/app/oracle/oradata/==MEMADG==/control02.ctl'

*.db_block_size=8192

*.db_file_name_convert='/u01/app/oracle/oradata/==MEMA==/datafile','/u01/app/oracle/oradata/==MEMADG==/datafile'

*.db_name='mema'

*.db_recovery_file_dest_size=5368709120

*.db_recovery_file_dest==='/u01/app/oracle/fast_recovery_area/'==

*.db_unique_name='==memaDG=='

*.diagnostic_dest='/u01/app/oracle'

*.dispatchers='(PROTOCOL=TCP) (SERVICE===memaDGXDB==)'

*.enable_pluggable_database=true

*.fal_client='==memaDG=='

*.fal_server==='mema=='

*.local_listener='LISTENER_MEMA'

*.log_archive_config='DG_CONFIG=(==memaDG,mema==)'

*.log_archive_dest_1='location=/u01/archivelog'

*.log_archive_dest_2='SERVICE===mema== VALID_FOR=(ONLINE_LOGFILES,PRIMARY_ROLE) DB_UNIQUE_NAME===mema=='

*.log_archive_dest_state_1='enable'

*.log_archive_dest_state_2='enable'

*.log_archive_format='%t_%s_%r.arc'

*.log_file_name_convert='/u01/app/oracle/oradata/==MEMA==/onlinelog','/u01/app/oracle/oradata/==MEMADG==/onlinelog'

*.nls_language='AMERICAN'

*.nls_territory='AMERICA'

*.open_cursors=300

*.pga_aggregate_target=566m

*.processes=300

*.remote_login_passwordfile='EXCLUSIVE'

*.sga_target=1696m

*.standby_file_management='AUTO'

*.undo_tablespace='UNDOTBS1'



#### 3.2修改监听配置

```
cd $ORACLE_HOME/network/admin

vi listener.ora

LISTENER =
 (DESCRIPTION_LIST =
  (DESCRIPTION =
   (ADDRESS = (PROTOCOL = TCP)(HOST = 192.168.56.212)(PORT = 1521))
   (ADDRESS = (PROTOCOL = IPC)(KEY = EXTPROC1521))
  )
 )


SID_LIST_LISTENER =
 (SID_LIST =
 (SID_DESC =
 (GLOBAL_DBNAME = memaDG)
 (ORACLE_HOME = /u01/app/oracle/product/19.0.0/dbhome_1)
 (SID_NAME = memaDG)
 )
)

ADR_BASE_LISTENER = /u01/app/oracle 
```



#### 3.3创建文件目录

```
mkdir -p /u01/app/oracle/admin/orcldg/adump

mkdir -p /u01/app/oracle/oradata/ORCLDG/controlfile/

mkdir -p /u01/app/oracle/oradata/ORCLDG/datafile

mkdir -p /u01/app/oracle/oradata/ORCLDG/onlinelog/

mkdir -p /u01/archivelog

mkdir -p /u01/db_recovery_file_dest

mkdir -p /home/oracle/rman

chown -R oracle:oinstall /u01
```



#### 3.4配置tns

```
 cd /u01/app/oracle/product/19.0.0/dbhome_1/network/admin

vi tnsnames.ora

mema =
 (DESCRIPTION =
 (ADDRESS_LIST =
 (ADDRESS = (PROTOCOL = TCP)(HOST = 192.168.56.211)(PORT = 1521))
 )
 (CONNECT_DATA =
 (SERVICE_NAME = mema)
 )
 )

memaDG =
 (DESCRIPTION =
 (ADDRESS_LIST =
 (ADDRESS = (PROTOCOL = TCP)(HOST = 192.168.56.212)(PORT = 1521))
 )
 (CONNECT_DATA =
 (SERVICE_NAME = memaDG)
 )
 ) 
```

#### 3.5启动监听

```
lsnrctl start
```

#### 3.6启动数据库到nomount

```
export ORACLE_SID=memaDG
sqlplus / as sysdba

SQL> startup nomount pfile='/u01/app/oracle/product/19.0.0/dbhome_1/dbs/initmemaDG.ora'
```

![image-20210820092115766](Oracle DataGuard.assets/image-20210820092115766.png)

#### 3.7测试tns远程连接数据库

```
#两个节点的监听需要都开启
#主库备库都要测试齐全：
tnsping mema

tnsping memaDG

sqlplus sys/oracle@mema as sysdba

show parameter name;

sqlplus sys/oracle@memaDG as sysdba

show parameter name;
```

![image-20210831101325061](Oracle DataGuard.assets/image-20210831101325061.png)

![image-20210831101454720](Oracle DataGuard.assets/image-20210831101454720.png)

![image-20210831101553636](Oracle DataGuard.assets/image-20210831101553636.png)

#### 3.8 rman恢复数据库

```
rman target sys/oracle@mema auxiliary sys/oracle@memaDG

duplicate target database for standby from active database;

报错可以执行下列语句，但是最好解决报错问题

duplicate target database for standby from active database nofilenamecheck;
```

==**注意：备库的状态一定要是 not mounted**==

![image-20210831101729609](Oracle DataGuard.assets/image-20210831101729609.png)

(以下报错可以忽略)

![image-20210831101624639](Oracle DataGuard.assets/image-20210831101624639.png)

#### 3.9开始实时同步

```
SQL> alter database open;

SQL> alter database recover managed standby database using current logfile disconnect from session;
```

#### 3.10开启闪回

```
SQL> alter database recover managed standby database cancel;

SQL> shutdown immediate

SQL> startup mount

SQL> alter database flashback on;

SQL> alter database open;

SQL> alter database recover managed standby database using current logfile disconnect from session;
```

### 4 验证DG同步

#### 4.1查看archive_log_dest_2是否有error

```
col dest_name format a30

col error format a20

select dest_name,error from v$archive_dest;
```

![image-20210831094820674](Oracle DataGuard.assets/image-20210831094820674.png)

#### 4.2查看主库备库时间号

```
select max(sequence#) from v$archived_log;
```

主库：

![image-20210831094838799](Oracle DataGuard.assets/image-20210831094838799.png)

备库：

![image-20210831094855155](Oracle DataGuard.assets/image-20210831094855155.png)

#### 4.3执行日志切换，查看时间号

```
alter system archive log current;

select max(sequence#) from v$archived_log;
```

主库：

![image-20210831095015193](Oracle DataGuard.assets/image-20210831095015193.png)

备库：

![image-20210831095023627](Oracle DataGuard.assets/image-20210831095023627.png)

#### 4.4查看主备库状态

主库：

```
select switchover_status,database_role from v$database;

 

SWITCHOVER_STATUS  DATABASE_ROLE

------------        ----------------

TOSTANDBY           PRIMARY

 
```

![image-20210831095107534](Oracle DataGuard.assets/image-20210831095107534.png)

备库：

```
SWITCHOVER_STATUS  DATABASE_ROLE

---------------------        ---------------

NOTALLOWED         PHYSICAL STANDBY
```

![image-20210831095123772](Oracle DataGuard.assets/image-20210831095123772.png)

#### 4.5创表测试

```
create table sys.test (id number);

insert into sys.test(id) values (1);

alter system archive log current;

select * from sys.test;
```

主库：

![image-20210831095721819](Oracle DataGuard.assets/image-20210831095721819.png)

![image-20210831095810989](Oracle DataGuard.assets/image-20210831095810989.png)

![image-20210831095820823](Oracle DataGuard.assets/image-20210831095820823.png)

备库：

![image-20210831095842695](Oracle DataGuard.assets/image-20210831095842695.png)

### 5 主备库切换

#### 5.1 switchover

主库：

```
SQL> select switchover_status,database_role from v$database;

 

SWITCHOVER_STATUS    DATABASE_ROLE

------------------------------------  --------------------------

TO STANDBY            PRIMARY
```

switchover_status状态为to standby或sessions active表明可以进行切换

```
SQL> alter database commit to switchover to physical standby;

SQL> startup mount

SQL> select database_role from v$database;
```

备库：

```
SQL> select switchover_status,database_role from v$database;

 

SWITCHOVER_STATUS    DATABASE_ROLE

---------------------------------     ------------------------------

TO PRIMARY            PHYSICAL STANDBY

```

switchover_status状态为to standby或sessions active表明可以进行切换

```
SQL> alter database commit to switchover to primary with session shutdown;

SQL> alter database open;

SQL> select switchover_status,database_role,open_mode from v$database;
```

原先的主库(现从主库转为备库):

```
SQL> alter database open;

SQL> alter database recover managed standby database using current logfile disconnect from session;
```

 
