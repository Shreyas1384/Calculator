# 🧮 Shrey's Calc - Modern Scientific Calculator

A modern, high-precision scientific calculator application powered by Python with a glassmorphism web UI and a native Streamlit edition.

---

## ✨ Features

### 🔬 Scientific Capabilities
- **Trigonometry**: `sin`, `cos`, `tan` with degree (`DEG`) and radian (`RAD`) angle mode toggle.
- **Inverse Trigonometry**: `2nd` function toggle switches to `sin⁻¹` (asin), `cos⁻¹` (acos), `tan⁻¹` (atan).
- **Logarithms & Exponents**:
  - `ln`: Natural logarithm ($\ln x$, base $e$)
  - `log`: Common logarithm ($\log_{10} x$, base 10)
  - `eˣ`: Exponential function ($\exp x$)
  - `x²`: Square
  - `x³`: Cube
  - `xʸ`: Arbitrary power / exponentiation
- **Roots**:
  - `√x`: Square root
  - `∛x`: Cube root (supports negative numbers)
- **Advanced Arithmetic**:
  - `1/x`: Reciprocal
  - `|x|`: Absolute value
  - `n!`: Factorial (non-negative integers up to 170!)
  - `mod`: Modulo operator
  - `( )`: Parentheses with full nested expression support
- **Mathematical Constants**:
  - `π` ($3.1415926535...$)
  - `e` ($2.7182818284...$)

### 🎨 Design & Interaction
- **Single-Line Multi-Operand Calculation**: Numbers and operators remain on the same contiguous line (e.g. `8 + 7`) with dynamic scaling.
- **Glassmorphic UI**: Frosted glass container with ambient background glow animations.
- **Calculation History**: Review past equations, click any result to reload into display, or clear logs.
- **Memory Operations**: `MC`, `MR`, `M+`, `M−`.

---

## 🚀 Running with Streamlit

To launch the native Streamlit app:
```bash
streamlit run streamlit_app.py
```
This serves the application on `http://localhost:8501` and opens your browser automatically.

### Deploying to Streamlit Community Cloud:
1. Push this repository to GitHub.
2. Sign in to [share.streamlit.io](https://share.streamlit.io/).
3. Select your repository, branch, and set main file path to:
   ```
   streamlit_app.py
   ```
4. Click **Deploy**! (All dependencies are defined in `requirements.txt`).

---

## 🌐 Running with Flask / Web App

```bash
python main.py
```
Starts the standalone web server and automatically opens `http://127.0.0.1:5001`.

---

## 🧪 Automated Testing

Run all unit and integration tests:
```bash
python -m unittest discover -s . -p "test_*.py"
```
