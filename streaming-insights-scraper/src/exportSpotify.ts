import fs from "node:fs";
import path from "node:path";
import { launchChromium } from "./browser.js";

const STORAGE_STATE_PATH = path.resolve("./.auth/spotify-artists.json");
const EXPORTS_DIR = path.resolve("./exports");

// A Spotify muda o layout/rótulos do dashboard sem aviso — se o download falhar,
// rode com HEADLESS=false para ver a página ao vivo e ajustar este seletor.
const DOWNLOAD_BUTTON_TEXT = /download csv/i;

const PAGES_TO_EXPORT = [
  { name: "audience", url: "https://artists.spotify.com/audience" },
  { name: "playlists", url: "https://artists.spotify.com/playlists" },
  { name: "songs", url: "https://artists.spotify.com/songs" },
];

async function main() {
  if (!fs.existsSync(STORAGE_STATE_PATH)) {
    console.error(`Sessão não encontrada em ${STORAGE_STATE_PATH}.`);
    console.error('Rode "npm run login:spotify" primeiro (numa máquina com tela).');
    process.exit(1);
  }
  fs.mkdirSync(EXPORTS_DIR, { recursive: true });

  const headless = process.env.HEADLESS !== "false";
  const browser = await launchChromium({ headless });
  const context = await browser.newContext({ storageState: STORAGE_STATE_PATH });
  const page = await context.newPage();

  await page.goto("https://artists.spotify.com/home");

  if (page.url().includes("accounts.spotify.com")) {
    console.error('Sessão expirada — rode novamente "npm run login:spotify" para logar de novo.');
    await browser.close();
    process.exit(1);
  }

  let failures = 0;

  for (const { name, url } of PAGES_TO_EXPORT) {
    try {
      await page.goto(url);
      await page.waitForLoadState("networkidle");

      const downloadButton = page.getByRole("button", { name: DOWNLOAD_BUTTON_TEXT }).first();
      const [download] = await Promise.all([
        page.waitForEvent("download", { timeout: 15000 }),
        downloadButton.click(),
      ]);

      const timestamp = new Date().toISOString().slice(0, 10);
      const destination = path.join(EXPORTS_DIR, `${name}-${timestamp}.csv`);
      await download.saveAs(destination);
      console.log(`OK   ${name} -> ${destination}`);
    } catch (err) {
      failures += 1;
      console.error(`FAIL ${name}: ${(err as Error).message}`);
      console.error(`     Verifique se o botão de download ainda existe em ${url}.`);
    }
  }

  await browser.close();
  process.exitCode = failures > 0 ? 1 : 0;
}

main();
