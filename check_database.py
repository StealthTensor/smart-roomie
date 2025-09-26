import sqlite3
import os
from datetime import datetime

def check_database():
    print(" Smart Roomie Database Checker")
    print("=" * 50)
    
    db_path = 'backend/smartroomie.db'
    
    if not os.path.exists(db_path):
        print(" Database file not found!")
        return
    
    print(f" Database found at: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables_rows = cursor.fetchall()
        table_names = [row[0] for row in tables_rows] 
        print(f" Tables found: {table_names}")
        
        if 'students' not in table_names:
            print(" Students table missing!")
            print(" Creating students table...")
            
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    student_id TEXT UNIQUE NOT NULL,
                    contact_info TEXT NOT NULL,
                    email TEXT NOT NULL,
                    prefers_ac BOOLEAN NOT NULL,
                    room_capacity INTEGER NOT NULL,
                    gender TEXT NOT NULL,
                    smoker_okay BOOLEAN NOT NULL,
                    q1_sleep INTEGER NOT NULL,
                    q2_tidy INTEGER NOT NULL,
                    q3_noise INTEGER NOT NULL,
                    q4_friends_freq INTEGER NOT NULL,
                    q5_friday_pref INTEGER NOT NULL,
                    q6_overnight_guests INTEGER NOT NULL,
                    q7_conflict_style INTEGER NOT NULL,
                    q8_alone_time INTEGER NOT NULL,
                    q9_sports_games INTEGER NOT NULL,
                    q10_movies_music INTEGER NOT NULL,
                    self_description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            print("✅ Students table created successfully!")
        else:
            print("✅ Students table exists")
            
        
        cursor.execute("SELECT COUNT(*) FROM students")
        count = cursor.fetchone()[0]
        print(f" Total students: {count}")
        
        if count > 0:
            cursor.execute("SELECT name, student_id, email FROM students LIMIT 5")
            students = cursor.fetchall()
            print(f"\n Sample students:")
            for student in students:
                print(f"   • {student['name']} ({student['student_id']})")
        
        conn.close()
        print(f"\n Database check complete!")
        
    except Exception as e:
        print(f" Database error: {e}")

if __name__ == "__main__":
    check_database()
