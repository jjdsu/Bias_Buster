# app/services/ml_service.py
import pickle
import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class MLService:
    def __init__(self, model_path: str):
        self.model = self._load_model(model_path)
        self.tokenizer = None 

    def _load_model(self, model_path: str):
        """
        지정된 경로에서 AI 모델을 로드합니다.
        실제 AI 모델 로딩 로직을 여기에 구현해야 합니다.
        """
        if not os.path.exists(model_path):
            logger.warning(f"모델 파일이 존재하지 않습니다: {model_path}. 더미 모델을 로드합니다.")
            return self._create_dummy_model()

        try:
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            logger.info(f"모델을 성공적으로 로드했습니다: {model_path}")
            return model
        except Exception as e:
            logger.error(f"모델 로드 중 오류 발생 ({model_path}): {e}")
            logger.warning("더미 모델을 로드합니다.")
            return self._create_dummy_model()

    def _create_dummy_model(self):
        """
        모델 로드 실패 시 또는 테스트를 위한 더미 모델을 생성합니다.
        """
        logger.info("더미 ML 모델을 생성합니다.")
        class DummyModel:
            def predict(self, text: str) -> str:
                if "정부" in text and "비판" in text:
                    return "우편향"
                elif "시민단체" in text and "옹호" in text:
                    return "좌편향"
                return "중립"

            def predict_proba(self, text: str) -> Dict[str, float]:
                # 더미 확률
                bias_type = self.predict(text)
                if bias_type == "우편향":
                    return {"중립": 0.2, "좌편향": 0.1, "우편향": 0.7}
                elif bias_type == "좌편향":
                    return {"중립": 0.2, "좌편향": 0.7, "우편향": 0.1}
                return {"중립": 0.8, "좌편향": 0.1, "우편향": 0.1}

        return DummyModel()

    def analyze_bias(self, text: str) -> Dict[str, Any]:
        """
        입력된 텍스트의 편향성을 분석합니다.
        실제 AI 모델 예측 로직을 여기에 구현해야 합니다.
        """
        if not self.model:
            raise RuntimeError("ML 모델이 로드되지 않았습니다.")

        predicted_category = self.model.predict(text)
        predicted_proba = self.model.predict_proba(text)

        bias_score = round(max(predicted_proba.values()) * 100, 2)
        if predicted_category == "중립":
            bias_score = 50.0 

        keywords = []
        if "정부" in text: keywords.append("정부")
        if "시민단체" in text: keywords.append("시민단체")
        if "비판" in text: keywords.append("비판")
        if "옹호" in text: keywords.append("옹호")


        return {
            "bias_score": bias_score,
            "bias_category": predicted_category,
            "keywords": keywords,
            "detailed_analysis": {"probabilities": predicted_proba}
        }