import cx_Oracle
import sys

def connect_oracle(username,pwd,host,port,sid):

    """
    Input:

    username : String : Database username
    pwd: String : Database password
    host : String : Database host ip
    sid : String : Database host
    """


    dsn =   cx_Oracle.makedsn(host,port,service_name = sid).replace('SID','SERVICE_NAME')
    try :
        o_connect = cx_Oracle.connect(username,pwd,dsn=dsn)
    except:

        raise ValueError(sys.exc_info()[1])

    return o_connect
