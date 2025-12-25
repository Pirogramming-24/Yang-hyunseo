// 게임 상태 객체
const game = {
    answer: [],
    attempts: 9,

    init() {
        this.answer = this.makeAnswer(); //answer에 랜덤한 값 넣음.
        this.attempts = 9;
        document.getElementById("attempts").textContent = this.attempts;
        console.log("정답:", this.answer); // 디버깅용
    },

    makeAnswer() {
        const nums = [];
        while (nums.length < 3) {
            const n = Math.floor(Math.random() * 10);
            if (!nums.includes(n)) nums.push(n);
        }
        return nums;
    }
};

game.init();


// 확인 버튼 클릭 시 실행
/*
입력 숫자 받기 -> 완료
각 숫자 비교 -> 완료
attempts 값 하나씩 줄이기 -> 완료
조건 충족 시 success 혹은 fail -> 완료
*/
function check_numbers() {
    const inputs = [
        document.getElementById("number1").value,
        document.getElementById("number2").value,
        document.getElementById("number3").value
    ];

    // 빈칸 검사
    if (inputs.includes("")) {
        alert("숫자 3개를 모두 입력하세요!");

        document.getElementById("number1").value = "";
        document.getElementById("number2").value = "";
        document.getElementById("number3").value = "";
        document.getElementById("number1").focus();

        return;
    }

    //확인하기 버튼 누르면 입력칸 비우기.
    document.getElementById("number1").value = "";
    document.getElementById("number2").value = "";
    document.getElementById("number3").value = "";


    const userNums = inputs.map(Number); //inputs에 들어있는 값을 '수'로 바꾸어서 userNums 배열에 넣기.
    const resultImg = document.getElementById("game-result-img");
    const submitBtn = document.querySelector(".submit-button");

    // 중복 숫자 검사
    if (new Set(userNums).size !== 3) {
        alert("중복되지 않은 숫자를 입력하세요!");
        return;
    }

    let strike = 0;
    let ball = 0;

    userNums.forEach((num, idx) => { //userNums 배열에 수와 해당하는 인덱스 가져옴
        if (num === game.answer[idx]) strike++; //그 인덱스의 수와 일치한다면 스트아리크
        else if (game.answer.includes(num)) ball++; //인덱스 관련 없이 num이 배열에 inclue 된다면 볼
    });

    game.attempts--;
    document.getElementById("attempts").textContent = game.attempts;

    updateUI(userNums, strike, ball);


    if (strike === 3) {
        resultImg.src = "success.png";

    } else if (game.attempts === 0) {
        resultImg.src = "fail.png";
        submitBtn.disabled = true;
        submitBtn.style.opacity = "0.5";
        submitBtn.style.cursor = "not-allowed";
    }

}

// 결과 출력
function updateUI(nums, strike, ball) {
    const results = document.getElementById("results");

    const row = document.createElement("div");
    row.className = "check-result";

    // 왼쪽: 입력 숫자 + :
    const left = document.createElement("div");
    left.className = "left";
    left.textContent = nums.join(" ") + " :";

    const right = document.createElement("div");
    right.className = "right";

    //아웃 처리
    if (strike === 0 && ball === 0) {
        const out = document.createElement("span");
        out.className = "num-result out";
        out.textContent = "O";
        right.appendChild(out);
    } 
    //스트라이크 / 볼
    else {
        // 스트라이크
        const strikeCount = document.createElement("span");
        strikeCount.textContent = strike + " ";

        const strikeCircle = document.createElement("span");
        strikeCircle.className = "num-result strike";
        strikeCircle.textContent = "S";

        // 볼
        const ballCount = document.createElement("span");
        ballCount.textContent = " " + ball + " ";

        const ballCircle = document.createElement("span");
        ballCircle.className = "num-result ball";
        ballCircle.textContent = "B";

        right.appendChild(strikeCount);
        right.appendChild(strikeCircle);
        right.appendChild(ballCount);
        right.appendChild(ballCircle);
    }

    row.appendChild(left);
    row.appendChild(right);
    results.appendChild(row);
}


