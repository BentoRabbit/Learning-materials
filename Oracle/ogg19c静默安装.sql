***报错先决条件swap空间不足解决
***测试写入数据内存是否足够
dd if=/dev/zero of=/dataB/swapfile bs=1M count=512

mkswap /dataB/swapfile

swapon /dataB/swapfile
***vi /etc/fstab
/dataB/swapfile swap swap defaults 0 0


***静默安装
./runInstaller  -silent -responseFile /dataB/oggsoft/fbo_ggs_Linux_x64_shiphome/Disk1/response/oggcore.rsp



***修改静默安装脚本
vi oggcore.rsp

INSTALL_OPTION=ORA18c

SOFTWARE_LOCATION=/oracle/soft/ogg18

START_MANAGER=mgr

MANAGER_PORT=7844

DATABASE_LOCATION=/oracle/app/oracle/product/12.2.0/dbhome_1

INVENTORY_LOCATION=/oracle/app/oraInventory

UNIX_GROUP_NAME=oinstall



