import "dotenv/config";
import { fetchArtistInsights } from "./spotify.js";
import { fetchChannelInsights } from "./youtube.js";

interface CheckResult {
  ok: boolean;
  reason?: string;
}

async function validateSpotify(): Promise<CheckResult> {
  const { SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_ARTIST_ID } = process.env;
  if (!SPOTIFY_CLIENT_ID || !SPOTIFY_CLIENT_SECRET || !SPOTIFY_ARTIST_ID) {
    return { ok: false, reason: "Faltam SPOTIFY_CLIENT_ID / SPOTIFY_CLIENT_SECRET / SPOTIFY_ARTIST_ID no .env" };
  }

  const artist = await fetchArtistInsights({
    clientId: SPOTIFY_CLIENT_ID,
    clientSecret: SPOTIFY_CLIENT_SECRET,
    artistId: SPOTIFY_ARTIST_ID,
  });

  console.log("Spotify:", artist);
  return { ok: true };
}

async function validateYoutube(): Promise<CheckResult> {
  const { YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_REDIRECT_URI, YOUTUBE_REFRESH_TOKEN } = process.env;
  if (!YOUTUBE_CLIENT_ID || !YOUTUBE_CLIENT_SECRET || !YOUTUBE_REFRESH_TOKEN) {
    return {
      ok: false,
      reason: "Faltam credenciais do YouTube no .env. Rode `npm run auth:youtube` primeiro.",
    };
  }

  const insights = await fetchChannelInsights({
    clientId: YOUTUBE_CLIENT_ID,
    clientSecret: YOUTUBE_CLIENT_SECRET,
    redirectUri: YOUTUBE_REDIRECT_URI ?? "http://localhost:8787/oauth2callback",
    refreshToken: YOUTUBE_REFRESH_TOKEN,
  });

  console.log("YouTube:", insights);
  return { ok: true };
}

async function main() {
  const results: Record<string, CheckResult> = {};

  try {
    results.spotify = await validateSpotify();
  } catch (err) {
    results.spotify = { ok: false, reason: (err as Error).message };
  }

  try {
    results.youtube = await validateYoutube();
  } catch (err) {
    results.youtube = { ok: false, reason: (err as Error).message };
  }

  console.log("\n--- Resumo da validação ---");
  for (const [name, result] of Object.entries(results)) {
    console.log(`${result.ok ? "OK " : "FAIL"} ${name}${result.reason ? ` — ${result.reason}` : ""}`);
  }

  if (Object.values(results).some((r) => !r.ok)) {
    process.exitCode = 1;
  }
}

main();
