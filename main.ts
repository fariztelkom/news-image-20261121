import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR;
if (!outDir) {
  throw new Error("MAKEFUN_OUTPUT_DIR must point to a writable output directory");
}

const source = new URL("entry.png", import.meta.url);
if (!existsSync(source)) {
  throw new Error("entry.png is missing from the repository root");
}
const bytes = statSync(source).size;
if (bytes === 0 || bytes > 1048576) {
  throw new Error(`entry.png is ${bytes} bytes; expected 1..1048576`);
}

mkdirSync(outDir, { recursive: true });
const destination = join(outDir, "entry.png");
copyFileSync(source, destination);
if (statSync(destination).size !== bytes) {
  throw new Error("copied image size does not match the source");
}
console.log(`wrote entry.png (${bytes} bytes)`);
