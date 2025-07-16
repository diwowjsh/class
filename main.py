import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="중력 렌즈 시뮬레이터", layout="centered")
st.title("🔭 중력 렌즈 효과 시뮬레이터 (광원 위치 조절 + 렌즈/행성 시간 이동)")

# 슬라이더 크기 조절 CSS
st.markdown(
    """
    <style>
    div[data-baseweb="slider"] {
        max-width: 300px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 유저 입력: 광원 위치, 렌즈/행성 반지름, 행성 포함 여부
source_x = st.slider("광원 위치 (x축)", -50, 50, -30, step=1)
has_planet = st.checkbox("렌즈에 행성 포함", value=False)
lens_radius = st.slider("항성 렌즈 효과 반지름", 1.0, 10.0, 3.0, step=0.5)
planet_radius = st.slider("행성 렌즈 효과 반지름", 1.0, 10.0, 3.0, step=0.5)
planet_offset = 5  # 행성은 렌즈에서 +5 오른쪽 고정

observer_x = 0  # 관측자 고정 위치

# 애니메이션 시간 변수 (t)
t = st.slider("시간 (t)", 0, 628, 0)  # 0 ~ 2π*100 (100단위 정밀도)

# 렌즈와 행성 위치를 시간에 따라 결정 (sin 함수로 움직임)
lens_x = 30 * np.sin(t / 100)
planet_x = lens_x + planet_offset if has_planet else None

def compute_brightness(lens_x, source_x, planet_x=None, lens_r=3.0, planet_r=3.0):
    lens_dist = abs(source_x - lens_x)
    brightness = 1 + 0.8 * np.exp(- (lens_dist / lens_r) ** 2)
    if planet_x is not None:
        planet_dist = abs(source_x - planet_x)
        brightness += 0.3 * np.exp(- (planet_dist / planet_r) ** 2)
    return min(brightness, 2.5)

brightness = compute_brightness(lens_x, source_x, planet_x, lens_radius, planet_radius)

# 위치도 시각화
fig1, ax1 = plt.subplots(figsize=(6, 2))
ax1.set_xlim(-50, 50)
ax1.set_ylim(-2, 2)
ax1.set_title(f"위치도 (t={t})")
ax1.get_yaxis().set_visible(False)

# 광원
ax1.plot(source_x, 1, 'yellow', marker='*', markersize=18, label="광원 (사용자 조절)")

# 관측자
ax1.plot(observer_x, -1, 'green', marker='^', markersize=12, label="관측자 (고정)")

# 렌즈 궤도 선
ax1.hlines(0, -50, 50, colors='gray', linestyles='dashed')

# 렌즈 현재 위치
ax1.plot(lens_x, 0, 'black', marker='o', markersize=12, label="렌즈")

# 행성 현재 위치
if has_planet:
    ax1.plot(planet_x, 0, 'blue', marker='o', markersize=10, label="행성")

ax1.legend(loc="upper right")
st.pyplot(fig1)

# 밝기 출력
st.write(f"현재 밝기: {brightness:.3f}")

# 밝기 곡선: 렌즈가 x=-50부터 50까지 움직일 때 밝기 변화 (참고용)
lens_positions = np.linspace(-50, 50, 500)
brightness_values = []
for lx in lens_positions:
    px = lx + planet_offset if has_planet else None
    b = compute_brightness(lx, source_x, px, lens_radius, planet_radius)
    brightness_values.append(b)

fig2, ax2 = plt.subplots()
ax2.plot(lens_positions, brightness_values, color='orange', linewidth=2)
ax2.axvline(x=lens_x, color='red', linestyle='--', label='현재 렌즈 위치')
ax2.set_title("밝기 곡선 (렌즈 위치에 따른 밝기)")
ax2.set_xlabel("렌즈 위치")
ax2.set_ylabel("측정 밝기")
ax2.grid(True)
ax2.legend()

st.pyplot(fig2)
