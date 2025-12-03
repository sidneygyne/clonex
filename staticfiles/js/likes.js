$(function() {
  $(document).on("submit", "form.like-form", function(e) {
    e.preventDefault();

    const $form = $(this);
    const url = $form.attr("action");
    const postId = $form.data("post-id");

    $.ajax({
      url: url,
      type: "POST",
      data: $form.serialize(),
      success: function(data) {
        // Atualiza APENAS o número (mantém ícone)
        if (typeof data.likes_count !== "undefined") {
          $(`#likes-count-${postId} .like-number`).text(data.likes_count);
        }

        // Alterna o botão
        const $btn = $form.find("button");
        if (data.liked) {
          $btn.removeClass("btn-primary").addClass("btn-danger").text("Descurtir");
        } else {
          $btn.removeClass("btn-danger").addClass("btn-primary").text("Curtir");
        }
      },
      error: function(xhr) {
        console.error("Erro no like:", xhr.status, xhr.responseText);
        alert("Não foi possível atualizar a curtida. Tente novamente.");
      }
    });
  });
});
