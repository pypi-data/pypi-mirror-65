from lmfinstall.greenplum.core import   data,soft ,install 
from lmfinstall.greenplum import support 

import time 

# 环境 cnetos 7.6   + pivotal greenplum.beta 6 rpm 版本  +python3.5.2 
#场景一:
#几台新机器centos 7.6 （测试通过），新装的机器
#此类要运行成功，window上 预先taskkill /F /IM python.exe ;  如果内存太小，考虑预先swap分区
# window上 预先taskkill /F /IM python.exe ;

#百度云上 刚装完机的稍微等一下，等机器初始化完毕，否则容易出错

#gpinitsystem 阶段失败是正常的，此时多运行几次 restart_data即可
def base(pin,gpfile_path,segs_pernode=2,superuser='gpadmin',data_prefix='/data/gpadmin'):

    install(pin,gpfile_path,segs_pernode=segs_pernode,superuser=superuser,data_prefix=data_prefix)



#场景二:
#不重装系统，软件已经安装哈哦，想重新生成data ,且有可能修改data目录 和 segs数量，修改用户
#要注意的是先关闭服务

#1）用户不修改，服务端口不修改，同一时刻只运行一套， data目录修改
#   停掉原有服务，原数据目录不删，且以后可能还想启动。 做法就是 data_prefix='/data/gpadmin1' 
#以后想重新用 /data/gpadmin 时，可修改 用户下.bashrc 文件的  MASTER_DATA_DIRECTORY

#2) 修改用户 服务端口不修改，同一时刻只运行一套 ,data目录修改
# 停掉原有服务，原数据目录不删 做法就是 data_prefix='/data/gpadmin1' 
#因为某些节点连接失败导致的错误，是可预见的，重复运行代码即可
def restart_data(pin,segs_pernode=2,superuser='gpadmin',data_prefix='/data/gpadmin',init=True):

    data(pin,segs_pernode=segs_pernode,superuser=superuser,data_prefix=data_prefix,init=init)


#场景三：需运行不同实例于同一集群的，init= False 手动gpinitsystem 





def complete(pin,gpfile_path,python_file,segs_pernode=2,superuser='gpadmin',data_prefix='/data/gpadmin'):
    bg=time.time()
    install(pin,gpfile_path,segs_pernode=segs_pernode,superuser=superuser,data_prefix=data_prefix)
    ed=time.time()
    cost=int(ed-bg)
    print("软件安装耗时 %d 秒 "%cost)

    support.python(pin,python_file)
    ed=time.time()
    cost=int(ed-bg)
    print("软件安装+后续python 耗时 %d 秒 "%cost)

# 20191119 百度云 centos 7.6 python3.5.2 测试通过 1+3 2p2m  耗时 1298 秒