// static/js/likes.js
$(function () {
  $(document).on("click", ".btn-toggle-like", function (e) {
    e.preventDefault();

    const $btn = $(this);
    const postId = $btn.data("post-id");
    const url = $btn.data("like-url");
    const currentlyLiked = $btn.hasClass("btn-danger"); // true se está "Descurtir"
    const action = currentlyLiked ? "unlike" : "like";   // ação desejada

    $.ajax({
      url: url,
      type: "POST", // sempre POST
      data: JSON.stringify({ action: action }),
      contentType: "application/json",
      headers: { "X-CSRFToken": getCookie("csrftoken") },
      success: function (data) {
        // Espera { likes_count: int, liked: bool }
        if (typeof data.likes_count !== "undefined") {
          $(`#likes-count-${postId}`).text(data.likes_count);
        }

        const liked = !!data.liked;
        if (liked) {
          $btn.removeClass("btn-primary").addClass("btn-danger").text("Descurtir");
        } else {
          $btn.removeClass("btn-danger").addClass("btn-primary").text("Curtir");
        }
      },
      error: function (xhr) {
        console.error("Erro no like:", xhr.status, xhr.responseText);
        alert("Não foi possível atualizar a curtida. Verifique sua conexão e tente novamente.");
      },
    });
  });
});

// CSRF helper (Django)
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
