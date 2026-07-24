#!/usr/bin/env python3
"""
Student Grade Calculator
------------------------
An interactive command-line tool that:
  * Collects scores for as many students as you like
  * Supports weighted categories (e.g. Exams 50%, Homework 30%, Quizzes 20%)
  * Assigns plus/minus letter grades (A+, A, A-, ... , F)
  * Reports each student's percentage, letter grade, and GPA points
  * Prints a class summary at the end
"""

# ---- Grade scale (plus/minus) -------------------------------------------------
# Each tuple: (minimum percentage, letter, GPA points)
GRADE_SCALE = [
    (97, "A+", 4.0),
    (93, "A",  4.0),
    (90, "A-", 3.7),
    (87, "B+", 3.3),
    (83, "B",  3.0),
    (80, "B-", 2.7),
    (77, "C+", 2.3),
    (73, "C",  2.0),
    (70, "C-", 1.7),
    (67, "D+", 1.3),
    (63, "D",  1.0),
    (60, "D-", 0.7),
    (0,  "F",  0.0),
]


def letter_and_points(percent):
    """Return (letter, gpa_points) for a given percentage."""
    for minimum, letter, points in GRADE_SCALE:
        if percent >= minimum:
            return letter, points
    return "F", 0.0


# ---- Input helpers ------------------------------------------------------------
def ask_float(prompt, lo=None, hi=None):
    """Prompt until the user enters a valid number within optional bounds."""
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
        except ValueError:
            print("  Please enter a number.")
            continue
        if lo is not None and value < lo:
            print(f"  Value must be at least {lo}.")
            continue
        if hi is not None and value > hi:
            print(f"  Value must be at most {hi}.")
            continue
        return value


def yes_no(prompt):
    while True:
        ans = input(prompt).strip().lower()
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        print("  Please answer y or n.")


# ---- Category setup -----------------------------------------------------------
def setup_categories():
    """Let the user define weighted categories or fall back to a simple average."""
    print("\nWould you like to use weighted categories")
    print("(e.g. Exams 50%, Homework 30%, Quizzes 20%)?")
    if not yes_no("Enter y for weighted, n for a simple average: "):
        return None  # signals simple-average mode

    categories = []
    total_weight = 0.0
    print("\nDefine your categories. Weights should add up to 100.")
    while True:
        name = input("  Category name (blank to finish): ").strip()
        if not name:
            if not categories:
                print("  Add at least one category.")
                continue
            break
        weight = ask_float(f"  Weight for '{name}' (%): ", lo=0, hi=100)
        categories.append({"name": name, "weight": weight})
        total_weight += weight
        print(f"    (running total weight: {total_weight:.0f}%)")

    if abs(total_weight - 100) > 0.01:
        print(f"\nNote: weights total {total_weight:.0f}%. "
              "Scores will be normalized to this total.")
    return categories


# ---- Score collection ---------------------------------------------------------
def score_for_student(name, categories):
    """Compute a student's overall percentage."""
    if categories is None:
        # Simple average of an arbitrary number of scores
        print(f"  Enter {name}'s scores. Press enter on a blank line to finish.")
        scores = []
        while True:
            raw = input(f"    Score #{len(scores) + 1} (0-100, blank to finish): ").strip()
            if not raw:
                if scores:
                    break
                print("      Enter at least one score.")
                continue
            try:
                val = float(raw)
            except ValueError:
                print("      Please enter a number.")
                continue
            if not 0 <= val <= 100:
                print("      Score must be between 0 and 100.")
                continue
            scores.append(val)
        return sum(scores) / len(scores)

    # Weighted mode
    weighted_sum = 0.0
    total_weight = 0.0
    for cat in categories:
        pct = ask_float(f"    {name} - {cat['name']} score (0-100): ", lo=0, hi=100)
        weighted_sum += pct * cat["weight"]
        total_weight += cat["weight"]
    return weighted_sum / total_weight if total_weight else 0.0


def collect_students(categories):
    students = []
    print("\n--- Enter students ---")
    while True:
        name = input("Student name (blank to finish): ").strip()
        if not name:
            if students:
                break
            print("  Add at least one student.")
            continue
        percent = score_for_student(name, categories)
        letter, points = letter_and_points(percent)
        students.append({
            "name": name,
            "percent": percent,
            "letter": letter,
            "points": points,
        })
        print(f"  => {name}: {percent:.1f}%  {letter}  ({points:.1f} GPA)\n")
    return students


# ---- Reporting ----------------------------------------------------------------
def print_report(students):
    print("\n" + "=" * 46)
    print("               CLASS REPORT")
    print("=" * 46)
    print(f"{'Student':<20}{'Percent':>9}{'Grade':>8}{'GPA':>7}")
    print("-" * 46)
    for s in students:
        print(f"{s['name']:<20}{s['percent']:>8.1f}%{s['letter']:>8}{s['points']:>7.1f}")
    print("-" * 46)

    avg_pct = sum(s["percent"] for s in students) / len(students)
    avg_gpa = sum(s["points"] for s in students) / len(students)
    top = max(students, key=lambda s: s["percent"])
    print(f"{'Class average':<20}{avg_pct:>8.1f}%{'':>8}{avg_gpa:>7.2f}")
    print(f"Top student: {top['name']} ({top['percent']:.1f}%, {top['letter']})")
    print("=" * 46)


# ---- Main ---------------------------------------------------------------------
def main():
    print("=" * 46)
    print("        STUDENT GRADE CALCULATOR")
    print("=" * 46)
    categories = setup_categories()
    students = collect_students(categories)
    print_report(students)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting. Goodbye!")
