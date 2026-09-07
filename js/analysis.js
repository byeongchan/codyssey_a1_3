document.addEventListener("DOMContentLoaded", () => {

const form =
    document.getElementById("analysis-form");

const errorMessage =
    document.getElementById("analysis-error");

const result =
    document.getElementById("analysis-result");

const summaryDays =
    document.getElementById("summary-days");

const summaryHours =
    document.getElementById("summary-hours");

const summaryTasks =
    document.getElementById("summary-tasks");

const analysisTitle =
    document.getElementById("analysis-title");

const analysisDescription =
    document.getElementById("analysis-description");


form.addEventListener("submit", (event) => {

    event.preventDefault();

    errorMessage.hidden = true;
    errorMessage.textContent = "";


    const studyDays =
        Number(
            document.getElementById("study-days").value
        );

    const studyHours =
        Number(
            document.getElementById("study-hours").value
        );

    const completedTasks =
        Number(
            document.getElementById("completed-tasks").value
        );


    if (
        Number.isNaN(studyDays) ||
        Number.isNaN(studyHours) ||
        Number.isNaN(completedTasks)
    ) {

        showError(
            "모든 학습 정보를 입력해주세요."
        );

        return;
    }


    if (studyDays < 0 || studyDays > 7) {

        showError(
            "학습 일수는 0일에서 7일까지 입력해주세요."
        );

        return;
    }


    if (studyHours < 0) {

        showError(
            "학습 시간은 0 이상으로 입력해주세요."
        );

        return;
    }


    if (completedTasks < 0) {

        showError(
            "완료한 학습 항목은 0 이상으로 입력해주세요."
        );

        return;
    }


    summaryDays.textContent =
        `${studyDays}일`;

    summaryHours.textContent =
        `${studyHours}시간`;

    summaryTasks.textContent =
        `${completedTasks}개`;


    showAnalysis(
        studyDays,
        studyHours,
        completedTasks
    );


    result.hidden = false;

});


function showAnalysis(
    studyDays,
    studyHours,
    completedTasks
) {

    if (studyDays >= 5 && studyHours >= 7) {

        analysisTitle.textContent =
            "아주 잘하고 있습니다!";

        analysisDescription.textContent =
            "꾸준한 학습 습관을 잘 유지하고 있습니다. 지금의 학습 패턴을 계속 이어가보세요.";

        return;
    }


    if (studyDays >= 3 && studyHours >= 4) {

        analysisTitle.textContent =
            "좋은 흐름을 유지하고 있습니다.";

        analysisDescription.textContent =
            "꾸준히 공부하고 있습니다. 학습 시간을 조금씩 늘려보세요.";

        return;
    }


    if (completedTasks >= 3) {

        analysisTitle.textContent =
            "학습 목표를 잘 수행하고 있습니다.";

        analysisDescription.textContent =
            "완료한 학습 항목이 있습니다. 다음 주에도 목표를 하나씩 달성해보세요.";

        return;
    }


    analysisTitle.textContent =
        "조금 더 꾸준히 공부해보세요.";

    analysisDescription.textContent =
        "작은 목표부터 시작해 매일 조금씩 학습하는 습관을 만들어보세요.";
}


function showError(message) {

    errorMessage.textContent =
        `⚠️ ${message}`;

    errorMessage.hidden = false;
}
});
