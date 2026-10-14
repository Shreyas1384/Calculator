"""
Flask Application for Shrey's Calc (Modern Scientific Calculator).
Serves the web UI and handles mathematical operations via the Python engine.
Automatically launches the web browser when executed.
"""

import os
import sys
import argparse
import webbrowser
import threading
import socket
from flask import Flask, render_template, request, jsonify
from calculator import Calculator

app = Flask(__name__)
calc = Calculator()


def find_available_port(starting_port=5000, max_attempts=20):
    """Find an available port starting from starting_port."""
    for port in range(starting_port, starting_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
    return starting_port


@app.route("/")
def index():
    """Render the primary calculator application UI."""
    return render_template("index.html")


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "shreys-calc"})


@app.route("/api/calculate", methods=["POST"])
def calculate():
    """
    Evaluate a mathematical expression or perform an operation.
    Accepts:
        {"expression": "sin(30) + log(100)", "angle_mode": "DEG"}
    Or:
        {"operation": "sin", "a": 30, "angle_mode": "DEG"}
    """
    data = request.get_json(silent=True) or {}
    expression = data.get("expression")
    operation = data.get("operation")
    angle_mode = data.get("angle_mode", "DEG").upper()

    try:
        if expression is not None:
            result = calc.evaluate_expression(expression, angle_mode=angle_mode)
            return jsonify({
                "success": True,
                "result": result,
                "formatted": str(result),
                "expression": expression,
                "angle_mode": angle_mode
            })

        if operation:
            a = float(data.get("a", 0))
            b = float(data.get("b", 0)) if "b" in data else None

            if operation == "add":
                res = calc.add(a, b)
            elif operation == "subtract":
                res = calc.subtract(a, b)
            elif operation == "multiply":
                res = calc.multiply(a, b)
            elif operation == "divide":
                res = calc.divide(a, b)
            elif operation == "power":
                res = calc.power(a, b)
            elif operation == "modulo":
                res = calc.modulo(a, b)
            elif operation == "square_root":
                res = calc.square_root(a)
            elif operation == "cube_root":
                res = calc.cube_root(a)
            elif operation == "percentage":
                res = calc.percentage(a)
            elif operation == "negate":
                res = calc.negate(a)
            elif operation == "reciprocal":
                res = calc.reciprocal(a)
            elif operation == "abs":
                res = calc.abs_val(a)
            elif operation == "factorial":
                res = calc.factorial(a)
            elif operation == "sin":
                res = calc.sin(a, mode=angle_mode)
            elif operation == "cos":
                res = calc.cos(a, mode=angle_mode)
            elif operation == "tan":
                res = calc.tan(a, mode=angle_mode)
            elif operation == "asin":
                res = calc.asin(a, mode=angle_mode)
            elif operation == "acos":
                res = calc.acos(a, mode=angle_mode)
            elif operation == "atan":
                res = calc.atan(a, mode=angle_mode)
            elif operation == "ln":
                res = calc.ln(a)
            elif operation == "log10":
                res = calc.log10(a)
            elif operation == "exp":
                res = calc.exp(a)
            else:
                return jsonify({"success": False, "error": f"Unknown operation '{operation}'"}), 400

            # Format result
            if isinstance(res, float):
                res = round(res, 10)
                if res.is_integer() and abs(res) < 1e15:
                    res = int(res)

            return jsonify({
                "success": True,
                "result": res,
                "formatted": str(res),
                "operation": operation
            })

        return jsonify({"success": False, "error": "No expression or operation provided"}), 400

    except ZeroDivisionError as e:
        return jsonify({"success": False, "error": "Cannot divide by zero"}), 400
    except OverflowError as e:
        return jsonify({"success": False, "error": "Number too large (overflow)"}), 400
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": f"Calculation error: {str(e)}"}), 500


@app.route("/api/history", methods=["GET"])
def get_history():
    """Return historical calculations."""
    return jsonify({
        "success": True,
        "history": calc.get_history()
    })


@app.route("/api/clear-history", methods=["POST"])
def clear_history():
    """Clear calculation history."""
    calc.clear_history()
    return jsonify({
        "success": True,
        "message": "History cleared"
    })


def open_browser(url: str):
    """Open default system web browser after server starts."""
    try:
        webbrowser.open_new_tab(url)
    except Exception as e:
        print(f"Browser auto-open notice: {e}")


def main():
    parser = argparse.ArgumentParser(description="Shrey's Calc - Modern Scientific Calculator")
    parser.add_argument("--port", type=int, default=5000, help="Server port (default: 5000)")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Server host")
    parser.add_argument("--no-browser", action="store_true", help="Do not automatically open browser")
    args = parser.parse_args()

    port = find_available_port(args.port)
    url = f"http://{args.host}:{port}"

    print("=" * 60)
    print(" 🚀 Shrey's Calc (Scientific Calculator)")
    print(f" 🌐 Access UI at: {url}")
    print("=" * 60)

    if not args.no_browser:
        timer = threading.Timer(1.0, open_browser, args=[url])
        timer.daemon = True
        timer.start()

    app.run(host=args.host, port=port, debug=False)


if __name__ == "__main__":
    main()
