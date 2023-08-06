import pymysql
import sys

def connect_(username,pwd,host,database,port):
    """
    Input :

    username: String  : username of the sql database
    pwd: String :password of the sql database
    host: String :host ip
    database: String :database name to be used
    port : String: database port

    Output:
    :return: connection object if successfull, else returns
    """
    try :
        connection = pymysql.connect(host=host,
                               user=username,
                               password=pwd,
                               db=database,port = int(port)
                               )
    except:

        raise ValueError(str(sys.exc_info()[1]))

    return connection