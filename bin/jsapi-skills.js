#!/usr/bin/env node

import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const packageRoot = path.resolve(path.dirname(__filename), "..");
const command = process.argv[2] || "install";

function resolveTargetDir() {
  const customTarget = process.env.MAPTEC_SKILL_INSTALL_DIR;
  if (customTarget) {
    return path.resolve(customTarget, "jsapi-skills");
  }

  return path.join(os.homedir(), ".agents", "skills", "jsapi-skills");
}

function copyDir(src, dest) {
  fs.mkdirSync(dest, { recursive: true });

  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);

    if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
      continue;
    }

    fs.copyFileSync(srcPath, destPath);
  }
}

function copyEntry(name, targetDir) {
  const src = path.join(packageRoot, name);
  const dest = path.join(targetDir, name);

  if (!fs.existsSync(src)) {
    throw new Error(`Package entry not found: ${name}`);
  }

  const stat = fs.statSync(src);
  if (stat.isDirectory()) {
    copyDir(src, dest);
    return;
  }

  fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.copyFileSync(src, dest);
}

function install() {
  const targetDir = resolveTargetDir();
  const entries = ["SKILL.md", "README.md", "references", "scripts", "package.json"];

  fs.mkdirSync(targetDir, { recursive: true });
  for (const entry of entries) {
    copyEntry(entry, targetDir);
  }

  console.log(`jsapi-skills installed to ${targetDir}`);
}

function printHelp() {
  console.log(`Usage:
  npx @maptec/jsapi-skills install

Environment:
  MAPTEC_SKILL_INSTALL_DIR  Optional parent directory for installing jsapi-skills.
                            Defaults to ~/.agents/skills`);
}

try {
  if (command === "install") {
    install();
  } else if (command === "help" || command === "--help" || command === "-h") {
    printHelp();
  } else {
    console.error(`Unknown command: ${command}`);
    printHelp();
    process.exit(1);
  }
} catch (error) {
  console.error(error instanceof Error ? error.message : error);
  process.exit(1);
}
