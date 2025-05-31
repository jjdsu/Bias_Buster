# scripts/predict_model.py
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os

# 모델 저장 경로 설정
script_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(script_dir, '..'))
model_path = os.path.join(project_root,'app', 'data', 'models', 'political_bias_model')

# 라벨 매핑 (학습 시 사용한 라벨과 동일하게)
# 0: 좌파/진보, 1: 중도, 2: 우파/보수
LABEL_MAP = {
    0: "좌파/진보",
    1: "중도",
    2: "우파/보수"
}

# 모델 로드 및 추론 함수
class PoliticalBiasPredictor:
    def __init__(self, model_path: str):
        try:
            print(f"Attempting to load model from: {model_path}")

            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model directory does not exist at: {model_path}")

            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model.to(self.device)
            self.model.eval() # 평가 모드로 설정
            print(f"Model and tokenizer loaded from {model_path} on {self.device}")
        except Exception as e:
            print(f"Error loading model from {model_path}: {e}")
            self.tokenizer = None
            self.model = None

    def predict_political_bias(self, text: str):
        if not self.model or not self.tokenizer:
            return {
                "predicted_bias_label": "Model Not Loaded",
                "predicted_bias_id": -1,
                "probability_distribution": []
            }

        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding="max_length",
            max_length=512
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probabilities = torch.nn.functional.softmax(logits, dim=-1)[0] # 배치에서 첫 번째 결과
        
        # 가장 높은 확률을 가진 라벨 ID
        predicted_class_id = torch.argmax(probabilities).item()
        
        # 라벨 이름 매핑
        predicted_bias_label = LABEL_MAP.get(predicted_class_id, "알 수 없음")
        
        return {
            "predicted_bias_label": predicted_bias_label,
            "predicted_bias_id": predicted_class_id, # 0, 1, 2
            "probability_distribution": probabilities.tolist() # 각 클래스에 대한 확률
        }

if __name__ == "__main__":
    predictor = PoliticalBiasPredictor(model_path)

    test_texts = [
        "정부는 서민 생활 안정을 위해 강력한 부동산 규제를 도입하고, 공공 주택 공급을 확대할 방침이다.", # 좌파성
        "현 정부의 경제 정책은 시장의 자율성을 침해하며, 기업 활동을 위축시켜 국가 경쟁력을 저해한다. 규제 완화와 감세가 필요하다.", # 우파성
        "오늘 국회에서는 여야가 팽팽하게 맞서며 예산안 심의가 진행되었다. 양측은 각자의 입장을 고수하며 타협점을 찾기 위한 노력을 계속하고 있다.", # 중도성
        "김건희 여사의 명품백 수수 의혹을 해명하기 위한 국정조사 요구에 야당은 강하게 압박하고 나섰다. 대통령실은 법적 절차에 따라 대응할 것이라는 입장만 되풀이하고 있다.", # 정치적 사건, 중도적 서술
        "윤석열 정부의 자유주의 경제 정책은 시대착오적이며, 빈부격차를 심화시켜 사회적 불평등을 초래할 것이다.", # 좌파성 비판
        "문재인 정권의 소득주도성장 정책은 실패했으며, 막대한 국가 부채만 남긴 채 국민들에게 실망을 안겨주었다." # 우파성 비판
    ]

    for i, text in enumerate(test_texts):
        print(f"\n--- Test Text {i+1} ---")
        print(f"Text: {text[:100]}...") # 긴 텍스트는 일부만 출력
        result = predictor.predict_political_bias(text)
        print(f"Predicted Bias: {result['predicted_bias_label']} (ID: {result['predicted_bias_id']})")
        print(f"Probabilities (Left/Center/Right): {result['probability_distribution']}")