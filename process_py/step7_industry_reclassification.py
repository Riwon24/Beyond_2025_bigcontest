import pandas as pd

# 1. 파일 불러오기
df = pd.read_csv('main_set_f.csv', encoding='cp949')

SOURCE_COLUMN = 'hpsn_mct_zcd_nm'

# 1. 키 리스트로 정의
# 업종-한식
key_to_korean = ['한식-단품요리일반','백반/가정식','한식-육류/고기','한식-해물/생선',
                 '한식-국밥/설렁탕','기사식당','한식-두부요리','한식뷔페','한식-찌개/전골',
                 '한식-감자탕','한식-국수/만두','한식-냉면','한식-죽','한정식','도시락','구내식당/푸드코트']
new_korean = '한식음식점'

# 업종-제과점
key_to_bakery = ['베이커리','떡/한과','도너츠','마카롱','와플/크로플','떡/한과 제조','아이스크림/빙수','탕후루']
new_bakery = '제과점'

# 업종-패스트푸드점
key_to_fastfood = ['햄버거']
new_fastfood = '패스트푸드점'

# 업종-치킨전문점
key_to_chicken = ['치킨']
new_chicken = '치킨전문점'

# 업종-분식전문점
key_to_snackfood = ['포장마차','분식','샌드위치/토스트']
new_snackfood = '분식전문점'

# 업종-호프-간이주점
key_to_pub = ['호프/맥주','이자카야','와인바','민속주점','일반 유흥주점','요리주점','주류','룸살롱/단란주점','와인샵']
new_pub = '호프-간이주점'


# 업종-커피-음료
key_to_drink = ['커피전문점','카페','차','주스','테마카페','테이크아웃커피']
new_drink = '커피-음료'

# 업종-중식음식점
key_to_chinese = ['중식당','중식-딤섬/중식만두','중식-훠궈/마라탕']
new_chinese = '중식음식점'

# 업종-반찬가게
key_to_banchan = ['반찬']
new_banchan = '반찬가게'

# 업종-양식음식점
key_to_westernfood = ['양식','피자','스테이크']
new_westernfood = '양식음식점'

# 업종-일식음식점
key_to_japanese = ['일식당','일식-덮밥/돈가스','일식-초밥/롤','일식-우동/소바/라면',
                   '일식-샤브샤브','일식-참치회','꼬치구이']
new_japanese = '일식음식점'

#==============
# 기타-세계음식
key_to_otherfood = ['동남아/인도음식','기타세계요리']
new_otherfood = '기타_세계요리'

# 기타-식재료
key_to_other = ['식료품','축산물','미곡상','식품 제조','농산물','건강식품','건강원','유제품','인삼제품',
                 '건어물','청과물','수산물','담배']
new_other = '기타_식재료'


# 2. 새로운 값으로 매핑된 딕셔너리 생성
final_mapping_dict = {}

final_mapping_dict.update(dict.fromkeys(key_to_korean, new_korean))
final_mapping_dict.update(dict.fromkeys(key_to_bakery, new_bakery))
final_mapping_dict.update(dict.fromkeys(key_to_fastfood, new_fastfood))
final_mapping_dict.update(dict.fromkeys(key_to_chicken, new_chicken))
final_mapping_dict.update(dict.fromkeys(key_to_snackfood, new_snackfood))
final_mapping_dict.update(dict.fromkeys(key_to_pub, new_pub))
final_mapping_dict.update(dict.fromkeys(key_to_drink, new_drink))
final_mapping_dict.update(dict.fromkeys(key_to_chinese, new_chinese))
final_mapping_dict.update(dict.fromkeys(key_to_banchan, new_banchan))
final_mapping_dict.update(dict.fromkeys(key_to_westernfood, new_westernfood))
final_mapping_dict.update(dict.fromkeys(key_to_japanese, new_japanese))
final_mapping_dict.update(dict.fromkeys(key_to_otherfood, new_otherfood))
final_mapping_dict.update(dict.fromkeys(key_to_other, new_other))

# 변환할 대상 컬럼 리스트 및 저장할 컬럼명
SOURCE_COLUMN = 'hpsn_mct_zcd_nm' 
NEW_COLUMN = 'new_area_with_public' 

df[NEW_COLUMN] = df[SOURCE_COLUMN].map(final_mapping_dict)


# 최종 결과 저장
df.to_csv('main_set_f.csv', index=False, encoding='cp949')
