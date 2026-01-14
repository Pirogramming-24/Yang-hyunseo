document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("id_ingPhoto");
    if (!input) return;

    input.addEventListener("change", function () {
        const file = this.files[0];
        const formData = new FormData();
        formData.append("image", file);

        document.getElementById("ocr-status").innerText = "🔍 분석 중…";

        fetch("/posts/ocr/", {
            method: "POST",
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            document.getElementById("ocr-status").innerText = "✅ 분석 완료";

            console.log("OCR data:", data);   // 디버깅용

            if (data.calorie !== null && data.calorie !== undefined)
                document.getElementById("id_calorie").value = data.calorie;

            if (data.carb)
                document.getElementById("id_carb").value = data.carb;

            if (data.protein)
                document.getElementById("id_protien").value = data.protein;

            if (data.fat)
                document.getElementById("id_fat").value = data.fat;
        })

        .catch(() => {
            document.getElementById("ocr-status").innerText = "❌ OCR 실패";
        });
    });
});
