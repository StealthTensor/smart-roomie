***

# Smart Roomie

This project is called Smart Roomie. It is an app that helps students find and apply for hostel rooms, matching them based on preferences like AC or non-AC rooms. It also has an admin dashboard to manage all the applications and match students to rooms.

## How it works

There are two parts in the project: the backend and the frontend.

- The backend is built with Python. It handles the data part, like saving student details, room preferences, and doing the matching. It uses a database to store all this information.
- The frontend is made of HTML, CSS, and JavaScript. This is what the users see and use to fill out forms or check room availability.

When a student applies, they enter details about themselves and what kind of room they want (AC or non-AC). The backend saves this information and later matches students with available rooms based on their choices.

Admins can log in to a special dashboard to see all applications, assign rooms, and make changes if needed.

## Project structure

```
/smart-roomie
├── backend
│   ├── app
│   │   ├── __init__.py        # Initializes the backend app
│   │   ├── database.py        # Database connection and setup
│   │   ├── main.py            # Main backend server code
│   │   ├── matching.py        # Logic for matching students to rooms
│   │   ├── models.py          # Database models for students, rooms, etc.
│   │   └── requirements.txt   # Python dependencies for backend
│   ├── smartroomie.db         # The database file storing all data
│   └── venv                   # Virtual environment for backend
├── frontend
│   ├── assets
│   │   ├── main.js            # JavaScript for frontend interaction
│   │   └── styles.css         # Styling for the frontend pages
│   ├── index.html             # Main page for students to apply
│   └── admin.html             # Admin dashboard page
├── check_database.py          # Script to check or debug database state
└── generate-test-data.py      # Script to create example data for testing
```

## How to use

1. Clone the project and go to the backend folder.
2. Set up a Python virtual environment and install the required packages.
3. Run the backend server (usually with `uvicorn`).
4. Open the `index.html` file in a browser to start applying.
5. Admins can open `admin.html` to manage applications and assign rooms.

## Why I made this

I made Smart Roomie to make hostel applications easier and faster for students and admins. It helps avoid confusion, saves time, and matches students to the best rooms based on their choices.

***
