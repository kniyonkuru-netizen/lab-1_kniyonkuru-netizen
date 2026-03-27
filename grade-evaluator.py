import csv
import sys
import os

def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists, 
    and extracts all fields into a list of dictionaries.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ")

    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
        
    assignments = []
    
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                assignments.append({
                    'assignment': row['assignment'],
                    'group': row['group'],
                    'score': float(row['score']),
                    'weight': float(row['weight'])
                })
        return assignments
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)


def evaluate_grades(data):
    """
    Evaluates grades based on assignment rules.
    """
    print("\n--- Processing Grades ---")

    total_weight = 0
    formative_weight = 0
    summative_weight = 0

    formative_total = 0
    summative_total = 0

    formative_scores_weight = 0
    summative_scores_weight = 0

    failed_formatives = []

    # --- Grade Validation ---
    for item in data:
        score = item['score']
        weight = item['weight']
        group = item['group'].lower()

        if score < 0 or score > 100:
            print(f"Invalid score for {item['assignment']}. Score must be between 0 and 100.")
            sys.exit(1)

        total_weight += weight

        if group == "formative":
            formative_weight += weight
            formative_total += score * weight
            formative_scores_weight += weight

            if score < 50:
                failed_formatives.append(item)

        elif group == "summative":
            summative_weight += weight
            summative_total += score * weight
            summative_scores_weight += weight

    # --- Weight Validation ---
    if total_weight != 100:
        print("Error: Total assignment weights must equal 100.")
        sys.exit(1)

    if formative_weight != 60:
        print("Error: Formative assignments must total 60 weight.")
        sys.exit(1)

    if summative_weight != 40:
        print("Error: Summative assignments must total 40 weight.")
        sys.exit(1)

    # --- Calculate category percentages ---
    formative_percentage = formative_total / formative_scores_weight
    summative_percentage = summative_total / summative_scores_weight

    # --- Final Grade ---
    total_grade = formative_total + summative_total

    # --- GPA Calculation ---
    gpa = (total_grade / 100) * 5.0

    print(f"\nFormative Score: {formative_percentage:.2f}%")
    print(f"Summative Score: {summative_percentage:.2f}%")
    print(f"Total Grade: {total_grade:.2f}")
    print(f"GPA: {gpa:.2f}")

    # --- Pass/Fail Decision ---
    if formative_percentage >= 50 and summative_percentage >= 50:
        print("\nFinal Status: PASSED")
    else:
        print("\nFinal Status: FAILED")

        # --- Resubmission Logic ---
        if failed_formatives:
            max_weight = max(a['weight'] for a in failed_formatives)

            resubmit = [a for a in failed_formatives if a['weight'] == max_weight]

            print("\nAssignment(s) eligible for resubmission:")
            for a in resubmit:
                print(f"- {a['assignment']} (Weight: {a['weight']})")
        else:
            print("No formative assignments eligible for resubmission.")


if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()
    
    # 2. Process the features
    evaluate_grades(course_data)