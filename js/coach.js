document.addEventListener("DOMContentLoaded", () => {

const form = document.getElementById("coach-form");
const questionInput = document.getElementById("question");
const questionCount = document.getElementById("question-count");
questionInput.addEventListener("input", () => {
    questionCount.textContent = questionInput.value.length;
});

const errorMessage =
    document.getElementById("coach-error");

const emptyResult =
    document.getElementById("coach-empty");

const loadingResult =
    document.getElementById("coach-loading");

const contentResult =
    document.getElementById("coach-content");

const coachOutput =
    document.getElementById("coach-output");


form.addEventListener("submit", async (event) => {

    event.preventDefault();

    errorMessage.hidden = true;
    errorMessage.textContent = "";

    const question =
        questionInput.value.trim();


    // 질문 입력 여부 확인
    if (!question) {

        showError(
            "질문을 입력해주세요."
        );

        return;
    }


    // 결과 화면 초기화
    emptyResult.hidden = true;
    contentResult.hidden = true;
    loadingResult.hidden = false;


    try {

        const response = await fetch(
            "/api/ai-coach",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    question: question
                })
            }
        );


        const data =
            await response.json();


        // API 오류 처리
        if (!response.ok || !data.success) {

            throw new Error(
                data.message ||
                "AI 코치 답변을 가져오지 못했습니다."
            );
        }


        // 답변 출력
        renderAnswer(data.answer);


    } catch (error) {

        console.error(
            "AI 코치 오류:",
            error
        );

        loadingResult.hidden = true;
        emptyResult.hidden = false;

        showError(
            error.message ||
            "AI 코치에 연결할 수 없습니다. 잠시 후 다시 시도해주세요."
        );
    }

});


function showError(message) {

    errorMessage.textContent =
        `⚠️ ${message}`;

    errorMessage.hidden = false;
}


function renderAnswer(answer) {

    if (!answer) {
        throw new Error(
            "AI 코치의 답변이 비어 있습니다."
        );
    }

    loadingResult.hidden = true;
    emptyResult.hidden = true;
    contentResult.hidden = false;


    const safeAnswer =
        escapeHtml(answer)
            .replace(/\n/g, "<br>");


    coachOutput.innerHTML = `
        <div class="ai-coach-text">
            ${safeAnswer}
        </div>
    `;
}


function escapeHtml(text) {

    const div =
        document.createElement("div");

    div.textContent = text;

    return div.innerHTML;
}
});