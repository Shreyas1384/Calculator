"""
Shrey's Calc - Streamlit Edition
Modern Scientific Calculator with Glassmorphic UI & Python Core Engine.
"""

import math
import streamlit as st
from calculator import Calculator

# Configure page
st.set_page_config(
    page_title="Shrey's Calc - Scientific Calculator",
    page_icon="🧮",
    layout="centered",
    initial_sidebar_state="auto"
)

# Initialize Calculator engine in session state
if "calc" not in st.session_state:
    st.session_state.calc = Calculator()

if "expression" not in st.session_state:
    st.session_state.expression = "0"

if "previous_equation" not in st.session_state:
    st.session_state.previous_equation = ""

if "memory" not in st.session_state:
    st.session_state.memory = 0.0

if "angle_mode" not in st.session_state:
    st.session_state.angle_mode = "DEG"

if "is_evaluated" not in st.session_state:
    st.session_state.is_evaluated = False

if "show_sci" not in st.session_state:
    st.session_state.show_sci = True


# --- Custom CSS Styling ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Outfit:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }

    .stApp {
        background-color: #090a10;
        background-image:
            radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(168, 85, 247, 0.15) 0px, transparent 50%);
    }

    /* Screen Container */
    .calc-screen {
        background: rgba(10, 12, 22, 0.88);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 18px 24px;
        box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.5), 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        margin-bottom: 16px;
    }

    .calc-screen-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        min-height: 22px;
    }

    .prev-formula {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.95rem;
        color: #94a3b8;
    }

    .calc-screen-main {
        font-family: 'Outfit', sans-serif;
        font-size: 2.6rem;
        font-weight: 700;
        color: #f8fafc;
        text-align: right;
        white-space: nowrap;
        overflow-x: auto;
        line-height: 1.2;
        padding: 6px 0;
        letter-spacing: -0.02em;
    }

    .calc-screen-bottom {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        color: #64748b;
    }

    .badge-pill {
        background: rgba(99, 102, 241, 0.2);
        color: #818cf8;
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 700;
        border: 1px solid rgba(99, 102, 241, 0.3);
    }

    /* Streamlit Button Overrides */
    div.stButton > button {
        border-radius: 12px;
        font-size: 1.05rem;
        font-weight: 600;
        padding: 10px 0;
        height: 52px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        background: rgba(255, 255, 255, 0.04);
        color: #f1f5f9;
        transition: all 0.15s ease;
    }

    div.stButton > button:hover {
        background: rgba(255, 255, 255, 0.12);
        border-color: rgba(99, 102, 241, 0.4);
        transform: translateY(-2px);
    }

    div.stButton > button:active {
        transform: scale(0.96);
    }

    /* Header styling */
    .app-brand {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 8px;
    }

    .brand-title {
        font-size: 1.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 40%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)


# --- Action Handlers ---

def append_digit(d):
    if st.session_state.is_evaluated or st.session_state.expression == "0":
        st.session_state.expression = str(d)
        st.session_state.is_evaluated = False
    else:
        st.session_state.expression += str(d)


def append_operator(op):
    if st.session_state.is_evaluated:
        st.session_state.is_evaluated = False

    expr = st.session_state.expression.strip()
    if expr.endswith(("+", "-", "×", "÷", "^", "%")):
        st.session_state.expression = expr[:-1].strip() + f" {op} "
    else:
        st.session_state.expression = f"{expr} {op} "


def append_decimal():
    if st.session_state.is_evaluated:
        st.session_state.expression = "0."
        st.session_state.is_evaluated = False
        return

    expr = st.session_state.expression
    parts = expr.split()
    last = parts[-1] if parts else ""
    if "." not in last:
        if expr.endswith(" ") or expr == "":
            st.session_state.expression += "0."
        else:
            st.session_state.expression += "."


def append_function(fn):
    if st.session_state.is_evaluated:
        st.session_state.is_evaluated = False

    expr = st.session_state.expression.strip()
    if expr == "0" or expr == "":
        st.session_state.expression = f"{fn}("
    elif expr.endswith(("+", "-", "×", "÷", "^", "%", "(")):
        st.session_state.expression += f" {fn}("
    else:
        st.session_state.expression = f"{fn}({expr})"


def apply_backspace():
    if st.session_state.is_evaluated:
        st.session_state.expression = "0"
        st.session_state.is_evaluated = False
        return

    expr = st.session_state.expression.rstrip()
    if len(expr) > 1:
        st.session_state.expression = expr[:-1].rstrip()
    else:
        st.session_state.expression = "0"


def clear_all():
    st.session_state.expression = "0"
    st.session_state.previous_equation = ""
    st.session_state.is_evaluated = False


def calculate_expression():
    expr = st.session_state.expression.strip()
    if not expr or expr == "0":
        return

    try:
        res = st.session_state.calc.evaluate_expression(expr, angle_mode=st.session_state.angle_mode)
        st.session_state.previous_equation = f"{expr} ="
        st.session_state.expression = str(res)
        st.session_state.is_evaluated = True
    except Exception as e:
        st.toast(f"Error: {str(e)}", icon="⚠️")


# --- App Header ---
col_brand, col_mode = st.columns([3, 1])

with col_brand:
    st.markdown("""
    <div class="app-brand">
        <span style="font-size: 2rem;">🧮</span>
        <div>
            <div class="brand-title">Shrey's Calc</div>
            <div style="font-size: 0.75rem; color: #94a3b8;">Streamlit Edition &bull; Python Core</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_mode:
    new_mode = st.radio("Angle Mode", ["DEG", "RAD"], horizontal=True, label_visibility="collapsed")
    if new_mode != st.session_state.angle_mode:
        st.session_state.angle_mode = new_mode


# --- Display Screen (Everything stays on the same line!) ---
prev_eq = st.session_state.previous_equation if st.session_state.is_evaluated else ""
mem_status = f"M: {st.session_state.memory}" if st.session_state.memory != 0 else "M: 0"

st.markdown(f"""
<div class="calc-screen">
    <div class="calc-screen-top">
        <span class="prev-formula">{prev_eq}</span>
        <span class="badge-pill">{st.session_state.angle_mode}</span>
    </div>
    <div class="calc-screen-main">{st.session_state.expression}</div>
    <div class="calc-screen-bottom">
        <span>{mem_status}</span>
        <span>Python 3.11 AST Engine</span>
    </div>
</div>
""", unsafe_allow_html=True)


# --- Memory Bar ---
m1, m2, m3, m4, m5 = st.columns(5)
with m1:
    if st.button("MC", use_container_width=True):
        st.session_state.memory = 0.0
        st.toast("Memory Cleared", icon="🧹")
with m2:
    if st.button("MR", use_container_width=True):
        st.session_state.expression = str(st.session_state.memory)
        st.session_state.is_evaluated = False
        st.rerun()
with m3:
    if st.button("M+", use_container_width=True):
        try:
            val = float(st.session_state.expression)
            st.session_state.memory += val
            st.toast(f"Memory: {st.session_state.memory}", icon="💾")
        except: pass
with m4:
    if st.button("M−", use_container_width=True):
        try:
            val = float(st.session_state.expression)
            st.session_state.memory -= val
            st.toast(f"Memory: {st.session_state.memory}", icon="💾")
        except: pass
with m5:
    sci_label = "Hide Sci" if st.session_state.show_sci else "Show Sci"
    if st.button(sci_label, use_container_width=True):
        st.session_state.show_sci = not st.session_state.show_sci
        st.rerun()


# --- Scientific Keypad Section ---
if st.session_state.show_sci:
    s_r1_1, s_r1_2, s_r1_3, s_r1_4, s_r1_5 = st.columns(5)
    with s_r1_1:
        if st.button("sin", use_container_width=True): append_function("sin"); st.rerun()
    with s_r1_2:
        if st.button("cos", use_container_width=True): append_function("cos"); st.rerun()
    with s_r1_3:
        if st.button("tan", use_container_width=True): append_function("tan"); st.rerun()
    with s_r1_4:
        if st.button("ln", use_container_width=True): append_function("ln"); st.rerun()
    with s_r1_5:
        if st.button("log", use_container_width=True): append_function("log"); st.rerun()

    s_r2_1, s_r2_2, s_r2_3, s_r2_4, s_r2_5 = st.columns(5)
    with s_r2_1:
        if st.button("√x", use_container_width=True): append_function("sqrt"); st.rerun()
    with s_r2_2:
        if st.button("∛x", use_container_width=True): append_function("cbrt"); st.rerun()
    with s_r2_3:
        if st.button("x²", use_container_width=True):
            st.session_state.expression += " ^ 2"; st.rerun()
    with s_r2_4:
        if st.button("xʸ", use_container_width=True):
            append_operator("^"); st.rerun()
    with s_r2_5:
        if st.button("n!", use_container_width=True):
            st.session_state.expression += "!"; st.rerun()

    s_r3_1, s_r3_2, s_r3_3, s_r3_4, s_r3_5 = st.columns(5)
    with s_r3_1:
        if st.button("π", use_container_width=True):
            st.session_state.expression = "π" if st.session_state.expression == "0" else st.session_state.expression + " * π"
            st.rerun()
    with s_r3_2:
        if st.button("e", use_container_width=True):
            st.session_state.expression = "e" if st.session_state.expression == "0" else st.session_state.expression + " * e"
            st.rerun()
    with s_r3_3:
        if st.button("(", use_container_width=True):
            st.session_state.expression = "(" if st.session_state.expression == "0" else st.session_state.expression + " * ("
            st.rerun()
    with s_r3_4:
        if st.button(")", use_container_width=True):
            st.session_state.expression += ")"; st.rerun()
    with s_r3_5:
        if st.button("1/x", use_container_width=True):
            st.session_state.expression = f"1 / ({st.session_state.expression})"
            st.rerun()


# --- Standard Keypad Grid ---
k1, k2, k3, k4 = st.columns(4)

with k1:
    if st.button("AC", use_container_width=True, type="primary"): clear_all(); st.rerun()
with k2:
    if st.button("⌫", use_container_width=True): apply_backspace(); st.rerun()
with k3:
    if st.button("%", use_container_width=True): append_operator("%"); st.rerun()
with k4:
    if st.button("÷", use_container_width=True): append_operator("÷"); st.rerun()

r2_1, r2_2, r2_3, r2_4 = st.columns(4)
with r2_1:
    if st.button("7", use_container_width=True): append_digit(7); st.rerun()
with r2_2:
    if st.button("8", use_container_width=True): append_digit(8); st.rerun()
with r2_3:
    if st.button("9", use_container_width=True): append_digit(9); st.rerun()
with r2_4:
    if st.button("×", use_container_width=True): append_operator("×"); st.rerun()

r3_1, r3_2, r3_3, r3_4 = st.columns(4)
with r3_1:
    if st.button("4", use_container_width=True): append_digit(4); st.rerun()
with r3_2:
    if st.button("5", use_container_width=True): append_digit(5); st.rerun()
with r3_3:
    if st.button("6", use_container_width=True): append_digit(6); st.rerun()
with r3_4:
    if st.button("−", use_container_width=True): append_operator("-"); st.rerun()

r4_1, r4_2, r4_3, r4_4 = st.columns(4)
with r4_1:
    if st.button("1", use_container_width=True): append_digit(1); st.rerun()
with r4_2:
    if st.button("2", use_container_width=True): append_digit(2); st.rerun()
with r4_3:
    if st.button("3", use_container_width=True): append_digit(3); st.rerun()
with r4_4:
    if st.button("+", use_container_width=True): append_operator("+"); st.rerun()

r5_1, r5_2, r5_3, r5_4 = st.columns(4)
with r5_1:
    if st.button("±", use_container_width=True):
        if st.session_state.expression.startswith("-"):
            st.session_state.expression = st.session_state.expression[1:]
        elif st.session_state.expression != "0":
            st.session_state.expression = "-" + st.session_state.expression
        st.rerun()
with r5_2:
    if st.button("0", use_container_width=True): append_digit(0); st.rerun()
with r5_3:
    if st.button(".", use_container_width=True): append_decimal(); st.rerun()
with r5_4:
    if st.button("=", use_container_width=True, type="primary"):
        calculate_expression()
        st.rerun()


# --- Sidebar: Calculation History ---
with st.sidebar:
    st.header("📜 Calculation History")
    history = st.session_state.calc.get_history()

    if st.button("Clear History", use_container_width=True):
        st.session_state.calc.clear_history()
        st.toast("History Cleared", icon="🗑️")
        st.rerun()

    if not history:
        st.caption("No calculations recorded yet.")
    else:
        for idx, item in enumerate(history):
            with st.container():
                st.markdown(f"**{item['expression']}**")
                st.markdown(f"### `{item['result']}`")
                if st.button(f"Load {item['result']}", key=f"hist_{idx}", use_container_width=True):
                    st.session_state.expression = str(item['result'])
                    st.session_state.previous_equation = f"{item['expression']} ="
                    st.session_state.is_evaluated = True
                    st.rerun()
                st.divider()
