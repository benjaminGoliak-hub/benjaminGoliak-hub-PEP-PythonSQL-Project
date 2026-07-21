import csv
import sqlite3

# Connect to the SQLite in-memory database
conn = sqlite3.connect(':memory:')

# A cursor object to execute SQL commands
cursor = conn.cursor()

def main():
    # Set logging level
    logging.basicConfig(level=logging.DEBUG, stream=logging)

    # users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        userId INTEGER PRIMARY KEY AUTOINCREMENT,
                        firstName TEXT,
                        lastName TEXT
                      )'''
                   )

    # callLogs table (with FK to users table)
    cursor.execute('''CREATE TABLE IF NOT EXISTS callLogs (
        callId INTEGER PRIMARY KEY AUTOINCREMENT,
        phoneNumber TEXT,
        startTime INTEGER,
        endTime INTEGER,
        direction TEXT,
        userId INTEGER,
        FOREIGN KEY (userId) REFERENCES users(userId)
    )''')

    # You will implement these methods below. They just print TO-DO messages for now.
    load_and_clean_users('../../resources/users.csv')
    load_and_clean_call_logs('../../resources/callLogs.csv')
    write_user_analytics('../../resources/userAnalytics.csv')
    write_ordered_calls('../../resources/orderedCalls.csv')

    # Helper method that prints the contents of the users and callLogs tables. Uncomment to see data.
    # select_from_users_and_call_logs()

    # Close the cursor and connection. main function ends here.
    cursor.close()
    conn.close()

# Helper to reuse the logic for filtering and inserting
def insert_csv_generic(file_path, statement):
    with open(file_path, "r") as user_file:
        print(f"File: {file_path} opened for reading")
        
        # Read the file lines
        file_lines = user_file.readlines()

        # Calculate the number of entries for a line 
        # Assumes the correct number of columns are in the header
        field_count = len(file_lines[0].split(','))
        print(f"{field_count} fields found in csv header")

        # Loop through all lines in the file except the headder line
        for line in file_lines[1:]:
            # Trim the line members using list comprehension
            line = [x.strip() for x in line.split(',')]
            print(f"Line to filter: {line}")

            # Skip if line has wrong field count
            if len(line) != field_count:
                print("Line Skipped! Wrong field count")
                continue

            # Skip if line has a whitespace entry (has been trimmed to '' at this point)
            if '' in line:
                print("Line Skipped! Whitespace entry")
                continue

            # Insert with provided statement
            cursor.execute(statement, line)

def write_csv_generic(file_path, statement, header):
    with open(file_path, "w") as usr_file:
        print(f"File {file_path} opened to write")

        # Write the header cleanly
        usr_file.write(header.strip() + '\n')
        print(f"Header: {header} added to CSV")

        # Run the sql statement and get the results
        try:
            # get the results for the querry
            statement_results = cursor.execute(statement).fetchall()
            print(f"SQL statement executed! Got {len(statement_results)} hits")

            # Cast all inner elements as strings
            statement_results = [[str(y) for y in x] for x in statement_results]

            # join each element in a line with ',' via list comprehension
            statement_results = [','.join(x) for x in statement_results]

            # join each line string with a newline
            statement_results = '\n'.join(statement_results)

            # write to file
            usr_file.write(statement_results)
            print("File written")
        except Exception as e:
            print(f"Caught Error: {e}")



# TODO: Implement the following 4 functions. The functions must pass the unit tests to complete the project.

# This function will load the users.csv file into the users table, discarding any records with incomplete data
def load_and_clean_users(file_path):
    print("Function load_and_clean_users called!")

    sql_statement = """
    INSERT INTO users (firstName, lastName) VALUES (?, ?)
    """
    insert_csv_generic(file_path, sql_statement)


# This function will load the callLogs.csv file into the callLogs table, discarding any records with incomplete data
def load_and_clean_call_logs(file_path):
    print("Function load_and_clean_call_logs called!")

    sql_statement = """
    INSERT INTO callLogs (phoneNumber, startTime, endTime, direction, userId) 
        VALUES (?, ?, ?, ?, ?)
    """
    insert_csv_generic(file_path, sql_statement)


# This function will write analytics data to testUserAnalytics.csv - average call time, and number of calls per user.
# You must save records consisting of each userId, avgDuration, and numCalls
# example: 1,105.0,4 - where 1 is the userId, 105.0 is the avgDuration, and 4 is the numCalls.
def write_user_analytics(csv_file_path):
    print("Function write_user_analytics called")
    
    # Select userID and avg of end-start group it by users
    sql_statement = """
    SELECT userId, (AVG(endTime) - AVG(startTime)), COUNT(*) FROM callLogs
    GROUP BY userId
    """
    header = "userId,avgDuration,numCalls"
    write_csv_generic(csv_file_path, sql_statement, header)


# This function will write the callLogs ordered by userId, then start time.
# Then, write the ordered callLogs to orderedCalls.csv
def write_ordered_calls(csv_file_path):
    print("Function write_ordered_calls called")
    
    # Select from callLogs but order it 
    sql_statement = """
    SELECT * FROM callLogs
    ORDER BY userID ASC, startTime ASC
    """
    header = "callId,phoneNumber,startTime,endTime,direction,userId"
    write_csv_generic(csv_file_path, sql_statement, header)



# No need to touch the functions below!------------------------------------------

# This function is for debugs/validation - uncomment the function invocation in main() to see the data in the database.
def select_from_users_and_call_logs():

    print()
    print("PRINTING DATA FROM USERS")
    print("-------------------------")

    # Select and print users data
    cursor.execute('''SELECT * FROM users''')
    for row in cursor:
        print(row)

    # new line
    print()
    print("PRINTING DATA FROM CALLLOGS")
    print("-------------------------")

    # Select and print callLogs data
    cursor.execute('''SELECT * FROM callLogs''')
    for row in cursor:
        print(row)


def return_cursor():
    return cursor


if __name__ == '__main__':
    main()
