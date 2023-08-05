from .connection import connect_oracle
import cx_Oracle
import sys
import json
import pandas as pd



class oracle:


    def __init__(self):
        """
        Initialising  the variables for use
        """

        self.username = None
        self.pwd = None
        self.host = None
        self.port = None
        self.sid = None
        self.format = None
        self.connect_check = False
        self.format_name = None


    def set_connect(self,username,password,hostname,port,sid,format):
        """
        Input :
        username : String : Database Username
        hostname : String : Database Hostname
        password : String : Database password
        sid : String : Database Service ID : Schema Name
        port : Integer : Database port
        format : Integer: 1 for Dataframe , 2 for Parsed Json (List of Dictionaries)
        """
        #setting the instance variables using this setter function
        self.username = username
        self.pwd = password
        self.host = hostname
        self.sid= sid
        self.port = port
        self.format = format

        if isinstance(format, int):

            if format == 1 or format == 2:

                pass
            else:

                raise ValueError("Format must be either 1 (DataFrame) or 2 (Json) ")

        else:

            raise ValueError("Format must be  a integer")

        # connecting to the database to check the connection

        connection = connect_oracle(username=self.username, pwd=self.pwd, sid = self.sid, port=self.port,
                              host=self.host)

        self.connect_check = True

        connection.close()

        # setting the format name

        self.format_name = {1: "DataFrame", 2: "JSON"}[self.format]



    def count(self,tablename,condition = None):

        """
        Function to get the tablename and sql condition to return the count of rows which satisfies the condition in the tablename

        Input :
        tablename: String : Table name in DB
        where: String : where condition to filter the table

        Output:
        Count : Integer : Count of the rows for the given condition and  tablename
        """

        if self.connect_check == True:
            if isinstance(tablename, str):
                pass
            else:
                raise Exception("Tablename should be a String")

            if condition == None or isinstance(condition, str):
                pass
            else:
                raise Exception("Condition can only be either None or String")

            # connecting to the DB
            try:

                connection = connect_oracle(username=self.username, pwd=self.pwd, sid=self.sid, port=self.port,
                                            host=self.host)
                cursor = connection.cursor()

            except:

                raise Exception(sys.exc_info()[1])

            if condition == None:

                query = "select count(*) from " + tablename

            else:
                # building the query
                query = "select count(*) from " + tablename + " where " + condition

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




    def fetch_one(self,columns,tablename,condition=None):
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



        if self.connect_check == True :

            if (len(columns) > 1):
                cols = ""
                for i in columns:
                    cols = cols + i + ","

                cols = cols[:len(cols) - 1]
            else:

                cols = str(columns)[1:len(columns) - 1]

            try:

                connection = connect_oracle(username=self.username, pwd=self.pwd, sid=self.sid, port=self.port,
                                            host=self.host)
                cursor = connection.cursor()

            except:

                raise ValueError(sys.exc_info()[1])

            if condition == None:

                query = "select " + cols + " from " + tablename + " fetch first 1 rows only"

            else:

                query = "select " + cols + " from " + tablename + " where " + condition + " fetch first 1 rows only"

            try:

                result = 0
                for row in cursor.execute(query):
                    result = i

                connection.close()

                return result

            except:

                # closing the connection and cursor

                connection.close()

                raise ValueError(sys.exc_info()[1])

        else:

            raise ValueError("Database credentials not initialised : call set_connect function")

    def fetch_many(self,columns,tablename,rows= -1,condition=None):
        """
        Function to fetch all the values from a given table with a given condition

        Input :

        columns : Tuple : Columns in the table you want to view
        tablename: String : Tablename in the DB
        condition: String : Where condition to filter in the Table
        rows : Integer: Number of rows to be fetched, Default = -1 : Fetch all

        Output: Data frame or Parsed Json (List of Dictionaries)
        """

        if isinstance(tablename, str):
            pass
        else:
            raise Exception("Tablename should be a String")

        if condition == None or isinstance(condition, str):
            pass
        else:
            raise Exception("Condition can only be either None or String")
        
        


        if self.connect_check == True:

            # connecting to the DB

            try:

                connection = connect_oracle(username=self.username, pwd=self.pwd, sid=self.sid, port=self.port,
                                            host=self.host)
                cursor = connection.cursor()

            except:

                raise Exception(sys.exc_info()[1])

            # converting tuples to string
            cols = ""
            for i in columns:
                cols = cols + i + ","

            cols = cols[:len(cols) - 1]

            # 2 different queries : with and without where clause

            if condition == None:

                if rows == -1:
                    query = "Select " + cols + " from " + tablename
                else:
                    query = "Select " + cols + " from " + tablename + " fetch first {} rows only".format(rows)


            else:
                if rows == -1:
                    query = "Select " + cols + " from " + tablename + " where " + condition
                else:
                    query = "Select " + cols + " from " + tablename + " where " + condition + " fetch first {} rows only".format(
                        rows)

            try:

                final = []
                cursor.arraysize = 1000  # default
                results = cursor.execute(query)

                for row in results:
                    final.append(row)

                connection.close()

                return final

            except:

                # closing the connection and cursor

                connection.close()

                raise ValueError(sys.exc_info()[1])


        else:

            raise ValueError("Database credentials not initialised : call set_connect function")




    def insert_one(self,tablename,objects):
        """
        Input :

        tablename: String : Tablename of the Database
        object: Dictionary : Format : {sql table column Name :Value}

        Output: Boolean : Last Row ID  in case of successfuly objects else Raise Value error
        """

        if isinstance(tablename, str):
            pass
        else:
            raise Exception("Tablename should be a String")

        if isinstance(objects, dict):
            pass
        else:
            raise Exception("Object can only be Dictionary")
        

        if self.connect_check == True:

            # connecting to the DB
            try:

                connection = connect_oracle(username=self.username, pwd=self.pwd, sid=self.sid, port=self.port,
                                            host=self.host)
                cursor = connection.cursor()

            except:

                raise ValueError(sys.exc_info()[1])

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


            # making the query
            query = "INSERT INTO " + tablename + cols + " values" + val + " returning id into :1"


            try:

                new_id = cursor.var(cx_Oracle.NUMBER)
                cursor.execute(query, [new_id])

                connection.commit()
                connection.close()

                return int(new_id.getvalue()[0])

            except:

                # closing the connection and cursor
                connection.close()

                raise ValueError(sys.exc_info()[1])

        else:

            raise ValueError("Database credentials not initialised : call set_connect function")




    def update(self,tablename,updations,condition=None):
          """

           tablename: String : Tablename of the DB
           updations: Object : Dictionary : Format : {column:value}
           condition: String : Where condition to filter in the Table
           returns: True if successful updation is done successfully

          """

          if isinstance(tablename, str):
              pass
          else:
              raise Exception("Tablename should be a String")

          if condition == None or isinstance(condition, str):
              pass
          else:
              raise Exception("Condition can only be either None or String")

          if isinstance(updations, dict):
              pass
          else:
              raise Exception("Object can only be Dictionary")

          # connecting to the DB

          try:

              connection = connect_oracle(username=self.username, pwd=self.pwd, sid=self.sid, port=self.port,
                                            host=self.host)
              cursor = connection.cursor()

          except :

              raise Exception(sys.exc_info()[1])

            # preparing the columns and values

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

              cursor.execute(query)

              connection.commit()
              connection.close()

              return True

          except Exception as  e:

              # closing the connection and cursor

              connection.close()

              raise Exception(sys.exc_info()[1])



    def insert_all(self,tablename,objects,condition=None):
        """
        Input :

        table name: String : Table name of the DB
        objects : List of Dictionary : Format : {column:value}
        condition: String : Where condition to filter in the Table

        Output: Boolean : True if successful insertion else value Error
        """



        if isinstance(objects, list):
            pass
        else:
            raise ValueError("Object argument must be a list of Dictionaries in format {column name : Value}")

        # connecting to the DB

        try:

            connection = connect_oracle(username=self.username, pwd=self.pwd, sid=self.sid, port=self.port,
                                            host=self.host)
            cursor = connection.cursor()

        except :

            raise Exception(sys.exc_info()[1])

        # preparing the columns and placeholders

        val= objects[0]

        #columns

        cols = ""
        for i in tuple(val.keys()):
            cols += str(i) + ","
        cols = "(" + cols[:len(cols) - 1] + ")"



        #placeholders
        placeholders = ""
        for i in tuple(val.keys()):
            placeholders += ":" + str(i) + ","

        placeholders = "(" + placeholders[:len(placeholders) - 1] + ")"


        if condition == None:
            query = "INSERT INTO "+ tablename+ " " + cols + " values " + placeholders
        else:
            query = "INSERT INTO " + tablename + " " + cols + " values " + placeholders + " where " + condition

        try:

            cursor.bindarraysize = 1000
            cursor.arraysize = 1000

            cursor.executemany(query,objects)


            connection.commit()
            connection.close()

            return True

        except:

            # closing the connection and cursor

            connection.close()

            raise ValueError(sys.exc_info()[1])


