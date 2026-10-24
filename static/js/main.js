(() => {
  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];

  // Clickable room objects scroll to real portfolio sections.
  $$("[data-panel]").forEach(button => {
    button.addEventListener("click", () => {
      const target = $("#" + button.dataset.panel);
      if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });

  // Active navigation follows the visible section.
  const navLinks = $$(".main-nav a");
  const observedSections = $$("main section[id]");
  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          navLinks.forEach(link => link.classList.toggle("active", link.getAttribute("href") === "#" + entry.target.id));
        }
      });
    }, { rootMargin: "-25% 0px -60% 0px" });
    observedSections.forEach(section => observer.observe(section));
  }

  $("#themeToggle")?.addEventListener("click", () => {
    document.body.classList.toggle("light-theme");
  });

  $("#menuToggle")?.addEventListener("click", () => {
    $(".main-nav")?.classList.toggle("open");
  });
  navLinks.forEach(link => link.addEventListener("click", () => $(".main-nav")?.classList.remove("open")));

  // Profile photo preview is local to the visitor's browser; it is not uploaded to the server.
  //$("#avatarUpload")?.addEventListener("change", event => {
    //const file = event.target.files?.[0];
    //if (!file) return;
    //if (!file.type.startsWith("image/")) { alert("Please choose an image file."); return; }
    //if (file.size > 5 * 1024 * 1024) { alert("Choose an image smaller than 5 MB."); return; }
    //const reader = new FileReader();
    //reader.onload = () => { $("#avatarPreview").src = reader.result; };
    //reader.readAsDataURL(file);
  //});

  // Project detail modal reads structured JSON embedded by Django.
  const projectNode = $("#project-data");
  const projects = projectNode ? JSON.parse(projectNode.textContent) : [];
  const modal = $("#projectModal");
  $$(".project-more").forEach(button => button.addEventListener("click", () => {
    const project = projects[Number(button.dataset.project)];
    if (!project || !modal) return;
    $("#modalTitle").textContent = project.name;
    $("#modalDescription").textContent = project.description;
    $("#modalStack").textContent = project.stack;
    modal.classList.add("open");
    modal.setAttribute("aria-hidden", "false");
    $("#modalClose")?.focus();
  }));
  const closeModal = () => { modal?.classList.remove("open"); modal?.setAttribute("aria-hidden", "true"); };
  $("#modalClose")?.addEventListener("click", closeModal);
  modal?.addEventListener("click", event => { if (event.target === modal) closeModal(); });
  document.addEventListener("keydown", event => { if (event.key === "Escape") closeModal(); });

  // Respect browser autoplay restrictions: sound only plays after explicit user action.
  let audioContext = null, oscillator = null, gain = null, soundOn = false;
  function toggleSound() {
    soundOn = !soundOn;
    const buttons = [$("#soundToggle"), $("#musicToggle")].filter(Boolean);
    buttons.forEach(button => button.textContent = soundOn ? "Ⅱ" : (button.id === "musicToggle" ? "▶" : "♫"));
    if (!soundOn) {
      if (gain && audioContext) gain.gain.setTargetAtTime(0, audioContext.currentTime, .08);
      return;
    }
    try {
      const AudioContextClass = window.AudioContext || window.webkitAudioContext;
      if (!AudioContextClass) { alert("Ambient sound is not supported by this browser."); soundOn = false; return; }
      audioContext ||= new AudioContextClass();
      if (!oscillator) {
        oscillator = audioContext.createOscillator();
        gain = audioContext.createGain();
        oscillator.type = "sine";
        oscillator.frequency.value = 110;
        gain.gain.value = 0;
        oscillator.connect(gain);
        gain.connect(audioContext.destination);
        oscillator.start();
      }
      audioContext.resume();
      gain.gain.setTargetAtTime(.012, audioContext.currentTime, .15);
    } catch (_) { soundOn = false; }
  }
  $("#soundToggle")?.addEventListener("click", toggleSound);
  $("#musicToggle")?.addEventListener("click", toggleSound);

  // Search and type filter for the study-material gallery.
  const search = $("#gallerySearch"), filter = $("#galleryFilter");
  function filterGallery() {
    const term = (search?.value || "").trim().toLowerCase();
    const kind = filter?.value || "all";
    $$("#galleryGrid .gallery-card").forEach(card => {
      card.hidden = !(card.dataset.title.includes(term) && (kind === "all" || card.dataset.kind === kind));
    });
  }
  search?.addEventListener("input", filterGallery);
  filter?.addEventListener("change", filterGallery);
})();
