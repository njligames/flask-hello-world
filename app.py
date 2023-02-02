from flask import Flask, render_template, request
import psycopg2
import os
import time
import facebook
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path
import base64
import random
import redis

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

        SELECT_ALL_FROM_TABLE = ( "SELECT * from sudoku_image WHERE used = FALSE AND solution = FALSE;")

        with conn:
            with conn.cursor() as cursor:
                cursor.execute(SELECT_ALL_FROM_TABLE)

                data_tuple = cursor.fetchone()

                UPDATE_TABLE = ( "UPDATE sudoku_image SET used = TRUE WHERE id = {id}".format(id=data_tuple[0]) )

                cursor.execute(UPDATE_TABLE)

                name = data_tuple[1]
                image = data_tuple[2]
                message = getRandomMessage()

                home = "https://sudokuaday.onrender.com/"
                solution = home + name.split(".")[2]
                message = message + "\n\n\n\n\n\nSolution: " + solution

                post_binary_photo_to_facebook(image, message)

    except (Exception, psycopg2.DatabaseError) as error:
        print(str(error))
    finally:
        if conn is not None:
            conn.close()
            print('finally - Database connection closed.')

    return conn
def getRandomMessage():
    messages = [
            "Rise and shine, it's time for a new sudoku challenge! Who's ready to put their skills to the test today? 💪🧩 Check out today's puzzle and check your answers on our site. #SudokuLife #SudokuChallenge #SudokuAddict",
            "It's a beautiful day for a sudoku puzzle! What better way to start your day than with a mental workout? 🧠 Try today's puzzle and see how you stack up! #SudokuSolver #SudokuLife #SudokuCommunity",
            "Feeling stuck on today's sudoku puzzle? Don't give up! Our website has the answers you need to keep going. Happy solving! 💪🧩 #SudokuChallenge #SudokuLife #SudokuAddict",
            "Calling all sudoku enthusiasts! It's time for a new puzzle. Are you up for the challenge? 🧩 Check out today's puzzle and see if you can beat your personal best. #SudokuSolver #SudokuFun #SudokuMaster",
            "Step away from the screens and enjoy some offline sudoku fun with our new book, now available on Amazon! 📚 Follow the link to purchase: {link}. Happy solving! 🧩 #SudokuLover #SudokuBook #SudokuChallenge",
            "{dayofweek} mornings just got a whole lot better with a new sudoku puzzle! Get your mind working and start the week off right. 🧠 #SudokuMonday #SudokuLife #SudokuFun",
            "Think you're a sudoku pro? Prove it with today's puzzle! 🧩 Check your answers on our website and see where you stand. #SudokuPro #SudokuChallenge #SudokuAddict",
            "Can't get enough sudoku? Join our community and never run out of puzzles! 🧩 #SudokuCommunity #SudokuLife #SudokuAddict",
            "Sudoku for all skill levels! Whether you're just starting or a seasoned pro, we've got the puzzle for you. Check out today's puzzle on our site. 🧩 #SudokuForEveryone #SudokuFun #SudokuLife",
            "Take a break from work and solve some sudoku! Today's puzzle is ready and waiting. 🧩 Check your answers on our site. #SudokuBreak #SudokuLife #SudokuChallenge",
            "Need a brain boost? Look no further than today's sudoku puzzle! Give your mind a workout and check your answers on our site. 🧠🧩 #SudokuBrainBoost #SudokuLife #SudokuChallenge",
            "Looking for a new hobby? Try sudoku! Today's puzzle is up on our site. 🧩 #SudokuHobby #SudokuLife #SudokuChallenge",
            "Can't get enough of sudoku? Check out our new book, packed with puzzles and fun! Available now on Amazon. 📚 Follow the link to purchase: {link}. #SudokuBook #SudokuFun #SudokuLover",
            "Feeling competitive? Challenge your friends to today's sudoku puzzle and see who comes out on top! Check answers on our site. 🧩 #SudokuCompetition #SudokuChallenge #SudokuLife",
            "Take a break from screen time and enjoy some sudoku instead! Today's puzzle is up on our site. 🧩 #SudokuBreak #SudokuFun #SudokuChallenge",
            "Sudoku for all ages! Today's puzzle is perfect for the whole family. Check answers on our site. 🧩 #SudokuFamily #SudokuFun #SudokuChallenge",
            "Get your daily dose of sudoku with today's puzzle! Check your answers on our site. 🧩 #SudokuEveryday #SudokuChallenge #SudokuLife",
            "Step up your sudoku game with our new book! Packed with tips and tricks. Available now on Amazon. 📚 Follow the link to purchase: {link}. #SudokuMaster #SudokuBook #SudokuChallenge",
            "Take on today's sudoku puzzle and see how you measure up! Check answers on our site. 🧩 #SudokuMeasureUp #SudokuChallenge #SudokuLife",
            "Sudoku for all skill levels! Check out today's puzzle and see if you can beat your best time. 🧩 #SudokuForEveryone #SudokuChallenge #SudokuLife",
            "Join the sudoku community and never run out of puzzles! Today's puzzle is up on our site. 🧩 #SudokuCommunity #SudokuLife #SudokuChallenge",
            "Sudoku lovers unite! Share your progress and challenge your friends with today's puzzle. Check answers on our site. 🧩 #SudokuCommunity #SudokuChallenge #SudokuLove",
            "Take your sudoku skills to the next level with our expert tips and tricks. Available in our new book on Amazon. 📚 Follow the link to purchase: {link}. #SudokuExpert #SudokuBook #SudokuChallenge",
            "Today's sudoku puzzle is a real brain teaser! Can you solve it? Check your answers on our site. 🧩 #SudokuBrainTeaser #SudokuChallenge #SudokuLife",
            "Never a dull moment with sudoku! Today's puzzle is up on our site. 🧩 #SudokuEntertainment #SudokuLife #SudokuChallenge",
            "Put your sudoku skills to the test with today's challenging puzzle. Check answers on our site. 🧩 #SudokuSkillsTest #SudokuChallenge #SudokuLife",
            "Take a break from the world and solve today's sudoku puzzle. Check answers on our site. 🧩 #SudokuEscape #SudokuChallenge #SudokuLife",
            "Get inspired to solve today's sudoku puzzle with our motivational quotes. Check out our site. 🧩 #SudokuMotivation #SudokuChallenge #SudokuLife",
            "Step up your sudoku game with our new book, filled with advanced strategies. Available now on Amazon. 📚 Follow the link to purchase: {link}. #SudokuStrategy #SudokuBook #SudokuChallenge",
            "Challenge yourself and solve today's sudoku puzzle! Check answers on our site. 🧩 #SudokuChallengeYourself #SudokuChallenge #SudokuLife",
            "Sudoku for all levels of experience! Check out today's puzzle and see how you measure up. 🧩 #SudokuExperience #SudokuChallenge #SudokuLife",
            "Sudoku for all moods! Whether you're feeling stressed or relaxed, today's puzzle is perfect for you. Check answers on our site. 🧩 #SudokuForAllMoods #SudokuChallenge #SudokuLife",
            "Never run out of sudoku puzzles with our daily updates! Today's puzzle is up on our site. 🧩 #SudokuDaily #SudokuLife #SudokuChallenge",
            "Take your sudoku game to the next level with our expert book. Available now on Amazon. 📚 Follow the link to purchase: {link}. #SudokuExpertLevel #SudokuBook #SudokuChallenge",
            "Today's sudoku puzzle is perfect for a quick break from work. Check answers on our site. 🧩 #SudokuWorkBreak #SudokuChallenge #SudokuLife",
            "Get your daily sudoku fix with our daily puzzles. Check answers on our site. 🧩 #SudokuDailyFix #SudokuChallenge #SudokuLife",
            ]
    randomIndex = random.randrange(len(messages))
    dt = datetime.now()

    dayofweek=dt.strftime('%A')
    link = "https://bit.ly/3WUI0Y8"

    return messages[randomIndex].format(dayofweek=dayofweek, link=link)

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
# print_date_time()

# initialize()
# connect()

# Shut down the scheduler when exiting the app
# atexit.register(lambda: scheduler.shutdown)

app = Flask(__name__)

@app.route('/')
def hello():


    """ Connect to the PostgreSQL database server """
    conn = None
    try:

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        url = os.environ.get("DATABASE_URL")  # gets variables from environment
        conn = psycopg2.connect(url)

        SELECT_ALL_TABLE = ( "SELECT name from sudoku_image WHERE used = TRUE;")
        with conn:
            with conn.cursor() as cursor:
                # cursor.execute("SELECT * from sudoku_image;")
                # print(cursor.fetchall())

                cursor.execute(SELECT_ALL_TABLE)

                names = cursor.fetchall()

                # home = "http://127.0.0.1:5000/"
                solutions=[]
                home = request.base_url
                for name in names:
                    solution = home + name[0].split(".")[2]
                    solutions.append((solution, name[0].split(".")[2]))

    except (Exception, psycopg2.DatabaseError) as error:
        print(str(error))
    finally:
        if conn is not None:
            conn.close()
            print('finally - Database connection closed.')

    return render_template('solutions.html', solutions=solutions )

@app.route('/<name>')
def hello_world(name=None):

    # r = redis.from_url(os.environ['REDIS_URL'])
    r = redis.from_url("redis://red-cfdksekgqg45rntqt0cg:6379")


    """ Connect to the PostgreSQL database server """
    conn = None
    encoded_image = r.get(name)
    if None == encoded_image:
        try:

            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            url = os.environ.get("DATABASE_URL")  # gets variables from environment
            conn = psycopg2.connect(url)

            SELECT_ALL_TABLE = ( "SELECT photo from sudoku_image WHERE LOWER(name) = LOWER('solved.sudoku.{name}.png');".format(name=name))
            with conn:
                with conn.cursor() as cursor:
                    # cursor.execute("SELECT * from sudoku_image;")
                    # print(cursor.fetchall())

                    cursor.execute(SELECT_ALL_TABLE)

                    photo = cursor.fetchone()
                    if None != photo:
                        print("James")
                        print(photo[0])
                        print("JAMES")

                        encoded_image = base64.b64encode(photo[0])
                        r.set(name, encoded_image)

        except (Exception, psycopg2.DatabaseError) as error:
            print(str(error))
        finally:
            if conn is not None:
                conn.close()
                print('finally - Database connection closed.')

    return render_template('solution.html', img=encoded_image )









