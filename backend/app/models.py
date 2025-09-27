# backend/app/models.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class StudentCreate(BaseModel):
    """Model for creating a new student - REMOVED OTHER GENDER"""
    name: str = Field(..., min_length=1, max_length=100)
    student_id: str = Field(..., min_length=1, max_length=50)
    contact_info: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    prefers_ac: bool
    room_capacity: int = Field(..., ge=2, le=4)  # 2-4 people per room (REMOVED 1-sharing)
    gender: str = Field(..., pattern=r'^(Male|Female)$')  # REMOVED Other gender
    
    # Questionnaire responses (1-5 scale)
    q1_sleep: int = Field(..., ge=1, le=5, description="Sleep schedule preference (1=Early bird, 5=Night owl)")
    q2_tidy: int = Field(..., ge=1, le=5, description="Tidiness level (1=Very messy, 5=Very neat)")
    q3_noise: int = Field(..., ge=1, le=5, description="Noise tolerance (1=Need quiet, 5=Don't mind noise)")
    q4_friends_freq: int = Field(..., ge=1, le=5, description="Friends visit frequency (1=Never, 5=Daily)")
    q5_friday_pref: int = Field(..., ge=1, le=5, description="Friday night preference (1=Stay in, 5=Go out)")
    q6_overnight_guests: int = Field(..., ge=1, le=5, description="Overnight guests frequency (1=Never, 5=Often)")
    q7_conflict_style: int = Field(..., ge=1, le=5, description="Conflict resolution style (1=Avoid, 5=Direct confrontation)")
    q8_alone_time: int = Field(..., ge=1, le=5, description="Need for alone time (1=Very social, 5=Need lots of alone time)")
    q9_sports_games: int = Field(..., ge=1, le=5, description="Interest in sports/games (1=Not interested, 5=Very interested)")
    q10_movies_music: int = Field(..., ge=1, le=5, description="Interest in movies/music (1=Not interested, 5=Very interested)")
    
    # Optional description
    self_description: Optional[str] = Field(None, max_length=500)

class Student(BaseModel):
    """Model for student data from database - REMOVED OTHER GENDER"""
    id: int
    name: str
    student_id: str
    contact_info: str
    email: str
    prefers_ac: bool
    room_capacity: int
    gender: str  # Only Male or Female
    
    # Questionnaire responses
    q1_sleep: int
    q2_tidy: int
    q3_noise: int
    q4_friends_freq: int
    q5_friday_pref: int
    q6_overnight_guests: int
    q7_conflict_style: int
    q8_alone_time: int
    q9_sports_games: int
    q10_movies_music: int
    
    self_description: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class MatchResult(BaseModel):
    """Model for roommate match result"""
    student1_id: str
    student2_id: str
    student1_name: str
    student2_name: str
    compatibility_score: float = Field(..., ge=0.0, le=1.0)
    habits_similarity: float = Field(..., ge=0.0, le=1.0)
    social_similarity: float = Field(..., ge=0.0, le=1.0)
    conflict_similarity: float = Field(..., ge=0.0, le=1.0)
    interests_similarity: float = Field(..., ge=0.0, le=1.0)
    constraints_matched: bool
    match_explanation: Optional[str] = None
    created_at: datetime