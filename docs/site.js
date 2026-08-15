const PATH = [
  [0, 0], [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [0, 4], [0, 5], [1, 5],
  [2, 5], [2, 6], [1, 6], [0, 6], [0, 7], [1, 7], [2, 7], [3, 7], [3, 6],
  [3, 5], [4, 5], [4, 4]
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

function createGlowTexture(color, THREE) {
  const canvas = document.createElement("canvas");
  canvas.width = 64;
  canvas.height = 64;
  const context = canvas.getContext("2d");
  const gradient = context.createRadialGradient(32, 32, 0, 32, 32, 32);
  gradient.addColorStop(0, "rgba(255, 255, 255, 1)");
  gradient.addColorStop(0.28, color);
  gradient.addColorStop(1, "rgba(0, 0, 0, 0)");
  context.fillStyle = gradient;
  context.fillRect(0, 0, 64, 64);
  return new THREE.CanvasTexture(canvas);
}

async function loadModel(url, GLTFLoader, onProgress) {
  const response = await fetch(url);
  if (!response.body) {
    return new GLTFLoader().loadAsync(url);
  }
  const total = Number(response.headers.get("content-length") || 0);
  const reader = response.body.getReader();
  const chunks = [];
  let received = 0;

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    chunks.push(value);
    received += value.length;
    if (total) onProgress(Math.min(received / total, 1));
  }

  const blob = new Blob(chunks);
  const blobUrl = URL.createObjectURL(blob);
  try {
    return await new GLTFLoader().loadAsync(blobUrl);
  } finally {
    URL.revokeObjectURL(blobUrl);
  }
}

function formatNumber(value) {
  return new Intl.NumberFormat("zh-CN").format(value);
}

const translations = {
  zh: {
    "nav.features": "核心功能",
    "nav.interface": "界面",
    "nav.protocol": "通信协议",
    "nav.downloads": "下载",
    "hero.eyebrow": "苏州大学电子信息学院 · 电子系统课程设计",
    "hero.title.1": "让迷宫，",
    "hero.title.2": "有迹可循。",
    "hero.lead": "通过串口实时接收电脑鼠的位置、朝向与传感器数据，把 8×8 迷宫中的每一次探索，变成清晰可见的轨迹与墙体。",
    "hero.download": "下载 Windows 安装包",
    "hero.see": "了解功能",
    "hero.total": "总下载次数",
    "hero.maze": "8 × 8 迷宫",
    "hero.serial": "实时串口",
    "hero.views": "2D / 3D 视图",
    "overview.heading.1": "把调试过程，",
    "overview.heading.2": "变成可见的状态。",
    "overview.p1": "MazeMouse 是苏州大学电子信息学院《电子系统设计》课程设计项目，服务于电脑鼠竞赛中最需要反馈的环节：连接、探索、回溯、优化，并在同一个界面里把数据与图形对应起来。",
    "overview.p2": "原生桌面架构确保低延迟接收，轨迹优先的界面让每一次移动、每一面墙、每一个传感器状态都即时可见。",
    "cap.serial": "串口通信",
    "cap.trail": "实时轨迹",
    "cap.walls": "墙体绘制",
    "cap.sensors": "传感器监控",
    "cap.replay": "路径回放",
    "cap.path": "最短路径",
    "cap.export": "数据导出",
    "cap.views": "2D / 3D",
    "features.sub": "四组能力，覆盖从连接到交付。",
    "features.heading": "少一点切换，多一点看见。",
    "feature1.title": "实时轨迹可视化",
    "feature1.p": "2D / 3D 双模式显示，动态轨迹与渐隐效果，实时呈现电脑鼠的位置、朝向与角度。",
    "feature2.title": "串口通信管理",
    "feature2.p": "自动检测可用串口，支持波特率、数据位、停止位与校验位配置，并实时统计通信速率。",
    "feature3.title": "传感器与墙体",
    "feature3.p": "前后左右传感器状态实时显示，并根据电脑鼠朝向自动判断、更新迷宫墙体。",
    "feature4.title": "回放与路径优化",
    "feature4.p": "自动保存运行轨迹，支持多轨迹回放对比、快照导出，以及最短路径计算与下发。",
    "protocol.heading.1": "一条数据帧，",
    "protocol.heading.2": "还原整场探索。",
    "protocol.p": "电脑鼠通过串口持续上报状态，上位机解析后同步更新轨迹、墙体与传感器面板。",
    "protocol.link": "查看仓库文档",
    "protocol.meta.xy": "X / Y — 迷宫坐标 0–7",
    "protocol.meta.o": "O — 朝向 0–3",
    "protocol.meta.sensors": "Front / Left / Right — 传感器",
    "gallery.sub": "主操作、日志、设置与轨迹记录。",
    "gallery.heading": "界面，服务于调试。",
    "shot.main": "主操作页 · 串口、传感器与迷宫轨迹",
    "shot.log": "实时日志 · 数据收发与过滤",
    "shot.settings": "设置页 · 主题、串口与启动项",
    "shot.replay": "轨迹记录 · 回放、对比与导出",
    "carousel.prev": "上一张",
    "carousel.next": "下一张",
    "releases.sub": "自动同步 GitHub Releases。",
    "releases.heading": "选择适合你的版本。",
    "releases.total": "总下载次数",
    "release.expand": "展开全部版本",
    "release.collapse": "收起版本",
    "closing.heading.1": "连接你的电脑鼠，",
    "closing.heading.2": "让迷宫开口说话。",
    "closing.download": "下载 Windows 安装包",
    "footer.copyright": "© 2025 石殷睿 · 苏州大学电子信息学院",
    "loader.loading": "正在加载小车模型…",
    "release.latest": "Latest",
    "release.prerelease": "预发布",
    "release.windows": "Windows 安装包",
    "release.view": "查看 Release",
    "release.file": "文件",
    "release.downloads": "次下载",
    "release.copy": "复制链接",
    "release.copied": "已复制",
    "release.notes": "查看更新说明",
    "release.notes.close": "收起更新说明",
    "release.empty": "版本信息暂时无法加载，",
    "release.link": "前往 GitHub Releases ↗"
  },
  en: {
    "nav.features": "Features",
    "nav.interface": "Interface",
    "nav.protocol": "Protocol",
    "nav.downloads": "Downloads",
    "hero.eyebrow": "Soochow University · EIE Course Project",
    "hero.title.1": "Make every maze",
    "hero.title.2": "traceable.",
    "hero.lead": "Receive the micromouse's position, heading and sensor data over serial, and turn every run in the 8×8 maze into visible paths and walls.",
    "hero.download": "Download Windows installer",
    "hero.see": "See features",
    "hero.total": "Total downloads",
    "hero.maze": "8 × 8 maze",
    "hero.serial": "Live serial",
    "hero.views": "2D / 3D views",
    "overview.heading.1": "Make debugging",
    "overview.heading.2": "visible state.",
    "overview.p1": "MazeMouse is a course project from the School of Electronic Information Engineering at Soochow University. It focuses on the most feedback-heavy parts of a micromouse run: connect, explore, backtrack, optimize — and maps data to graphics in one workspace.",
    "overview.p2": "A native desktop architecture keeps latency low, while a preview-first interface makes every move, wall and sensor state instantly visible.",
    "cap.serial": "Serial",
    "cap.trail": "Live trail",
    "cap.walls": "Wall drawing",
    "cap.sensors": "Sensors",
    "cap.replay": "Replay",
    "cap.path": "Shortest path",
    "cap.export": "Export",
    "cap.views": "2D / 3D",
    "features.sub": "Four capabilities, from connection to delivery.",
    "features.heading": "Less switching, more seeing.",
    "feature1.title": "Live path visualization",
    "feature1.p": "2D / 3D modes, dynamic fading trails, and real-time position, heading and angle.",
    "feature2.title": "Serial management",
    "feature2.p": "Auto-detect ports, configure baud, data, stop and parity bits, and track throughput in real time.",
    "feature3.title": "Sensors and walls",
    "feature3.p": "Show front, left and right sensor states, and update maze walls based on the mouse heading.",
    "feature4.title": "Replay and optimization",
    "feature4.p": "Auto-save runs, compare replays, export snapshots, and compute or send the shortest path.",
    "protocol.heading.1": "One frame,",
    "protocol.heading.2": "the whole run.",
    "protocol.p": "The micromouse reports its state over serial; the host parses it and updates the trail, walls and sensor panel together.",
    "protocol.link": "View repository docs",
    "protocol.meta.xy": "X / Y — maze coordinates 0–7",
    "protocol.meta.o": "O — heading 0–3",
    "protocol.meta.sensors": "Front / Left / Right — sensors",
    "gallery.sub": "Main, log, settings and replay.",
    "gallery.heading": "An interface built for debugging.",
    "shot.main": "Main page · serial, sensors and maze trail",
    "shot.log": "Live log · data traffic and filtering",
    "shot.settings": "Settings · theme, serial and startup",
    "shot.replay": "Replay · compare and export paths",
    "carousel.prev": "Previous",
    "carousel.next": "Next",
    "releases.sub": "Synced with GitHub Releases.",
    "releases.heading": "Choose your version.",
    "releases.total": "Total downloads",
    "release.expand": "Show all versions",
    "release.collapse": "Collapse versions",
    "closing.heading.1": "Connect your mouse,",
    "closing.heading.2": "and let the maze speak.",
    "closing.download": "Download Windows installer",
    "footer.copyright": "© 2025 Shi Yinrui · School of Electronic Information Engineering, Soochow University",
    "loader.loading": "Loading vehicle model…",
    "release.latest": "Latest",
    "release.prerelease": "Pre-release",
    "release.windows": "Windows installer",
    "release.view": "View release",
    "release.file": "File",
    "release.downloads": "downloads",
    "release.copy": "Copy link",
    "release.copied": "Copied",
    "release.notes": "View release notes",
    "release.notes.close": "Hide release notes",
    "release.empty": "Version info is unavailable. ",
    "release.link": "View GitHub Releases ↗"
  }
};

let currentLang = "zh";

function translate(key) {
  return (translations[currentLang] && translations[currentLang][key]) || translations.zh[key] || key;
}

function releaseNotesText(markdown) {
  return String(markdown || "")
    .replace(/```[\s\S]*?```/g, "")
    .replace(/`([^`]+)`/g, "$1")
    .replace(/!\[[^\]]*\]\([^)]*\)/g, "")
    .replace(/\[([^\]]+)\]\([^)]*\)/g, "$1")
    .replace(/^#{1,6}\s+/gm, "")
    .replace(/^\s*[-*+]\s+/gm, "• ")
    .replace(/^\s*\d+\.\s+/gm, "")
    .replace(/\*\*([^*]+)\*\*/g, "$1")
    .replace(/__([^_]+)__/g, "$1")
    .replace(/\r/g, "")
    .trim();
}

function applyLanguage() {
  document.documentElement.lang = currentLang === "zh" ? "zh-CN" : "en";
  document.title = currentLang === "zh"
    ? "MazeMouse · 电脑鼠迷宫上位机"
    : "MazeMouse · Micromouse Maze Host";
  const description = document.querySelector('meta[name="description"]');
  if (description) {
    description.content = currentLang === "zh"
      ? "面向 Micromouse 电脑鼠竞赛的迷宫可视化与控制系统，支持串口通信、实时轨迹、墙体绘制、传感器监控与路径回放。"
      : "A maze visualization and control host for Micromouse competitions, with serial communication, live trails, wall drawing, sensor monitoring and path replay.";
  }

  document.querySelectorAll("[data-i18n]").forEach((element) => {
    element.textContent = translate(element.dataset.i18n);
  });
  document.querySelectorAll("[data-i18n-aria]").forEach((element) => {
    element.setAttribute("aria-label", translate(element.dataset.i18nAria));
  });

  const toggle = document.querySelector("#lang-toggle");
  if (toggle) toggle.textContent = currentLang === "zh" ? "EN" : "中文";

  const releaseToggle = document.querySelector("#release-toggle");
  if (releaseToggle) {
    releaseToggle.textContent = translate(releaseToggle.dataset.expanded === "true" ? "release.collapse" : "release.expand");
  }

  setupHeroType();
}

function setupLanguage() {
  const saved = localStorage.getItem("maze-language");
  currentLang = saved === "en" || saved === "zh" ? saved : "zh";
  applyLanguage();
  document.querySelector("#lang-toggle")?.addEventListener("click", () => {
    currentLang = currentLang === "zh" ? "en" : "zh";
    localStorage.setItem("maze-language", currentLang);
    applyLanguage();
  });
}

let audioContext = null;
let motorGain = null;
let motorOscillator = null;
let audioAnalyser = null;
let frequencyData = null;
let soundEnabled = true;

function setMotorLevel(level) {
  if (!motorGain || !audioContext) return;
  if (!soundEnabled) level = 0;
  motorGain.gain.setTargetAtTime(level, audioContext.currentTime, 0.08);
}

function ensureAudio() {
  const AudioContextClass = window.AudioContext || window.webkitAudioContext;
  if (!AudioContextClass) return;
  if (!audioContext) {
    audioContext = new AudioContextClass();
    motorGain = audioContext.createGain();
    motorGain.gain.value = 0;
    const filter = audioContext.createBiquadFilter();
    filter.type = "lowpass";
    filter.frequency.value = 180;
    motorOscillator = audioContext.createOscillator();
    motorOscillator.type = "triangle";
    motorOscillator.frequency.value = 58;
    audioAnalyser = audioContext.createAnalyser();
    audioAnalyser.fftSize = 32;
    frequencyData = new Uint8Array(audioAnalyser.frequencyBinCount);
    motorOscillator.connect(filter);
    filter.connect(motorGain);
    motorGain.connect(audioAnalyser);
    audioAnalyser.connect(audioContext.destination);
    motorOscillator.start();
  }
  if (audioContext.state === "suspended") audioContext.resume();
}

function setupSound() {
  const button = document.querySelector("#sound-toggle");
  if (!button) return;

  const updateIcon = () => {
    button.classList.toggle("is-muted", !soundEnabled);
    button.setAttribute("aria-pressed", String(soundEnabled));
    button.setAttribute("aria-label", soundEnabled ? "关闭电机音效" : "开启电机音效");
  };

  const bars = Array.from(button.querySelectorAll(".wave-bars i"));
  const updateSpectrum = () => {
    if (!soundEnabled || !audioAnalyser) {
      bars.forEach((bar) => { bar.style.transform = "scaleY(0.15)"; });
    } else {
      audioAnalyser.getByteFrequencyData(frequencyData);
      bars.forEach((bar, index) => {
        const value = frequencyData[Math.min(index, frequencyData.length - 1)] / 255;
        bar.style.transform = `scaleY(${(0.2 + value * 0.8).toFixed(2)})`;
      });
    }
    requestAnimationFrame(updateSpectrum);
  };
  updateSpectrum();

  button.addEventListener("click", () => {
    ensureAudio();
    soundEnabled = !soundEnabled;
    updateIcon();
    setMotorLevel(0);
  });

  document.addEventListener("pointerdown", () => {
    ensureAudio();
  }, { once: true });

  let lastScrollY = window.scrollY;
  let scrollTimer = 0;
  window.addEventListener("scroll", () => {
    ensureAudio();
    const speed = Math.min(Math.abs(window.scrollY - lastScrollY), 90);
    lastScrollY = window.scrollY;
    setMotorLevel(Math.min(0.16, 0.02 + speed * 0.004));
    if (motorOscillator && audioContext) {
      motorOscillator.frequency.setTargetAtTime(58 + speed * 0.18, audioContext.currentTime, 0.08);
    }
    clearTimeout(scrollTimer);
    scrollTimer = window.setTimeout(() => setMotorLevel(0), 120);
  }, { passive: true });

  updateIcon();
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

    fetch(`https://api.github.com/repos/${repository}`, {
      headers: { Accept: "application/vnd.github+json" },
    }).then((res) => res.json()).then((repo) => {
      document.querySelectorAll("[data-star-count]").forEach((node) => {
        node.textContent = formatNumber(repo.stargazers_count || 0);
      });
      document.querySelectorAll("[data-watch-count]").forEach((node) => {
        node.textContent = formatNumber(repo.subscribers_count || 0);
      });
    }).catch(() => {});

    const installerRelease = releases.find((release) => (release.assets || []).some(
      (asset) => asset.name.toLowerCase().endsWith(".exe")
    ));
    if (installerRelease) {
      const installer = installerRelease.assets.find((asset) => asset.name.toLowerCase().endsWith(".exe"));
      document.querySelectorAll("[data-download-link]").forEach((link) => {
        link.href = installer.browser_download_url;
      });
    }

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
        ? (asset.name.toLowerCase().endsWith(".exe") ? translate("release.windows") : asset.name)
        : translate("release.view");

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
        badge.textContent = translate("release.prerelease");
        titleRow.appendChild(badge);
      }

      if (release === installerRelease) {
        const latest = document.createElement("span");
        latest.className = "badge latest";
        latest.textContent = translate("release.latest");
        titleRow.appendChild(latest);
      }

      const meta = document.createElement("div");
      meta.className = "release-meta";
      const dateSpan = document.createElement("span");
      dateSpan.textContent = date;
      const sizeSpan = document.createElement("span");
      sizeSpan.textContent = asset && asset.size ? `${(asset.size / 1048576).toFixed(1)} MB` : translate("release.file");
      const countSpan = document.createElement("span");
      countSpan.textContent = `${asset ? (asset.download_count || 0) : 0} ${translate("release.downloads")}`;
      meta.append(dateSpan, sizeSpan, countSpan);

      main.append(titleRow, meta);
      item.appendChild(main);

      const actions = document.createElement("div");
      actions.className = "release-actions";

      const download = document.createElement("a");
      download.className = "release-download";
      download.href = downloadUrl;
      download.setAttribute("target", "_blank");
      download.setAttribute("rel", "noreferrer");
      download.textContent = assetName;
      actions.appendChild(download);

      const copy = document.createElement("button");
      copy.className = "release-copy";
      copy.type = "button";
      copy.textContent = translate("release.copy");
      copy.addEventListener("click", async () => {
        try {
          await navigator.clipboard.writeText(downloadUrl);
          copy.textContent = translate("release.copied");
          window.setTimeout(() => { copy.textContent = translate("release.copy"); }, 1600);
        } catch {
          copy.textContent = downloadUrl;
        }
      });
      actions.appendChild(copy);
      item.appendChild(actions);

      if (release.body) {
        const notes = document.createElement("div");
        notes.className = "release-notes";
        notes.textContent = releaseNotesText(release.body);

        const notesToggle = document.createElement("button");
        notesToggle.className = "release-notes-toggle";
        notesToggle.type = "button";
        notesToggle.textContent = translate("release.notes");
        notesToggle.addEventListener("click", () => {
          const open = notes.classList.toggle("is-open");
          notesToggle.textContent = translate(open ? "release.notes.close" : "release.notes");
        });

        item.appendChild(notesToggle);
        item.appendChild(notes);
      }

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
        toggle.dataset.expanded = expanded ? "true" : "false";
        toggle.textContent = translate(expanded ? "release.collapse" : "release.expand");
      });
    } else {
      toggle.hidden = true;
    }
  } catch (error) {
    setCount("—");
    if (list) {
      list.innerHTML = `<p class="release-empty">${translate("release.empty")}<a href="https://github.com/Quartzsyr/MazeMouse/releases" target="_blank" rel="noreferrer">${translate("release.link")}</a></p>`;
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

function setupParallax() {
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  const items = document.querySelectorAll("[data-parallax]");
  if (!items.length) return;

  let ticking = false;
  const update = () => {
    const viewportHeight = window.innerHeight;
    items.forEach((element) => {
      const rect = element.getBoundingClientRect();
      const center = rect.top + rect.height / 2 - viewportHeight / 2;
      const speed = parseFloat(element.dataset.parallax || "0.08");
      const offset = center * speed * -1;
      element.style.transform = `translate3d(0, ${offset.toFixed(1)}px, 0)`;
    });
    ticking = false;
  };

  const requestUpdate = () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(update);
  };

  window.addEventListener("scroll", requestUpdate, { passive: true });
  window.addEventListener("resize", requestUpdate, { passive: true });
  update();
}

function setupCarousel() {
  const track = document.querySelector("#carousel-track");
  const dots = Array.from(document.querySelectorAll(".carousel-dot"));
  const marker = document.querySelector("#car-marker");
  const previous = document.querySelector("#carousel-prev");
  const next = document.querySelector("#carousel-next");
  const viewport = document.querySelector("#carousel-viewport");

  if (!track || !dots.length) return;

  let index = 0;
  const count = dots.length;

  const update = () => {
    track.style.transform = `translateX(-${index * 100}%)`;
    dots.forEach((dot, dotIndex) => {
      dot.classList.toggle("is-active", dotIndex === index);
    });
    const activeDot = dots[index];
    if (marker && activeDot) {
      marker.style.left = `${activeDot.offsetLeft + activeDot.offsetWidth / 2}px`;
    }
  };

  const go = (nextIndex) => {
    index = (nextIndex + count) % count;
    update();
  };

  if (previous) previous.addEventListener("click", () => go(index - 1));
  if (next) next.addEventListener("click", () => go(index + 1));
  dots.forEach((dot) => {
    dot.addEventListener("click", () => go(Number(dot.dataset.index || 0)));
  });

  let startX = 0;
  if (viewport) {
    viewport.addEventListener("touchstart", (event) => {
      startX = event.touches[0].clientX;
    }, { passive: true });
    viewport.addEventListener("touchend", (event) => {
      const deltaX = event.changedTouches[0].clientX - startX;
      if (Math.abs(deltaX) > 40) go(index + (deltaX < 0 ? 1 : -1));
    }, { passive: true });
  }

  update();
}

function setupTilt() {
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  const items = document.querySelectorAll("[data-tilt]");
  items.forEach((item) => {
    item.addEventListener("pointermove", (event) => {
      const rect = item.getBoundingClientRect();
      const x = (event.clientX - rect.left) / rect.width - 0.5;
      const y = (event.clientY - rect.top) / rect.height - 0.5;
      item.style.transform = `perspective(900px) rotateX(${(-y * 6).toFixed(2)}deg) rotateY(${(x * 6).toFixed(2)}deg) translateY(-4px)`;
    });
    item.addEventListener("pointerleave", () => {
      item.style.transform = "";
    });
  });
}

function setupHeroType() {
  const title = document.querySelector("#hero-title");
  if (!title) return;
  title.querySelectorAll(".title-line").forEach((line) => {
    const text = line.textContent;
    line.textContent = "";
    [...text].forEach((character, index) => {
      const span = document.createElement("span");
      span.className = "char";
      span.style.setProperty("--i", index);
      span.textContent = character === " " ? "\u00A0" : character;
      line.appendChild(span);
    });
  });
}

async function setupMaze() {
  const canvas = document.querySelector("#maze-canvas");
  if (!canvas) return;

  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const THREE = await import("three");
  const { GLTFLoader } = await import("three/addons/loaders/GLTFLoader.js");
  const { EffectComposer } = await import("three/addons/postprocessing/EffectComposer.js");
  const { RenderPass } = await import("three/addons/postprocessing/RenderPass.js");
  const { UnrealBloomPass } = await import("three/addons/postprocessing/UnrealBloomPass.js");
  const { OutputPass } = await import("three/addons/postprocessing/OutputPass.js");

  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.08;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(32, 1, 0.1, 100);

  const composer = new EffectComposer(renderer);
  composer.addPass(new RenderPass(scene, camera));
  const bloomPass = new UnrealBloomPass(new THREE.Vector2(1, 1), 0.34, 0.65, 0.5);
  composer.addPass(bloomPass);
  composer.addPass(new OutputPass());

  const maze = new THREE.Group();
  scene.add(maze);

  const worldPoint = ([row, col]) => new THREE.Vector3(col + 0.5, 0, row + 0.5);
  const pathPoints = PATH.map(worldPoint);

  const wallSet = new Set();
  SEGMENTS.forEach(([x1, z1, x2, z2]) => {
    wallSet.add(`${x1},${z1},${x2},${z2}`);
    wallSet.add(`${x2},${z2},${x1},${z1}`);
  });
  const hasWall = (row, col, direction) => {
    const [a, b, c, d] = direction === 0
      ? [col, row, col + 1, row]
      : direction === 1
        ? [col + 1, row, col + 1, row + 1]
        : direction === 2
          ? [col, row + 1, col + 1, row + 1]
          : [col, row, col, row + 1];
    return wallSet.has(`${a},${b},${c},${d}`);
  };

  const floor = new THREE.Mesh(
    new THREE.BoxGeometry(8, 0.08, 8),
    new THREE.MeshStandardMaterial({ color: 0x101f1a, roughness: 0.5, metalness: 0.18 })
  );
  floor.position.set(4, -0.05, 4);
  floor.receiveShadow = true;
  maze.add(floor);

  const grid = new THREE.GridHelper(8, 8, 0x2c4a40, 0x15261f);
  grid.position.set(4, 0.015, 4);
  maze.add(grid);

  const wallMaterial = new THREE.MeshStandardMaterial({
    color: 0x1b3a30,
    roughness: 0.55,
    metalness: 0.24,
    emissive: 0x06110d,
    emissiveIntensity: 0.25
  });
  const wallTopMaterial = new THREE.MeshStandardMaterial({
    color: 0x2f6a58,
    roughness: 0.45,
    metalness: 0.2,
    emissive: 0x173b2e,
    emissiveIntensity: 0.7
  });

  const wallMeshes = [];
  const wallTopMeshes = [];

  SEGMENTS.forEach(([x1, z1, x2, z2]) => {
    const vertical = x1 === x2;
    const length = vertical ? Math.abs(z2 - z1) : Math.abs(x2 - x1);
    const width = vertical ? 0.055 : length;
    const depth = vertical ? length : 0.055;
    const wall = new THREE.Mesh(new THREE.BoxGeometry(width, 0.52, depth), wallMaterial);
    wall.position.set((x1 + x2) / 2, 0.26, (z1 + z2) / 2);
    wall.userData.dist = Math.hypot((x1 + x2) / 2 - 0.5, (z1 + z2) / 2 - 0.5);
    wall.castShadow = true;
    wall.receiveShadow = true;
    maze.add(wall);
    wallMeshes.push(wall);

    const topWidth = vertical ? 0.075 : length;
    const topDepth = vertical ? length : 0.075;
    const topStrip = new THREE.Mesh(new THREE.BoxGeometry(topWidth, 0.015, topDepth), wallTopMaterial);
    topStrip.position.set((x1 + x2) / 2, 0.5275, (z1 + z2) / 2);
    topStrip.userData.dist = wall.userData.dist;
    topStrip.castShadow = true;
    topStrip.receiveShadow = true;
    maze.add(topStrip);
    wallTopMeshes.push(topStrip);
  });

  const rippleMaterialFactory = (color) => new THREE.ShaderMaterial({
    transparent: true,
    depthWrite: false,
    side: THREE.DoubleSide,
    uniforms: {
      uColor: { value: new THREE.Color(color) },
      uOpacity: { value: 0 },
      uTime: { value: 0 }
    },
    vertexShader: `
      uniform float uTime;
      void main() {
        vec3 pos = position;
        float angle = atan(pos.y, pos.x);
        float radius = length(pos.xy);
        float wobble = sin(angle * 8.0 + uTime * 3.0) * 0.012;
        pos.xy *= 1.0 + wobble / max(radius, 0.0001);
        gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
      }
    `,
    fragmentShader: `
      uniform vec3 uColor;
      uniform float uOpacity;
      void main() {
        gl_FragColor = vec4(uColor, uOpacity);
      }
    `
  });

  const createRipple = (color, x, z) => {
    const group = new THREE.Group();
    group.position.set(x, 0.032, z);
    const rings = [0, 1].map((index) => {
      const ring = new THREE.Mesh(
        new THREE.RingGeometry(0.88, 1.0, 64),
        rippleMaterialFactory(color)
      );
      ring.rotation.x = -Math.PI / 2;
      ring.userData.offset = index / 2;
      group.add(ring);
      return ring;
    });
    maze.add(group);
    return rings;
  };

  const startRipples = createRipple(0x34d399, 0.5, 0.5);
  const goalRipples = createRipple(0xf0b35a, 4.5, 4.5);

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
    new THREE.PointsMaterial({
      color: 0xf0b35a,
      size: 0.24,
      map: createGlowTexture("#f0b35a", THREE),
      transparent: true,
      opacity: 0.9,
      depthWrite: false,
      blending: THREE.AdditiveBlending
    })
  );
  trail.frustumCulled = false;
  maze.add(trail);

  const trailLine = new THREE.Line(
    trailGeometry,
    new THREE.LineBasicMaterial({ color: 0xf0b35a, transparent: true, opacity: 0.34 })
  );
  trailLine.frustumCulled = false;
  maze.add(trailLine);

  const mouse = new THREE.Group();
  const carRig = new THREE.Group();
  mouse.add(carRig);
  const loaderElement = document.querySelector("#scene-loader");
  const loaderText = loaderElement?.querySelector(".loader-text");
  const loaderBar = loaderElement?.querySelector(".loader-bar i");
  const updateLoadProgress = (fraction) => {
    const percent = Math.round(fraction * 100);
    if (loaderText) loaderText.textContent = `${translate("loader.loading")} ${percent}%`;
    if (loaderBar) loaderBar.style.width = `${percent}%`;
  };
  const gltf = await loadModel("./assets/model.glb", GLTFLoader, updateLoadProgress);
  const model = gltf.scene || gltf.scenes[0];
  const box = new THREE.Box3().setFromObject(model);
  const size = box.getSize(new THREE.Vector3());
  const center = box.getCenter(new THREE.Vector3());
  const targetSize = 0.72;
  const scale = targetSize / Math.max(size.x, size.y, size.z);
  model.scale.setScalar(scale);
  model.rotation.y = -Math.PI / 2;
  model.position.set(
    -center.x * scale,
    -center.y * scale + size.y * scale / 2,
    -center.z * scale
  );
  carRig.add(model);
  model.traverse((node) => {
    if (node.isMesh) {
      node.castShadow = true;
      node.receiveShadow = true;
    }
  });

  const carAccessories = new THREE.Group();
  const headlightMaterial = new THREE.MeshStandardMaterial({
    color: 0xfff3c4,
    emissive: 0xffe6a0,
    emissiveIntensity: 2.6
  });
  const taillightMaterial = new THREE.MeshStandardMaterial({
    color: 0xff4d4d,
    emissive: 0xff2222,
    emissiveIntensity: 2.6
  });

  const headlightSphere = (x, z) => {
    const sphere = new THREE.Mesh(new THREE.SphereGeometry(0.032, 12, 12), headlightMaterial);
    sphere.position.set(x, 0.08, z);
    sphere.visible = false;
    carAccessories.add(sphere);
  };
  headlightSphere(-0.13, 0.38);
  headlightSphere(0.13, 0.38);

  const taillightSphere = (x, z) => {
    const sphere = new THREE.Mesh(new THREE.SphereGeometry(0.03, 12, 12), taillightMaterial);
    sphere.position.set(x, 0.08, z);
    sphere.visible = false;
    carAccessories.add(sphere);
  };
  taillightSphere(-0.13, -0.38);
  taillightSphere(0.13, -0.38);

  const frontLight = new THREE.PointLight(0xffe9b8, 2.4, 1.8, 2);
  frontLight.position.set(0, 0.16, 0.75);
  carAccessories.add(frontLight);

  const rearLight = new THREE.PointLight(0xff3030, 1.0, 1.0, 2);
  rearLight.position.set(0, 0.12, -0.58);
  carAccessories.add(rearLight);

  const sensorMaterials = {
    front: new THREE.LineBasicMaterial({ color: 0x34d399, transparent: true, opacity: 0.7 }),
    left: new THREE.LineBasicMaterial({ color: 0x34d399, transparent: true, opacity: 0.7 }),
    right: new THREE.LineBasicMaterial({ color: 0x34d399, transparent: true, opacity: 0.7 })
  };
  const frontLine = new THREE.Line(new THREE.BufferGeometry().setFromPoints([
    new THREE.Vector3(0, 0.035, 0.44), new THREE.Vector3(0, 0.035, 0.78)
  ]), sensorMaterials.front);
  const leftLine = new THREE.Line(new THREE.BufferGeometry().setFromPoints([
    new THREE.Vector3(-0.28, 0.035, 0.16), new THREE.Vector3(-0.74, 0.035, 0.16)
  ]), sensorMaterials.left);
  const rightLine = new THREE.Line(new THREE.BufferGeometry().setFromPoints([
    new THREE.Vector3(0.28, 0.035, 0.16), new THREE.Vector3(0.74, 0.035, 0.16)
  ]), sensorMaterials.right);
  carAccessories.add(frontLine, leftLine, rightLine);

  carRig.add(carAccessories);
  maze.add(mouse);
  document.querySelector("#scene-loader")?.classList.add("is-hidden");

  const hemisphere = new THREE.HemisphereLight(0xd8fff0, 0x04100c, 2.1);
  const key = new THREE.DirectionalLight(0xffffff, 2.8);
  key.position.set(-4, 9, 7);
  key.castShadow = true;
  key.shadow.mapSize.set(1024, 1024);
  key.shadow.camera.near = 0.5;
  key.shadow.camera.far = 30;
  key.shadow.camera.left = -12;
  key.shadow.camera.right = 12;
  key.shadow.camera.top = 12;
  key.shadow.camera.bottom = -12;
  key.shadow.bias = -0.0002;
  const rim = new THREE.PointLight(0x34d399, 18, 18);
  rim.position.set(5, 2.5, 6);
  const fill = new THREE.AmbientLight(0x2c4139, 0.8);
  scene.add(hemisphere, key, rim, fill);

  const pointer = new THREE.Vector2();
  let scrollProgress = 0;
  let frameId = 0;

  function resize() {
    const { width, height } = canvas.getBoundingClientRect();
    if (!width || !height) return;
    renderer.setSize(width, height, false);
    composer.setSize(width, height);
    bloomPass.resolution.set(width, height);
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
    const row = Math.round(current.z - 0.5);
    const col = Math.round(current.x - 0.5);
    const dx = next.x - current.x;
    const dz = next.z - current.z;
    const cardinal = dx > 0 ? 1 : dx < 0 ? 3 : dz > 0 ? 2 : 0;
    return { point, heading, row, col, cardinal };
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
    mouse.position.y = 0.02 + Math.sin(idle * 2.2) * 0.012;
    mouse.position.z += (state.point.z - mouse.position.z) * 0.14;
    const angleDiff = Math.atan2(Math.sin(state.heading - mouse.rotation.y), Math.cos(state.heading - mouse.rotation.y));
    mouse.rotation.y += (state.heading - mouse.rotation.y) * 0.16;
    const targetRoll = Math.max(-0.12, Math.min(0.12, -angleDiff * 0.35));
    carRig.rotation.z += (targetRoll - carRig.rotation.z) * 0.08;

    const leftDirection = (state.cardinal + 3) % 4;
    const rightDirection = (state.cardinal + 1) % 4;
    const frontBlocked = hasWall(state.row, state.col, state.cardinal);
    const leftBlocked = hasWall(state.row, state.col, leftDirection);
    const rightBlocked = hasWall(state.row, state.col, rightDirection);
    sensorMaterials.front.color.set(frontBlocked ? 0xff4d4d : 0x34d399);
    sensorMaterials.left.color.set(leftBlocked ? 0xff4d4d : 0x34d399);
    sensorMaterials.right.color.set(rightBlocked ? 0xff4d4d : 0x34d399);

    wallMeshes.forEach((wall) => {
      const rise = smoothstep((scrollProgress - 0.02 - wall.userData.dist * 0.035) / 0.16);
      wall.scale.y = Math.max(0.001, rise);
      wall.position.y = 0.26 * rise;
    });
    wallTopMeshes.forEach((strip) => {
      const rise = smoothstep((scrollProgress - 0.02 - strip.userData.dist * 0.035) / 0.16);
      strip.scale.y = Math.max(0.001, rise);
      strip.position.y = 0.5275 * rise;
    });

    trail.geometry.setDrawRange(0, Math.max(2, Math.floor(mouseProgress * pathPoints.length + 1)));
    trail.material.opacity = mix(0.55, 0.92, mouseProgress);

    const rippleTime = time * 0.001;
    [startRipples, goalRipples].forEach((ripples) => {
      ripples.forEach((ring) => {
        const duration = 3.6;
        const progress = ((rippleTime / duration) + ring.userData.offset) % 1;
        ring.scale.setScalar(0.16 + progress * 0.72);
        ring.material.uniforms.uOpacity.value = (1 - progress) * 0.26;
        ring.material.uniforms.uTime.value = rippleTime;
      });
    });

    composer.render();
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
    mouse.position.set(state.point.x, 0.02, state.point.z);
    mouse.rotation.y = state.heading;
    carRig.rotation.z = 0;
    const leftDirection = (state.cardinal + 3) % 4;
    const rightDirection = (state.cardinal + 1) % 4;
    sensorMaterials.front.color.set(hasWall(state.row, state.col, state.cardinal) ? 0xff4d4d : 0x34d399);
    sensorMaterials.left.color.set(hasWall(state.row, state.col, leftDirection) ? 0xff4d4d : 0x34d399);
    sensorMaterials.right.color.set(hasWall(state.row, state.col, rightDirection) ? 0xff4d4d : 0x34d399);
    trail.geometry.setDrawRange(0, Math.floor(pathPoints.length * 0.58));
    wallMeshes.forEach((wall) => {
      wall.scale.y = 1;
      wall.position.y = 0.26;
    });
    wallTopMeshes.forEach((strip) => {
      strip.scale.y = 1;
      strip.position.y = 0.5275;
    });
    [startRipples, goalRipples].forEach((ripples) => {
      ripples.forEach((ring, index) => {
        ring.scale.setScalar(0.16 + (index / 2) * 0.72);
        ring.material.uniforms.uOpacity.value = (1 - index / 2) * 0.26;
        ring.material.uniforms.uTime.value = 0;
      });
    });
    composer.render();
  } else {
    frameId = requestAnimationFrame(render);
  }
}

setupReveals();
setupParallax();
setupCarousel();
setupLanguage();
setupTilt();
setupSound();
setupMaze().catch(() => {
  document.querySelector(".maze-stage")?.classList.add("three-unavailable");
  document.querySelector("#scene-loader")?.classList.add("is-hidden");
});
loadReleases();
