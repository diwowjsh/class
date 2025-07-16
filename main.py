import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="중력 렌즈 시뮬레이터", layout="centered")
st.title("🔭 중력 렌즈 효과 시뮬레이터 (광원 뒤, 관측자 고정)")

# 렌즈 위치 범위
lens_positions = np.arange(-50, 51)
planet_offset = 5

# 고정 위치
observer_x = 0
source_x = -30  # 광원을 렌즈 뒤(왼쪽)로 고정

# 사용자 입력
has_planet = st.checkbox("렌즈에 행성 포함", value=False)
lens_radius = st.slider("항성 렌즈 효과 반지름", 1.0, 10.0, 3.0, step=0.5)
planet_radius = st.slider("행성 렌즈 효과 반지름", 1.0, 10.0, 3.0, step=0.5)

# 밝기 계산 함수
def compute_brightness(lens_x, source_x, planet_x=None, lens_r=3.0, planet_r=3.0):
    lens_dist = abs(source_x - lens_x)
    brightness = 1 + 0.8 * np.exp(- (lens_dist / lens_r) ** 2)

    if planet_x is not None:
        planet_dist = abs(source_x - planet_x)
        brightness += 0.3 * np.exp(- (planet_dist / planet_r) ** 2)

    return min(brightness, 2.5)

# 밝기 계산 (렌즈 이동)
brightness_values = []
for lens_x in lens_positions:
    planet_x = lens_x + planet_offset if has_planet else None
    b = compute_brightness(lens_x, source_x, planet_x, lens_radius, planet_radius)
    brightness_values.append(b)

# 위치도 시각화
fig1, ax1 = plt.subplots(figsize=(6, 2))
ax1.set_xlim(-50, 50)
ax1.set_ylim(-2, 2)
ax1.set_title("위치도: 렌즈, 행성, 광원(뒤쪽), 관측자(고정)")
ax1.get_yaxis().set_visible(False)

# 광원 위치
ax1.plot(source_x, 1, 'yellow', marker='*', markersize=18, label="광원 (뒤쪽)")

# 관측자 위치
ax1.plot(observer_x, -1, 'green', marker='^', markersize=12, label="관측자 (고정)")

# 렌즈 궤도 (x축 선)
ax1.hlines(0, -50, 50, colors='gray', linestyles='dashed')

# 현재 렌즈 위치 (0으로 표시)
current_lens_x = 0
ax1.plot(current_lens_x, 0, 'black', marker='o', markersize=12, label="렌즈")

# 행성 위치
if has_planet:
    ax1.plot(current_lens_x + planet_offset, 0, 'blue', marker='o', markersize=10, label="행성")

ax1.legend(loc="upper right")
st.pyplot(fig1)

# 밝기 곡선 시각화
fig2, ax2 = plt.subplots()
ax2.plot(lens_positions, brightness_values, color='orange', linewidth=2)
ax2.set_title("밝기 곡선 (렌즈가 움직이며 측정)")
ax2.set_xlabel("렌즈 위치")
ax2.set_ylabel("측정 밝기")
ax2.grid(True)

st.pyplot(fig2)
