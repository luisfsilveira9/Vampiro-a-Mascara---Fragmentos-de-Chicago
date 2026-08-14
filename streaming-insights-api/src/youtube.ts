import { google } from "googleapis";

export interface YoutubeChannelInsights {
  channelTitle: string;
  subscribers: number;
  totalViews: number;
  last28Days: {
    views: number;
    estimatedMinutesWatched: number;
    subscribersGained: number;
    subscribersLost: number;
  };
}

export async function fetchChannelInsights(params: {
  clientId: string;
  clientSecret: string;
  redirectUri: string;
  refreshToken: string;
}): Promise<YoutubeChannelInsights> {
  const oauth2Client = new google.auth.OAuth2(params.clientId, params.clientSecret, params.redirectUri);
  oauth2Client.setCredentials({ refresh_token: params.refreshToken });

  const youtube = google.youtube({ version: "v3", auth: oauth2Client });
  const channelsRes = await youtube.channels.list({ part: ["snippet", "statistics"], mine: true });
  const channel = channelsRes.data.items?.[0];
  if (!channel) {
    throw new Error("Nenhum canal encontrado para esta conta autenticada.");
  }

  const youtubeAnalytics = google.youtubeAnalytics({ version: "v2", auth: oauth2Client });
  const end = new Date();
  const start = new Date();
  start.setDate(start.getDate() - 28);
  const fmt = (d: Date) => d.toISOString().slice(0, 10);

  const analyticsRes = await youtubeAnalytics.reports.query({
    ids: "channel==MINE",
    startDate: fmt(start),
    endDate: fmt(end),
    metrics: "views,estimatedMinutesWatched,subscribersGained,subscribersLost",
  });

  const row = (analyticsRes.data.rows?.[0] ?? [0, 0, 0, 0]) as number[];

  return {
    channelTitle: channel.snippet?.title ?? "desconhecido",
    subscribers: Number(channel.statistics?.subscriberCount ?? 0),
    totalViews: Number(channel.statistics?.viewCount ?? 0),
    last28Days: {
      views: Number(row[0] ?? 0),
      estimatedMinutesWatched: Number(row[1] ?? 0),
      subscribersGained: Number(row[2] ?? 0),
      subscribersLost: Number(row[3] ?? 0),
    },
  };
}
