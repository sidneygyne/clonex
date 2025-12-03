$(function () {
  console.log("comments.js carregado");

  $(document).on("submit", "form.comment-form", function (e) {
    e.preventDefault();

    const $form = $(this);
    const url = $form.attr("action");
    const postId = $form.data("post-id");

    console.log("Enviando comentário. URL:", url, "postId:", postId);

    $.ajax({
      url: url,
      type: "POST",
      data: $form.serialize(),
      success: function (data) {
        console.log("AJAX success data:", data);

        const $list = $(`#comments-list-${postId}`);
        const $count = $(`#comments-count-${postId}`);

        // Remove mensagem "Nenhum comentário ainda." se existir
        $list.find(".no-comments").remove();

        // Insere o novo comentário no topo
        $list.prepend(`
          <div class="card mb-2">
            <div class="card-body">
              <strong>${data.author}</strong>
              <p>${data.content}</p>
              <p class="text-muted small">${data.created_at}</p>

              <form method="post"
                    action="/comments/${data.id}/like/"
                    class="comment-like-form d-inline"
                    data-comment-id="${data.id}">
                <input type="hidden" name="csrfmiddlewaretoken"
                       value="${$form
                         .find("input[name=csrfmiddlewaretoken]")
                         .val()}">
                <button type="submit" class="btn btn-sm btn-primary">Curtir</button>
              </form>

              <span id="comment-likes-count-${data.id}">
                <span class="like-number">0</span>
                <i class="bi bi-hand-thumbs-up-fill text-primary"></i>
              </span>
            </div>
          </div>
        `);

        // Atualiza a contagem
        if (data.total_comments !== undefined) {
          let texto;
          if (data.total_comments === 0) {
            texto = "Nenhum comentário";
          } else if (data.total_comments === 1) {
            texto = "1 comentário";
          } else {
            texto = `${data.total_comments} comentários`;
          }
          $(`#comments-count-${postId}`).text(texto);
        } else {
          console.warn("total_comments não veio no JSON:", data);
        }

        // Limpa o formulário
        console.log("postId:", postId);
        console.log("Elemento contador encontrado:", $count.length);
        console.log("total_comments recebido:", data.total_comments);
        $form[0].reset();
      },
      error: function (xhr) {
        console.error("Erro no comentário:", xhr.status, xhr.responseText);
      },
    });
  });
});
