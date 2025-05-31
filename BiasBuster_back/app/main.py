# python -m uvicorn --app-dir app main:app --reload --host 0.0.0.0 --port 8001

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import os
import torch
import re 
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

political_bias_model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'models', 'political_bias_model')

bias_tokenizer = None
bias_model = None

SUMMARIZATION_MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'models', 'kobart_summarization_model')
summarizer_pipeline = None

LABEL_MAP = {
    0: "좌파/진보",
    1: "중도",
    2: "우파/보수"
}

app = FastAPI()


origins = [
    "http://localhost:8001",
    "chrome-extension://*", 
    "*" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ArticleRequest(BaseModel):
    text: str

class AnalysisScore(BaseModel):
    category: str  # 예: "보수", "진보", "중립"
    score: float   # 편향 점수 (예: 0.0 ~ 1.0)

class SuspiciousPoint(BaseModel):
    reason: str # 의심스러운 이유 (예: "인용 출처 불분명")
    phrase: str # 기사에서 탐지된 실제 문구
    note: str   # 해당 패턴에 대한 설명

class AnalysisResult(BaseModel):
    summary: str # 분석 결과에 대한 요약 문자열
    scores: List[AnalysisScore] # 카테고리별 편향 점수 리스트
    trust_issues: List[SuspiciousPoint] # 신뢰도 분석 결과 리스트 

@app.on_event("startup")
async def load_ai_models():
    global bias_tokenizer, bias_model, summarizer_pipeline
    print("AI 모델 및 토크나이저 로드 중...")
    try:
        if not os.path.exists(political_bias_model_path):
            raise FileNotFoundError(f"정치 편향 모델 경로를 찾을 수 없습니다: {political_bias_model_path}")

        bias_tokenizer = AutoTokenizer.from_pretrained(political_bias_model_path)
        bias_model = AutoModelForSequenceClassification.from_pretrained(political_bias_model_path)
        bias_model.eval() 
        print("정치 편향 분석 모델 로드 완료.")

    except Exception as e:
        print(f"AI 모델 로드 실패: {e}")
        raise RuntimeError(f"AI 모델 로드 중 심각한 오류 발생: {e}. 'train_model.py' 실행 및 모델 저장 경로를 확인하세요.")

def get_bias_scores(text: str) -> List[Dict[str, Any]]:
    """
    주어진 텍스트의 정치적 편향을 AI 모델로 분석하는 함수.
    """
    if bias_tokenizer is None or bias_model is None:
        raise RuntimeError("정치 편향 분석 모델 또는 토크나이저가 로드되지 않았습니다.")

    print(f"정치 편향 모델: 텍스트 분석 중... (길이: {len(text)})")

    inputs = bias_tokenizer(
        text,
        return_tensors="pt", 
        truncation=True,     
        padding="max_length",
        max_length=512   
    )

    with torch.no_grad():
        outputs = bias_model(**inputs)
        logits = outputs.logits 

    probabilities = torch.softmax(logits, dim=1).squeeze().tolist()

    bias_scores = []
    for i, score in enumerate(probabilities):
        category = LABEL_MAP.get(i, f"알 수 없는 카테고리_{i}") 
        bias_scores.append({"category": category, "score": float(score)}) 

    return bias_scores

def analyze_article_trust(article_text: str) -> List[Dict[str, str]]:
    """
    주어진 기사 텍스트에서 신뢰도를 떨어뜨릴 수 있는 의심스러운 지점을 탐지합니다.
    탐지된 각 지점에 대해 이유와 관련 문구, 설명을 반환합니다.
    """
    suspicious_points: List[Dict[str, str]] = []

    rules = {
        "인용 출처 불분명": [
            (r"\b관계자[는가]\s+말했다", "불분명한 '관계자' 인용. 구체적인 출처 명시 부족."),
            (r"\b전문가[들은는]?\s+(우려|경고|지적|분석했다|제기했다)", "익명 '전문가' 의견. 어떤 분야의 전문가인지, 혹은 신뢰할 수 있는 단체 소속인지 불분명."),
            (r"\b일각에서는", "'일각'이라는 불분명한 주체. 누가, 왜 그렇게 주장하는지 불명확."),
            (r"\b소식통[에따르면]?", "'소식통'이라는 불분명한 출처. 정보의 신빙성 확인 필요."),
            (r"\b익명의\s+[가-힣]+\s*에\s+따르면", "익명의 정보원 인용. 정보의 진위 확인 어려움."),
        ],
        "최신 정보 미반영 또는 오래된 데이터 사용": [
            (r"(20[0-1][0-9]|202[0-3])년(도)?\s*(기준|통계|자료|연구|조사)(에따르면)?", "2000년대~2023년 데이터 사용. 최신 정보가 아닐 수 있음."),
            (r"\b수년\s*전\b", "불분명한 과거 시점 언급. 정확한 시점 확인 필요."),
            (r"\b구체적인\s+날짜\s*없이\s+.*발표", "구체적 날짜 없는 발표 인용. 정보의 시점 및 맥락 확인 필요.")
        ],
        "공신력 낮은 매체 인용 또는 자가 출처": [
            (r"출처:\s*(자극적인뉴스|가짜뉴스일보|미확인방송|찌라시|커뮤니티|온라인\s*게시판)", "공신력 낮은 출처 인용. 정보의 신뢰성 검증 필요."),
            (r"\b(온라인|인터넷)\s*커뮤니티[에서는]?", "검증되지 않은 온라인 커뮤니티 인용. 루머나 왜곡된 정보일 가능성."),
            (r"\b(개인의\s*견해|주관적인\s*판단|일방적인\s*주장)\b", "객관성 부족한 서술. 사실이 아닌 개인의 의견 강조."),
            (r"(\b[가-힣]+[뉴스신문통신]|이\s*매체는)\s+단독보도했다", "매체 자체의 단독 보도 강조. 교차 검증을 통해 사실 여부 확인 필요."),
        ],
        "전문성 부족 또는 불분명한 기자/작성자": [
            (r"\b기자:\s*(홍길동|김아무개|익명)", "일반적인 이름 또는 익명 기자. 기자의 전문성이나 신뢰성 확인 필요."),
            (r"\b(견습|인턴)\s*기자", "경험 부족 기자. 기사의 완성도나 정확도에 영향 가능성."),
            (r"\b[가-힣]+\s*통신원", "불분명한 통신원. 정보의 출처 및 신뢰성 확인 필요."),
            (r"\b무명\s*작성자", "무명 작성자. 정보의 책임 소재가 불분명.")
        ],
        "과도한 일반화 또는 확대 해석": [
            (r"\b모든\s+[가-힣]+\s+.*[다들]\b", "'모든', '다들' 등의 과도한 일반화. 특정 사례를 전체로 확대 해석."),
            (r"\b항상\s*.*(할\s*것이다|했다)", "'항상', '항시' 등의 과도한 일반화. 극단적인 표현 사용."),
            (r"\b명백한\s*(사실|증거|결과)", "'명백한' 등의 단정적 표현 사용. 독자의 판단을 오도할 수 있음."),
            (r"\b틀림없이\s*.*(할\s*것이다|했다)", "'틀림없이' 등의 단정적 표현 사용. 확정되지 않은 사실을 단정적으로 서술."),
        ],
        "선정적/자극적 표현": [
            (r"\b충격적인\s*.*(사실|진실)", "'충격적인', '경악할' 등의 선정적 표현. 감정적인 반응 유도."),
            (r"\b경악할\s*.*(수준|일)", "'충격적인', '경악할' 등의 선정적 표현. 사실 전달보다 감정적 자극 목적."),
            (r"\b(분노|격분|경고|우려)\s*폭발", "감정적 과장 표현. 독자의 감정을 과도하게 자극."),
            (r"\b(초토화|붕괴|궤멸|파괴)\s*.*(될\s*것이다|되었다)", "재앙적/극단적 표현. 사태를 과장하여 불안감 조성."),
        ]
    }

    for reason, patterns_with_notes in rules.items():
        for pattern_str, note in patterns_with_notes:
            match = re.search(pattern_str, article_text, re.IGNORECASE)
            if match:
                suspicious_points.append({
                    "reason": reason,    
                    "phrase": match.group(0), 
                    "note": note          
                })
    return suspicious_points

@app.get("/")
async def root():
    """기본 엔드포인트: API 서버가 실행 중임을 확인."""
    return {"message": "Welcome to BiasBuster API!"}

@app.post("/analyze", response_model=AnalysisResult) 
async def analyze_article_endpoint(request: ArticleRequest):
    """
    프론트엔드로부터 기사 본문 문자열을 받아 AI 모델로 분석하고 요약, 신뢰도 분석 결과를 반환합니다.
    """
    article_text = request.text
    print(f"프론트엔드로부터 받은 텍스트 {article_text}")
    print(f"프론트엔드로부터 받은 텍스트 (길이: {len(article_text)})")

    analysis_scores: List[AnalysisScore] = []
    trust: List[SuspiciousPoint] = []

    try:
        analysis_scores = get_bias_scores(article_text)
    except RuntimeError as e:
        print(f"편향 분석 모델 로드 오류: {e}")
        analysis_scores = [{"category": "분석 오류", "score": 0.0}]
    except Exception as e:
        print(f"정치 편향 분석 중 예상치 못한 오류 발생: {e}")
        analysis_scores = [{"category": "분석 오류", "score": 0.0}]

    summary_text = "기사 내용에 대한 편향성 분석이 완료되었습니다."

    if analysis_scores:
        top_score_category = max(analysis_scores, key=lambda x: x['score'])

        summary_text = f"이 기사는 '{top_score_category['category']}' 편향이 {top_score_category['score']*100:.0f}%로 가장 두드러집니다."
    else:
        summary_text = "분석 결과, 특정 편향이 감지되지     않거나 분석할 데이터가 부족합니다."

    print(f"summary: {summary_text}")

    try:
        trust = analyze_article_trust(article_text)
    except Exception as e:
        print(f"신뢰도 분석 중 예상치 못한 오류 발생: {e}")
        trust = [{"reason": "신뢰도 분석 오류", "phrase": "내부 서버 오류", "note": str(e)}]

    print(f"scores: {analysis_scores}")
    print(f"trust_issues: {trust}")

    return AnalysisResult(
        summary=summary_text,
        scores=analysis_scores,
        trust_issues=trust
    )