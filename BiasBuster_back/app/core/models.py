# app/core/models.py
from pydantic import BaseModel, Field
from typing import List, Dict, Any

class AnalyzeTextRequest(BaseModel):
    """
    텍스트 분석 요청을 위한 Pydantic 모델.
    """
    text: str = Field(..., min_length=1, description="분석할 뉴스 기사 또는 텍스트 내용.")

class AnalysisResult(BaseModel):
    """
    텍스트 분석 결과를 위한 Pydantic 모델.
    """
    bias_score: float = Field(..., description="텍스트의 편향성 점수 (0~100).")
    bias_category: str = Field(..., description="텍스트의 편향성 범주 (예: '중립', '좌편향', '우편향').")
    keywords: List[str] = Field(default_factory=list, description="편향성을 나타내는 주요 키워드.")
    detailed_analysis: Dict[str, Any] = Field(default_factory=dict, description="더 상세한 분석 정보 (선택 사항).")

class HealthCheckResponse(BaseModel):
    """
    상태 체크 응답을 위한 Pydantic 모델.
    """
    status: str = Field(..., description="API 서버의 상태.")
    version: str = Field(..., description="API 버전.")