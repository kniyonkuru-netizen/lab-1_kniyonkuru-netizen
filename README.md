1. # Grade Evaluator & Organizer

A Python application that calculates a student's final academic standing from a CSV file of course grades, paired with a Bash shell script that archives and resets the workspace.

# Project Structure

lab1_gmweene-wq/
│
├── grade-evaluator.py   # Python grade calculator
├── organizer.sh         # Bash archiving script
├── grades.csv           # CSV file containing course grades
├── organizer.log        # Auto-generated log file (created on first run)
└── archive/             # Auto-generated archive folder (created on first run)

# required software

- *Python3 installed on your machine
- *Bash shell — Git Bash (Windows), Terminal (Mac/Linux), or WSL

# The CSV File Format

The `grades.csv` file must follow this exact structure:
assignment,group,score,weight
   for example:
Quiz,Formative,85,20
Group Exercise,Formative,40,20
Functions and Debugging Lab,Formative,45,20
Midterm Project - Simple Calculator,Summative,70,20
Final Project - Text-Based Game,Summative,60,20

*Rules:
- `score` must be between 0 and 100 (percentage)
- All weights must sum to exactly 100
- Summative weights must sum to exactly 40
- Formative weights must sum to exactly 60
otherwise it becomes an error.

# Running the Python Application (grade-evaluator.py)

# Step 1 — Open your terminal
Navigate to the project folder:
cd path/to/project or press the run button if using VS Code to skip step 2

# Step 2 — Run the script
python3 grade-evaluator.py 

# Step 3 — Enter the filename when prompted
Enter the name of the CSV file to process (e.g., grades.csv): grades.csv

# Expected Output
Based on the above example:

--- Processing Grades ---
[OK] All scores are valid (0-100).
[OK] All weights are valid (Total=100, Summative=40, Formative=60).

--- Grade Summary ---
  Summative Grade : 26.00 / 40
  Formative Grade : 34.00 / 60
  Final Grade     : 60.00%
  GPA             : 3.00 / 5.0

--- Final Decision ---
  Status: PASSED

--- Resubmission Eligible ---
  The following formative assignment(s) failed and carry the highest weight (20.0):
  - Group Exercise (Score: 40.0, Weight: 20.0)
  - Functions and Debugging Lab (Score: 45.0, Weight: 20.0)

# Error Cases
| Situation |       Message |
| File not found | Error: The file 'x.csv' was not found. |
| File is empty | Error: The file 'x.csv' is empty or contains no grade records. |
| Invalid score | [ERROR] The following assignments have invalid scores (must be 0-100) |
| Invalid weights | [ERROR] Weight validation failed |


2. # Running the Shell Script (organizer.sh)

The shell script archives the current `grades.csv`, and creates a fresh empty one for the next batch of grades.

# Step 1 — Make the script executable (first time only)
bash
chmod +x organizer.sh

# Step 2 — Run the script
bash organizer.sh

# Expected Output
Created directory: archive
Archived: grades.csv → archive/grades_20251105-170000.csv
Workspace reset: new empty 'grades.csv' created.
Logged operation to: organizer.log

Done!

# What the organizer.sh does
1. Checks if `grades.csv` exists — exits with an error if not found
2. Creates the `archive/` folder if it does not already exist
3. Renames `grades.csv` by appending the current timestamp (e.g. `grades_20251105-170000.csv`)
4. Moves the renamed file into the `archive/` folder
5. Creates a fresh empty `grades.csv` in the current directory
6. Appends a log entry to `organizer.log`

# The Log File (organizer.log)
Every run appends a new entry — it never overwrites previous ones:

[20251105-170000] Original: grades.csv | Archived as: archive/grades_20251105-170000.csv
[20251105-173000] Original: grades.csv | Archived as: archive/grades_20251105-173000.csv

# Running on Windows (VS Code)
Since Bash is not natively available on Windows, use one of the following:
- *Git Bash — right-click the project folder → "Git Bash Here" → `bash organizer.sh`
- *WSL — open WSL terminal in VS Code and run `bash organizer.sh`
- *Set Git Bash as default in VS Code — `Ctrl+Shift+P` → "Select Default Profile" → Git Bash

# Recommended Workflow

1. Fill in `grades.csv` with the student's grades
2. Run `python3 grade-evaluator.py` to evaluate the grades
3. Run `bash organizer.sh` to archive the CSV and reset the workspace
4. Repeat for the next student