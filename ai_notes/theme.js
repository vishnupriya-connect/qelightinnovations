(() => {
  const key = "qelight-ai-notes-theme";
  const system = window.matchMedia("(prefers-color-scheme: dark)");
  const stored = () => {
    try { return localStorage.getItem(key); }
    catch { return null; }
  };
  const apply = theme => {
    document.documentElement.dataset.theme = theme;
    const button = document.getElementById("theme-toggle");
    if (button) {
      button.textContent = theme === "dark" ? "Light mode" : "Dark mode";
      button.setAttribute("aria-pressed", String(theme === "dark"));
      button.setAttribute("aria-label", theme === "dark" ? "Switch to light mode" : "Switch to dark mode");
    }
  };

  apply(stored() ?? (system.matches ? "dark" : "light"));
  document.addEventListener("DOMContentLoaded", () => {
    apply(document.documentElement.dataset.theme);
    document.getElementById("theme-toggle")?.addEventListener("click", () => {
      const next = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
      try { localStorage.setItem(key, next); } catch { /* Private browsing can block storage. */ }
      apply(next);
    });
  });
  system.addEventListener("change", event => {
    if (!stored()) apply(event.matches ? "dark" : "light");
  });
})();
