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

function fly(id, at, length, x, y) {
  move(`${id} .bird`, { x, y, duration: length, ease: "sine.inOut" }, at);
  move(`${id} .wing`, { rotation: -42, duration: .18, repeat: Math.max(0, Math.floor(length/.18)-1),
    yoyo: true, svgOrigin: "118 150", ease: "sine.inOut" }, at);
}
function sleep(id, at, length) {
  tl.set(`${id} .rabbit`, { rotation: -16, y: 56, svgOrigin: "148 245" }, at);
  tl.set(`${id} .rabbit .eye`, { scaleY: .08, transformOrigin: "50% 50%" }, at);
  move(`${id} .rabbit .torso`, { scaleY: 1.025, duration: .8,
    repeat: Math.max(0, Math.floor(length/.8)-1), yoyo: true, transformOrigin: "50% 100%", ease: "sine.inOut" }, at);
  tl.fromTo(`${id} .sleep`, { opacity: .35, y: 20 }, { opacity: 1, y: -25,
    duration: 1.2, repeat: Math.max(0, Math.floor(length/1.2)-1), yoyo: true, ease: "sine.inOut" }, at);
}
function dropStone(id, i, at, speed, waterY) {
  const ox = 1270 + i*48, oy = 785 + i%2*18;
  const stone = `${id} .stone-${i}`;
  move(`${id} .bird`, { x: ox-1190, y: 145, duration: speed*.22 }, at);
  move(`${id} .head`, { rotation: -55, duration: speed*.2, svgOrigin: "109 106" }, at);
  move(`${id} .bird`, { x: 0, y: 0, duration: speed*.24 }, at+speed*.25);
  move(stone, { x: 1145-ox, y: 510-oy, duration: speed*.24 }, at+speed*.25);
  move(`${id} .head`, { rotation: -7, duration: speed*.2, svgOrigin: "109 106" }, at+speed*.25);
  move(stone, { x: 977-ox, y: 458-oy, duration: speed*.22, ease: "sine.out" }, at+speed*.5);
  move(stone, { y: 649-i*45-oy, duration: speed*.2, ease: "power2.in" }, at+speed*.72);
  tl.set(stone, { opacity: 0 }, at+speed*.92);
  tl.set(`${id} .settled-${i}`, { opacity: 1 }, at+speed*.92);
  move(`${id} .water`, { y: waterY, duration: .35 }, at+speed*.92);
  tl.fromTo(`${id} .ripple`, { opacity: .85, scale: .3 }, { opacity: 0, scale: 1.3,
    duration: .6, immediateRender: false, transformOrigin: "50% 50%" }, at+speed*.92);
  for(let j=0;j<5;j++) tl.fromTo(`${id} .splash-${j}`, { opacity: 1, x: 0, y: 0 }, {
    opacity: 0, x: (j-2)*17, y: -45-j%2*20, duration: .5,
    ease: "power2.out", immediateRender: false }, at+speed*.92);
}

for (const section of document.querySelectorAll(".scene")) {
  const id = `#${section.id}`, at = Number(section.dataset.start);
  const length = Number(section.dataset.duration), beat = section.dataset.beat;
  const second = Number(section.dataset.cueSecond);
  tl.fromTo(`${id} .world`, { scale: 1.018, x: 0 }, { scale: 1.055, x: -12,
    duration: length, ease: "sine.inOut", transformOrigin: "50% 60%" }, at);
  reveal(`${id} .chapter`, at+.12);
  if(section.querySelector("h1")) reveal(`${id} h1`, at+.25, .65);
  if(section.querySelector(".subtitle")) reveal(`${id} .subtitle`, at+.48, .65);
  move(`${id} .cloud`, { x: 45, duration: length, ease: "none" }, at);
  move(`${id} .distant`, { x: -18, duration: length, ease: "none" }, at);
  if(section.querySelector(".tree")) move(`${id} .tree`, { x: -30, duration: length, ease: "none" }, at);
  sway(`${id} .plant`, 2, at, length, 1.7);
  sway(`${id} .flower`, 4, at, length, 1.2);
  if(section.querySelector(".bubble")) reveal(`${id} .bubble`, beat==='test'?second:at+.7);
  if(section.querySelector(".spark")) reveal(`${id} .spark`, at+1.1);
  if(section.querySelector(".eye") && !['sleep','overtake','wake'].includes(beat)) {
    for(let i=1.5;i<length-.2;i+=3.7) blink(`${id} .eye`, at+i);
  }

  if(STORY_ID === "crow-water") {
    if(beat==='thirst') {
      tl.fromTo(`${id} .bird`, { x: 340, y: -180 }, { x: -340, y: 110, duration: length, ease: "sine.inOut" }, at);
      move(`${id} .wing`, { rotation: -42, duration: .24, repeat: Math.max(0, Math.floor(length/.24)-1), yoyo: true, svgOrigin: "118 150" }, at);
      move(`${id} .head`, { rotation: 12, duration: 1.5, svgOrigin: "109 106" }, second);
    } else if(beat==='search') {
      fly(id,at,2,-195,40);
      move(`${id} .head`, { rotation: -32, duration: 1, svgOrigin: "109 106" }, at+2);
      move(`${id} .head`, { rotation: 10, duration: .7, svgOrigin: "109 106" }, second);
      fly(id,second+1.1,length-(second-at)-1.3,350,-240);
    } else if(beat==='discover') {
      tl.fromTo(`${id} .bird`, { x: 430, y: -300 }, { x: 0, y: 0, duration: 2, ease: "power2.out" }, at);
      move(`${id} .wing`, { rotation: -42, duration: .18, repeat: 9, yoyo: true, svgOrigin: "118 150" }, at);
      move(`${id} .bird`, { x: -150, y: -190, duration: 1.1 }, second-.3);
      move(`${id} .head`, { rotation: -25, duration: .7, svgOrigin: "109 106" }, second);
    } else if(beat==='reach') {
      move(`${id} .bird`, { x: -195, y: -205, rotation: -7, duration: 1 }, at+.5);
      move(`${id} .head`, { rotation: -32, duration: .7, svgOrigin: "109 106" }, at+1.5);
      move(`${id} .head`, { rotation: -25, duration: .35, repeat: 3, yoyo: true, svgOrigin: "109 106" }, second-.5);
      move(`${id} .bird`, { x: 0, y: 0, rotation: 0, duration: .8 }, second+2);
    } else if(beat==='push') {
      move(`${id} .bird`, { x: -20, y: 40, rotation: -8, duration: 1 }, at+.6);
      for(let t=at+2;t<at+length-2;t+=2) {
        move(`${id} .bird`, { x: -40, rotation: -13, duration: .45, repeat: 1, yoyo: true }, t);
        move(`${id} .wing`, { rotation: -35, duration: .45, repeat: 1, yoyo: true, svgOrigin: "118 150" }, t);
        move(`${id} .pot`, { rotation: -.8, duration: .25, repeat: 1, yoyo: true, transformOrigin: "50% 100%" }, t+.3);
      }
      move(`${id} .bird`, { x: 15, rotation: 0, duration: .8 }, at+length-1.4);
    } else if(beat==='idea') {
      move(`${id} .head`, { rotation: 15, duration: .8, svgOrigin: "109 106" }, at+1);
      move(`${id} .head`, { rotation: -24, duration: .8, svgOrigin: "109 106" }, at+3);
      tl.set(`${id} .idea-light`, { opacity: 0 }, at);
      reveal(`${id} .idea-light`, second-.2);
      move(`${id} .stone-0`, { scale: 1.3, duration: .5, repeat: 3, yoyo: true, transformOrigin: "50% 50%" }, second);
    } else if(['test','repeat'].includes(beat)) {
      tl.set(`${id} .settled, ${id} .splash, ${id} .ripple`, { opacity: 0 }, at);
      if(beat==='test') dropStone(id,0,at+1,Math.max(2,second-at-1.7),-38);
      else for(let i=0;i<4;i++) dropStone(id,i,at+.7+i*(length-1.6)/4,(length-1.6)/4,-30*(i+1));
    } else if(beat==='drink') {
      tl.set(`${id} .splash, ${id} .ripple`, { opacity: 0 }, at);
      move(`${id} .bird`, { x: -158, y: -65, duration: 1.1 }, at+.6);
      move(`${id} .head`, { rotation: -31, duration: .7, svgOrigin: "109 106" }, at+1.4);
      move(`${id} .head`, { rotation: -23, duration: .45, repeat: Math.max(0, Math.floor((length-2.5)/.45)-1), yoyo: true, svgOrigin: "109 106" }, at+2.3);
    } else {
      move(`${id} .head`, { rotation: 5, duration: .5, repeat: 3, yoyo: true, svgOrigin: "109 106" }, at+.5);
      fly(id,second,length-(second-at)-.2,260,-280);
    }
  }

  if(STORY_ID === "turtle-rabbit") {
    if(beat==='rivalry') {
      walk(`${id} .tortoise`,at+1,length-1.2,.5,10);
      move(`${id} .tortoise`, { x: 90, duration: length-1.2, ease: "none" }, at+1);
      move(`${id} .rabbit .arm`, { rotation: -30, duration: .5, repeat: 5, yoyo: true, svgOrigin: "0 10" }, second);
      sway(`${id} .rabbit .ear`,8,second,length-(second-at),.5);
    } else if(beat==='challenge') {
      move(`${id} .tortoise .head`, { y: -12, rotation: -6, duration: .6, repeat: 3, yoyo: true, transformOrigin: "50% 80%" }, at+1);
      move(`${id} .rabbit .head`, { rotation: 8, duration: .5, repeat: 3, yoyo: true, svgOrigin: "160 135" }, second);
    } else if(beat==='start') {
      move(`${id} .flag`, { rotation: -12, duration: .25, repeat: 3, yoyo: true, transformOrigin: "50% 100%" }, second-.3);
      const run=length-(second-at)-.2;
      walk(`${id} .rabbit`,second,run,.14,28); walk(`${id} .tortoise`,second,run,.45,10);
      move(`${id} .rabbit`, { x: 640, duration: run, ease: "power1.in" }, second);
      move(`${id} .tortoise`, { x: 150, duration: run, ease: "none" }, second);
    } else if(beat==='lead') {
      move(`${id} .rabbit`, { x: 390, duration: length-1, ease: "none" }, at);
      walk(`${id} .rabbit`,at,length-1,.14,28);
      move(`${id} .tortoise`, { x: 100, duration: length, ease: "none" }, at);
      walk(`${id} .tortoise`,at,length-.1,.5,10);
      move(`${id} .rabbit .head`, { rotation: -22, duration: .8, svgOrigin: "160 135" }, second);
    } else if(beat==='sleep') {
      tl.set(`${id} .sleep`, { opacity: 0 }, at);
      move(`${id} .rabbit .head`, { rotation: -16, duration: .8, svgOrigin: "160 135" }, second-.6);
      sleep(id,second,length-(second-at)-.1);
    } else if(beat==='steady') {
      move(`${id} .tortoise`, { x: 380, duration: length, ease: "none" }, at);
      walk(`${id} .tortoise`,at,length-.1,.5,10);
      sway(`${id} .tortoise .scarf`,5,at,length,.5);
    } else if(beat==='overtake') {
      sleep(id,at,length-.1);
      move(`${id} .tortoise`, { x: 950, duration: length, ease: "none" }, at);
      walk(`${id} .tortoise`,at,length-.1,.5,10);
    } else if(beat==='wake') {
      sleep(id,at,2);
      move(`${id} .rabbit`, { rotation: 0, y: 0, duration: .4, ease: "back.out(1.5)" }, at+2);
      move(`${id} .rabbit .eye`, { scaleY: 1, duration: .1 }, at+2);
      move(`${id} .sleep`, { opacity: 0, duration: .2 }, at+2);
      sway(`${id} .rabbit .ear`,12,at+2.2,1,.15);
      move(`${id} .rabbit`, { x: 700, duration: length-(second-at), ease: "power2.in" }, second);
      walk(`${id} .rabbit`,second,length-(second-at)-.1,.12,32);
    } else if(beat==='finish') {
      const crossing=second-at;
      move(`${id} .tortoise`, { x: 390, duration: crossing, ease: "none" }, at);
      walk(`${id} .tortoise`,at,crossing,.45,10);
      move(`${id} .ribbon`, { scaleX: 0, opacity: 0, duration: .4, transformOrigin: "50% 50%" }, second-.4);
      move(`${id} .rabbit`, { x: 920, duration: length-1, ease: "power2.out" }, at);
      walk(`${id} .rabbit`,at,length-1,.15,24);
      move(`${id} .spectator`, { y: -15, duration: .3, repeat: 7, yoyo: true, stagger: .09 }, second);
    } else {
      move(`${id} .rabbit .head`, { rotation: 12, y: 10, duration: 1, svgOrigin: "160 135" }, at+.6);
      move(`${id} .rabbit .ear`, { rotation: -24, duration: 1, transformOrigin: "50% 100%" }, at+.6);
      move(`${id} .tortoise .head`, { y: -10, duration: .7, repeat: 3, yoyo: true }, second);
    }
  }

  if(STORY_ID === "foolish-move-mountain") {
    if(beat==='blocked') {
      move(`${id} .elder`, { x: 145, duration: 3, ease: "none" }, second);
      walk(`${id} .elder`,second,3,.5,10);
      move(`${id} .elder .head`, { rotation: -8, duration: .8, transformOrigin: "50% 90%" }, second+3);
    } else if(['plan','question','answer'].includes(beat)) {
      move(`${id} .elder .arm-tool`, { rotation: -24, duration: .7, repeat: 3, yoyo: true, svgOrigin: "0 15" }, second);
      move(`${id} .elder .head`, { rotation: -5, duration: .65, repeat: 3, yoyo: true, transformOrigin: "50% 90%" }, at+1);
      if(beat==='answer') move(`${id} .sage .head`, { y: 8, rotation: 10, duration: 1, transformOrigin: "50% 90%" }, second+1);
    } else if(['dig','generations','seasons'].includes(beat)) {
      for(let i=0;i<3;i++) dig(`${id} .worker-${i}`,at+.3+i*.2,length-.6-i*.2,1.5);
      for(let i=0;i<7;i++) {
        tl.fromTo(`${id} .chip-${i}`, { x: -80, y: -10, opacity: 0 }, {
          x: i*10, y: -70, opacity: 1, duration: .4, immediateRender: false }, at+1.3+i*.13);
        move(`${id} .chip-${i}`, { y: 0, duration: .5 }, at+1.7+i*.13);
      }
      if(beat==='seasons') {
        tl.set(`${id} .winter`, { opacity: 0 }, at);
        move(`${id} .autumn`, { opacity: 0, duration: 1.3 }, second-1);
        move(`${id} .leaf`, { y: 260, rotation: 90, duration: second-at, stagger: .08 }, at);
        move(`${id} .winter`, { opacity: 1, duration: 1.3 }, second-1);
        move(`${id} .snow`, { y: 350, x: 30, duration: length-(second-at)+1, stagger: .04 }, second-1);
      }
    } else if(beat==='carry') {
      for(let i=0;i<3;i++) {
        move(`${id} .carrier-${i}, ${id} .basket-${i}`, { x: 285, duration: length, ease: "none" }, at);
        walk(`${id} .carrier-${i}`,at,length-.1,.55,10);
        move(`${id} .basket-${i}`, { y: -5, duration: .55, repeat: Math.max(0, Math.floor(length/.55)-1), yoyo: true }, at);
      }
    } else if(beat==='doubt') {
      move(`${id} .sage .head`, { rotation: 8, duration: .5, repeat: 5, yoyo: true, transformOrigin: "50% 90%" }, at+1);
      move(`${id} .sage .arm-tool`, { rotation: -28, duration: .8, repeat: 3, yoyo: true, svgOrigin: "0 15" }, second);
    } else if(beat==='divine') {
      tl.fromTo(`${id} .god`, { y: -650, opacity: 0 }, { y: 0, opacity: 1,
        duration: 3, stagger: .3, ease: "power2.out" }, at+.3);
      sway(`${id} .god .halo`,3,at,length,.8);
    } else if(beat==='lift') {
      // The helpers visibly bear the mountains as they lift and carry them away.
      move(`${id} .mountain-left, ${id} .mountain-right`, { scale: .58, y: -365,
        duration: 2.6, transformOrigin: "50% 100%" }, at+.4);
      move(`${id} .god`, { y: -40, duration: 2.6 }, at+.4);
      move(`${id} .mountain-left, ${id} .god-left`, { x: -920, y: -600,
        duration: second-at-2.8, ease: "power2.in" }, at+3.1);
      move(`${id} .mountain-right, ${id} .god-right`, { x: 920, y: -600,
        duration: second-at-2.8, ease: "power2.in" }, at+3.1);
    } else {
      move(`${id} .elder`, { x: 260, y: -100, scale: .9, duration: length, ease: "none" }, at);
      move(`${id} .child`, { x: 250, y: -125, scale: .9, duration: length, ease: "none" }, at);
      walk(`${id} .elder`,at,length-.1,.5,10); walk(`${id} .child`,at,length-.1,.4,14);
    }
  }
}
for (const caption of document.querySelectorAll(".caption")) {
  reveal(`#${caption.id} span`, Number(caption.dataset.start), .16);
}
window.__timelines[STORY_ID] = tl;
