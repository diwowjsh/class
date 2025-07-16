import numpy as np
import matplotlib.pyplot as plt

def create_gravitational_lens_image(
    source_x_pos,
    source_y_pos,
    lens_mass_factor,
    image_resolution=400,
    field_of_view_scale=0.01,
    gravitational_constant_effect=0.005,
    output_filename="gravitational_lens_simulation.png"
):
    """
    중력 렌즈 효과를 시뮬레이션하여 이미지 파일을 생성합니다.

    Args:
        source_x_pos (float): 광원의 X축 상대 위치 (렌즈 중앙 기준).
        source_y_pos (float): 광원의 Y축 상대 위치 (렌즈 중앙 기준).
        lens_mass_factor (float): 렌즈의 질량 강도를 나타내는 요소. 값이 클수록 렌즈 효과가 강해집니다.
        image_resolution (int): 생성될 이미지의 한 변 해상도 (픽셀). 예를 들어 400이면 400x400 픽셀 이미지.
        field_of_view_scale (float): 시뮬레이션 영역의 스케일. 픽셀당 실제 공간 단위를 결정합니다.
        gravitational_constant_effect (float): 중력 렌즈 효과의 전반적인 강도를 조절하는 상수.
                                               시각적 효과를 위해 조절됩니다 (실제 물리 상수 아님).
        output_filename (str): 생성될 이미지 파일의 이름 (예: "my_lens_image.png").
    """

    # 1. 시뮬레이션 그리드 설정
    # 이미지 해상도에 맞춰 X, Y 좌표 그리드를 생성합니다.
    # field_of_view_scale을 곱하여 픽셀 단위를 실제 공간 단위로 변환합니다.
    x_coords = np.linspace(-image_resolution / 2, image_resolution / 2, image_resolution) * field_of_view_scale
    y_coords = np.linspace(-image_resolution / 2, image_resolution / 2, image_resolution) * field_of_view_scale
    X, Y = np.meshgrid(x_coords, y_coords) # 모든 그리드 점의 X, Y 좌표 조합

    # 렌즈는 (0,0)에 위치한다고 가정합니다 (그리드의 중앙).
    lens_center_x, lens_center_y = 0, 0

    # 광원의 실제 위치 (시뮬레이션 공간 단위로 변환)
    actual_source_x = source_x_pos * field_of_view_scale
    actual_source_y = source_y_pos * field_of_view_scale

    # 2. 각 그리드 점에서 렌즈까지의 거리 계산
    # 빛이 렌즈를 향해 휘어지는 정도를 계산하기 위해 필요합니다.
    distance_to_lens = np.sqrt((X - lens_center_x)**2 + (Y - lens_center_y)**2)
    
    # 0으로 나누는 것을 방지하기 위해 매우 작은 값으로 대체합니다.
    distance_to_lens[distance_to_lens < 1e-9] = 1e-9

    # 3. 빛의 굴절 각도 계산 (매우 단순화된 모델)
    # 굴절 각도는 렌즈 질량에 비례하고 렌즈로부터의 거리에 반비례합니다.
    # gravitational_constant_effect는 시뮬레이션의 '휘어짐' 강도를 조절합니다.
    deflection_angle_magnitude = (lens_mass_factor * gravitational_constant_effect) / distance_to_lens

    # 4. 렌즈를 향하는 방향 벡터 계산
    # 각 그리드 점과 렌즈 중앙 사이의 각도를 계산합니다.
    angle_towards_lens = np.arctan2(Y - lens_center_y, X - lens_center_x)

    # 5. 관측자가 보는 광원의 겉보기 위치 (왜곡된 위치) 계산
    # 빛은 렌즈 질량에 의해 휘어지므로, 관측자는 실제 광원이 아닌
    # 휘어진 경로에 의해 생성된 '가상' 위치에서 오는 것처럼 봅니다.
    # 이 계산은 매우 단순화된 기하학적 근사입니다.
    apparent_source_x = X - deflection_angle_magnitude * np.cos(angle_towards_lens)
    apparent_source_y = Y - deflection_angle_magnitude * np.sin(angle_towards_lens)

    # 6. 겉보기 위치에서 광원의 밝기 계산 (가우시안 분포 가정)
    # 겉보기 위치가 실제 광원의 위치에 가까울수록 더 밝게 보입니다.
    # 0.02는 광원의 '크기' 또는 '번짐' 정도를 나타내는 표준편차입니다.
    source_spread = 0.02
    brightness_map = np.exp(-((apparent_source_x - actual_source_x)**2 +
                              (apparent_source_y - actual_source_y)**2) / (2 * source_spread**2))

    # 7. Matplotlib을 사용하여 이미지 생성 및 저장
    plt.figure(figsize=(6, 6)) # 6x6 인치 크기의 그림 생성
    
    # 밝기 맵을 이미지로 표시합니다.
    # cmap='hot': 뜨거운 색상 스케일 (어두운 곳은 검정, 밝은 곳은 노랑/흰색)
    # origin='lower': Y축 원점을 아래로 설정 (일반적인 좌표계와 일치)
    # extent: X, Y축의 실제 좌표 범위를 설정합니다.
    plt.imshow(brightness_map, cmap='hot', origin='lower',
               extent=[-image_resolution/2, image_resolution/2, -image_resolution/2, image_resolution/2])
    
    # 렌즈 위치를 파란색 점으로 표시
    plt.scatter(lens_center_x / field_of_view_scale, lens_center_y / field_of_view_scale,
                color='blue', s=200, alpha=0.6, label='Lens (Center)')
    
    # 실제 광원 위치를 빨간색 점으로 표시
    plt.scatter(source_x_pos, source_y_pos, color='red', s=50, label='Actual Source')
    
    # 그래프 제목 및 축 레이블 설정
    plt.title(f"Gravitational Lens Simulation\nMass Factor: {lens_mass_factor}, Source: ({source_x_pos}, {source_y_pos})")
    plt.xlabel("Relative X Position")
    plt.ylabel("Relative Y Position")
    
    plt.colorbar(label="Apparent Brightness") # 색상 바 추가
    plt.legend() # 범례 표시
    plt.grid(True, linestyle='--', alpha=0.7) # 그리드 표시
    plt.tight_layout() # 레이아웃 자동 조절
    
    # 이미지를 파일로 저장하고, 그림 객체를 닫아 메모리 해제
    plt.savefig(output_filename)
    plt.close()
    print(f"'{output_filename}' 이미지가 성공적으로 생성되었습니다.")

if __name__ == "__main__":
    print("중력 렌즈 효과 시뮬레이션 이미지 생성을 시작합니다...")

    # 예시 1: 아인슈타인 링 (광원이 렌즈 중앙에 매우 가까울 때)
    create_gravitational_lens_image(
        source_x_pos=0,
        source_y_pos=0,
        lens_mass_factor=50,
        output_filename="1_einstein_ring.png"
    )

    # 예시 2: 이중 이미지 (광원이 렌즈 옆에 있을 때)
    create_gravitational_lens_image(
        source_x_pos=70,
        source_y_pos=0,
        lens_mass_factor=30,
        output_filename="2_double_image.png"
    )

    # 예시 3: 약한 렌즈 효과 (광원이 렌즈에서 멀리 떨어져 있고 질량이 작을 때)
    create_gravitational_lens_image(
        source_x_pos=150,
        source_y_pos=80,
        lens_mass_factor=10,
        output_filename="3_weak_lens.png"
    )
    
    # 예시 4: 광원이 렌즈에 더 가깝고 질량이 강할 때 (더 큰 왜곡)
    create_gravitational_lens_image(
        source_x_pos=20,
        source_y_pos=-10,
        lens_mass_factor=80,
        output_filename="4_strong_distortion.png"
    )

    print("\n모든 중력 렌즈 시뮬레이션 이미지 생성이 완료되었습니다.")
