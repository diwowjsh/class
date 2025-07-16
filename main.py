import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="중력 렌즈 시뮬레이터", layout="centered")
st.title("🔭 중력 렌즈 시뮬레이터 (현실적 렌즈 효과)")

# 사용자 입력
lens_x = st.slider("렌즈 위치 (x축)", -20, 20, 0, step=1)
has_planet = st.checkbox("렌즈에 행성 포함", value=False)
planet_offset = 5
effect_width = 3.0  # 렌즈 효과 범위

# 관측자 x=0 고정
observer_x = 0

# 광원 x축 위치 (시간 흐름)
source_positions = np.linspace(-50, 50, 500)

# 밝기 계산 함수 (현실적 모델: 중심부에서만 영향)
def compute_brightness(source_x, lens_x, planet_x=None):
    dist_lens = abs(source_x - lens_x)
    brightness = 1 + 0.8 * np.exp(- (dist_lens / effect_width) ** 2)

    if planet_x is not None:
        dist_planet = abs(source_x - planet_x)
        brightness += 0.3 * np.exp(- (dist_planet / effect_width) ** 2)

    return brightness

# 밝기 계산
brightness_values = []
for sx in source_positions:
    planet_x = lens_x + planet_offset if has_planet else None
    b = compute_brightness(sx, lens_x, planet_x)
    brightness_values.append(b)

# =======================
# 위치 시각화
# =======================
fig1, ax1 = plt.subplots(figsize=(6, 2))
ax1.set_xlim(-50, 50)
ax1.set_ylim(-2, 2)
ax1.set_title("광원, 렌즈, 행성, 관측자 위치도")
ax1.get_yaxis().set_visible(False)

# 렌즈
ax1.plot(lens_x, 0, 'black', marker='o', markersize=12, label="렌즈")

# 행성
if has_planet:
    ax1.plot(lens_x + planet_offset, 0, 'blue', marker='o', markersize=10, label="행성")

# 관측자
ax1.plot(observer_x, -1, 'green', marker='^', markersize=12, label="관측자")

# 광원 예시
ax1.plot(-20, 1, 'yellow', marker='*', markersize=20, label="광원")

ax1.legend()
st.pyplot(fig1)

# =======================
# 밝기 곡선 시각화
# =======================
fig2, ax2 = plt.subplots()
ax2.plot(source_positions, brightness_values, color='orange', linewidth=2)
ax2.set_title("관측자가 측정한 밝기 (현실적 곡선)")
ax2.set_xlabel("광원 위치 (시간 흐름)")
ax2.set_ylabel("밝기")
ax2.grid(True)

st.pyplot(fig2)
