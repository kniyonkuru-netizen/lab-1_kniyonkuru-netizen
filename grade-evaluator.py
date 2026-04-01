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

    # Handle empty file (freshly reset by organizer.sh)
    if os.path.getsize(filename) == 0:
        print(f"Error: The file '{filename}' is empty.")
        print("Hint: The workspace may have just been reset by organizer.sh.")
        print("Please populate grades.csv with data before running the evaluator.")
        sys.exit(1)

    assignments = []

    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            # Validate required headers exist
            required = {'assignment', 'group', 'score', 'weight'}
            if not required.issubset(set(reader.fieldnames or [])):
                print(f"Error: Missing required columns.")
                print(f"  Expected : {required}")
                print(f"  Found    : {set(reader.fieldnames or [])}")
                sys.exit(1)

            for i, row in enumerate(reader, start=2):
                try:
                    assignments.append({
                        'assignment': row['assignment'].strip(),
                        'group':      row['group'].strip(),
                        'score':      float(row['score']),
                        'weight':     float(row['weight'])
                    })
                except ValueError:
                    print(f"Error: Row {i} has an invalid score or weight: {dict(row)}")
                    sys.exit(1)

        if not assignments:
            print(f"Error: '{filename}' contains headers but no data rows.")
            sys.exit(1)

        return assignments

    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)


# ─────────────────────────────────────────────────────────────
#  FEATURE 1 — Grade Validation
# ─────────────────────────────────────────────────────────────
def validate_grades(data):
    """Check that every score is between 0 and 100."""
    errors = []
    for item in data:
        if not (0 <= item['score'] <= 100):
            errors.append(
                f"  '{item['assignment']}' has score {item['score']} "
                f"(must be between 0 and 100)."
            )
    if errors:
        print("\n[VALIDATION ERROR] Invalid scores detected:")
        for e in errors:
            print(e)
        sys.exit(1)
    print("  [OK] All scores are within valid range (0-100).")


# ─────────────────────────────────────────────────────────────
#  FEATURE 2 — Weight Validation
# ─────────────────────────────────────────────────────────────
def validate_weights(data):
    """
    Verify:
      - Total weights == 100
      - Summative weights == 40
      - Formative weights == 60
    """
    total_w     = sum(i['weight'] for i in data)
    summative_w = sum(i['weight'] for i in data if i['group'].lower() == 'summative')
    formative_w = sum(i['weight'] for i in data if i['group'].lower() == 'formative')

    errors = []
    if round(total_w, 2) != 100.0:
        errors.append(f"  Total weight = {total_w:.2f} (expected 100.00).")
    if round(summative_w, 2) != 40.0:
        errors.append(f"  Summative weight = {summative_w:.2f} (expected 40.00).")
    if round(formative_w, 2) != 60.0:
        errors.append(f"  Formative weight = {formative_w:.2f} (expected 60.00).")

    if errors:
        print("\n[VALIDATION ERROR] Weight validation failed:")
        for e in errors:
            print(e)
        sys.exit(1)
    print("  [OK] Weights valid — Total: 100 | Summative: 40 | Formative: 60.")


# ─────────────────────────────────────────────────────────────
#  FEATURE 3 — GPA Calculation
# ─────────────────────────────────────────────────────────────
def calculate_gpa(data):
    """
    Total Grade = sum(score * weight / 100) across all assignments
    GPA         = (Total Grade / 100) * 5.0

    Category averages use weighted mean within each group.
    """
    total_grade = sum(i['score'] * (i['weight'] / 100) for i in data)

    summative_items = [i for i in data if i['group'].lower() == 'summative']
    formative_items = [i for i in data if i['group'].lower() == 'formative']

    def weighted_avg(items):
        total_w = sum(i['weight'] for i in items)
        return sum(i['score'] * i['weight'] for i in items) / total_w if total_w else 0.0

    summative_score = weighted_avg(summative_items)
    formative_score = weighted_avg(formative_items)
    gpa             = (total_grade / 100) * 5.0

    return total_grade, gpa, summative_score, formative_score


# ─────────────────────────────────────────────────────────────
#  FEATURE 4 — Final Decision (Pass / Fail)
# ─────────────────────────────────────────────────────────────
def final_decision(summative_score, formative_score):
    """
    Student PASSES only if BOTH categories are >= 50%.
    A high overall average does NOT override a failing category.
    """
    if summative_score >= 50 and formative_score >= 50:
        return "PASSED"
    return "FAILED"


# ─────────────────────────────────────────────────────────────
#  FEATURE 5 — Resubmission Logic
# ─────────────────────────────────────────────────────────────
def resubmission_logic(data):
    """
    - Only Formative assignments with score < 50 are eligible.
    - Among those, find the one(s) with the highest weight.
    - If multiple share the same highest weight, return ALL of them.
    """
    failed_formative = [
        i for i in data
        if i['group'].lower() == 'formative' and i['score'] < 50
    ]
    if not failed_formative:
        return []

    max_weight = max(i['weight'] for i in failed_formative)
    return [i for i in failed_formative if i['weight'] == max_weight]


# ─────────────────────────────────────────────────────────────
#  MAIN EVALUATE FUNCTION
# ─────────────────────────────────────────────────────────────
def evaluate_grades(data):
    """
    Runs all features and prints the final transcript.
    """
    print("\n--- Processing Grades ---\n")

    validate_grades(data)    # Feature 1
    validate_weights(data)   # Feature 2

    total_grade, gpa, summative_score, formative_score = calculate_gpa(data)  # Feature 3
    status   = final_decision(summative_score, formative_score)                # Feature 4
    resubmit = resubmission_logic(data)                                        # Feature 5

    # ── Print Transcript ──────────────────────────────────────
    print("\n" + "=" * 60)
    print("             STUDENT GRADE TRANSCRIPT")
    print("=" * 60)

    print(f"\n  {'Assignment':<28} {'Group':<12} {'Score':>6}  {'Weight':>7}")
    print("  " + "-" * 56)
    for item in data:
        print(
            f"  {item['assignment']:<28} {item['group']:<12}"
            f" {item['score']:>6.1f}  {item['weight']:>6.1f}%"
        )

    print("\n  " + "-" * 56)
    print(f"  {'Summative Average Score':<32} : {summative_score:.2f}%")
    print(f"  {'Formative Average Score':<32} : {formative_score:.2f}%")
    print(f"  {'Total Weighted Grade':<32} : {total_grade:.2f}%")
    print(f"  {'GPA  ( ' + f'{total_grade:.2f}/100 x 5.0 )':<32} : {gpa:.2f} / 5.0")

    print("\n  " + "-" * 56)
    print(f"  Final Status  :  >>> {status} <<<")
    print("  " + "-" * 56)

    # Resubmission section
    if resubmit:
        print("\n  Eligible for Resubmission:")
        print("  (Failed Formative assignment(s) with the highest weight)\n")
        for item in resubmit:
            print(
                f"    ->  {item['assignment']:<28}"
                f"  Score: {item['score']:.1f}%   Weight: {item['weight']:.1f}%"
            )
    else:
        if status == "PASSED":
            print("\n  No resubmission required.")
        else:
            print("\n  No failed Formative assignments found — review Summative scores.")

    print("=" * 60 + "\n")


# ─────────────────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    data = load_csv_data()
    evaluate_grades(data)