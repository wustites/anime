// Every move belongs to one paused timeline. Static SVG placement stays on
// the parent group, while articulated parts animate in their local coordinates.
window.__timelines = window.__timelines || {};
const tl = gsap.timeline({ paused: true, defaults: { ease: "power2.inOut" } });
const root = document.getElementById("book");
const duration = Number(root.dataset.duration);

function move(selector, vars, at) {
  tl.to(selector, { ...vars, immediateRender: false }, at);
}
function reveal(selector, at, length = 0.5) {
  tl.fromTo(selector, { opacity: 0, y: 18 },
    { opacity: 1, y: 0, duration: length, ease: "power2.out" }, at);
}
function sway(selector, angle, at, length, cycle = 1.5) {
  tl.fromTo(selector, { rotation: -angle }, {
    rotation: angle, duration: cycle, repeat: Math.max(0, Math.floor(length / cycle) - 1),
    yoyo: true, ease: "sine.inOut", transformOrigin: "50% 100%",
  }, at);
}
function blink(selector, at) {
  move(selector, { scaleY: 0.09, duration: 0.09, repeat: 1,
    yoyo: true, transformOrigin: "50% 50%", ease: "power1.inOut" }, at);
}
function walk(selector, at, length, stride = 0.3, strength = 12) {
  const count = Math.max(0, Math.floor(length / stride) - 1);
  tl.fromTo(`${selector} .leg-a`, { rotation: -strength }, {
    rotation: strength, duration: stride, repeat: count, yoyo: true,
    svgOrigin: "15 10", ease: "sine.inOut",
  }, at);
  tl.fromTo(`${selector} .leg-b`, { rotation: strength }, {
    rotation: -strength, duration: stride, repeat: count, yoyo: true,
    svgOrigin: "15 10", ease: "sine.inOut",
  }, at);
  tl.fromTo(`${selector} .torso, ${selector} .shell`, { y: 0 }, {
    y: -5, duration: stride, repeat: count, yoyo: true, ease: "sine.inOut",
  }, at);
  move(`${selector} .head`, { rotation: 2, duration: stride * 2,
    repeat: Math.max(0, Math.floor(length / (stride * 2)) - 1), yoyo: true,
    transformOrigin: "50% 80%", ease: "sine.inOut" }, at);
}
function dig(selector, at, length, cycle = 0.95) {
  for (let beat = at; beat + cycle <= at + length; beat += cycle) {
    move(`${selector} .arm-tool`, { rotation: -32, duration: cycle * 0.42,
      svgOrigin: "0 15", ease: "power2.out" }, beat);
    move(`${selector} .arm-tool`, { rotation: 105, duration: cycle * 0.23,
      svgOrigin: "0 15", ease: "power3.in" }, beat + cycle * 0.42);
    move(`${selector} .arm-tool`, { rotation: 0, duration: cycle * 0.35,
      svgOrigin: "0 15", ease: "power2.out" }, beat + cycle * 0.65);
    move(`${selector} .torso, ${selector} .head`, { y: 8, rotation: 3,
      duration: cycle * 0.23, yoyo: true, repeat: 1,
      transformOrigin: "50% 100%" }, beat + cycle * 0.42);
    if (document.querySelector(selector + " .beard")) {
      move(`${selector} .beard`, { rotation: 8, duration: cycle * 0.3,
        repeat: 1, yoyo: true, transformOrigin: "50% 0%" }, beat + cycle * 0.48);
    }
  }
}

for (const section of document.querySelectorAll(".scene")) {
  const id = `#${section.id}`;
  const start = Number(section.dataset.start);
  const length = Number(section.dataset.duration);
  // A slow camera push supplies depth without moving the reading layer.
  tl.fromTo(`${id} .world`, { scale: 1.018, x: 0 }, {
    scale: 1.055, x: -12, duration: length, ease: "sine.inOut",
    transformOrigin: "50% 60%",
  }, start);
  reveal(`${id} .chapter`, start + 0.12);
  const delayedMoral = STORY_ID === "foolish-move-mountain" && section.id === "s4";
  if (!delayedMoral && section.querySelector("h1")) reveal(`${id} h1`, start + 0.25, 0.65);
  if (!delayedMoral && section.querySelector(".subtitle")) reveal(`${id} .subtitle`, start + 0.48, 0.65);
  move(`${id} .cloud`, { x: 45, duration: length, ease: "none" }, start);
  move(`${id} .distant`, { x: -18, duration: length, ease: "none" }, start);
  if (section.querySelector(".tree")) move(`${id} .tree`, { x: -30, duration: length, ease: "none" }, start);
  move(`${id} .plant`, { x: -48, duration: length, ease: "none" }, start);
  sway(`${id} .plant`, 2, start, length, 1.7);
  sway(`${id} .flower`, 4, start, length, 1.2);
  if (section.querySelector(".bubble") && !(STORY_ID === "turtle-rabbit" && section.id === "s2")) {
    tl.fromTo(`${id} .bubble`, { opacity: 0, scale: 0.8 }, {
      opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.3)",
      transformOrigin: "50% 100%",
    }, start + 0.6);
  }
  if (section.querySelector(".spark")) {
    tl.fromTo(`${id} .spark`, { opacity: 0, scale: 0.2 }, {
      opacity: 1, scale: 1, duration: 0.6, stagger: 0.1,
      transformOrigin: "50% 50%", ease: "back.out(2)",
    }, start + (STORY_ID === "crow-water" && section.id === "s3" ? 4.4 : 1.1));
  }
  if (section.querySelector(".eye")) {
    const eyes = STORY_ID === "turtle-rabbit" && ["s2", "s3"].includes(section.id)
      ? `${id} .tortoise .eye` : `${id} .eye`;
    blink(eyes, start + Math.min(1.5, length - 0.4));
    if (length > 4) blink(eyes, start + 3.7);
  }
}
for (const caption of document.querySelectorAll(".caption")) {
  tl.fromTo(`#${caption.id} span`, { opacity: 0, y: 8 }, {
    opacity: 1, y: 0, duration: 0.16, ease: "power1.out",
  }, Number(caption.dataset.start));
}

if (STORY_ID === "crow-water") {
  tl.fromTo("#s1 .bird", { x: 400, y: -300, rotation: -12 }, {
    x: 0, y: 0, rotation: 0, duration: 1.55, ease: "power2.out",
  }, 0);
  move("#s1 .wing", { rotation: -42, duration: 0.15, repeat: 8,
    yoyo: true, svgOrigin: "118 150", ease: "sine.inOut" }, 0);
  move("#s1 .landing-shadow", { scaleX: 0.7, duration: 0.7, repeat: 1,
    yoyo: true, transformOrigin: "50% 50%" }, 0.1);

  // Lean in, try to reach the low water, then pull back and look at the stones.
  move("#s2 .bird", { x: -198, y: -200, rotation: -7, duration: 0.8 }, 2.15);
  move("#s2 .head", { rotation: -27, duration: 0.5,
    svgOrigin: "109 106" }, 2.7);
  move("#s2 .wing", { rotation: -25, duration: 0.45, yoyo: true,
    repeat: 1, svgOrigin: "118 150" }, 3.1);
  move("#s2 .bird", { x: 0, y: 0, rotation: 0, duration: 0.65,
    ease: "back.out(1.2)" }, 4.05);
  move("#s2 .head", { rotation: 13, duration: 0.6,
    svgOrigin: "109 106" }, 4.45);
  move("#s2 .bubble", { opacity: 0, duration: 0.25 }, 5.65);

  // Each stone follows ground -> beak -> jar -> water. Water rises on impact.
  tl.set("#s3 .settled, #s3 .splash, #s3 .ripple", { opacity: 0 }, 6.2);
  for (let i = 0; i < 4; i++) {
    const at = 7.4 + i * 0.85;
    const originX = 1270 + i * 48;
    const originY = 785 + (i % 2) * 18;
    const selector = `#s3 .stone-${i}`;
    move("#s3 .bird", { x: originX - 1190, y: 145, duration: 0.2,
      ease: "power2.inOut" }, at);
    move("#s3 .head", { rotation: -55, y: 0, duration: 0.18,
      svgOrigin: "109 106" }, at);
    move("#s3 .bird", { x: 0, y: 0, duration: 0.25,
      ease: "power2.out" }, at + 0.22);
    move(selector, { x: 1145 - originX, y: 510 - originY,
      duration: 0.25, ease: "power2.out" }, at + 0.22);
    move("#s3 .head", { rotation: -7, y: 0, duration: 0.2,
      svgOrigin: "109 106" }, at + 0.22);
    move("#s3 .wing", { rotation: -35, duration: 0.12,
      repeat: 1, yoyo: true, svgOrigin: "118 150" }, at + 0.22);
    move(selector, { x: 977 - originX, y: 458 - originY,
      duration: 0.22, ease: "sine.out" }, at + 0.47);
    move(selector, { y: 649 - i * 50 - originY,
      duration: 0.16, ease: "power2.in" }, at + 0.69);
    move(selector, { opacity: 0, duration: 0.03 }, at + 0.85);
    tl.set(`#s3 .settled-${i}`, { opacity: 1 }, at + 0.85);
    move("#s3 .water", { y: -38 * (i + 1), duration: 0.22,
      ease: "power1.out" }, at + 0.85);
    tl.fromTo("#s3 .ripple", { opacity: 0.85, scale: 0.3 }, {
      opacity: 0, scale: 1.3, duration: 0.45, immediateRender: false,
      transformOrigin: "50% 50%",
    }, at + 0.84);
    for (let drop = 0; drop < 5; drop++) {
      tl.fromTo(`#s3 .splash-${drop}`, { opacity: 1, x: 0, y: 0 }, {
        opacity: 0, x: (drop - 2) * 17, y: -45 - (drop % 2) * 20,
        duration: 0.38, ease: "power2.out", immediateRender: false,
      }, at + 0.84);
    }
  }
  move("#s3 .bubble", { opacity: 0, duration: 0.2 }, 7.35);
  move("#s3 .bird", { x: -158, y: -65, duration: 0.55 }, 11.6);
  move("#s3 .head", { rotation: -31, duration: 0.45,
    svgOrigin: "109 106" }, 11.75);
  move("#s3 .head", { rotation: -23, duration: 0.17,
    repeat: 3, yoyo: true, svgOrigin: "109 106" }, 12.15);
  walk("#s4 .bird", 13.2, 2, 0.28, 7);
  move("#s4 .wing", { rotation: -32, duration: 0.32,
    repeat: 3, yoyo: true, svgOrigin: "118 150" }, 14.2);
  move("#s4 .bird", { y: -18, duration: 0.35,
    repeat: 3, yoyo: true, ease: "sine.inOut" }, 14.2);
  reveal(".seal", 13.85);
}

if (STORY_ID === "turtle-rabbit") {
  move("#s1 .flag", { rotation: -5, duration: 0.25,
    repeat: 5, yoyo: true, transformOrigin: "50% 100%" }, 2.15);
  walk("#s1 .rabbit", 2.2, 1.5, 0.14, 28);
  walk("#s1 .tortoise", 2.2, 1.5, 0.45, 10);
  move("#s1 .rabbit", { x: 200, duration: 1.5, ease: "power2.in" }, 2.2);
  move("#s1 .tortoise", { x: 65, duration: 1.5, ease: "none" }, 2.2);

  // A rapid run decelerates under the tree; ears and arms carry the momentum.
  tl.fromTo("#s2 .rabbit", { x: -920 }, { x: 50,
    duration: 2.6, ease: "power2.out" }, 3.8);
  walk("#s2 .rabbit", 3.8, 2.7, 0.13, 30);
  sway("#s2 .rabbit .ear", 12, 3.8, 2.6, 0.26);
  move("#s2 .rabbit .arm", { rotation: -30, duration: 0.15,
    repeat: 15, yoyo: true, svgOrigin: "0 10" }, 3.8);
  move("#s2 .rabbit", { y: 56, rotation: -16, duration: 0.65,
    svgOrigin: "148 245" }, 6.65);
  move("#s2 .rabbit .head", { rotation: -16, duration: 0.6,
    svgOrigin: "160 135" }, 6.7);
  move("#s2 .rabbit .eye", { scaleY: 0.08, duration: 0.3,
    transformOrigin: "50% 50%" }, 7.3);
  // Keep the sleeping eyes shut even after the general blink for this scene.
  tl.set("#s2 .rabbit .eye", { scaleY: 0.08 }, 7.65);
  move("#s2 .rabbit .torso", { scaleY: 1.025, duration: 0.7,
    yoyo: true, repeat: 2, transformOrigin: "50% 100%", ease: "sine.inOut" }, 7.7);
  tl.fromTo("#s2 .sleep", { opacity: 0, y: 25 }, {
    opacity: 1, y: -15, duration: 0.8, repeat: 2, yoyo: true,
    ease: "sine.inOut",
  }, 7.3);
  tl.set("#s2 .bubble", { opacity: 0 }, 3.8);
  reveal("#s2 .bubble", 7.15);
  move("#s2 .tortoise", { x: 195, duration: 6.4, ease: "none" }, 3.8);
  walk("#s2 .tortoise", 3.8, 6.3, 0.5, 11);

  move("#s3 .tortoise", { x: 760, duration: 7.25, ease: "none" }, 10.2);
  walk("#s3 .tortoise", 10.2, 7.2, 0.4, 12);
  move("#s3 .tortoise .scarf", { rotation: 5, duration: 0.45,
    repeat: 14, yoyo: true, svgOrigin: "293 210" }, 10.2);
  tl.set("#s3 .rabbit", { rotation: -16, y: 50, opacity: 0.8 }, 10.2);
  tl.set("#s3 .rabbit .eye", { scaleY: 0.08,
    transformOrigin: "50% 50%" }, 10.2);
  move("#s3 .rabbit", { rotation: 0, y: 0, opacity: 1,
    duration: 0.3, ease: "back.out(1.5)" }, 14.1);
  move("#s3 .rabbit .eye", { scaleY: 1, duration: 0.1 }, 14.1);
  move("#s3 .rabbit .ear", { rotation: 15, duration: 0.12,
    repeat: 1, yoyo: true, transformOrigin: "50% 100%" }, 14.2);
  move("#s3 .rabbit", { x: 770, duration: 2.8, ease: "power2.in" }, 14.5);
  walk("#s3 .rabbit", 14.5, 2.9, 0.12, 32);
  move("#s3 .bubble", { opacity: 0, duration: 0.25 }, 13.8);

  move("#s4 .tortoise", { x: 190, duration: 1, ease: "power1.out" }, 17.5);
  walk("#s4 .tortoise", 17.5, 1, 0.3, 13);
  move("#s4 .ribbon", { scaleX: 0, opacity: 0, duration: 0.35,
    transformOrigin: "50% 50%" }, 17.85);
  move("#s4 .rabbit", { x: 255, duration: 0.85, ease: "power2.out" }, 17.5);
  walk("#s4 .rabbit", 17.5, 0.85, 0.13, 24);
  move("#s4 .rabbit .head", { rotation: 12, y: 10, duration: 0.6,
    svgOrigin: "160 135" }, 18.45);
  move("#s4 .rabbit .ear", { rotation: -24, duration: 0.6,
    transformOrigin: "50% 100%" }, 18.45);
  move("#s4 .tortoise .head", { y: -10, duration: 0.5,
    repeat: 3, yoyo: true, ease: "sine.inOut" }, 18.7);
  move("#s4 .spectator", { y: -15, duration: 0.3, repeat: 5,
    yoyo: true, stagger: 0.09, ease: "sine.inOut" }, 18.1);
}

if (STORY_ID === "foolish-move-mountain") {
  move("#s1 .elder", { x: 150, duration: 3.1, ease: "none" }, 1.3);
  walk("#s1 .elder", 1.3, 3, 0.5, 10);
  move("#s1 .elder .head", { rotation: -8, duration: 0.8,
    transformOrigin: "50% 90%" }, 4.5);
  move("#s1 .elder .arm-tool", { rotation: -13, duration: 0.6,
    svgOrigin: "0 15" }, 5.4);

  dig("#s2 .elder", 8.1, 2.9, 0.95);
  tl.set("#s2 .chip", { opacity: 0 }, 7.8);
  for (let i = 0; i < 7; i++) {
    const impact = 8.72 + (i % 3) * 0.95;
    tl.fromTo(`#s2 .chip-${i}`, { x: -120, y: -35, opacity: 1 }, {
      x: 25 + i * 12, y: -90 - (i % 3) * 18,
      rotation: 100 + i * 35, duration: 0.22,
      ease: "power1.out", immediateRender: false,
    }, impact);
    move(`#s2 .chip-${i}`, { y: 5, opacity: 0.85,
      duration: 0.33, ease: "power2.in" }, impact + 0.22);
  }
  for (let i = 0; i < 4; i++) dig(`#s3 .worker-${i}`, 11.25 + i * 0.15, 6.3 - i * 0.15, 1.1);
  move("#s3 .rock-pile", { y: -8, duration: 0.15, repeat: 1,
    yoyo: true, stagger: 0.03 }, 14.05);

  // Mountain silhouettes remain intact while they separate; the road underneath
  // is revealed rather than swapping the landscape for a static moral slide.
  move("#s4 .mountain-left", { x: -760, y: 100, duration: 2.8,
    ease: "power3.inOut" }, 18.1);
  move("#s4 .mountain-right", { x: 770, y: 110, duration: 2.8,
    ease: "power3.inOut" }, 18.1);
  tl.fromTo("#s4 .open-road", { opacity: 0 }, {
    opacity: 1, duration: 1.6, ease: "sine.inOut",
  }, 18.5);
  tl.fromTo("#s4 h1, #s4 .subtitle", { opacity: 0, y: 18 }, {
    opacity: 1, y: 0, duration: 0.8, stagger: 0.2,
    immediateRender: false, ease: "power2.out",
  }, 20.9);
  tl.set("#s4 h1, #s4 .subtitle", { opacity: 0 }, 18.1);
  move("#s4 .elder", { x: 290, y: -110, scale: 0.9, duration: 3, ease: "none" }, 21.2);
  move("#s4 .child", { x: 270, y: -150, scale: 0.9, duration: 3, ease: "none" }, 21.2);
  walk("#s4 .elder", 21.2, 3, 0.45, 11);
  walk("#s4 .child", 21.2, 3, 0.35, 17);
}
window.__timelines[STORY_ID] = tl;
