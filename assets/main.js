// Idée Studio : en-tête au défilement, apparitions, filtres de la boîte à idées.
(() => {
  const top = document.querySelector(".top");
  const onScroll = () => top && top.classList.toggle("scrolled", window.scrollY > 8);
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  const io = "IntersectionObserver" in window
    ? new IntersectionObserver((entries) => entries.forEach((en) => {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      }), { threshold: 0.12 })
    : null;
  document.querySelectorAll(".reveal").forEach((el) => (io ? io.observe(el) : el.classList.add("in")));

  const chips = document.querySelectorAll(".chip");
  const cards = document.querySelectorAll(".card");
  chips.forEach((chip) => chip.addEventListener("click", () => {
    const f = chip.dataset.filtre;
    chips.forEach((c) => c.setAttribute("aria-pressed", String(c === chip)));
    cards.forEach((card) => card.classList.toggle("hide", f !== "all" && card.dataset.stade !== f));
  }));

  document.querySelectorAll("[data-annee]").forEach((el) => (el.textContent = new Date().getFullYear()));
})();
