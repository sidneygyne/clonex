$(function() {
  $(document).on("submit", "form.comment-like-form", function(e) {
    e.preventDefault();

    const $form = $(this);
    const url = $form.attr("action");
    const commentId = $form.data("comment-id");

    $.ajax({
      url: url,
      type: "POST",
      data: $form.serialize(),
      success: function(data) {
        // Atualiza só o número, mantém o ícone
        $(`#comment-likes-count-${commentId} .like-number`).text(data.likes_count);

        const $btn = $form.find("button");
        if (data.liked) {
          $btn.removeClass("btn-primary").addClass("btn-danger").text("Descurtir");
        } else {
          $btn.removeClass("btn-danger").addClass("btn-primary").text("Curtir");
        }
      },
      error: function(xhr) {
        console.error("Erro no like do comentário:", xhr.status, xhr.responseText);
      }
    });
  });
});
