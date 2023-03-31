#!/usr/bin/env python3
import time
import subprocess
import pymysql

# MySQL database connection details
db_host = "localhost"
db_user = "sqluser"
db_pass = "sqlpass"
db_name = "temp_fl"
table_name = "temp_fl"
field_name = "input_time"

# Command to start the server
start_command = "python3 /usr/sbin/server.py &"

# Command to kill the server
kill_command = "pkill -f 'python3 /usr/sbin/server.py'"

# Time to wait before checking again (in seconds)
check_interval = 600

def check_database():
    try:
        # Connect to the database
        conn = pymysql.connect(host=db_host, user=db_user, password=db_pass, db=db_name)

        # Create a cursor object
        cursor = conn.cursor()

        # Query to check the latest entry in the table
        query = "SELECT %s FROM %s ORDER BY %s DESC LIMIT 2" % (field_name, table_name, field_name)

        # Execute the query
        cursor.execute(query)

        # Get the latest input time
        latest_input_time = cursor.fetchone()[0]

        # Calculate the time difference
        time_difference = time.time() - latest_input_time.timestamp()

        # Check if the time difference is greater than 10 minutes
        if time_difference > check_interval:
            # Kill the server process
            subprocess.run(kill_command, shell=True)

            # Start the server process
            subprocess.Popen(start_command.split())

    except pymysql.Error as e:
        print("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))

    finally:
        # Close the database connection
        conn.close()

if __name__ == '__main__':
    while True:
        check_database()
        time.sleep(check_interval)
