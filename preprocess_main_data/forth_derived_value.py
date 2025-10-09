import os
import pandas as pd
import numpy as np

# 파일 불러오기
script_dir = os.path.dirname(os.path.abspath(__file__))

df = pd.read_csv('rank_quant_set_f.csv', encoding='cp949')

# 파생변수

# ------------------고객군 파생변수---------------------

# 1. 주요 고객군 추출 (최대 비중 컬럼명)
age_gender_cols = [col for col in df.columns if 'm12_mal_' in col or 'm12_fme_' in col]
df['main_group'] = df[age_gender_cols].astype(float).idxmax(axis=1)

# 2. 약한 고객군 추출 (업종 평균 - 10%)
df_gender_avg = df.groupby('hpsn_mct_zcd_nm')[age_gender_cols].mean()
main_threshold = df_gender_avg - 10

def find_low_groups(row):
    low_groups = []
    
    mct_type = row['hpsn_mct_zcd_nm']
    
    thresholds = main_threshold.loc[mct_type] 
    
    for col in age_gender_cols:
        if row[col] < thresholds[col]:
            low_groups.append(col)
    return low_groups

df['low_group'] = df.apply(find_low_groups, axis=1)

# 3. 단골손님 (재방문율 60% 이상)
regular_threshold = 60
df['regular_group'] = df['mct_ue_cln_reu_rat'].astype(float) >= regular_threshold

# 4. 신규 고객 약함 (신규 고객 비율 업종 내 하위 25%)
new_threshold = df.groupby('hpsn_mct_zcd_nm')['mct_ue_cln_new_rat'].quantile(0.25)

def is_new_weak(row):
    mct_type = row['hpsn_mct_zcd_nm']
    thresholds = new_threshold.loc[mct_type]
    return row['mct_ue_cln_new_rat'] <= thresholds

df['new_weak'] = df.apply(is_new_weak, axis=1)

# ----------------상권/입지/점유율 파생변수-----------------

# 1. 동네맛집 (거주 이용 고객 비율 50% 초과)
threshold = 50
df['is_local'] = df['rc_m1_shc_rsd_ue_cln_rat'].astype(float) > threshold

# 2. 업무지구 (직장 이용 고객 비율 50% 초과)
df['is_salary'] = df['rc_m1_shc_wp_ue_cln_rat'].astype(float) > threshold
