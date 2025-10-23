import pandas as pd

df = pd.read_csv('big_data_set1_f.csv', encoding='cp949')

# 주소를 길/로 or 동 단위로 끊어서 추출
def extract_area(address):
    parts = address.split()
    # 주소 끝부분에서부터 탐색
    for part in reversed(parts):
        if '길' in part or '로' in part:
            return part
    for part in reversed(parts):
        if '동' in part:
            return part
    return ' 기타'

# 추출된 파트끼리 묶어 최빈값 구한 후 결측치 최빈값으로 채우기
def fill_missing_values(area):
    # 결측치가 없거나 최빈값을 구할 수 없는 경우
    if area.isnull().all():
        return area
    # 최빈값 계산해서 결측치 채우기
    mode_val = area.mode().iloc[0]
    return area.fillna(mode_val)

# 추출한 파트 'divied_area'에 저장
df['divied_area'] = df['mct_bse_ar'].apply(extract_area)
df['hpsn_mct_bzn_cd_nm'] = df.groupby('divied_area')['hpsn_mct_bzn_cd_nm'].transform(fill_missing_values)

# 최종 결과를 저장
df.to_csv('big_data_set1_f.csv', index=False, encoding='cp949')

print("작업이 완료되었습니다. 'big_data_set1_f.csv' 파일을 확인해주세요.")