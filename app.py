from flask import Flask, render_template, request

app = Flask(__name__)

# 🔥 Smart Code Analyzer Logic
def analyze_code(code):
    lines = code.split("\n")

    loop_count = 0
    max_depth = 0
    current_depth = 0

    for line in lines:
        stripped = line.strip()

        if "for " in stripped or "while " in stripped:
            loop_count += 1
            current_depth += 1
            max_depth = max(max_depth, current_depth)
        else:
            current_depth = 0

    # Detect sorting
    if "sort(" in code or "sorted(" in code:
        return "O(n log n)", "Sorting detected. Efficient for large datasets."

    # Detect binary search
    if "mid" in code and ("left" in code or "right" in code):
        return "O(log n)", "Binary search detected. Very efficient."

    # Recursion detection
    recursion = False
    for line in lines:
        if line.strip().startswith("def"):
            func_name = line.split("def")[1].split("(")[0].strip()
            if func_name in code.replace(line, ""):
                recursion = True

    # Complexity logic
    if max_depth >= 3:
        return "O(n^3)", "High complexity! Reduce nested loops."
    elif max_depth == 2:
        return "O(n^2)", "Try optimizing nested loops."
    elif loop_count >= 1:
        return "O(n)", "Good. Can optimize further."
    elif recursion:
        return "O(n) or O(2^n)", "Use memoization (DP)."
    else:
        return "O(1)", "Highly efficient."


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    suggestion = None

    if request.method == "POST":
        code = request.form["code"]
        result, suggestion = analyze_code(code)

    data = []  # 🔥 No DB (important for deployment)

    return render_template("index.html", result=result, suggestion=suggestion, data=data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)