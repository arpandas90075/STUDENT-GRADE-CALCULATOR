#!/usr/bin/env python3
"""
Student Grade Calculator - GUI
A simple desktop app (tkinter). Add subjects and scores, hit Calculate,
and see the average, letter grade (A/B/C/D/F), and pass/fail.
Run:  python grade_calculator_gui.py
"""

import tkinter as tk
from tkinter import ttk, messagebox

# ---- Simple grade scale -------------------------------------------------------
def letter_grade(avg):
    if avg >= 90: return "A"
    if avg >= 80: return "B"
    if avg >= 70: return "C"
    if avg >= 60: return "D"
    return "F"

COLORS = {
    "A": "#16a34a", "B": "#65a30d", "C": "#ca8a04",
    "D": "#ea580c", "F": "#dc2626",
}


class GradeApp:
    def __init__(self, root):
        self.root = root
        root.title("Student Grade Calculator")
        root.geometry("440x560")
        root.configure(bg="#0f172a")
        root.resizable(False, False)

        self.rows = []  # list of (subject_entry, score_entry)

        # Title
        tk.Label(root, text="Grade Calculator", bg="#0f172a", fg="white",
                 font=("Segoe UI", 20, "bold")).pack(pady=(20, 4))
        tk.Label(root, text="Enter each subject and its score (0-100)",
                 bg="#0f172a", fg="#94a3b8",
                 font=("Segoe UI", 10)).pack(pady=(0, 12))

        # Header row
        header = tk.Frame(root, bg="#0f172a")
        header.pack(fill="x", padx=24)
        tk.Label(header, text="Subject", bg="#0f172a", fg="#64748b",
                 font=("Segoe UI", 9, "bold"), width=22, anchor="w").pack(side="left")
        tk.Label(header, text="Score", bg="#0f172a", fg="#64748b",
                 font=("Segoe UI", 9, "bold")).pack(side="left")

        # Scrollable rows area
        self.rows_frame = tk.Frame(root, bg="#0f172a")
        self.rows_frame.pack(fill="x", padx=24, pady=(4, 8))

        # Buttons
        btns = tk.Frame(root, bg="#0f172a")
        btns.pack(pady=6)
        self._btn(btns, "+ Add subject", self.add_row, "#334155").pack(side="left", padx=4)
        self._btn(btns, "Clear", self.clear_all, "#334155").pack(side="left", padx=4)
        self._btn(btns, "Calculate", self.calculate, "#2563eb").pack(side="left", padx=4)

        # Result card
        self.result = tk.Frame(root, bg="#1e293b", height=150)
        self.result.pack(fill="x", padx=24, pady=16)
        self.result.pack_propagate(False)

        self.grade_lbl = tk.Label(self.result, text="—", bg="#1e293b", fg="white",
                                  font=("Segoe UI", 46, "bold"))
        self.grade_lbl.pack(pady=(18, 0))
        self.detail_lbl = tk.Label(self.result, text="Add subjects and press Calculate",
                                   bg="#1e293b", fg="#94a3b8", font=("Segoe UI", 11))
        self.detail_lbl.pack()

        # Start with three rows
        for _ in range(3):
            self.add_row()

    def _btn(self, parent, text, cmd, color):
        return tk.Button(parent, text=text, command=cmd, bg=color, fg="white",
                         font=("Segoe UI", 10, "bold"), relief="flat",
                         activebackground=color, padx=12, pady=6, cursor="hand2",
                         bd=0)

    def add_row(self):
        row = tk.Frame(self.rows_frame, bg="#0f172a")
        row.pack(fill="x", pady=3)
        subject = tk.Entry(row, width=24, font=("Segoe UI", 11), relief="flat",
                           bg="#1e293b", fg="white", insertbackground="white")
        subject.pack(side="left", ipady=5, padx=(0, 8))
        score = tk.Entry(row, width=8, font=("Segoe UI", 11), relief="flat",
                         bg="#1e293b", fg="white", insertbackground="white",
                         justify="center")
        score.pack(side="left", ipady=5)
        tk.Button(row, text="✕", command=lambda: self.remove_row(row),
                  bg="#0f172a", fg="#64748b", relief="flat", bd=0,
                  font=("Segoe UI", 11), cursor="hand2",
                  activebackground="#0f172a").pack(side="left", padx=8)
        self.rows.append((row, subject, score))

    def remove_row(self, row):
        self.rows = [r for r in self.rows if r[0] is not row]
        row.destroy()

    def clear_all(self):
        for row, _, _ in self.rows:
            row.destroy()
        self.rows = []
        for _ in range(3):
            self.add_row()
        self.grade_lbl.config(text="—", fg="white")
        self.detail_lbl.config(text="Add subjects and press Calculate")

    def calculate(self):
        scores = []
        for _, subject, score in self.rows:
            raw = score.get().strip()
            if not raw:
                continue
            try:
                val = float(raw)
            except ValueError:
                messagebox.showerror("Invalid input",
                                     f"'{raw}' is not a number.")
                return
            if not 0 <= val <= 100:
                messagebox.showerror("Out of range",
                                     "Scores must be between 0 and 100.")
                return
            scores.append(val)

        if not scores:
            messagebox.showwarning("No scores", "Enter at least one score.")
            return

        avg = sum(scores) / len(scores)
        grade = letter_grade(avg)
        status = "PASS" if avg >= 60 else "FAIL"
        self.grade_lbl.config(text=grade, fg=COLORS[grade])
        self.detail_lbl.config(
            text=f"Average: {avg:.1f}%   •   {status}   •   {len(scores)} subject(s)")


if __name__ == "__main__":
    root = tk.Tk()
    GradeApp(root)
    root.mainloop()
