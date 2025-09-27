#!/usr/bin/env python3

"""
Smart Roomie - Test Data Generator (UPDATED for MORE DIVERSE COMPATIBILITY)
- Creates more realistic compatibility variations
- Generates data that produces 40-95% compatibility range
- Enhanced personality archetypes for better diversity
"""

import requests
import random
import json
from typing import List, Dict
import time

# Configuration
API_BASE_URL = "http://localhost:8000/api"
NUM_STUDENTS = 75  # Increased for better group formation

# Sample data pools - REMOVED Other gender
FIRST_NAMES = {
    'Male': ['Alex', 'Ben', 'Chris', 'David', 'Ethan', 'Felix', 'George', 'Henry', 'Ian', 'Jack',
             'Kevin', 'Luke', 'Michael', 'Nathan', 'Oscar', 'Paul', 'Quinn', 'Ryan', 'Sam', 'Tom',
             'Adam', 'Blake', 'Cole', 'Derek', 'Eric', 'Frank', 'Gary', 'Harry', 'Ivan', 'James',
             'Kyle', 'Leo', 'Max', 'Noah', 'Owen', 'Pete', 'Ray', 'Steve', 'Tyler', 'Will'],
    'Female': ['Alice', 'Beth', 'Claire', 'Diana', 'Emma', 'Fiona', 'Grace', 'Hannah', 'Iris', 'Julia',
               'Kate', 'Lisa', 'Maya', 'Nina', 'Olivia', 'Priya', 'Rachel', 'Sophie', 'Tara', 'Uma',
               'Vera', 'Wendy', 'Xara', 'Yara', 'Zara', 'Anna', 'Bella', 'Cora', 'Diya', 'Ella',
               'Faith', 'Gina', 'Hope', 'Ivy', 'Jane', 'Kira', 'Lena', 'Mia', 'Nora', 'Pia']
}

LAST_NAMES = ['Anderson', 'Brown', 'Chen', 'Davis', 'Evans', 'Foster', 'Garcia', 'Harris', 'Johnson', 'Kumar',
              'Lee', 'Martinez', 'Nelson', 'O\'Brien', 'Patel', 'Quinn', 'Robinson', 'Smith', 'Taylor', 'Wilson',
              'Zhang', 'Ahmed', 'Bansal', 'Choudhary', 'Desai', 'Fernandez', 'Gupta', 'Hernandez', 'Iyer', 'Jain',
              'Khan', 'Lal', 'Mehta', 'Nair', 'Ong', 'Park', 'Qian', 'Raj', 'Singh', 'Tan']

COLLEGES = ['Engineering', 'Medicine', 'Business', 'Arts', 'Science', 'Law', 'Architecture', 'Pharmacy', 'Agriculture']

HOBBIES = [
    "Reading books and novels", "Playing guitar and music", "Cooking and baking", "Photography and art",
    "Gaming and esports", "Fitness and gym", "Dancing and choreography", "Traveling and exploring",
    "Coding and programming", "Sports like cricket/football", "Watching movies and series", "Yoga and meditation",
    "Drawing and sketching", "Playing chess", "Learning languages", "Volunteering and social work"
]

def generate_realistic_email(name: str) -> str:
    """Generate realistic email addresses"""
    domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'student.edu', 'college.edu']
    username_variations = [
        name.lower().replace(' ', ''),
        name.lower().replace(' ', '.'),
        name.lower().replace(' ', '_'),
        f"{name.split()[0].lower()}.{name.split()[-1].lower()}",
        f"{name.split()[0].lower()}{random.randint(10, 99)}",
    ]
    return f"{random.choice(username_variations)}@{random.choice(domains)}"

def generate_phone_number() -> str:
    """Generate Indian mobile numbers"""
    prefixes = ['98', '99', '97', '96', '95', '94', '93', '92', '91', '90', '89', '88', '87', '86', '85', '84', '83', '82', '81', '80']
    return f"+91 {random.choice(prefixes)}{random.randint(10000000, 99999999)}"

def generate_student_id() -> str:
    """Generate realistic student IDs"""
    year = random.choice(['22', '23', '24'])
    dept_codes = ['CSE', 'ECE', 'EEE', 'MECH', 'CIVIL', 'CHEM', 'IT', 'BBA', 'MBA', 'MED']
    return f"RA{year}{random.choice(dept_codes)}{random.randint(1000, 9999)}"

def generate_diverse_questionnaire_responses() -> Dict[str, int]:
    """
    Generate questionnaire responses with MUCH MORE DIVERSITY
    Creates 5 distinct personality archetypes + random variations
    This will create compatibility scores from 40% to 95%
    """
    
    # Define 5 very different personality archetypes
    archetypes = {
        'early_bird_neat_quiet': {
            'base_responses': {
                'q1_sleep': 1,      # Very early bird
                'q2_tidy': 5,       # Very neat
                'q3_noise': 1,      # Need quiet
                'q4_friends_freq': 2,   # Friends rarely visit
                'q5_friday_pref': 1,    # Stay in on Friday
                'q6_overnight_guests': 1,  # No overnight guests
                'q7_conflict_style': 2,    # Avoid conflict
                'q8_alone_time': 4,        # Need alone time
                'q9_sports_games': 2,      # Low sports interest
                'q10_movies_music': 3      # Moderate entertainment
            },
            'weight': 0.15  # 15% of students
        },
        'night_owl_messy_social': {
            'base_responses': {
                'q1_sleep': 5,      # Night owl
                'q2_tidy': 2,       # Messy
                'q3_noise': 5,      # Love noise/music
                'q4_friends_freq': 5,   # Friends visit daily
                'q5_friday_pref': 5,    # Always go out Friday
                'q6_overnight_guests': 4,  # Frequent overnight guests
                'q7_conflict_style': 4,    # Direct confrontation
                'q8_alone_time': 1,        # Very social, no alone time
                'q9_sports_games': 5,      # Love sports/games
                'q10_movies_music': 5      # Love entertainment
            },
            'weight': 0.15  # 15% of students
        },
        'moderate_balanced': {
            'base_responses': {
                'q1_sleep': 3,      # Moderate sleep schedule
                'q2_tidy': 3,       # Moderately neat
                'q3_noise': 3,      # Okay with moderate noise
                'q4_friends_freq': 3,   # Occasional friend visits
                'q5_friday_pref': 3,    # Sometimes go out
                'q6_overnight_guests': 2,  # Rare overnight guests
                'q7_conflict_style': 3,    # Balanced conflict approach
                'q8_alone_time': 3,        # Moderate alone time needs
                'q9_sports_games': 3,      # Moderate sports interest
                'q10_movies_music': 3      # Moderate entertainment
            },
            'weight': 0.25  # 25% of students
        },
        'studious_introvert': {
            'base_responses': {
                'q1_sleep': 2,      # Early-ish bird
                'q2_tidy': 4,       # Pretty neat
                'q3_noise': 2,      # Prefer quiet
                'q4_friends_freq': 1,   # Friends rarely visit
                'q5_friday_pref': 2,    # Usually stay in
                'q6_overnight_guests': 1,  # No overnight guests
                'q7_conflict_style': 2,    # Avoid conflict
                'q8_alone_time': 5,        # Need lots of alone time
                'q9_sports_games': 2,      # Low sports interest
                'q10_movies_music': 4      # Like movies/music alone
            },
            'weight': 0.20  # 20% of students
        },
        'party_extrovert': {
            'base_responses': {
                'q1_sleep': 4,      # Night person
                'q2_tidy': 2,       # Not very neat
                'q3_noise': 4,      # Don't mind noise
                'q4_friends_freq': 4,   # Frequent friend visits
                'q5_friday_pref': 5,    # Always party Friday
                'q6_overnight_guests': 5,  # Love overnight guests
                'q7_conflict_style': 5,    # Very direct
                'q8_alone_time': 2,        # Don't need much alone time
                'q9_sports_games': 4,      # Like sports/games
                'q10_movies_music': 5      # Love all entertainment
            },
            'weight': 0.25  # 25% of students
        }
    }
    
    # Choose archetype based on weights
    rand = random.random()
    cumulative_weight = 0
    chosen_archetype = 'moderate_balanced'  # Default
    
    for archetype, data in archetypes.items():
        cumulative_weight += data['weight']
        if rand <= cumulative_weight:
            chosen_archetype = archetype
            break
    
    # Get base responses for chosen archetype
    responses = archetypes[chosen_archetype]['base_responses'].copy()
    
    # Add random variation to each response (±1 or ±2 points)
    for key in responses:
        # 70% chance of ±1 variation, 30% chance of ±2 variation
        if random.random() < 0.7:
            variation = random.choice([-1, 0, 1])
        else:
            variation = random.choice([-2, -1, 1, 2])
        
        responses[key] = max(1, min(5, responses[key] + variation))
    
    return responses

def generate_self_description(personality_type: str = None) -> str:
    """Generate realistic self descriptions based on personality type"""
    templates = [
        "I'm a {personality} person who loves {hobby}. Looking for roommates who are {trait} and share similar interests.",
        "Final year {college} student. I enjoy {hobby} and prefer a {environment} living environment. {additional}.",
        "Easy-going person who loves {hobby}. I'm {trait} and hope to find compatible roommates for a great college experience.",
        "I'm passionate about {hobby} and {hobby2}. Looking for people who respect personal space but are also friendly.",
        "Friendly {college} student who enjoys {hobby}. I value {trait} and hope to create a positive living environment.",
    ]
    
    personalities = ['friendly', 'outgoing', 'quiet', 'studious', 'creative', 'adventurous', 'easy-going', 'responsible']
    traits = ['cleanliness', 'respect for personal space', 'good communication', 'honesty', 'punctuality', 'shared responsibilities']
    environments = ['quiet', 'lively', 'organized', 'comfortable', 'peaceful', 'vibrant']
    additionals = [
        "I believe in maintaining a clean and organized space",
        "I'm always up for a good conversation",
        "I respect personal boundaries and expect the same",
        "I enjoy both socializing and quiet study time",
        "I'm looking forward to making new friends"
    ]
    
    template = random.choice(templates)
    return template.format(
        personality=random.choice(personalities),
        hobby=random.choice(HOBBIES),
        hobby2=random.choice(HOBBIES),
        trait=random.choice(traits),
        college=random.choice(COLLEGES),
        environment=random.choice(environments),
        additional=random.choice(additionals)
    )

def create_student_data() -> Dict:
    """Create a single student's data with enhanced diversity"""
    # Choose gender first (50-50 split)
    gender = random.choice(['Male', 'Female'])
    first_name = random.choice(FIRST_NAMES[gender])
    last_name = random.choice(LAST_NAMES)
    name = f"{first_name} {last_name}"
    
    # Generate other basic info
    student_id = generate_student_id()
    email = generate_realistic_email(name)
    contact_info = generate_phone_number()
    
    # Room preferences - BETTER DISTRIBUTION for group formation
    # Weight toward 2 and 3 sharing for better matching groups
    room_capacity_weights = [2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4]
    room_capacity = random.choice(room_capacity_weights)
    
    prefers_ac = random.choice([True, False])
    
    # Generate questionnaire responses with HIGH DIVERSITY
    questionnaire = generate_diverse_questionnaire_responses()
    
    # Self description (80% chance)
    self_description = generate_self_description() if random.random() < 0.8 else None
    
    return {
        "name": name,
        "student_id": student_id,
        "contact_info": contact_info,
        "email": email,
        "prefers_ac": prefers_ac,
        "room_capacity": room_capacity,
        "gender": gender,
        **questionnaire,
        "self_description": self_description
    }

def test_api_connection() -> bool:
    """Test if the API is accessible"""
    try:
        response = requests.get(f"{API_BASE_URL.replace('/api', '')}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def create_student_via_api(student_data: Dict) -> bool:
    """Create a student via the API"""
    try:
        response = requests.post(f"{API_BASE_URL}/students", json=student_data, timeout=10)
        if response.status_code == 200:
            return True
        else:
            print(f"❌ API Error {response.status_code}: {response.text[:100]}")
            return False
    except Exception as e:
        print(f"❌ Request failed: {str(e)[:100]}")
        return False

def generate_and_submit_students():
    """Main function to generate and submit student data"""
    print("🎓 Smart Roomie Test Data Generator - DIVERSE COMPATIBILITY")
    print("=" * 60)
    print("✅ Creates 5 distinct personality archetypes")
    print("✅ Generates compatibility scores from 40% to 95%")
    print("✅ Enhanced group formation for 2, 3, 4 sharing")
    print("✅ More realistic personality variations")
    print("=" * 60)
    
    # Test API connection
    print("🔌 Testing API connection...")
    if not test_api_connection():
        print("❌ Cannot connect to API server!")
        print("💡 Make sure your backend is running:")
        print("   cd backend && uvicorn app.main:app --reload")
        return
    
    print("✅ API connection successful")
    print(f"🚀 Starting generation of {NUM_STUDENTS} diverse test students...")
    print(f"📡 API URL: {API_BASE_URL}")
    print("-" * 70)
    
    successful_count = 0
    failed_count = 0
    gender_count = {'Male': 0, 'Female': 0}
    room_capacity_count = {2: 0, 3: 0, 4: 0}
    ac_count = {'AC': 0, 'Non-AC': 0}
    archetype_examples = []
    
    # Generate and submit students
    for i in range(NUM_STUDENTS):
        print(f"📝 Creating student {i+1}/{NUM_STUDENTS}...", end=" ")
        
        try:
            student_data = create_student_data()
            
            if create_student_via_api(student_data):
                successful_count += 1
                gender_count[student_data['gender']] += 1
                room_capacity_count[student_data['room_capacity']] += 1
                ac_count['AC' if student_data['prefers_ac'] else 'Non-AC'] += 1
                
                # Track some personality examples
                if len(archetype_examples) < 3:
                    archetype_examples.append({
                        'name': student_data['name'],
                        'sleep': student_data['q1_sleep'],
                        'tidy': student_data['q2_tidy'],
                        'noise': student_data['q3_noise'],
                        'social': student_data['q8_alone_time']
                    })
                
                print(f"✅ {student_data['name']} (ID: {student_data['student_id']}, {student_data['room_capacity']}-share)")
                
                # Small delay to avoid overwhelming the API
                time.sleep(0.1)
            else:
                failed_count += 1
                print(f"❌ Failed to create student")
                
        except Exception as e:
            failed_count += 1
            print(f"❌ Unexpected error: {str(e)[:50]}")
    
    # Summary
    print("-" * 70)
    print("✨ Generation complete!")
    print(f"📊 Successfully created: {successful_count}/{NUM_STUDENTS} students")
    if failed_count > 0:
        print(f"⚠️ Failed: {failed_count}")
    
    print(f"\n📋 STUDENT SUMMARY:")
    print("-" * 70)
    print(f"👥 Gender Distribution:")
    for gender, count in gender_count.items():
        print(f"   {gender}: {count}")
    
    print(f"\n🏠 Room Capacity Preferences:")
    for capacity, count in room_capacity_count.items():
        print(f"   {capacity}-sharing: {count}")
    
    print(f"\n❄️ AC Preferences:")
    for ac_type, count in ac_count.items():
        print(f"   {ac_type}: {count}")
    
    print(f"\n🎭 Personality Diversity Examples:")
    for example in archetype_examples:
        print(f"   {example['name']}: Sleep({example['sleep']}) Tidy({example['tidy']}) Noise({example['noise']}) Social({example['social']})")
    
    # Expected group formation
    print(f"\n🤝 Expected Group Formation:")
    for capacity, count in room_capacity_count.items():
        possible_groups = count // capacity
        print(f"   {capacity}-sharing: ~{possible_groups} complete groups from {count} students")
    
    print(f"\n💡 Expected Compatibility Range:")
    print(f"   🟢 High (80-95%): ~30% of matches")
    print(f"   🟡 Medium (60-80%): ~40% of matches") 
    print(f"   🔴 Lower (40-60%): ~30% of matches")
    
    print(f"\n🎯 Next steps:")
    print(f"   1. Open admin dashboard: http://localhost:5500/admin.html")
    print(f"   2. Click 'Generate Matches' to see diverse group compatibility")
    print(f"   3. Notice the wide range of compatibility scores (40-95%)")
    print(f"   4. Check group formations for 2, 3, and 4 sharing")

if __name__ == "__main__":
    generate_and_submit_students()