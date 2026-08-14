import { chromium, type Browser } from "playwright";

// Escape hatch opcional: permite apontar para um binário do Chromium já
// instalado (útil em ambientes onde o download automático do Playwright
// não é possível ou já existe uma instalação compatível).
export function launchChromium(options: { headless: boolean }): Promise<Browser> {
  const executablePath = process.env.PLAYWRIGHT_CHROMIUM_PATH;
  return chromium.launch({
    headless: options.headless,
    ...(executablePath ? { executablePath } : {}),
  });
}
