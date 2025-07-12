import streamlit as st
import numpy as np
from scipy.optimize import fsolve

def solve_linear(a, b):
    """
    1차 방정식 ax + b = 0 을 풉니다.
    """
    if a == 0:
        return "계수 'a'는 0이 될 수 없습니다 (1차 방정식)."
    return -b / a

def solve_quadratic(a, b, c):
    """
    2차 방정식 ax^2 + bx + c = 0 을 풉니다.
    """
    delta = b**2 - 4*a*c
    if delta >= 0:
        x1 = (-b + np.sqrt(delta)) / (2*a)
        x2 = (-b - np.sqrt(delta)) / (2*a)
        return f"x1 = {x1:.4f}, x2 = {x2:.4f}"
    else:
        # 복소수 해
        real_part = -b / (2*a)
        imag_part = np.sqrt(abs(delta)) / (2*a)
        return f"x1 = {real_part:.4f} + {imag_part:.4f}i, x2 = {real_part:.4f} - {imag_part:.4f}i"

def solve_cubic(a, b, c, d):
    """
    3차 방정식 ax^3 + bx^2 + cx + d = 0 을 풉니다.
    scipy.optimize.fsolve를 사용하여 근사해를 찾습니다.
    (분석적 해는 복잡하므로 근사해를 사용)
    """
    if a == 0:
        return "계수 'a'는 0이 될 수 없습니다 (3차 방정식)."

    def poly(x):
        return a*x**3 + b*x**2 + c*x + d

    # 초기 추정값 설정 (여러 초기값으로 여러 해를 찾을 수 있음)
    initial_guesses = [-10, 0, 10]
    roots = []
    for guess in initial_guesses:
        try:
            root = fsolve(poly, guess)[0]
            if not any(np.isclose(root, r, atol=1e-6) for r in roots): # 중복 제거
                roots.append(root)
        except Exception:
            pass # 해를 찾지 못한 경우 건너뜀
    
    if len(roots) > 0:
        return ", ".join([f"x{i+1} = {r:.4f}" for i, r in enumerate(roots)])
    else:
        return "해를 찾을 수 없습니다 (근사)."

def solve_quartic(a, b, c, d, e):
    """
    4차 방정식 ax^4 + bx^3 + cx^2 + dx + e = 0 을 풉니다.
    numpy.roots를 사용하여 해를 찾습니다.
    """
    if a == 0:
        return "계수 'a'는 0이 될 수 없습니다 (4차 방정식)."
    
    coefficients = [a, b, c, d, e]
    roots = np.roots(coefficients)
    
    # 복소수 해를 포함하여 문자열로 포맷팅
    formatted_roots = []
    for i, r in enumerate(roots):
        if np.isreal(r):
            formatted_roots.append(f"x{i+1} = {r.real:.4f}")
        else:
            formatted_roots.append(f"x{i+1} = {r.real:.4f} + {r.imag:.4f}i")
    return ", ".join(formatted_roots)


st.set_page_config(page_title="방정식 계산기", layout="centered")

st.title("🔢 4차 이하 방정식 계산기")
st.write("각 차수에 맞는 계수를 입력하여 방정식을 풀어보세요.")

# 방정식 선택 라디오 버튼
equation_type = st.radio(
    "풀고 싶은 방정식의 차수를 선택하세요:",
    ("1차 방정식 (선형)", "2차 방정식 (2차)", "3차 방정식 (3차)", "4차 방정식 (4차)")
)

st.header("계수 입력")

if equation_type == "1차 방정식 (선형)":
    st.markdown("1차 방정식: $ax + b = 0$")
    col1, col2 = st.columns(2)
    with col1:
        a1 = st.number_input("계수 a (x의 계수)", value=1.0, key="a1")
    with col2:
        b1 = st.number_input("계수 b (상수항)", value=0.0, key="b1")
    
    if st.button("1차 방정식 풀기"):
        if a1 == 0:
            st.error("1차 방정식의 계수 'a'는 0이 될 수 없습니다. 'a'가 0이면 상수가 되어 방정식이 아닙니다.")
        else:
            result = solve_linear(a1, b1)
            st.success(f"**해:** {result}")

elif equation_type == "2차 방정식 (2차)":
    st.markdown("2차 방정식: $ax^2 + bx + c = 0$")
    col1, col2, col3 = st.columns(3)
    with col1:
        a2 = st.number_input("계수 a (x^2의 계수)", value=1.0, key="a2")
    with col2:
        b2 = st.number_input("계수 b (x의 계수)", value=0.0, key="b2")
    with col3:
        c2 = st.number_input("계수 c (상수항)", value=0.0, key="c2")
    
    if st.button("2차 방정식 풀기"):
        if a2 == 0:
            st.error("2차 방정식의 계수 'a'는 0이 될 수 없습니다. 'a'가 0이면 1차 방정식이 됩니다.")
        else:
            result = solve_quadratic(a2, b2, c2)
            st.success(f"**해:** {result}")

elif equation_type == "3차 방정식 (3차)":
    st.markdown("3차 방정식: $ax^3 + bx^2 + cx + d = 0$")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        a3 = st.number_input("계수 a (x^3의 계수)", value=1.0, key="a3")
    with col2:
        b3 = st.number_input("계수 b (x^2의 계수)", value=0.0, key="b3")
    with col3:
        c3 = st.number_input("계수 c (x의 계수)", value=0.0, key="c3")
    with col4:
        d3 = st.number_input("계수 d (상수항)", value=0.0, key="d3")

    if st.button("3차 방정식 풀기"):
        if a3 == 0:
            st.error("3차 방정식의 계수 'a'는 0이 될 수 없습니다. 'a'가 0이면 2차 이하의 방정식이 됩니다.")
        else:
            result = solve_cubic(a3, b3, c3, d3)
            st.success(f"**해:** {result}")
            st.info("3차 방정식은 일반적으로 분석적 해가 매우 복잡하며, 여기서는 SciPy의 `fsolve`를 이용한 근사해를 제공합니다. 모든 해를 찾지 못할 수도 있습니다.")


elif equation_type == "4차 방정식 (4차)":
    st.markdown("4차 방정식: $ax^4 + bx^3 + cx^2 + dx + e = 0$")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        a4 = st.number_input("계수 a (x^4의 계수)", value=1.0, key="a4")
    with col2:
        b4 = st.number_input("계수 b (x^3의 계수)", value=0.0, key="b4")
    with col3:
        c4 = st.number_input("계수 c (x^2의 계수)", value=0.0, key="c4")
    with col4:
        d4 = st.number_input("계수 d (x의 계수)", value=0.0, key="d4")
    with col5:
        e4 = st.number_input("계수 e (상수항)", value=0.0, key="e4")

    if st.button("4차 방정식 풀기"):
        if a4 == 0:
            st.error("4차 방정식의 계수 'a'는 0이 될 수 없습니다. 'a'가 0이면 3차 이하의 방정식이 됩니다.")
        else:
            result = solve_quartic(a4, b4, c4, d4, e4)
            st.success(f"**해:** {result}")
            st.info("4차 방정식은 NumPy의 `roots` 함수를 사용하여 모든 해를 찾습니다 (복소수 해 포함).")

st.markdown("""
---
**참고:**
* 2차 방정식의 경우 판별식에 따라 실수 또는 복소수 해를 제공합니다.
* 3차 방정식은 `scipy.optimize.fsolve`를 사용하여 근사해를 찾습니다. 이는 여러 초기값을 시도하여 가능한 해를 찾지만, 모든 해를 항상 정확히 찾아내지는 못할 수 있습니다.
* 4차 방정식은 `numpy.roots`를 사용하여 모든 해를 찾습니다. 복소수 해를 포함할 수 있습니다.
""")
