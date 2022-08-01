## 安装Oracle 12c Restart

### 1、修改虚拟机基本配置

```
# 修改oracle和root用户密码
echo "Mema_1234" | passwd root --stdin > /dev/null 2>&1
echo "oracle" | passwd oracle --stdin > /dev/null 2>&1

# 修改sshd配置
sed -i -e "s\PasswordAuthentication no\PasswordAuthentication yes\g" /etc/ssh/sshd_config
systemctl restart sshd

# 关闭selinux
sed -i 's/SELINUX=enforcing/\SELINUX=disabled/' /etc/selinux/config

# 关闭防火墙
systemctl stop firewalld
systemctl disable firewalld

hostnamectl set-hostname orestart
timedatectl set-timezone Asia/Shanghai

cat >> /etc/hosts <<EOF
192.168.56.149    orestart.dbtest.mema.com     orestart
EOF

```

### 2、安装需要的软件包

```
yum update -y
mv /etc/motd /etc/motd.orgn

#安装必要软件
yum install -y unzip 	
yum -y install oracle-database-server-12cR2-preinstall
yum -y install oracleasm*
yum -y install kmod-oracleasm*
yum -y install rlwrap
```

![image-20211028105235797](Oracle Restart.assets/image-20211028105235797.png)

### 3. 格式化硬盘

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
```

![image-20211021164713424](Oracle Restart.assets/image-20211021164713424.png)



### 4、准备oracle用户环境

```
#创建软件安装目录
mkdir -p /u01/app/oracle/product/12.0.0/db
mkdir -p /u01/app/12.0.0/grid
chown -R oracle:oinstall /u01
chmod -R 775 /u01

#切换用户到oracle
su - oracle

#设置环境变量
#-------------------------------------------------------------------------------------------
cat >> .setEnv.sh <<EOF
TMP=/tmp; export TMP
TMPDIR=\$TMP; export TMPDIR

ORACLE_HOSTNAME=orestart; export ORACLE_HOSTNAME
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
#-------------------------------------------------------------------------------------------

#环境变量注入.bash_profile，以便oracle用户登录生效
echo ". /home/oracle/.setEnv.sh" >> /home/oracle/.bash_profile

#设置与db软件有关环境变量
#-------------------------------------------------------------------------------------------
cat >> .db.sh <<EOF
ORACLE_SID=MEMA; export ORACLE_SID
ORACLE_HOME=\$DB_HOME; export ORACLE_HOME

PATH=\$ORACLE_HOME/bin:\$PATH; export PATH
LD_LIBRARY_PATH=\$ORACLE_HOME/lib:/lib:/usr/lib; export LD_LIBRARY_PATH
CLASSPATH=\$ORACLE_HOME/JRE:\$ORACLE_HOME/jlib:\$ORACLE_HOME/rdbms/jlib; export CLASSPATH
EOF
#-------------------------------------------------------------------------------------------

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
#-------------------------------------------------------------------------------------------
```

![image-20211029094430522](Oracle Restart.assets/image-20211029094430522.png)

![image-20211029094248766](Oracle Restart.assets/image-20211029094248766.png)

### 5. 共享磁盘设置

参考文档：[创建ASM磁盘的两种方式：asmlib、udev（RHEL 7.6）](https://blog.csdn.net/shayuwei/article/details/90481922)

https://www.oracle.com/linux/technologies/install-asmlib.html

https://www.oracle.com/linux/downloads/linux-asmlib-v7-downloads.html 下载：`oracleasmlib-2.0.12-1.el7.x86_64.rpm`

在使用ASMlib创建ASM时，需要对所有节点进行配置和加载。

创建磁盘的工作在一个节点完成就可以，其余的节点通过scandisks可以扫出来。

在重启rac的时候，除了创建磁盘的节点，其余节点都要重新scan。

```
# root用户

# Note: All ASMLib installations require the oracleasmlib and oracleasm-support packages appropriate for their machine
# The oracleasm kernel driver is built into the Unbreakable Enterprise Kernel for Oracle Linux 7 and does not need to be installed manually.
# The oracleasm kernel driver for the 64-bit (x86_64) Red Hat Compatible Kernel for Oracle Linux 7 can be installed manually from ULN
# or:`yum install kmod-oracleasm`

# 安装oracleasm-support
yum install -y oracleasm-support

# 安装Library and Tools
# https://www.oracle.com/linux/downloads/linux-asmlib-v7-downloads.html 
# 下载：oracleasmlib-2.0.12-1.el7.x86_64.rpm
rpm -i /software/oracleasmlib-2.0.12-1.el7.x86_64.rpm

#确认
rpm -qa |grep oracleasm
#应该显示：
# 1、oracleasm-support-2.1.11-2.el7.x86_64
# 2、kmod-oracleasm-2.0.8-28.0.1.el7.x86_64
# 3、oracleasmlib-2.0.12-1.el7.x86_64

# 配置，指定磁盘的用户和组为oracle.dba
oracleasm configure -i

# 启动asm管理器
oracleasm init

# 确认状态
oracleasm status

# 磁盘管理
# 分区
echo -e "n\np\n1\n\n\nw" | fdisk /dev/sdc
echo -e "n\np\n1\n\n\nw" | fdisk /dev/sdd
echo -e "n\np\n1\n\n\nw" | fdisk /dev/sde
echo -e "n\np\n1\n\n\nw" | fdisk /dev/sdf

# 确认
lsblk

# 创建asmdisk
oracleasm createdisk VOL1 /dev/sdc1
oracleasm createdisk VOL2 /dev/sdd1
oracleasm createdisk VOL3 /dev/sde1
oracleasm createdisk VOL4 /dev/sdf1

# 确认
oracleasm listdisks

#RAC其他节点只需要scan
#oracleasm scandisks

# 自动启动
oracleasm configure -e

# 服务管理
systemctl start oracleasm
systemctl status oracleasm

#Discovery Strings for Linux ASMLib : "ORCL:VOL*"
```

![image-20211029101401135](Oracle Restart.assets/image-20211029101401135.png)

![image-20211029101510931](Oracle Restart.assets/image-20211029101510931.png)

![image-20211029101614945](Oracle Restart.assets/image-20211029101614945.png)

![image-20211029101641418](Oracle Restart.assets/image-20211029101641418.png)

![image-20211029101705762](Oracle Restart.assets/image-20211029101705762.png)

![image-20211029101721675](Oracle Restart.assets/image-20211029101721675.png)

![image-20211029101753464](Oracle Restart.assets/image-20211029101753464.png)

### 6. 准备软件包

| 软件包         | 说明           | 位置      |
| -------------- | -------------- | --------- |
| V839960-01.zip | DB数据库软件   | /software |
| V840012-01.zip | GI集群基础软件 | /software |

```
#oracle用户安装
su - oracle

mkdir -p /home/oracle/OraSetup

cd /home/oracle/OraSetup
unzip /software/V839960-01.zip

cd /u01/app/12.0.0/grid
unzip /software/V840012-01.zip
```

### 7. 安装GI

**oracle用户执行**

```
gridenv
cd $ORACLE_HOME
pwd
/u01/app/12.0.0/grid

./gridSetup.sh
```

![image-20211029103906852](Oracle Restart.assets/image-20211029103906852.png)

点击：change

查找：ORCL:VOL*

![image-20211029105209197](Oracle Restart.assets/image-20211029105209197.png)

创建磁盘组：DATA

![image-20211029105307792](Oracle Restart.assets/image-20211029105307792.png)

设置口令密码：oracle

![image-20211029105428468](Oracle Restart.assets/image-20211029105428468.png)

设置操作系统特权组：

![image-20211029105512425](Oracle Restart.assets/image-20211029105512425.png)

进行检查：

![image-20211029105623937](Oracle Restart.assets/image-20211029105623937.png)

最后按照提示：

新建终端窗口，root用户登录，执行安装后脚本：

![image-20211029105837658](Oracle Restart.assets/image-20211029105837658.png)

==root用户执行==

```
/u01/app/oraInventory/orainstRoot.sh
/u01/app/12.0.0/grid/root.sh
```

![image-20211029110050549](Oracle Restart.assets/image-20211029110050549.png)

### 8. 安装DB

```
#oracle用户安装
## install software only

dbenv
cd /home/oracle/OraSetup/database
./runInstaller 

```

![image-20211028150311534](Oracle Restart.assets/image-20211028150311534.png)

![image-20211029110952381](Oracle Restart.assets/image-20211029110952381.png)

![image-20211029111010165](Oracle Restart.assets/image-20211029111010165.png)

最后按照提示：

新建终端窗口，root用户登录，执行安装后脚本：

![image-20211029112022878](Oracle Restart.assets/image-20211029112022878.png)

==root用户执行==

```
/u01/app/oracle/product/12.0.0/db/root.sh
```

![image-20211029112011584](Oracle Restart.assets/image-20211029112011584.png)

### 9. 创建RECO磁盘组

创建asm磁盘组：RECO。

```
创建asm磁盘组：RECO。
gridenv
asmca

#password:oracle (all)
```

![image-20211029112354220](Oracle Restart.assets/image-20211029112354220.png)

![image-20211029112538330](Oracle Restart.assets/image-20211029112538330.png)

![image-20211029112719661](Oracle Restart.assets/image-20211029112719661.png)

### 10. 建库

```
dbenv
dbca

# 数据库全局名称：MEMA
# SID：MEMA
###若自定义安装失败，尝试默认安装设置
```

![image-20211029112841615](Oracle Restart.assets/image-20211029112841615.png)

![image-20211029112852319](Oracle Restart.assets/image-20211029112852319.png)

![image-20211029112934353](Oracle Restart.assets/image-20211029112934353.png)

![image-20211029113009025](Oracle Restart.assets/image-20211029113009025.png)

密码：oracle

![image-20211029113037392](Oracle Restart.assets/image-20211029113037392.png)

![image-20211029135737930](Oracle Restart.assets/image-20211029135737930.png)

### 11. 检查

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

#root用户
systemctl status oracle-ohasd

```

![image-20211029135852351](Oracle Restart.assets/image-20211029135852351.png)

![image-20211029141405463](Oracle Restart.assets/image-20211029141405463.png)

![image-20211029141440307](Oracle Restart.assets/image-20211029141440307.png)

![image-20211029141502861](Oracle Restart.assets/image-20211029141502861.png)

![image-20211029141556448](Oracle Restart.assets/image-20211029141556448.png)

![image-20211029141615888](Oracle Restart.assets/image-20211029141615888.png)

![image-20211029141645753](Oracle Restart.assets/image-20211029141645753.png)

### 12. 打补丁

使用“opatchauto”命令自动安装此补丁。自动修补可帮助您减少修补 Oracle 主目录所涉及的手动步骤数量。从技术上讲，作为预安装步骤，自动修补会停止所有依赖数据库、CRS 资源和整个 GI 堆栈。然后，它会修补 OracleClusterware 和所有适用的数据库，然后作为安装后的步骤，它会自动重新启动整个 GI 堆栈、CRS 资源和相关数据库。

| 软件包                            | 说明       | 位置             |
| --------------------------------- | ---------- | ---------------- |
| p6880880_190000_Linux-x86-64.zip  | Opatch工具 | /software/OPatch |
| p33290750_122010_Linux-x86-64.zip | GI补丁包   | /software        |

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
mv OPatch.old OPatch
unzip /software/OPatch/p6880880_190000_Linux-x86-64.zip
chown -R oracle.oinstall OPatch
chmod -R 755 OPatch

# 回oracle窗口
cd
dbenv
cd $ORACLE_HOME
mv OPatch OPatch.old
unzip /software/Oracle/LINUX.X64_193000/OPatch/p6880880_190000_Linux-x86-64.zip
```

#### 2、利用opatchauto打补丁

注意硬盘剩余空间要大于8G

```
#oracle用户
cd /u01
mkdir patch
cd patch
unzip /software/p33290750_122010_Linux-x86-64.zip

#root用户
export PATH=$PATH:/u01/app/12.0.0/grid/OPatch
opatchauto apply /u01/patch/33290750
```

> ```
> [root@restart12 grid]# opatchauto apply /home/oracle/patch/33290750
> 
> OPatchauto session is initiated at Sat Oct 23 11:31:16 2021
> 
> System initialization log file is /u01/app/12.0.0/grid/cfgtoollogs/opatchautodb/systemconfig2021-10-23_11-31-17AM.log.
> 
> Session log file is /u01/app/12.0.0/grid/cfgtoollogs/opatchauto/opatchauto2021-10-23_11-31-22AM.log
> The id for this session is YYNC
> 
> Executing OPatch prereq operations to verify patch applicability on home /u01/app/oracle/product/12.0.0/db
> Patch applicability verified successfully on home /u01/app/oracle/product/12.0.0/db
> 
> 
> Executing patch validation checks on home /u01/app/oracle/product/12.0.0/db
> Patch validation checks successfully completed on home /u01/app/oracle/product/12.0.0/db
> 
> 
> Verifying SQL patch applicability on home /u01/app/oracle/product/12.0.0/db
> SQL patch applicability verified successfully on home /u01/app/oracle/product/12.0.0/db
> 
> 
> Executing OPatch prereq operations to verify patch applicability on home /u01/app/12.0.0/grid
> Patch applicability verified successfully on home /u01/app/12.0.0/grid
> 
> 
> Executing patch validation checks on home /u01/app/12.0.0/grid
> Patch validation checks successfully completed on home /u01/app/12.0.0/grid
> 
> 
> Preparing to bring down database service on home /u01/app/oracle/product/12.0.0/db
> Successfully prepared home /u01/app/oracle/product/12.0.0/db to bring down database service
> 
> 
> Bringing down database service on home /u01/app/oracle/product/12.0.0/db
> Following database has been stopped and will be restarted later during the session: mema
> Database service successfully brought down on home /u01/app/oracle/product/12.0.0/db
> 
> 
> Performing prepatch operations on CRS - bringing down CRS service on home /u01/app/12.0.0/grid
> Prepatch operation log file location: /u01/app/oracle/crsdata/restart12/crsconfig/hapatch_2021-10-23_11-32-09AM.log
> CRS service brought down successfully on home /u01/app/12.0.0/grid
> 
> 
> Start applying binary patch on home /u01/app/oracle/product/12.0.0/db
> Binary patch applied successfully on home /u01/app/oracle/product/12.0.0/db
> 
> 
> Start applying binary patch on home /u01/app/12.0.0/grid
> Binary patch applied successfully on home /u01/app/12.0.0/grid
> 
> 
> Performing postpatch operations on CRS - starting CRS service on home /u01/app/12.0.0/grid
> Postpatch operation log file location: /u01/app/oracle/crsdata/restart12/crsconfig/hapatch_2021-10-23_11-36-32AM.log
> CRS service started successfully on home /u01/app/12.0.0/grid
> 
> 
> Starting database service on home /u01/app/oracle/product/12.0.0/db
> Database service successfully started on home /u01/app/oracle/product/12.0.0/db
> 
> 
> Preparing home /u01/app/oracle/product/12.0.0/db after database service restarted
> No step execution required.........
> 
> 
> Trying to apply SQL patch on home /u01/app/oracle/product/12.0.0/db
> SQL patch applied successfully on home /u01/app/oracle/product/12.0.0/db
> 
> OPatchAuto successful.
> 
> --------------------Summary-----------------------
> 
> Patching is completed successfully. Please find the summary as follows:
> 
> Host:restart12
> SIDB Home:/u01/app/oracle/product/12.0.0/db
> Version:12.2.0.1.0
> Summary:
> 
> ==Following patches were SKIPPED:
> 
> Patch: /home/oracle/patch/33290750/33116894
> Reason: This patch is not applicable to this specified target type - "oracle_database"
> 
> Patch: /home/oracle/patch/33290750/26839277
> Reason: This patch is not applicable to this specified target type - "oracle_database"
> 
> Patch: /home/oracle/patch/33290750/33239961
> Reason: This patch is not applicable to this specified target type - "oracle_database"
> 
> 
> ==Following patches were SUCCESSFULLY applied:
> 
> Patch: /home/oracle/patch/33290750/31802727
> Log: /u01/app/oracle/product/12.0.0/db/cfgtoollogs/opatchauto/core/opatch/opatch2021-10-23_11-32-30AM_1.log
> 
> Patch: /home/oracle/patch/33290750/33261817
> Log: /u01/app/oracle/product/12.0.0/db/cfgtoollogs/opatchauto/core/opatch/opatch2021-10-23_11-32-30AM_1.log
> 
> 
> Host:restart12
> SIHA Home:/u01/app/12.0.0/grid
> Version:12.2.0.1.0
> Summary:
> 
> ==Following patches were SUCCESSFULLY applied:
> 
> Patch: /home/oracle/patch/33290750/26839277
> Log: /u01/app/12.0.0/grid/cfgtoollogs/opatchauto/core/opatch/opatch2021-10-23_11-34-02AM_1.log
> 
> Patch: /home/oracle/patch/33290750/31802727
> Log: /u01/app/12.0.0/grid/cfgtoollogs/opatchauto/core/opatch/opatch2021-10-23_11-34-02AM_1.log
> 
> Patch: /home/oracle/patch/33290750/33116894
> Log: /u01/app/12.0.0/grid/cfgtoollogs/opatchauto/core/opatch/opatch2021-10-23_11-34-02AM_1.log
> 
> Patch: /home/oracle/patch/33290750/33239961
> Log: /u01/app/12.0.0/grid/cfgtoollogs/opatchauto/core/opatch/opatch2021-10-23_11-34-02AM_1.log
> 
> Patch: /home/oracle/patch/33290750/33261817
> Log: /u01/app/12.0.0/grid/cfgtoollogs/opatchauto/core/opatch/opatch2021-10-23_11-34-02AM_1.log
> 
> 
> 
> OPatchauto session completed at Sat Oct 23 11:43:01 2021
> Time taken to complete the session 11 minutes, 46 seconds
> ```

#### 3、pdb需要升级数据字典

**pdb1打开出错会进入受限模式**

> ```
> [oracle@restart12 patch]$ sqlplus /nolog
> 
> SQL> connect / as sysdba
> 
> SQL> select DESCRIPTION from dba_registry_sqlpatch;
> 
> SQL> show pdbs
> 
>  CON_ID CON_NAME         OPEN MODE  RESTRICTED
> ---------- ------------------------------ --------
>          2 PDB$SEED      READ ONLY  NO
>          3 MEMAPDB       MOUNTED
> 
> SQL> alter pluggable database MEMAPDB open ;
> 
> SQL> SELECT NAME,STATUS,MESSAGE FROM PDB_PLUG_IN_VIOLATIONS;
> ```

注意：

**PDB1还要升级数据字典：**

```
SQL> alter pluggable database MEMAPDB close immediate;
SQL> alter pluggable database MEMAPDB open upgrade;
SQL> exit
dbenv
cd $ORACLE_HOME/OPatch
./datapatch -verbose
```

打补丁后，没有出现pdb数据字典未升级的情况。

sql:

```
SQL>  alter pluggable database MEMAPDB close immediate;
SQL>  alter pluggable database MEMAPDB open ;
SQL>  show pdbs
SQL>  alter session set container=MEMAPDB;

SQL>  select BUNDLE_SERIES,PATCH_UID,PATCH_ID,VERSION,ACTION,STATUS,ACTION_TIME ,DESCRIPTION from dba_registry_sqlpatch;

SQL>  select DESCRIPTION from dba_registry_sqlpatch;

SQL>  SELECT NAME,STATUS,MESSAGE FROM PDB_PLUG_IN_VIOLATIONS;
```

![image-20211102113113855](Oracle Restart(ASM).assets/image-20211102113113855.png)
