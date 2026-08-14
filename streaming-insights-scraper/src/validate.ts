import fs from "node:fs";
import path from "node:path";
import { launchChromium } from "./browser.js";

async function main() {
  console.log("Validando que o Playwright consegue abrir um navegador e acessar a página de login...");

  const browser = await launchChromium({ headless: true });
  const page = await browser.newPage();
  await page.goto("https://artists.spotify.com/home", { waitUntil: "domcontentloaded" });
  const title = await page.title();
  await browser.close();

  console.log(`OK   Navegador funcionando. Título da página carregada: "${title}"`);

  const storageStatePath = path.resolve("./.auth/spotify-artists.json");
  if (fs.existsSync(storageStatePath)) {
    console.log(`OK   Sessão salva encontrada em ${storageStatePath} — pronto para "npm run export:spotify".`);
  } else {
    console.log('INFO Nenhuma sessão salva ainda. Rode "npm run login:spotify" (em máquina com tela) antes de exportar.');
  }
}

main();
