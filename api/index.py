import os

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from google import genai


app = FastAPI()


# =========================
# 파일 경로
# =========================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# =========================
# CSS / JS 파일 제공
# =========================

app.mount(
    "/css",
    StaticFiles(directory=os.path.join(BASE_DIR, "css")),
    name="css"
)

app.mount(
    "/js",
    StaticFiles(directory=os.path.join(BASE_DIR, "js")),
    name="js"
)


# =========================
# HTML 페이지
# =========================

@app.get("/")
def home():
    return FileResponse(
        os.path.join(BASE_DIR, "index.html")
    )

@app.get("/index.html")
def index_page():
    return FileResponse(
        os.path.join(BASE_DIR, "index.html")
    )

@app.get("/plan.html")
def plan_page():
    return FileResponse(
        os.path.join(BASE_DIR, "plan.html")
    )


@app.get("/coach.html")
def coach_page():
    return FileResponse(
        os.path.join(BASE_DIR, "coach.html")
    )


@app.get("/analysis.html")
def analysis_page():
    return FileResponse(
        os.path.join(BASE_DIR, "analysis.html")
    )


# =========================
# AI Coach
# =========================

class CoachRequest(BaseModel):
    question: str


@app.post("/api/ai-coach")
def ask_coach(request: CoachRequest):

    if not request.question.strip():
        return {
            "success": False,
            "message": "질문을 입력해주세요."
        }

    if len(request.question) > 1000:
        return {
            "success": False,
            "message": "질문은 1000자 이내로 입력해주세요."
    }

    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        return {
            "success": False,
            "message": "Gemini API 키가 설정되지 않았습니다."
        }

    try:

        client = genai.Client(
            api_key=api_key
        )

        prompt = f"""
당신은 친절하고 전문적인 AI 학습 코치입니다.

학생이 공부하면서 궁금한 내용을 질문하면
학생의 학습을 도와주는 방식으로 답변해주세요.

답변 원칙:

1. 어려운 개념은 쉽게 설명해주세요.
2. 필요한 경우 간단한 예시를 들어주세요.
3. 핵심 내용을 단계적으로 설명해주세요.
4. 다음에 공부하면 좋은 내용도 알려주세요.
5. 너무 길지 않고 이해하기 쉽게 작성해주세요.
6. 답변은 한국어로 작성해주세요.

학생의 질문:

{request.question}
"""

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        return {
            "success": True,
            "answer": response.text
        }

    except Exception as error:

        print("Gemini API ERROR:", error)

        return {
            "success": False,
            "message": f"AI 코치 답변을 생성하지 못했습니다.: {error}"
        }


# =========================
# Study Plan
# =========================

class StudyPlanRequest(BaseModel):
    subject: str
    level: str
    goal: str
    duration: str
    daily_time: str


@app.post("/api/study-plan")
def create_study_plan(request: StudyPlanRequest):

    if not request.subject.strip():
        return {
            "success": False,
            "message": "공부할 분야를 입력해주세요."
        }

    if not request.goal.strip():
        return {
            "success": False,
            "message": "학습 목표를 입력해주세요."
        }

    if len(request.subject) > 100:
        return {
            "success": False,
            "message": "공부할 분야는 100자 이내로 입력해주세요."
        }

    if len(request.goal) > 1000:
        return {
            "success": False,
            "message": "학습 목표는 1000자 이내로 입력해주세요."
        }

    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        return {
            "success": False,
            "message": "Gemini API 키가 설정되지 않았습니다."
        }

    try:

        client = genai.Client(
            api_key=api_key
        )

        prompt = f"""
당신은 전문적인 AI 학습 코치입니다.

사용자의 학습 정보를 바탕으로
현실적으로 실천할 수 있는 맞춤형 학습 계획을 만들어주세요.

[사용자 정보]

공부 분야:
{request.subject}

현재 수준:
{request.level}

학습 목표:
{request.goal}

학습 기간:
{request.duration}

하루 학습 시간:
{request.daily_time}

다음 내용을 포함해주세요.

1. 전체 학습 방향
2. 주차별 학습 계획
3. 각 주차의 핵심 학습 내용
4. 실습 또는 복습 방법
5. 학습자가 주의해야 할 점

사용자가 실제로 실행할 수 있는 수준으로
현실적인 계획을 작성해주세요.

답변은 한국어로 작성해주세요.
"""

        response = client.models.generate_content(
            model="gemini-3.7-flash",
            contents=prompt
        )

        return {
            "success": True,
            "plan": response.text
        }

    except Exception as error:

        print("Gemini API ERROR:", error)

        return {
            "success": False,
            "message": f"AI 학습 계획을 생성하지 못했습니다. : {error}"
        }