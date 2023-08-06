from .connection import connect_oracle
import sys
from .query_processor import count_query,fetchone_query,fetchmany_query,update_query,insertone_query,insertmany_query
import pandas as pd
import json 


class oracle:


    def __init__(self):
        """
        Initialising  the variables for use
        """

        self.__username = None
        self.__pwd = None
        self.__host = None
        self.__port = None
        self.__sid = None
        self.connect_check = False




    def setConnect(self,username,password,hostname,port,sid):
        """
        Input :
        username : String : Database Username
        hostname : String : Database Hostname
        password : String : Database password
        sid : String : Database Service ID : Schema Name
        port : String: Database port
        """
        #setting the instance variables using this setter function
        self.__username = username
        self.__pwd = password
        self.__host = hostname
        self.__sid= sid
        self.__port = port



        # connecting to the database to check the connection

        connection = connect_oracle(username=self.__username, pwd=self.__pwd, sid = self.__sid, port=self.__port,
                              host=self.__host)

        self.connect_check = True

        connection.close()





    def count(self,tablename,condition = None):

        """
        Function to get return the count of rows given the condition and the tablename

        Input :
        tablename: String : Table name in DB
        condtion : String : SQL  where clause condition

        Output:
        Count : Integer : Count of the rows for the given condition and  tablename
        """

        if self.connect_check == True:


            #processing the query

            query = count_query(tablename,condition)

            # connecting to the DB
            try:

                connection = connect_oracle(username=self.__username, pwd=self.__pwd, sid=self.__sid, port=self.__port,
                                            host=self.__host)
                cursor = connection.cursor()

            except:

                raise ValueError(sys.exc_info()[1])


            try:
                count = 0

                for i in cursor.execute(query):
                    count = i[0]

                    # closing the connection and cursor

                connection.close()

                return count

            except:

                # closing the connection and cursor

                connection.close()

                raise ValueError(sys.exc_info()[1])



        else:

            raise ValueError("Database credentials not initialised : call set_connect function")




    def fetchOne(self,columns,tablename,condition=None,return_type=1):


        """
        Function to return the first row of the table and where the condition satisfies

        Input :

        columns : iterator of Strings (list or tuple )  : Column names  in the table you want to view
        table name: String : Table name in the DB
        condition : String : SQL  where clause condition
        return_type : Integer : 1 for Data Frame and 2 for JSON parsed Dictionary object

        Output : Parsed Json (List of Dictionaries) or DataFrame
        """



        if isinstance(return_type,int) and (return_type==1 or return_type == 2):
            pass
        else:
            raise  ValueError("return_type argument must be integer of value one or two")


        if self.connect_check == True :

            #processing the query

            query = fetchone_query(columns=columns,tablename=tablename,condition=condition)


            #connecting to Database
            try:

                connection = connect_oracle(username=self.__username, pwd=self.__pwd, sid=self.__sid, port=self.__port,
                                            host=self.__host)
                cursor = connection.cursor()

            except:

                raise ValueError(sys.exc_info()[1])


            try:

                result = pd.read_sql_query(con=connection, sql=query)


                if len(result.columns) != len(columns): #exception for * input in the iterator

                    pass

                else:
                    result.columns = columns


                connection.close()

                if return_type == 1:

                    return result

                else:

                    json.loads(result.to_json(orient='records'))[0]

            except:

                # closing the connection and cursor

                connection.close()

                raise ValueError(sys.exc_info()[1])

        else:

            raise ValueError("Database credentials not initialised : call set_connect function")




    def fetchMany(self,columns,tablename,rows= -1,condition=None,return_type = 1):
        """
        Function to fetch all the values from a given table with a given condition

        Input :

        columns : iterator of Strings (list or tuple )  : Column names  in the table you want to view
        table name: String : Table name in the DB
        condition : String : SQL  where clause condition
        rows : Integer: Number of rows to be fetched, Default = -1 : Fetch all
        return_type : Integer : 1 for Data Frame and 2 for JSON parsed Dictionary object


        Output: Data frame or Parsed Json (List of Dictionaries)
        """



        if isinstance(return_type,int) and (return_type ==1 or return_type == 2):
            pass
        else:
            raise  ValueError("type argument must be integer of value one or two")


        if self.connect_check == True:

            #processing the query


            query = fetchmany_query(columns=columns,tablename=tablename,rows=rows,condition=condition)

            # connecting to the DB

            try:

                connection = connect_oracle(username=self.__username, pwd=self.__pwd, sid=self.__sid, port=self.__port,
                                            host=self.__host)
                cursor = connection.cursor()

            except:

                raise ValueError(sys.exc_info()[1])


            try:

                result = pd.read_sql_query(con=connection,sql=query)


                if len(result.columns) != len(columns):  # exception for * input in the iterator

                    pass

                else:
                    result.columns = columns

                connection.close()

                if return_type ==  1:


                    return  result

                else:

                    return  json.loads(result.to_json(orient='records'))




            except:

                # closing the connection and cursor

                connection.close()

                raise ValueError(sys.exc_info()[1])


        else:

            raise ValueError("Database credentials not initialised : call set_connect function")




    def insert(self,tablename,objects):
        """
        Function to insert records in the table given the objects and the tablename

        Input :

        tablename : String : Table name of the Database

        objects : List of Dictionaries or dictionary : Format : {sql table column Name :Value}

        Output:

        Boolean :  True in case of successfully objects else Raise Value error
        """

        

        if self.connect_check == True:



            if isinstance(objects,dict) or (isinstance(objects,list) and len(objects)==1):

                #insert one logic

                if isinstance(objects,dict):
                    pass
                else:
                    objects = objects[0] #getting the dictionary from the list

                query = insertone_query(tablename=tablename,objects=objects)

                # connecting to the DB
                try:

                    connection = connect_oracle(username=self.__username, pwd=self.__pwd, sid=self.__sid, port=self.__port,
                                                host=self.__host)
                    cursor = connection.cursor()

                except:

                    raise ValueError(sys.exc_info()[1])

                try:

                    cursor.execute(query)

                    connection.commit()
                    connection.close()

                    return  True

                except:

                    # closing the connection and cursor
                    connection.close()

                    raise ValueError(sys.exc_info()[1])


            else:

                query = insertmany_query(tablename=tablename,objects=objects)

                # connecting to the DB
                try:

                    connection = connect_oracle(username=self.__username, pwd=self.__pwd, sid=self.__sid, port=self.__port,
                                                host=self.__host)
                    cursor = connection.cursor()

                except:

                    raise ValueError(sys.exc_info()[1])

                try:

                    cursor.bindarraysize = 1000
                    cursor.arraysize = 1000

                    cursor.executemany(query, objects)

                    connection.commit()
                    connection.close()

                    return True

                except:

                    # closing the connection and cursor

                    connection.close()

                    raise ValueError(sys.exc_info()[1])

        else:

            raise ValueError("Database credentials not initialised : call set_connect function")




    def update(self,tablename,updations,condition=None):
        """
        Input :

        table name: String : Tablename of the DB
        updations: Object : Dictionary : Format : {column:value}
        condition: String : Where condition to filter in the Table

        Output:

        returns: True if successful updation is done successfully

        """

        #query

        query = update_query(tablename=tablename,objects=updations,condition=condition)


        # connecting to the DB

        try:

             connection = connect_oracle(username=self.__username, pwd=self.__pwd, sid=self.__sid, port=self.__port,
                                            host=self.__host)
             cursor = connection.cursor()

        except:

            raise ValueError(sys.exc_info()[1])


        try:

            cursor.execute(query)

            connection.commit()
            connection.close()

            return True

        except:

              # closing the connection and cursor

            connection.close()

            raise ValueError(sys.exc_info()[1])



