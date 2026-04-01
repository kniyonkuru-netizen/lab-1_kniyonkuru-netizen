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
                # Convert numeric fields to floats for calculations
                assignments.append({
                    'assignment': row['assignment'],
                    'group': row['group'],
                    'score': float(row['score']),
                    'weight': float(row['weight'])
                })
        if not assignments:
            print(f"Error: The file '{filename}' is empty or contains no grade records.")
            sys.exit(1)
        return assignments
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

def evaluate_grades(data):
    """
    Evaluates a student's grades based on weighted scores.
    """
    print("\n--- Processing Grades ---")

    
    #  Grade Validation: all scores must be between 0 and 100
   
    invalid_scores = [a for a in data if not (0 <= a['score'] <= 100)]
    if invalid_scores:
        print("\n[ERROR] The following assignments have invalid scores (must be 0-100):")
        for a in invalid_scores:
            print(f"  - {a['assignment']}: {a['score']}")
        sys.exit(1)
    print("[OK] All scores are valid (0-100).")

    
    #  Weight Validation: total=100, Summative=40, Formative=60
    
    total_weight     = sum(a['weight'] for a in data)
    summative_weight = sum(a['weight'] for a in data if a['group'] == 'Summative')
    formative_weight = sum(a['weight'] for a in data if a['group'] == 'Formative')

    weight_errors = []
    if round(total_weight, 2) != 100:
        weight_errors.append(f"  - Total weights sum to {total_weight} (expected 100).")
    if round(summative_weight, 2) != 40:
        weight_errors.append(f"  - Summative weights sum to {summative_weight} (expected 40).")
    if round(formative_weight, 2) != 60:
        weight_errors.append(f"  - Formative weights sum to {formative_weight} (expected 60).")

    if weight_errors:
        print("\n[ERROR] Weight validation failed:")
        for err in weight_errors:
            print(err)
        sys.exit(1)
    print("[OK] All weights are valid (Total=100, Summative=40, Formative=60).")

    
    #  GPA Calculation
    #    Weighted grade per assignment = (score * weight) / 100
    #    Final Grade = sum of all weighted grades
    #    GPA = (Final Grade / 100) * 5.0
    
    summative_assignments = [a for a in data if a['group'] == 'Summative']
    formative_assignments = [a for a in data if a['group'] == 'Formative']

    # Weighted average per category (scaled to the category's total weight)
    summative_grade = sum((a['score'] * a['weight']) / 100 for a in summative_assignments)
    formative_grade = sum((a['score'] * a['weight']) / 100 for a in formative_assignments)

    final_grade = summative_grade + formative_grade
    gpa = (final_grade / 100) * 5.0

    print(f"\n--- Grade Summary ---")
    print(f"  Summative Grade : {summative_grade:.2f} / 40")
    print(f"  Formative Grade : {formative_grade:.2f} / 60")
    print(f"  Final Grade     : {final_grade:.2f}%")
    print(f"  GPA             : {gpa:.3f} / 5.0")

    
    #  Pass/Fail: student must score >= 50% in BOTH categories
    #    Summative pass threshold : 50% of 40 = 20
    #    Formative pass threshold : 50% of 60 = 30
    
    summative_pass = summative_grade >= 20   # which is 50% of 40
    formative_pass = formative_grade >= 30   # which is 50% of 60
    overall_pass   = summative_pass and formative_pass

    
    #  Resubmission Logic
    #    - Only applies to Formative assignments with score < 50
    #    - Find the highest weight among those failed ones
    #    - Flag ALL that share that highest weight
    
    failed_formative = [a for a in formative_assignments if a['score'] < 50]
    resubmission_candidates = []

    if failed_formative:
        highest_weight = max(a['weight'] for a in failed_formative)
        resubmission_candidates = [a for a in failed_formative if a['weight'] == highest_weight]

    
    # f) Final Output
    
    print(f"\n--- Final Decision ---")

    if overall_pass:
        print("  Status: PASSED")
    else:
        print("  Status: FAILED")
        if not summative_pass:
            print(f"  Reason: Summative grade ({summative_grade:.3f}) is below the passing threshold of 20.00.")
        if not formative_pass:
            print(f"  Reason: Formative grade ({formative_grade:.3f}) is below the passing threshold of 30.00.")

    if resubmission_candidates:
        print(f"\n--- Resubmission Eligible ---")
        print(f"  The following formative assignment(s) failed and carry the highest weight ({highest_weight}):")
        for a in resubmission_candidates:
            print(f"  - {a['assignment']} (Score: {a['score']}, Weight: {a['weight']})")
    else:
        print("\n  No formative assignments are eligible for resubmission.")


if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()
    
    # 2. Process the features
    evaluate_grades(course_data)