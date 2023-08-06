# Yutils
>A Python utility package written by Yuval Arbel

## module  base
>yutils.base

## module  conn
>yutils.conn

## module  exceptions
>yutils.exceptions

## module  ml
>yutils.ml

## module  queries
>yutils.queries

## module  tools
>yutils.tools

## function  match_arabic_nls_lang
>yutils.match_arabic_nls_lang

### module  attribute_dict
>yutils.base.attribute_dict

### module  generic_object
>yutils.base.generic_object

### module  input_checker
>yutils.base.input_checker

### module  list_container
>yutils.base.list_container

### module  pretty_printer
>yutils.base.pretty_printer

### module  updating_dict
>yutils.base.updating_dict

#### object  AttributeDict
>yutils.base.attribute_dict.AttributeDict



#### object  GenericObject
>yutils.base.generic_object.GenericObject

    A generic object you can easily use for your scripts, with a pprint and a str/repr for easy printing
    

        :param object_name: The name for your object!
        :type object_name: str
        
#### function  dict_to_generic_object
>yutils.base.generic_object.dict_to_generic_object

    Converts a dictionary (recursively) to a GenericObject, with keys as attributes.

    :param dictionary: dictionary to convert (key-values will be converted to attribute-values)
    :type dictionary: dict
    :param object_name: a name for your new object's type
    :type object_name: str
    :return: GenericObject object
    


#### object  InputChecker
>yutils.base.input_checker.InputChecker


        Base object for making a Python object more static-typed.
        It is useful for checking __init__ argument inputs (type and content).

        Type check is defined by _INPUT_TYPES class constant. (see yutils.tools.check_object_type for usage)
        Option check is defined by _INPUT_OPTIONS class constant.

        This also:
            - creates self._inputs as the inputs dict given, as an AttributeDict.
            - adds each input in inputs as an attribute to your object.

        :param inputs: your __init__ inputs, can be anything you wish to check

        :raises: yutils.exceptions.WrongDatatype if any input is not of the specified type, defined by _INPUT_TYPES
                 yutils.exceptions.InputError if any input is not one of the options, defined by _INPUT_OPTIONS
        


#### object  ListContainer
>yutils.base.list_container.ListContainer

    An object that wraps a list, allowing you to use your object as a list and configure it as you wish.
    

        :param _list: the original list you wish to keep in the backbone of your object
        :type _list: list
        :param _objects_type: a plural name for your objects in your ListContainer! This is for printing your object.
                              For Example:
                              >>> class Students(ListContainer):
                              >>>     def __init__(self):
                              >>>         super(Students, self).__init__([], 'students')
        :type _objects_type: str
        


#### object  PrintableObject
>yutils.base.pretty_printer.PrintableObject

    An object you can derive from, that has a pprint method - printing all set attributes
    


#### object  DictValueList
>yutils.base.updating_dict.DictValueList

Initialize self.  See help(type(self)) for accurate signature.
#### object  UpdatingDict
>yutils.base.updating_dict.UpdatingDict

Initialize self.  See help(type(self)) for accurate signature.




### module  sql_connection_details
>yutils.conn.sql_connection_details

#### object  ConnectionDetails
>yutils.conn.sql_connection_details.ConnectionDetails

Initialize self.  See help(type(self)) for accurate signature.
#### object  ElasticConnectionDetails
>yutils.conn.sql_connection_details.ElasticConnectionDetails

Initialize self.  See help(type(self)) for accurate signature.
#### object  MSSQLConnectionDetails
>yutils.conn.sql_connection_details.MSSQLConnectionDetails

Initialize self.  See help(type(self)) for accurate signature.
#### object  MySQLConnectionDetails
>yutils.conn.sql_connection_details.MySQLConnectionDetails

Initialize self.  See help(type(self)) for accurate signature.
#### object  OracleConnectionDetails
>yutils.conn.sql_connection_details.OracleConnectionDetails

Initialize self.  See help(type(self)) for accurate signature.




### module  exceptions
>yutils.exceptions.exceptions

#### object  CodeMistake
>yutils.exceptions.exceptions.CodeMistake

    Gets raised to find mistakes when writing code
    

        :param mistake_string: an error message explaining why this was raised
        :type mistake_string: str
        
#### object  InputError
>yutils.exceptions.exceptions.InputError

    Gets raised when the input wasn't as expected (e.g. isn't a valid option)
    

        :param error_string: an error message explaining the InputError
        :type error_string: str
        
#### object  MissingAttribute
>yutils.exceptions.exceptions.MissingAttribute

    Gets raised when an attribute was expected in a certain class
    

        :param class_object: the object itself that is missing an attribute
        :type class_object: object
        :param attribute_name: the name of the attribute that is missing
        :type attribute_name: str
        
#### object  MissingInput
>yutils.exceptions.exceptions.MissingInput

    Gets raised when an input was expected in a certain class but not received
    

        :param class_object: the object itself that is missing an attribute
        :type class_object: object
        :param attribute_name: the name of the attribute that is missing
        :type attribute_name: str
        
#### object  UncaughtEndCase
>yutils.exceptions.exceptions.UncaughtEndCase

    Gets raised to catch unexpected cases in the future
    

        :param explanation: an optional string to explain the end case.
                            Default: 'An uncaught end case was found. Check it out!'
        :type explanation: str
        
#### object  UserCancellation
>yutils.exceptions.exceptions.UserCancellation

    Gets raised when a user chooses to cancel an operation, and you wish the program to abort.
    

        :param operation_name: (optional) the operation the user chose to cancel
        :type operation_name: (optional) str
        
#### object  WrongDatatype
>yutils.exceptions.exceptions.WrongDatatype

    Gets raised when something isn't the right datatype as was expected
    

        :param name: object name
        :type name: str
        :param expectation: expected type
        :type expectation: type or str
        :param reality: the object's actual type
        :type reality: type or str
        
#### object  WrongInputDatatype
>yutils.exceptions.exceptions.WrongInputDatatype

    Gets raised when an input argument isn't the right datatype as was expected
    

        :param name: object name
        :type name: str
        :param expectation: expected type
        :type expectation: type or str
        :param reality: the object's actual type
        :type reality: type or str
        
#### object  YutilsException
>yutils.exceptions.exceptions.YutilsException

Initialize self.  See help(type(self)) for accurate signature.




### module  classification
>yutils.ml.classification

### module  features
>yutils.ml.features

### module  linear_regression
>yutils.ml.linear_regression

### module  ml_base
>yutils.ml.ml_base

### module  regression
>yutils.ml.regression

#### object  LogisticRegression
>yutils.ml.classification.LogisticRegression

#### object  LogisticRegressionOptimizedClassifier
>yutils.ml.classification.LogisticRegressionOptimizedClassifier

#### object  MultiClassClassification
>yutils.ml.classification.MultiClassClassification



#### object  FeatureNormalizer
>yutils.ml.features.FeatureNormalizer


        Normalizes features for a ML object

        :param info: info to normalize, across column axis (normalizes each column by different normalization data)
        :type info:
        


#### object  LinearRegression
>yutils.ml.linear_regression.LinearRegression


        Not written yet...

        :param training_data:
        :param training_results:
        :param learning_rate:
        :param iterations:
        :param normalize_data:
        :param verbose:
        
#### object  NormalEquation
>yutils.ml.linear_regression.NormalEquation


        Not explained yet...

        :param training_data:
        :param training_results:
        :param assess_for_warning:
        :param verbose:
        


#### object  MLObject
>yutils.ml.ml_base.MLObject


        Base object for making a Python object more static-typed.
        It is useful for checking __init__ argument inputs (type and content).

        Type check is defined by _INPUT_TYPES class constant. (see yutils.tools.check_object_type for usage)
        Option check is defined by _INPUT_OPTIONS class constant.

        This also:
            - creates self._inputs as the inputs dict given, as an AttributeDict.
            - adds each input in inputs as an attribute to your object.

        :param inputs: your __init__ inputs, can be anything you wish to check

        :raises: yutils.exceptions.WrongDatatype if any input is not of the specified type, defined by _INPUT_TYPES
                 yutils.exceptions.InputError if any input is not one of the options, defined by _INPUT_OPTIONS
        
#### function  create_data_from_text_file
>yutils.ml.ml_base.create_data_from_text_file



#### object  Regression
>yutils.ml.regression.Regression





### module  db_connection
>yutils.queries.db_connection

### module  oracle_field_list_format
>yutils.queries.oracle_field_list_format

#### module  db_connection
>yutils.queries.db_connection.db_connection

#### module  fetchers
>yutils.queries.db_connection.fetchers

##### object  DBConnection
>yutils.queries.db_connection.db_connection.DBConnection

    Wraps a connection to a DB, for executing SQL queries, using given connection_details.
    

        :param connection_details: Details for connection to the wanted DB
        :type: connection_details: yutils.conn.sql_connection_details.ConnectionDetails
        :param verbose: If to print warnings or not
        :type verbose: bool
        


##### module  base_fetcher
>yutils.queries.db_connection.fetchers.base_fetcher

##### module  elastic
>yutils.queries.db_connection.fetchers.elastic

##### module  mssql
>yutils.queries.db_connection.fetchers.mssql

##### module  mysql
>yutils.queries.db_connection.fetchers.mysql

##### module  oracle
>yutils.queries.db_connection.fetchers.oracle

###### object  ElasticSearchFetcher
>yutils.queries.db_connection.fetchers.elastic.ElasticSearchFetcher



###### object  MSSQLFetcher
>yutils.queries.db_connection.fetchers.mssql.MSSQLFetcher



###### object  MySQLFetcher
>yutils.queries.db_connection.fetchers.mysql.MySQLFetcher



###### object  OracleFetcher
>yutils.queries.db_connection.fetchers.oracle.OracleFetcher







#### function  format_oracle_field_list
>yutils.queries.oracle_field_list_format.format_oracle_field_list

    Takes a list that can be more than 999 values long, and wraps them in SQL OR clauses.
    This is useful because Oracle can only accept lists 1000 values long.

    :param field_name: the name of the column you are querying
    :type field_name: str
    :param value_list: list of your values to format into the query
    :type value_list: list of str

    :return: formatted string containing your new WHERE clause
    :rtype: unicode
    




### module  case_conversions
>yutils.tools.case_conversions

### module  files
>yutils.tools.files

### module  list
>yutils.tools.list

### module  numpy_tools
>yutils.tools.numpy_tools

### module  pretty_print
>yutils.tools.pretty_print

### module  str
>yutils.tools.str

### module  xlsx_creator
>yutils.tools.xlsx_creator

### function  check_object_type
>yutils.tools.check_object_type

    This checks the types of an object using a certain syntax:
    Lets say we have an object_to_check and the types_to_validate.
    The object_to_check is the object

    :param object_to_check: the object you wish to check its type, and raise an exception should its type not be correct
    :type object_to_check: ....that's what we're here for....
    :param types_to_validate: defines the wanted types for the object to check:
    :type types_to_validate:
                type - checks that object_to_check is of that type
                        Example: float will make sure object_to_check is a float
                list of types - checks that object_to_check is one of the types in the list
                        Example: [int, float] will make sure object_to_check is either an int or a float
                tuple of types - checks hierarchically:
                                    checks that object_to_check is of the type of the first item,
                                    then checks that each item in object_to_check is of the type of the second item,
                                    etc.
                                 Remember, all types in the tuple except the last must support indexing.
                        Example: (list, str) will make sure object_to_check is a list of strings
                                 (tuple, [int, float]) will make sure object_to_check is a tuple of either ints or floats
                dict - checks that object_to_check is an object. It's type is defined by key 'type',
                       with other keys to be checked as the object's attributes.
                        Example: {'type': Person, 'age': int} will make sure object_to_check is a Person object,
                                 with an 'age' attribute that is an int.
                All values can have as many recursive dimensions as wanted.
    :param input_name: Do not use, this is for recursive inner use.

    More examples
    Lets say we create:

    integer = 13
    unicode_str = u'foo'
    int_list = list(range(10))
    input_object = MyObject()
    input_object.num = 3
    input_object.lis = [1, 'bar']
    input_object.3dlist = [[(1, 2, 3), (1, 1, 1)], [('a', 'b', 'c'), [7, 8, 9]]]

    We can send:
    check_object_type(integer, int)
    check_object_type(unicode_str, unicode)
    check_object_type(int_list, (list, int))
    check_object_type(input_object, {'type': MyObject,
                                     'num': int,
                                     'lis': (list, [int, str]),
                                     '3dlist': (list, list, [tuple, list], [int, str, unicode])
                                     })

    :raises:
             Because of invalid inputs:
                yutils.exceptions.CodeMistake - When no 'type' key is found (for when types_to_validate is a dict)
                yutils.exceptions.WrongDatatype - When no type type is found when isinstance-ing an object's type
             Exceptions raised by check:
                yutils.exceptions.WrongInputDatatype - When the type is not correct during validation
                yutils.exceptions.MissingInput - When an attribute is missing (for when types_to_validate is a dict)
    
### function  equivilence
>yutils.tools.equivilence

    Divides an iterator to groups, based on the function's result of every item in the iterator.
    Returns dict of lists.

    Example:
        >>> equivilence(range(10), lambda x: x % 3)
        >>>out>>> {0: [0, 3, 6, 9],
        >>>out>>>  1: [1, 4, 7],
        >>>out>>>  2: [2, 5, 8]}

    :param iterator: an iterator you wish to run on and divide into groups
    :type iterator: iterator
    :param func: a function to activate on each iterator item - its result decides the return dict's keys.
    :type func: function

    :rtype: dict of lists (lists are groups of original iterator)
    
#### function  camel_back_to_snake_case
>yutils.tools.case_conversions.camel_back_to_snake_case

    Turns a camelBack word to a snake_case word

    :param camel_back_word: wordInCamelCase
    :return: a_word_in_snake_case
    
#### function  camel_case_to_snake_case
>yutils.tools.case_conversions.camel_case_to_snake_case

    Turns a CamelCase word to a snake_case word

    :param camel_case_word: AWordInCamelCase
    :return: a_word_in_snake_case
    
#### function  snake_case_to_camel_back
>yutils.tools.case_conversions.snake_case_to_camel_back

    Turns a snake_case word to a camelBack word

    :param snake_case_word: a_word_in_snake_case
    :return: wordInCamelCase
    
#### function  snake_case_to_camel_case
>yutils.tools.case_conversions.snake_case_to_camel_case

    Turns a snake_case word to a CamelCase word

    :param snake_case_word: a_word_in_snake_case
    :return: AWordInCamelCase
    


#### function  get_file_length
>yutils.tools.files.get_file_length

    This function gets a file path and returns its length without reading it

    :param file_path: path to return length of
    :type file_path: str
    :return: file length (in bytes)
    :rtype: int
    
#### function  recursive_glob
>yutils.tools.files.recursive_glob

    Returns a list of all files in directory including sub-directories.

    :param dir_name: Dir name to glob recursively on
    :type dir_name: str
    :param ignore_hidden: if to ignore hidden files (that start with '.')
    :type ignore_hidden: bool

    :return: list of all files in the dir_name
    :rtype: list of str
    
#### function  save_file
>yutils.tools.files.save_file

    This function saves the file content to the destination dir (defaulted to ".") as base_name + extension,
    but adds a counter if needed.

    :param content: the content of the file
    :type content: str
    :param file_base_name: the future file name without extension
    :type file_base_name: str
    :param extension: the file name extension (for example: 'xlsx')
    :type extension: str
    :param dest_dir: where to save the file
                     Default: current directory
    :type dest_dir: str

    :return: full file path file was saved to
    :rtype: unicode
    


#### function  make_list
>yutils.tools.list.make_list

#### function  repr_list
>yutils.tools.list.repr_list

    Returns an iterator as a string, representing the list.
    :param iterator: the iterator you wish to represent as a list
    :type iterator: iterator
    :return: representation of your iterator as a list
    :rtype: unicode
    


#### function  get_indices_containing_all_substrings
>yutils.tools.numpy_tools.get_indices_containing_all_substrings

#### function  is_iterable
>yutils.tools.numpy_tools.is_iterable

#### function  magic
>yutils.tools.numpy_tools.magic

    Implementation taken from https://stackoverflow.com/questions/47834140/numpy-equivalent-of-matlabs-magic
    from user: user6655984
    
#### function  normalize_array
>yutils.tools.numpy_tools.normalize_array

#### function  r2c
>yutils.tools.numpy_tools.r2c

#### function  to_array
>yutils.tools.numpy_tools.to_array



#### function  pprint_dict
>yutils.tools.pretty_print.pprint_dict

    Prints a dict in a very pretty way!

    :param dictionary: your dict to print
    :type dictionary: dict
    :param long_value_limit: when a dict value exceeds this limit, it won't be printed
                             Default: 120
    :type long_value_limit: int
    :param long_value_filler: A filler to print instead of a long value, must have {type} and {length} fields!
                              Default: '<Long {type} object with repr length {length}>'
    :type long_value_filler: str
    :return: None
    
#### function  pprint_list
>yutils.tools.pretty_print.pprint_list

    Prints a list in an easy, short way.

    :param list_to_print: the list you wish to print
    :type list_to_print: list
    :return: None
    


#### function  turn_numeric
>yutils.tools.str.turn_numeric

    Turns a string into either an int or a float

    :param string: a string to assess
    :type string: str

    :rtype: str or float

    :raises: TypeError if no type was found
    


#### object  XLSXCreator
>yutils.tools.xlsx_creator.XLSXCreator


        A class to create an XLSX file from a table.
        It will format the table inside an actual excel's table, according to each field's width.

        :param headers: The fields of the table (headers)
        :type headers: list of unicode
        :param table: The table
        :type table: matrix - list of lists of the same lengths (cells may be any datatype)
        :param output_path: The path where to save the excel
        :type output_path: unicode
        
#### function  create_xlsx
>yutils.tools.xlsx_creator.create_xlsx

    Creates an XLSX file from a table.
    It will format the table inside an actual excel's table, according to each field's width.

    :param headers: The fields of the table (headers)
    :type headers: list of unicode
    :param table: The table
    :type table: matrix - list of lists of the same lengths (cells may be any datatype)
    :param output_path: The path where to save the excel
    :type output_path: unicode
    
#### function  get_next_column
>yutils.tools.xlsx_creator.get_next_column

#### function  get_next_letter
>yutils.tools.xlsx_creator.get_next_letter

#### function  table_to_str
>yutils.tools.xlsx_creator.table_to_str

    matrix good for the function xlsxwriter.Worksheet.add_table(['data': table))
    :param table: matrix - list of lists of the same lengths (cells may be any datatype)
    :return: fully string matrix
    




