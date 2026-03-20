document.addEventListener("DOMContentLoaded", () => {
    const deleteButtons = document.querySelectorAll("[data-manufacturer-id]");

    deleteButtons.forEach((button) => {
        button.addEventListener("click", async () => {
            const manufacturerId = button.dataset.manufacturerId;

            const shouldDelete = confirm("Na pewno usunąć tego producenta?");
            if (!shouldDelete) return;

            try {
                const response = await fetch(`/admin/manufacturer/${manufacturerId}`, {
                    method: "DELETE",
                });

                if (response.ok) {
                    window.location.reload();
                    return;
                }

                alert("Nie udało się usunąć producenta.");
            } catch (error) {
                alert("Wystąpił błąd podczas usuwania producenta.");
            }
        });
    });
});