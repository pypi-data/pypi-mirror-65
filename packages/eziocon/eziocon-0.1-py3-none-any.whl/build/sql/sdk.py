from  .connection import connect_
import sys
import pandas as pd
import json


class Mysql :

    def __int__(self):
        """
        Initialising  the variables for use
        """
        self.username = None
        self.pwd = None
        self.host = None
        self.database = None
        self.port = None
        self.format =  None
        self.connect_check = False
        self.format_name = None



    def set_connect(self,username, password, hostname, database, port, format):
        """
        Input :
        username : String : Database Username
        hostname : String : Database Hostname
        database : String : Database Name
        port : Integer : Database port
        format : Integer: 1 for Dataframe , 2 for Parsed Json (List of Dictionaries)
        """

        self.username = username
        self.pwd = password
        self.host = hostname
        self.database = database
        self.port= port
        self.format = format



        if isinstance(format,int):

            if format ==1 or format == 2 :

                pass
            else:

                raise ValueError("Format must be either 1 (DataFrame) or 2 (Json) ")

        else:

            raise ValueError("Format must be  a integer")

        #connecting to the database to check the connection


        connection = connect_(username=self.username,pwd = self.pwd,database =self.database,port=self.port,host=self.host)

        self.connect_check = True

        connection.close()

        #setting the format name

        self.format_name =  {1 : "DataFrame", 2:"JSON"}[self.format]




    def count(self,tablename, condition=None):

        """
        Function to get the tablename and sql condition to return the count of rows which satisfies the condition in the tablename

        Input :
        tablename: String : Table name in DB
        where: String : where condition to filter the table

        Output:
        Count : Integer : Count of the rows for the given condition and  tablename
        """


        if isinstance(tablename,str):
            pass
        else:
            raise ValueError("Tablename should be a String")

        if condition ==None or isinstance(condition,str):
            pass
        else:
            raise ValueError("Condition can only be either None or String")



        if self.connect_check :

            try:
                connection = connect_(username=self.username,pwd = self.pwd,database =self.database,port=self.port,host=self.host)
                cursor = connection.cursor()

            except:

                raise ValueError(str(sys.exc_info()[1]))

            if condition == None:

                query = "select count(*) from " + tablename

            else:
                # building the query
                query = "select count(*) from " + tablename + " where " + condition

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






    def fetch_one(self,columns, tablename, condition=None):

        """
        Function to return the first row of the table and where the condition satisfies

        Input :
        columns : Tuple of Strings : Column names  in the table you want to view
        tablename: String : Tablename in the DB
        condition: String : Where condition to filter in the Table

        Output : Parsed Json (List of Dictionaries) or DataFrame
        """

        if isinstance(columns,tuple):
            pass
        else:
            raise  ValueError("Columns argument must be tuple of String s")

        if isinstance(tablename, str):
            pass
        else:
            raise ValueError("Tablename should be a String")

        if condition == None or isinstance(condition, str):
            pass
        else:
            raise ValueError("Condition can only be either None or String")



        #parsing columns into a string for quering
        if (len(columns) > 1):
            cols = ""
            for i in columns:
                cols = cols + i + ","

            cols = cols[:len(cols) - 1]
        else:
            cols = str(columns)[1:len(columns) - 1]



        if self.connect_check :

            try:
                connection = connect_(username=self.username, pwd=self.pwd, database=self.database, port=self.port,
                                      host=self.host)
                cursor = connection.cursor()

            except:

                raise ValueError(str(sys.exc_info()[1]))


            if condition == None:

                query = "select " + cols + " from " + tablename

            else:

                query = "select " + cols + " from " + tablename + " where " + condition

            
            
            try:

                if self.format == 1:

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






    def fetch_many(self,columns, tablename, condition=None, rows=-1):
  
        """
        Function to fetch all the values from a given table with a given condition

        Input :

        columns : Tuple : Columns in the table you want to view
        tablename: String : Tablename in the DB
        condition: String : Where condition to filter in the Table
        rows : Integer: Number of rows to be fetched, Default = -1 : Fetch all


        Output: Data frame or Parsed Json (List of Dictionaries)
        """


        if isinstance(columns,tuple):
            pass
        else:
            raise  ValueError("Columns argument must be tuple of String s")


        # connecting to the DB

        if self.connect_check == True :

            try:
                connection = connect_(username=self.username, pwd=self.pwd, database=self.database, port=self.port,
                                      host=self.host)
                cursor = connection.cursor()

            except:

                raise ValueError(str(sys.exc_info()[1]))


            # converting tuples to string
            cols = ""
            for i in columns:
                cols = cols + i + ","

            cols = cols[:len(cols) - 1]

            # 2 different queries : with and without where clause

            if condition == None:

                if rows == -1:
                    # fetch all
                    query = "Select " + cols + " from " + tablename
                else:
                    # fetch given records
                    query = "Select " + cols + " from " + tablename + " LIMIT " + str(rows)


            else:

                if rows == -1:
                    # fetch all
                    query = "Select " + cols + " from " + tablename + " where " + condition
                else:
                    # fetch given records
                    query = "Select " + cols + " from " + tablename + " where " + condition + " LIMIT " + str(rows)

            try:

                # fetch N records

                if self.format == 1:

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






    def insert_one(self,tablename, objects):

        """
        Input :

        tablename: String : Tablename of the Database
        object: Dictionary : Format : {sql table column Name :Value}

        Output: Boolean : Last Row ID  in case of successfuly insertion else Raise Value error
        """



        if isinstance(objects,dict):
            pass
        else:
            raise  ValueError("Object argument must be Dictionary in format {column name : Value}")


        if self.connect_check == True:

            try:
                connection = connect_(username=self.username, pwd=self.pwd, database=self.database, port=self.port,
                                      host=self.host)
                cursor = connection.cursor()

            except:

                raise ValueError(str(sys.exc_info()[1]))

            # preparing the columns and values

            cols = ""
            for i in tuple(objects.keys()):
                cols += str(i) + ","
            cols = "(" + cols[:len(cols) - 1] + ")"

            if len(objects) == 1:
                if isinstance(list(objects.values())[0], str):
                    val = "('" + str(tuple(objects.values())[0]) + "')"
                else:
                    val = "(" + str(tuple(objects.values())[0]) + ")"
            else:
                val = str(tuple(objects.values()))

            query = "INSERT INTO " + tablename + cols + " values" + val

        # print(query)

            try:

                cursor.execute(query)
                connection.commit()
                connection.close()

                return int(cursor.lastrowid)

            except Exception as  e:

                # closing the connection and cursor

                connection.close()

                raise ValueError(str(sys.exc_info()[1]))

        else:

            raise ValueError("Database credentials not initialised : call set_connect function")




    def insert_all(self, tablename, objects, condition=None):

        """
        Input :

        table name: String : Table name of the DB
        objects : List of Dictionary : Format : {column:value}
        condition: String : Where condition to filter in the Table

        Output: Boolean : True if successful insertion else value Error
        """

        if isinstance(tablename,str):
            pass
        else:
            raise  ValueError("Tablename argument must be a String ")


        if isinstance(objects, list):
            pass
        else:
            raise ValueError("Object argument must be Dictionary in format {column name : Value}")

        # connecting to the DB

        if self.connect_check == True:

            try:
                connection = connect_(username=self.username, pwd=self.pwd, database=self.database, port=self.port,
                                      host=self.host)
                cursor = connection.cursor()

            except:

                raise ValueError(str(sys.exc_info()[1]))

            # preparing the columns and placeholders

            cols = objects[0].keys()
            data = []
            for i in objects:
                data.append(tuple(i.values()))

            # formating the reg string
            reg_string = ""
            for i in range(len(data[0])):
                reg_string += "%s, "
            reg_string = reg_string[:len(reg_string) - 2]



            #making the query

            if condition == None:
                query = "INSERT INTO " + tablename + " (%s) VALUES(%s)" % (",".join(cols), reg_string)
            else:
                query = "INSERT INTO " + tablename + " (%s) VALUES(%s)" % (
                    ",".join(cols), reg_string) + " where " + condition

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

            raise ValueError("Database credentials not initialised : call set connect function")




    def update(self,tablename, updations, condition=None):

        """
        Input :
        table name: String : table name of the DB
        updations: Object : Dictionary : Format : {column:value}
        condition: String : Where condition to filter in the Table

        Output: Boolean : True if successful else Value error
        """

        # connecting to the DB

        if isinstance(object, dict):
            pass
        else:
            raise ValueError("Object argument must be Dictionary in format {column name : Value}")



        if self.connect_check == True:

            try:
                connection = connect_(username=self.username, pwd=self.pwd, database=self.database, port=self.port,
                                      host=self.host)
                cursor = connection.cursor()

            except:

                raise ValueError(str(sys.exc_info()[1]))


            # processing columns
            cols = ""

            for i in updations.keys():
                substr = str(i) + " = " + str(updations[i]) + ","
                cols = cols + substr

            cols = cols[:len(cols) - 1]


            # query creation

            if condition == None:

                query = "Update " + tablename + " set " + cols

            else:
                query = "Update " + tablename + " set " + cols + " where " + condition

            try:
                cursor.executemany(query)
                connection.commit()
                connection.close()

                return True

            except Exception as e:

                # closing the connection and cursor
                connection.close()

                raise ValueError(str(sys.exc_info()[1]))

        else:

            raise ValueError("Database credentials not initialised : call set_connect function")
