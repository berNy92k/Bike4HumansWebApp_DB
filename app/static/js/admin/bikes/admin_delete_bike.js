document.addEventListener("DOMContentLoaded", () => {
  const deleteButtons = document.querySelectorAll("[data-bike-id]");

  deleteButtons.forEach((button) => {
    button.addEventListener("click", async () => {
      const bikeId = button.dataset.bikeId;

      const shouldDelete = confirm("Na pewno usunąć ten rower?");
      if (!shouldDelete) return;

      try {
        const response = await fetch(`/admin/bikes/${bikeId}`, {
          method: "DELETE",
        });

        if (response.ok) {
          window.location.reload();
          return;
        }

        alert("Nie udało się usunąć roweru.");
      } catch (error) {
        alert("Wystąpił błąd podczas usuwania roweru.");
      }
    });
  });
});
