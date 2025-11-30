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
