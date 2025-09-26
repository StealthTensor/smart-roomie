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
        """Initialize the database with required tables"""
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
            """)
            
            # Create indexes for better performance
            conn.execute("CREATE INDEX IF NOT EXISTS idx_student_id ON students(student_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_gender ON students(gender)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_prefers_ac ON students(prefers_ac)")
            
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def create_student(self, student: StudentCreate) -> str:
        """Create a new student record"""
        conn = self.get_connection()
        try:
            cursor = conn.execute("""
                INSERT INTO students (
                    name, student_id, contact_info, email, prefers_ac, room_capacity,
                    gender, smoker_okay, q1_sleep, q2_tidy, q3_noise, q4_friends_freq,
                    q5_friday_pref, q6_overnight_guests, q7_conflict_style, q8_alone_time,
                    q9_sports_games, q10_movies_music, self_description
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                student.name, student.student_id, student.contact_info, student.email,
                student.prefers_ac, student.room_capacity, student.gender, student.smoker_okay,
                student.q1_sleep, student.q2_tidy, student.q3_noise, student.q4_friends_freq,
                student.q5_friday_pref, student.q6_overnight_guests, student.q7_conflict_style,
                student.q8_alone_time, student.q9_sports_games, student.q10_movies_music,
                student.self_description
            ))
            conn.commit()
            return student.student_id
        except sqlite3.IntegrityError:
            raise ValueError(f"Student with ID {student.student_id} already exists")
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def get_student(self, student_id: str) -> Optional[Student]:
        """Get a student by ID"""
        conn = self.get_connection()
        try:
            cursor = conn.execute("""
                SELECT * FROM students WHERE student_id = ?
            """, (student_id,))
            row = cursor.fetchone()
            
            if row:
                return Student(**dict(row))
            return None
        finally:
            conn.close()
    
    def get_all_students(self) -> List[Student]:
        """Get all students"""
        conn = self.get_connection()
        try:
            cursor = conn.execute("SELECT * FROM students ORDER BY created_at DESC")
            rows = cursor.fetchall()
            return [Student(**dict(row)) for row in rows]
        finally:
            conn.close()
    
    def update_student(self, student_id: str, student_data: Dict) -> bool:
        """Update a student record"""
        conn = self.get_connection()
        try:
            # Build dynamic update query
            set_clauses = []
            values = []
            
            for key, value in student_data.items():
                if key != 'student_id':  # Don't allow updating the primary identifier
                    set_clauses.append(f"{key} = ?")
                    values.append(value)
            
            if not set_clauses:
                return False
            
            set_clauses.append("updated_at = ?")
            values.append(datetime.now())
            values.append(student_id)
            
            query = f"UPDATE students SET {', '.join(set_clauses)} WHERE student_id = ?"
            cursor = conn.execute(query, values)
            conn.commit()
            
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def delete_student(self, student_id: str) -> bool:
        """Delete a student record"""
        conn = self.get_connection()
        try:
            cursor = conn.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def get_students_by_filters(self, filters: Dict) -> List[Student]:
        """Get students matching specific filters"""
        conn = self.get_connection()
        try:
            where_clauses = []
            values = []
            
            for key, value in filters.items():
                where_clauses.append(f"{key} = ?")
                values.append(value)
            
            if where_clauses:
                query = f"SELECT * FROM students WHERE {' AND '.join(where_clauses)}"
            else:
                query = "SELECT * FROM students"
            
            cursor = conn.execute(query, values)
            rows = cursor.fetchall()
            return [Student(**dict(row)) for row in rows]
        finally:
            conn.close()