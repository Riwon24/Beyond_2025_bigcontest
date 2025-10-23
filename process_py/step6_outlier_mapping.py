import pandas as pd

# 1. 파일 불러오기
df = pd.read_csv('main_set_f.csv', encoding='cp949')
df2 = pd.read_csv('data_outlier_mapping.csv', encoding='cp949')

ADDRESS_COL_DF2 = '이상치_주소' # df2의 주소 컬럼
FILL_VALUE_COL_DF2 = '결측치_상권' # df2의 상권 컬럼
TARGET_COL_DF = 'hpsn_mct_bzn_cd_nm' # df에서 결측치를 채울 컬럼

# df2의 컬럼 이름을 매핑에 사용하기 편리하도록 변경
df2_cols_map = {
    ADDRESS_COL_DF2: TARGET_COL_DF + '_주소_매핑키',  # 병합 키가 될 임시 이름
    FILL_VALUE_COL_DF2: '매핑된_상권_값'
}

# 2. 매핑에 필요한 df2 데이터만 추출 및 컬럼 이름 변경
df2_map = df2[[ADDRESS_COL_DF2, FILL_VALUE_COL_DF2]].rename(columns=df2_cols_map).drop_duplicates()

# 3. 결측치 채우기 
DF_ADDRESS_KEY_COL = 'mct_bse_ar' 

# df와 df2_map을 '주소 키 컬럼'을 기준으로 병합
df_merged = df.merge(
    df2_map, 
    left_on=DF_ADDRESS_KEY_COL, 
    right_on=TARGET_COL_DF + '_주소_매핑키', 
    how='left'
)

# 3-2. 병합된 결과를 사용하여 TARGET_COL_DF('hpsn_mct_bzn_cd_nm')의 결측치 채움
df[TARGET_COL_DF] = df[TARGET_COL_DF].fillna(df_merged['매핑된_상권_값'])


# 4. 결과 저장
df.to_csv('main_set_f.csv', index=False, encoding='cp949')

print("결측치 매핑으로 채우기 완료")