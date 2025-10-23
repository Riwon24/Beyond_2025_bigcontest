#전처리 폴더
---
##파일 구조

process_py       ← 전처리 과정 py파일, data 묶음 폴더
    ├── step1_conversion       
    ├── step2_missingvalue
    ├── step3_drop_and_merge
    ├── step4_scaling
    ├── step5_outlier
    ├── step6_outlier_mapping
    ├──step7_industry_reclassification
    └── step8_join_by_year
---
## 실행 순서
step1, 2, 3, 4, 5 실행
이상치 상권 매핑용 데이터 활용하여 step 6 실행
step 7, 8 실행
