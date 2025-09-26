# backend/app/matching.py
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple
from datetime import datetime
from .models import Student, MatchResult
from .database import Database

class MatchingService:
    def __init__(self, database: Database):
        self.db = database
        
        # Weights for different compatibility domains
        self.weights = {
            'habits': 0.5,
            'social': 0.25,
            'conflict': 0.2,
            'interests': 0.05
        }
        
        # Penalty thresholds for deal-breaker model
        self.penalty_thresholds = {
            'habits': 0.6,
            'conflict': 0.5
        }
        
        # Penalty factors
        self.penalty_factors = {
            'habits': 0.7,  # 30% penalty
            'conflict': 0.8  # 20% penalty
        }
    
    def filter_potential_matches(self, target_student: Student, all_students: List[Student]) -> List[Student]:
        """Filter students based on hard constraints"""
        potential_matches = []
        
        for student in all_students:
            if student.student_id == target_student.student_id:
                continue
                
            # Hard constraints that must match
            if (student.prefers_ac == target_student.prefers_ac and
                student.room_capacity == target_student.room_capacity and
                student.gender == target_student.gender and
                student.smoker_okay == target_student.smoker_okay):
                potential_matches.append(student)
        
        return potential_matches
    
    def vectorize_student(self, student: Student) -> Dict[str, np.ndarray]:
        """Convert student questionnaire responses to domain vectors"""
        return {
            'habits': np.array([student.q1_sleep, student.q2_tidy, student.q3_noise]),
            'social': np.array([student.q4_friends_freq, student.q5_friday_pref, student.q6_overnight_guests]),
            'conflict': np.array([student.q7_conflict_style, student.q8_alone_time]),
            'interests': np.array([student.q9_sports_games, student.q10_movies_music])
        }
    
    def calculate_similarity(self, vector1: np.ndarray, vector2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        # Reshape vectors for sklearn
        v1 = vector1.reshape(1, -1)
        v2 = vector2.reshape(1, -1)
        
        # Calculate cosine similarity
        similarity = cosine_similarity(v1, v2)[0][0]
        
        # Convert to 0-1 range (cosine similarity returns -1 to 1)
        normalized_similarity = (similarity + 1) / 2
        
        return max(0.0, min(1.0, normalized_similarity))
    
    def calculate_compatibility_score(self, student1: Student, student2: Student) -> Tuple[float, Dict[str, float]]:
        """
        Calculate compatibility score using the Deal-Breaker Penalty Model
        Returns: (final_score, similarity_breakdown)
        """
        # Vectorize both students
        vectors1 = self.vectorize_student(student1)
        vectors2 = self.vectorize_student(student2)
        
        # Calculate similarity for each domain
        similarities = {}
        for domain in self.weights.keys():
            similarities[domain] = self.calculate_similarity(vectors1[domain], vectors2[domain])
        
        # Calculate base weighted score
        base_score = sum(similarities[domain] * self.weights[domain] for domain in self.weights.keys())
        
        # Apply penalty model
        final_score = base_score
        
        # Apply habit penalty if below threshold
        if similarities['habits'] < self.penalty_thresholds['habits']:
            final_score *= self.penalty_factors['habits']
        
        # Apply conflict penalty if below threshold
        if similarities['conflict'] < self.penalty_thresholds['conflict']:
            final_score *= self.penalty_factors['conflict']
        
        # Ensure score is between 0 and 1
        final_score = max(0.0, min(1.0, final_score))
        
        return final_score, similarities
    
    def create_match_explanation(self, score: float, similarities: Dict[str, float], student1: Student, student2: Student) -> str:
        """Generate a human-readable explanation for the match"""
        explanations = []
        
        # Overall compatibility
        if score >= 0.8:
            explanations.append("Excellent overall compatibility")
        elif score >= 0.6:
            explanations.append("Good compatibility with minor differences")
        elif score >= 0.4:
            explanations.append("Moderate compatibility with some differences")
        else:
            explanations.append("Lower compatibility with significant differences")
        
        # Domain-specific insights
        if similarities['habits'] >= 0.8:
            explanations.append("Very similar living habits")
        elif similarities['habits'] < 0.4:
            explanations.append("Different living habits may require adjustment")
        
        if similarities['social'] >= 0.8:
            explanations.append("Compatible social preferences")
        elif similarities['social'] < 0.4:
            explanations.append("Different social preferences")
        
        if similarities['conflict'] < 0.4:
            explanations.append("Different conflict resolution styles")
        
        return "; ".join(explanations)
    
    def get_matches_for_student(self, student_id: str, limit: int = 10) -> List[MatchResult]:
        """Get top matches for a specific student"""
        target_student = self.db.get_student(student_id)
        if not target_student:
            return []
        
        all_students = self.db.get_all_students()
        potential_matches = self.filter_potential_matches(target_student, all_students)
        
        match_results = []
        
        for candidate in potential_matches:
            score, similarities = self.calculate_compatibility_score(target_student, candidate)
            
            explanation = self.create_match_explanation(score, similarities, target_student, candidate)
            
            match_result = MatchResult(
                student1_id=target_student.student_id,
                student2_id=candidate.student_id,
                student1_name=target_student.name,
                student2_name=candidate.name,
                compatibility_score=score,
                habits_similarity=similarities['habits'],
                social_similarity=similarities['social'],
                conflict_similarity=similarities['conflict'],
                interests_similarity=similarities['interests'],
                constraints_matched=True,  # All filtered matches have constraints matched
                match_explanation=explanation,
                created_at=datetime.now()
            )
            
            match_results.append(match_result)
        
        # Sort by compatibility score (descending)
        match_results.sort(key=lambda x: x.compatibility_score, reverse=True)
        
        return match_results[:limit]
    
    def calculate_all_matches(self) -> List[MatchResult]:
        """Calculate matches for all students (for admin dashboard)"""
        all_students = self.db.get_all_students()
        all_matches = []
        processed_pairs = set()
        
        for i, student1 in enumerate(all_students):
            for j, student2 in enumerate(all_students):
                if i >= j:  # Skip same student and avoid duplicate pairs
                    continue
                
                pair_key = tuple(sorted([student1.student_id, student2.student_id]))
                if pair_key in processed_pairs:
                    continue
                
                processed_pairs.add(pair_key)
                
                # Check hard constraints
                if not (student1.prefers_ac == student2.prefers_ac and
                       student1.room_capacity == student2.room_capacity and
                       student1.gender == student2.gender and
                       student1.smoker_okay == student2.smoker_okay):
                    continue
                
                score, similarities = self.calculate_compatibility_score(student1, student2)
                explanation = self.create_match_explanation(score, similarities, student1, student2)
                
                match_result = MatchResult(
                    student1_id=student1.student_id,
                    student2_id=student2.student_id,
                    student1_name=student1.name,
                    student2_name=student2.name,
                    compatibility_score=score,
                    habits_similarity=similarities['habits'],
                    social_similarity=similarities['social'],
                    conflict_similarity=similarities['conflict'],
                    interests_similarity=similarities['interests'],
                    constraints_matched=True,
                    match_explanation=explanation,
                    created_at=datetime.now()
                )
                
                all_matches.append(match_result)
        
        # Sort by compatibility score (descending)
        all_matches.sort(key=lambda x: x.compatibility_score, reverse=True)
        
        return all_matches