import os

from fastapi import FastAPI
from pydantic import BaseModel
from google import genai

app = FastAPI()

class StudyPlanRequest(BaseModel):
    subject: str
    level: str
    goal: str
    duration: str
    daily_time: str

@app.post("/")
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
            "message": "AI 학습 계획을 생성하지 못했습니다."
        }
