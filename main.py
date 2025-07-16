import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="중력 렌즈 시뮬레이터", layout="centered")

st.title("🔭 중력 렌즈 효과 시뮬레이터")

# 사용자 입력
lens_x = st.slider("렌즈의 위치 (x축)", -30, 30, 0, step=1)
has_planet = st.checkbox("렌즈에 행성 포함", value=False)

# 데이터 생성
x = np.arange(-50, 51)
brightness = 1 / ((x - lens_x)**2 + 1)  # 기본 렌즈 밝기

# 행성 효과 추가
if has_planet:
    planet_offset = 10
    planet_x = lens_x + planet_offset
    brightness += 0.5 / ((x - planet_x)**2 + 1)

brightness = np.clip(brightness, 0, 2)  # 밝기 제한

# 그래프 출력
fig, ax = plt.subplots()
ax.plot(x, brightness, color='orange', linewidth=2)
ax.set_title("밝기 곡선 (Light Curve)")
ax.set_xlabel("관측 위치")
ax.set_ylabel("밝기")
ax.grid(True)

st.pyplot(fig)
