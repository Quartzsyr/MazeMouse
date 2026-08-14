const PATH = [
  [0, 0], [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [0, 4], [0, 5], [1, 5],
  [2, 5], [2, 6], [1, 6], [0, 6], [0, 7], [1, 7], [2, 7], [3, 7], [3, 6],
  [3, 5], [4, 5], [4, 4], [5, 4], [5, 3], [6, 3], [6, 2], [6, 1], [6, 0],
  [7, 0], [7, 1], [7, 2], [7, 3], [7, 4], [7, 5], [7, 6], [7, 7]
];

const SEGMENTS = [
  [1, 0, 1, 1], [1, 1, 2, 1], [2, 1, 3, 1], [3, 1, 4, 1], [6, 0, 6, 1],
  [8, 0, 8, 1], [0, 2, 1, 2], [1, 2, 2, 2], [2, 2, 3, 2], [3, 2, 4, 2],
  [5, 1, 5, 2], [4, 2, 5, 2], [6, 1, 6, 2], [7, 1, 7, 2], [8, 1, 8, 2],
  [2, 3, 3, 3], [3, 3, 4, 3], [5, 2, 5, 3], [5, 3, 6, 3], [7, 2, 7, 3],
  [6, 3, 7, 3], [8, 2, 8, 3], [1, 3, 1, 4], [1, 4, 2, 4], [2, 4, 3, 4],
  [4, 3, 4, 4], [5, 3, 5, 4], [4, 4, 5, 4], [6, 4, 7, 4], [8, 3, 8, 4],
  [7, 4, 8, 4], [1, 4, 1, 5], [0, 5, 1, 5], [4, 4, 4, 5], [3, 5, 4, 5],
  [6, 4, 6, 5], [5, 5, 6, 5], [8, 4, 8, 5], [2, 5, 2, 6], [1, 6, 2, 6],
  [3, 5, 3, 6], [2, 6, 3, 6], [5, 5, 5, 6], [4, 6, 5, 6], [7, 5, 7, 6],
  [6, 6, 7, 6], [8, 5, 8, 6], [1, 7, 2, 7], [2, 7, 3, 7], [4, 6, 4, 7],
  [3, 7, 4, 7], [4, 7, 5, 7], [5, 7, 6, 7], [7, 6, 7, 7], [6, 7, 7, 7],
  [8, 6, 8, 7], [0, 8, 1, 8], [1, 8, 2, 8], [2, 8, 3, 8], [3, 8, 4, 8],
  [4, 8, 5, 8], [5, 8, 6, 8], [6, 8, 7, 8], [8, 7, 8, 8], [7, 8, 8, 8],
  [0, 0, 1, 0], [1, 0, 2, 0], [2, 0, 3, 0], [3, 0, 4, 0], [4, 0, 5, 0],
  [5, 0, 6, 0], [6, 0, 7, 0], [7, 0, 8, 0], [0, 0, 0, 1], [0, 1, 0, 2],
  [0, 2, 0, 3], [0, 3, 0, 4], [0, 4, 0, 5], [0, 5, 0, 6], [0, 6, 0, 7],
  [0, 7, 0, 8]
];

function clamp(value, minimum, maximum) {
  return Math.min(Math.max(value, minimum), maximum);
}

function smoothstep(value) {
  const progress = clamp(value, 0, 1);
  return progress * progress * (3 - 2 * progress);
}

function mix(start, end, progress) {
  return start + (end - start) * progress;
}

function formatNumber(value) {
  return new Intl.NumberFormat("zh-CN").format(value);
}

async function loadReleases() {
  const repository = "Quartzsyr/MazeMouse";
  const countNodes = document.querySelectorAll("[data-download-count]");
  const list = document.querySelector("#release-list");
  const toggle = document.querySelector("#release-toggle");

  const setCount = (value) => {
    countNodes.forEach((node) => { node.textContent = value; });
  };

  try {
    const response = await fetch(`https://api.github.com/repos/${repository}/releases?per_page=100`, {
      headers: { Accept: "application/vnd.github+json" },
    });
    if (!response.ok) throw new Error(`GitHub API responded with ${response.status}`);
    const releases = await response.json();

    releases.sort((a, b) => new Date(b.published_at) - new Date(a.published_at));

    const totalDownloads = releases.reduce((total, release) => total + (release.assets || []).reduce(
      (assetTotal, asset) => assetTotal + (asset.download_count || 0), 0
    ), 0);
    setCount(formatNumber(totalDownloads));

    const visibleCount = 3;
    const fragment = document.createDocumentFragment();

    releases.forEach((release, index) => {
      const title = release.name || release.tag_name || "Release";
      const date = new Date(release.published_at).toLocaleDateString("zh-CN", {
        year: "numeric", month: "short", day: "numeric"
      });
      const asset = (release.assets || [])[0];
      const downloadUrl = asset ? asset.browser_download_url : release.html_url;
      const assetName = asset
        ? (asset.name.toLowerCase().endsWith(".exe") ? "Windows 安装包" : asset.name)
        : "查看 Release";

      const item = document.createElement("article");
      item.className = "release-item";
      if (index >= visibleCount) item.classList.add("is-hidden");

      const main = document.createElement("div");
      main.className = "release-main";

      const titleRow = document.createElement("div");
      titleRow.className = "release-title";
      const strong = document.createElement("strong");
      strong.textContent = title;
      titleRow.appendChild(strong);

      const tag = document.createElement("span");
      tag.className = "tag";
      tag.textContent = release.tag_name;
      titleRow.appendChild(tag);

      if (release.prerelease) {
        const badge = document.createElement("span");
        badge.className = "badge";
        badge.textContent = "预发布";
        titleRow.appendChild(badge);
      }

      const meta = document.createElement("div");
      meta.className = "release-meta";
      const dateSpan = document.createElement("span");
      dateSpan.textContent = date;
      const sizeSpan = document.createElement("span");
      sizeSpan.textContent = asset && asset.size ? `${(asset.size / 1048576).toFixed(1)} MB` : "文件";
      meta.append(dateSpan, sizeSpan);

      main.append(titleRow, meta);
      item.appendChild(main);

      const download = document.createElement("a");
      download.className = "release-download";
      download.href = downloadUrl;
      download.setAttribute("target", "_blank");
      download.setAttribute("rel", "noreferrer");
      download.textContent = assetName;
      item.appendChild(download);

      fragment.appendChild(item);
    });

    list.replaceChildren(fragment);

    if (releases.length > visibleCount) {
      toggle.hidden = false;
      let expanded = false;
      toggle.addEventListener("click", () => {
        expanded = !expanded;
        const items = list.querySelectorAll(".release-item");
        items.forEach((item, index) => {
          if (index >= visibleCount) item.classList.toggle("is-hidden", !expanded);
        });
        toggle.textContent = expanded ? "收起版本" : "展开全部版本";
      });
    } else {
      toggle.hidden = true;
    }
  } catch (error) {
    setCount("—");
    if (list) {
      list.innerHTML = '<p class="release-empty">版本信息暂时无法加载，<a href="https://github.com/Quartzsyr/MazeMouse/releases" target="_blank" rel="noreferrer">前往 GitHub Releases ↗</a></p>';
    }
    if (toggle) toggle.hidden = true;
  }
}

function setupReveals() {
  const elements = document.querySelectorAll(".reveal");
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add("is-visible");
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.14 });

  elements.forEach((element, index) => {
    element.style.transitionDelay = `${Math.min(index % 4, 3) * 70}ms`;
    observer.observe(element);
  });
}

async function setupMaze() {
  const canvas = document.querySelector("#maze-canvas");
  if (!canvas) return;

  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const THREE = await import("https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js");

  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.outputColorSpace = THREE.SRGBColorSpace;

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(32, 1, 0.1, 100);

  const maze = new THREE.Group();
  scene.add(maze);

  const worldPoint = ([row, col]) => new THREE.Vector3(col + 0.5, 0, row + 0.5);
  const pathPoints = PATH.map(worldPoint);

  const floor = new THREE.Mesh(
    new THREE.BoxGeometry(8, 0.08, 8),
    new THREE.MeshStandardMaterial({ color: 0x0c1916, roughness: 0.82, metalness: 0.08 })
  );
  floor.position.set(4, -0.05, 4);
  maze.add(floor);

  const grid = new THREE.GridHelper(8, 8, 0x2c4a40, 0x15261f);
  grid.position.set(4, 0.015, 4);
  maze.add(grid);

  const wallMaterial = new THREE.MeshStandardMaterial({
    color: 0x17352c,
    roughness: 0.62,
    metalness: 0.16
  });

  SEGMENTS.forEach(([x1, z1, x2, z2]) => {
    const vertical = x1 === x2;
    const length = vertical ? Math.abs(z2 - z1) : Math.abs(x2 - x1);
    const width = vertical ? 0.055 : length;
    const depth = vertical ? length : 0.055;
    const wall = new THREE.Mesh(new THREE.BoxGeometry(width, 0.52, depth), wallMaterial);
    wall.position.set((x1 + x2) / 2, 0.26, (z1 + z2) / 2);
    maze.add(wall);
  });

  const padGeometry = new THREE.CylinderGeometry(0.24, 0.24, 0.035, 28);
  const startPad = new THREE.Mesh(
    padGeometry,
    new THREE.MeshStandardMaterial({ color: 0x34d399, roughness: 0.35, emissive: 0x0f5138, emissiveIntensity: 0.65 })
  );
  startPad.position.set(0.5, 0.018, 0.5);
  maze.add(startPad);

  const goalPad = new THREE.Mesh(
    padGeometry,
    new THREE.MeshStandardMaterial({ color: 0xf0b35a, roughness: 0.35, emissive: 0x59351a, emissiveIntensity: 0.65 })
  );
  goalPad.position.set(7.5, 0.018, 7.5);
  maze.add(goalPad);

  const trailGeometry = new THREE.BufferGeometry();
  const trailPositions = new Float32Array(pathPoints.length * 3);
  pathPoints.forEach((point, index) => {
    trailPositions[index * 3] = point.x;
    trailPositions[index * 3 + 1] = 0.06;
    trailPositions[index * 3 + 2] = point.z;
  });
  trailGeometry.setAttribute("position", new THREE.BufferAttribute(trailPositions, 3));
  const trail = new THREE.Points(
    trailGeometry,
    new THREE.PointsMaterial({ color: 0xf0b35a, size: 0.14, transparent: true, opacity: 0.86 })
  );
  trail.frustumCulled = false;
  maze.add(trail);

  const mouse = new THREE.Group();
  const bodyMaterial = new THREE.MeshStandardMaterial({ color: 0xf0b35a, roughness: 0.38, metalness: 0.12 });
  const darkMaterial = new THREE.MeshStandardMaterial({ color: 0x202b28, roughness: 0.55, metalness: 0.22 });
  const body = new THREE.Mesh(new THREE.BoxGeometry(0.46, 0.14, 0.46), bodyMaterial);
  mouse.add(body);
  const top = new THREE.Mesh(new THREE.BoxGeometry(0.24, 0.1, 0.24), darkMaterial);
  top.position.y = 0.12;
  mouse.add(top);
  const nose = new THREE.Mesh(new THREE.ConeGeometry(0.075, 0.22, 4), darkMaterial);
  nose.rotation.x = Math.PI / 2;
  nose.position.set(0, 0.08, 0.28);
  mouse.add(nose);
  const light = new THREE.Mesh(
    new THREE.SphereGeometry(0.045, 12, 12),
    new THREE.MeshStandardMaterial({ color: 0xffe2b0, emissive: 0xffd18a, emissiveIntensity: 1.4 })
  );
  light.position.set(0, 0.14, 0.2);
  mouse.add(light);
  maze.add(mouse);

  const hemisphere = new THREE.HemisphereLight(0xd8fff0, 0x04100c, 2.1);
  const key = new THREE.DirectionalLight(0xffffff, 2.8);
  key.position.set(-3, 8, 7);
  const rim = new THREE.PointLight(0x34d399, 18, 18);
  rim.position.set(5, 2.5, 6);
  scene.add(hemisphere, key, rim);

  const pointer = new THREE.Vector2();
  let scrollProgress = 0;
  let frameId = 0;

  function resize() {
    const { width, height } = canvas.getBoundingClientRect();
    if (!width || !height) return;
    renderer.setSize(width, height, false);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
  }

  function updateScroll() {
    const scrollableHeight = Math.max(document.documentElement.scrollHeight - window.innerHeight, 1);
    scrollProgress = clamp(window.scrollY / scrollableHeight, 0, 1);
  }

  function cameraPose(progress, compact) {
    const stops = compact
      ? [
          { at: 0, x: 4.0, y: 13.5, z: 10.0, lookY: 0.0 },
          { at: 0.25, x: 8.0, y: 9.0, z: 8.2, lookY: 0.15 },
          { at: 0.5, x: 9.6, y: 6.0, z: 8.5, lookY: 0.35 },
          { at: 0.75, x: 7.6, y: 4.0, z: 10.4, lookY: 0.42 },
          { at: 1, x: 4.0, y: 3.0, z: 11.5, lookY: 0.42 }
        ]
      : [
          { at: 0, x: 4.0, y: 12.5, z: 11.0, lookY: 0.0 },
          { at: 0.25, x: 9.2, y: 8.8, z: 7.8, lookY: 0.12 },
          { at: 0.5, x: 11.4, y: 5.6, z: 8.2, lookY: 0.35 },
          { at: 0.75, x: 8.6, y: 3.3, z: 11.4, lookY: 0.42 },
          { at: 1, x: 4.0, y: 2.2, z: 12.5, lookY: 0.42 }
        ];
    const end = stops.findIndex((stop) => stop.at >= progress);
    if (end <= 0) return stops[0];
    const start = stops[end - 1];
    const finish = stops[end];
    const local = smoothstep((progress - start.at) / (finish.at - start.at));
    return {
      x: mix(start.x, finish.x, local),
      y: mix(start.y, finish.y, local),
      z: mix(start.z, finish.z, local),
      lookY: mix(start.lookY, finish.lookY, local)
    };
  }

  function mouseState(progress) {
    const position = clamp(progress, 0, 1) * (pathPoints.length - 1);
    const index = Math.min(Math.floor(position), pathPoints.length - 2);
    const local = position - index;
    const current = pathPoints[index];
    const next = pathPoints[index + 1];
    const point = new THREE.Vector3(
      mix(current.x, next.x, local),
      mix(current.y, next.y, local),
      mix(current.z, next.z, local)
    );
    const heading = Math.atan2(next.x - current.x, next.z - current.z);
    return { point, heading };
  }

  function render(time) {
    const compact = window.innerWidth <= 700;
    const pose = cameraPose(scrollProgress, compact);
    const mouseProgress = smoothstep((scrollProgress - 0.03) / 0.86);
    const state = mouseState(mouseProgress);
    const idle = time * 0.00045;

    camera.position.x += (pose.x + pointer.x * (compact ? 0.12 : 0.28) - camera.position.x) * 0.055;
    camera.position.y += (pose.y - camera.position.y) * 0.055;
    camera.position.z += (pose.z + pointer.y * (compact ? 0.06 : 0.16) - camera.position.z) * 0.055;
    camera.lookAt(4, pose.lookY, 4);

    mouse.position.x += (state.point.x - mouse.position.x) * 0.14;
    mouse.position.y = 0.08 + Math.sin(idle * 2.2) * 0.02;
    mouse.position.z += (state.point.z - mouse.position.z) * 0.14;
    mouse.rotation.y += (state.heading - mouse.rotation.y) * 0.16;

    trail.geometry.setDrawRange(0, Math.max(2, Math.floor(mouseProgress * pathPoints.length + 1)));
    trail.material.opacity = mix(0.55, 0.92, mouseProgress);

    renderer.render(scene, camera);
    frameId = requestAnimationFrame(render);
  }

  window.addEventListener("resize", resize, { passive: true });
  window.addEventListener("scroll", updateScroll, { passive: true });
  window.addEventListener("pointermove", (event) => {
    pointer.set((event.clientX / window.innerWidth - 0.5) * 2, (event.clientY / window.innerHeight - 0.5) * 2);
  }, { passive: true });

  document.addEventListener("visibilitychange", () => {
    if (document.hidden) {
      cancelAnimationFrame(frameId);
    } else if (!reducedMotion) {
      frameId = requestAnimationFrame(render);
    }
  });

  resize();
  updateScroll();

  if (reducedMotion) {
    const pose = cameraPose(0.45, window.innerWidth <= 700);
    camera.position.set(pose.x, pose.y, pose.z);
    camera.lookAt(4, pose.lookY, 4);
    const state = mouseState(0.58);
    mouse.position.set(state.point.x, 0.08, state.point.z);
    mouse.rotation.y = state.heading;
    trail.geometry.setDrawRange(0, Math.floor(pathPoints.length * 0.58));
    renderer.render(scene, camera);
  } else {
    frameId = requestAnimationFrame(render);
  }
}

setupReveals();
setupMaze().catch(() => {
  document.querySelector(".maze-stage")?.classList.add("three-unavailable");
});
loadReleases();
