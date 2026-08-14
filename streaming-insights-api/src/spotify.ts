export interface SpotifyArtistInsights {
  id: string;
  name: string;
  followers: number;
  popularity: number;
  genres: string[];
  externalUrl: string;
}

async function getAppToken(clientId: string, clientSecret: string): Promise<string> {
  const basic = Buffer.from(`${clientId}:${clientSecret}`).toString("base64");
  const res = await fetch("https://accounts.spotify.com/api/token", {
    method: "POST",
    headers: {
      Authorization: `Basic ${basic}`,
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: "grant_type=client_credentials",
  });

  if (!res.ok) {
    throw new Error(`Falha ao obter token do Spotify (${res.status}): ${await res.text()}`);
  }

  const data = (await res.json()) as { access_token: string };
  return data.access_token;
}

export async function fetchArtistInsights(params: {
  clientId: string;
  clientSecret: string;
  artistId: string;
}): Promise<SpotifyArtistInsights> {
  const token = await getAppToken(params.clientId, params.clientSecret);

  const res = await fetch(`https://api.spotify.com/v1/artists/${params.artistId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  if (!res.ok) {
    throw new Error(`Falha ao buscar artista no Spotify (${res.status}): ${await res.text()}`);
  }

  const data = await res.json();

  return {
    id: data.id,
    name: data.name,
    followers: data.followers.total,
    popularity: data.popularity,
    genres: data.genres,
    externalUrl: data.external_urls.spotify,
  };
}
