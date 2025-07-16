import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="중력 렌즈 시뮬레이터 (공전 궤도)", layout="centered")
st.title("🔭 중력 렌즈 효과 시뮬레이터 (렌즈의 광원 공전)")

# 사용자 입력
has_planet = st.checkbox("렌즈에 행성 포함", value=False)
lens_radius = st.slider("항성 렌즈 효과 반지름", 1.0, 10.0, 3.0, step=0.5)
planet_radius = st.slider("행성 렌즈 효과 반지름", 1.0, 10.0, 3.0, step=0.5)
planet_orbit_offset = 5  # 행성은 렌즈 기준 x축 방향으로 +5 떨어짐

observer_x, observer_y = 0, -30  # 관측자 위치 (광원에서 아래쪽)

# 광원 위치 고정 (원점)
source_x, source_y = 0, 0

# 시간 슬라이더 (각도, 0 ~ 2pi)
t_deg = st.slider("시간 (t): 각도 (도)", 0, 360, 0)
t = np.radians(t_deg)

# 렌즈 공전 반지름
orbit_radius = st.slider("렌즈 공전 궤도 반지름", 10, 50, 30)

# 렌즈 위치 (원 궤도)
lens_x = orbit_radius * np.cos(t)
lens_y = orbit_radius * np.sin(t)

# 행성 위치 (렌즈 기준 +x 방향)
if has_planet:
    planet_x = lens_x + planet_orbit_offset
    planet_y = lens_y
else:
    planet_x = None
    planet_y = None

# 거리 계산 함수 (광원 ~ 렌즈/행성)
def distance(x1, y1, x2, y2):
    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

# 밝기 계산
def compute_brightness(source_x, source_y, lens_x, lens_y, planet_x=None, planet_y=None,
                       lens_r=3.0, planet_r=3.0):
    lens_dist = distance(source_x, source_y, lens_x, lens_y)
    brightness = 1 + 0.8 * np.exp(- (lens_dist / lens_r) ** 2)
    if planet_x is not None and planet_y is not None:
        planet_dist = distance(source_x, source_y, planet_x, planet_y)
        brightness += 0.3 * np.exp(- (planet_dist / planet_r) ** 2)
    return min(brightness, 2.5)

brightness = compute_brightness(source_x, source_y, lens_x, lens_y, planet_x, planet_y, lens_radius, planet_radius)

# =======================
# 위치도 시각화 (2D)
# =======================
fig, ax = plt.subplots(figsize=(6,6))
ax.set_title(f"렌즈의 광원 공전 (시간 t={t_deg}도)")
ax.set_xlim(-orbit_radius-15, orbit_radius+15)
ax.set_ylim(-orbit_radius-15, orbit_radius+15)
ax.set_aspect('equal')

# 공전 궤도 점선 표시
circle = plt.Circle((0,0), orbit_radius, color='gray', linestyle='dotted', fill=False)
ax.add_artist(circle)

# 광원
ax.plot(source_x, source_y, 'yellow', marker='*', markersize=20, label="광원 (고정)")

# 렌즈
ax.plot(lens_x, lens_y, 'black', marker='o', markersize=14, label="렌즈")

# 행성
if has_planet:
    ax.plot(planet_x, planet_y, 'blue', marker='o', markersize=10, label="행성")

# 관측자 (광원 아래쪽 고정)
ax.plot(observer_x, observer_y, 'green', marker='^', markersize=14, label="관측자 (고정)")

ax.legend(loc="upper right")
ax.grid(True)
st.pyplot(fig)

# =======================
# 밝기 출력
# =======================
st.write(f"현재 밝기: {brightness:.3f}")

# =======================
# 밝기 곡선: 렌즈 각도 변화에 따른 밝기
# =======================
angles = np.linspace(0, 2*np.pi, 360)
brightness_vals = []
for angle in angles:
    lx = orbit_radius * np.cos(angle)
    ly = orbit_radius * np.sin(angle)
    px = lx + planet_orbit_offset if has_planet else None
    py = ly if has_planet else None
    b = compute_brightness(source_x, source_y, lx, ly, px, py, lens_radius, planet_radius)
    brightness_vals.append(b)

fig2, ax2 = plt.subplots()
ax2.plot(np.degrees(angles), brightness_vals, color='orange', linewidth=2)
ax2.axvline(t_deg, color='red', linestyle='--', label="현재 각도")
ax2.set_xlabel("렌즈 각도 (도)")
ax2.set_ylabel("측정 밝기")
ax2.set_title("렌즈 각도에 따른 밝기 변화")
ax2.legend()
ax2.grid(True)
st.pyplot(fig2)
