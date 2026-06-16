import sqlite3
# *******************************Setting up DB*******************************************************************
# connect to db
connection = sqlite3.connect(database='interview_tracker.db')

# create a cursor object to execute sql command
cursor = connection.cursor()

# create a table & query a db
cursor.execute('''
    CREATE TABLE IF NOT EXISTS CompanyDetails (
        company_id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT NOT NULL,
        position TEXT NOT NULL,
        overall_status TEXT CHECK (
            overall_status IN ('Pending', 'Selected', 'Rejected', 'OfferReceived')
        ),
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        total_rounds INT DEFAULT 0,
        UNIQUE(company_name, position)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS InterviewRounds (
        interview_id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id INTEGER NOT NULL,
        round_number INTEGER NOT NULL,
        interview_date DATETIME,
        interview_status TEXT CHECK(
            interview_status IN ('Pending', 'Selected', 'Rejected')
        ),
        questions_asked TEXT,
        need_improvement TEXT,
        UNIQUE(company_id, round_number),
        FOREIGN KEY (company_id) REFERENCES CompanyDetails(company_id)              
    )
''')

# save(commit) the changes and close the connection 
connection.commit()
connection.close()