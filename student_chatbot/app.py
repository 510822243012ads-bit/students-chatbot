from flask import Flask, render_template, request
import csv

app = Flask(__name__)

def get_student_data(register_number):
    with open('students.csv', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['RegisterNumber'] == register_number:
                return row
    return None

@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    if request.method == "POST":
        reg_no = request.form["register_number"]
        student = get_student_data(reg_no)
        if student:
            response = f"""
            Name: {student['Name']}<br>
            Attendance: {student['Attendance']}%<br>
            GPA: {student['GPA']}<br>
            Result: {student['Result']}
            """
        else:
            response = "Student not found!"
    return render_template("chat.html", response=response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8501)
