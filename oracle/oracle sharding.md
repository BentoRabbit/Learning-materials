# Oracle sharding 安装部署



| 主机名 | IP             | 操作系统 | 数据库 |
| ------ | -------------- | -------- | ------ |
| node1  | 192.168.56.131 | ol7      | 19.3   |
| node2  | 192.168.56.132 | ol7      | 19.3   |
| node3  | 192.168.56.133 | ol7      | 19.3   |

| 用户   | 密码      |
| ------ | --------- |
| root   | Mema_1234 |
| oracle | oracle    |



### 1.安装Oracle

==在所有节点安装数据库软件（不创建DB）==

**备注：在所有节点确保执行root.sh**

#### 1.1 编辑内核参数

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
sysctl -p
```

#### 1.2 修改访问限制

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
export ORACLE_SID=shard

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
cd $ORACLE_HOME
./runInstaller
```



### 2. 安装Oracle Database 19c Global Service Manager (GSM/GDS)

==在主节点node1上进行==

#### 2.1 解压GSM软件

```sql
unzip /opt/software/LINUX.X64_193000_gsm.zip
```

#### 2.2 oracle用户下进行安装

```sql
./runInstaller
```

![image-20210915160106460](oracle sharding.assets/image-20210915160106460.png)

### 3. 创建Shard Catalog Database

**在主节点dbca创建shard数据库实例,这里需要注意的是选择非CDB选项，字符集使用UTF8（zhs16gbk不支持），启用OMF,归档以及快闪区**

![image-20210915131532788](oracle sharding.assets/image-20210915131532788.png)

![image-20210915131545079](oracle sharding.assets/image-20210915131545079.png)

![image-20210915131807625](oracle sharding.assets/image-20210915131807625.png)

![image-20210915132026950](oracle sharding.assets/image-20210915132026950.png)

![image-20210915132953549](oracle sharding.assets/image-20210915132953549.png)

![image-20210915133618313](oracle sharding.assets/image-20210915133618313.png)

![image-20210915133807515](oracle sharding.assets/image-20210915133807515.png)

![image-20210915133932023](oracle sharding.assets/image-20210915133932023.png)

![image-20210915160705872](oracle sharding.assets/image-20210915160705872.png)

密码：oracle

![image-20210915134033399](oracle sharding.assets/image-20210915134033399.png)

![image-20210915135018796](oracle sharding.assets/image-20210915135018796.png)

![image-20210915135808550](oracle sharding.assets/image-20210915135808550.png)



### 4.设置OracleSharding Manage和路由层

4.1-4.4都是在主节点操作

#### 4.1：创建用户

```
SQL> alter user gsmcatuser identified by oracle account unlock;
```

**备注：创建gsmcatuser用户目的是可以让shard director通过此用户连接到shard catalog数据库**

![image-20210915142245764](oracle sharding.assets/image-20210915142245764.png)

#### 4.2：创建管理用户gsmadmin

```
SQL> create user gsmadmin identified by oracle;
SQL> grant connect, create session, gsmadmin_role to gsmadmin;
SQL> grant inherit privileges on user SYS to GSMADMIN_INTERNAL;
SQL> exec DBMS_SCHEDULER.SET_AGENT_REGISTRATION_PASS('oracle');
```

**备注： 1、在catalog数据库创建管理用户gsmadmin用于存储Sharding节点管理信息，以及GDSCTL接口可以通过gsmadmin用户连接到catalog数据库**

![image-20210915142849669](oracle sharding.assets/image-20210915142849669.png)

#### 4.3 进入到GDSCTL命令行，创建shard catalog

```
./gdsctl

GDSCTL> create shardcatalog -database 192.168.56.131:1521:shard -chunks 12 -user gsmadmin/oracle -sdb shard -region region1,region2
```

![image-20210915144210922](oracle sharding.assets/image-20210915144210922.png)

#### 4.4 创建并启动shard director。并设置操作系统安全认证

```
GDSCTL> add gsm -gsm sharddirector1 -listener 1522 -pwd oracle -catalog 192.168.56.131:1521:shard -region region1
```

参数含义：

```
-gsm: 指定shard director名称
-listener: 指定shard director的监听端口，注意不能与数据库的listener端口冲突
-catalog: 指定catalog database 信息，catalog数据库的主机名:监听器port: catalog 数据库db_name
```

![image-20210915144434109](oracle sharding.assets/image-20210915144434109.png)

#### 4.4.2：启动director

```
GDSCTL> start gsm -gsm sharddirector1
```

![image-20210915144525050](oracle sharding.assets/image-20210915144525050.png)

#### 4.4.3：添加操作系统认证

```
GDSCTL> add credential -credential region1_cred -osaccount oracle -ospassword oracle

GDSCTL> exit
```

![image-20210915144602297](oracle sharding.assets/image-20210915144602297.png)

#### 4.5：在其余节点注册Scheduler agents, 并创建好oradata和fast_recovery_area文件夹。

node2:

```
schagent -start

schagent -status

mkdir /u01/app/oracle/oradata

mkdir /u01/app/oracle/fast_recovery_area

echo oracle | schagent -registerdatabase 192.168.56.131 8080
```

![image-20210915145429446](oracle sharding.assets/image-20210915145429446.png)

![image-20210915162425304](oracle sharding.assets/image-20210915162425304.png)

node3:

```
schagent -start

schagent -status

mkdir /u01/app/oracle/oradata

mkdir /u01/app/oracle/fast_recovery_area

echo oracle | schagent -registerdatabase 192.168.56.131 8080
```

![image-20210915162530608](oracle sharding.assets/image-20210915162530608.png)



### 5. 开始布署SharedDatabase

本例将布署System-ManagedSDB。

主节点进行

#### 5.1 添加shardgroup

```sql
[oracle@node1 ~]$ gdsctl

GDSCTL> set gsm -gsm sharddirector1

GDSCTL> connect gsmadmin/oracle

GDSCTL> add shardgroup -shardgroup primary_shardgroup -deploy_as primary -region region1
```

**备注：
 shardgroup是一组shard的集合，shardgroup名称为primary_shardgroup，-deploy_as primary表示这个group中的shard都是主库。**

![image-20210915163035166](oracle sharding.assets/image-20210915163035166.png)

#### 5.2 创建shard

node2：

```sql
GDSCTL> add invitednode node2

GDSCTL> create shard -shardgroup primary_shardgroup -destination node2 -credential region1_cred -sys_password oracle 

The operation completed successfully
DB Unique Name: sh1

```

![image-20210917142113185](oracle sharding.assets/image-20210917142113185.png)

node3：

```sql
GDSCTL> add invitednode node3

GDSCTL> create shard -shardgroup primary_shardgroup -destination node3 -credential region1_cred -sys_password oracle

The operation completed successfully
DB Unique Name: sh21

```

![image-20210917150253189](oracle sharding.assets/image-20210917150253189.png)

附删除shard方式

```sql
-REMOVE SHARD -SHARD{shard_name_list | ALL} | -SHARDSPACE shardspace_list |    -SHARDGROUP shardgroup_list} [-FORCE]

-remove shard -shard sh21 -force

-remove shard -shard sh1 -force

--primary_shardgroup

--shardspaceora

```

#### 5.3 查看shard节点配置信息

```sql
GDSCTL>config shard

Name                Shard Group         Status    State       Region    Availability 
----                -----------         ------    -----       ------    ------------ 
sh1                 primary_shardgroup  U         none        region1   -            
sh2                primary_shardgroup  U         none        region1   -            

由于还未部署，state为none

```

![image-20210917150328612](oracle sharding.assets/image-20210917150328612.png)

#### 5.4 查看gsm状态信息

```sql
GDSCTL>status gsm
```

![image-20210917150350715](oracle sharding.assets/image-20210917150350715.png)

#### 5.5 利用GDS自动部署shard节点数据库

```sql
GDSCTL>deploy
```

![image-20210917150432919](oracle sharding.assets/image-20210917150432919.png)

备注：
 1、deploy命令会调用远程每一个节点上的dbca去静默安装sharded database
 2、可以通过查看dbca日志跟踪每个节点的安装进度
 3、deploy过程会持续一段时间，中间没有输出过程

```sql
 dbca日志：$ORACLE_BASE/cfgtoollogs/dbca/实例名/trace.log 

[oracle@node2 sh1]$ tail -100f /u01/app/oracle/cfgtoollogs/dbca/sh1/trace.log_2018-10-16_03-00-25-PM 
123
deploy: examining configuration...
deploy: deploying primary shard 'sh1' ...
deploy: network listener configuration successful at destination 'node2'
deploy: starting DBCA at destination 'node2' to create primary shard 'sh1' ...
deploy: deploying primary shard 'sh21' ...
deploy: network listener configuration successful at destination 'node3'
deploy: starting DBCA at destination 'node3' to create primary shard 'sh21' ...
deploy: waiting for 2 DBCA primary creation job(s) to complete...
deploy: waiting for 2 DBCA primary creation job(s) to complete...
deploy: waiting for 2 DBCA primary creation job(s) to complete...
deploy: waiting for 2 DBCA primary creation job(s) to complete...
deploy: waiting for 2 DBCA primary creation job(s) to complete...
deploy: waiting for 2 DBCA primary creation job(s) to complete...
deploy: DBCA primary creation job succeeded at destination 'node3' for shard 'sh21'
deploy: waiting for 1 DBCA primary creation job(s) to complete...
deploy: DBCA primary creation job succeeded at destination 'node2' for shard 'sh1'
deploy: requesting Data Guard configuration on shards via GSM
deploy: shards configured successfully
The operation completed successfully
部署完毕

```

#### 5.6 再次查看shard数据库状态

```sql
GDSCTL>config shard   

status状态ok已部署完毕
```

![image-20210917154445706](oracle sharding.assets/image-20210917154445706.png)

### 6. 建立service

#### 6.1：创建服务

```
add service -service oltp_rw_srvc -role primary
```

![image-20210917155129608](oracle sharding.assets/image-20210917155129608.png)

#### 6.2：启动服务

```
start service -service oltp_rw_srvc
```

#### 6.3：查看服务状态

```
status service
```

![image-20210917155153606](oracle sharding.assets/image-20210917155153606.png)

### 7. 创建用户并授权

```
alter session enable shard ddl;

--创建应用用户app_schema
create user app_schema identified by oracle;

--对用户授权
grant all privileges to app_schema;

grant gsmadmin_role to app_schema; 

grant select_catalog_role to app_schema;

grant connect, resource to app_schema;

grant dba to app_schema;

grant execute on dbms_crypto to app_schema;
```

![image-20210917155524074](oracle sharding.assets/image-20210917155524074.png)

### 8. 利用应用用户登录，创建sharded table和duplicated table

#### 8.1 **创建表空间集合**

```
conn app_schema/oracle

alter session enable shard ddl;
 
CREATE TABLESPACE SET TSP_SET_1 using template (datafile size 100m extent management local segment space management auto );
 
CREATE TABLESPACE products_tsp datafile size 100m extent management local uniform size 1m;
```

备注： 1、创建TSP_SET_1表空间集是提供给以下customers，orders，lineitems，这3个sharded table使用。products_tsp表空间是用于duplicate表products使用。 2、TABLESPACE SET只有sharding环境才能创建，并且需要在catalog数据库以sdb用户创建 3、TABLESPACE SET中的表空间是bigfile，每一个表空间会自动创建，其总数量与chunks相同（所有节点chunks之和）

![image-20210917155734424](oracle sharding.assets/image-20210917155734424.png)

#### 8.2 **创建表家族**

```
-- Create sharded table family
CREATE SHARDED TABLE Customers
    (
    CustId VARCHAR2(60) NOT NULL,
    FirstName VARCHAR2(60),
    LastName VARCHAR2(60),
    Class VARCHAR2(10),
    Geo VARCHAR2(8),
    CustProfile VARCHAR2(4000),
    Passwd RAW(60),
    CONSTRAINT pk_customers PRIMARY KEY (CustId),
    CONSTRAINT json_customers CHECK (CustProfile IS JSON)
    ) TABLESPACE SET TSP_SET_1
   PARTITION BY CONSISTENT HASH (CustId) PARTITIONS AUTO;
```

![image-20210917155928107](oracle sharding.assets/image-20210917155928107.png)

```
 CREATE SHARDED TABLE Orders
    (
    OrderId INTEGER NOT NULL,
    CustId VARCHAR2(60) NOT NULL,
    OrderDate TIMESTAMP NOT NULL,
    SumTotal NUMBER(19,4),
    Status CHAR(4),
    constraint pk_orders primary key (CustId, OrderId),
    constraint fk_orders_parent foreign key (CustId)
    references Customers on delete cascade
   ) partition by reference (fk_orders_parent);
CREATE SEQUENCE Orders_Seq;
CREATE SHARDED TABLE LineItems
    (
    OrderId INTEGER NOT NULL,
    CustId VARCHAR2(60) NOT NULL,
    ProductId INTEGER NOT NULL,
    Price NUMBER(19,4),
    Qty NUMBER,
    constraint pk_items primary key (CustId, OrderId, ProductId),
    constraint fk_items_parent foreign key (CustId, OrderId)
    references Orders on delete cascade
    ) partition by reference (fk_items_parent);
-- duplicated table
CREATE DUPLICATED TABLE Products
    (
    ProductId INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    Name VARCHAR2(128),
    DescrUri VARCHAR2(128),
    LastPrice NUMBER(19,4)
    ) TABLESPACE products_tsp;
```

备注：  1、如上创建了customers、orders、lineitems3张表，均为shared  table，三张表组成了表家族，其中customers是根表，orders以及lineitems表为子表，他们按照sharding key  （custid）根表的主键进行分区 2、customers表partitioning by consistent hash.主要作用是打散数据

![image-20210917161545266](oracle sharding.assets/image-20210917161545266.png)

#### 8.3 创建function，目的是为了后面的DEMO：

```
CREATE OR REPLACE FUNCTION PasswCreate(PASSW IN RAW)
RETURN RAW
IS
Salt RAW(8);
BEGIN
Salt := DBMS_CRYPTO.RANDOMBYTES(8);
RETURN UTL_RAW.CONCAT(Salt, DBMS_CRYPTO.HASH(UTL_RAW.CONCAT(Salt,
PASSW), DBMS_CRYPTO.HASH_SH256));
END;
/
CREATE OR REPLACE FUNCTION PasswCheck(PASSW IN RAW, PHASH IN RAW)
RETURN INTEGER IS
BEGIN
RETURN UTL_RAW.COMPARE(
DBMS_CRYPTO.HASH(UTL_RAW.CONCAT(UTL_RAW.SUBSTR(PHASH, 1, 8),
PASSW), DBMS_CRYPTO.HASH_SH256),
UTL_RAW.SUBSTR(PHASH, 9));
END;
/
```

![image-20210917161626443](oracle sharding.assets/image-20210917161626443.png)

#### 8.4 进入catalog数据库检查刚才执行的ddl操作是否有错误

```
./gdsctl
connect gsmadmin/oracle
show ddl
```

![image-20210917161703495](oracle sharding.assets/image-20210917161703495.png)

#### 8.5 检查每个shard是否有ddl错误 

##### shard node1节点：

```
config shard -shard sh1
```

![image-20210917162157929](oracle sharding.assets/image-20210917162157929.png)

##### shard node2节点：

```
config shard -shard sh21
```

![image-20210917162216520](oracle sharding.assets/image-20210917162216520.png)

### 9. 验证环境-表空间/chunks

#### 9.1 在gsm节点，检查chunks信息

前面创建shardcatalog时指定chunks为12，因此后续创建shard table分配12个chunks 每个shard节点均有6个chunk

```
config chunks
```

![image-20210917162244348](oracle sharding.assets/image-20210917162244348.png)

#### 9.2 在shard所有节点检查表空间和chunks信息

shard node1:

```
select TABLESPACE_NAME, BYTES/1024/1024 MB from sys.dba_data_file order by tablespace_name;
```

#### 9.3 在catalog数据库检查chunks信息

```
select a.name Shard, count( b.chunk_number) Number_of_Chunks from gsmadmin_internal.database a, gsmadmin_internal.chunk_loc b where  a.database_num=b.database_num group by a.name;
```

与gdsctl中config chunks命令一样，在catalog数据库查询的数量一致

#### 9.4 检查catalog以及shard节点数据库中表信息是否正确

–catalog数据库

```
select table_name from user_tables;
```

–shard节点node1、node2

```
conn app_schema/oracle

select table_name from user_tables;
```

