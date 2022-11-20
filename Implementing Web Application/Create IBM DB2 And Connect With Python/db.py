import ibm_db
conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=ba99a9e6-d59e-4883-8fc0-d6a8c9f7a08f.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=31321;PROTOCOL=TCPIP;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=rsk98167;PWD=lC3PwBvgyonwS7NT;", "", "")
if conn:
    sql="select * from users"
    stmt = ibm_db.exec_immediate(conn, sql)
    result = ibm_db.fetch_both(stmt)
    while( result ):
        print("Result from XMLSerialize and XMLQuery:", result)
        result = ibm_db.fetch_both(stmt)