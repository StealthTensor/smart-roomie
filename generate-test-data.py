"""
Smart Roomie - Test Data Generator

This script generates random student data for testing the Smart Roomie application.
It creates diverse student profiles with varying preferences to demonstrate the matching algorithm.
"""

import requests
import random
import json
from typing import List, Dict
import time


API_BASE_URL = "http://localhost:8000/api"
NUM_STUDENTS = 20  


FIRST_NAMES = {
    'Male': ['Alex', 'Ben', 'Chris', 'David', 'Ethan', 'Felix', 'George', 'Henry', 'Ian', 'Jack', 
             'Kevin', 'Luke', 'Michael', 'Nathan', 'Oscar', 'Paul', 'Quinn', 'Ryan', 'Sam', 'Tom'],
    'Female': ['Alice', 'Beth', 'Claire', 'Diana', 'Emma', 'Fiona', 'Grace', 'Hannah', 'Iris', 'Julia',
               'Kate', 'Lisa', 'Maya', 'Nina', 'Olivia', 'Priya', 'Quinn', 'Rachel', 'Sophie', 'Tara'],
    'Other': ['Avery', 'Blake', 'Cameron', 'Dakota', 'Emery', 'Finley', 'Gray', 'Harper', 'Jordan', 'Kai']
}

LAST_NAMES = ['Anderson', 'Brown', 'Chen', 'Davis', 'Evans', 'Fisher', 'Garcia', 'Harris', 'Johnson', 'Kim',
              'Lee', 'Martinez', 'Nielsen', 'O\'Connor', 'Patel', 'Rodriguez', 'Smith', 'Thompson', 'Wilson', 'Zhang']

UNIVERSITIES = ['university.edu', 'college.edu', 'tech.edu', 'state.edu']

PHONE_FORMATS = ['+1-555-{:03d}-{:04d}', '(555) {:03d}-{:04d}', '555.{:03d}.{:04d}']

SELF_DESCRIPTIONS = [
    "I'm a computer science major who loves gaming and coding late into the night. Looking for someone who doesn't mind the occasional keyboard clicking!",
    "Pre-med student who's very organized and focused on studies. I enjoy quiet environments and early morning workouts.",
    "Art major with a creative spirit. I love painting, music, and having deep conversations. My space tends to be a bit messy but I'm working on it!",
    "Business student who's pretty social and loves networking events. I enjoy having friends over and trying new restaurants.",
    "Engineering student with a practical mindset. I keep things neat, respect quiet hours, and believe in direct communication.",
    "Psychology major who's empathetic and easy-going. I love watching movies, listening to podcasts, and occasional social gatherings.",
    "Literature student who enjoys quiet reading time and intellectual discussions. I prefer a calm, organized living space.",
    "Sports management major who's active and outgoing. I play intramural sports and enjoy weekend adventures.",
    "Environmental science student passionate about sustainability. I prefer natural lighting, plants, and eco-friendly living.",
    "Music major who practices piano daily. I'm respectful of noise levels and looking for someone who appreciates the arts.",
    "International student adjusting to campus life. I'm friendly, curious about American culture, and love cooking traditional dishes.",
    "Finance major who's goal-oriented and organized. I enjoy networking, studying in groups, and the occasional party.",
    "Philosophy major who enjoys deep conversations and quiet contemplation. I'm a night owl who loves reading and writing.",
    "Biology major planning for graduate school. I'm studious, keep regular hours, and appreciate a clean, focused environment.",
    "Communications major who's social and loves meeting new people. I'm involved in several clubs and enjoy campus events.",
    ""  
]

PERSONALITY_PROFILES = [
    # Early Bird, Very Neat, Quiet
    {'q1_sleep': 1, 'q2_tidy': 5, 'q3_noise': 1, 'q4_friends_freq': 1, 'q5_friday_pref': 1, 
     'q6_overnight_guests': 1, 'q7_conflict_style': 2, 'q8_alone_time': 4, 'q9_sports_games': 2, 'q10_movies_music': 3},
    
    # Night Owl, Messy, Social
    {'q1_sleep': 5, 'q2_tidy': 2, 'q3_noise': 4, 'q4_friends_freq': 4, 'q5_friday_pref': 5, 
     'q6_overnight_guests': 4, 'q7_conflict_style': 4, 'q8_alone_time': 2, 'q9_sports_games': 4, 'q10_movies_music': 5},
    
    # Moderate Morning Person, Organized, Balanced
    {'q1_sleep': 2, 'q2_tidy': 4, 'q3_noise': 3, 'q4_friends_freq': 3, 'q5_friday_pref': 2, 
     'q6_overnight_guests': 2, 'q7_conflict_style': 3, 'q8_alone_time': 3, 'q9_sports_games': 3, 'q10_movies_music': 4},
    
    # Party Person, Outgoing
    {'q1_sleep': 4, 'q2_tidy': 2, 'q3_noise': 5, 'q4_friends_freq': 5, 'q5_friday_pref': 5, 
     'q6_overnight_guests': 5, 'q7_conflict_style': 4, 'q8_alone_time': 1, 'q9_sports_games': 5, 'q10_movies_music': 5},
    
    # Studious, Introverted
    {'q1_sleep': 2, 'q2_tidy': 5, 'q3_noise': 1, 'q4_friends_freq': 1, 'q5_friday_pref': 1, 
     'q6_overnight_guests': 1, 'q7_conflict_style': 1, 'q8_alone_time': 5, 'q9_sports_games': 1, 'q10_movies_music': 3},
    
    # Athletic, Team Player
    {'q1_sleep': 2, 'q2_tidy': 3, 'q3_noise': 3, 'q4_friends_freq': 4, 'q5_friday_pref': 4, 
     'q6_overnight_guests': 3, 'q7_conflict_style': 5, 'q8_alone_time': 2, 'q9_sports_games': 5, 'q10_movies_music': 3},
    
    # Creative, Flexible
    {'q1_sleep': 4, 'q2_tidy': 2, 'q3_noise': 4, 'q4_friends_freq': 3, 'q5_friday_pref': 3, 
     'q6_overnight_guests': 3, 'q7_conflict_style': 2, 'q8_alone_time': 3, 'q9_sports_games': 2, 'q10_movies_music': 5},
    
    # Balanced, Mature
    {'q1_sleep': 3, 'q2_tidy': 4, 'q3_noise': 3, 'q4_friends_freq': 3, 'q5_friday_pref': 3, 
     'q6_overnight_guests': 2, 'q7_conflict_style': 4, 'q8_alone_time': 3, 'q9_sports_games': 3, 'q10_movies_music': 4}
]

class StudentDataGenerator:
    """Generates realistic student data for testing purposes"""
    
    def __init__(self, api_url: str = API_BASE_URL):
        self.api_url = api_url
        self.created_students = []
        self.used_student_ids = set()
        
    def generate_student_id(self) -> str:
        """Generate a unique student ID"""
        while True:
            student_id = f"STU{random.randint(1000, 9999)}"
            if student_id not in self.used_student_ids:
                self.used_student_ids.add(student_id)
                return student_id
    
    def generate_phone_number(self) -> str:
        """Generate a random phone number"""
        format_template = random.choice(PHONE_FORMATS)
        return format_template.format(random.randint(100, 999), random.randint(1000, 9999))
    
    def generate_student_data(self) -> Dict:
        """Generate a single student's data"""
        gender = random.choice(['Male', 'Female', 'Other'])
        first_name = random.choice(FIRST_NAMES[gender])
        last_name = random.choice(LAST_NAMES)
        name = f"{first_name} {last_name}"
        
        # Generate email
        email_name = f"{first_name.lower()}.{last_name.lower()}"
        university = random.choice(UNIVERSITIES)
        email = f"{email_name}@{university}"
        
        # Generate student ID
        student_id = self.generate_student_id()
        
        # Contact info
        contact_info = self.generate_phone_number()
        
        # Room preferences
        prefers_ac = random.choice([True, False])
        room_capacity = random.choices([1, 2, 3, 4], weights=[10, 60, 25, 5])[0]  # Weighted towards doubles
        smoker_okay = random.choices([True, False], weights=[20, 80])[0]  # 20% okay with smokers
        
        # Personality (choose from profiles with some variation)
        base_profile = random.choice(PERSONALITY_PROFILES)
        personality = {}
        
        for key, base_value in base_profile.items():
            # Add slight variation (±1) but keep within 1-5 range
            variation = random.randint(-1, 1)
            personality[key] = max(1, min(5, base_value + variation))
        
        # Self description (70% chance of having one)
        self_description = random.choice(SELF_DESCRIPTIONS) if random.random() < 0.7 else ""
        
        student_data = {
            "name": name,
            "student_id": student_id,
            "contact_info": contact_info,
            "email": email,
            "prefers_ac": prefers_ac,
            "room_capacity": room_capacity,
            "gender": gender,
            "smoker_okay": smoker_okay,
            "self_description": self_description,
            **personality
        }
        
        return student_data
    
    def create_student_via_api(self, student_data: Dict) -> bool:
        """Submit student data to the API"""
        try:
            response = requests.post(
                f"{self.api_url}/students",
                json=student_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f" Created student: {student_data['name']} (ID: {student_data['student_id']})")
                self.created_students.append(student_data)
                return True
            else:
                error_detail = response.json().get('detail', 'Unknown error') if response.status_code != 500 else 'Server error'
                print(f" Failed to create student {student_data['name']}: {error_detail}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f" Network error creating student {student_data['name']}: {str(e)}")
            return False
        except Exception as e:
            print(f" Unexpected error creating student {student_data['name']}: {str(e)}")
            return False
    
    def generate_and_create_students(self, count: int = NUM_STUDENTS) -> None:
        """Generate and create multiple students"""
        print(f" Starting generation of {count} test students...")
        print(f" API URL: {self.api_url}")
        print("-" * 60)
        
        successful_creations = 0
        
        for i in range(count):
            student_data = self.generate_student_data()
            
            if self.create_student_via_api(student_data):
                successful_creations += 1
            
            # Small delay to avoid overwhelming the API
            time.sleep(0.2)
        
        print("-" * 60)
        print(f" Generation complete!")
        print(f" Successfully created: {successful_creations}/{count} students")
        
        if successful_creations > 0:
            self.print_summary()
    
    def print_summary(self) -> None:
        """Print a summary of created students"""
        if not self.created_students:
            return
            
        print("\n STUDENT SUMMARY:")
        print("-" * 60)
        
        # Gender distribution
        gender_counts = {}
        room_capacity_counts = {}
        ac_preference_counts = {'AC': 0, 'Non-AC': 0}
        
        for student in self.created_students:
            # Gender
            gender = student['gender']
            gender_counts[gender] = gender_counts.get(gender, 0) + 1
            
            # Room capacity
            capacity = student['room_capacity']
            room_capacity_counts[capacity] = room_capacity_counts.get(capacity, 0) + 1
            
            # AC preference
            if student['prefers_ac']:
                ac_preference_counts['AC'] += 1
            else:
                ac_preference_counts['Non-AC'] += 1
        
        print(f" Gender Distribution:")
        for gender, count in gender_counts.items():
            print(f"   {gender}: {count}")
        
        print(f"\n Room Capacity Preferences:")
        for capacity, count in sorted(room_capacity_counts.items()):
            print(f"   {capacity} people: {count}")
        
        print(f"\n AC Preferences:")
        for pref, count in ac_preference_counts.items():
            print(f"   {pref}: {count}")
        
        # Personality insights
        avg_sleep = sum(s['q1_sleep'] for s in self.created_students) / len(self.created_students)
        avg_tidy = sum(s['q2_tidy'] for s in self.created_students) / len(self.created_students)
        avg_social = sum(s['q4_friends_freq'] for s in self.created_students) / len(self.created_students)
        
        print(f"\n Average Personality Scores (1-5 scale):")
        print(f"   Sleep Schedule (1=Early, 5=Night): {avg_sleep:.1f}")
        print(f"   Tidiness (1=Messy, 5=Neat): {avg_tidy:.1f}")
        print(f"   Social Level (1=Quiet, 5=Social): {avg_social:.1f}")
    
    def check_api_connection(self) -> bool:
        """Test if the API is accessible"""
        try:
            response = requests.get(f"{self.api_url.replace('/api', '')}/", timeout=5)
            if response.status_code == 200:
                print(" API connection successful")
                return True
            else:
                print(f" API responded with status {response.status_code}")
                return False
        except Exception as e:
            print(f" Cannot connect to API: {str(e)}")
            print(" Make sure the backend server is running on http://localhost:8000")
            return False

def main():
    """Main function"""
    print(" Smart Roomie Test Data Generator")
    print("=" * 60)
    
    generator = StudentDataGenerator()
    
    # Check API connection first
    if not generator.check_api_connection():
        print("\n Cannot proceed without API connection")
        print(" To start the backend:")
        print("   1. cd smart-roomie/backend")
        print("   2. source smartroomie-env/bin/activate  # or smartroomie-env\\Scripts\\activate on Windows")
        print("   3. uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload")
        return
    
    # Generate students
    try:
        generator.generate_and_create_students(NUM_STUDENTS)
        
        print(f"\n Next Steps:")
        print(f"   1. Open your student portal to see the updated student count")
        print(f"   2. Use the admin dashboard to view all created students")
        print(f"   3. Generate matches to see the compatibility algorithm in action!")
        
    except KeyboardInterrupt:
        print(f"\n Generation stopped by user")
        print(f" Successfully created {len(generator.created_students)} students before stopping")
    
    except Exception as e:
        print(f"\n Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()