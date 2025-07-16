import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="중력 렌즈 시뮬레이터 (디테일 버전)", layout="centered")
st.title("🔭 중력 렌즈 효과 시뮬레이터 (관측자 고정 + 디테일 곡선)")

# 입력
lens_x = st.slider("렌즈 위치 (x축)", -20, 20, 0)
has_planet = st.checkbox("렌즈에 행성 포함", value=False)
planet_offset = 5
einstein_radius = 5  # 정규화용 반지름

# 관측자 x=0 고정
observer_x = 0

# 광원 위치 (시간 흐름)
source_positions = np.linspace(-50, 50, 500)

def microlens_brightness(u):
    # u는 정규화된 거리
    return (u**2 + 2) / (u * np.sqrt(u**2 + 4))

brightness_values = []
for sx in source_positions:
    u_lens = abs(sx - lens_x) / einstein_radius
    brightness = microlens_brightness(u_lens)

    # 행성 렌즈 효과 추가
    if has_planet:
        planet_x = lens_x + planet_offset
        u_planet = abs(sx - planet_x) / einstein_radius
        brightness += 0.3 * microlens_brightness(u_planet)  # 약한 영향 가정

    brightness_values.append(min(brightness, 5))  # 상한 제한

# ======================
# 위치도 시각화
# ======================
fig1, ax1 = plt.subplots(figsize=(6, 2))
ax1.set_xlim(-50, 50)
ax1.set_ylim(-2, 2)
ax1.set_title("위치도: 광원 - 렌즈 - 행성 - 관측자")
ax1.get_yaxis().set_visible(False)

# 궤도
ax1.hlines(1, -50, 50, colors='lightgray', linestyles='dashed')

# 렌즈
ax1.plot(lens_x, 0, 'black', marker='o', markersize=12, label="렌즈 (별)")

# 행성
if has_planet:
    ax1.plot(lens_x + planet_offset, 0, 'blue', marker='o', markersize=10, label="행성")

# 관측자
ax1.plot(observer_x, -1, 'green', marker='^', markersize=12, label="관측자")

# 예시 광원
ax1.plot(-20, 1, 'yellow', marker='*', markersize=20, label="광원")

ax1.legend()
st.pyplot(fig1)

# ======================
# 밝기 곡선 시각화
# ======================
fig2, ax2 = plt.subplots()
ax2.plot(source_positions, brightness_values, color='orange', linewidth=2)
ax2.set_title("정밀 밝기 곡선 (Microlensing Light Curve)")
ax2.set_xlabel("광원의 위치 (시간 흐름)")
ax2.set_ylabel("측정 밝기 (증폭률)")
ax2.grid(True)

st.pyplot(fig2)
