# Oracle中用expdp/impdp,exp/imp命令参数详解

## 一丶expdp介绍

以下是参数的详解，常用参数红色标出:

| **关键字**                              | **说明**                                                     | **默认值**                                                   |
| --------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| ATTACH                                  | 连接到现有作业                                               | 例如, ATTACH=job_name                                        |
| COMPRESSION                             | 减少转储文件大小                                             | ALL, DATA_ONLY, [METADATA_ONLY] 和 NONE                      |
| <font color=#FF0000 >CONTENT</font>     | 指定要卸载的数据                                             | [ALL], DATA_ONLY 和 METADATA_ONLY                            |
| DATA_OPTIONS                            | 数据层选项标记                                               | XML_CLOBS                                                    |
| DIRECTORY                               | 用于转储文件和日志文件的目录对象                             |                                                              |
| <font color=#FF0000 >DUMPFILE</font>    | 指定目标转储文件名的列表 [expdat.dmp]                        |                                                              |
| ENCRYPTION                              | 加密某个转储文件的一部分或全部                               | ALL, DATA_ONLY, ENCRYPTED_COLUMNS_ONLY, METADATA_ONLY 和 NONE |
| ENCRYPTION_ALGORITHM                    | 指定加密的方式                                               | [AES128], AES192 和 AES256                                   |
| <font color=#FF0000 >cluster</font>     | 关闭集群导入导出                                             |                                                              |
| ENCRYPTION_MODE                         | 生成加密密钥的方法                                           | DUAL, PASSWORD 和 [TRANSPARENT]                              |
| ENCRYPTION_PASSWORD                     | 用于在转储文件中创建加密数据的口令密钥                       |                                                              |
| ESTIMATE                                | 计算作业估计值                                               | [BLOCKS] 和 STATISTICS                                       |
| ESTIMATE_ONLY                           | 计算作业估计值而不执行导出                                   |                                                              |
| EXCLUDE                                 | 排除特定对象类型                                             | 例如, EXCLUDE=SCHEMA:"='HR'"                                 |
| FILESIZE                                | 以字节为单位指定每个转储文件的大小                           |                                                              |
| FLASHBACK_SCN                           | SCN号                                                        |                                                              |
| FLASHBACK_TIME                          | SCN号最接近指定时间的时间                                    |                                                              |
| <font color=#FF0000 >FULL</font>        | 导出整个数据库                                               | (N)                                                          |
| HELP                                    | 显示帮助消息                                                 | (N)                                                          |
| INCLUDE                                 | 包括特定对象类型                                             | 例如, INCLUDE=TABLE_DATA                                     |
| JOB_NAME                                | 要创建的导出作业的名称                                       |                                                              |
| <font color=#FF0000 >LOGFILE</font>     | 指定日志文件名                                               | [export.log]                                                 |
| NETWORK_LINK                            | 源系统的远程数据库链接的名称                                 |                                                              |
| NOLOGFILE                               | 不写入日志文件                                               | (N)                                                          |
| PARALLEL                                | 更改当前作业的活动 worker 的数量                             |                                                              |
| <font color=#FF0000 >PARFILE</font>     | 指定参数文件名                                               |                                                              |
| <font color=#FF0000 >QUERY</font>       | 用于导出表的子集的谓词子句                                   | 例如, QUERY=employees:"WHERE department_id > 10"             |
| REMAP_DATA                              | 指定数据转换函数                                             | 例如, REMAP_DATA=EMP.EMPNO:REMAPPKG.EMPNO                    |
| REUSE_DUMPFILES                         | 覆盖目标转储文件 (如果文件存在)                              | (N)                                                          |
| SAMPLE                                  | 要导出的数据的百分比                                         |                                                              |
| <font color=#FF0000 >SCHEMAS</font>     | 要导出的方案的列表 [登录方案]                                |                                                              |
| SOURCE_EDITION                          | 用于提取元数据的版本                                         |                                                              |
| STATUS                                  | 监视作业状态的频率, 其中 默认值 [0] 表示只要有新状态可用, 就立即显示新状态 |                                                              |
| <font color=#FF0000 >TABLES</font>      | 标识要导出的表的列表                                         | 例如, TABLES=HR.EMPLOYEES                                    |
| <font color=#FF0000 >TABLESPACES</font> | 标识要导出的表空间的列表                                     |                                                              |
| TRANSPORTABLE                           | 指定是否可以使用可传输方法                                   | ALWAYS 和 [NEVER]                                            |
| TRANSPORT_FULL_CHECK                    | 验证所有表的存储段                                           | (N)                                                          |
| TRANSPORT_TABLESPACES                   | 要从中卸载元数据的表空间的列表                               |                                                              |
| VERSION                                 | 要导出的对象版本                                             | [COMPATIBLE], LATEST 或任何有效的数据库版本                  |

### 1.1 CONTENT

该选项用于指定要导出的内容.默认值为ALL
CONTENT={ALL | DATA_ONLY | METADATA_ONLY}
当设置CONTENT为ALL时,将导出对象定义及其所有数据。为DATA_ONLY时,只导出对象数据,为METADATA_ONLY时,只导出对象定义

```
----------只导出对象定义
expdp system/oracle@tnsname directory=expdp  dumpfile=test.dmp content=metadata_only

----------导出所有数据
expdp system/oracle@tnsname directory=expdp  dumpfile=test.dmp content=data_only
```

### 1.2 DUMPFILE

用于指定转储文件的名称,默认名称为expdat.dmp
DUMPFILE=[directory_object:]file_name [,….]
Directory_object用于指定目录对象名,file_name用于指定转储文件名.需要注意,如果不指定directory_object,导出工具会自动使用DIRECTORY选项指定的目录对象

```
expdp system/oracle@tnsname directory=expdp  dumpfile=test.dmp
```

### 1.3 数据泵工具导出的步骤：

```
(1)、创建DIRECTORY
create directory 目录名 as '路径';

(2)、授权与查看
Grant read,write on directory 目录名 to 用户名;

--查看目录
select * from dba_directories;

(3)、执行导出
expdp system/oracle@tnsname directory=目录名 dumpfile=expdp_test1.dmp logfile=expdp_test1.log;

备注：
(4)、directory=目录名 必须放在前面，如果将其放置最后，会提示:

ORA-39002: 操作无效
ORA-39070: 无法打开日志文件。
ORA-39087: 目录名 DATA_PUMP_DIR; 无效

(5)、在导出过程中，DATA DUMP 创建并使用了一个名为SYS_EXPORT_SCHEMA_01的对象，此对象就是DATA DUMP导出过程中所用的JOB名字，如果在执行这个命令时如果没有指定导出的JOB名字那么就会产生一个默认的JOB名字，如果在导出过程中指定JOB名字就为以指定名字出现
     如下改成：
expdp system/oracle@tnsname schemas=pdb1 directory=目录名 dumpfile=expdp_test1.dmp logfile=expdp_test1.log job_name=my_job1

(6)、导出语句后面不要有分号，否则如上的导出语句中的job表名为‘my_job1;’，而不是my_job1。因此导致expdp system/oracle attach=tnsname.my_job1执行该命令时一直提示找不到job表
```



### 2.数据泵导出的各种模式：

举例：

```
1、 按表模式导出：
expdp system/oracle@tnsname directory=expdump dumpfile=test0322.dmp logfile=exp_test0322_1.log tables=用户.table1,用户.table2

2、按查询条件导出：
expdp system/oracle@tnsname directory=expdump tables=用户.table1 dumpfile=test0322.dmp logfile=exp_test0322_2.log  query='"where rownum<11"'

3、按表空间导出
expdp system/oracle@tnsname directory=expdump dumpfile=test0322.dmp tablespaces=表空间名 logfile=exp_test0322_3.log  

4、按用户导出
expdp system/oracle@tnsname schemas=用户 directory=expdump dumpfile =test0322.dmp logfile=exp_test0322_4.log;

5、导出整个数据库
expdp system/oracle@tnsname directory=expdump dumpfile=test0322.dmp logfile=exp_test0322_5.log full=y 
```



####################################################################################################

## 二丶impdp介绍

以下是参数的详解，常用参数红色标出:

| **关键字**                                   | **说明**                                                     | 有效的关键字或**默认值**                                |
| -------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------- |
| ATTACH                                       | 连接到现有作业                                               |                                                         |
| DATA_OPTIONS                                 | 数据层选项标记                                               | SKIP_CONSTRAINT_ERRORS                                  |
| <font color=#FF0000 >DIRECTORY</font>        | 用于转储文件, 日志文件和 SQL 文件的目录对象                  |                                                         |
| <font color=#FF0000 >DUMPFILE</font>         | 要从中导入的转储文件的列表                                   |                                                         |
| ENCRYPTION_PASSWORD                          | 用于访问转储文件中的加密数据的口令密钥                       |                                                         |
| ESTIMATE                                     | 计算作业估计值                                               | [BLOCKS] 和 STATISTICS                                  |
| <font color=#FF0000 >EXCLUDE</font>          | 排除特定对象类型                                             |                                                         |
| FLASHBACK_SCN                                | 用于重置会话快照的 SCN                                       |                                                         |
| FLASHBACK_TIME                               | 用于查找最接近的相应 SCN 值的时间                            |                                                         |
| <font color=#FF0000 >FULL</font>             | 导入源中的所有对象                                           | (Y)                                                     |
| HELP                                         | 显示帮助消息                                                 | (N)                                                     |
| INCLUDE                                      | 包括特定对象类型                                             |                                                         |
| JOB_NAME                                     | 要创建的导入作业的名称                                       |                                                         |
| <font color=#FF0000 >LOGFILE</font>          | 日志文件名                                                   |                                                         |
| NOLOGFILE                                    | 不写入日志文件                                               | (N)                                                     |
| PARALLEL                                     | 更改当前作业的活动 worker 的数量                             |                                                         |
| <font color=#FF0000 >PARFILE</font>          | 指定参数文件                                                 |                                                         |
| PARTITION_OPTIONS                            | 指定应如何转换分区                                           | DEPARTITION, MERGE 和 [NONE]                            |
| QUERY                                        | 用于导入表的子集的谓词子句                                   |                                                         |
| REMAP_DATA                                   | 指定数据转换函数                                             |                                                         |
| REMAP_DATAFILE                               | 在所有 DDL 语句中重新定义数据文件引用                        |                                                         |
| <font color=#FF0000 >REMAP_SCHEMA</font>     | 将一个方案中的对象加载到另一个方案                           |                                                         |
| <font color=#FF0000 >REMAP_TABLE</font>      | 将表名重新映射到另一个表                                     |                                                         |
| <font color=#FF0000 >REMAP_TABLESPACE</font> | 将表空间对象重新映射到另一个表空间                           |                                                         |
| REUSE_DATAFILES                              | 如果表空间已存在, 则将其初始化                               | (N)                                                     |
| <font color=#FF0000 >SCHEMAS</font>          | 要导入的方案的列表                                           |                                                         |
| SKIP_UNUSABLE_INDEXES                        | 跳过设置为“索引不可用”状态的索引                             |                                                         |
| SOURCE_EDITION                               | 用于提取元数据的版本                                         |                                                         |
| SQLFILE                                      | 将所有的 SQL DDL 写入指定的文件                              |                                                         |
| STATUS                                       | 监视作业状态的频率, 其中 默认值 [0] 表示只要有新状态可用, 就立即显示新状态 |                                                         |
| STREAMS_CONFIGURATION                        | 启用流元数据的加载                                           |                                                         |
| TABLE_EXISTS_ACTION                          | 导入对象已存在时执行的操作                                   | APPEND, REPLACE, [SKIP] 和 TRUNCATE                     |
| <font color=#FF0000 >TABLES</font>           | 标识要导入的表的列表                                         | 例如, TABLES=HR.EMPLOYEES                               |
| <font color=#FF0000 >TABLESPACES</font>      | 标识要导入的表空间的列表                                     |                                                         |
| TARGET_EDITION                               | 用于加载元数据的版本                                         |                                                         |
| TRANSFORM                                    | 要应用于适用对象的元数据转换                                 | OID, PCTSPACE, SEGMENT_ATTRIBUTES 和 STORAGE            |
| TRANSPORTABLE                                | 用于选择可传输数据移动的选项                                 | ALWAYS 和 [NEVER]。仅在 NETWORK_LINK 模式导入操作中有效 |
| TRANSPORT_DATAFILES                          | 按可传输模式导入的数据文件的列表                             |                                                         |
| TRANSPORT_FULL_CHECK                         | 验证所有表的存储段                                           | (N)                                                     |
| TRANSPORT_TABLESPACES                        | 要从中加载元数据的表空间的列表                               |                                                         |
| VERSION                                      | 要导入的对象的版本                                           | [COMPATIBLE], LATEST 或任何有效的数据库版本             |



举例：

```
1、按表导入
impdp system/oracle@tnsname  dumpfile=test.dmp logfile=imp_test01.log directory=impdp tables=table1,table2 

2、按用户导入
（可以将用户信息直接导入，即如果用户信息不存在的情况下也可以直接导入）
impdp system/oracle@tnsname schemas=用户名 dumpfile =test.dmp logfile=imp_test02.log directory=impdp

3、导入整个数据库
impdp system/oracle@tnsname directory=impdp dumpfile=test.dmp logfile=imp_test03.log full=y
```



####################################################################################################

## 三丶exp介绍

以下是参数的详解，常用参数红色标出:

| **关键字**                              | **说明**                                                     | **默认值**     |
| --------------------------------------- | ------------------------------------------------------------ | -------------- |
| USERID                                  | 用户名/密码                                                  | 必须填写       |
| <font color=#FF0000 >FILE</font>        | 指定输出文件                                                 | (EXPDAT.DMP)   |
| COMPRESS                                | 是否压缩导出的文件                                           | (Y)            |
| <font color=#FF0000 >GRANTS</font>      | 导出权限                                                     | (Y)            |
| <font color=#FF0000 >INDEXES </font>    | 导出索引                                                     | (Y)            |
| DIRECT                                  | 直接路径读取导出(导出速度更快)                               | (N)            |
| <font color=#FF0000 >LOG</font>         | 指定屏幕输出的日志文件位置                                   | 分析对象(估计) |
| <font color=#FF0000 >BUFFER</font>      | 数据缓冲区大小单位是bytes(合理值在100MB左右)                 |                |
| <font color=#FF0000 >ROWS</font>        | 导出数据行                                                   | (Y)            |
| CONSISTENT                              | 先导出序列，后导出表(如果序列导出后，表又使用序列插入新数据，会导致数据不一致) | (Y)            |
| <font color=#FF0000 >CONSTRAINTS</font> | 导出约束                                                     | (Y)            |
| OBJECT_CONSISTENT                       | 事务设置为在对象导出期间只读                                 | (N)            |
| FEEDBACK                                | 显示每 x 行 (0) 的进度                                       | (0)            |
| FILESIZE                                | 导出文件的最大尺寸                                           |                |
| FLASHBACK_SCN                           | SCN号                                                        |                |
| FLASHBACK_TIME                          | SCN号最接近指定时间的时间                                    |                |
| QUERY                                   | 选定导出表子集的子句(query="where c1\>20 and c2=to_date")    |                |
| RESUMABLE                               | 导出时在遇到有关空间的错误时挂起                             | (N)            |
| RESUMABLE_NAME                          | 挂起会话的名称，默认值为：'User USERNAME (USERID), Session SESSIONID, Instance INSTANCEID'，可以指定为其它字符串 |                |
| RESUMABLE_TIMEOUT                       | 会话挂起超时，默认值为：7200秒，会话超时也会报错退出程序     |                |
| TTS_FULL_CHECK                          | 对TTS执行完全或部分依赖检查                                  |                |
| VOLSIZE                                 | 磁带卷要写入的字节数(一般不会用)                             |                |
| TABLESPACES                             | 导出指定的表空间列表                                         |                |
| TRANSPORT_TABLESPACE                    | 导出可传输的表空间元数据                                     | (N)            |
| TEMPLATE                                | 调用iAS模式导出的模板名称                                    |                |
| FULL                                    | 导出整个数据库                                               | (N)            |

举例：



 ``` 
1.将数据库中A06018用户与A07031用户的表导出
exp system/manager@TEST
file=/expback/daochu.dmp 
log=/expback/xxx.log 
buffer=999999
grants=y
constraints=y
compress=n
indexes=y
rows=y
owner=(A06018,A07031)

2.将数据库中的表table1 、table2导出
exp system/manager@TEST
file=/expback/daochu.dmp 
log=/expback/xxx.log 
buffer=999999
compress=n
indexes=y
rows=y 
tables=(table1,table2)

3 .将数据库中的表table1中的字段c1,c2筛选条件的数据导出
exp system/manager@TEST
file=d:\daochu.dmp
buffer=999999
compress=n
indexes=y
rows=y 
tables=(table1) 
query=\"where c1>20 and c2=to_date\”
 ```



####################################################################################################

## **四丶imp介绍**

以下是参数的详解，常用参数红色标出:

| **关键字**                            | **说明**                                                     | **默认值**     |
| ------------------------------------- | ------------------------------------------------------------ | -------------- |
| <font color=#FF0000 >FILE</font>      | 指定输出文件                                                 | (EXPDAT.DMP)   |
| <font color=#FF0000 >BUFFER</font>    | 数据缓冲区大小单位是bytes(合理值在100MB左右)                 |                |
| SHOW                                  | 只列出文件内容                                               | (N)            |
| <font color=#FF0000 >IGNORE</font>    | 忽略创建错误                                                 | (N)            |
| <font color=#FF0000 >GRANTS</font>    | 导入权限                                                     | (Y)            |
| <font color=#FF0000 >INDEXES </font>  | 导入索引                                                     | (Y)            |
| <font color=#FF0000 >ROWS</font>      | 导入数据行                                                   | (Y)            |
| <font color=#FF0000 >LOG</font>       | 指定屏幕输出的日志文件位置                                   | 分析对象(估计) |
| DESTROY                               | 覆盖表空间数据文件                                           | (N)            |
| <font color=#FF0000 >FROMUSER</font>  | 所有人用户名列表(导出时的用户名)                             |                |
| <font color=#FF0000 >TOUSER</font>    | 用户名列表(导入时的用户名，如导出导入用户名一致，不需要TOUSER) |                |
| <font color=#FF0000 >TABLES</font>    | 表名列表                                                     |                |
| <font color=#FF0000 >COMMIT</font>    | 提交数组插入                                                 | (N)            |
| INDEXFILE                             | 将表/索引信息写入指定的文件                                  |                |
| CONSTRAINTS                           | 导入约束                                                     | (Y)            |
| FEEDBACK                              | 每x行显示进度(0)                                             |                |
| SKIP_UNUSABLE_INDEXES                 | 跳过不可用索引的维护                                         | (N)            |
| TOID_NOVALIDATE                       | 跳过指定类型id的验证                                         |                |
| FILESIZE                              | 每个转储文件的最大大小                                       |                |
| STATISTICS                            | 导入数据库优化器统计数据                                     | (ALWAYS)       |
| RESUMABLE                             | 导入时在遇到有关空间的错误时挂起                             | (N)            |
| RESUMABLE_NAME                        | 挂起会话的名称，默认值为：'User USERNAME (USERID), Session SESSIONID, Instance INSTANCEID'，可以指定为其它字符串 |                |
| RESUMABLE_TIMEOUT                     | 会话挂起超时，默认值为：7200秒，会话超时也会报错退出程序     |                |
| COMPILE                               | 编译过程, 程序包和函数                                       | (Y)            |
| <font color=#FF0000 >DATA_ONLY</font> | 只导入数据                                                   | (N)            |
| VOLSIZE                               | 磁带卷要写入的字节数(一般不会用)                             |                |
| STREAMS_CONFIGURATION                 | 导入 Streams 的一般元数据                                    | (Y)            |
| STREAMS_INSTANTIATION                 | 导入 Streams 的实例化元数据                                  | (N)            |
| FULL                                  | 导入整个数据库                                               | (N)            |

举例：



```
1.导入一个或一组指定用户所属的全部表、索引和其他对象
imp system/manager file=/seapark.dmp log=/seapark.log fromuser=seapark grants=y indexes=y ignore=y rows=y buffer=999999 commit=y

imp system/manager file=/seapark.dmp log=/seapark.log fromuser=(seapark,amy,amyc,harold) grants=y indexes=y ignore=y rows=y buffer=999999 commit=y

2.将一个用户所属的数据导入另一个用户
imp system/manager file=/tank.dmp log=/tank.log fromuser=seapark touser=seapark_copy
imp system/manager file=/tank.dmp log=/tank.log fromuser=(seapark,amy) touser=(seapark1, amy1)

3.导入一个表
imp system/manager file=/tank.dmp log=/tank.log fromuser=seapark TABLES=(a,b)

4.从多个文件导入
imp system/manager file=(paycheck_1,paycheck_2,paycheck_3,paycheck_4) log=paycheck,filesize=1G full=y

5.使用参数文件
imp system/manager parfile=bible_tables.par

vim bible_tables.par参数文件：
log=/u01/app/oracle/imp/20220217_full.log
file=/u01/app/oracle/imp/20220217_full.dmp
buffer=999999
grants=y
indexes=y
ignore=y 
rows=y
commit=y
constraints=y
fromuser=(A06018,A07031,..)


#parfile 适用于 exp,imp,expdp,impdp
```

## 五、expdp/impdp与exp/imp的区别

(1)  把用户usera的对象导到用户userb,用法区别在于fromuser=usera touser=userb ,remap_schema=usera:usera。

```
例如:
imp system/passwd fromuser=usera touser=userb file=/oracle/exp.dmp log=/oracle/exp.log

impdp system/passwd directory=expdp dumpfile=expdp.dmp remap_schema=usera:userb logfile=/oracle/exp.log
```

(2)  更换表空间，用exp/imp的时候，要想更改表所在的表空间，需要手工去处理

```
alter table xxx move tablespace_new
用impdp只要用remap_tablespace=tabspace_old:tablespace_new
```

(3)  当指定一些表的时候，使用exp/imp 时，tables的用法是 tables=(‘table1′,’table2′,’table3′)。expdp/impdp的用法是tables=table1,table2,table3

(4)  是否要导出数据行

exp（ROWS=Y 导出数据行，ROWS=N 不导出数据行）

expdp content（ALL:对象＋导出数据行，DATA_ONLY：只导出对象，METADATA_ONLY：只导出数据的记录）

(5)  expdp是[10g]的新特性而且只能在服务器执行。而exp/imp是通用的。

(6)  oracle11g中有个新特性，当表无数据时，不分配segment，以节省空间,所以exp导不出空表。解决的办法是用expdp， 当然也可以设置deferred_segment_creation 参数 或者 insert一行，再rollback，但是这样很麻烦。

(7)   在平常备库和数据库迁移的时候，当遇到大的数据库的时候在用exp的时候往往是需要好几个小时，耗费大量时间。oracle10g以后可以用expdp来导出数据库花费的时间要远小于exp花费的时间，而且文件也要小很多。