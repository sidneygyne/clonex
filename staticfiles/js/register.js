document.addEventListener("DOMContentLoaded", function () {
  const modalElement = document.getElementById("successModal");
  const shouldShowModal = modalElement?.dataset.show === "true";

  if (shouldShowModal) {
    const modal = new bootstrap.Modal(modalElement);
    modal.show();

    setTimeout(() => {
      window.location.href = modalElement.dataset.redirect;
    }, 5000);
  }
});
