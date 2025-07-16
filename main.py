import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="중력 렌즈 시뮬레이터", layout="centered")
st.title("🔭 중력 렌즈 효과 시뮬레이터 (고정 관측자 + 반지름 조절)")

# 🌟 입력값
lens_x = st.slider("렌즈의 위치 (x축)", -20, 20, 0, step=1)
has_planet = st.checkbox("렌즈에 행성 포함", value=False)
planet_offset = 5  # 행성은 렌즈에서 +5만큼 오른쪽에 고정

# 🔧 렌즈 효과 범위 조절
lens_radius = st.slider("항성 렌즈 효과 반지름", 1.0, 10.0, 3.0, step=0.5)
planet_radius = st.slider("행성 렌즈 효과 반지름", 1.0, 10.0, 3.0, step=0.5)

# 관측자는 x=0 에 고정
observer_x = 0

# 광원 x 위치 (시간 흐름)
source_positions = np.arange(-50, 51)

# 🌠 밝기 계산 함수
def compute_brightness(source_x, lens_x, planet_x=None, lens_r=3.0, planet_r=3.0):
    # 항성 렌즈 효과 (가우시안)
    lens_dist = abs(source_x - lens_x)
    brightness = 1 + 0.8 * np.exp(- (lens_dist / lens_r) ** 2)

    # 행성 렌즈 효과
    if planet_x is not None:
        planet_dist = abs(source_x - planet_x)
        brightness += 0.3 * np.exp(- (planet_dist / planet_r) ** 2)

    return min(brightness, 2.5)

# 밝기 계산
brightness_values = []
for sx in source_positions:
    px = lens_x + planet_offset if has_planet else None
    b = compute_brightness(sx, lens_x, px, lens_radius, planet_radius)
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

# 예시 광원
ax1.plot(-20, 1, 'yellow', marker='*', markersize=20, label="광원 (예시)")

ax1.legend(loc="upper right")
st.pyplot(fig1)

# =======================
# 밝기 곡선 시각화
# =======================
fig2, ax2 = plt.subplots()
ax2.plot(source_positions, brightness_values, color='orange', linewidth=2)
ax2.set_title("밝기 곡선 (관측자가 측정한 값)")
ax2.set_xlabel("광원의 위치 (시간 흐름)")
ax2.set_ylabel("측정 밝기")
ax2.grid(True)

st.pyplot(fig2)
