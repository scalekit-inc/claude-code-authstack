import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const MARKETPLACE_PATH = path.resolve(
  __dirname,
  "..",
  ".claude-plugin",
  "marketplace.json"
);

function emitLog({ hypothesisId, message, data, location }) {
  // #region agent log
  fetch("http://127.0.0.1:7243/ingest/edcf95d5-0156-42ac-ac48-4bc3c77b9e56", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      runId: "marketplace-validate",
      hypothesisId,
      location,
      message,
      data,
      timestamp: Date.now(),
    }),
  }).catch(() => {});
  // #endregion
}

function main() {
  // #region agent log
  emitLog({
    hypothesisId: "A",
    location: "scripts/validate-marketplace.mjs:28",
    message: "Validate marketplace.json start",
    data: { marketplacePath: MARKETPLACE_PATH },
  });
  // #endregion

  const raw = fs.readFileSync(MARKETPLACE_PATH, "utf8");
  const parsed = JSON.parse(raw);

  // #region agent log
  emitLog({
    hypothesisId: "B",
    location: "scripts/validate-marketplace.mjs:40",
    message: "Parsed marketplace.json",
    data: {
      topLevelKeys: Object.keys(parsed),
      pluginsCount: Array.isArray(parsed.plugins) ? parsed.plugins.length : null,
      topLevelSourceType: typeof parsed.source,
    },
  });
  // #endregion

  const plugins = Array.isArray(parsed.plugins) ? parsed.plugins : [];

  // #region agent log
  emitLog({
    hypothesisId: "C",
    location: "scripts/validate-marketplace.mjs:55",
    message: "Begin plugin source validation",
    data: { pluginsCount: plugins.length },
  });
  // #endregion

  for (const plugin of plugins) {
    const sourceType = typeof plugin.source;
    const sourceValue =
      sourceType === "string" ? plugin.source : JSON.stringify(plugin.source);
    const sourcePath =
      sourceType === "string"
        ? path.resolve(path.dirname(MARKETPLACE_PATH), plugin.source)
        : null;
    const sourceExists = sourcePath ? fs.existsSync(sourcePath) : null;

    // #region agent log
    emitLog({
      hypothesisId: "D",
      location: "scripts/validate-marketplace.mjs:77",
      message: "Plugin source inspection",
      data: {
        pluginName: plugin.name,
        sourceType,
        sourceValue,
        sourcePath,
        sourceExists,
        sourceKeys:
          sourceType === "object" && plugin.source
            ? Object.keys(plugin.source)
            : null,
      },
    });
    // #endregion
  }

  // #region agent log
  emitLog({
    hypothesisId: "E",
    location: "scripts/validate-marketplace.mjs:96",
    message: "Marketplace validation finished",
    data: { pluginsCount: plugins.length },
  });
  // #endregion
}

main();
