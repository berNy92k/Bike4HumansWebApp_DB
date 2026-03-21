document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("user-edit-form");
  const messageBox = document.getElementById("form-message");

  if (!form) return;

  const showMessage = (text, type = "error") => {
    if (!messageBox) return;
    messageBox.textContent = text;
    messageBox.className = `form-message ${type}`;
  };

  const clearMessage = () => {
    if (!messageBox) return;
    messageBox.textContent = "";
    messageBox.className = "form-message";
  };

  const getUserIdFromPath = () => {
    const parts = window.location.pathname.split("/").filter(Boolean);
    return parts.find((part, index) => parts[index - 1] === "users" && /^\d+$/.test(part)) || null;
  };

  const userId = getUserIdFromPath();

  if (!userId) {
    showMessage("Nie udało się odczytać ID użytkownika.");
    return;
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    clearMessage();

    const formData = new FormData(form);

    const payload = {
      username: formData.get("username")?.toString().trim(),
      email: formData.get("email")?.toString().trim(),
      name: formData.get("name")?.toString().trim(),
      surname: formData.get("surname")?.toString().trim(),
      role: formData.get("role")?.toString().trim(),
      is_active: formData.get("is_active") === "on",
      email_verified: formData.get("email_verified") === "on",
    };

    const password = formData.get("password")?.toString().trim();
    if (password) {
      payload.password = password;
    }

    try {
      const response = await fetch(`/admin/users/${userId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        window.location.href = "/admin/user/list";
        return;
      }

      const data = await response.json().catch(() => null);
      showMessage(data?.detail || "Nie udało się zapisać zmian.");
    } catch (error) {
      showMessage("Wystąpił błąd podczas zapisywania użytkownika.");
    }
  });
});
