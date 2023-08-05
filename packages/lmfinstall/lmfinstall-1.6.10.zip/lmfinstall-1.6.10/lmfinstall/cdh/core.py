from fabric import Connection

from lmfinstall import common
import os 

def base(pin,java_file):

    common.hostname(pin)

    common.dns(pin)

    common.ssh(pin)
    #java_file="E:\\运维之王\\file\\jdk-8u151-linux-x64.rpm"
    for w in pin :
        conp=w[:2]
        common.java(conp,java_file)


def repo_ambari(pin,repo_url):

    repo1="""
[lmf-cdh]
name=lmf-cdh
baseurl=http://172.16.0.25/ambari/2.5.0.3/centos7/
priority=1
enabled=1
gpgcheck=0
    """
    repo1=repo1.replace("http://172.16.0.25/ambari/2.5.0.3/centos7/",repo_url)

    for w in pin:
        conp=w[:2]
        with Connection(conp[0],connect_kwargs={"password":conp[1]}) as c:

            c.run("""echo "%s" > /etc/yum.repos.d/cdh.repo"""%repo1,pty=True)

def other(pin):
    path1=os.path.join(os.path.dirname(__file__),'jar','mysql-connector-java-5.1.45-bin.jar')

    path2=os.path.join(os.path.dirname(__file__),'jar','postgresql-42.2.1.jar')
    for conp in pin:
        with Connection(conp[0],connect_kwargs={"password":conp[1]}) as c :
            c.run("mkdir -p /usr/share/java",pty=True,encoding="utf8")
            c.put(path1,"/usr/share/java/mysql-connector-java.jar")
            c.put(path2,"/usr/share/java/postgresql.jar")

            c.run("echo never > /sys/kernel/mm/transparent_hugepage/defrag",pty=True,encoding="utf8")
            c.run("echo never > /sys/kernel/mm/transparent_hugepage/enabled",pty=True,encoding="utf8")
            c.run("""sed -i '/vm.swappiness/d' /etc/sysctl.conf """,pty=True,encoding="utf8")
            c.run("echo 'vm.swappiness=30' >> /etc/sysctl.conf & sysctl -p",pty=True,encoding="utf8")

def install(pin,java_file,repo_url):
    base(pin,java_file)
    repo_ambari(pin,repo_url)
    other(pin)



# pin=[
# ["root@172.16.0.10:22","Since2015!","master"],

# #["root@172.16.0.10:22","Since2015!","master"]
# ["root@172.16.0.12:22","Since2015!","datanode1"],


# ["root@172.16.0.39:22","Since2015!","datanode2"],

# ["root@172.16.0.40:22","Since2015!","datanode3"],
# ]
# other(pin)
# java_file="E:/download/jdk-8u151-linux-x64.rpm"

# repo_url="http://172.16.0.25/cm/"
# install(pin,java_file,repo_url)

# echo never > /sys/kernel/mm/transparent_hugepage/defrag
# echo never > /sys/kernel/mm/transparent_hugepage/enabled

# vm/swappiness 设置为最大值 10。当前设置为 30。使用 sysctl 命令在运行时更改该设置并编辑 /etc/sysctl.conf
