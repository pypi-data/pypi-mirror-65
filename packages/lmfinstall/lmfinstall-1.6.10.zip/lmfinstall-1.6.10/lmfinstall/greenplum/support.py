from lmfinstall.python import python352 

def python(pin,python_file):
    for conp in pin:
        print(conp[0])
        python352.install(conp,python_file)







#hba 自动化管理

# def enable_pg_hba(ips=None):
#     conp=["root@192.168.4.183:22","rootHDPHAWQMaster1@zhulong.com","master1"] 
#     c=Connection(conp[0],connect_kwargs={"password":conp[1]})
#     if ips is None:ips=[190,191,192,193,194,195,196,197,171]#,202,203,204,205,206,207]
#     for ip in ips:
#         c.run("""sed -i 's/#*host    all         developer        192.168.4.%d\\/32   md5/host    all         developer        192.168.4.%d\\/32   md5/g' /data/greenplum/data/master/seg-1/pg_hba.conf """%(ip,ip),pty=True,encoding='utf8')
#     c.run("""su -l  gpadmin1 -c  "gpstop -u" """,pty=True,encoding='utf8')

# def disable_pg_hba(ips=None):
#     conp=["root@192.168.4.183:22","rootHDPHAWQMaster1@zhulong.com","master1"] 
#     c=Connection(conp[0],connect_kwargs={"password":conp[1]})
#     if ips is None:ips=[190,191,192,193,194,195,196,197,171]#,202,203,204,205,206,207]
#     for ip in ips:
#         c.run("""sed -i 's/^host    all         developer        192.168.4.%d\\/32   md5/#host    all         developer        192.168.4.%d\\/32   md5/g' /data/greenplum/data/master/seg-1/pg_hba.conf """%(ip,ip),pty=True,encoding='utf8')
#     c.run("""su -l  gpadmin1 -c  "gpstop -u" """,pty=True,encoding='utf8')