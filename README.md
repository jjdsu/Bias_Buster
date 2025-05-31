# BiasBuster

**BiasBuster**는 뉴스 기사, 블로그 글 등 텍스트를 입력하면 해당 콘텐츠의 정치 성향(좌파/진보 · 중도 · 우파/보수)을 AI 모델로 분석하여 점수를 제공해 주는 웹 애플리케이션입니다.  
FastAPI 기반의 백엔드와 React 기반의 프론트엔드로 구성되어 있으며, 텍스트를 입력하면 점수와 주제(토픽)를 JSON으로 반환하고, 프론트엔드에서는 결과를 시각화하여 사용자에게 보여줍니다.

---

## 목차

1. [프로젝트 개요](#프로젝트-개요)  
2. [환경 변수](#환경-변수)  
3. [백엔드 실행](#백엔드-실행)  
4. [프론트엔드 실행](#프론트엔드-실행)  
5. [CORS 설정](#cors-설정)  
6. [참여자](#참여자)  

---

## 프로젝트 개요

- **프로젝트명**: BiasBuster  
- **목적**:  
  - 뉴스 기사나 블로그 글을 읽을 때, 해당 텍스트가 어떤 정치적 스펙트럼(좌파/진보, 중도, 우파/보수)에 가까운지 사용자에게 시각적으로 알려 줌으로써, 정보 소비자의 편향 인지 능력을 높이기 위함.  
- **주요 기능**:  
  1. 사용자가 텍스트를 입력 → 백엔드에 POST 요청  
  2. 백엔드 AI 모델이 3가지 정치 성향 점수(0~1)와 의심 요소들을 JSON으로 반환  
  3. 프론트엔드가 결과를 받아 성향별 막대 그래프, 의심요소 리스트로 시각화  

## 환경 변수

프로젝트를 로컬에서 실행하거나 배포할 때 다음 환경 변수를 설정해야 합니다.

### 공통(.env 파일)

```env
# frontend/.env.development
VITE_API_URL=http://localhost:8001
```
---

## 백엔드 실행

1. **가상환경 생성 & 활성화**  
   ```bash
   cd backend
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS / Linux
   source venv/bin/activate
   ```
2. **의존성 설치**  
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
3. **서버 실행**  
   ```bash
   cd app
   # uvicorn으로 실행
   python -m uvicorn --app-dir app main:app --reload --host 0.0.0.0 --port 8001
   ```
---

## 프론트엔드 실행

1. **Node.js 설치 확인**  
   - Node.js 버전 ≥ 14.x  
   - Yarn 또는 npm이 설치되어 있어야 합니다.
2. **의존성 설치**  
   ```bash
   cd frontend
   # npm
   npm install
   ```
3. **파일 빌드 및 로드**  
   ```bash
   # npm
   npm run build
   ```
   - Vite 프로젝트 기준으로 `npm run build`를 실행하면 `dist/` 폴더에 정적 파일이 생성됩니다.  
   - `dist` 파일을 크롬 확장프로그램(`chrome://extensions/`)에 업로드 합니다.
4. **환경 변수 확인**  
   - `.env.development` 파일에서 `VITE_API_URL`이 `http://localhost:8001`로 설정되어 있어야 합니다.
   - 만약 프론트엔드/백엔드를 서로 다른 호스트에서 실행한다면, CORS 설정을 확인하세요.

---

## CORS 설정

프론트엔드가 백엔드(예: `http://localhost:8001`)와 다른 도메인으로 실행될 때, 브라우저가 교차 출처 요청을 차단할 수 있습니다. 이를 해결하려면 백엔드에서 `CORSMiddleware`를 설정해야 합니다.

```python
# backend/app/cors.py (예시)
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

app = FastAPI()

origins = [
    "http://localhost:8001",
    "chrome-extension://*", 
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # 허용할 도메인 목록
    allow_credentials=True,
    allow_methods=["*"],              # 모든 HTTP 메서드 허용
    allow_headers=["*"],              # 모든 헤더 허용
)
```
---

## 참여자

- **창업**: 방예진 
- **백엔드**: 김예원  
- **프론트엔드**: 이은지, 정동현  

감사합니다.  
