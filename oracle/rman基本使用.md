# RMAN基本使用

## 1、进入RMAN和基本使用

```
## shell命令
# 进入oracle用户
su - oracle

# 建立用户环境
dbenv

#确认环境
env|grep ORACLE
echo $ORACLE_SID

#启动rman
rman
## rman命令

#以操作系统身份验证连接到目标数据库
connect target /

#报告目标数据库的物理结构
report schema;

#报告那些文件需要备份（根据备份策略）
report need backup;

#从目标数据库的控制文件中查看rman的备份配置信息
show all;

#全库备份
backup database plus archivelog;
```

## 2、关于缺省的备份位置

```
## shell命令
# 进入oracle用户
su - oracle

# 建立用户环境
dbenv

#确认环境
env|grep ORACLE
echo $ORACLE_SID

#启动sqlplus
sqlplus 
## SQL plus 命令
connect / as sysdba
archive log list;
show parameter DB_RECOVERY_FILE_DEST
```

## 3、备份到指定目录

```
## shell命令
# oracle 用户
mkdir -p /u01/app/orabackup
##rman命令

#备份到指定的位置
backup database format '/u01/app/orabackup/mema_%u.db' plus archivelog format '/u01/app/orabackup/mema_%u.arc';
 
```

## 4、查看备份集

```
## rman命令

#查看备份集
list backup;
list backup summary;

# 查看数据文件的备份集
list backup of database;
# 查看所有归档日志文件的备份集
list backup of archivelog all;
# 查看控制文件的备份集
list backup of controlfile;
# 查看参数文件的备份集
list backup of spfile;
```

## 5、典型的备份脚本

```
## rman命令

# 备份配置

# 备份保留策略：基于恢复窗口
RMAN> CONFIGURE RETENTION POLICY TO RECOVERY WINDOW OF 7 DAYS;

#指定备份位置
RMAN> CONFIGURE DEFAULT DEVICE TYPE TO DISK;
RMAN> CONFIGURE CHANNEL DEVICE TYPE DISK FORMAT '/u03/backup/orcl/backup%d_DB_%u_%s_%p';

#控制文件和参数文件自动备份
RMAN> CONFIGURE CONTROLFILE AUTOBACKUP ON;
## rman命令

RUN {
  #全备份
  BACKUP DATABASE PLUS ARCHIVELOG;
  #根据备份保留策略删除过期的备份集
  DELETE NOPROMPT OBSOLETE;
}
```

## 6、FORMAT命令格式

使用backup命令进行备份时，需要明确备份文件的存储路径及文件名称的格式。其路径和格式可以使用FORMAT参数进行统一设置。FORMAT格式由两部分组成：即存储路径和文件名称格式；

如果没有使用FORMAT指定存储路径和文件名称格式，则默认情况下BACKUP所产生的备份集将存储在快闪恢复区中，RMAN自动使用%U来确定文件名称不会被重复。

常用的替换变量：

| 替换变量 | 说明                                                         |
| -------- | ------------------------------------------------------------ |
| %s       | 备份集的ID号                                                 |
| %c       | 备份片的拷贝数                                               |
| %t       | 备份集时间戳                                                 |
| %T       | 年月日格式（YYYYMMDD）                                       |
| %d       | 数据库名称                                                   |
| %D       | 位于该月中的第几天（DD）                                     |
| %M       | 位于该年中第几月（MM）                                       |
| %F       | 一个基于DBID的唯一名称，它的形式为C-DBID-YYYYMMDD-QQ。其中DBID为数据库的DBID，YYYYMMDD为日志，QQ是一个1-256的序列(用于控制文件自动备份) |
| %n       | 数据库名称，向右填补到最大8个字符                            |
| %u       | 一个8个字符的名称，它是根据备份集个数与创建时间信息生成的    |
| %p       | 该备份集中的备份片号，从1开始到创建的文件数。                |
| %U       | 系统生成的一个唯一文件名，对于备份片来说，它的含义相当于%u_%p_%c。 |

## 7、OMF

10g+，OMF+ASM+BTS

**OMF**,全称是Oracle_Managed Files,即Oracle文件管理，使用OMF可以简化管理员的管理工作，不用指定文件的名字、大小、路径，其名字，大小，路径由oracle 自动分配。在删除不再使用的日志、数据、控制文件时，OMF也可以自动删除其对应的OS文件。

OMF有关参数:

| 参数                       | 说明                                                         |
| -------------------------- | ------------------------------------------------------------ |
| db_create_file_dest        | 数据文件缺省位置                                             |
| db_recovery_file_dest      | 快速恢复区位置，日志文件控制文件多重镜像的位置，归档的缺省位置，rman备份的缺省位置 |
| db_create_online_log_dest_ | 日志文件和控制文件多重镜像的进一步设置                       |

**Bigfile tablespace**

在Oracle 10g中，推出了Bigfile tablespace的概念。表空间Tablespace从Oracle 10g以后就分为两个类型，smallfile tablespace和bigfile tablespace。过去一个表空间对应多个数据文件我们成为Smallfile Tablespace。

传统的small datafile每个文件中最多包括**4M**个数据块，按照一个数据块8K的大小核算，最大文件大小为32G。

Bigfile tablespace每个文件中最多包括**4G**个数据块。

每个Small Tablespace理论上能够包括1024个数据文件，这样计算理论的最大值为32TB大小。而Bigfile Datafile具有更强大的数据块block容纳能力，最多能够包括4G个数据块。同样按照数据块8K计算，Bigfile Datafile大小为32KG=32TB。理论上small tablespace和big tablespace总容量相同。

使用大文件表空间的优势

● 使用大文件表空间（bigfile tablespace）可以显著地增强Oracle数据库的存储能力。但是由 于每个数据库最多使用**64K**个数据文件，因此使用大文件表空间时数据库中表空间的极限个数是使用小文件表空间时的1024倍，使用大文件表空间时的总数据 库容量比使用小文件表空间时高出三个数量级。换言之，当一个Oracle数据库使用大文件表空间，且使用最大的数据块容量时（32K），其总容量可以达到 8EB。

● 在超大型数据库中使用大文件表空间减少了数据文件的数量，因此也简化了对数据文件的管理工作。由于数据文件的减少，SGA中关于数据文件的信息，以及控制文件（control file）的容量也得以减小。

● 由于数据文件对用户透明，由此简化了数据库管理工作。

使用大文件表空间时需要考虑的因素

● 大文件表空间（bigfile tablespace）应该和自动存储管理（Automatic  Storage Management）或其他逻辑卷管理工具（logical volume manager）配合使用，这些工具应该能够支持动态扩展逻辑卷，也能支持striping（数据跨磁盘分布）或RAID。

● 应该避免在不支持striping的系统上使用大文件表空间，因为这将不利于并行执行（parallel execution）及 RMAN 的并行备份（backupparallelization）。

● 当表空间正在使用的磁盘组（disk group）可能没有足够的空间，且扩展表空间的唯一办法是向另一个磁盘组加入数据文件时，应避免使用大文件表空间。

● 不建议在不支持大文件的平台上使用大文件表空间，这会限制表空间（tablespace）的容量。参考相关的操作系统文档了解其支持的最大文件容量。

● 如果使用大文件表空间替代传统的表空间，数据库开启（open），checkpoints，以及 DBWR 进程的性能会得到提高。但是增大数据文件（datafile）容量可能会增加备份与恢复的时间。

## 8、用cron自动执行备份

参考：

[Linux Cron 定时任务](https://zhuanlan.zhihu.com/p/353029881)

[Linux创建cron定时任务](https://zhuanlan.zhihu.com/p/343895819)

[Automate RMAN Backup using Shell Script](https://www.support.dbagenesis.com/post/automate-rman-backups-using-shell-scripts)

### 1、确认crond服务已经运行

```
## shell | root用户

systemctl status crond
```

### 2、创建备份目录

```
## shell | oracle用户

cd /u01/app/orabackup
mkdir scripts backups logs
```

### 3、编辑备份脚本

```
vi /u01/app/orabackup/scripts/full_backup.sh
```

> ```
> #!/bin/bash
> 
> export ORACLE_SID=MEMA
> export ORACLE_HOME=/u01/app/oracle/product/12.0.0/db
> export DATE=$(date +%y-%m-%d_%H%M%S)
> 
> rman target / log=/u01/app/orabackup/logs/MEMA_${DATE}.log << EOF
> run
> {
>  CONFIGURE CONTROLFILE AUTOBACKUP FORMAT FOR DEVICE TYPE DISK TO '/u01/app/orabackup/backups/con_pfile_%F';
>   #全备份
>   backup database format '/u01/app/orabackup/backups/%d_%s_%U.db' plus archivelog format '/u01/app/orabackup/backups/%d_%s_%U.arc';
>   #根据备份保留策略删除过期的备份集
>   DELETE NOPROMPT OBSOLETE;
> }
> EOF
> ```

### 4、修改文件权限

```
## shell | oracle用户

chmod 775 /u01/app/orabackup/scripts/full_backup.sh
```

### 5、加入任务调度

编辑crontab，让备份作业自动执行

```
## shell | oracle用户

crontab -e
```

> ```
> 0 13,16 * * *  /u01/app/orabackup/scripts/full_backup.sh
> ```

### 6、确认

```
## shell | oracle用户

crontab -l
```

## 9、数据库异机相同环境恢复

参考：https://oracle-base.com/articles/9i/recovery-manager-9i#DisasterRecoveryNoCatalog

|         | 源库            | 目标库          |
| ------- | --------------- | --------------- |
| 主机    | restart159-udev | restart160-udev |
| ip      | 192.168.56.159  | 192.168.56.160  |
| SID     | MEMA            | -               |
| DB_NAME | mema            | -               |
| 存储    | ASM             | ASM             |

### 1）目标库建立备份目录

```
[oracle@restart160-udev app]$ pwd
/u01/app
[oracle@restart160-udev app]$ mkdir orabackup
```

### 2）源库备份集拷贝到目标库

```
 scp * oracle@restart160-udev:`pwd`
```

过程：

> ```
> [oracle@restart159-udev orabackup]$ scp * oracle@restart160-udev:`pwd`
> oracle@restart160-udev's password:
> con_pfile_c-965776013-20211124-09                                             100%   18MB 101.0MB/s   00:00
> MEMA_85_2l0f0jj9_1_1.db                                                       100% 1187MB 131.8MB/s   00:09
> MEMA_86_2m0f0jjc_1_1.db                                                       100%  577MB 115.3MB/s   00:05
> MEMA_87_2n0f0jje_1_1.db                                                       100%  639MB 127.8MB/s   00:05
> MEMA_88_2o0f0jjf_1_1.arc                                                      100% 7168     5.4MB/s   00:00
> ```

### 3）目标端建立一个最简pfile

```
dbenv
cd $ORACLE_HOME/dbs
export ORACLE_SID=MEMA
echo "DB_NAME=MEMA" > pfile.ini
```

过程：

> ```
> [oracle@restart160-udev orabackup]$ dbenv
> [oracle@restart160-udev orabackup]$ cd $ORACLE_HOME/dbs
> [oracle@restart160-udev dbs]$ export ORACLE_SID=MEMA
> [oracle@restart160-udev dbs]$ echo "DB_NAME=MEMA" > pfile.ini
> ```

### 4）目标端启动例程到nomount状态

```
sqlplus /nolog
connect / as sysdba
startup nomount pfile='pfile.ini'
```

过程：

```
[oracle@restart160-udev dbs]$ sqlplus /nolog

SQL*Plus: Release 12.2.0.1.0 Production on Wed Nov 24 21:47:26 2021

Copyright (c) 1982, 2016, Oracle.  All rights reserved.

SQL> connect / as sysdba
Connected to an idle instance.
SQL> startup nomount pfile='pfile.ini'
ORACLE instance started.

Total System Global Area  306184192 bytes
Fixed Size                  8619936 bytes
Variable Size             239077472 bytes
Database Buffers           50331648 bytes
Redo Buffers                8155136 bytes
SQL> exit
```

### 5）从备份中的spfile恢复pfile

```
rman target /
SET DBID 965776013;
RESTORE SPFILE TO PFILE '/u01/app/oracle/product/12.0.0/db/dbs/initMEMA.ora' FROM AUTOBACKUP;
exit;
```

过程：

> ```
> [oracle@restart160-udev dbs]$ rman target /
> 
> Recovery Manager: Release 12.2.0.1.0 - Production on Wed Nov 24 21:49:37 2021
> 
> Copyright (c) 1982, 2017, Oracle and/or its affiliates.  All rights reserved.
> 
> connected to target database: MEMA (not mounted)
> 
> RMAN> SET DBID 965776013;
> 
> executing command: SET DBID
> 
> RMAN> SET CONTROLFILE AUTOBACKUP FORMAT FOR DEVICE TYPE DISK TO '/u01/app/orabackup/con_pfile_%F';
> 
> executing command: SET CONTROLFILE AUTOBACKUP FORMAT
> 
> RMAN> RESTORE SPFILE TO PFILE '/u01/app/oracle/product/12.0.0/db/dbs/initMEMA.ora' FROM AUTOBACKUP;
> 
> Starting restore at 24-NOV-21
> allocated channel: ORA_DISK_1
> channel ORA_DISK_1: SID=10 device type=DISK
> 
> channel ORA_DISK_1: looking for AUTOBACKUP on day: 20211124
> channel ORA_DISK_1: AUTOBACKUP found: /u01/app/orabackup/con_pfile_c-965776013-20211124-09
> channel ORA_DISK_1: restoring spfile from AUTOBACKUP /u01/app/orabackup/con_pfile_c-965776013-20211124-09
> channel ORA_DISK_1: SPFILE restore from AUTOBACKUP complete
> Finished restore at 24-NOV-21
> 
> RMAN> exit;
> ```

### 6）使用新的pfile启动例程

```
sqlplus /nolog
connect / as sysdba
startup pfile='initMEMA.ora' FORCE NOMOUNT;
exit

mkdir -p /u01/app/oracle/admin/MEMA_S1/adump

sqlplus /nolog
connect / as sysdba
startup pfile='initMEMA.ora' FORCE NOMOUNT;
exit
```

过程：

> ```
> [oracle@restart160-udev dbs]$ sqlplus /nolog
> 
> SQL*Plus: Release 12.2.0.1.0 Production on Wed Nov 24 21:56:19 2021
> 
> Copyright (c) 1982, 2016, Oracle.  All rights reserved.
> 
> SQL> connect / as sysdba
> 
> SQL> startup pfile='initMEMA.ora' FORCE NOMOUNT;
> ORA-09925: Unable to create audit trail file
> Linux-x86_64 Error: 2: No such file or directory
> Additional information: 9925
> SQL> exit
> 
> Disconnected from Oracle Database 12c Enterprise Edition Release 12.2.0.1.0 - 64bit Production
> 
> [oracle@restart160-udev dbs]$ mkdir -p /u01/app/oracle/admin/MEMA_S1/adump
> 
> [oracle@restart160-udev dbs]$ sqlplus /nolog
> 
> SQL*Plus: Release 12.2.0.1.0 Production on Wed Nov 24 22:01:43 2021
> 
> Copyright (c) 1982, 2016, Oracle.  All rights reserved.
> 
> SQL> connect / as sysdba
> Connected to an idle instance.
> SQL> startup pfile='initMEMA.ora' FORCE NOMOUNT;
> ORACLE instance started.
> 
> Total System Global Area 2415919104 bytes
> Fixed Size                  8795616 bytes
> Variable Size             671091232 bytes
> Database Buffers         1728053248 bytes
> Redo Buffers                7979008 bytes
> 
> SQL> exit
> ```

### 7）恢复控制文件并mount数据库

```
rman target /
SET DBID 965776013;
SET CONTROLFILE AUTOBACKUP FORMAT FOR DEVICE TYPE DISK TO '/u01/app/orabackup/con_pfile_%F';
RESTORE CONTROLFILE FROM AUTOBACKUP;
ALTER DATABASE MOUNT;
```

过程：

> ```
> [oracle@restart160-udev dbs]$ rman target /
> 
> Recovery Manager: Release 12.2.0.1.0 - Production on Wed Nov 24 22:03:30 2021
> 
> Copyright (c) 1982, 2017, Oracle and/or its affiliates.  All rights reserved.
> 
> connected to target database: MEMA (not mounted)
> 
> RMAN> SET DBID 965776013;
> 
> executing command: SET DBID
> 
> RMAN> SET CONTROLFILE AUTOBACKUP FORMAT FOR DEVICE TYPE DISK TO '/u01/app/orabackup/con_pfile_%F';
> 
> executing command: SET CONTROLFILE AUTOBACKUP FORMAT
> 
> RMAN> RESTORE CONTROLFILE FROM AUTOBACKUP;
> 
> Starting restore at 24-NOV-21
> using target database control file instead of recovery catalog
> allocated channel: ORA_DISK_1
> channel ORA_DISK_1: SID=265 device type=DISK
> 
> recovery area destination: +RECO
> database name (or database unique name) used for search: MEMA_S1
> channel ORA_DISK_1: no AUTOBACKUPS found in the recovery area
> channel ORA_DISK_1: looking for AUTOBACKUP on day: 20211124
> channel ORA_DISK_1: AUTOBACKUP found: /u01/app/orabackup/con_pfile_c-965776013-20211124-09
> channel ORA_DISK_1: restoring control file from AUTOBACKUP /u01/app/orabackup/con_pfile_c-965776013-20211124-09
> channel ORA_DISK_1: control file restore from AUTOBACKUP complete
> output file name=+DATA/MEMA_S1/CONTROLFILE/current.258.1089497059
> output file name=+RECO/MEMA_S1/CONTROLFILE/current.256.1089497059
> Finished restore at 24-NOV-21
> 
> RMAN> ALTER DATABASE MOUNT;
> 
> Statement processed
> released channel: ORA_DISK_1
> 
> RMAN>
> ```

### 8）还原和恢复数据库

```
RESTORE DATABASE;
RECOVER DATABASE;
```

过程：

> ```
> RMAN>  RESTORE DATABASE;
> 
> Starting restore at 24-NOV-21
> Starting implicit crosscheck backup at 24-NOV-21
> allocated channel: ORA_DISK_1
> channel ORA_DISK_1: SID=267 device type=DISK
> Crosschecked 10 objects
> Finished implicit crosscheck backup at 24-NOV-21
> 
> Starting implicit crosscheck copy at 24-NOV-21
> using channel ORA_DISK_1
> Finished implicit crosscheck copy at 24-NOV-21
> 
> searching for all files in the recovery area
> cataloging files...
> no files cataloged
> 
> using channel ORA_DISK_1
> 
> channel ORA_DISK_1: starting datafile backup set restore
> channel ORA_DISK_1: specifying datafile(s) to restore from backup set
> channel ORA_DISK_1: restoring datafile 00001 to +DATA/MEMA_S1/DATAFILE/system.257.1088543993
> channel ORA_DISK_1: restoring datafile 00003 to +DATA/MEMA_S1/DATAFILE/sysaux.258.1088544017
> channel ORA_DISK_1: restoring datafile 00004 to +DATA/MEMA_S1/DATAFILE/undotbs1.259.1088544033
> channel ORA_DISK_1: restoring datafile 00007 to +DATA/MEMA_S1/DATAFILE/users.260.1088544033
> channel ORA_DISK_1: reading from backup piece /u01/app/orabackup/MEMA_85_2l0f0jj9_1_1.db
> channel ORA_DISK_1: piece handle=/u01/app/orabackup/MEMA_85_2l0f0jj9_1_1.db tag=TAG20211124T201537
> channel ORA_DISK_1: restored backup piece 1
> channel ORA_DISK_1: restore complete, elapsed time: 00:00:03
> channel ORA_DISK_1: starting datafile backup set restore
> channel ORA_DISK_1: specifying datafile(s) to restore from backup set
> channel ORA_DISK_1: restoring datafile 00009 to +DATA/MEMA_S1/D0AC83B7D6866E2FE0539F38A8C0A50C/DATAFILE/system.272.1088544351
> channel ORA_DISK_1: restoring datafile 00010 to +DATA/MEMA_S1/D0AC83B7D6866E2FE0539F38A8C0A50C/DATAFILE/sysaux.273.1088544351
> channel ORA_DISK_1: restoring datafile 00011 to +DATA/MEMA_S1/D0AC83B7D6866E2FE0539F38A8C0A50C/DATAFILE/undotbs1.271.1088544351
> channel ORA_DISK_1: restoring datafile 00012 to +DATA/MEMA_S1/D0AC83B7D6866E2FE0539F38A8C0A50C/DATAFILE/users.275.1088544355
> channel ORA_DISK_1: reading from backup piece /u01/app/orabackup/MEMA_86_2m0f0jjc_1_1.db
> channel ORA_DISK_1: piece handle=/u01/app/orabackup/MEMA_86_2m0f0jjc_1_1.db tag=TAG20211124T201537
> channel ORA_DISK_1: restored backup piece 1
> channel ORA_DISK_1: restore complete, elapsed time: 00:00:01
> channel ORA_DISK_1: starting datafile backup set restore
> channel ORA_DISK_1: specifying datafile(s) to restore from backup set
> channel ORA_DISK_1: restoring datafile 00005 to +DATA/MEMA_S1/4700A987085B3DFAE05387E5E50A8C7B/DATAFILE/system.267.1088544089
> channel ORA_DISK_1: restoring datafile 00006 to +DATA/MEMA_S1/4700A987085B3DFAE05387E5E50A8C7B/DATAFILE/sysaux.266.1088544089
> channel ORA_DISK_1: restoring datafile 00008 to +DATA/MEMA_S1/4700A987085B3DFAE05387E5E50A8C7B/DATAFILE/undotbs1.268.1088544089
> channel ORA_DISK_1: reading from backup piece /u01/app/orabackup/MEMA_87_2n0f0jje_1_1.db
> channel ORA_DISK_1: piece handle=/u01/app/orabackup/MEMA_87_2n0f0jje_1_1.db tag=TAG20211124T201537
> channel ORA_DISK_1: restored backup piece 1
> channel ORA_DISK_1: restore complete, elapsed time: 00:00:01
> Finished restore at 24-NOV-21
> 
> RMAN> RECOVER DATABASE;
> 
> Starting recover at 24-NOV-21
> using channel ORA_DISK_1
> 
> starting media recovery
> 
> channel ORA_DISK_1: starting archived log restore to default destination
> channel ORA_DISK_1: restoring archived log
> archived log thread=1 sequence=40
> channel ORA_DISK_1: reading from backup piece /u01/app/orabackup/MEMA_88_2o0f0jjf_1_1.arc
> channel ORA_DISK_1: piece handle=/u01/app/orabackup/MEMA_88_2o0f0jjf_1_1.arc tag=TAG20211124T201543
> channel ORA_DISK_1: restored backup piece 1
> channel ORA_DISK_1: restore complete, elapsed time: 00:00:01
> archived log file name=+RECO/MEMA_S1/ARCHIVELOG/2021_11_24/thread_1_seq_40.259.1089497155 thread=1 sequence=40
> channel default: deleting archived log(s)
> archived log file name=+RECO/MEMA_S1/ARCHIVELOG/2021_11_24/thread_1_seq_40.259.1089497155 RECID=40 STAMP=1089497155
> unable to find archived log
> archived log thread=1 sequence=41
> RMAN-00571: ===========================================================
> RMAN-00569: =============== ERROR MESSAGE STACK FOLLOWS ===============
> RMAN-00571: ===========================================================
> RMAN-03002: failure of recover command at 11/24/2021 22:05:56
> RMAN-06054: media recovery requesting unknown archived log for thread 1 with sequence 41 and starting SCN of 2284466
> ```

### 9）打开数据库

```
ALTER DATABASE OPEN RESETLOGS;
```

过程：

> ```
> RMAN> ALTER DATABASE OPEN RESETLOGS;
> 
> Statement processed
> ```

### 10）验证

```
sqlplus /nolog
connect / as sysdba
show pdbs
select * from all_users;
```

过程：

> ```
> [oracle@restart160-udev dbs]$ sqlplus /nolog
> 
> SQL*Plus: Release 12.2.0.1.0 Production on Wed Nov 24 22:06:49 2021
> 
> Copyright (c) 1982, 2016, Oracle.  All rights reserved.
> 
> SQL> connect / as sysdba
> Connected.
> SQL> show pdbs
> 
>     CON_ID CON_NAME                       OPEN MODE  RESTRICTED
> ---------- ------------------------------ ---------- ----------
>          2 PDB$SEED                       READ ONLY  NO
>          3 PDB1                           READ WRITE NO
> SQL> select * from all_users;
> ...
> ```

### 11）注册数据库到crs

```
sqlplus / as sysdba 
create spfile='+DATA/spfileMEMA.ORA' from pfile;
gridenv
srvctl add database -db MEMA_S1 -dbname MEMA -instance MEMA -oraclehome /u01/app/oracle/product/12.0.0/db -spfile '+DATA/spfileMEMA.ORA'  -diskgroup "DATA,RECO"
```

如果无法启动，是找不到控制文件：

```
SQL> alter system set control_files='+DATA/MEMA_S1/CONTROLFILE/current.258.1089497059','+RECO/MEMA_S1/CONTROLFILE/current.256.1089497059' scope=spfile;
```