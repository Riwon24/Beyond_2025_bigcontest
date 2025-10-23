import os
import pandas as pd

# 데이터셋 불러옴
script_dir = os.path.dirname(os.path.abspath(__file__))

df = pd.read_csv('main_set_f.csv', encoding='cp949')

# 구간 문자열 → 중앙값 수치로 변환
rank_mapping1 = {
    '1_10%이하': 5,
    '2_10-25%': 17.5,
    '3_25-50%': 37.5,
    '4_50-75%': 62.5,
    '5_75-90%': 82.5,
    '6_90%초과(하위 10% 이하)': 95
}

# 변환할 대상 컬럼 리스트
target_cols1 = ['rc_m1_ue_cus_cn', 'rc_m1_av_np_at','mct_ope_ms_cn','rc_m1_saa','rc_m1_to_ue_ct']

rank_mapping2 = {
    '1_상위1구간': -1,
    '6_상위6구간(하위1구간)': 1
}

# 변환할 대상 컬럼 리스트
target_cols2 = ['apv_ce_rat']

# 변환 적용(원본 컬럼 대체)
for col in target_cols1:
    df[col] = df[col].map(rank_mapping1)
for col in target_cols2:
    df[col] = df[col].map(rank_mapping2)

# 최종 파일 저장
df.to_csv('main_set_f.csv', index=False, encoding='cp949')
print('완료되었습니다')