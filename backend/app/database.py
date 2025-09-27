# backend/app/database.py

import sqlite3
import json
from datetime import datetime
from typing import List, Optional, Dict
from .models import Student, StudentCreate

class Database:
    def __init__(self, db_path: str = "smartroomie.db"):
        self.db_path = db_path

    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn

    def init_db(self):
        """Initialize the database with required tables - REMOVED SMOKING PREFERENCES"""
        conn = self.get_connection()
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    student_id TEXT UNIQUE NOT NULL,
                    contact_info TEXT NOT NULL,
                    email TEXT NOT NULL,
                    prefers_ac BOOLEAN NOT NULL,
                    room_capacity INTEGER NOT NULL,
                    gender TEXT NOT NULL,
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
            """)
            conn.commit()
            print("✅ Database table created/verified (smoking preferences removed)")
        except Exception as e:
            print(f"❌ Database initialization error: {e}")
            raise
        finally:
            conn.close()

    def create_student(self, student_data: StudentCreate) -> str:
        """Create a new student profile - REMOVED SMOKING PREFERENCES"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO students (
                    name, student_id, contact_info, email, prefers_ac, room_capacity, gender,
                    q1_sleep, q2_tidy, q3_noise, q4_friends_freq, q5_friday_pref,
                    q6_overnight_guests, q7_conflict_style, q8_alone_time, 
                    q9_sports_games, q10_movies_music, self_description
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                student_data.name,
                student_data.student_id,
                student_data.contact_info,
                student_data.email,
                student_data.prefers_ac,
                student_data.room_capacity,
                student_data.gender,
                student_data.q1_sleep,
                student_data.q2_tidy,
                student_data.q3_noise,
                student_data.q4_friends_freq,
                student_data.q5_friday_pref,
                student_data.q6_overnight_guests,
                student_data.q7_conflict_style,
                student_data.q8_alone_time,
                student_data.q9_sports_games,
                student_data.q10_movies_music,
                student_data.self_description
            ))
            conn.commit()
            return student_data.student_id
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                raise ValueError(f"Student ID {student_data.student_id} already exists")
            raise ValueError(f"Database constraint error: {e}")
        except Exception as e:
            raise ValueError(f"Failed to create student: {e}")
        finally:
            conn.close()

    def get_student(self, student_id: str) -> Optional[Student]:
        """Get a student by their ID"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
            row = cursor.fetchone()
            
            if row:
                return Student(
                    id=row['id'],
                    name=row['name'],
                    student_id=row['student_id'],
                    contact_info=row['contact_info'],
                    email=row['email'],
                    prefers_ac=bool(row['prefers_ac']),
                    room_capacity=row['room_capacity'],
                    gender=row['gender'],
                    q1_sleep=row['q1_sleep'],
                    q2_tidy=row['q2_tidy'],
                    q3_noise=row['q3_noise'],
                    q4_friends_freq=row['q4_friends_freq'],
                    q5_friday_pref=row['q5_friday_pref'],
                    q6_overnight_guests=row['q6_overnight_guests'],
                    q7_conflict_style=row['q7_conflict_style'],
                    q8_alone_time=row['q8_alone_time'],
                    q9_sports_games=row['q9_sports_games'],
                    q10_movies_music=row['q10_movies_music'],
                    self_description=row['self_description'],
                    created_at=datetime.fromisoformat(row['created_at']),
                    updated_at=datetime.fromisoformat(row['updated_at'])
                )
            return None
        finally:
            conn.close()

    def get_all_students(self) -> List[Student]:
        """Get all students from database"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students ORDER BY created_at DESC")
            rows = cursor.fetchall()
            
            students = []
            for row in rows:
                student = Student(
                    id=row['id'],
                    name=row['name'],
                    student_id=row['student_id'],
                    contact_info=row['contact_info'],
                    email=row['email'],
                    prefers_ac=bool(row['prefers_ac']),
                    room_capacity=row['room_capacity'],
                    gender=row['gender'],
                    q1_sleep=row['q1_sleep'],
                    q2_tidy=row['q2_tidy'],
                    q3_noise=row['q3_noise'],
                    q4_friends_freq=row['q4_friends_freq'],
                    q5_friday_pref=row['q5_friday_pref'],
                    q6_overnight_guests=row['q6_overnight_guests'],
                    q7_conflict_style=row['q7_conflict_style'],
                    q8_alone_time=row['q8_alone_time'],
                    q9_sports_games=row['q9_sports_games'],
                    q10_movies_music=row['q10_movies_music'],
                    self_description=row['self_description'],
                    created_at=datetime.fromisoformat(row['created_at']),
                    updated_at=datetime.fromisoformat(row['updated_at'])
                )
                students.append(student)
            
            return students
        finally:
            conn.close()

    def delete_student(self, student_id: str) -> bool:
        """Delete a student from database"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    def update_student_timestamp(self, student_id: str):
        """Update the updated_at timestamp for a student"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE students SET updated_at = CURRENT_TIMESTAMP WHERE student_id = ?",
                (student_id,)
            )
            conn.commit()
        finally:
            conn.close()