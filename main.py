import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="중력 렌즈 시뮬레이터 (광원 반대편 밝기 차단 + 그래프)", layout="wide")
st.title("🔭 중력 렌즈 효과 시뮬레이터 (광원 반대편 밝기 없음)")

# 사용자 입력
has_planet = st.checkbox("렌즈에 행성 포함", value=False)
lens_radius = st.slider("항성 렌즈 효과 반지름", 1.0, 10.0, 3.0, step=0.5)
planet_radius = st.slider("행성 렌즈 효과 반지름", 1.0, 10.0, 3.0, step=0.5)
planet_orbit_offset = 5  # 행성은 렌즈 기준 x축 방향으로 +5 떨어짐

# 광원 위치 (원점)
source_x, source_y = 0, 0

# 렌즈 궤도 반지름
orbit_radius = st.slider("렌즈 공전 궤도 반지름", 10, 50, 30)
# 관측자 위치 (궤도 뒤, y축 음수 방향으로 충분히 멀리)
observer_x, observer_y = 0, -orbit_radius - 20

# 시간 각도 (도)
t_deg = st.slider("시간 (t): 각도 (도)", 0, 360, 0)
t = np.radians(t_deg)

# 렌즈 위치
lens_x = orbit_radius * np.cos(t)
lens_y = orbit_radius * np.sin(t)

# 행성 위치
if has_planet:
    planet_x = lens_x + planet_orbit_offset
    planet_y = lens_y
else:
    planet_x = None
    planet_y = None

def distance(x1, y1, x2, y2):
    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def vector(a_x, a_y, b_x, b_y):
    return np.array([b_x - a_x, b_y - a_y])

def compute_brightness(observer_x, observer_y, source_x, source_y, lens_x, lens_y,
                       planet_x=None, planet_y=None, lens_r=3.0, planet_r=3.0):
    obs_to_src = vector(observer_x, observer_y, source_x, source_y)
    obs_to_lens = vector(observer_x, observer_y, lens_x, lens_y)
    cos_theta = np.dot(obs_to_src, obs_to_lens) / (np.linalg.norm(obs_to_src)*np.linalg.norm(obs_to_lens) + 1e-9)

    if cos_theta > 0 and np.linalg.norm(obs_to_lens) < np.linalg.norm(obs_to_src):
        abx, aby = obs_to_src
        ab_len2 = abx*abx + aby*aby
        apx, apy = lens_x - observer_x, lens_y - observer_y
        dot = apx*abx + apy*aby
        t_param = dot / ab_len2
        proj_x = observer_x + abx * t_param
        proj_y = observer_y + aby * t_param
        impact_dist = distance(lens_x, lens_y, proj_x, proj_y)
        lens_amp = 1 + 0.8 * np.exp(- (impact_dist / lens_r) ** 2)
    else:
        lens_amp = 1

    amp = lens_amp

    if planet_x is not None and planet_y is not None:
        obs_to_planet = vector(observer_x, observer_y, planet_x, planet_y)
        cos_theta_p = np.dot(obs_to_src, obs_to_planet) / (np.linalg.norm(obs_to_src)*np.linalg.norm(obs_to_planet) + 1e-9)

        if cos_theta_p > 0 and np.linalg.norm(obs_to_planet) < np.linalg.norm(obs_to_src):
            dot_p = (planet_x - observer_x)*abx + (planet_y - observer_y)*aby
            t_param_p = dot_p / ab_len2
            proj_x_p = observer_x + abx * t_param_p
            proj_y_p = observer_y + aby * t_param_p
            impact_dist_p = distance(planet_x, planet_y, proj_x_p, proj_y_p)
            planet_amp = 0.3 * np.exp(- (impact_dist_p / planet_r) ** 2)
        else:
            planet_amp = 0
        amp += planet_amp

    dist_obs_src = distance(observer_x, observer_y, source_x, source_y)
    brightness = amp / (dist_obs_src**2 + 1)
    return min(brightness, 2.5)

brightness = compute_brightness(observer_x, observer_y, source_x, source_y, lens_x, lens_y,
                                planet_x, planet_y, lens_radius, planet_radius)

# 한 화면에 위치도와 밝기 곡선 함께 출력
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14,6))

# --- 위치도 ---
ax1.set_title(f"렌즈 공전 궤도 및 위치 (t={t_deg}도)")
ax1.set_xlim(-orbit_radius-30, orbit_radius+30)
ax1.set_ylim(-orbit_radius-40, orbit_radius+30)
ax1.set_aspect('equal')
circle = plt.Circle((0,0), orbit_radius, color='gray', linestyle='dotted', fill=False)
ax1.add_artist(circle)
ax1.plot(source_x, source_y, 'yellow', marker='*', markersize=20, label="광원 (고정)")
ax1.plot(lens_x, lens_y, 'black', marker='o', markersize=14, label="렌즈")
if has_planet:
    ax1.plot(planet_x, planet_y, 'blue', marker='o', markersize=10, label="행성")
ax1.plot(observer_x, observer_y, 'green', marker='^', markersize=14, label="관측자 (고정)")
ax1.legend(loc="upper right")
ax1.grid(True)

# --- 밝기 곡선 ---
angles = np.linspace(0, 2*np.pi, 360)
brightness_vals = []
for angle in angles:
    lx = orbit_radius * np.cos(angle)
    ly = orbit_radius * np.sin(angle)
    px = lx + planet_orbit_offset if has_planet else None
    py = ly if has_planet else None
    b = compute_brightness(observer_x, observer_y, source_x, source_y, lx, ly, px, py, lens_radius, planet_radius)
    brightness_vals.append(b)

ax2.plot(np.degrees(angles), brightness_vals, color='orange', linewidth=2)
ax2.axvline(t_deg, color='red', linestyle='--', label="현재 각도")
ax2.set_xlabel("렌즈 각도 (도)")
ax2.set_ylabel("측정 밝기")
ax2.set_title("렌즈 각도에 따른 밝기 변화 (광원 반대편 밝기 없음)")
ax2.legend()
ax2.grid(True)

st.pyplot(fig)

# 밝기 텍스트 출력
st.write(f"현재 밝기: {brightness:.5f}")
