import "dotenv/config";
import http from "node:http";
import { google } from "googleapis";

const CLIENT_ID = process.env.YOUTUBE_CLIENT_ID;
const CLIENT_SECRET = process.env.YOUTUBE_CLIENT_SECRET;
const REDIRECT_URI = process.env.YOUTUBE_REDIRECT_URI ?? "http://localhost:8787/oauth2callback";

if (!CLIENT_ID || !CLIENT_SECRET) {
  console.error("Defina YOUTUBE_CLIENT_ID e YOUTUBE_CLIENT_SECRET no .env antes de rodar este script.");
  process.exit(1);
}

const oauth2Client = new google.auth.OAuth2(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI);

const SCOPES = [
  "https://www.googleapis.com/auth/yt-analytics.readonly",
  "https://www.googleapis.com/auth/youtube.readonly",
];

const authUrl = oauth2Client.generateAuthUrl({
  access_type: "offline",
  prompt: "consent",
  scope: SCOPES,
});

console.log("\nAbra esta URL no navegador e autorize o acesso à sua conta do YouTube:\n");
console.log(authUrl, "\n");

const redirectUrl = new URL(REDIRECT_URI);
const port = Number(redirectUrl.port) || 8787;

const server = http.createServer(async (req, res) => {
  if (!req.url) return;
  const url = new URL(req.url, REDIRECT_URI);
  const code = url.searchParams.get("code");

  if (url.pathname !== redirectUrl.pathname || !code) {
    res.writeHead(404);
    res.end();
    return;
  }

  res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
  res.end("<h1>Autorizado! Pode fechar esta aba e voltar ao terminal.</h1>");
  server.close();

  const { tokens } = await oauth2Client.getToken(code);
  console.log("\nAutorização concluída. Copie o refresh token abaixo para o seu .env:\n");
  console.log(`YOUTUBE_REFRESH_TOKEN=${tokens.refresh_token}\n`);
});

server.listen(port, () => {
  console.log(`Aguardando callback em ${REDIRECT_URI} ...`);
});
