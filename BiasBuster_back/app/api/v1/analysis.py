# app/api/v1/analysis.py
from fastapi import APIRouter, HTTPException
from app.core.models import AnalyzeTextRequest, AnalysisResult, HealthCheckResponse
from app.services.ml_service import MLService
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

try:
    ml_service = MLService(model_path=settings.MODEL_PATH)
    logger.info(f"AI 모델 로드 성공: {settings.MODEL_PATH}")
except Exception as e:
    logger.error(f"AI 모델 로드 실패: {e}")


@router.post("/analyze", response_model=AnalysisResult)
async def analyze_text(request: AnalyzeTextRequest):
    """
    제공된 텍스트의 편향성을 분석합니다.
    """
    try:
        analysis_result = ml_service.analyze_bias(request.text)
        logger.info(f"텍스트 분석 완료: {request.text[:50]}...")
        return AnalysisResult(**analysis_result)
    except Exception as e:
        logger.error(f"텍스트 분석 중 오류 발생: {e}")
        raise HTTPException(status_code=500, detail=f"텍스트 분석 중 오류가 발생했습니다: {e}")

@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    API 서버의 상태를 확인합니다.
    """
    return HealthCheckResponse(status="ok", version=settings.PROJECT_VERSION)