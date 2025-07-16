import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="중력 렌즈 시뮬레이터", layout="centered")
st.title("🔭 중력 렌즈 효과 시뮬레이터 (고정 관측자)")

# 입력값
lens_x = st.slider("렌즈의 위치 (x축)", -20, 20, 0, step=1)
has_planet = st.checkbox("렌즈에 행성 포함", value=False)
planet_offset = 5  # 행성은 렌즈에서 +5만큼 오른쪽에 고정

# 관측자는 x=0 에 고정
observer_x = 0

# 광원 x 위치 (시간 축) -50 ~ 50
source_positions = np.arange(-50, 51)

def compute_brightness(source_x, lens_x, planet_x=None):
    # 거리 기준 밝기 계산: 관측자-렌즈-광원 정렬 중심
    lens_dist = abs(source_x - lens_x)
    brightness = 1 / (lens_dist ** 2 + 1)

    if planet_x is not None:
        planet_dist = abs(source_x - planet_x)
        brightness += 0.5 / (planet_dist ** 2 + 1)

    return min(brightness, 2)

# 밝기 계산
brightness_values = []
for sx in source_positions:
    if has_planet:
        px = lens_x + planet_offset
    else:
        px = None
    b = compute_brightness(sx, lens_x, px)
    brightness_values.append(b)

# =======================
# 위치도 시각화
# =======================
fig1, ax1 = plt.subplots(figsize=(6, 2))
ax1.set_xlim(-50, 50)
ax1.set_ylim(-2, 2)
ax1.set_title("위치도: 광원, 렌즈, 행성, 관측자")
ax1.get_yaxis().set_visible(False)

# 광원 이동 궤도
ax1.hlines(1, -50, 50, colors='lightgray', linestyles='dashed', linewidth=1)

# 렌즈
ax1.plot(lens_x, 0, 'black', marker='o', markersize=12, label="렌즈 (별)")

# 행성
if has_planet:
    ax1.plot(lens_x + planet_offset, 0, 'blue', marker='o', markersize=10, label="행성")

# 관측자
ax1.plot(observer_x, -1, 'green', marker='^', markersize=12, label="관측자")

# 예시 광원 (x=-20, 움직이는 객체)
ax1.plot(-20, 1, 'yellow', marker='*', markersize=20, label="광원 (예시)")

ax1.legend(loc="upper right")
st.pyplot(fig1)

# =======================
# 밝기 곡선 (Light Curve)
# =======================
fig2, ax2 = plt.subplots()
ax2.plot(source_positions, brightness_values, color='orange', linewidth=2)
ax2.set_title("밝기 곡선 (관측자가 측정한 값)")
ax2.set_xlabel("광원의 위치 (시간 흐름)")
ax2.set_ylabel("측정 밝기")
ax2.grid(True)

st.pyplot(fig2)
