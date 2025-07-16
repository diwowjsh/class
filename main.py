import numpy as np
import matplotlib.pyplot as plt

def gravitational_lens_effect(source_x, source_y, lens_mass, grid_size=400, scale=0.01):
    """
    단순화된 중력 렌즈 효과를 시뮬레이션하여 이미지를 생성합니다.
    이 모델은 실제 물리 모델보다 시각적 효과를 위한 근사치입니다.
    """
    
    # 캔버스에 해당하는 그리드 생성
    x = np.linspace(-grid_size / 2, grid_size / 2, grid_size) * scale
    y = np.linspace(-grid_size / 2, grid_size / 2, grid_size) * scale
    X, Y = np.meshgrid(x, y)

    # 렌즈 위치 (중앙)
    lens_pos = np.array([0, 0])

    # 광원 위치
    source_pos = np.array([source_x * scale, source_y * scale])

    # 각 그리드 점에서 렌즈까지의 거리 계산
    dist_to_lens = np.sqrt(X**2 + Y**2)
    # 0으로 나누는 것을 방지
    dist_to_lens[dist_to_lens < 1e-6] = 1e-6

    # 굴절 각도 계산 (질량에 비례하고 거리에 반비례)
    # GRAVITATIONAL_CONSTANT는 시각적 효과를 위해 조절
    gravitational_constant_effect = 0.005 # 이 값을 조절하여 렌즈 효과 강도 변경
    alpha_r = (lens_mass * gravitational_constant_effect) / dist_to_lens

    # 렌즈를 향하는 단위 벡터 계산
    theta = np.arctan2(Y, X)
    
    # 왜곡된 광원 위치 (관측자가 보는 위치)
    # 이 부분은 빛이 렌즈 질량에 의해 휘어지는 것을 시뮬레이션합니다.
    # 단순화를 위해 광원 방향으로 굴절된 것처럼 처리합니다.
    deflected_x = X - alpha_r * np.cos(theta)
    deflected_y = Y - alpha_r * np.sin(theta)

    # 광원의 밝기 분포 (가우시안)
    # 광원이 실제 위치(source_pos)에 있을 때 가장 밝다고 가정
    source_brightness = np.exp(-((deflected_x - source_pos[0])**2 + \
                                  (deflected_y - source_pos[1])**2) / (2 * (0.02)**2))

    return source_brightness

def create_lens_image(source_x, source_y, lens_mass, filename="lens_effect.png"):
    """
    중력 렌즈 효과 이미지를 생성하고 파일로 저장합니다.
    """
    grid_size = 400
    brightness_map = gravitational_lens_effect(source_x, source_y, lens_mass, grid_size)

    plt.figure(figsize=(6, 6))
    plt.imshow(brightness_map, cmap='hot', origin='lower', extent=[-grid_size/2, grid_size/2, -grid_size/2, grid_size/2])
    
    # 렌즈 위치 (중앙)
    plt.scatter(0, 0, color='blue', s=200, alpha=0.6, label='Lens')
    
    # 실제 광원 위치 (빨간 점)
    plt.scatter(source_x, source_y, color='red', s=50, label='Actual Source')
    
    plt.title(f"Gravitational Lens Effect (Mass: {lens_mass}, Source: ({source_x}, {source_y}))")
    plt.xlabel("X Position")
    plt.ylabel("Y Position")
    plt.colorbar(label="Brightness")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close() # 메모리 절약

if __name__ == "__main__":
    # 예시 사용:
    print("중력 렌즈 효과 이미지 생성 중...")

    # 1. 아인슈타인 링 효과 (광원이 렌즈 중앙에 있을 때)
    create_lens_image(0, 0, 50, "einstein_ring.png")
    print("einstein_ring.png 생성 완료")

    # 2. 이중 이미지 효과 (광원이 렌즈 옆에 있을 때)
    create_lens_image(70, 0, 30, "double_image.png")
    print("double_image.png 생성 완료")

    # 3. 약한 렌즈 효과 (광원이 멀리 있고 질량이 작을 때)
    create_lens_image(150, 80, 10, "weak_lens.png")
    print("weak_lens.png 생성 완료")

    print("모든 이미지 생성이 완료되었습니다.")
