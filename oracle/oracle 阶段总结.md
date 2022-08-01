### 1 用vagrant初始化一台linux虚拟机，添加hostonly网卡和public网卡

```
vagrant box list
vagrant init centos-7

#使用 Visual Studio Code 添加网卡
code vagrantfile	--hostonly网卡的IP：192.168.56.200
```

![image-20210817095612243](oracle 阶段总结.assets/image-20210817095612243.png)

```
#启动虚拟机
vagrant up

#连接虚拟机
vagrant ssh

#修改ssh
sudo -i
vi /etc/ssh/sshd_config		
--将PasswordAuthentication改为 yes

systemctl restart sshd
#给root设置密码
echo "Mema_1234" | passwd --stdin root
```

### 2 完成linux系统的初始化设置，修改主机名，调整时区

```
hostnamectl set-hostname oracle-19c
bash

timedatectl set-timezone 'Asia/Shanghai'
date

yum install -y unzip
yum install -y rlwrap
```

### 3 安装oracle数据库

#### 3.1 安装前准备

##### 3.1.1 安装包准备

安装包放置路径：

```
/opt/software
```

Oracle19.3数据库安装包:

![image-20210817102617649](oracle 阶段总结.assets/image-20210817102617649.png)

Oracle19.8升级补丁包:

![image-20210817102707468](oracle 阶段总结.assets/image-20210817102707468.png)

Opatch高版本包：

![image-20210817102716587](oracle 阶段总结.assets/image-20210817102716587.png)

#### 3.2 安装数据库软件

##### 3.2.1 编辑内核参数

```
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
[root@oracle-19c ~]# sysctl -p
```

##### 3.2.2 修改访问限制

```
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

##### 3.2.3 安装rpm包

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

##### 3.2.4 创建用户组和用户及目录

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

##### 3.2.5 修改firewall和selinux

```
vim /etc/selinux/config

SELINUX=disabled

systemctl stop firewalld
systemctl disable firewalld
```

##### 3.2.6 编辑bash_profile

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

##### 3.2.7 解压oracle安装包

```
[root@oracle-19c ~]# su - oracle
[oracle@oracle-19c ~]$ cd $ORACLE_HOME
[oracle@oracle-19c ~]$ ll
total 0
[oracle@oracle-19c ~]$ unzip /opt/software/LINUX.X64_193000_db_home.zip 
```

##### 3.2.8 图形化安装

```
#为了使用xstart，需要安装
yum install -y xorg-x11-xauth

#修改sshd_config
vi /etc/ssh/sshd_config
X11Forwarding yes
```

```
cd $ORACLE_HOME
./runInstaller
```

使用Xstart

![image-20210817111957992](oracle 阶段总结.assets/image-20210817111957992.png)

点击仅设置软件

![image-20210817112029367](oracle 阶段总结.assets/image-20210817112029367.png)

点击单实例数据库安装

![image-20210817112219621](oracle 阶段总结.assets/image-20210817112219621.png)

点击企业版

![image-20210817112237771](oracle 阶段总结.assets/image-20210817112237771.png)

选择默认oracle base

![image-20210817112252215](oracle 阶段总结.assets/image-20210817112252215.png)

选择默认orainventory位置

![image-20210817112304064](oracle 阶段总结.assets/image-20210817112304064.png)

选择默认组

![image-20210817112318060](oracle 阶段总结.assets/image-20210817112318060.png)

不设置脚本

![image-20210817112337933](oracle 阶段总结.assets/image-20210817112337933.png)

先决条件检查

![image-20210817112816239](oracle 阶段总结.assets/image-20210817112816239.png)

总结

![image-20210817112834547](oracle 阶段总结.assets/image-20210817112834547.png)

安装产品

![image-20210817112852930](oracle 阶段总结.assets/image-20210817112852930.png)

执行脚本

![image-20210817113128931](oracle 阶段总结.assets/image-20210817113128931.png)

![image-20210817113249737](oracle 阶段总结.assets/image-20210817113249737.png)

产品安装完成

![image-20210817113230763](oracle 阶段总结.assets/image-20210817113230763.png)

##### 3.2.9 升级数据库

###### 3.2.9.1 更新高版本Opatch

```
cd $ORACLE_HOME
mv OPatch/ OPatch_old
unzip /opt/software/p6880880_190000_Linux-x86-64.zip
```

###### 3.2.9.2 解压19.7数据库升级补丁

```
unzip /opt/software/p31281355_190000_Linux-x86-64.zip
```

###### 3.2.9.3 打补丁

```
yum install -y psmisc
```

在31281355文件夹中执行

![image-20210817114641378](oracle 阶段总结.assets/image-20210817114641378.png)

```
/u01/app/oracle/product/19.0.0/dbhome_1/OPatch/opatch apply
```

##### 3.2.9.4 数据库软件升级成功



### 4 创建监听

![image-20210817160912096](oracle 阶段总结.assets/image-20210817160912096.png)

netca图形化创建

![image-20210817160956198](oracle 阶段总结.assets/image-20210817160956198.png)

添加监听

![image-20210817161246384](oracle 阶段总结.assets/image-20210817161246384.png)

设置监听名字

![image-20210817161300701](oracle 阶段总结.assets/image-20210817161300701.png)

设置端口

![image-20210817161312408](oracle 阶段总结.assets/image-20210817161312408.png)

![image-20210817161326987](oracle 阶段总结.assets/image-20210817161326987.png)

![image-20210817161340296](oracle 阶段总结.assets/image-20210817161340296.png)

创建成功

![image-20210817161419716](oracle 阶段总结.assets/image-20210817161419716.png)

### 5 创建数据库

![image-20210817161506114](oracle 阶段总结.assets/image-20210817161506114.png)

图形化创建数据库

![image-20210817162034755](oracle 阶段总结.assets/image-20210817162034755.png)

高级安装

管理口令都为  oracle

数据库名称为  orcl

![image-20210817162055443](oracle 阶段总结.assets/image-20210817162055443.png)

创建orcl实例

![image-20210817162125649](oracle 阶段总结.assets/image-20210817162125649.png)

![image-20210817162231383](oracle 阶段总结.assets/image-20210817162231383.png)

![image-20210817162252659](oracle 阶段总结.assets/image-20210817162252659.png)

![image-20210817162305066](oracle 阶段总结.assets/image-20210817162305066.png)

![image-20210817162322611](oracle 阶段总结.assets/image-20210817162322611.png)

![image-20210817162336039](oracle 阶段总结.assets/image-20210817162336039.png)

![image-20210817162428279](oracle 阶段总结.assets/image-20210817162428279.png)

![image-20210817162503123](oracle 阶段总结.assets/image-20210817162503123.png)

![image-20210817162529834](oracle 阶段总结.assets/image-20210817162529834.png)

![image-20210817162548621](oracle 阶段总结.assets/image-20210817162548621.png)

![image-20210817162739093](oracle 阶段总结.assets/image-20210817162739093.png)

![image-20210817162759400](oracle 阶段总结.assets/image-20210817162759400.png)

![image-20210817162816233](oracle 阶段总结.assets/image-20210817162816233.png)

![image-20210817162833160](oracle 阶段总结.assets/image-20210817162833160.png)



### 6 启动pdb1创建测试用户，分配表空间

```
create pluggable database pdb1 admin user mema01  identified by Mema_1234 file_name_convert=('/u01/app/oracle/oradata/ORCL/pdbseed','/u01/app/oracle/oradata/ORCL/orcl1pdb2');

alter pluggable database pdb1 open;

create tablespace test01 datafile '/u01/app/oracle/product/19.0.0/dbhome_1/data/test01.dbf' size 100M autoextend on next 100M;

create user mema01 identified by Mema_1234
default tablespace test01;

select default_tablespace from dba_users where username='mema01';

grant resource to mema01;
```

### 7 为测试用户创建表tab1，添加100万条数据

```
conn user01/Mema_1234@host1:5241

CREATE TABLE tab1 (
id int,
name varchar(20),
data1 int,
data2 int,
data3 int
);

insert into tab1 select rownum as id,
dbms_random.string('1',trunc(dbms_random.value(3,8))),
trunc(dbms_random.value(0,100)),
trunc(dbms_random.value(0,100)),
trunc(dbms_random.value(0,100))
from dual
connect by level <=1000000;
```

### 8 创建各种表，普通表，堆表，列式存储表，各种分区表（四种），每个表插入10万条数据

#### 普通表

```
CREATE TABLE comm_student (
id bigint identity,
name varchar(20),
birthday date,
math int,
english int,
science int
);

insert into comm_student 
select
dbms_random.string('1',trunc(dbms_random.value(3,8))),
current_date()-365*20+dbms_random.value(-365,365),
trunc(dbms_random.value(40,100)),
trunc(dbms_random.value(40,100)),
trunc(dbms_random.value(40,100))
from dual
connect by level <=1000000;

commit;
```

#### 堆表

```
CREATE TABLE heap_student (
id bigint identity,
name varchar(20),
birthday date,
math int,
english int,
science int
)
STORAGE (BRANCH(4,2));

insert into heap_student 
select
dbms_random.string('1',trunc(dbms_random.value(3,8))),
current_date()-365*28+dbms_random.value(-366,366),
trunc(dbms_random.value(0,100)),
trunc(dbms_random.value(0,100)),
trunc(dbms_random.value(0,100))
from dual
connect by level <=1000000;

commit;
```

#### 列存储表

```
CREATE HUGE TABLE huge_student (
id bigint,
name varchar(20),
birthday date,
math int,
english int,
science int
);

insert into huge_student 
select ROWNUM AS id,
dbms_random.string('1',trunc(dbms_random.value(3,8))),
current_date()-365*28+dbms_random.value(-366,366),
trunc(dbms_random.value(0,100)),
trunc(dbms_random.value(0,100)),
trunc(dbms_random.value(0,100))
from dual
connect by level <=100000;

commit;
```

#### 分区表

###### 1）范围分区

```
CREATE TABLE RANG_STUDENT(
id bigint,
name varchar(20),
city varchar(10),
birthday date,
tel varchar(20),
email varchar(50),
math int,
english int,
science int
)
PARTITION BY RANGE (math)(
PARTITION FALED VALUES LESS THAN ('45'),
PARTITION BAD VALUES LESS THAN ('60'),
PARTITION GOOD VALUES LESS THAN ('80'),
PARTITION EXCELLENT VALUES EQU OR LESS THAN (MAXVALUE)
);

insert into RANG_STUDENT 
select
  level,
  dbms_random.string('1',trunc(dbms_random.value(3,8))),
  get_city(),
  current_date()-365*20+dbms_random.value(-365*3,365*3),
  to_char(10000000000+floor(dbms_random.value(3111111111,3999999999))),
  dbms_random.string('L',8)||'@'||dbms_random.string('L',5)||'.com',
  trunc(dbms_random.value(40,100)),
  trunc(dbms_random.value(40,100)),
  trunc(dbms_random.value(40,100))
  from dual
connect by level <=100000;
commit;
```

###### 2）列表分区

```
CREATE TABLE LIST_STUDENT(
id bigint,
name varchar(20),
city varchar(10),
birthday date,
tel varchar(20),
email varchar(50),
math int,
english int,
science int
)
PARTITION BY LIST(city)(                         
PARTITION p1 VALUES ('北京', '天津'),                        
PARTITION p2 VALUES ('上海', '合肥'),                        
PARTITION p3 VALUES ('武汉', '长沙'),                        
PARTITION p4 VALUES ('广州', '深圳'),
PARTITION P0 VALUES (DEFAULT)                        
);

insert into LIST_STUDENT 
select
  level,
  dbms_random.string('1',trunc(dbms_random.value(3,8))),
  get_city(),
  current_date()-365*20+dbms_random.value(-365*3,365*3),
  to_char(10000000000+floor(dbms_random.value(3111111111,3999999999))),
  dbms_random.string('L',8)||'@'||dbms_random.string('L',5)||'.com',
  trunc(dbms_random.value(40,100)),
  trunc(dbms_random.value(40,100)),
  trunc(dbms_random.value(40,100))
  from dual
connect by level <=100000;
```

###### 3）哈希分区

```
CREATE TABLE HASH_STUDENT(
id bigint,
name varchar(20),
city varchar(10),
birthday date,
tel varchar(20),
email varchar(50),
math int,
english int,
science int
)
PARTITION BY HASH(name)(             
PARTITION p1,            
PARTITION p2,            
PARTITION p3,            
PARTITION p4            
); 

insert into HASH_STUDENT 
select
  level,
  dbms_random.string('1',trunc(dbms_random.value(3,8))),
  get_city(),
  current_date()-365*20+dbms_random.value(-365*3,365*3),
  to_char(10000000000+floor(dbms_random.value(3111111111,3999999999))),
  dbms_random.string('L',8)||'@'||dbms_random.string('L',5)||'.com',
  trunc(dbms_random.value(40,100)),
  trunc(dbms_random.value(40,100)),
  trunc(dbms_random.value(40,100))
  from dual
connect by level <=100000;
```

###### 4）间隔分区

```
CREATE TABLE INTE_STUDENT(
id bigint,
name varchar(20),
city varchar(10),
birthday date,
tel varchar(20),
email varchar(50),
math int,
english int,
science int
)
PARTITION BY RANGE (birthday)  INTERVAL(NUMTOYMINTERVAL(1,'MONTH'))
(
PARTITION "PART_1" VALUES LESS THAN (TO_DATE('1900-01-01 00:00:0','YYYY-MM-DD HH24:MI:SS'))
);

insert into INTE_STUDENT 
select
  level,
  dbms_random.string('1',trunc(dbms_random.value(3,8))),
  get_city(),
  current_date()-365*20+dbms_random.value(-365*3,365*3),
  to_char(10000000000+floor(dbms_random.value(3111111111,3999999999))),
  dbms_random.string('L',8)||'@'||dbms_random.string('L',5)||'.com',
  trunc(dbms_random.value(40,100)),
  trunc(dbms_random.value(40,100)),
  trunc(dbms_random.value(40,100))
  from dual
connect by level <=100000;
```

### 9 导出数据

```
dexp user01/Mema_1234@host1:5241 SCHEMAS=USER01 DIRECTORY=/opt/dm8/data/memadb1/imp/ FILE=user01.DMP LOG=user01.log
```

### 10 初始化第二个实例，数据库名称DB2

```
dminit PAGE_SIZE=32 EXTENT_SIZE=32 CHARSET=1 CASE_SENSITIVE=0 LENGTH_IN_CHAR=0 BLANK_PAD_MODE=1 DB_NAME=memadb2 PATH=/opt/dm8/data port_num=5242
```

### 11 注册数据库实例到Systemd，实现自动启停

```
cd /opt/dm8/script/root
./dm_service_installer.sh -t dmserver -p memadb2 -dm_ini /opt/dm8/data/memadb2/dm.ini
systemctl start DmServicememadb2
```

### 12 启动DB2，导入数据； 脱机备份DB1

```
dimp user01/Mema_1234@host1:5242 DIRECTORY=/opt/dm8/data/memadb1/imp/  FILE=user01.DMP  LOG=user02.log 

systemctl stop DmServicememadb1

dmrman

backup database '/opt/dm8/data/memadb1/dm.ini' full backupset '/opt/dm8/data/memadb1/testdb_full_bak_01';
```

### 13 初始化数据库DB3，用DB1脱机备份集恢复

```
dminit PAGE_SIZE=32 EXTENT_SIZE=32 CHARSET=1 CASE_SENSITIVE=0 LENGTH_IN_CHAR=0 BLANK_PAD_MODE=1 DB_NAME=memadb3 PATH=/opt/dm8/data port_num=5243

dmrman

RESTORE DATABASE '/opt/dm8/data/memadb3/dm.ini' FROM BACKUPSET '/opt/dm8/data/memadb1/testdb_full_bak_01';

RECOVER DATABASE '/opt/dm8/data/memadb3/dm.ini' FROM BACKUPSET '/opt/dm8/data/memadb1/testdb_full_bak_01';

RECOVER DATABASE '/opt/dm8/data/memadb3/dm.ini' UPDATE DB_MAGIC;
```

### 14 注册数据库实例到Systemd，实现自动启停

```
cd /opt/dm8/script/root
./dm_service_installer.sh -t dmserver -p memadb3 -dm_ini /opt/dm8/data/memadb3/dm.ini
systemctl start DmServicememadb3
```

### 15 设置DB1数据库为归档方式

```
alter database mount;
alter database archivelog;
alter database add archivelog 'type=local,dest=/opt/dm8/data/memadb1/arch,file_size=256,space_limit=0';
alter database open;
```

### 16 在线备份数据库DB1

```
backup database;
```

### 17 向DB1第一张测试表tab1添加1000万条数据，观察归档日志形成

```
insert into tab1 select rownum as id,
dbms_random.string('1',trunc(dbms_random.value(3,8))),
trunc(dbms_random.value(0,100)),
trunc(dbms_random.value(0,100)),
trunc(dbms_random.value(0,100))
from dual
connect by level <=10000000;
```

### 18 记录时间值T1

```
host date;
Thu Aug  5 15:46:08 CST 2021
```

### 19 删除DB1的第一张表tab1

```
drop table tab1;
commit;
host date;
```

### 20 初始化数据库DB4，在DB4上用DB1的在线备份集和归档日志恢复数据库到T1时间

```
dminit PAGE_SIZE=32 EXTENT_SIZE=32 CHARSET=1 CASE_SENSITIVE=0 LENGTH_IN_CHAR=0 BLANK_PAD_MODE=1 DB_NAME=memadb4 PATH=/opt/dm8/data port_num=5244

restore database '/opt/dm8/data/memadb4/dm.ini' from backupset '/opt/dm8/data/memadb1/bak/DB_memadb1_FULL_20210805_152948_537150';

recover database '/opt/dm8/data/memadb4/dm.ini' with archivedir '/opt/dm8/data/memadb1/arch' until time '2021-08-05 15:50:00';

recover database '/opt/dm8/data/memadb4/dm.ini' update db_magic;
```

### 21 注册数据库实例到Systemd，实现自动启停

```
cd /opt/dm8/script/root
./dm_service_installer.sh -t dmserver -p memadb4 -dm_ini /opt/dm8/data/memadb4/dm.ini
systemctl start DmServicememadb4
```

### 22 启动DB4，确认tab1表已经恢复

```
disql user01/Mema_1234@host1:5244

select count(*) from tab1;
```

### 23 将DB4的tab1表导出，然后导入回DB1

```
dexp USERID=user01/Mema_1234@host1:5244 file=tab1.dmp DIRECTORY=/opt/dm8/data/memadb4/dmp TABLES=user01.tab1

dimp user01/Mema_1234@host1:5241 file=tab1.dmp DIRECTORY=/opt/dm8/data/memadb4/dmp
```

### 24 设置DB4为归档方式

```
alter database mount;
alter database archivelog;
alter database add archivelog 'type=local,dest=/opt/dm8/data/memadb4/arch,file_size=256,space_limit=0';
alter database open;
```

### 25 通过作业系统定期备份DB4，每5分钟一次在线全备，每10分钟一次归档备份

```
call SP_INIT_JOB_SYS(1);



call SP_CREATE_JOB('在线全备DB4',1,0,'',0,0,'',0,'');

call SP_JOB_CONFIG_START('在线全备DB4');

call SP_ADD_JOB_STEP('在线全备DB4', '在线全备', 6, '09000000/opt/dm8/data/memadb4/bak/', 0, 0, 0, 0, NULL, 0);

call SP_ADD_JOB_SCHEDULE('在线全备DB4', '每5分钟', 1, 1, 1, 0, 5, '00:00:00', '23:59:59', '2021-08-05 16:46:21', NULL, '');

call SP_JOB_CONFIG_COMMIT('在线全备DB4');




call SP_CREATE_JOB('归档备份',1,0,'',0,0,'',0,'');

call SP_JOB_CONFIG_START('归档备份');

call SP_ADD_JOB_STEP('归档备份', 'pase1', 6, '39000000/opt/dm8/data/memadb4/arch/', 0, 0, 0, 0, NULL, 0);

call SP_ADD_JOB_SCHEDULE('归档备份', '每十分钟', 1, 1, 1, 0, 10, '00:00:00', '23:59:59', '2021-08-05 16:53:32', NULL, '');

call SP_JOB_CONFIG_COMMIT('归档备份');
```

### 26 确认定期备份执行成功

