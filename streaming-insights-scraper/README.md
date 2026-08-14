# streaming-insights-scraper

Automação de exportação dos dashboards de artista (**Spotify for Artists**, e futuramente Apple Music for Artists / SoundCloud for Artists) via Playwright — para conseguir métricas que não existem em nenhuma API pública, como **ouvintes mensais** e **número/alcance de playlists**.

## Como funciona

1. `npm run login:spotify` abre um navegador de verdade, você faz login manual (incluindo 2FA), e a sessão é salva em `.auth/spotify-artists.json`.
2. `npm run export:spotify` reaproveita essa sessão salva, navega pelas abas do dashboard e clica no botão "Download CSV" de cada uma, salvando os arquivos em `exports/`.
3. Seu pipeline (fora deste projeto) importa esses CSVs para um banco de dados e monta os gráficos.

Nenhuma senha é armazenada em texto — apenas os cookies de sessão do navegador (`storageState` do Playwright), e só localmente.

## ⚠️ Aviso importante sobre Termos de Serviço

Este projeto **não usa nenhuma API oficial** — ele automatiza cliques num painel feito para uso humano manual. Isso normalmente está fora do que os Termos de Serviço da Spotify (e da maioria das plataformas) permitem ("acesso automatizado" costuma ser proibido), mesmo sendo a sua própria conta e seus próprios dados. Riscos práticos:

- A conta de artista pode ser sinalizada/suspensa se o uso automatizado for detectado.
- Os seletores usados aqui (`src/exportSpotify.ts`) vão quebrar sempre que a Spotify mudar o layout do dashboard — não há garantia de estabilidade.
- Recomendado para uso pessoal, com moderação (ex: 1x por semana), nunca em alta frequência.

Use por sua conta e risco.

## Setup

```bash
npm install
```

Este projeto não precisa de `.env` — não há segredos armazenados. O login é sempre manual e interativo.

### Rodar o login (precisa de máquina com tela)

```bash
npm run login:spotify
```

Isso **não funciona neste ambiente remoto/sandbox** (não há display gráfico nem forma de resolver 2FA aqui) — rode localmente na sua máquina, com Node instalado.

### Exportar os relatórios

```bash
npm run export:spotify
```

Por padrão roda headless. Para depurar visualmente (ex: se o botão de download não for encontrado), rode:

```bash
HEADLESS=false npm run export:spotify
```

Se o Playwright reclamar que não encontra o executável do Chromium (versão baixada não bate com uma instalação existente), aponte manualmente com `PLAYWRIGHT_CHROMIUM_PATH=/caminho/para/chrome`.

## Validar

```bash
npm run validate
```

Testa se o Playwright consegue abrir o Chromium e alcançar a página de login (não requer sessão salva) — útil para confirmar que a parte "motor de automação" está funcionando, independente de já ter feito login ou não.
