document.addEventListener("DOMContentLoaded", () => {

document.querySelectorAll(".star-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    const ideaId = btn.dataset.id
    const star = btn.querySelector(".star-count")

    fetch(`/myIdeas/idea/${ideaId}/star/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      }
    })
    .then(res => res.json())
    .then(data => {
      btn.classList.toggle("active", data.starred)
    })
  })
})



  /* ❤️ 관심도 +/- */
  document.querySelectorAll(".interest-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const delta = btn.dataset.delta
      const ideaId = btn.dataset.id

      fetch(`/myIdeas/idea/${ideaId}/interest/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `delta=${delta}`
      })
      .then(res => res.json())
      .then(data => {
        btn.closest(".interest-box")
           .querySelector(".interest-value")
           .innerText = data.interest
      })
    })
  })

})


// CSRF 토큰 가져오기 (Django AJAX 필수)
function getCookie(name) {
  let cookieValue = null;
  document.cookie.split(';').forEach(cookie => {
    cookie = cookie.trim();
    if (cookie.startsWith(name + '=')) {
      cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
    }
  })
  return cookieValue;
}
