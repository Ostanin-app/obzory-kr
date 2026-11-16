/* Увеличение рисунков: клик по картинке открывает её крупно,
   повторный клик — масштаб 1:1, Esc или крестик закрывают. */
(function () {
  "use strict";

  var overlay = null;
  var overlayImg = null;
  var hint = null;
  var lastFocus = null;

  function build() {
    overlay = document.createElement("div");
    overlay.className = "zoom-overlay";
    overlay.hidden = true;
    overlay.setAttribute("role", "dialog");
    overlay.setAttribute("aria-modal", "true");
    overlay.setAttribute("aria-label", "Увеличенный рисунок");

    var close = document.createElement("button");
    close.type = "button";
    close.className = "zoom-close";
    close.setAttribute("aria-label", "Закрыть");
    close.textContent = "×";

    overlayImg = document.createElement("img");
    overlayImg.alt = "";

    hint = document.createElement("div");
    hint.className = "zoom-hint";
    hint.textContent = "нажмите на рисунок — масштаб 1:1";

    overlay.appendChild(overlayImg);
    overlay.appendChild(close);
    overlay.appendChild(hint);
    document.body.appendChild(overlay);

    close.addEventListener("click", hide);
    overlay.addEventListener("click", function (e) {
      if (e.target === overlay) hide();
    });
    overlayImg.addEventListener("click", function (e) {
      e.stopPropagation();
      setZoomed(!overlay.classList.contains("is-zoomed"));
    });
  }

  function setZoomed(on) {
    overlay.classList.toggle("is-zoomed", on);
    hint.textContent = on
      ? "нажмите на рисунок, чтобы вернуть по размеру экрана"
      : "нажмите на рисунок — масштаб 1:1";
    if (on) {
      overlay.scrollTop = 0;
      overlay.scrollLeft = 0;
    }
  }

  function show(src, alt) {
    if (!overlay) build();
    lastFocus = document.activeElement;
    overlayImg.src = src;
    overlayImg.alt = alt || "";
    overlay.hidden = false;
    document.body.classList.add("zoom-open");
    setZoomed(false);
    overlay.querySelector(".zoom-close").focus();
  }

  function hide() {
    if (!overlay || overlay.hidden) return;
    overlay.hidden = true;
    overlayImg.removeAttribute("src");
    document.body.classList.remove("zoom-open");
    setZoomed(false);
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  document.addEventListener("click", function (e) {
    var img = e.target.closest && e.target.closest("figure.fig img, img.zoomable");
    if (!img) return;
    e.preventDefault();
    show(img.currentSrc || img.src, img.alt);
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") hide();
  });
})();
