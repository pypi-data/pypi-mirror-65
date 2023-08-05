from fabric import Connection 
import os
import re 
#依赖一个
# run('rpm -ivh /root/cdh/mysql/MySQL-server-5.6.26-1.linux_glibc2.5.x86_64.rpm')
# run('rpm -ivh /root/cdh/mysql/MySQL-client-5.6.26-1.linux_glibc2.5.x86_64.rpm ')
# run(' rpm -ivh /root/cdh/mysql/MySQL-devel-5.6.26-1.linux_glibc2.5.x86_64.rpm')
#conp=["root@172.16.0.13:22","Since2015!"]
#mysql_dir="E:\\download\\mysql5.6"
#install(conp,mysql_dir)
def install(conp,mysql_dir):
    c=Connection(conp[0],connect_kwargs={"password":conp[1]})
    c.run(" rm -rf /tmp/mysql5.6 & mkdir -p /tmp/mysql5.6",pty=True,encoding='utf8')
    
    files=list(   filter( lambda x:x.endswith('rpm'),os.listdir(mysql_dir) ) )
    for file in files:
        file1=os.path.join(mysql_dir,file)
        print(file1)
        c.put(file1,"/tmp/mysql5.6")

    c.run("yum install autoconf -y ",pty=True,encoding='utf8')

    c.run("rpm -e --nodeps mariadb-libs",pty=True,warn=True,encoding='utf8')

    for file in files:
        file2="/tmp/mysql5.6/%s"%file
        print(file2)
        c.run('rpm -ivh %s'%file2,pty=True,encoding='utf8')

    c.run('cp /usr/share/mysql/my-default.cnf  /etc/my.cnf',pty=True,encoding='utf8')
    c.run("""echo "character-set-server=utf8\ncollation-server=utf8_general_ci " >> /etc/my.cnf """,pty=True,encoding='utf8')

    c.run("systemctl start mysql",pty=True,encoding='utf8')

    x=c.run('cat /root/.mysql_secret')
    pd=re.findall('\(local time\): (\w*)',x.stdout)[0]
    c.run("""mysqladmin -hlocalhost -uroot -p%s  password 'since2015' """%pd)
    c.run("""mysql -hlocalhost -uroot -psince2015 -e "delete from mysql.user where host!='localhost';update mysql.user set host='%';flush privileges  " """)
    #c.run("""mysql -hlocalhost -uroot -psince2015 -e 'create database hive;' """)

# conp=["root@172.16.0.13:22","Since2015!"]
# mysql_dir="E:\\download\\mysql5.6"
# install(conp,mysql_dir)