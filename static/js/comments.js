$(function() {
  $(document).on("submit", "form.comment-form", function(e) {
    e.preventDefault();

    const $form = $(this);
    const url = $form.attr("action");
    const postId = $form.data("post-id");

    $.ajax({
      url: url,
      type: "POST",
      data: $form.serialize(),
      success: function(data) {
        const $list = $(`#comments-list-${postId}`);
        $list.prepend(`
          <div class="card mb-2">
            <div class="card-body">
              <strong>${data.author}</strong>
              <p>${data.content}</p>
              <p class="text-muted small">${data.created_at}</p>

              <!-- Botão Curtir/Descurtir -->
              <form method="post"
                    action="/comments/${data.id}/like/"
                    class="comment-like-form d-inline"
                    data-comment-id="${data.id}">
                <input type="hidden" name="csrfmiddlewaretoken" value="${$form.find('input[name=csrfmiddlewaretoken]').val()}">
                <button type="submit" class="btn btn-sm btn-primary">Curtir</button>
              </form>

              <!-- Contador com ícone -->
              <span id="comment-likes-count-${data.id}">
                <span class="like-number">0</span>
                <i class="bi bi-hand-thumbs-up-fill text-primary"></i>
              </span>
            </div>
          </div>
        `);
        $form[0].reset();
      },
      error: function(xhr) {
        console.error("Erro no comentário:", xhr.status, xhr.responseText);
      }
    });
  });
});
