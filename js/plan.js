document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("plan-form");

    const formError =
        document.getElementById("form-error");

    const resultEmpty =
        document.getElementById("result-empty");

    const resultLoading =
        document.getElementById("result-loading");

    const resultContent =
        document.getElementById("result-content");

    const planOutput =
        document.getElementById("plan-output");

    const subjectInput =
    document.getElementById("subject");

    const subjectCount =
        document.getElementById("subject-count");

    const goalInput =
        document.getElementById("goal");

    const goalCount =
        document.getElementById("goal-count");


    subjectInput.addEventListener("input", () => {
        subjectCount.textContent =
            subjectInput.value.length;
    });


goalInput.addEventListener("input", () => {
    goalCount.textContent =
        goalInput.value.length;
});

    form.addEventListener("submit", async (event) => {

        event.preventDefault();


        // 에러 메시지 초기화
        formError.hidden = true;
        formError.textContent = "";


        // 입력값 가져오기
        const subject =
            document.getElementById("subject").value.trim();

        const level =
            document.getElementById("level").value;

        const goal =
            document.getElementById("goal").value.trim();

        const duration =
            document.getElementById("duration").value;

        const dailyTime =
            document.getElementById("daily-time").value;


        // 프론트엔드 입력값 검증
        if (!subject) {
            showError("공부할 분야를 입력해주세요.");
            return;
        }

        if (!level) {
            showError("현재 수준을 선택해주세요.");
            return;
        }

        if (!goal) {
            showError("학습 목표를 입력해주세요.");
            return;
        }

        if (!duration) {
            showError("학습 기간을 선택해주세요.");
            return;
        }

        if (!dailyTime) {
            showError("하루 학습 시간을 선택해주세요.");
            return;
        }


        // 로딩 화면
        resultEmpty.hidden = true;
        resultContent.hidden = true;
        resultLoading.hidden = false;


        try {

            // 백엔드 API 호출
            const response = await fetch(
                "/api/study-plan",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        subject: subject,
                        level: level,
                        goal: goal,
                        duration: duration,
                        daily_time: dailyTime
                    })
                }
            );


            // JSON 응답
            const data = await response.json();


            // API 오류
            if (!response.ok || !data.success) {

                throw new Error(
                    data.message ||
                    "AI 학습 계획을 생성하지 못했습니다."
                );

            }


            // AI 결과 출력
            renderPlan(data.plan);


        } catch (error) {

            console.error(
                "학습 계획 생성 오류:",
                error
            );


            resultLoading.hidden = true;
            resultEmpty.hidden = false;


            showError(
                error.message ||
                "AI 학습 계획을 생성하지 못했습니다. 잠시 후 다시 시도해주세요."
            );

        }

    });


    // 에러 메시지 표시
    function showError(message) {

        formError.textContent =
            `⚠️ ${message}`;

        formError.hidden = false;

    }


    // AI 결과 출력
    function renderPlan(plan) {

    if (!plan) {
        throw new Error(
            "AI 학습 계획의 답변이 비어 있습니다."
        );
    }

    resultLoading.hidden = true;
    resultEmpty.hidden = true;
    resultContent.hidden = false;


    // 줄바꿈을 HTML로 변환
    const formattedPlan =
        escapeHtml(plan)
            .replace(/\n/g, "<br>");


    planOutput.innerHTML = `
        <div class="ai-plan-text">
            ${formattedPlan}
        </div>
    `;

}


    // AI 응답을 HTML에 안전하게 출력
    function escapeHtml(text) {

        const div =
            document.createElement("div");

        div.textContent = text;

        return div.innerHTML;

    }

});