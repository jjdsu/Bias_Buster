# scripts/preprocess_test.py
import pandas as pd
import os

# 현재 스크립트 파일의 디렉토리 경로를 기준으로 상대 경로 설정
script_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(script_dir, '..'))

raw_data_path = os.path.join(project_root, 'data', 'raw', 'complete_test_stratified.csv')
processed_output_path = os.path.join(project_root, 'data', 'processed', 'test.csv')

try:
    df = pd.read_csv(raw_data_path, encoding='utf8')
except FileNotFoundError:
    print(f"Error: Raw data file not found at {raw_data_path}")
    print("Please ensure 'complete_test_stratified.csv' is in the 'data/raw/' directory.")
    exit()

# 필요한 컬럼만 선택
df = df[['title', 'content', 'label1', 'label2']]

# content와 label1에 결측치가 있는 행 제거
df = df.dropna(subset=['content', 'label1'])

# label1 (1~5)을 3개의 클래스 (0:좌, 1:중도, 2:우)로 매핑
def map_political_label(value):
    if value in [1, 2]: # 1:매우진보, 2:진보
        return 0 # 좌
    elif value == 3: # 3:중도
        return 1 # 중도
    elif value in [4, 5]: # 4:보수, 5:매우보수
        return 2 # 우
    else:
        return None # 유효하지 않은 값 처리

df['label'] = df['label1'].apply(map_political_label)

# 매핑 후 None이 된 행 제거
df = df.dropna(subset=['label'])
df['label'] = df['label'].astype(int) # label 컬럼을 정수형으로 변환

# content 텍스트 정제
df['content'] = df['content'].astype(str).str.replace('\n', ' ').str.strip()

# 전처리된 데이터를 CSV로 저장
df.to_csv(processed_output_path, index=False, encoding='utf8')

print(f"Test 데이터 전처리 완료. 저장 경로: {processed_output_path}")
print(f"최종 데이터 개수: {len(df)}")
print(f"라벨 분포:\n{df['label'].value_counts()}")