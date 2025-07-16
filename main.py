import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="중력 렌즈 시뮬레이터", layout="centered")

st.title("🔭 중력 렌즈 효과 시뮬레이터")

# 사용자 입력
lens_x = st.slider("렌즈의 위치 (x축)", -30, 30, 0, step=1)
has_planet = st.checkbox("렌즈에 행성 포함", value=False)

# ==========================
# 데이터 생성
# ==========================

x = np.arange(-50, 51)
brightness = 1 / ((x - lens_x) ** 2 + 1)

# 행성 효과 추가
if has_planet:
    planet_offset = 10
    planet_x = lens_x + planet_offset
    brightness += 0.5 / ((x - planet_x) ** 2 + 1)
else:
    planet_x = None

brightness = np.clip(brightness, 0, 2)

# ==========================
# 📍 위치도 시각화
# ==========================

fig1, ax1 = plt.subplots(figsize=(6, 2))
ax1.set_xlim(-50, 50)
ax1.set_ylim(-2, 2)
ax1.set_title("광원 - 렌즈 - 행성 위치도")
ax1.set_xlabel("위치 (x축)")
ax1.get_yaxis().set_visible(False)

# 광원
ax1.plot(0, 0, 'yellow', marker='*', markersize=20, label="광원 (Source)")

# 렌즈
ax1.plot(lens_x, 0, 'black', marker='o', markersize=12, label="렌즈 (별)")

# 행성
if has_planet:
    ax1.plot(planet_x, 0, 'blue', marker='o', markersize=10, label="행성 (Planet)")

ax1.legend(loc="upper right")
ax1.axhline(0, color='gray', linestyle='--', linewidth=0.5)

st.pyplot(fig1)

# ==========================
# 📈 밝기 곡선 시각화
# ==========================

fig2, ax2 = plt.subplots()
ax2.plot(x, brightness, color='orange', linewidth=2)
ax2.set_title("밝기 곡선 (Light Curve)")
ax2.set_xlabel("관측 위치")
ax2.set_ylabel("밝기")
ax2.grid(True)

st.pyplot(fig2)
