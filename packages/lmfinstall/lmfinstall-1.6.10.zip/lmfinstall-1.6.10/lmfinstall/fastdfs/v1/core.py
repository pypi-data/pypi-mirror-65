from fabric import Connection
from invoke import Responder
import shutil
import os ,sys,copy

class fdfs:
    def __init__(self,pin=None):
        self.tdir='/root/lmfinstall_fdfs'
        if __name__!='__main__':
            path=os.path.dirname(__file__)
        else:
            path=os.path.dirname(sys.argv[0])
        path=os.path.join(path,'file')
        self.filenames=os.listdir(path)
        self.sdir=[os.path.join(path,file) for file in self.filenames ]
        
        if pin is None:
            self.pin=[
                ["root@172.16.0.10:22","Since2015!","master","tracker:/data/fdfs/tracker:22122"] ,
                ["root@172.16.0.11:22","Since2015!","seg1","storage:group1:/data/fdfs/storage/base:/data/fdfs/storage,/data1/fdfs/storage:23000"] ,
                #["root@172.16.0.12:22","Since2015!","seg2","storage:group1:/data/fdfs/storage/base:/data/fdfs/storage,/data1/fdfs/storage:23000"]  ,
                ["root@172.16.32.6:22","Since2015!","seg3","storage:group2:/data/fdfs/storage/base:/data/fdfs/storage:23000"]  
            ]
        else:
            self.pin=copy.deepcopy(pin)

    def add_node(self,conp,tracker_server=None):
        if tracker_server is None:
            thost=self.pin[0][0]
            tport=self.pin[0][3]
            tracker_server=thost[thost.index('@')+1:thost.index(':')]+':'+tport.split(':')[2]
            print(tracker_server)
        
        self.node_install(conp)
        self.node_config(conp,tracker_server)
    def from_zero(self):
        w=None
        for conp in self.pin:
            if conp[3].split(":")[0]=='tracker':w=conp
            self.node_install(conp)

        for conp in self.pin:
            self.node_config(conp)
        self.node_client(w)

    def node_install(self,conp):
        self.node_pre_file(conp)
        self.node_pre_libfastcommon(conp)
        self.node_pre_fastdfs(conp)

    def node_pre_file(self,conp):

        #上传相关文件
        with Connection(conp[0],connect_kwargs={"password":conp[1],"banner_timeout":120}) as c:
            sdir=self.sdir
            tdir=self.tdir
            
            if c.run("test -f %s"%tdir,warn=True).failed:
                c.run("mkdir -p %s"%tdir)
            for file in self.sdir:
                file_dir,file_name=os.path.split(file)
                if  c.run("test -f %s/%s"%(tdir,file_name),pty=True,warn=True).failed:
                    print("上传fastdfs 相关file ---%s"%file_name)
                    c.put(file,tdir)
            c.clear()

    def node_pre_libfastcommon(self,conp):
        libfastcommon=None
        for w in self.filenames:
            if 'libfastcommon' in w:
                libfastcommon=w 
                break
        if libfastcommon is None:return 'no-libfastcommon-file-found'
        
        with Connection(conp[0],connect_kwargs={"password":conp[1],"banner_timeout":120}) as c:
            c.run("yum install -y libevent gcc-c++ ",pty=True)

            c.run("tar -zxvf %s/%s -C /root"%(self.tdir,libfastcommon),pty=True)
            libfastcommon_=libfastcommon.replace('.tar.gz','')
            c.run("cd /root/%s && ./make.sh && ./make.sh install"%(libfastcommon_),pty=True)

            c.clear()

    def node_pre_fastdfs(self,conp):
        fastdfs=None
        for w in self.filenames:
            if w.startswith('fastdfs') and w.endswith('tar.gz'):
                fastdfs=w 
                break
        if fastdfs is None:return 'no-fastdfs-file-found'
        
        with Connection(conp[0],connect_kwargs={"password":conp[1],"banner_timeout":120}) as c:
            c.run("tar -zxvf %s/%s -C /root"%(self.tdir,fastdfs),pty=True)
            fastdfs=fastdfs.replace('.tar.gz','')
            c.run("cd /root/%s && ./make.sh && ./make.sh install"%(fastdfs),pty=True)
            c.clear()

    def node_config(self,conp,tracker_server=None):
        if tracker_server is None:
            thost=self.pin[0][0]
            tport=self.pin[0][3]
            tracker_server=thost[thost.index('@')+1:thost.index(':')]+':'+tport.split(':')[2]
            print(tracker_server)
        cfg=conp[3].split(":")
        if cfg[0]=='tracker':
            with Connection(conp[0],connect_kwargs={"password":conp[1],"banner_timeout":120}) as c:
                c.run("cp /etc/fdfs/tracker.conf.sample /etc/fdfs/tracker.conf ",pty=True)
                c.run("sed -i 's/base_path.*/base_path=%s/g' /etc/fdfs/tracker.conf "%(cfg[1].replace("/",'\/')),pty=True)
                c.run("sed -i 's/^port=.*/port=%s/g' /etc/fdfs/tracker.conf "%(cfg[2]),pty=True)
                c.run("mkdir -p %s "%cfg[1],pty=True)
                c.run("/etc/init.d/fdfs_trackerd start",pty=True)
                c.clear()
        else:
            with Connection(conp[0],connect_kwargs={"password":conp[1],"banner_timeout":120}) as c:
                c.run("cp /etc/fdfs/storage.conf.sample /etc/fdfs/storage.conf ",pty=True)
                c.run("sed -i 's/^group_name=.*/group_name=%s/g' /etc/fdfs/storage.conf "%(cfg[1]),pty=True)
                c.run("sed -i 's/base_path.*/base_path=%s/g' /etc/fdfs/storage.conf "%(cfg[2].replace("/",'\/')),pty=True)
                c.run("mkdir -p %s "%cfg[2],pty=True)
                #store_path
                arr=cfg[3].split(",")
                c.run("sed -i 's/^store_path_count=.*/store_path_count=%s/g' /etc/fdfs/storage.conf "%(len(arr)),pty=True)

                c.run("sed -i 's/^store_path0=.*/store_path0=%s/g' /etc/fdfs/storage.conf "%(arr[0].replace("/",'\/')),pty=True)

                c.run("sed -i '/^store_path[1-9]=.*/d' /etc/fdfs/storage.conf ",pty=True)
                if len(arr)>=2:
                    for i in range(1,len(arr)):
                        c.run("sed -i '/^store_path%d=.*/a\\store_path%d=%s' /etc/fdfs/storage.conf "%(i-1,i,arr[i].replace("/",'\/')),pty=True)

                for store_path in arr:
                    c.run("mkdir -p %s "%store_path,pty=True)

                c.run("sed -i 's/^tracker_server=.*/tracker_server=%s/g' /etc/fdfs/storage.conf "%(tracker_server),pty=True)

                c.run("sed -i 's/^port=.*/port=%s/g' /etc/fdfs/storage.conf "%(cfg[4]),pty=True)

                c.run("/etc/init.d/fdfs_storaged start",pty=True)
                c.clear()

    def node_client(self,conp,tracker_server=None):
        if tracker_server is None:
            thost=self.pin[0][0]
            tport=self.pin[0][3]
            tracker_server=thost[thost.index('@')+1:thost.index(':')]+':'+tport.split(':')[2]
            print(tracker_server)
        with Connection(conp[0],connect_kwargs={"password":conp[1],"banner_timeout":120}) as c:
            c.run("cp /etc/fdfs/client.conf.sample /etc/fdfs/client.conf ",pty=True)
            c.run("sed -i 's/^tracker_server=.*/tracker_server=%s/g' /etc/fdfs/client.conf "%(tracker_server),pty=True)
            c.run("sed -i 's/base_path.*/base_path=\/root\/fdfs-client/g' /etc/fdfs/client.conf ",pty=True)
            c.run("mkdir -p /root/fdfs-client ",pty=True)

        print("for i in {1..100};do /usr/bin/fdfs_upload_file /etc/fdfs/client.conf  /root/greenplum-text-3.4.0-rhel6_x86_64.tar.gz ;done")

        print("/usr/bin/fdfs_monitor /etc/fdfs/storage.conf ")

#fdfs().from_zero()

fdfs().add_node(["root@172.16.0.12:22","Since2015!","seg2","storage:group1:/data/fdfs/storage/base:/data/fdfs/storage,/data1/fdfs/storage:23000"] )