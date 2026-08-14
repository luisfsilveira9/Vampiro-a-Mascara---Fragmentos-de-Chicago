import fs from "node:fs";
import path from "node:path";
import { launchChromium } from "./browser.js";

const AUTH_DIR = path.resolve("./.auth");
const STORAGE_STATE_PATH = path.join(AUTH_DIR, "spotify-artists.json");

async function main() {
  fs.mkdirSync(AUTH_DIR, { recursive: true });

  console.log("Abrindo navegador para login manual no Spotify for Artists...");
  console.log(
    "IMPORTANTE: este script precisa rodar em uma máquina com tela (não funciona em " +
      "ambientes remotos/headless-only, como este sandbox) — o login real com 2FA exige " +
      "interação manual num navegador de verdade.\n",
  );

  const browser = await launchChromium({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();

  await page.goto("https://artists.spotify.com/home");

  console.log("Faça login manualmente na janela do navegador (incluindo 2FA se for pedido).");
  console.log("Assim que o dashboard carregar, volte aqui e pressione ENTER no terminal.");

  await new Promise<void>((resolve) => {
    process.stdin.once("data", () => resolve());
  });

  await context.storageState({ path: STORAGE_STATE_PATH });
  console.log(`\nSessão salva em ${STORAGE_STATE_PATH}`);
  console.log('Agora rode "npm run export:spotify" para baixar os relatórios.');

  await browser.close();
  process.exit(0);
}

main();
