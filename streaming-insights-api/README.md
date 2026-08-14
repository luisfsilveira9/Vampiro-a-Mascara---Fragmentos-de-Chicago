# streaming-insights-api

Insights de streaming usando **APIs oficiais** — sem scraping, sem engenharia reversa.

Cobre o que dá para conseguir de forma 100% suportada:

| Fonte | Dados | Método |
|---|---|---|
| Spotify Web API | seguidores do artista, popularidade (0-100), gêneros | Client Credentials (nível de app, sem login) |
| YouTube Data API + YouTube Analytics API | inscritos, views totais, views/minutos assistidos/inscritos ganhos-perdidos nos últimos 28 dias | OAuth2 (autoriza sua própria conta) |

Não cobre (porque essas APIs não expõem): ouvintes mensais do Spotify, número/alcance de playlists. Isso só existe no painel Spotify for Artists — ver o projeto irmão `streaming-insights-scraper`.

## Setup

```bash
npm install
cp .env.example .env
```

### 1. Spotify

1. Acesse https://developer.spotify.com/dashboard e crie um app (qualquer nome/descrição).
2. Copie o **Client ID** e **Client Secret** para `SPOTIFY_CLIENT_ID` / `SPOTIFY_CLIENT_SECRET` no `.env`.
3. Pegue o ID do artista pela URL do Spotify: `open.spotify.com/artist/<ID>` → cole em `SPOTIFY_ARTIST_ID`.

Não precisa de login de usuário — é autenticação de app (Client Credentials Flow), então só dá acesso a dados públicos de catálogo (não a métricas privadas como ouvintes mensais).

### 2. YouTube

1. Crie um projeto em https://console.cloud.google.com.
2. Habilite as APIs **YouTube Data API v3** e **YouTube Analytics API**.
3. Configure a tela de consentimento OAuth (modo "Testing" é suficiente para uso pessoal).
4. Crie uma credencial **OAuth Client ID** do tipo **Desktop app**.
5. Copie Client ID/Secret para o `.env`.
6. Rode:
   ```bash
   npm run auth:youtube
   ```
   Abra a URL impressa, autorize com a conta dona do canal, e copie o `YOUTUBE_REFRESH_TOKEN` mostrado no terminal para o `.env`.

## Validar

```bash
npm run validate
```

Roda as duas integrações de forma independente e imprime um resumo OK/FAIL — útil para testar cada uma isoladamente enquanto você configura as credenciais aos poucos.
