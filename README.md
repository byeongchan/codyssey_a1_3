# codyssey_a1_3

AI Study Coach는 학습자가 자신의 학습 목표와 궁금한 내용을 입력하면 AI가 맞춤형 학습 계획과 학습 코칭을 제공하는 웹 서비스입니다.

순수 HTML, CSS, JavaScript로 프론트엔드를 구현하고, Python 기반 FastAPI 백엔드와 Gemini API를 연동하여 AI 기능을 제공합니다.

---

## 1. 서비스 소개

### 서비스 목적

학습자가 혼자 공부하면서 겪는 어려움을 줄이고, 자신의 수준과 목표에 맞는 학습 방향을 쉽게 설정할 수 있도록 돕는 것을 목적으로 합니다.

사용자가 학습 정보를 입력하면 AI가 학습 계획을 생성하고, 궁금한 내용을 질문하면 AI 학습 코치가 답변을 제공합니다.

### 타겟 사용자

* AI 및 프로그래밍을 공부하는 대학생
* 취업을 준비하는 학습자
* 새로운 기술을 독학하는 초보자
* 체계적인 학습 계획이 필요한 사용자

### 핵심 가치

* AI를 활용한 개인 맞춤형 학습 계획
* 학습 중 궁금한 내용을 바로 질문할 수 있는 AI 코치
* 학습 목표에 맞는 단계별 학습 방향 제공
* PC와 모바일에서 사용할 수 있는 반응형 웹 서비스

---

## 2. 주요 기능

### ① 학습 계획 생성

사용자가 다음 정보를 입력하면 AI가 맞춤형 학습 계획을 생성합니다.

**입력**

* 공부 분야
* 현재 수준
* 학습 목표
* 학습 기간
* 하루 학습 시간

**출력**

* 전체 학습 방향
* 주차별 학습 계획
* 핵심 학습 내용
* 실습 및 복습 방법
* 학습 시 주의사항

### ② AI 학습 코치

사용자가 공부하면서 궁금한 내용을 질문하면 Gemini API를 이용하여 AI가 답변합니다.

**입력 예시**

> Python에서 리스트와 튜플의 차이를 알려줘.

**출력**

* 개념 설명
* 간단한 예시
* 단계별 설명
* 다음에 공부하면 좋은 내용

### ③ 학습 분석

학습 분석 페이지를 통해 학습 내용을 확인하고 자신의 학습 방향을 점검할 수 있도록 구성했습니다.

---

## 3. 페이지 구성

| 페이지        | 설명                      |
| ---------- | ----------------------- |
| Home       | 서비스 소개 및 주요 기능 안내       |
| Study Plan | AI를 이용한 맞춤형 학습 계획 생성    |
| AI Coach   | 학습 관련 질문을 입력하고 AI 답변 확인 |
| Analysis   | 학습 내용을 확인하고 분석          |

페이지 상단 메뉴와 버튼을 통해 각 페이지를 이동할 수 있습니다.

총 4개의 페이지로 구성하여 과제의 최소 3개 페이지 요구사항을 충족합니다.

---

## 4. 기술 스택

### Frontend

* HTML5
* CSS3
* Vanilla JavaScript
* Fetch API
* 반응형 웹 디자인

### Backend

* Python
* FastAPI
* Pydantic

### AI

* Google Gemini API
* `google-genai`

### Deployment

* GitHub
* Vercel

---

## 5. 프로젝트 구조

```text
AI Study Coach/
│
├── index.html
├── coach.html
├── plan.html
├── analysis.html
│
├── css/
│   └── style.css
│
├── js/
│   ├── main.js
│   ├── coach.js
│   ├── plan.js
│   └── analysis.js
│
├── api/
│   └── index.py
│
├── requirements.txt
│
└── vercel.json
```

### Frontend / Backend 구분

**Frontend**

```text
index.html
coach.html
plan.html
analysis.html
css/
js/
```

사용자 화면과 입력 UI, 결과 표시 및 페이지 이동을 담당합니다.

**Backend**

```text
api/index.py
```

FastAPI를 이용하여 웹 페이지를 제공하고 AI API 요청을 처리합니다.

---

## 6. API 구조

### AI Coach

```http
POST /api/ai-coach
```

요청 데이터:

```json
{
  "question": "Python에서 리스트와 튜플의 차이를 알려줘."
}
```

성공 응답:

```json
{
  "success": true,
  "answer": "..."
}
```

### Study Plan

```http
POST /api/study-plan
```

요청 데이터:

```json
{
  "subject": "Python",
  "level": "초급",
  "goal": "Python 기초 문법 익히기",
  "duration": "4주",
  "daily_time": "1시간"
}
```

성공 응답:

```json
{
  "success": true,
  "plan": "..."
}
```

프론트엔드는 `fetch('/api/...')`를 사용하여 백엔드 API를 호출하고 AI 결과를 화면에 출력합니다.

---

## 7. AI 기능 처리 기준

### 입력 처리

필수 입력값이 비어 있는 경우 AI API를 호출하지 않고 사용자에게 안내 메시지를 표시합니다.

예:

```text
질문을 입력해주세요.
```

또는

```text
공부할 분야를 입력해주세요.
```

### API 오류 처리

Gemini API 호출 과정에서 오류가 발생하면 사용자에게 다음과 같은 메시지를 표시합니다.

```text
AI 코치 답변을 생성하지 못했습니다.
```

또는

```text
AI 학습 계획을 생성하지 못했습니다.
```

### API 키 미설정

환경 변수에 Gemini API 키가 설정되지 않은 경우 다음 메시지를 반환합니다.

```text
Gemini API 키가 설정되지 않았습니다.
```

### 로딩 처리

AI 응답을 기다리는 동안 화면에 로딩 상태를 표시하여 사용자가 요청이 처리되고 있음을 알 수 있도록 구성했습니다.

---

## 8. 환경 변수 설정

Gemini API를 사용하기 위해 `GEMINI_API_KEY` 환경 변수가 필요합니다.

### 로컬 환경

Windows PowerShell:

```powershell
$env:GEMINI_API_KEY="발급받은_API_키"
```

또는 `.env` 파일을 사용하는 경우 프로젝트 환경에 맞게 API 키를 설정합니다.

### Vercel

Vercel 프로젝트의

**Settings → Environment Variables**

에서 다음 변수를 추가합니다.

```text
Name: GEMINI_API_KEY
Value: 발급받은 Gemini API Key
```

API 키는 GitHub 저장소에 직접 작성하거나 공개해서는 안 됩니다.

---

## 9. 로컬 실행 방법

### 1. 저장소 클론

```bash
git clone 저장소_URL
cd "AI Study Coach"
```

### 2. 가상환경 생성

```bash
python -m venv venv
```

### 3. 가상환경 활성화

Windows:

```bash
venv\Scripts\activate
```

### 4. 패키지 설치

```bash
pip install -r requirements.txt
```

### 5. Gemini API 키 설정

```text
GEMINI_API_KEY=발급받은_API_키
```

### 6. Vercel 개발 서버 실행

```bash
vercel dev
```

실행 후 브라우저에서 로컬 주소로 접속합니다.

```text
http://localhost:3000
```

---

## 10. Vercel 배포 방법

### 1. GitHub 저장소 생성

프로젝트를 GitHub 저장소에 업로드합니다.

### 2. Vercel 연결

Vercel에서 GitHub 저장소를 Import하여 프로젝트를 연결합니다.

### 3. 환경 변수 설정

Vercel 프로젝트의 Environment Variables에 다음 값을 등록합니다.

```text
GEMINI_API_KEY
```

### 4. 배포

GitHub의 `main` 브랜치에 변경사항을 Push하면 Vercel에서 자동으로 배포됩니다.

배포가 완료되면 Vercel에서 제공하는 URL을 통해 서비스를 이용할 수 있습니다.

---

## 11. 배포 URL

**Vercel**

> [https://codyssey-a1-3-gamma.vercel.app/]


---

## 12. 반응형 웹

다양한 화면 크기에서 사용할 수 있도록 반응형 CSS를 적용했습니다.

확인 대상:

* Desktop
* Tablet
* Mobile

화면 크기에 따라 콘텐츠 영역, 버튼, 입력 폼 등의 크기와 배치를 조정하여 모바일에서도 사용할 수 있도록 구현했습니다.

---

## 13. 동작 흐름

### AI 학습 계획

```text
사용자
  ↓
학습 정보 입력
  ↓
프론트엔드 JavaScript
  ↓
POST /api/study-plan
  ↓
FastAPI
  ↓
Gemini API
  ↓
AI 학습 계획 생성
  ↓
JSON 응답
  ↓
화면에 결과 출력
```

### AI 학습 코치

```text
사용자
  ↓
질문 입력
  ↓
프론트엔드 JavaScript
  ↓
POST /api/ai-coach
  ↓
FastAPI
  ↓
Gemini API
  ↓
AI 답변 생성
  ↓
JSON 응답
  ↓
화면에 결과 출력
```

---

## 14. 증빙 자료

### 서비스 스크린샷

1. 데스크톱 메인 화면
<p align="center">
<img src="./image/PC환경.png">
</p>

2. 모바일 메인 화면
<p align="center">
<img src="./image/모바일환경.png">
</p>
3. AI 학습 계획 생성 결과
<p align="center">
<img src="./image/학습계획.png">
</p>
4. AI Coach 동작 화면
<p align="center">
<img src="./image/AI코치.png">
</p>

### AI 코딩 도구 사용 증빙

* AI 코딩 도구와의 대화 로그
<p align="center">
<img src="./image/AI대화로그.png">
</p>

---

## 15. 주의사항

* Gemini API Key는 GitHub에 업로드하지 않습니다.
* `.env` 등의 환경 설정 파일에 저장된 비밀 키는 `.gitignore`를 통해 관리합니다.
* AI가 생성하는 학습 계획은 참고용이며 사용자의 실제 학습 상황에 맞게 조정할 수 있습니다.
* API 사용량에 따라 Gemini API 사용 제한 또는 비용이 발생할 수 있습니다.

---

## 16. 향후 개선 사항

* 학습 기록 저장 기능
* 사용자별 학습 데이터 관리
* 학습 진행률 시각화
* AI 학습 계획 자동 수정 기능
* 학습 일정 알림 기능
* 사용자별 맞춤형 학습 피드백 강화