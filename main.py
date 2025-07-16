import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="중력 렌즈 시뮬레이터 (자동 공전)", layout="wide")
st.title("🔭 중력 렌즈 효과 시뮬레이터 (자동 공전 모드)")

# 사용자 입력
has_planet = st.checkbox("렌즈에 행성 포함", value=False)
lens_radius = st.slider("항성 렌즈 효과 반지름", 1.0, 10.0, 3.0, step=0.5)
planet_radius = st.slider("행성 렌즈 효과 반지름", 1.0, 10.0, 3.0, step=0.5)

planet_orbit_radius = st.slider("행성 공전 궤도 반경 (렌즈 기준)", 1, 20, 5)
planet_orbit_speed_ratio = st.slider("행성 공전 속도 비율 (렌즈 대비)", 1.1, 10.0, 3.0, 0.1)  # 렌즈 공전 속도보다 빠르게

# 공전 속도 조절 (각도 증가량) - 작게 해서 부드럽게
orbit_speed = st.slider("렌즈 공전 속도 (각도 증가량)", 0.1, 30.0, 0.5, step=0.1)

# 광원 위치 (원점)
source_x, source_y = 0, 0

# 렌즈 궤도 반지름
orbit_radius = st.slider("렌즈 공전 궤도 반지름", 10, 50, 30)
# 관측자 위치 (궤도 뒤, y축 음수 방향으로 충분히 멀리)
observer_x, observer_y = 0, -orbit_radius - 20

auto_run = st.checkbox("자동 공전 시작", value=False)

def distance(x1, y1, x2, y2):
    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def vector(a_x, a_y, b_x, b_y):
    return np.array([b_x - a_x, b_y - a_y])

def compute_brightness(observer_x, observer_y, source_x, source_y, lens_x, lens_y,
                       planet_x=None, planet_y=None, lens_r=3.0, planet_r=3.0):
    obs_to_src = vector(observer_x, observer_y, source_x, source_y)
    obs_to_lens = vector(observer_x, observer_y, lens_x, lens_y)
    cos_theta = np.dot(obs_to_src, obs_to_lens) / (np.linalg.norm(obs_to_src)*np.linalg.norm(obs_to_lens) + 1e-9)

    abx, aby = obs_to_src
    ab_len2 = abx*abx + aby*aby

    if cos_theta > 0 and np.linalg.norm(obs_to_lens) < np.linalg.norm(obs_to_src):
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

placeholder = st.empty()

angle_deg = 0  # 초기 각도

while auto_run:
    with placeholder.container():
        t = np.radians(angle_deg)
        lens_x = orbit_radius * np.cos(t)
        lens_y = orbit_radius * np.sin(t)

        if has_planet:
            # 행성은 렌즈 위치를 중심으로 빠르게 공전
            planet_angle = angle_deg * planet_orbit_speed_ratio
            pt = np.radians(planet_angle)
            planet_x = lens_x + planet_orbit_radius * np.cos(pt)
            planet_y = lens_y + planet_orbit_radius * np.sin(pt)
        else:
            planet_x = None
            planet_y = None

        brightness = compute_brightness(observer_x, observer_y, source_x, source_y, lens_x, lens_y,
                                        planet_x, planet_y, lens_radius, planet_radius)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14,6))

        # 위치도
        ax1.set_title(f"렌즈와 행성 공전 궤도 및 위치 (t={angle_deg:.1f}도)")
        ax1.set_xlim(-orbit_radius - planet_orbit_radius - 30, orbit_radius + planet_orbit_radius + 30)
        ax1.set_ylim(-orbit_radius - planet_orbit_radius - 40, orbit_radius + planet_orbit_radius + 30)
        ax1.set_aspect('equal')
        # 렌즈 궤도
        circle = plt.Circle((0, 0), orbit_radius, color='gray', linestyle='dotted', fill=False)
        ax1.add_artist(circle)
        # 행성 궤도
        if has_planet:
            inner_circle = plt.Circle((lens_x, lens_y), planet_orbit_radius, color='gray', linestyle='dashdot', fill=False)
            ax1.add_artist(inner_circle)

        ax1.plot(source_x, source_y, 'yellow', marker='*', markersize=20, label="광원 (고정)")
        ax1.plot(lens_x, lens_y, 'black', marker='o', markersize=14, label="렌즈")
        if has_planet:
            ax1.plot(planet_x, planet_y, 'blue', marker='o', markersize=10, label="행성")
        ax1.plot(observer_x, observer_y, 'green', marker='^', markersize=14, label="관측자 (고정)")
        ax1.legend(loc="upper right")
        ax1.grid(True)

        # 밝기 곡선
        angles = np.linspace(0, 2 * np.pi, 360)
        brightness_vals = []
        for angle in angles:
            lx = orbit_radius * np.cos(angle)
            ly = orbit_radius * np.sin(angle)
            if has_planet:
                planet_angle = np.degrees(angle) * planet_orbit_speed_ratio
                pt = np.radians(planet_angle)
                px = lx + planet_orbit_radius * np.cos(pt)
                py = ly + planet_orbit_radius * np.sin(pt)
            else:
                px = None
                py = None
            b = compute_brightness(observer_x, observer_y, source_x, source_y, lx, ly, px, py, lens_radius, planet_radius)
            brightness_vals.append(b)

        ax2.plot(np.degrees(angles), brightness_vals, color='orange', linewidth=2)
        ax2.axvline(angle_deg, color='red', linestyle='--', label="현재 각도")
        ax2.set_xlabel("렌즈 각도 (도)")
        ax2.set_ylabel("측정 밝기")
        ax2.set_title("렌즈 각도에 따른 밝기 변화")
        ax2.legend()
        ax2.grid(True)

        st.pyplot(fig)
        st.write(f"현재 밝기: {brightness:.5f}")

    angle_deg = (angle_deg + orbit_speed) % 360  # 각도 증가량 조절 (작게 해서 부드럽게)
    time.sleep(0.01)  # 0.05초 대기 (더 빠르고 부드럽게)
