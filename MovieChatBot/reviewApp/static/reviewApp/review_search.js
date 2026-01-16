console.log("🔥 review_search.js loaded");


const searchInput = document.getElementById("searchInput");
const reviewCards = document.querySelectorAll(".review-card-link");

searchInput.addEventListener("input", function () {
  const keyword = searchInput.value.trim().toLowerCase();

  reviewCards.forEach((card) => {
    const titleElement = card.querySelector(".review-title");
    const titleText = titleElement.innerText.toLowerCase();

    if (titleText.includes(keyword)) {
      card.style.display = "";
    } else {
      card.style.display = "none";
    }
  });
});
