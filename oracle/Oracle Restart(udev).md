## 安装Oracle Restart (udev)

### 一、虚拟机

| 项目                 | 配置                      | 说明                |
| -------------------- | ------------------------- | ------------------- |
| box                  | oraclelinux/7             |                     |
| vm_name              | OL7_Oracle19_Restart_1021 |                     |
| mem_size:            | 8192                      |                     |
| cpus                 | 4                         |                     |
| public_ip            | 192.168.56.147            |                     |
| disk1_name           | sdb_u01.vdi               | /u01:安装oracle软件 |
| disk2_name           | sdc_u02.vdi               | +DATA               |
| disk3_name           | sdd_u03.vdi               | +DATA               |
| disk4_name           | sde_u04.vdi               | +RECO               |
| disk5_name           | sdf_u05.vdi               | +RECO               |
| ocr_size             | 50                        |                     |
| data_size: data_size | 50                        |                     |

### 二、操作系统准备

以root用户进入系统，进行数据库安装初始设置和准备工作。

```
######################################################
# 系统初始化设置
# 以下root用户执行
######################################################

#设置主机名称
hostnamectl set-hostname orestart-udev

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
#-----------------------------------------------------
cat >> /etc/hosts <<EOF
192.168.56.147    orestart-udev.testdb.mema.com     orestart-udev
192.168.56.149    orestart.dbtest.mema.com     orestart
EOF
#-----------------------------------------------------

# 关闭透明大页THP
#-----------------------------------------------------
cat >> /etc/rc.local << EOF
if test -f /sys/kernel/mm/transparent_hugepage/enabled; then
 echo never > /sys/kernel/mm/transparent_hugepage/enabled
fi
if test -f /sys/kernel/mm/transparent_hugepage/defrag; then
 echo never > /sys/kernel/mm/transparent_hugepage/defrag
fi
EOF
#-----------------------------------------------------

#安装必要软件
yum install -y unzip rlwrap	
```

### 三、数据库安装环境准备

```
# 格式化第二块硬盘/dev/sdb,自动挂载到/u01	
# 用于Oracle软件安装

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

#确认
df -Th /u01

```

![image-20211103094611836](Oracle Restart(udev).assets/image-20211103094611836.png)

```
#安装Oracle preinstall包
yum install -y oracle-database-server-12cR2-preinstall

#修改oracle用户密码
echo "oracle" | passwd oracle --stdin > /dev/null 2>&1

#创建软件安装目录
mkdir -p /u01/app/oracle/product/12.0.0/db
mkdir -p /u01/app/12.0.0/grid
chown -R oracle:oinstall /u01
chmod -R 775 /u01

#切换用户到oracle
su - oracle

#设置环境变量
#-----------------------------------------------------
cat >> .setEnv.sh <<EOF
TMP=/tmp; export TMP
TMPDIR=\$TMP; export TMPDIR

ORACLE_HOSTNAME=orestart-udev; export ORACLE_HOSTNAME
ORACLE_UNQNAME=MEMA; export ORACLE_UNQNAME

# ORACLE_SID=MEMA; export ORACLE_SID
ORACLE_BASE=/u01/app/oracle; export ORACLE_BASE
GRID_HOME=/u01/app/12.0.0/grid; export GRID_HOME
DB_HOME=\$ORACLE_BASE/product/12.0.0/db; export DB_HOME
ORACLE_HOME=\$DB_HOME; export ORACLE_HOME

# ORACLE_HOME_LISTNER=\$ORACLE_HOME export ORACLE_HOME_LISTNER
ORACLE_TERM=xterm; export ORACLE_TERM

#BASE_PATH=/usr/sbin:\$PATH; export BASE_PATH
PATH=\$ORACLE_HOME/bin:\$PATH; export PATH
LD_LIBRARY_PATH=\$ORACLE_HOME/lib:/lib:/usr/lib; export LD_LIBRARY_PATH
CLASSPATH=\$ORACLE_HOME/JRE:\$ORACLE_HOME/jlib:\$ORACLE_HOME/rdbms/jlib; export CLASSPATH

alias gridenv='. /home/oracle/.grid.sh'
alias dbenv='. /home/oracle/.db.sh'
alias sqlplus='rlwrap sqlplus'
alias rman='rlwrap rman'
alias dgmgrl='rlwrap dgmgrl'
alias asmcmd='rlwrap asmcmd'

export DISPLAY=192.168.56.1:0.0
#在oracle linux8上防止gridSetup.sh出错。
#export CV_ASSUME_DISTID=OL7

export JAVA_HOME=\$ORACLE_HOME/jdk
export PATH=\$JAVA_HOME/bin:\$JAVA_HOME/jre/bin:\$PATH
export CLASSPATH=.:\$JAVA_HOME/lib/dt.jar:\$JAVA_HOME/lib/tools.jar

EOF
#-----------------------------------------------------

#环境变量注入.bash_profile，以便oracle用户登录生效
echo ". /home/oracle/.setEnv.sh" >> /home/oracle/.bash_profile

#设置与db软件有关环境变量
#-----------------------------------------------------
cat >> .db.sh <<EOF
ORACLE_SID=MEMA; export ORACLE_SID
ORACLE_HOME=\$DB_HOME; export ORACLE_HOME

PATH=\$ORACLE_HOME/bin:\$PATH; export PATH
LD_LIBRARY_PATH=\$ORACLE_HOME/lib:/lib:/usr/lib; export LD_LIBRARY_PATH
CLASSPATH=\$ORACLE_HOME/JRE:\$ORACLE_HOME/jlib:\$ORACLE_HOME/rdbms/jlib; export CLASSPATH
EOF
#-----------------------------------------------------

#环境变量注入.bash_profile，以便oracle用户登录生效
echo ". /home/oracle/.db.sh" >> /home/oracle/.bash_profile

#设置与grid软件有关环境变量
#-------------------------------------------------------------------------------------------
cat >> .grid.sh <<EOF
ORACLE_SID=+ASM; export ORACLE_SID
ORACLE_HOME=\$GRID_HOME; export ORACLE_HOME

PATH=\$ORACLE_HOME/bin:\$PATH; export PATH
LD_LIBRARY_PATH=\$ORACLE_HOME/lib:/lib:/usr/lib; export LD_LIBRARY_PATH
CLASSPATH=\$ORACLE_HOME/JRE:\$ORACLE_HOME/jlib:\$ORACLE_HOME/rdbms/jlib; export CLASSPATH
EOF
#-----------------------------------------------------
```

![image-20211103095050453](Oracle Restart(udev).assets/image-20211103095050453.png)

### 四、准备软件包

| 软件包         | 说明           | 位置          |
| -------------- | -------------- | ------------- |
| V839960-01.zip | DB数据库软件   | /software/12c |
| V840012-01.zip | GI集群基础软件 | /software/12c |

```
#oracle用户安装
exit
su - oracle

mkdir -p /home/oracle/OraSetup

cd /home/oracle/OraSetup
unzip /software/12c/linuxx64_12201_database.zip

cd /u01/app/12.0.0/grid
unzip /software/12c/linuxx64_12201_grid_home.zip
```

### 五、共享磁盘设置

#### 1、AFD(OL7.9不支持)

磁盘配置情况：

![image-20211103100748237](Oracle Restart(udev).assets/image-20211103100748237.png)

root用户执行：

```
# 1. Set Env
export ORACLE_HOME=/u01/app/12.0.0/grid
export ORACLE_BASE=/tmp

# 2. Provision Disks Using ASMCMD
cd $ORACLE_HOME/bin
./asmcmd afd_label DISK01 /dev/sdc --init
./asmcmd afd_label DISK02 /dev/sdd --init
./asmcmd afd_label DISK03 /dev/sde --init
./asmcmd afd_label DISK04 /dev/sdf --init

#  3. Verify
./asmcmd afd_lslbl '/dev/sd*'
ls -alrt /dev/oracleafd/disks/*
```



OL7.9不支持AFD，报错。



```
gridenv
cd $ORACLE_HOME
cat /etc/os-release | head -n2
cd bin
./afdroot version_check
./afddriverstate -orahome $ORACLE_HOME version
./afddriverstate -orahome $ORACLE_HOME supported
```

#### 2、udev方式

参考文档：

[UDEV SCSI Rules Configuration In Oracle Linux 5, 6 , 7 and 8](https://oracle-base.com/articles/linux/udev-scsi-rules-configuration-in-oracle-linux)

[创建ASM磁盘的两种方式：asmlib、udev（RHEL 7.6）](https://blog.csdn.net/shayuwei/article/details/90481922)

关于分区：如果磁盘大于2.2T，需要用parted命令做分区，fdisk不支持那么大的盘。 当然这只在生产环境才会遇到

##### 分区方案

```
# 绑定共享磁盘：设备名称和ID对应，固定设备所有者。
# 以下root用户执行
######################################################
# 给4个硬盘分区，每个硬盘分一个区即可
if [ ! -e /dev/sdc1 ]; then
  echo -e "n\np\n1\n\n\nw" | fdisk /dev/sdc
fi
if [ ! -e /dev/sdd1 ]; then
  echo -e "n\np\n1\n\n\nw" | fdisk /dev/sdd
fi
if [ ! -e /dev/sde1 ]; then
  echo -e "n\np\n1\n\n\nw" | fdisk /dev/sde
fi
if [ ! -e /dev/sdf1 ]; then
  echo -e "n\np\n1\n\n\nw" | fdisk /dev/sdf
fi

# 设置受信任白名单，编辑文件 /etc/scsi_id 添加选项 options=-g，如果没有那么创建它。
cat > /etc/scsi_id.config <<EOF
options=-g
EOF

# 确认SCSI标识符
ASM_DISK1=`/usr/lib/udev/scsi_id -g -u -d /dev/sdc1`
ASM_DISK2=`/usr/lib/udev/scsi_id -g -u -d /dev/sdd1`
ASM_DISK3=`/usr/lib/udev/scsi_id -g -u -d /dev/sde1`
ASM_DISK4=`/usr/lib/udev/scsi_id -g -u -d /dev/sdf1`

# 创建编辑UDEV规则文件
# 创建文件 vim /etc/udev/rules.d/99-oracle-asmdevices.rules ，并将获取到的SCSI标识符添加进该文件的 RESULT 参数中。
# 需要注意的是：每个SCSI标识符占用一个条目，且每个条目必须在同一行，不可换行。
# 可以根据实际情况修改 SYMLINK+ 对应的显示名字。
cat > /etc/udev/rules.d/99-oracle-asmdevices.rules <<EOF
KERNEL=="sd?1", SUBSYSTEM=="block", PROGRAM=="/usr/lib/udev/scsi_id -g -u -d /dev/\$parent", RESULT=="${ASM_DISK1}", SYMLINK+="asm/DATA1", OWNER="oracle", GROUP="oinstall", MODE="0660"
KERNEL=="sd?1", SUBSYSTEM=="block", PROGRAM=="/usr/lib/udev/scsi_id -g -u -d /dev/\$parent", RESULT=="${ASM_DISK2}", SYMLINK+="asm/DATA2", OWNER="oracle", GROUP="oinstall", MODE="0660"
KERNEL=="sd?1", SUBSYSTEM=="block", PROGRAM=="/usr/lib/udev/scsi_id -g -u -d /dev/\$parent", RESULT=="${ASM_DISK3}", SYMLINK+="asm/FRA1", OWNER="oracle", GROUP="oinstall", MODE="0660"
KERNEL=="sd?1", SUBSYSTEM=="block", PROGRAM=="/usr/lib/udev/scsi_id -g -u -d /dev/\$parent", RESULT=="${ASM_DISK4}", SYMLINK+="asm/FRA2", OWNER="oracle", GROUP="oinstall", MODE="0660"
EOF

# 通过 root 用户执行 partprobe 命令重新识别
/sbin/partprobe /dev/sdc1
/sbin/partprobe /dev/sdd1
/sbin/partprobe /dev/sde1
/sbin/partprobe /dev/sdf1
sleep 10
# 重启UDEV服务
/sbin/udevadm control --reload-rules

sleep 10
/sbin/partprobe /dev/sdc1
/sbin/partprobe /dev/sdd1
/sbin/partprobe /dev/sde1
/sbin/partprobe /dev/sdf1
sleep 10
/sbin/udevadm control --reload-rules
sleep 10

# 查看设备
ls -al /dev/asm/*
```

![image-20211103101020833](Oracle Restart(udev).assets/image-20211103101020833.png)

##### 非分区方案

```
# 绑定共享磁盘：设备名称和ID对应，固定设备所有者。
# 以下root用户执行
######################################################

for i in c d e f; 
do
echo "KERNEL==\"sd?\", ENV{DEVTYPE}==\"disk\", SUBSYSTEM==\"block\", PROGRAM==\"/usr/lib/udev/scsi_id -g -u -d \$devnode\", RESULT==\"`/usr/lib/udev/scsi_id --whitelisted --replace-whitespace --device=/dev/sd$i`\", RUN+=\"/bin/sh -c 'mknod /dev/asm-disk$i b \$major \$minor; chown oracle:dba /dev/asm-disk$i; chmod 0660 /dev/asm-disk$i'\"">> /etc/udev/rules.d/99-oracle-asmdevices.rules 
done

# 重启UDEV服务
systemctl restart systemd-udev-trigger.service

#确认
ls -l /dev/asm*
```

![image-20211103101200644](Oracle Restart(udev).assets/image-20211103101200644.png)

### 六、安装GI

oracle用户执行

```
gridenv
cd $ORACLE_HOME
./gridSetup.sh
```

![image-20211103101302435](Oracle Restart(udev).assets/image-20211103101302435.png)

![image-20211103101342603](Oracle Restart(udev).assets/image-20211103101342603.png)

password : oracle

![image-20211103101358472](Oracle Restart(udev).assets/image-20211103101358472.png)

![image-20211103101432238](Oracle Restart(udev).assets/image-20211103101432238.png)

默认下一步到检查页面

![image-20211103101528431](Oracle Restart(udev).assets/image-20211103101528431.png)

进行安装，根据弹出的窗口执行语句

![image-20211103101713119](Oracle Restart(udev).assets/image-20211103101713119.png)

```
/u01/app/oraInventory/orainstRoot.sh
/u01/app/12.0.0/grid/root.sh
```

![image-20211103102103921](Oracle Restart(udev).assets/image-20211103102103921.png)

### 七、安装DB

```
dbenv
cd /home/oracle/OraSetup/database
./runInstaller 

## install software only
```

![image-20211103102515207](Oracle Restart(udev).assets/image-20211103102515207.png)

进行安装，根据弹出的窗口执行语句

![image-20211103103423955](Oracle Restart(udev).assets/image-20211103103423955.png)

```
/u01/app/oracle/product/12.0.0/db/root.sh
```

### 八、创建RECO磁盘组

创建asm磁盘组：RECO。

```
gridenv
asmca
```

![image-20211103104014647](Oracle Restart(udev).assets/image-20211103104014647.png)

![image-20211103104045924](Oracle Restart(udev).assets/image-20211103104045924.png)

### 九、建库

```
dbenv
dbca
```

![image-20211103110054865](Oracle Restart(udev).assets/image-20211103110054865.png)

### 十、打补丁

使用“opatchauto”命令自动安装此补丁。自动修补可帮助您减少修补 Oracle 主目录所涉及的手动步骤数量。从技术上讲，作为预安装步骤，自动修补会停止所有依赖数据库、CRS 资源和整个 GI 堆栈。然后，它会修补 OracleClusterware 和所有适用的数据库，然后作为安装后的步骤，它会自动重新启动整个 GI 堆栈、CRS 资源和相关数据库。

**确保打补丁前将可插拔数据库打开并至于保持打开方式。**

| 软件包                            | 说明       | 位置      |
| --------------------------------- | ---------- | --------- |
| p6880880_190000_Linux-x86-64.zip  | Opatch工具 | /software |
| p33290750_122010_Linux-x86-64.zip | GI补丁包   | /software |

#### 1、升级opatch工具

```
# oracle 用户

gridenv
cd $ORACLE_HOME
# grid的$ORACLE_HOME所有者是root，所以需要root用户才能操作

# 开新窗口，root用户
# 进入grid环境$ORACLE_HOME目录
cd /u01/app/12.0.0/grid
mv OPatch OPatch.old
unzip /software/p6880880_190000_Linux-x86-64.zip
chown -R oracle.oinstall OPatch
chmod -R 755 OPatch

# 回oracle窗口
cd
dbenv
cd $ORACLE_HOME
mv OPatch OPatch.old
unzip /software/p6880880_190000_Linux-x86-64.zip
```

#### 2、利用opatchauto打补丁

注意

1、硬盘剩余空间要大于8G

2、所有可插拔数据库处于**打开状态**。

将可插拔数据库打开并至于保持打开方式。

```
sqlplus / as sysdba
alter pluggable database MEMAPDB open;
alter pluggable database MEMAPDB save state;
#oracle用户
cd /u01
mkdir patch
cd patch
unzip /software/p33290750_122010_Linux-x86-64.zip

#root用户
export PATH=$PATH:/u01/app/12.0.0/grid/OPatch
opatchauto apply /u01/patch/33290750
```

#### 3、升级可插拔数据库数据字典[可选]

**(Doc ID 1635482.1)**

对于可插拔数据库，**打补丁前务必打开并保持打开状态**，否者无法升级数据字典，出现如下问题：

报`DBRU bundle patch 211019 (DATABASE OCT 2021 RELEASE UPDATE 12.2.0.1.211019): Ins talled in the CDB but not in the PDB.`问题。最好删除重建。

解决方法：

```
[oracle@restart12 ~]$ sqlplus /nolog

SQL*Plus: Release 12.2.0.1.0 Production on Fri Oct 22 10:30:03 2021

Copyright (c) 1982, 2016, Oracle.  All rights reserved.

SQL> connect / as sysdba
Connected.

SQL> select name,cause,type,message,status from PDB_PLUG_IN_VIOLATIONs order by name;

NAME
--------------------------------------------------------------------------------
CAUSE                                                            TYPE
---------------------------------------------------------------- ---------
MESSAGE
--------------------------------------------------------------------------------
STATUS
---------
PDB1
SQL Patch                                                        ERROR
DBRU bundle patch 211019 (DATABASE OCT 2021 RELEASE UPDATE 12.2.0.1.211019): Ins
talled in the CDB but not in the PDB.
PENDING


SQL> shutdown immediate;
Database closed.
Database dismounted.
ORACLE instance shut down.
SQL> startup upgrade
ORACLE instance started.

Total System Global Area 2415919104 bytes
Fixed Size                  8795616 bytes
Variable Size             671091232 bytes
Database Buffers         1728053248 bytes
Redo Buffers                7979008 bytes
Database mounted.
Database opened.
SQL> alter pluggable database all open upgrade;

Pluggable database altered.
[oracle@restart12 ~]$ cd $ORACLE_HOME/rdbms/admin
[oracle@restart12 admin]$ $ORACLE_HOME/perl/bin/perl catctl.pl -c 'PDB1' catupgrd.sql
SQL> shutdown immediate;
Database closed.
Database dismounted.
ORACLE instance shut down.
SQL> startup
ORACLE instance started.

Total System Global Area 2415919104 bytes
Fixed Size                  8795616 bytes
Variable Size             671091232 bytes
Database Buffers         1728053248 bytes
Redo Buffers                7979008 bytes
Database mounted.
Database opened.
SQL> show pdbs

CON_ID CON_NAME                 OPEN MODE  RESTRICTED
---------- ------------------------------ ---------- 
         2 PDB$SEED            READ ONLY  NO
         3 MEMAPDB             READ WRITE NO


SQL> alter pluggable database MEMAPDB close;

Pluggable database altered.

SQL> alter pluggable database MEMAPDB open;

Pluggable database altered.

SQL> show pdbs

CON_ID CON_NAME                 OPEN MODE  RESTRICTED
---------- ------------------------------ ---------- 
         2 PDB$SEED            READ ONLY  NO
         3 MEMAPDB             READ WRITE NO

```

### 十一、启用hugepages

#### 1、alert文件提示信息

建议大页数量：1153 （共2306M）

#### 2、修改核心参数

在系统参数配置文件`/etc/sysctl.conf`添加以下一行：

> ```
> # setting oracle database hugepages
> vm.nr_hugepages=1200 
> ```

#### 3、修改环境限制配置

修改环境资源限制配置文件`/etc/security/limits.conf`

添加或修改以下行(k为单位)：

> ```
> oracle               soft    memlock 2400000
> oracle               hard    memlock 2400000
> ```

#### 4、重启系统

重启，reboot操作系统。

#### 5、确认

```
grep Huge /proc/meminfo
```

![image-20211104094004735](Oracle Restart(udev).assets/image-20211104094004735.png)

### 十二、基本使用

#### 1、查看服务和相关进程

```
# 查看hasd服务情况，需root用户权限
systemctl status oracle-ohasd

# 从操作系统查看相关进程情况
ps -ef|grep smon
ps -ef|grep pmon
ps -ef|grep tns
```

![image-20211104094129471](Oracle Restart(udev).assets/image-20211104094129471.png)

#### 2、查看服务端口

```
# 查看服务监听端口
ss -nltp
```

![image-20211104094346482](Oracle Restart(udev).assets/image-20211104094346482.png)

#### 3、查询数据库基本信息

```
dbenv
sqlplus /nolog
connect / as sysdba
select name from v$datafile;
-- 查看数据库大小
select
( select sum(bytes)/1024/1024/1024 data_size from dba_data_files ) +
( select nvl(sum(bytes),0)/1024/1024/1024 temp_size from dba_temp_files ) +
( select sum(bytes)/1024/1024/1024 redo_size from sys.v_$log ) +
( select sum(BLOCK_SIZE*FILE_SIZE_BLKS)/1024/1024/1024 controlfile_size from v$controlfile) "Size in GB"
from
dual;
-- 查看pdbs
show pdbs;
exit
```

![image-20211104094518843](Oracle Restart(udev).assets/image-20211104094518843.png)

#### 4、监听情况

```
gridenv
# 查看监听情况
lsnrctl status
# 停止监听
lsnrctl stop
# 启动监听
lsnrctl start
```

![image-20211104094557778](Oracle Restart(udev).assets/image-20211104094557778.png)

#### 5、HAS管理

```
# 查看资源信息，以列表形式显示
crsctl status res -t
# 关闭oracle has及相关资源
crsctl stop has
# 启动oracle has及相关资源
crsctl start has
```

![image-20211104094616827](Oracle Restart(udev).assets/image-20211104094616827.png)

### 6、SRV管理

```
# 查看数据库配置信息
srvctl config database -d mema
# 查看数据库运行状态
srvctl status database -d mema
# 关闭数据库库
srvctl stop database -d mema
# 启动数据库
srvctl start database -d mema
```

![image-20211104094750341](Oracle Restart(udev).assets/image-20211104094750341.png)

### 十三、备份

```
# 指定要备份的数据库
export ORACLE_SID=MEMA

# rman链接到目标数据库
rman target=/
```

![image-20211104095204590](Oracle Restart(udev).assets/image-20211104095204590.png)

#### 1、定义备份和恢复策略

```
# 配置备份策略，只需要执行一次
CONFIGURE RETENTION POLICY TO RECOVERY WINDOW OF 7 DAYS;
CONFIGURE DEFAULT DEVICE TYPE TO DISK;
CONFIGURE CHANNEL DEVICE TYPE DISK FORMAT '/home/oracle/rmandata/backup%d_DB_%u_%s_%p';
CONFIGURE CONTROLFILE AUTOBACKUP ON;
CONFIGURE CONTROLFILE AUTOBACKUP FORMAT FOR DEVICE TYPE DISK TO '/home/oracle/rmandata/controlfile_%F';
```

![image-20211104100459580](Oracle Restart(udev).assets/image-20211104100459580.png)

#### 2、执行备份

```
# 执行备份，按需执行
RUN {
  BACKUP DATABASE PLUS ARCHIVELOG;
  DELETE NOPROMPT OBSOLETE;
}


# 查看备份集
LIST BACKUP;
LIST BACKUP SUMMARY; 
```

![image-20211104101340396](Oracle Restart(udev).assets/image-20211104101340396.png)

![image-20211104101621159](Oracle Restart(udev).assets/image-20211104101621159.png)

#### 3、调度备份定期执行

用schedule调度备份，参照：

[使用DBMS_SCHEDULER调度RMAN备份](https://git.memadata.cn/jianping.wang/dblearn/-/blob/master/Oracle/DBMS_SCHEDULER rman backup.md)

### 十四、导出数据

#### 1、建立操作系统目录

```
cd
# 建立目录/home/oracle/expdata
mkdir expdata
```

![image-20211104101657929](Oracle Restart(udev).assets/image-20211104101657929.png)

#### 2、建立数据库对象：目录

```
create or replace directory expdata as '/home/oracle/expdata';
```

![image-20211104101841814](Oracle Restart(udev).assets/image-20211104101841814.png)

#### 3、导出数据

cdb全库导出

```
expdp system/Mema_1234 directory=expdata dumpfile=fulldb.dmp logfile=fulldb.log full =y

# 根据日期生成expdp文件
expdp system/Mema_1234 directory=expdata dumpfile=fulldb`date +%F`.dmp logfile=fulldb`date +%F`.log full =y
```

```
expdp directory=expdata dumpfile=fulldb.dmp logfile=fulldb.log full =y
```

输入用户：`sys as sysdba`

输入对应密码。

![image-20211104102126009](Oracle Restart(udev).assets/image-20211104102126009.png)

#### 4 删除过期文件

```
# 删除7天前的文件
find /home/oracle/expdata -type f -mtime +7 -exec rm -f {} \;
```

#### 5 调度自动执行

利用操作系统crontab或数据库schedule调度导出任务，自动执行。（略）

### 2、导出可插拔数据库pdb1

#### 1 添加连接串

> ```
> tnsnames.ora
> # 添加指向pdb1数据库服务的连接字符串
> 
> MEMAPDB =
>   (DESCRIPTION =
>     (ADDRESS_LIST =
>       (ADDRESS = (PROTOCOL = TCP)(HOST = 192.168.56.147)(PORT = 1521))
>     )
>     (CONNECT_DATA =
>       (SERVICE_NAME = memapdb)
>     )
>   )
> ```

#### 2 建立操作系统目录

```
cd /home/oracle/expdata
# 建立目录/home/oracle/expdata/memapdb
mkdir memapdb
```

#### 3 建立数据库对象：目录

```
connect system/oracle@memapdb
create or replace directory memapdb_expdata as '/home/oracle/expdata/memapdb';
```

#### 4 建立一个全库导出管理用户

```
connect system/oracle@memapdb

create user memapdbexpadmin identified by Mema_1234;
alter user memapdbexpadmin default tablespace users quota unlimited on users;
-- 授予可连接，可建表，可导出全库权限
grant create session,resource,DATAPUMP_EXP_FULL_DATABASE to memapdbexpadmin;
-- 授予可读写目录对象权限
grant read,write on directory memapdb_expdata to memapdbexpadmin;
```

#### 5 导出数据

memapdb全库导出

```
expdp memapdbexpadmin/Mema_1234@MEMAPDB directory=memapdb_expdata dumpfile=memapdb.dmp logfile=fulldb.log full =y

# 根据日期生成expdp文件
expdp memapdbexpadmin/Mema_1234@memapdb directory=memapdb_expdata dumpfile=memapdb`date +%F`.dmp logfile=memapdb`date +%F`.log full =y
```

#### 6 删除过期文件

```
# 删除7天前的文件
find /home/oracle/expdata/memapdb -type f -mtime +7 -exec rm -f {} \;
```

#### 7 调度自动执行

利用操作系统crontab或数据库schedule调度导出任务，自动执行。（略）

### 十五、swingbench压力测试

#### 1、java环境

`.bash_profile`文件添加环境变量。

> ```
> export JAVA_HOME=$ORACLE_HOME/jdk
> export PATH=$JAVA_HOME/bin:$JAVA_HOME/jre/bin:$PATH
> export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
> ```

确认：

```
java -version
```

#### 2、解压swingbench软件包

```
unzip /software/Oracle/Swingbench/swingbenchlatest.zip
```

#### 3、使用swingbench

1、生成oe（订单系统）测试数据

```
cd 
cd /home/oracle/swingbench/bin
export DISPLAY=192.168.56.1:0.0
./oewizard
```

![image-20211104103133283](Oracle Restart(udev).assets/image-20211104103133283.png)

![image-20211104103158291](Oracle Restart(udev).assets/image-20211104103158291.png)

![image-20211104103212679](Oracle Restart(udev).assets/image-20211104103212679.png)

![image-20211104103225786](Oracle Restart(udev).assets/image-20211104103225786.png)

![image-20211104103236244](Oracle Restart(udev).assets/image-20211104103236244.png)

![image-20211104103246128](Oracle Restart(udev).assets/image-20211104103246128.png)

![image-20211104103307493](Oracle Restart(udev).assets/image-20211104103307493.png)

执行完毕，测试数据生成。

2、压力测试

```
./swingbench
```

![image-20211104103328658](Oracle Restart(udev).assets/image-20211104103328658.png)

![image-20211104103342768](Oracle Restart(udev).assets/image-20211104103342768.png)

点击开始按钮，开始测试：

![image-20211104103405603](Oracle Restart(udev).assets/image-20211104103405603.png)

可以调整测试参数，反复测试。

### 十六、客户端的安装和使用

#### 1、客户端软件包

| 软件包                               | 大小 | 说明                    |
| ------------------------------------ | ---- | ----------------------- |
| WINDOWS.X64_193000_client.zip        | 1G   | Oracle客户端for windows |
| sqldeveloper-21.2.1.204.1703-x64.zip | 430M | Oracle SQL Develope     |

#### 2、客户端sqlplus链接

![image-20211104102950071](Oracle Restart(udev).assets/image-20211104102950071.png)

#### 3、SQL Developer连接

普通用户链接：

![image-20211104103020368](Oracle Restart(udev).assets/image-20211104103020368.png)

dba链接

![image-20211104103028393](Oracle Restart(udev).assets/image-20211104103028393.png)

![image-20211104103044910](Oracle Restart(udev).assets/image-20211104103044910.png)





### 十二、基本使用

```
dbenv
sqlplus /nolog
connect / as sysdba
select name from v$datafile;
exit

gridenv
lsnrctl status
crsctl status res -t
srvctl config database -d mema
srvctl status database -d mema

exit

#
systemctl status oracle-ohasd
```

![image-20211103110300949](Oracle Restart(udev).assets/image-20211103110300949.png)

![image-20211103110346715](Oracle Restart(udev).assets/image-20211103110346715.png)

![image-20211103110359694](Oracle Restart(udev).assets/image-20211103110359694.png)

![image-20211103110459624](Oracle Restart(udev).assets/image-20211103110459624.png)

![image-20211103110523523](Oracle Restart(udev).assets/image-20211103110523523.png)

