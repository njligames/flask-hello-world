from flask import Flask
import psycopg2
import os
import time
import facebook
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv

load_dotenv()

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

        CREATE_IMAGES_TABLE = ( "CREATE TABLE IF NOT EXISTS sudoku_image (id SERIAL PRIMARY KEY, name TEXT, photo BYTEA, used BOOLEAN);")
        DROP_IMAGES_TABLE = ( " DROP TABLE sudoku_image;" )

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

def insertBLOB(name, photo):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:

        # connect to the PostgreSQL server
        url = os.environ.get("DATABASE_URL")  # gets variables from environment
        conn = psycopg2.connect(url)

        INSERT_IMAGE = "INSERT INTO sudoku_image(name, photo, used) VALUES ( %s, %s, %s);"

        with conn:
            with conn.cursor() as cursor:
                empPhoto = convertToBinaryData(photo)
                used = False

                # Convert data into tuple format
                data_tuple = (name, psycopg2.Binary(empPhoto), used)
                cursor.execute(INSERT_IMAGE, data_tuple)

    except (Exception, psycopg2.DatabaseError) as error:
        print(str(error))
    finally:
        if conn is not None:
            conn.close()
            # print('finally - Database connection closed.')

    return conn

def print_date_time():
    tme=str(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
    print(tme)
    post_photo()

scheduler = BackgroundScheduler()
# Everyday = 5184000 = 24 * 60 * 60
everyday = 86400
# Everyhour = 3600 = 60 * 60
everyhour = 3600
# Everyminute = 60
everyminute = 60
scheduler.add_job(func=print_date_time, trigger="interval", seconds=everyday)
scheduler.start()

# Shut down the scheduler when exiting the app
# atexit.register(lambda: scheduler.shutdown)

app = Flask(__name__)

def initialize():
    connect()

    index = 1
    directory="/Users/jamesfolk/Work/SudokuADay/test/sqlite/SudokuPuzzlesVault/"
    dir_list = os.listdir(directory)
    dir_list.sort()
    number_of_files = len(dir_list)

    for file in dir_list:
        if index < (360 * 3):
            insertBLOB(file, directory + file)

            print(str(index) + " of " + str(360*3) + " " + file)

            index = index + 1
    print(index)


def post_binary_photo_to_facebook(image, message):
    user_access_token=os.environ.get("FB_USER_TOKEN")
    page_id=os.environ.get("FB_PAGE_ID")

    if None != user_access_token and None != page_id:

        print("User Access Token", user_access_token)

        graph = facebook.GraphAPI(access_token=user_access_token)
        pages = graph.get_object("me/accounts")
        page_access_token = graph.get_object(page_id, fields="access_token")["access_token"]

        print("Page Access Token", page_access_token)
        # todo = '''
        # Almost there! Not to get the correct images... hmm...
        # '''

        graph = facebook.GraphAPI(access_token=page_access_token)
        graph.debug = True
        # with open(photo_file_name, "rb") as image:
        graph.put_photo(image=image, message=message)
    else:
        print("FB_USER_TOKEN or FB_PAGE_ID environment variables are empty.")

def post_photo():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        url = os.environ.get("DATABASE_URL")  # gets variables from environment
        conn = psycopg2.connect(url)

        SELECT_ALL_FROM_TABLE = ( "SELECT * from sudoku_image WHERE used = FALSE;")

        with conn:
            with conn.cursor() as cursor:
                cursor.execute(SELECT_ALL_FROM_TABLE)

                data_tuple = cursor.fetchone()

                UPDATE_TABLE = ( "UPDATE sudoku_image SET used = TRUE WHERE id = {id}".format(id=data_tuple[0]) )

                cursor.execute(UPDATE_TABLE)

                name = data_tuple[1]
                image = data_tuple[2]
                message = """
Good morning sudoku lovers! 🧩 Today's puzzle is ready and waiting for you. Solve to your heart's content and check your answers on our website. If you're looking for even more sudoku fun, be sure to check out our new sudoku book now available on Amazon! 📚 Follow the link to purchase your copy today: https://bit.ly/3WUI0Y8. Happy solving!












#SudokuLover #SudokuChallenge #SudokuAddict #SudokuLover #SudokuAddict #SudokuLife #SudokuChallenge #SudokuSolver #SudokuMaster #SudokuPuzzle #SudokuEveryday #SudokuFun #SudokuCommunity
                """
                post_binary_photo_to_facebook(image, message)

    except (Exception, psycopg2.DatabaseError) as error:
        print(str(error))
    finally:
        if conn is not None:
            conn.close()
            print('finally - Database connection closed.')

    return conn

# post_photo()

@app.route('/')
def hello_world():
    return 'Hello, World!'
