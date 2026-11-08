// Idée Studio : en-tête au défilement, apparitions douces, année.
(() => {
  const top = document.querySelector(".top");
  const onScroll = () => top.classList.toggle("scrolled", scrollY > 4);
  onScroll(); addEventListener("scroll", onScroll, { passive: true });
  const els = document.querySelectorAll(".svc, .case, .steps li, .studio-grid > *");
  els.forEach((el) => el.classList.add("rv"));
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver((list) => list.forEach((en) => {
      if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
    }), { threshold: 0.12 });
    els.forEach((el) => io.observe(el));
  } else els.forEach((el) => el.classList.add("in"));
  document.querySelectorAll("[data-annee]").forEach((el) => (el.textContent = new Date().getFullYear()));
})();
