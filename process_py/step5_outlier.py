import pandas as pd
import numpy as np
import re

# 1. 파일 불러오기
df = pd.read_csv('main_set_f.csv', encoding='cp949')

# 2. 이상치 상권 빈값으로 채우기
target_values = ['압구정로데오', '풍산지구', '오남', '미아사거리',
                  '화양시장', '방배역', '서면역']

df['hpsn_mct_bzn_cd_nm'] = df['hpsn_mct_bzn_cd_nm'].replace(target_values, np.nan)

def extract_area_improved(address):
    # 주소 끝부분의 마침표 제거
    address = address.strip().rstrip('.')
    
    # 1. '길/로' 패턴 추출
    road_match = re.search(r'([가-힣\d]+(길|로))', address)
    if road_match:
        # 찾은 패턴 전체를 반환
        return road_match.group(1)

    # 2. '동' 패턴 추출
    dong_match = re.search(r'([가-힣\d]+동)', address)
    if dong_match:
        # '동' 단위만 추출하고, 뒤에 붙은 불필요한 번지 등은 제거
        return dong_match.group(1)

    # 3. 위 패턴에 해당하지 않는 경우
    return '기타'

# 추출된 파트끼리 묶어 최빈값 구한 후 결측치 최빈값으로 채우기
def fill_missing_values(area):
    # 결측치가 없거나 최빈값을 구할 수 없는 경우
    if area.isnull().all():
        return area
    # 최빈값 계산해서 결측치 채우기
    mode_val = area.mode().iloc[0]
    return area.fillna(mode_val)

df['divied_area'] = df['mct_bse_ar'].apply(extract_area_improved)
df['hpsn_mct_bzn_cd_nm'] = df.groupby('divied_area')['hpsn_mct_bzn_cd_nm'].transform(fill_missing_values)

# 최종 결과를 csv에 저장
df.to_csv('main_set_f.csv', index=False, encoding='cp949')