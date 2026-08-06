#!/usr/bin/env node

import fs from "node:fs";

const STYLE_IDS = new Set([
  "swiss-grid",
  "minimal-product-launch",
  "editorial-magazine",
  "executive-consulting",
  "cinematic-photography",
  "art-deco",
  "bauhaus-modernism",
  "memphis-playful",
  "futuristic-tech",
  "scrapbook-collage",
  "neo-brutalism",
  "warm-japanese-minimal",
]);

const PRESENTATION_MODES = new Set(["live", "reading", "hybrid"]);

const HIGH_RISK_PAIRS = new Map([
  ["memphis-playful|neo-brutalism", "两者都使用高能量、强对抗图形，容易造成视觉竞争。"],
  ["futuristic-tech|scrapbook-collage", "光洁数字空间与手工触觉材质通常缺少共同语法。"],
  ["art-deco|futuristic-tech", "历史装饰语言与未来数字语言需要明确概念桥梁。"],
  ["cinematic-photography|executive-consulting", "全屏摄影的负空间与高密度证据通常争夺页面空间。"],
]);

function usage() {
  return [
    "Usage:",
    "  node validate-style-spec.mjs <style-spec.json>",
    "  node validate-style-spec.mjs -          # read JSON from stdin",
    "  node validate-style-spec.mjs --self-test",
  ].join("\n");
}

function isPlainObject(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function isNonEmptyString(value) {
  return typeof value === "string" && value.trim().length > 0;
}

function isStringArray(value) {
  return Array.isArray(value) && value.every(isNonEmptyString);
}

function canonicalPair(first, second) {
  return [first, second].sort().join("|");
}

function parseHex(hex) {
  if (typeof hex !== "string" || !/^#[0-9a-fA-F]{6}$/.test(hex)) return null;
  return {
    r: Number.parseInt(hex.slice(1, 3), 16),
    g: Number.parseInt(hex.slice(3, 5), 16),
    b: Number.parseInt(hex.slice(5, 7), 16),
  };
}

function channelToLinear(channel) {
  const normalized = channel / 255;
  return normalized <= 0.04045
    ? normalized / 12.92
    : ((normalized + 0.055) / 1.055) ** 2.4;
}

function luminance(rgb) {
  return (
    0.2126 * channelToLinear(rgb.r) +
    0.7152 * channelToLinear(rgb.g) +
    0.0722 * channelToLinear(rgb.b)
  );
}

function contrastRatio(firstHex, secondHex) {
  const first = parseHex(firstHex);
  const second = parseHex(secondHex);
  if (!first || !second) return null;
  const firstLum = luminance(first);
  const secondLum = luminance(second);
  const lighter = Math.max(firstLum, secondLum);
  const darker = Math.min(firstLum, secondLum);
  return (lighter + 0.05) / (darker + 0.05);
}

function validateStyleSpec(spec) {
  const errors = [];
  const warnings = [];
  const notes = [];

  const error = (path, message) => errors.push({ path, message });
  const warn = (path, message) => warnings.push({ path, message });
  const note = (path, message) => notes.push({ path, message });

  if (!isPlainObject(spec)) {
    error("$", "Style Spec 必须是 JSON 对象。");
    return { errors, warnings, notes };
  }

  if (!isNonEmptyString(spec.name)) error("name", "必须提供项目内可读名称。");

  if (!PRESENTATION_MODES.has(spec.presentationMode)) {
    error("presentationMode", "必须是 live、reading 或 hybrid。");
  }

  if (!STYLE_IDS.has(spec.primaryStyle)) {
    error("primaryStyle", `未知风格 ID；可用值：${[...STYLE_IDS].join(", ")}`);
  }

  if (spec.auxiliaryStyle !== undefined && spec.auxiliaryStyle !== null && spec.auxiliaryStyle !== "") {
    if (!isNonEmptyString(spec.auxiliaryStyle)) {
      error("auxiliaryStyle", "辅助风格必须是单个字符串；不允许数组或多个辅助风格。");
    } else if (!STYLE_IDS.has(spec.auxiliaryStyle)) {
      error("auxiliaryStyle", "未知辅助风格 ID。");
    } else if (spec.auxiliaryStyle === spec.primaryStyle) {
      error("auxiliaryStyle", "辅助风格不能与主风格相同。");
    } else if (STYLE_IDS.has(spec.primaryStyle)) {
      const pairWarning = HIGH_RISK_PAIRS.get(canonicalPair(spec.primaryStyle, spec.auxiliaryStyle));
      if (pairWarning) warn("auxiliaryStyle", pairWarning);
    }
  }

  for (const field of ["intent", "antiIntent"]) {
    if (!isStringArray(spec[field]) || spec[field].length === 0) {
      error(field, "必须是至少包含一个非空字符串的数组。");
    } else if (spec[field].length < 2) {
      warn(field, "建议至少写两个词，以减少风格解释歧义。");
    }
  }

  if (!isPlainObject(spec.palette)) {
    error("palette", "必须提供色板对象。");
  } else {
    for (const field of ["background", "text", "accent"]) {
      if (!parseHex(spec.palette[field])) {
        error(`palette.${field}`, "必须使用 #RRGGBB 十六进制颜色。");
      }
    }
    for (const field of ["surface", "mutedText"]) {
      if (spec.palette[field] !== undefined && !parseHex(spec.palette[field])) {
        error(`palette.${field}`, "可选颜色必须使用 #RRGGBB 十六进制格式。");
      }
    }

    const mainContrast = contrastRatio(spec.palette.text, spec.palette.background);
    if (mainContrast !== null) {
      if (mainContrast < 4.5) {
        error("palette.text", `正文与背景对比度仅 ${mainContrast.toFixed(2)}:1，目标至少 4.5:1。`);
      } else {
        note("palette.text", `正文与背景对比度 ${mainContrast.toFixed(2)}:1。`);
      }
    }

    if (spec.palette.mutedText !== undefined) {
      const mutedContrast = contrastRatio(spec.palette.mutedText, spec.palette.background);
      if (mutedContrast !== null && mutedContrast < 4.5) {
        warn("palette.mutedText", `弱化文字与背景对比度 ${mutedContrast.toFixed(2)}:1；若承载正文，应达到 4.5:1。`);
      }
    }

    const accentContrast = contrastRatio(spec.palette.accent, spec.palette.background);
    if (accentContrast !== null && accentContrast < 3) {
      warn("palette.accent", `强调色与背景对比度 ${accentContrast.toFixed(2)}:1，不宜单独承担关键图形编码。`);
    }

    if (spec.palette.surface !== undefined) {
      const surfaceTextContrast = contrastRatio(spec.palette.text, spec.palette.surface);
      if (surfaceTextContrast !== null && surfaceTextContrast < 4.5) {
        error("palette.surface", `正文与表面色对比度仅 ${surfaceTextContrast.toFixed(2)}:1。`);
      }
    }
  }

  if (!isPlainObject(spec.typography)) {
    error("typography", "必须提供字体系统对象。");
  } else {
    for (const field of ["display", "body", "cjkFallback"]) {
      if (!isNonEmptyString(spec.typography[field])) {
        error(`typography.${field}`, "必须提供非空字体名称。");
      }
    }

    const sizeRules = [
      ["deckTitlePt", 50, "封面标题"],
      ["slideTitlePt", 35, "页面标题"],
      ["bodyPt", 16, "正文"],
    ];
    for (const [field, minimum, label] of sizeRules) {
      const value = spec.typography[field];
      if (typeof value !== "number" || !Number.isFinite(value)) {
        error(`typography.${field}`, "必须是有限数值。");
      } else if (value < minimum) {
        error(`typography.${field}`, `${label} ${value}pt 低于无模板场景的默认下限 ${minimum}pt。`);
      }
    }

    if (
      typeof spec.typography.deckTitlePt === "number" &&
      typeof spec.typography.slideTitlePt === "number" &&
      spec.typography.deckTitlePt <= spec.typography.slideTitlePt
    ) {
      warn("typography.deckTitlePt", "封面标题不大于页面标题，可能缺少尺度层级。");
    }
    if (
      typeof spec.typography.slideTitlePt === "number" &&
      typeof spec.typography.bodyPt === "number" &&
      spec.typography.slideTitlePt < spec.typography.bodyPt * 1.5
    ) {
      warn("typography.slideTitlePt", "页面标题与正文字号差异较小，需用字重或位置强化层级。");
    }
  }

  if (!isPlainObject(spec.grid)) {
    error("grid", "必须提供网格对象。");
  } else {
    const { columns, marginPct, gutterPct } = spec.grid;
    if (!Number.isInteger(columns) || columns < 1 || columns > 16) {
      error("grid.columns", "栏数必须是 1 到 16 的整数。");
    }
    if (typeof marginPct !== "number" || !Number.isFinite(marginPct) || marginPct < 2 || marginPct > 15) {
      error("grid.marginPct", "页边距百分比必须在 2 到 15 之间。");
    }
    if (typeof gutterPct !== "number" || !Number.isFinite(gutterPct) || gutterPct < 0.25 || gutterPct > 6) {
      error("grid.gutterPct", "栏间距百分比必须在 0.25 到 6 之间。");
    }
    if (
      typeof marginPct === "number" &&
      typeof gutterPct === "number" &&
      typeof columns === "number" &&
      marginPct * 2 + gutterPct * Math.max(columns - 1, 0) >= 80
    ) {
      warn("grid", "边距与栏间距占比过高，可能导致可用内容区不足。");
    }
  }

  for (const field of ["imageDirection", "chartRules", "shapeRules", "motionRules", "forbidden"]) {
    if (!isStringArray(spec[field]) || spec[field].length === 0) {
      error(field, "必须是至少包含一条规则的字符串数组。");
    }
  }

  if (isStringArray(spec.forbidden) && spec.forbidden.length < 2) {
    warn("forbidden", "建议至少写两个禁用项，以防止风格退化为模板符号。");
  }

  if (spec.presentationMode === "reading" && isPlainObject(spec.typography) && spec.typography.bodyPt > 24) {
    warn("typography.bodyPt", "阅读型演示的正文大于 24pt，可能显著降低信息承载；请确认这是有意选择。");
  }

  if (spec.presentationMode === "live" && isPlainObject(spec.grid) && spec.grid.columns > 12) {
    warn("grid.columns", "现场演讲使用超过 12 栏的网格可能鼓励过高密度。");
  }

  return { errors, warnings, notes };
}

function printResult(result) {
  for (const item of result.errors) console.error(`ERROR ${item.path}: ${item.message}`);
  for (const item of result.warnings) console.warn(`WARN  ${item.path}: ${item.message}`);
  for (const item of result.notes) console.log(`INFO  ${item.path}: ${item.message}`);
  console.log(`Summary: ${result.errors.length} error(s), ${result.warnings.length} warning(s), ${result.notes.length} note(s).`);
}

function validFixture() {
  return {
    name: "Example",
    presentationMode: "live",
    primaryStyle: "minimal-product-launch",
    auxiliaryStyle: "swiss-grid",
    intent: ["克制", "精确"],
    antiIntent: ["模板感", "卡片堆叠"],
    palette: {
      background: "#F7F7F4",
      surface: "#FFFFFF",
      text: "#111111",
      mutedText: "#555555",
      accent: "#B42318",
    },
    typography: {
      display: "Inter",
      body: "Inter",
      cjkFallback: "Noto Sans CJK SC",
      deckTitlePt: 56,
      slideTitlePt: 36,
      bodyPt: 18,
    },
    grid: { columns: 12, marginPct: 5.5, gutterPct: 1.5 },
    imageDirection: ["真实产品特写"],
    chartRules: ["直接标注"],
    shapeRules: ["无阴影"],
    motionRules: ["只表达连续关系"],
    forbidden: ["随机渐变", "无意义装饰"],
  };
}

function runSelfTest() {
  const good = validateStyleSpec(validFixture());
  if (good.errors.length !== 0) {
    printResult(good);
    throw new Error("有效样例不应产生错误。");
  }

  const bad = validFixture();
  bad.primaryStyle = "unknown-style";
  bad.auxiliaryStyle = ["swiss-grid", "art-deco"];
  bad.palette.text = "#777777";
  bad.palette.background = "#888888";
  bad.typography.bodyPt = 10;
  bad.grid.columns = 24;
  bad.forbidden = [];
  const rejected = validateStyleSpec(bad);
  if (rejected.errors.length < 6) {
    printResult(rejected);
    throw new Error("无效样例应触发多项错误。");
  }

  const risky = validFixture();
  risky.primaryStyle = "futuristic-tech";
  risky.auxiliaryStyle = "scrapbook-collage";
  const warned = validateStyleSpec(risky);
  if (!warned.warnings.some((item) => item.path === "auxiliaryStyle")) {
    printResult(warned);
    throw new Error("高风险组合应触发辅助风格警告。");
  }

  console.log("Self-test passed: valid, invalid, and high-risk fixtures behave as expected.");
}

async function readStdin() {
  const chunks = [];
  for await (const chunk of process.stdin) chunks.push(chunk);
  return Buffer.concat(chunks).toString("utf8");
}

async function main() {
  const argument = process.argv[2];
  if (!argument || argument === "--help" || argument === "-h") {
    console.log(usage());
    process.exitCode = argument ? 0 : 2;
    return;
  }
  if (argument === "--self-test") {
    runSelfTest();
    return;
  }

  let source;
  try {
    source = argument === "-" ? await readStdin() : fs.readFileSync(argument, "utf8");
  } catch (error) {
    console.error(`Unable to read Style Spec: ${error.message}`);
    process.exitCode = 2;
    return;
  }

  let spec;
  try {
    spec = JSON.parse(source);
  } catch (error) {
    console.error(`Invalid JSON: ${error.message}`);
    process.exitCode = 2;
    return;
  }

  const result = validateStyleSpec(spec);
  printResult(result);
  process.exitCode = result.errors.length === 0 ? 0 : 1;
}

await main();
