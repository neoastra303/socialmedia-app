// Theme switcher functionality
(function () {
  const themeKey = "theme-preference";
  const savedTheme = localStorage.getItem(themeKey);
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  const initialTheme = savedTheme || (prefersDark ? "dark" : "light");

  document.documentElement.setAttribute("data-theme", initialTheme);
  localStorage.setItem(themeKey, initialTheme);

  document.addEventListener("DOMContentLoaded", function () {
    const themeSwitcher = document.getElementById("theme-switcher");
    if (!themeSwitcher) return;

    function updateThemeIcon(theme) {
      const icon = themeSwitcher.querySelector("i");
      if (icon) {
        icon.className = theme === "dark" ? "fas fa-sun" : "fas fa-moon";
      }
    }

    updateThemeIcon(initialTheme);

    themeSwitcher.addEventListener("click", function () {
      const root = document.documentElement;
      const current = root.getAttribute("data-theme");
      const next = current === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      localStorage.setItem(themeKey, next);
      updateThemeIcon(next);
    });
  });
})();

// Auto-hide alerts after 5 seconds
document.addEventListener("DOMContentLoaded", function () {
  const alerts = document.querySelectorAll(".alert");
  alerts.forEach(function (alert) {
    setTimeout(function () {
      const bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    }, 5000);
  });
});

// AJAX reaction handling
document.addEventListener("DOMContentLoaded", function () {
  const reactionButtons = document.querySelectorAll(".reactions form");
  reactionButtons.forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();

      const formData = new FormData(form);
      const url = form.getAttribute("action");

      fetch(url, {
        method: "POST",
        body: formData,
        headers: {
          "X-Requested-With": "XMLHttpRequest",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.status === "success") {
            location.reload(); // Simple reload for now
          }
        })
        .catch((error) => console.error("Error:", error));
    });
  });
});

// Form submission with AJAX
function submitFormWithAjax(formId, successCallback) {
  const form = document.getElementById(formId);
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();

      const formData = new FormData(form);
      const url = form.getAttribute("action");

      fetch(url, {
        method: "POST",
        body: formData,
        headers: {
          "X-Requested-With": "XMLHttpRequest",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.status === "success" && successCallback) {
            successCallback(data);
          }
        })
        .catch((error) => console.error("Error:", error));
    });
  }
}
