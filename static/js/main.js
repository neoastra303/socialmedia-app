document.addEventListener("DOMContentLoaded", () => {
  const themeSwitcher = document.getElementById("theme-switcher");
  const body = document.body;

  const currentTheme = localStorage.getItem("theme") || "light";
  body.classList.add(`${currentTheme}-theme`);
  themeSwitcher.innerHTML =
    currentTheme === "dark"
      ? '<i class="fas fa-sun"></i>'
      : '<i class="fas fa-moon"></i>';

  themeSwitcher.addEventListener("click", () => {
    body.classList.toggle("dark-theme");
    body.classList.toggle("light-theme");

    let theme = "dark";
    if (body.classList.contains("light-theme")) {
      theme = "light";
    }

    localStorage.setItem("theme", theme);
    themeSwitcher.innerHTML =
      theme === "dark"
        ? '<i class="fas fa-sun"></i>'
        : '<i class="fas fa-moon"></i>';
  });

  // Reaction button functionality
  document.querySelectorAll(".reaction-btn").forEach((button) => {
    button.addEventListener("click", function (e) {
      e.preventDefault();
      const postId = this.dataset.postId;
      const reaction = this.dataset.reaction;
      const dropdown = this.closest(".dropdown");
      const toggle = dropdown.querySelector(".dropdown-toggle");
      const count = toggle.querySelector(".reaction-count");

      fetch(`/posts/${postId}/react/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]")
            .value,
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `reaction=${reaction}`,
      })
        .then((response) => response.json())
        .then((data) => {
          count.textContent = data.total_reactions;
          if (data.reacted) {
            // Update button icon
            const icon = {
              like: "👍",
              love: "❤️",
              laugh: "😂",
              angry: "😠",
              sad: "😢",
            }[data.reaction_type];
            toggle.innerHTML = `${icon} <span class="reaction-count">${data.total_reactions}</span>`;
          } else {
            toggle.innerHTML = `👍 <span class="reaction-count">${data.total_reactions}</span>`;
          }
        })
        .catch((error) => console.error("Error:", error));
    });
  });

  // Form validation for registration and profile update
  const forms = document.querySelectorAll("form");
  forms.forEach((form) => {
    form.addEventListener("submit", function (e) {
      const requiredFields = form.querySelectorAll("[required]");
      let valid = true;
      requiredFields.forEach((field) => {
        if (!field.value.trim()) {
          field.classList.add("is-invalid");
          valid = false;
        } else {
          field.classList.remove("is-invalid");
        }
      });
      if (!valid) {
        e.preventDefault();
        alert("Please fill in all required fields.");
      }
    });
  });

  // Image preview for profile picture upload
  const imageInput = document.querySelector('input[type="file"][name="image"]');
  if (imageInput) {
    imageInput.addEventListener("change", function () {
      const file = this.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
          document.querySelector(".profile-img-preview").src = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    });
  }
});
