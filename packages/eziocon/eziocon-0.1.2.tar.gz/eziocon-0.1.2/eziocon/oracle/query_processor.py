



def count_query(tablename,condition):
    """
    Function to process query for count process
    """

    if isinstance(tablename, str):
        pass
    else:
        raise ValueError("Tablename should be a String")

    if condition == None or isinstance(condition, str):
        pass
    else:
        raise ValueError("Condition can only be either None or String")

    if condition == None:

        query = "select count(*) from " + tablename

    else:
        # building the query
        query = "select count(*) from " + tablename + " where " + condition


    return query





def fetchone_query(columns,tablename,condition):
    """"
    Function to process the query for fetch one process
    """

    if isinstance(columns, tuple) or isinstance(columns, list) :
        pass
    else:
        raise ValueError("Columns argument must be iterator of Strings")

    if isinstance(columns[0], str):
        pass
    else:
        raise ValueError("Column names must be a String")

    if isinstance(tablename, str):
        pass
    else:
        raise ValueError("Tablename should be a String")

    if condition == None or isinstance(condition, str):
        pass
    else:
        raise ValueError("Condition can only be either None or String")



    if (len(columns) > 1):
        cols = ""
        for i in columns:
            cols = cols + i + ","

        cols = cols[:len(cols) - 1]
    else:

        cols = str(columns[0])  # breakage -- check



    if condition == None:

        query = "select " + cols + " from " + tablename + " fetch first 1 rows only"

    else:

        query = "select " + cols + " from " + tablename + " where " + condition + " fetch first 1 rows only"



    return query


def fetchmany_query(columns,tablename,condition,rows=-1):
    """
    Function to process the query for fetch many process
    """

    if isinstance(columns, tuple) or isinstance(columns, list) :
        pass
    else:
        raise ValueError("Columns argument must be iterator of Strings")

    if isinstance(columns[0],str):
        pass
    else:
        raise ValueError("Column names must be a String")

    if isinstance(tablename, str):
        pass
    else:
        raise ValueError("Tablename should be a String")

    if condition == None or isinstance(condition, str):
        pass
    else:
        raise ValueError("Condition can only be either None or String")
    
    if isinstance(rows,int) and (rows > 1 or rows == -1):
        pass
    else:
        raise ValueError("rows can only be a integer and not less than 1")


    #generating columns

    if (len(columns) > 1):
        cols = ""
        for i in columns:
            cols = cols + i + ","

        cols = cols[:len(cols) - 1]
    else:

        cols = str(columns[0])  # breakage -- check

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


    return query



def insertone_query(tablename,objects):
    """
    Function to process insert one query
    """
    # validations
    if isinstance(tablename, str):
        pass
    else:
        raise ValueError("Table name argument must be a string")

    if isinstance(objects,dict):
        pass
    else:
        raise ValueError(" Objects argument must be a Dictionary")




    value = objects

    # preparing the columns

    cols = ""
    for i in tuple(value.keys()):
        cols += str(i) + ","
    cols = "(" + cols[:len(cols) - 1] + ")"

    # preparing the values

    if len(value) == 1:  # if the length of dictionary is 1
        if isinstance(list(value.values())[0], str):
            val = "('" + str(tuple(value.values())[
                                 0]) + "')"  # if the length is one and  the value is a string then have to prefix and suffix single quote for SQL query
        else:
            val = "(" + str(tuple(value.values())[0]) + ")"  # else just wrap with brackets
    else:
        val = str(tuple(value.values()))

    # making the query



    query = "INSERT INTO " + tablename + cols + " values" + val


    return query




def insertmany_query(tablename,objects):
    """
    Function to process the query for insert many  process
    """

    #validations
    if isinstance(tablename,str):
        pass
    else:
        raise ValueError("Table name argument must be a string")

    if isinstance(objects,list):
        pass
    else:
        raise ValueError(" objects argument must be list")

    if isinstance(objects[0], dict):
        pass
    else:
        raise ValueError("A value in objects argument must be a dictionary")





    """
    Sanity check of bulk insert
    """

    #same length check
    len_objects = []
    for val in map(len, objects):
        len_objects.append(val)

    if len(set(len_objects)) != 1:
        raise ValueError("Objects are off different length")


    #same columns check

    columns = set(objects[0].keys())
    for val in objects:
        if columns != set(val.keys()):
            raise ValueError("The number of columns that has to be updated must be same across all the objects")




    # preparing the columns and placeholders

    val = objects[0]

    # columns

    cols = ""
    for i in tuple(val.keys()):
        cols += str(i) + ","
    cols = "(" + cols[:len(cols) - 1] + ")"

    # placeholders
    placeholders = ""
    for i in tuple(val.keys()):
        placeholders += ":" + str(i) + ","

    placeholders = "(" + placeholders[:len(placeholders) - 1] + ")"


    query = "INSERT INTO " + tablename + " " + cols + " values " + placeholders


    return query





def update_query(tablename,objects,condition):
    """
    Function to process the query for update process
    """

    if isinstance(tablename, str):
        pass
    else:
        raise ValueError("Table name should be a String")

    if condition == None or isinstance(condition, str):
        pass
    else:
        raise ValueError("Condition can only be either None or String")

    if isinstance(objects, dict):
        pass
    else:
        raise ValueError("Object can only be Dictionary")

        # preparing the columns and values




    cols = ""

    for i in objects.keys():
        if isinstance(objects[i],str): #prefixing and suffixing ' for string values
            substr = str(i) + " = '" + str(objects[i]) + "',"
        else:
            substr = str(i) + " = " + str(objects[i]) + ","
        cols = cols + substr

    cols = cols[:len(cols) - 1]

    # query creation

    if condition == None:

        query = "Update " + tablename + " set " + cols

    else:
        query = "Update " + tablename + " set " + cols + " where " + condition


    return  query


