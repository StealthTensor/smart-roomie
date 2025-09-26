from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
from pydantic import BaseModel
import uvicorn
from datetime import datetime
import sqlite3
import json


from .models import Student, StudentCreate, MatchResult
from .matching import MatchingService
from .database import Database

app = FastAPI(title="Smart Roomie API", version="1.0.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5500", "http://127.0.0.1:5500"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


db = Database()
matching_service = MatchingService(db)

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    db.init_db()
    print(" Database initialized successfully")
    print(" Smart Roomie API is running")
    print(" Available endpoints:")
    print("   - POST /api/students - Create student")
    print("   - GET /api/students - Get all students")
    print("   - GET /api/students/{id} - Get specific student")
    print("   - DELETE /api/students/{id} - Delete student")
    print("   - POST /api/matches - Generate all matches")
    print("   - GET /api/matches/{id} - Get matches for student")
    print("   - GET /api/stats - Get statistics")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Smart Roomie API is running",
        "version": "1.0.0",
        "status": "healthy",
        "endpoints": {
            "students": "/api/students",
            "matches": "/api/matches",
            "stats": "/api/stats"
        }
    }

@app.post("/api/students", response_model=Dict[str, str])
async def create_student(student: StudentCreate):
    """Create a new student profile"""
    try:
        print(f" Creating student: {student.name} (ID: {student.student_id})")
        student_id = db.create_student(student)
        print(f" Successfully created student: {student.name}")
        return {
            "message": "Student created successfully", 
            "student_id": student_id,
            "name": student.name
        }
    except ValueError as e:
        print(f" Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f" Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/students", response_model=List[Student])
async def get_all_students():
    """Get all student profiles"""
    try:
        students = db.get_all_students()
        print(f" Retrieved {len(students)} students")
        return students
    except Exception as e:
        print(f" Error retrieving students: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/students/{student_id}", response_model=Student)
async def get_student(student_id: str):
    """Get a specific student profile"""
    try:
        student = db.get_student(student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return student
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/matches", response_model=List[MatchResult])
async def calculate_matches():
    """Calculate roommate matches for all students"""
    try:
        print(" Generating roommate matches...")
        matches = matching_service.calculate_all_matches()
        print(f" Generated {len(matches)} matches")
        return matches
    except Exception as e:
        print(f" Error generating matches: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/matches/{student_id}", response_model=List[MatchResult])
async def get_student_matches(student_id: str):
    """Get matches for a specific student"""
    try:
        student = db.get_student(student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        matches = matching_service.get_matches_for_student(student_id)
        return matches
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/students/{student_id}")
async def delete_student(student_id: str):
    """Delete a student profile"""
    try:
        success = db.delete_student(student_id)
        if not success:
            raise HTTPException(status_code=404, detail="Student not found")
        
        print(f" Deleted student: {student_id}")
        return {"message": "Student deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        print(f" Error deleting student: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def get_stats():
    """Get application statistics"""
    try:
        students = db.get_all_students()
        total_students = len(students)
        
        # Calculate additional stats
        male_count = len([s for s in students if s.gender == 'Male'])
        female_count = len([s for s in students if s.gender == 'Female'])
        other_count = len([s for s in students if s.gender == 'Other'])
        ac_preference = len([s for s in students if s.prefers_ac])
        non_ac_preference = total_students - ac_preference
        
        return {
            "total_students": total_students,
            "male_students": male_count,
            "female_students": female_count,
            "other_students": other_count,
            "ac_preference": ac_preference,
            "non_ac_preference": non_ac_preference,
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        print(f" Error getting stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        students = db.get_all_students()
        return {
            "status": "healthy",
            "database": "connected",
            "total_students": len(students),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

if __name__ == "__main__":
    print(" Starting Smart Roomie API...")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")