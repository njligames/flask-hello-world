from flask import Flask, render_template, request
import psycopg2
import os
from dotenv import load_dotenv
import base64
import redis

load_dotenv()

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

    r = redis.from_url(os.environ['REDIS_URL'])

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









