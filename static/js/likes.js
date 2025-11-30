$(function() {
  // Intercepta o submit dos forms de curtida
  $(document).on("submit", "form.like-form", function(e) {
    e.preventDefault(); // impede reload da página

    const $form = $(this);
    const url = $form.attr("action");          // URL da view toggle-like
    const postId = $form.data("post-id");      // ID do post

    $.ajax({
      url: url,
      type: "POST",
      data: $form.serialize(),                 // envia CSRF e dados do form
      success: function(data) {
        // Espera que a view retorne JSON: { likes_count: int, liked: bool }

        // Atualiza contador
        if (typeof data.likes_count !== "undefined") {
          $(`#likes-count-${postId}`).text(data.likes_count);
        }

        // Atualiza botão
        const $btn = $form.find("button");
        if (data.liked) {
          $btn.removeClass("btn-primary")
              .addClass("btn-danger")
              .text("Descurtir");
        } else {
          $btn.removeClass("btn-danger")
              .addClass("btn-primary")
              .text("Curtir");
        }
      },
      error: function(xhr) {
        console.error("Erro no like:", xhr.status, xhr.responseText);
        alert("Não foi possível atualizar a curtida. Tente novamente.");
      }
    });
  });
});
