// Idée Studio : apparitions, aperçu flottant dans l'index, année.
(() => {
  const els = document.querySelectorAll(".chap .txt, .chap .visu, .row, .contact > *");
  els.forEach((el) => el.classList.add("rv"));
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver((list) => list.forEach((en) => {
      if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
    }), { threshold: 0.15 });
    els.forEach((el) => io.observe(el));
  } else els.forEach((el) => el.classList.add("in"));

  const peek = document.querySelector(".peek");
  if (peek && matchMedia("(hover: hover) and (min-width: 901px)").matches) {
    let x = 0, y = 0, raf = 0;
    const move = () => { peek.style.left = x + 24 + "px"; peek.style.top = y + "px"; raf = 0; };
    document.querySelectorAll(".row").forEach((row) => {
      row.addEventListener("mouseenter", () => { peek.src = row.dataset.preview; peek.classList.add("on"); });
      row.addEventListener("mouseleave", () => peek.classList.remove("on"));
      row.addEventListener("mousemove", (ev) => { x = ev.clientX + 120; y = ev.clientY; if (!raf) raf = requestAnimationFrame(move); });
    });
  }
  document.querySelectorAll("[data-annee]").forEach((el) => (el.textContent = new Date().getFullYear()));
})();
