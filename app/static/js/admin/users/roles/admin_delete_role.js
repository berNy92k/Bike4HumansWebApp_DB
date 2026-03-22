document.addEventListener("DOMContentLoaded", () => {
    const deleteButtons = document.querySelectorAll("[data-role-id]");

    deleteButtons.forEach((button) => {
        button.addEventListener("click", async (event) => {
            event.preventDefault();

            const roleId = button.dataset.roleId;
            const shouldDelete = confirm("Na pewno usunąć tę rolę?");
            if (!shouldDelete) {
                return;
            }

            try {
                const response = await fetch(`/admin/user/role/${roleId}`, {
                    method: "DELETE"
                });

                if (response.ok) {
                    window.location.reload();
                    return;
                }

                alert("Nie udało się usunąć roli.");
            } catch (error) {
                alert("Wystąpił błąd podczas usuwania roli.");
            }
        });
    });
});
