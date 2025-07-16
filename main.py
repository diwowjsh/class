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

    # 광원의 실제
