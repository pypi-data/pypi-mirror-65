

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

    if isinstance(columns, tuple) or isinstance(columns, list) or isinstance(columns, set):
        pass
    else:
        raise ValueError("Columns argument must be tuple of String s")

    if isinstance(tablename, str):
        pass
    else:
        raise ValueError("Table name should be a String")

    if condition == None or isinstance(condition, str):
        pass
    else:
        raise ValueError("Condition can only be either None or String")

    # parsing columns into a string for quering
    if (len(columns) > 1):
        cols = ""
        for i in columns:
            cols = cols + i + ","

        cols = cols[:len(cols) - 1]
    else:
        cols = str(columns[0])

    #creating query

    if condition == None:

        query = "select " + cols + " from " + tablename

    else:

        query = "select " + cols + " from " + tablename + " where " + condition

    return   query



def fetchmany_query(columns,tablename,condition,rows=-1):
    """
    Function to process the query for fetch many process
    """

    if isinstance(columns, tuple) or isinstance(columns, list) or isinstance(columns, set):
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

    if isinstance(rows, int) and (rows > 1 or rows == -1):
        pass
    else:
        raise ValueError("rows can only be a integer and not less than 1")

        # generating columns

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


    return query




def insertone_query(tablename,objects):
    """
    Function to process the query for insert one  process
    """

    #validations
    if isinstance(tablename, str):
        pass
    else:
        raise ValueError("Tablename should be a String")



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

    return  query



def insertmany_query(tablename,objects):
    """
    Function to process the query for insert many  process
    """

    if isinstance(tablename, str):
        pass
    else:
        raise ValueError("Tablename should be a String")

    """
        Sanity check of bulk insert
    """

    # same length check
    len_objects = []
    for val in map(len, objects):
        len_objects.append(val)

    if len(set(len_objects)) != 1:
        raise ValueError("Objects are off different length")

    # same columns check

    columns = set(objects[0].keys())
    for val in objects:
        if columns != set(val.keys()):
            raise ValueError("The number of columns that has to be updated must be same across all the objects")




    #parsing column and data for the insertion

    cols = objects[0].keys()

    data = []
    for i in objects:
        data.append(tuple(i.values()))

    # formating the reg string
    reg_string = ""
    for i in range(len(data[0])):
        reg_string += "%s, "
    reg_string = reg_string[:len(reg_string) - 2]

    # making the query


    query = "INSERT INTO " + tablename + " (%s) VALUES(%s)" % (",".join(cols), reg_string)

    return query,data




def update_query(tablename,objects,condition):
    """
    Function to process the query for update process
    """

    if isinstance(tablename, str):
        pass
    else:
        raise ValueError("Tablename should be a String")

    if condition == None or isinstance(condition, str):
        pass
    else:
        raise ValueError("Condition can only be either None or String")

    if isinstance(objects, dict):
        pass
    else:
        raise ValueError("Object argument must be Dictionary in format {column name : Value}")


    # processing columns
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


    return query
