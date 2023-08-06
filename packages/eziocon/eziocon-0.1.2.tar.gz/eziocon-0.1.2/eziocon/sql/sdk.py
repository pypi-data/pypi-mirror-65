from  .connection import connect_
import sys
import pandas as pd
from .query_processor import count_query,update_query, fetchone_query, fetchmany_query , insertmany_query, insertone_query
import json
class Mysql :

    def __int__(self):
        """
        Initialising  the variables for use
        """
        self.__username = None
        self.__pwd = None
        self.__host = None
        self.__database = None
        self.__port = None

        self.connect_check = False



    def setConnect(self,username, password, hostname, database, port):
        """
        Function to set the connection and database credentials and testing connection to database
        Input :
        username : String : Database Username
        hostname : String : Database Hostname
        database : String : Database Name
        port : String : Database port
        """

        self.__username = username
        self.__pwd = password
        self.__host = hostname
        self.__database = database
        self.__port= port

        # connecting to the database to check the connection
        connection = connect_(username=self.__username,pwd = self.__pwd,database =self.__database,port=self.__port,host=self.__host)

        self.connect_check = True

        connection.close()




    def count(self,tablename, condition=None):

        """
        Function  return the count of rows given the condition and the tablename

        Input :
        table name: String : Table name in DB
        where: String : where condition to filter the table

        Output:
        Count : Integer : Count of the rows for the given condition and  tablename
        """

        #processing query

        query = count_query(tablename=tablename,condition=condition)

        if self.connect_check :

            try:
                connection = connect_(username=self.__username,pwd = self.__pwd,database =self.__database,port=self.__port,host=self.__host)
                cursor = connection.cursor()

            except:

                raise ValueError(str(sys.exc_info()[1]))


            try:
                cursor.execute(query)
                count = cursor.fetchone()[0]
                connection.close()

                return count

            except Exception as  e:

                # closing the connection and cursor

                connection.close()

                raise ValueError(str(sys.exc_info()[1]))
        else:

            raise ValueError("Database credentials not initialised : call set_connect function")






    def fetchOne(self,columns, tablename, condition=None,return_type = 1):

        """
        Function to return the first row of the table and where the condition satisfies

        Input :
        columns : Iterator of Strings list or tuple or set of Strings (columns names) in the table you want to view
        table name: String : Table name in the DB
        condition: String : Where condition to filter in the Table
        return_type : Integer: 1 for DataFrame and 2 For JSON parsed List of Dictionaries

        Output : Parsed Json (List of Dictionaries) or DataFrame
        """




        if isinstance(return_type,int):

            if return_type ==1 or return_type == 2 :

                pass
            else:

                raise ValueError("return type must be either 1 (DataFrame) or 2 (Json) ")

        else:

            raise ValueError("return type  must be  a integer")


        #procesing query

        query = fetchone_query(columns=columns,tablename=tablename,condition=condition)


        if self.connect_check :

            try:
                connection = connect_(username=self.__username, pwd=self.__pwd, database=self.__database, port=self.__port,
                                      host=self.__host)
                cursor = connection.cursor()

            except:

                raise ValueError(str(sys.exc_info()[1]))
            
            
            try:

                if return_type == 1:

                     result =  pd.read_sql(query,connection) #returning Dataframe

                     connection.close()

                     return result

                else:

                    result =  json.loads(pd.read_sql(query, connection).to_json(orient='records'))[0] #json

                    connection.close()

                    return result

            except:

                connection.close()

                raise  ValueError(str(sys.exc_info()[1]))

        else:

            raise ValueError("Database credentials not initialised : call set_connect function")






    def fetchMany(self,columns, tablename, condition=None, rows=-1,return_type = 1):
  
        """
        Function to fetch all the values from a given table with a given condition

        Input :

        columns : Tuple : Columns in the table you want to view
        table name: String : Tablename in the DB
        condition: String : Where condition to filter in the Table
        rows : Integer: Number of rows to be fetched, Default = -1 : Fetch all
        return_type : Integer: 1 for DataFrame and 2 For JSON parsed List of Dictionaries



        Output: Data frame or Parsed Json (List of Dictionaries)
        """

        if isinstance(return_type,int):

            if return_type ==1 or return_type == 2 :

                pass
            else:

                raise ValueError("return type must be either 1 (DataFrame) or 2 (Json) ")

        else:

            raise ValueError("return type  must be  a integer")

        #processing query

        query = fetchmany_query(tablename=tablename, columns=columns, condition=condition, rows=rows)

        # connecting to the DB

        if self.connect_check == True :

            try:
                connection = connect_(username=self.__username, pwd=self.__pwd, database=self.__database, port=self.__port,
                                      host=self.__host)
                cursor = connection.cursor()

            except:

                raise ValueError(str(sys.exc_info()[1]))


            try:

                # fetch N records

                if return_type == 1:

                     result =  pd.read_sql(query,connection) #returning Dataframe

                     connection.close()

                     return result

                else:

                    result = json.loads(pd.read_sql(query, connection).to_json(orient='records')) #json

                    connection.close()

                    return result

            except Exception as  e:

                # closing the connection and cursor

                connection.close()

                raise ValueError(str(sys.exc_info()[1]))

        else:

            raise ValueError("Database credentials not initialised : call set connect function")




    def insert(self,tablename,objects):
        """
        Function to insert records into the given table

        Input :

        tablename : String : Tablename of the Database

        objects : List of Dictionaries or dictionary : Format : {sql table column Name :Value}

        Output: Boolean :  True in case of successfully objects else Raise Value error
        """

        if self.connect_check == True:

            if isinstance(objects,dict) or (isinstance(objects,list) and len(objects)==1): #either it is a single dicitionary or list with only one dictionary object

                #insert one logic

                if isinstance(objects,dict):
                    pass
                else:
                    objects = objects[0] #getting the dictionary from the list

                #processing query

                query = insertone_query(tablename=tablename,objects=objects)


                try:
                    connection = connect_(username=self.__username, pwd=self.__pwd, database=self.__database, port=self.__port,
                                          host=self.__host)
                    cursor = connection.cursor()

                except:

                    raise ValueError(str(sys.exc_info()[1]))

                try:

                    cursor.execute(query)
                    connection.commit()
                    connection.close()

                    return True

                except Exception as  e:

                    # closing the connection and cursor

                    connection.close()

                    raise ValueError(str(sys.exc_info()[1]))

            else:
                #bulk insert logic

                #processing query
                query,data = insertmany_query(tablename=tablename, objects=objects)


                try:
                    connection = connect_(username=self.__username, pwd=self.__pwd, database=self.__database, port=self.__port,
                                          host=self.__host)
                    cursor = connection.cursor()

                except:

                    raise ValueError(str(sys.exc_info()[1]))

                try:
                    cursor.executemany(query, data)
                    connection.commit()
                    connection.close()

                    return True

                except Exception as  e:

                    # closing the connection and cursor

                    connection.close()

                    raise ValueError(str(sys.exc_info()[1]))

        else:

            raise ValueError("Database credentials not initialised : call set_connect function")




    def update(self,tablename, updations, condition=None):

        """
        Input :

        tablename: String : Tablename of the DB
        updations: Object : Dictionary : Format : {column:value}
        condition: String : Where condition to filter in the Table

        Output:

        returns: True if successful updation is done successfully

        """

        query = update_query(tablename=tablename,objects=updations,condition=condition)


        if self.connect_check == True:

            try:
                connection = connect_(username=self.__username, pwd=self.__pwd, database=self.__database, port=self.__port,
                                      host=self.__host)
                cursor = connection.cursor()

            except:

                raise ValueError(str(sys.exc_info()[1]))



            try:
                cursor.execute(query)
                connection.commit()
                connection.close()

                return True

            except Exception as e:

                # closing the connection and cursor
                connection.close()

                raise ValueError(str(sys.exc_info()[1]))

        else:

            raise ValueError("Database credentials not initialised : call set_connect function ")
