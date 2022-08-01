# Always On搭建

| **数据库**     | **SQL Server 2019**                         |
| -------------- | ------------------------------------------- |
| **操作系统**   | **Windows Server 2019 R2 DataCenter  64位** |
| **虚拟机环境** | **VMware**                                  |

注：（win2012/win2012R2 只有DataCenter 版本才能使用故障转移集群）

（administrator的密码设置为Mema_1234）

**虚拟机：需要创建3个虚拟机，2节点和1域控**

| 计算机           | 主域控        | 节点1         | 节点2         |
| ---------------- | ------------- | ------------- | ------------- |
| IP               | 192.168.0.134 | 192.168.0.150 | 192.168.0.151 |
| 子网掩码         | 255.255.255.0 | 255.255.255.0 | 255.255.255.0 |
| 默认网关         |               | 192.168.0.1   | 192.168.0.1   |
| 首选DNS服务器    | 127.0.0.1     | 192.168.0.134 | 192.168.0.134 |
|                  |               | 192.168.2.40  | 192.168.2.41  |
|                  |               | 255.255.255.0 | 255.255.255.0 |
| Vip-cluster      | 192.168.0.170 |               |               |
| Sql alwayson VIP | 192.168.0.171 |               |               |

**故障转移集群VIP跟Always On 的VIP的作用是不一样的！**

故障转移集群VIP(192.168.66.170)是让你连接故障转移集群管理器的集群用的，而不是让你连接Always On

Always On 的VIP(192.168.66.171)是用来连接Always On 



## 1、Windows server 2019 系统主域的安装配置

### 1.1、关闭防火墙

![image-20210813095434309](always on搭建.assets/image-20210813095434309.png)

### 1.2、配置域控IP

DNS服务器安装在域控上，首选DNS服务器填写：127.0.0.1

**勾选IPv4**，不用选IPv6

![image-20210813095748308](always on搭建.assets/image-20210813095748308.png)

![image-20210813095705885](always on搭建.assets/image-20210813095705885.png)



### 1.3、域功能安装

#### 1.3.1、 安装AD域服务

打开服务器管理中的仪表板“添加角色和功能“，然后点击下一步

![image-20210813100123125](always on搭建.assets/image-20210813100123125.png)

点击下一步

![image-20210813100140787](always on搭建.assets/image-20210813100140787.png)

选择基于角色或基于功能安装

![image-20210813100226200](always on搭建.assets/image-20210813100226200.png)

选择从服务器池中选择服务器

![image-20210813100257205](always on搭建.assets/image-20210813100257205.png)

选择域服务

![image-20210813100415289](always on搭建.assets/image-20210813100415289.png)

如果跳出添加域服务 所需功能点击添加功能

![image-20210813100332973](always on搭建.assets/image-20210813100332973.png)

默认选项，点击下一步

![image-20210813100611060](always on搭建.assets/image-20210813100611060.png)

点击下一步

![image-20210813100623692](always on搭建.assets/image-20210813100623692.png)

点击安装

（安装AD域服务的同时，操作系统会同时安装好DNS服务器）

![image-20210813100647439](always on搭建.assets/image-20210813100647439.png)

![image-20210813100658391](always on搭建.assets/image-20210813100658391.png)

#### 1.3.2、域功能的安装

方法一：

点击服务器管理器右上角的小旗帜，弹出对话框，点击“将此服务器提升为域控制器”以提升为域控

![image-20210813101500217](always on搭建.assets/image-20210813101500217.png)

方法二：

点击AD DS，然后点击更多，将其升为域控制器

![image-20210813101624326](always on搭建.assets/image-20210813101624326.png)

![image-20210813101650528](always on搭建.assets/image-20210813101650528.png)

进入AD域服务配置向导，选择 添加新林，设置根域名：aaa.com

![image-20210813101841080](always on搭建.assets/image-20210813101841080.png)

设置DSRM密码

默认林中的第一棵域树的根域的域控制器必须担当全局编录服务器和必须安装DNS服务，不能是只读域控制器

(密码：Mema_1234)

![image-20210813102038662](always on搭建.assets/image-20210813102038662.png)

点击下一步（出现的dns警告不影响）

![image-20210813102122322](always on搭建.assets/image-20210813102122322.png)

NetBIOS名称会自动设置（和根域名一致），点击下一步

![image-20210813102225125](always on搭建.assets/image-20210813102225125.png)

按默认设置点击下一步

![image-20210813102412739](always on搭建.assets/image-20210813102412739.png)

显示总结，没问题的话，点击下一步

（AD DS数据库文件路径保持默认就可以了，可以将日志文件和数据库文件放在不同的磁盘有助提升性能，这里选择默认）

![image-20210813102435317](always on搭建.assets/image-20210813102435317.png)

点击安装

![image-20210813102550706](always on搭建.assets/image-20210813102550706.png)

![image-20210813102616304](always on搭建.assets/image-20210813102616304.png)

安装完AD DS之后会**自动重启服务器**，重启服务器后登录界面会出现之前设置的NetBIOS名称

![image-20210813103321511](always on搭建.assets/image-20210813103321511.png)

打开DNS管理器

可以看到域控制器WIN-VC6OHIFAPQA.abc.com已经将主机名（WIN-VC6OHIFAPQA）和IP地址（192.168.0.134）注册到DNS服务器内

![image-20210813104619368](always on搭建.assets/image-20210813104619368.png)

![image-20210813104737167](always on搭建.assets/image-20210813104737167.png)

![image-20210813104929043](always on搭建.assets/image-20210813104929043.png)

注意：如果在tcp文件夹内没有ldap记录和_gc记录相关的记录，那么请重启Netlogon服务来重新注册

检查AD域服务和Netlogon服务是否正常启动

![image-20210813105122645](always on搭建.assets/image-20210813105122645.png)

![image-20210813105145518](always on搭建.assets/image-20210813105145518.png)

### 1.4、SQL用户的创建

在 服务器管理器->工具->Active Directory 用户和计算机

![image-20210813105502318](always on搭建.assets/image-20210813105502318.png)

aaa.com -> User -> 新建 -> 用户 

![image-20210813105618410](always on搭建.assets/image-20210813105618410.png)

![image-20210813105822069](always on搭建.assets/image-20210813105822069.png)

设置密码：Mema_1234 （勾选密码永不过期）

![image-20210813105908235](always on搭建.assets/image-20210813105908235.png)

![image-20210813105926158](always on搭建.assets/image-20210813105926158.png)

域用户zjy创建完成

![image-20210813105950992](always on搭建.assets/image-20210813105950992.png)

将这个域用户加入到域计算机组和域管理员组，右键属性，选择隶属于，添加

![image-20210813110035371](always on搭建.assets/image-20210813110035371.png)

点击高级，立即查询，选择Domain Admins用户和Domain Computers用户

![image-20210813110257359](always on搭建.assets/image-20210813110257359.png)

![image-20210813110328246](always on搭建.assets/image-20210813110328246.png)

将系统自动更新关闭掉（变为手动更新）

```
cmd
sconfig
```

![image-20210813110514540](always on搭建.assets/image-20210813110514540.png)

## 2、群集的配置创建

### 2.1、节点一配置

#### 2.1.1、设置节点1 IP

ipv6去掉，注意要设置网关，禁用TCP/IP上的NetBIOS

![image-20210813132830871](always on搭建.assets/image-20210813132830871.png)

![image-20210813132850518](always on搭建.assets/image-20210813132850518.png)

#### 2.1.2、加入域

右键计算机 属性-> 更改设置->更改->选择“域”并填入主域名->点“确定”->填写账户名(administrator)密码->点“确定”

![image-20210813133534083](always on搭建.assets/image-20210813133534083.png)

![image-20210813133603539](always on搭建.assets/image-20210813133603539.png)

![image-20210813133635393](always on搭建.assets/image-20210813133635393.png)

![image-20210813133730739](always on搭建.assets/image-20210813133730739.png)

![image-20210813133755672](always on搭建.assets/image-20210813133755672.png)

加域后客户端计算机会自动重启，重启后使用本地Administrator用户登录计算机，先不要用域用户（zjy）来登录计算机

选择计算机管理

![image-20210813134046724](always on搭建.assets/image-20210813134046724.png)

![image-20210813134210339](always on搭建.assets/image-20210813134210339.png)

![image-20210813134321162](always on搭建.assets/image-20210813134321162.png)

![image-20210813134657397](always on搭建.assets/image-20210813134657397.png)

![image-20210813134537978](always on搭建.assets/image-20210813134537978.png)

win建+R	输入sconfig

将系统自动更新关闭掉cmd--sconfig

![image-20210813134855807](always on搭建.assets/image-20210813134855807.png)

![image-20210813134834516](always on搭建.assets/image-20210813134834516.png)

#### 2.1.3 、故障转移群集添加

安装故障转移群集

首先在服务管理器中添加角色

![image-20210813135129965](always on搭建.assets/image-20210813135129965.png)

前面都按默认选择，到功能，**勾选故障转移群集**

![image-20210813135231583](always on搭建.assets/image-20210813135231583.png)

点击安装

![image-20210813135247048](always on搭建.assets/image-20210813135247048.png)

![image-20210813135258881](always on搭建.assets/image-20210813135258881.png)

### 2.2、节点二配置

配置方法和节点一一样

### 2.3、群集的创建

使用zjy这个域用户登录计算机(AAA\zjy)

打开“服务器管理器->工具->故障转移群集管理器”

![image-20210813141003264](always on搭建.assets/image-20210813141003264.png)

选择验证配置

![image-20210813141051832](always on搭建.assets/image-20210813141051832.png)

点击下一步

![image-20210813141111285](always on搭建.assets/image-20210813141111285.png)

点击预览

![image-20210813141157299](always on搭建.assets/image-20210813141157299.png)

选择高级

![image-20210813141212787](always on搭建.assets/image-20210813141212787.png)

立即查找，选择所在文件夹是aaa.com/Computer的机器

![image-20210813141237570](always on搭建.assets/image-20210813141237570.png)

点击下一步

![image-20210813141300450](always on搭建.assets/image-20210813141300450.png)

选择运行所有测试，点击下一步

![image-20210813141319975](always on搭建.assets/image-20210813141319975.png)

点击下一步

![image-20210813141335728](always on搭建.assets/image-20210813141335728.png)

点击完成

![image-20210813141533719](always on搭建.assets/image-20210813141533719.png)

报告里面一定不能出现失败，否则你需要检查是什么问题导致失败，失败是建立不了故障转移集群的

出现警告要看情况，对于存储的警告，由于目前为止没有添加任何的存储设备，这里可以忽略，还有网络警告

**创建集群向导**

点击创建集群

![image-20210813141558769](always on搭建.assets/image-20210813141558769.png)

点击下一步

![image-20210813141610381](always on搭建.assets/image-20210813141610381.png)

![image-20210813141641606](always on搭建.assets/image-20210813141641606.png)

输入群集名称：cluster

地址：192.168.0.170

![image-20210813141727247](always on搭建.assets/image-20210813141727247.png)

点击下一步

![image-20210813141746102](always on搭建.assets/image-20210813141746102.png)

![image-20210813141804023](always on搭建.assets/image-20210813141804023.png)

点击完成

![image-20210813141814517](always on搭建.assets/image-20210813141814517.png)

查看报告可以看到 找不到磁盘见证的相应磁盘，因为我们还没加见证共享文件夹或仲裁盘，这里可以忽略

群集创建完成

### 2.4、配置仲裁

由于我们是两个节点的故障转移集群，所以需要加上共享文件夹，在域控上建立一个共享文件夹，让两个集群节点都可以访问

在群集中选择更多操作，配置仲裁设置

![image-20210813142601662](always on搭建.assets/image-20210813142601662.png)

![image-20210813142616754](always on搭建.assets/image-20210813142616754.png)

![image-20210813142634145](always on搭建.assets/image-20210813142634145.png)

![image-20210813142652747](always on搭建.assets/image-20210813142652747.png)

需要在==主域==上创建==共享文件夹==

在C盘上新建一个share文件夹

![image-20210813154249069](always on搭建.assets/image-20210813154249069.png)

右键 share文件夹，点击属性

![image-20210813154355390](always on搭建.assets/image-20210813154355390.png)

点击共享选项卡，选共享

![image-20210813154537970](always on搭建.assets/image-20210813154537970.png)

添加everyone用户，点击共享

![image-20210813154659884](always on搭建.assets/image-20210813154659884.png)

共享文件夹创建完成！

![image-20210813154739483](always on搭建.assets/image-20210813154739483.png)

**添加在主域上创建的共享文件夹路径**

![image-20210813142922465](always on搭建.assets/image-20210813142922465.png)

点击下一步，直到完成

![image-20210813143103717](always on搭建.assets/image-20210813143103717.png)



## 3、安装Sql Server2019

两个节点上安装SQL server2019的方法一样，请先使用本地用户Administrator登录这两个集群节点并执行下面的操作

这里选择全新SQL server独立安装

输入产品密钥

![image-20210813151621743](always on搭建.assets/image-20210813151621743.png)

![image-20210813151802251](always on搭建.assets/image-20210813151802251.png)

![image-20210813151819292](always on搭建.assets/image-20210813151819292.png)

![image-20210813151940001](always on搭建.assets/image-20210813151940001.png)

![image-20210813152302578](always on搭建.assets/image-20210813152302578.png)

![image-20210813152341919](always on搭建.assets/image-20210813152341919.png)

![image-20210813152359322](always on搭建.assets/image-20210813152359322.png)

![image-20210813152428185](always on搭建.assets/image-20210813152428185.png)

![image-20210813152449757](always on搭建.assets/image-20210813152449757.png)

（密码：Mema_1234）

![image-20210813152541203](always on搭建.assets/image-20210813152541203.png)

![image-20210813152642805](always on搭建.assets/image-20210813152642805.png)

![image-20210813152719499](always on搭建.assets/image-20210813152719499.png)

![image-20210813152917808](always on搭建.assets/image-20210813152917808.png)

点击安装

![image-20210813152940170](always on搭建.assets/image-20210813152940170.png)

安装完成

![image-20210813154955548](always on搭建.assets/image-20210813154955548.png)

（另一个节点的安装方式一样）

## 4、配置always on可用性组

### 4.1、域用户phr配置

注销集群节点计算机，然后使用域用户zjy登录，然后设置SQL Server的启动账户为域用户zjy

打开服务管理器，先修改SQL代理的启动账户为域用户zjy,然后再修改SQL 引擎的启动账户为域用户zjy。

找到 SQL Server 代理（MSSQLSERVER），右键，属性

![image-20210813155912887](always on搭建.assets/image-20210813155912887.png)

点击登录选项卡，点击浏览，点位置，选择aaa.com

![image-20210813160038407](always on搭建.assets/image-20210813160038407.png)

点击高级

![image-20210813160102414](always on搭建.assets/image-20210813160102414.png)

添加zjy用户

![image-20210813160325388](always on搭建.assets/image-20210813160325388.png)

输入zjy用户的密码，点应用，后点击确定

![image-20210813160413648](always on搭建.assets/image-20210813160413648.png)

重启一下SQL代理服务

![image-20210813160512970](always on搭建.assets/image-20210813160512970.png)

重启之后可以看到登录用户为zjy@aaa.com

![image-20210813160558641](always on搭建.assets/image-20210813160558641.png)

同样，SQL引擎服务也需要同样的设置

![image-20210813160804437](always on搭建.assets/image-20210813160804437.png)

![image-20210813160845281](always on搭建.assets/image-20210813160845281.png)

![image-20210813160906805](always on搭建.assets/image-20210813160906805.png)

![image-20210813160928024](always on搭建.assets/image-20210813160928024.png)

![image-20210813161023736](always on搭建.assets/image-20210813161023736.png)

![image-20210813161153104](always on搭建.assets/image-20210813161153104.png)

![image-20210813161211220](always on搭建.assets/image-20210813161211220.png)

这样，SQL引擎服务和SQL代理服务都用域用户zjy启动

另一个集群节点的SQL Server也需要做同样的操作

**注意**：在集群节点脱离域之后，SQL引擎服务和SQL代理服务都要用本地服务帐号来启动，不能再用域用户来启动

### 4.2、将zjy域用户加入到两个集群节点的SQL Server登录用户中

打开 **SQL Server Management Studio**

![image-20210814202428738](always on搭建.assets/image-20210814202428738.png)

使用==sa==登录，Server name是 ==.==

![image-20210814203809890](always on搭建.assets/image-20210814203809890.png)

添加登录用户，跟SQL 服务添加启动账户的步骤一样，将zjy域用户添加为登录用户

点击Security，右键Logins，选New Login

![image-20210814204520777](always on搭建.assets/image-20210814204520777.png)

![image-20210814204724877](always on搭建.assets/image-20210814204724877.png)

![image-20210814204750630](always on搭建.assets/image-20210814204750630.png)

![image-20210814204836259](always on搭建.assets/image-20210814204836259.png)

![image-20210814204854698](always on搭建.assets/image-20210814204854698.png)

![image-20210814205100400](always on搭建.assets/image-20210814205100400.png)

设置服务器角色，给予sysadmin权限

![image-20210814205305063](always on搭建.assets/image-20210814205305063.png)

![image-20210814205401563](always on搭建.assets/image-20210814205401563.png)

两个群集节点都这样设置

### 4.3、创建always on可用性组

然后，两个集群节点都可以用zjy域用户来登录SQL Server

![image-20210814210910855](always on搭建.assets/image-20210814210910855.png)

![image-20210814210837425](always on搭建.assets/image-20210814210837425.png)

回到SQL Server配置管理器，启用AlwaysOn可用性组

![image-20210814211058093](always on搭建.assets/image-20210814211058093.png)

点击 启用Always On可用性组，勾选启用Always On可用性组，点击应用，在设置完成后，==重新启动此服务==

![image-20210814211154077](always on搭建.assets/image-20210814211154077.png)

如果AlwaysOn启用成功，在服务器属性里可以看到启用HADR为True

![image-20210814212154269](always on搭建.assets/image-20210814212154269.png)

![image-20210814212132173](always on搭建.assets/image-20210814212132173.png)

两个节点一样操作

在其中一个集群节点的SQL Server中验证各节点的投票数 ，在其中一个集群节点的SQL Server上执行

使用下面SQL语句

```
SELECT * FROM  sys.dm_hadr_cluster_members
```

![image-20210814212504186](always on搭建.assets/image-20210814212504186.png)

```
SELECT * FROM  sys.dm_hadr_cluster
```

![image-20210814213416805](always on搭建.assets/image-20210814213416805.png)

使用自行初始化数据库的方式

**新建**一个测试库和测试表并插入一些测试数据，然后对数据库做一个**完整备份** 和 **日志备份**

![image-20210814215156419](always on搭建.assets/image-20210814215156419.png)

在“Alwayson高可用性”节点上右键选择“新建可用性组向导

![image-20210814215306194](always on搭建.assets/image-20210814215306194.png)

![image-20210814215331506](always on搭建.assets/image-20210814215331506.png)

 输入一个从未使用过的高可用性组名称 steam

![image-20210814215406589](always on搭建.assets/image-20210814215406589.png)

选择要添加的数据库

注意：加入到AlwaysOn可用性组的数据库必须符合下面要求：

1. 数据库的恢复模式必须是“完整”恢复模式
2. 数据库已进行了一次完整备份
3. 需要是用户库，系统库不能加入可用性组
4. 数据库可以读写，只读库不能加入到可用性组
5. 数据库处于多用户模式
6. 数据库没有使用AUTO_CLOSE
7. 不属于任何其他的可用性组
8. 数据库没有配置数据库镜像

一个可用性组最大支持100个数据库

![image-20210814221053270](always on搭建.assets/image-20210814221053270.png)

添加副本

![image-20210814221151072](always on搭建.assets/image-20210814221151072.png)

加入另一个节点

![image-20210814221255898](always on搭建.assets/image-20210814221255898.png)

选择自动故障转移节点和同步提交节点，因为我们只有两个节点。并将辅助副本设置为可读

![image-20210814221828946](always on搭建.assets/image-20210814221828946.png)

点击“端点”tab页面设置端点

![image-20210814222100649](always on搭建.assets/image-20210814222100649.png)

端点URL使用IP的方式，不要用FQDN长名的方式，因为服务器通常会有两个网卡，一个public网卡，一个 private网卡，端点建议使用private网卡地址

![image-20210814222238278](always on搭建.assets/image-20210814222238278.png)

选择初始数据同步，这里选择“仅联接”模式

![image-20210814222308903](always on搭建.assets/image-20210814222308903.png)

因为使用的是“仅联接”数据库初始化方式，验证跳过像可用磁盘空间这样的检查

![image-20210814222357782](always on搭建.assets/image-20210814222357782.png)

点击“完成”。另外，此处也可保存建立可用性组脚本，以便分步诊断故障之用

![image-20210814222418200](always on搭建.assets/image-20210814222418200.png)

所有摘要均成功完成，显示绿色对勾。如果出现黄色警告，则需进行进一步判断是否成功。若出现红色错误， 表示AG创建不成功

![image-20210816093305380](always on搭建.assets/image-20210816093305380.png)

创建完成

主副本

数据库变为已同步

![image-20210816093439782](always on搭建.assets/image-20210816093439782.png)

然后把完整备份文件和日志备份文件复制到WIN-5PMSDHUI0KQ机器上依次进行还原，完整备份->还原完整备份->日志备份->还原日志备份

### 4.4、创建侦听器

在创建可用性组后，在“可用性组侦听器”上右键添加侦听器来创建侦听器，选择静态IP的网络模式（尽量不要选择DHCP网络模式），

输入一个从未使用过的名称（该名称将被用来创建网络名称资源）和访问端口

![image-20210816094203501](always on搭建.assets/image-20210816094203501.png)

![image-20210816094306430](always on搭建.assets/image-20210816094306430.png)

![image-20210816094333089](always on搭建.assets/image-20210816094333089.png)

![image-20210816094343429](always on搭建.assets/image-20210816094343429.png)

![image-20210816094436062](always on搭建.assets/image-20210816094436062.png)

在域控的DNS管理器上会注册一条A记录

![image-20210816094953551](always on搭建.assets/image-20210816094953551.png)





