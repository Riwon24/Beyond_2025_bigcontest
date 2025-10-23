import os
import pandas as pd
import numpy as np

# 데이터셋 불러옴
script_dir = os.path.dirname(os.path.abspath(__file__))

file_store = os.path.join(script_dir, 'big_data_set1_f.csv')
file_performance = os.path.join(script_dir, 'big_data_set2_f.csv')
file_customer = os.path.join(script_dir, 'big_data_set3_f.csv')

df_store = pd.read_csv(file_store, encoding='cp949')
df_performance = pd.read_csv(file_performance, encoding='cp949')
df_customer = pd.read_csv(file_customer, encoding='cp949')

# 1-1. 컬럼명 소문자 + 언더스코어로 통일
df_store.columns = [str(col).strip().lower().replace(" ", "_") for col in df_store.columns]
df_performance.columns = [str(col).strip().lower().replace(" ", "_") for col in df_performance.columns]
df_customer.columns = [str(col).strip().lower().replace(" ", "_") for col in df_customer.columns]

# 1-2. 날짜 컬럼 파싱
df_store['are_d'] = pd.to_datetime(df_store['are_d'], format='%Y%m%d', errors='coerce')
df_store['mct_me_d'] = pd.to_datetime(df_store['mct_me_d'], format='%Y%m%d', errors='coerce')
df_performance['ta_ym'] = pd.to_datetime(df_performance['ta_ym'], format='%Y%m', errors='coerce')
df_customer['ta_ym'] = pd.to_datetime(df_customer['ta_ym'], format = '%Y%m', errors= 'coerce')

# 1-3. 결측값 처리 (dataset2,3의 문자열 결측치는 빈 문자열로)
# dataset1의 문자열 결측치는 np.nan으로
df_store.replace("", np.nan, inplace=True)
df_performance.fillna("", inplace=True)
df_customer.fillna("", inplace=True)

# 변경된 DataFrame을 CSV 파일로 저장
df_store.to_csv(file_store, index=False, encoding='cp949')
df_performance.to_csv(file_performance, index=False, encoding='cp949')
df_customer.to_csv(file_customer, index=False, encoding='cp949')
