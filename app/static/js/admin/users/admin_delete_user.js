document.addEventListener("DOMContentLoaded", () => {
    const deleteButtons = document.querySelectorAll("[data-user-id]");

    deleteButtons.forEach((button) => {
        button.addEventListener("click", async (event) => {
            event.preventDefault();

            const userId = button.dataset.userId;
            const shouldDelete = confirm("Na pewno usunąć tego użytkownika?");
            if (!shouldDelete) {
                return;
            }

            try {
                const response = await fetch(`/admin/user/${userId}`, {
                    method: "DELETE"
                });

                if (response.ok) {
                    window.location.reload();
                    return;
                }

                alert("Nie udało się usunąć użytkownika.");
            } catch (error) {
                alert("Wystąpił błąd podczas usuwania użytkownika.");
            }
        });
    });
});
