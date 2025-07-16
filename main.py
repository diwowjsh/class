import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="중력 렌즈 시뮬레이터 애니메이션", layout="centered")
st.title("🔭 중력 렌즈 효과 시뮬레이터 - 자동 움직임 애니메이션")

# 사용자 입력
source_x = st.slider("광원 위치 (x축)", -50, 50, -30, step=1)
has_planet = st.checkbox("렌즈에 행성 포함", value=False)
lens_radius = st.slider("항성 렌즈 효과 반지름", 1.0, 10.0, 3.0, step=0.5)
planet_radius = st.slider("행성 렌즈 효과 반지름", 1.0, 10.0, 3.0, step=0.5)
planet_offset = 5  # 행성 위치 오프셋
observer_x = 0

def compute_brightness(lens_x, source_x, planet_x=None, lens_r=3.0, planet_r=3.0):
    lens_dist = abs(source_x - lens_x)
    brightness = 1 + 0.8 * np.exp(- (lens_dist / lens_r) ** 2)
    if planet_x is not None:
        planet_dist = abs(source_x - planet_x)
        brightness += 0.3 * np.exp(- (planet_dist / planet_r) ** 2)
    return min(brightness, 2.5)

# 렌즈가 왼쪽(-50)에서 오른쪽(50)으로 갔다가 다시 왼쪽으로 움직이는 x 위치 리스트 생성
positions_forward = np.linspace(-50, 50, 200)
positions_backward = np.linspace(50, -50, 200)
positions = np.concatenate([positions_forward, positions_backward])

# Streamlit에 위치도와 밝기 곡선 업데이트 할 공간 확보
pos_placeholder = st.empty()
brightness_placeholder = st.empty()

for lens_x in positions:
    planet_x = lens_x + planet_offset if has_planet else None
    brightness = compute_brightness(lens_x, source_x, planet_x, lens_radius, planet_radius)
    
    # 위치도 그리기
    fig1, ax1 = plt.subplots(figsize=(6, 2))
    ax1.set_xlim(-60, 60)
    ax1.set_ylim(-2, 2)
    ax1.set_title(f"위치도 (렌즈 위치: {lens_x:.2f})")
    ax1.get_yaxis().set_visible(False)
    
    ax1.plot(source_x, 1, 'yellow', marker='*', markersize=18, label="광원 (고정)")
    ax1.plot(observer_x, -1, 'green', marker='^', markersize=12, label="관측자 (고정)")
    ax1.hlines(0, -60, 60, colors='gray', linestyles='dashed')
    ax1.plot(lens_x, 0, 'black', marker='o', markersize=12, label="렌즈")
    if has_planet:
        ax1.plot(planet_x, 0, 'blue', marker='o', markersize=10, label="행성")
    ax1.legend(loc="upper right")
    
    # 밝기 곡선 전체
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
    
    # 업데이트
    pos_placeholder.pyplot(fig1)
    brightness_placeholder.pyplot(fig2)
    st.write(f"현재 밝기: {brightness:.3f}")
    
    time.sleep(0.05)  # 프레임 속도 조절 (0.05초 간격)
