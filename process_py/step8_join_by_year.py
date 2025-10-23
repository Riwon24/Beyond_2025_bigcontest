import pandas as pd
import numpy as np

# 1. 파일 불러오기
df = pd.read_csv('main_set_f.csv', encoding='cp949')

# 계산할 컬럼 (평균)과 대표값 (first)만 가져올 컬럼 구분
col_list = [
    'm12_mal_1020_rat', 'm12_mal_30_rat', 'm12_mal_40_rat',
    'm12_mal_50_rat', 'm12_mal_60_rat', 'm12_fme_1020_rat',
    'm12_fme_30_rat', 'm12_fme_40_rat', 'm12_fme_50_rat', 
    'm12_fme_60_rat', 'mct_ue_cln_reu_rat', 'mct_ue_cln_new_rat',
    'rc_m1_shc_rsd_ue_cln_rat', 'rc_m1_shc_wp_ue_cln_rat',
    'rc_m1_shc_flp_ue_cln_rat', 'mct_ope_ms_cn', 'rc_m1_saa',
    'rc_m1_to_ue_ct', 'rc_m1_ue_cus_cn', 'rc_m1_av_np_at',
    'apv_ce_rat', 'dlv_saa_rat', 'm1_sme_ry_saa_rat',
    'm1_sme_ry_cnt_rat', 'm12_sme_ry_saa_pce_rt', 'm12_sme_bzn_saa_pce_rt'
]

no_col = [
    'mct_bse_ar', 'mct_nm', 'mct_brd_num', 'hpsn_mct_zcd_nm',
    'hpsn_mct_bzn_cd_nm', 'new_area_with_public'
]

# 1-1. 'col_list' 컬럼들의 음수 값을 NaN으로 대체
df.loc[:, col_list] = df.loc[:, col_list].mask(df.loc[:, col_list] < 0, np.nan)


# 2. 기준년월 컬럼을 'year' 컬럼으로 변환 (연도별 그룹화 준비)
if 'ta_ym' in df.columns: 
    df['ta_ym'] = df['ta_ym'].astype(str).str[:4]

# 3. 결측치(NaN)가 5개 이상인 행(Row) 삭제 ------

# 3-1. 'col_list' 컬럼들 내에서 각 셀이 NaN인지 확인하는 불리언 데이터프레임 생성
nan_mask_df = df[col_list].isna()

# 3-2. 각 행(axis=1)별로 결측치(True)의 개수를 계산하여 임시 컬럼에 저장
df['nan_count'] = nan_mask_df.sum(axis=1)

# 3-3. 결측치의 개수가 5개 미만인 행만 선택 (5개 이상인 행은 삭제됨)
df = df[df['nan_count'] < 5].copy()

# 3-4. 임시로 생성한 'nan_count' 컬럼 삭제
del df['nan_count']
#---------------------------

# 4. 고유코드 및 연도별 그룹화 및 집계------

# 4-1. 집계 함수 딕셔너리 생성
agg_dict = {}

# 대표값(first)을 가져올 컬럼 추가
for col in no_col:
    agg_dict[col] = 'first'
# 평균을 낼 컬럼 추가 
for col in col_list:
    agg_dict[col] = 'mean'

    
# 4-2. 필요한 컬럼 묶음
group_keys = ['encoded_mct', 'ta_ym']
cols_to_select = group_keys + col_list + no_col

# 필요한 컬럼만 선택하고 복사본 생성
df_subset = df[cols_to_select].copy()

# 4-3. 그룹화 및 최종 집계
df_merged_final = df_subset.groupby(group_keys).agg(agg_dict).reset_index()

# 5. 최종 파일 새로운 csv 파일로 저장
df_merged_final.to_csv('new_final_set_f_yearly1022.csv', index=False, encoding='cp949')

# 결과 디버깅
print(f"최종 데이터프레임의 행 수: {df_merged_final.shape[0]}")
print(f"최종 데이터프레임의 컬럼 수: {df_merged_final.shape[1]}")