// @spec WRIT-POST-021 — included only on pages opting into math.
window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
  },
  options: { skipHtmlTags: ["script", "noscript", "style", "textarea", "pre", "code"] },
};
