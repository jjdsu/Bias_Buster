# scripts/train_model.py
import pandas as pd
import os
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import numpy as np
import torch

# 1. 데이터 로드 경로 설정 (프로젝트 루트 기준)
script_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(script_dir, '..'))

train_data_path = os.path.join(project_root, 'data', 'processed', 'train.csv')
test_data_path = os.path.join(project_root, 'data', 'processed', 'test.csv')
model_output_dir = os.path.join(project_root, 'data', 'models', 'political_bias_model')

# Ensure output directory exists
os.makedirs(model_output_dir, exist_ok=True)

# 2. 전처리된 데이터 로드
try:
    train_df = pd.read_csv(train_data_path)
    test_df = pd.read_csv(test_data_path)
except FileNotFoundError:
    print("Error: Processed train/test data not found. Please run preprocess_train.py and preprocess_test.py first.")
    exit()

# 3. HuggingFace Dataset으로 변환
# content와 label 컬럼만 사용
train_dataset = Dataset.from_pandas(train_df[['content', 'label']])
test_dataset = Dataset.from_pandas(test_df[['content', 'label']])

# 4. 토크나이저 및 전처리
tokenizer = AutoTokenizer.from_pretrained("klue/roberta-base")

def preprocess_function(examples):
    # 'title' 컬럼도 있었다면, 제목과 본문을 결합하여 더 많은 정보를 모델에 제공할 수 있습니다.
    # 예: return tokenizer(examples["title"] + " " + examples["content"], truncation=True, padding="max_length", max_length=512)
    return tokenizer(examples["content"], truncation=True, padding="max_length", max_length=512)

# map 함수 적용 시 'remove_columns'를 사용하여 불필요한 원본 컬럼 제거 (메모리 효율)
train_dataset = train_dataset.map(preprocess_function, batched=True, remove_columns=['content'])
test_dataset = test_dataset.map(preprocess_function, batched=True, remove_columns=['content'])

# 'label' 컬럼을 'labels'로 변경 (Hugging Face Trainer의 기본 기대값)
# 이미 label 컬럼이 있으므로 rename_column만 필요
train_dataset = train_dataset.rename_column("label", "labels")
test_dataset = test_dataset.rename_column("label", "labels")

# 'labels' 컬럼의 데이터 타입을 PyTorch 텐서에 맞게 설정 (int)
train_dataset.set_format(type='torch', columns=['input_ids', 'attention_mask', 'labels'])
test_dataset.set_format(type='torch', columns=['input_ids', 'attention_mask', 'labels'])

# 5. 모델 로딩
# num_labels는 전처리된 데이터의 실제 클래스 수(0, 1, 2 -> 3개)와 일치해야 합니다.
model = AutoModelForSequenceClassification.from_pretrained("klue/roberta-base", num_labels=3)

# 6. 학습 설정 (compute_metrics 추가)
def compute_metrics(p):
    predictions = np.argmax(p.predictions, axis=1)
    accuracy = accuracy_score(p.label_ids, predictions)
    # F1-score는 클래스 불균형에 강건하므로, average='weighted'로 사용
    precision, recall, f1, _ = precision_recall_fscore_support(p.label_ids, predictions, average='weighted')
    return {
        'accuracy': accuracy,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }

training_args = TrainingArguments(
    output_dir=model_output_dir,
    eval_strategy="epoch",
    save_strategy="epoch",
    logging_dir=os.path.join(project_root, 'logs'), # logs 폴더도 프로젝트 루트 아래에
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_steps=10,
    save_total_limit=1, # 가장 좋은 모델만 저장
    load_best_model_at_end=True, # 학습 종료 시 최고의 모델 로드
    metric_for_best_model="eval_loss", # 최고의 모델 선택 기준
    report_to="none" # wandb 등 다른 로깅 시스템 사용하지 않을 경우
)

# 7. 트레이너 구성 및 학습 시작
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    compute_metrics=compute_metrics # 평가 지표 계산 함수 추가
)

print("Starting model training...")
trainer.train()
print("Model training completed.")

# 학습이 끝난 후, 최종 모델을 명시적으로 저장 (load_best_model_at_end=True이므로 베스트 모델이 저장됨)
# trainer.save_model(model_output_dir) # Trainer가 자동으로 수행하므로, 명시적으로 호출할 필요 없음.
tokenizer.save_pretrained(model_output_dir) # 토크나이저도 함께 저장    

print(f"Best model and tokenizer saved to: {model_output_dir}")