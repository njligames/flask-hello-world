import psycopg2
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

def initialize():
    connect()

    total_number = 365 * 2

    directory= str(Path.cwd()) + "/SudokuPuzzlesVault/"
    puzzle_directory = directory + "puzzle/"

    index = 1
    puzzle_dir_list = os.listdir(puzzle_directory)
    puzzle_dir_list.sort()
    number_of_files = len(puzzle_dir_list)
    for file in puzzle_dir_list:
        if index < total_number:
            insertBLOB(file, puzzle_directory + file, False)
            print(str(index) + " of " + str(360*3) + " " + file + " for puzzle.")
            index = index + 1

    solved_directory = directory + "solved/"
    index = 1
    solved_dir_list = os.listdir(solved_directory)
    solved_dir_list.sort()
    number_of_files = len(solved_dir_list)
    for file in solved_dir_list:
        if index < total_number:
            insertBLOB(file, solved_directory + file, False)
            print(str(index) + " of " + str(360*3) + " " + file + " for solved.")
            index = index + 1


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        url = os.environ.get("DATABASE_URL")  # gets variables from environment
        conn = psycopg2.connect(url)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(str(db_version))

        DROP_IMAGES_TABLE = ( " DROP TABLE IF EXISTS sudoku_image;" )
        CREATE_IMAGES_TABLE = ( "CREATE TABLE IF NOT EXISTS sudoku_image (id SERIAL PRIMARY KEY, name TEXT, photo BYTEA, used BOOLEAN, solution BOOLEAN);")

        with conn:
            with conn.cursor() as cursor:
                cursor.execute(DROP_IMAGES_TABLE)
                cursor.execute(CREATE_IMAGES_TABLE)

        # execute a statement
        print('PostgreSQL database select sudoku_image table data:')
        cur.execute('SELECT * from sudoku_image')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(str(db_version))

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(str(error))
    finally:
        if conn is not None:
            conn.close()
            print('finally - Database connection closed.')

    return conn

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def insertBLOB(name, photo, isSolution):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:

        # connect to the PostgreSQL server
        url = os.environ.get("DATABASE_URL")  # gets variables from environment
        conn = psycopg2.connect(url)

        INSERT_IMAGE = "INSERT INTO sudoku_image(name, photo, used, solution) VALUES ( %s, %s, %s, %s);"

        with conn:
            with conn.cursor() as cursor:
                empPhoto = convertToBinaryData(photo)
                used = False

                # Convert data into tuple format
                data_tuple = (name, psycopg2.Binary(empPhoto), used, isSolution)
                cursor.execute(INSERT_IMAGE, data_tuple)

    except (Exception, psycopg2.DatabaseError) as error:
        print(str(error))
    finally:
        if conn is not None:
            conn.close()
            # print('finally - Database connection closed.')

    return conn
load_dotenv()
def initialize():
    connect()

    total_number = 365 * 2

    directory= str(Path.cwd()) + "/SudokuPuzzlesVault/"
    puzzle_directory = directory + "puzzle/"

    index = 1
    puzzle_dir_list = os.listdir(puzzle_directory)
    puzzle_dir_list.sort()
    number_of_files = len(puzzle_dir_list)
    for file in puzzle_dir_list:
        if index < total_number:
            insertBLOB(file, puzzle_directory + file, False)
            print(str(index) + " of " + str(360*3) + " " + file + " for puzzle.")
            index = index + 1

    solved_directory = directory + "solved/"
    index = 1
    solved_dir_list = os.listdir(solved_directory)
    solved_dir_list.sort()
    number_of_files = len(solved_dir_list)
    for file in solved_dir_list:
        if index < total_number:
            insertBLOB(file, solved_directory + file, False)
            print(str(index) + " of " + str(360*3) + " " + file + " for solved.")
            index = index + 1


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        url = os.environ.get("DATABASE_URL")  # gets variables from environment
        conn = psycopg2.connect(url)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(str(db_version))

        DROP_IMAGES_TABLE = ( " DROP TABLE IF EXISTS sudoku_image;" )
        CREATE_IMAGES_TABLE = ( "CREATE TABLE IF NOT EXISTS sudoku_image (id SERIAL PRIMARY KEY, name TEXT, photo BYTEA, used BOOLEAN, solution BOOLEAN);")

        with conn:
            with conn.cursor() as cursor:
                cursor.execute(DROP_IMAGES_TABLE)
                cursor.execute(CREATE_IMAGES_TABLE)

        # execute a statement
        print('PostgreSQL database select sudoku_image table data:')
        cur.execute('SELECT * from sudoku_image')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(str(db_version))

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(str(error))
    finally:
        if conn is not None:
            conn.close()
            print('finally - Database connection closed.')

    return conn

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def insertBLOB(name, photo, isSolution):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:

        # connect to the PostgreSQL server
        url = os.environ.get("DATABASE_URL")  # gets variables from environment
        conn = psycopg2.connect(url)

        INSERT_IMAGE = "INSERT INTO sudoku_image(name, photo, used, solution) VALUES ( %s, %s, %s, %s);"

        with conn:
            with conn.cursor() as cursor:
                empPhoto = convertToBinaryData(photo)
                used = False

                # Convert data into tuple format
                data_tuple = (name, psycopg2.Binary(empPhoto), used, isSolution)
                cursor.execute(INSERT_IMAGE, data_tuple)

    except (Exception, psycopg2.DatabaseError) as error:
        print(str(error))
    finally:
        if conn is not None:
            conn.close()
            # print('finally - Database connection closed.')

    return conn
load_dotenv()
def initialize():
    connect()

    total_number = 365 * 2

    directory= str(Path.cwd()) + "/SudokuPuzzlesVault/"
    puzzle_directory = directory + "puzzle/"

    index = 1
    puzzle_dir_list = os.listdir(puzzle_directory)
    puzzle_dir_list.sort()
    number_of_files = len(puzzle_dir_list)
    for file in puzzle_dir_list:
        if index < total_number:
            insertBLOB(file, puzzle_directory + file, False)
            print(str(index) + " of " + str(360*3) + " " + file + " for puzzle.")
            index = index + 1

    solved_directory = directory + "solved/"
    index = 1
    solved_dir_list = os.listdir(solved_directory)
    solved_dir_list.sort()
    number_of_files = len(solved_dir_list)
    for file in solved_dir_list:
        if index < total_number:
            insertBLOB(file, solved_directory + file, False)
            print(str(index) + " of " + str(360*3) + " " + file + " for solved.")
            index = index + 1


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        url = os.environ.get("DATABASE_URL")  # gets variables from environment
        conn = psycopg2.connect(url)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(str(db_version))

        DROP_IMAGES_TABLE = ( " DROP TABLE IF EXISTS sudoku_image;" )
        CREATE_IMAGES_TABLE = ( "CREATE TABLE IF NOT EXISTS sudoku_image (id SERIAL PRIMARY KEY, name TEXT, photo BYTEA, used BOOLEAN, solution BOOLEAN);")

        with conn:
            with conn.cursor() as cursor:
                cursor.execute(DROP_IMAGES_TABLE)
                cursor.execute(CREATE_IMAGES_TABLE)

        # execute a statement
        print('PostgreSQL database select sudoku_image table data:')
        cur.execute('SELECT * from sudoku_image')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(str(db_version))

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(str(error))
    finally:
        if conn is not None:
            conn.close()
            print('finally - Database connection closed.')

    return conn

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def insertBLOB(name, photo, isSolution):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:

        # connect to the PostgreSQL server
        url = os.environ.get("DATABASE_URL")  # gets variables from environment
        conn = psycopg2.connect(url)

        INSERT_IMAGE = "INSERT INTO sudoku_image(name, photo, used, solution) VALUES ( %s, %s, %s, %s);"

        with conn:
            with conn.cursor() as cursor:
                empPhoto = convertToBinaryData(photo)
                used = False

                # Convert data into tuple format
                data_tuple = (name, psycopg2.Binary(empPhoto), used, isSolution)
                cursor.execute(INSERT_IMAGE, data_tuple)

    except (Exception, psycopg2.DatabaseError) as error:
        print(str(error))
    finally:
        if conn is not None:
            conn.close()
            # print('finally - Database connection closed.')

    return conn

