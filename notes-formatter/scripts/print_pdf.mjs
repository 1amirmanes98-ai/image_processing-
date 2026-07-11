#!/usr/bin/env node
/*
 * print_pdf.mjs — dependency-free Chrome DevTools Protocol driver (Node 22).
 * Loads a local HTML file in headless Chromium, waits for KaTeX + fonts to
 * finish (window.__RENDER_DONE__), then Page.printToPDF to A4 with an RTL
 * "עמוד X מתוך Y" footer. Node 22 ships a global WebSocket + fetch, so no npm.
 *
 * Usage: node print_pdf.mjs <input.html> <output.pdf> [--footer "text"]
 */

import { spawn } from "node:child_process";
import {
  mkdtempSync, readFileSync, writeFileSync, existsSync, rmSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { pathToFileURL } from "node:url";

const CHROME = process.env.CHROME_BIN
  || "/opt/pw-browsers/chromium-1194/chrome-linux/chrome";

// ---- args -------------------------------------------------------------------
function parseArgs(argv) {
  const a = { footer: "" };
  const rest = [];
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === "--footer") a.footer = argv[++i] ?? "";
    else rest.push(argv[i]);
  }
  a.input = rest[0];
  a.output = rest[1];
  return a;
}
const args = parseArgs(process.argv.slice(2));
if (!args.input || !args.output) {
  console.error('usage: node print_pdf.mjs <input.html> <output.pdf> [--footer "text"]');
  process.exit(2);
}
const inputUrl = pathToFileURL(resolve(args.input)).href;
const outPath = resolve(args.output);

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
function escapeHtml(s) {
  return String(s).replace(/[&<>"]/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
}

// ---- launch chromium --------------------------------------------------------
const userDataDir = mkdtempSync(join(tmpdir(), "cdp-print-"));
const chrome = spawn(CHROME, [
  "--headless=new",
  "--no-sandbox",
  "--disable-gpu",
  "--disable-dev-shm-usage",
  "--hide-scrollbars",
  "--force-color-profile=srgb",
  "--remote-debugging-port=0",   // 0 → OS picks a free port, reported in DevToolsActivePort
  `--user-data-dir=${userDataDir}`,
  "about:blank",
], { stdio: ["ignore", "ignore", "pipe"] });

let chromeErr = "";
chrome.stderr.on("data", (d) => { chromeErr += d.toString(); });

let cleaned = false;
function cleanup() {
  if (cleaned) return;
  cleaned = true;
  try { chrome.kill("SIGKILL"); } catch {}
  try { rmSync(userDataDir, { recursive: true, force: true }); } catch {}
}
process.on("exit", cleanup);
process.on("SIGINT", () => { cleanup(); process.exit(130); });

function fail(msg) {
  console.error("print_pdf: " + msg);
  cleanup();
  process.exit(1);
}

// ---- discover the browser-level WebSocket endpoint --------------------------
async function readBrowserWs() {
  const portFile = join(userDataDir, "DevToolsActivePort");
  const deadline = Date.now() + 15000;
  while (Date.now() < deadline) {
    if (existsSync(portFile)) {
      const lines = readFileSync(portFile, "utf8").trim().split("\n");
      const port = (lines[0] || "").trim();
      const path = (lines[1] || "").trim();     // e.g. /devtools/browser/<uuid>
      if (port && path) return `ws://127.0.0.1:${port}${path}`;
    }
    if (chrome.exitCode !== null) {
      throw new Error("chromium exited early (code " + chrome.exitCode + "):\n" + chromeErr);
    }
    await sleep(100);
  }
  throw new Error("timed out waiting for DevToolsActivePort");
}

// ---- minimal CDP client over a single (flattened) WebSocket -----------------
class CDP {
  constructor(ws) {
    this.ws = ws;
    this.id = 0;
    this.pending = new Map();
    this.listeners = new Set();
    ws.addEventListener("message", (ev) => {
      let msg;
      try { msg = JSON.parse(ev.data); } catch { return; }
      if (msg.id !== undefined && this.pending.has(msg.id)) {
        const { resolve, reject } = this.pending.get(msg.id);
        this.pending.delete(msg.id);
        if (msg.error) reject(new Error(msg.method + ": " + msg.error.message));
        else resolve(msg.result);
      } else if (msg.method) {
        for (const l of this.listeners) l(msg);
      }
    });
  }
  send(method, params = {}, sessionId) {
    const id = ++this.id;
    const payload = { id, method, params };
    if (sessionId) payload.sessionId = sessionId;
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      this.ws.send(JSON.stringify(payload));
    });
  }
  on(fn) { this.listeners.add(fn); }
}

async function main() {
  const wsUrl = await readBrowserWs();

  const ws = new WebSocket(wsUrl);
  await new Promise((res, rej) => {
    const t = setTimeout(() => rej(new Error("ws open timeout")), 10000);
    ws.addEventListener("open", () => { clearTimeout(t); res(); }, { once: true });
    ws.addEventListener("error", () => { clearTimeout(t); rej(new Error("ws error")); }, { once: true });
  });

  const cdp = new CDP(ws);

  // Create a fresh page target and attach with flattened sessions so every
  // subsequent command/event is routed by sessionId over this one socket.
  const { targetId } = await cdp.send("Target.createTarget", { url: "about:blank" });
  const { sessionId } = await cdp.send("Target.attachToTarget", { targetId, flatten: true });

  await cdp.send("Page.enable", {}, sessionId);
  await cdp.send("Runtime.enable", {}, sessionId);
  await cdp.send("Page.navigate", { url: inputUrl }, sessionId);

  // Poll for the render signal set by page.html.j2 (KaTeX done + fonts.ready).
  const deadline = Date.now() + 30000;
  let ready = false;
  while (Date.now() < deadline) {
    try {
      const r = await cdp.send("Runtime.evaluate", {
        expression: "window.__RENDER_DONE__ === true",
        returnByValue: true,
      }, sessionId);
      if (r && r.result && r.result.value === true) { ready = true; break; }
    } catch { /* execution context swapped during navigation — retry */ }
    await sleep(150);
  }
  if (!ready) console.error("print_pdf: warning — __RENDER_DONE__ not set within 30s; printing anyway");

  // Footer: title (CLI arg) + Hebrew page counter. Header intentionally empty.
  const footerTemplate =
    '<div dir="rtl" style="font-size:7.5px;font-family:\'DejaVu Sans\',sans-serif;'
    + 'color:#5b6b7d;width:100%;text-align:center;">'
    + escapeHtml(args.footer)
    + (args.footer ? " — " : "")
    + 'עמוד <span class="pageNumber"></span> מתוך <span class="totalPages"></span>'
    + "</div>";

  const pdf = await cdp.send("Page.printToPDF", {
    printBackground: true,
    preferCSSPageSize: false,
    paperWidth: 8.27,     // A4 in inches
    paperHeight: 11.69,
    marginTop: 0.55,
    marginBottom: 0.63,
    marginLeft: 0.47,
    marginRight: 0.47,
    displayHeaderFooter: true,
    headerTemplate: "<span></span>",
    footerTemplate,
  }, sessionId);

  writeFileSync(outPath, Buffer.from(pdf.data, "base64"));
  try { ws.close(); } catch {}
  cleanup();
  console.log("print_pdf: wrote " + outPath);
  process.exit(0);
}

main().catch((e) => fail(e && e.stack ? e.stack : String(e)));
