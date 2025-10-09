import os
import pandas as pd

# 데이터셋 불러옴
script_dir = os.path.dirname(os.path.abspath(__file__))

file_store = os.path.join(script_dir, 'filled_big_data_set1_f.csv')
file_performance = os.path.join(script_dir, 'big_data_set2_f.csv')
file_customer = os.path.join(script_dir, 'big_data_set3_f.csv')

df_store = pd.read_csv(file_store, encoding='cp949')
df_performance = pd.read_csv(file_performance, encoding='cp949')
df_customer = pd.read_csv(file_customer, encoding='cp949')

# 2번과 3번 데이터셋 가맹점 고유코드, 기준년월 겹치는 것끼리 병합
df_pre_merge = df_customer.merge(df_performance, on=["encoded_mct", "ta_ym"], how="inner")
# 2번 데이터셋에서 필요없는 컬럼 제거
columns_to_drop = ['m12_sme_ry_me_mct_rat','m12_sme_bzn_me_mct_rat']
df_pre_merge.drop(columns=columns_to_drop, inplace=True)

# 2,3 병합 셋과 1번 셋 통합
df_merge = df_store.merge(df_pre_merge, on=["encoded_mct"], how="right")
columns_to_d = ['mct_sigungu_nm', 'are_d', 'mct_me_d', 'divied_area']
df_merge.drop(columns=columns_to_d, inplace=True)

# 변경된 DataFrame을 CSV 파일로 저장
df_merge.to_csv('main_merged_set_f.csv', index=False, encoding='cp949')
