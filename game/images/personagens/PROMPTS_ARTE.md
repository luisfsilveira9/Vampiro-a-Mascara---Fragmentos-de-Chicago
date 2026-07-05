# Prompts de arte — sprites de personagens

Este arquivo existe porque o Claude que trabalhou nesta branch **não tem uma
ferramenta de geração de imagens conectada** — só consegue editar código.
O que foi feito:

1. `game/script.rpy` já define, para cada personagem abaixo, uma imagem por
   expressão (ex.: `image isadora seria`, `image moto tenso`). Enquanto o
   arquivo PNG não existir, o jogo mostra automaticamente um placeholder
   colorido com o nome e a expressão escritos (função `retrato()` em
   `script.rpy`, via `renpy.loadable()`).
2. Quando você gerar a arte (Midjourney, Leonardo.Ai, ChatGPT/DALL-E, etc.)
   usando os prompts abaixo, **salve o PNG com o nome de arquivo exato**
   indicado em cada seção, dentro de `game/images/personagens/`. Não precisa
   mudar nada no código — o placeholder é substituído automaticamente na
   próxima vez que o jogo rodar.

## Estilo visual de referência (obrigatório em todo prompt)

As artes já existentes (`Isadora.png`, `Silas.png`, `Rook.png`, `Marcus.png`,
`MadameK.png`) definem o estilo. Use sempre esta base, adaptando só a
descrição do personagem/expressão:

> Semi-realistic painted digital illustration, digital painting style (not
> anime, not photo-real), visible soft brushwork, moody cinematic lighting
> with subtle rim light, dark desaturated gothic urban-fantasy palette in
> the tone of Vampire: The Masquerade, full-body standing figure, facing
> camera or slight three-quarter angle, centered in frame, square 1:1
> composition, isolated on a flat solid background (pure black or pure
> green) for easy background removal, transparent PNG cutout, no ground
> shadow beyond a soft contact shadow, sharp facial detail, highly detailed
> clothing textures, 1080x1080.

Depois de gerado, remova o fundo (remove.bg, Photoshop, GIMP) para deixar o
PNG com canal alfa transparente, igual às artes atuais.

**Importante para consistência entre expressões:** gere todas as expressões
de um mesmo personagem na mesma sessão/seed (ou usando a arte já existente
como referência de estilo/roupa, quando disponível), para que o rosto, a
roupa e o penteado não mudem entre uma expressão e outra — só a expressão
facial e a pose devem variar.

---

## Isadora Vane (já tem arte base: `Isadora.png`)

Personagem: vampira sedutora e perigosa, cabelo longo ondulado castanho
escuro, vestido gótico preto de mangas longas com detalhes em renda e um
colar de gargantilha vermelho, maquiagem escura e batom quase preto,
postura altiva e controlada.

| Arquivo | Expressão | Prompt (descrição facial/pose específica) |
|---|---|---|
| `Isadora.png` (já existe) | neutra | — arte já existente, usada como padrão |
| `Isadora_seria.png` | séria | Same character as reference, cold serious expression, narrowed eyes, arms crossed, interrogating stare, jaw tense |
| `Isadora_brava.png` | brava | Same character as reference, furious expression, brow lowered, teeth slightly bared showing a hint of fangs, fists clenched at her sides |
| `Isadora_medo.png` | medo (vulnerável) | Same character as reference, rare flash of fear in her eyes, slightly parted lips, shoulders tensed defensively, eyes wide, first time showing vulnerability |

---

## Silas (já tem arte base: `Silas.png`, mostrado ferido)

Personagem: jovem cria vampiro, moletom com capuz rasgado e manchado de
sangue e queimaduras, calça jeans escura rasgada, tênis surrados, cabelo
castanho claro bagunçado, olheiras fundas, ferimentos que regeneram
lentamente.

| Arquivo | Expressão | Prompt |
|---|---|---|
| `Silas.png` (já existe) | ferido | — arte já existente, usada como padrão |
| `Silas_dor.png` | dor | Same character as reference, grimacing in pain, leaning on a metal table for support, burnt skin visibly hissing/steaming as it regenerates, gritted teeth |
| `Silas_exausto.png` | exausto | Same character as reference, exhausted slumped posture, half-lidded eyes, drained vampiric pallor, catching his breath after fleeing |

---

## Rook (já tem arte base: `Rook.png`)

Personagem: líder anarquista vampiro, corte de cabelo raspado nas laterais,
cicatrizes no rosto, jaqueta de couro preta com remendos e patches,
camiseta cinza por baixo, calça jeans escura, postura de braços cruzados,
expressão desconfiada.

| Arquivo | Expressão | Prompt |
|---|---|---|
| `Rook.png` (já existe) | neutro | — arte já existente, usada como padrão |
| `Rook_irritado.png` | irritado | Same character as reference, openly irritated scowl, one eyebrow raised, pointing off-frame as if barking an order, aggressive stance |
| `Rook_preocupado.png` | preocupado | Same character as reference, worried frown, arms uncrossed, leaning forward slightly, studying something out of frame with concern |

---

## Moto (sem arte ainda)

Personagem: anarquista corpulento, segurança do bando de Rook, jaqueta de
couro molhada de chuva, camiseta justa, limpa uma escopeta, presença física
intimidadora, cabelo curto, barba por fazer.

| Arquivo | Expressão | Prompt |
|---|---|---|
| `Moto_neutro.png` | neutro | Burly bald or short-haired male anarch vampire bodyguard, rain-soaked leather jacket, tight t-shirt underneath, cleaning a shotgun, calm watchful neutral expression, imposing build |
| `Moto_tenso.png` | tenso | Same character, tense alert expression, water dripping from his jacket, reporting urgent news, gripping the shotgun tighter, jaw set |
| `Moto_alerta.png` | alerta | Same character, sharp alert combat-ready stance, scanning off-frame, shotgun raised slightly, focused predatory attention |

---

## Slick (sem arte ainda)

Personagem: hacker anarquista, garota pálida, estilo streetwear/punk,
laptop coberto de adesivos, roupas escuras práticas, dedos rápidos no
teclado, atitude irônica e confiante.

| Arquivo | Expressão | Prompt |
|---|---|---|
| `Slick_concentrada.png` | concentrada | Pale young female hacker vampire anarch, punk streetwear, dark practical clothes, sitting or leaning over a sticker-covered laptop, deeply focused concentrated expression, fingers blurring on the keyboard |
| `Slick_surpresa.png` | surpresa | Same character, eyes wide in excited surprise, pointing at her laptop screen triumphantly, half grin |
| `Slick_irritada.png` | irritada | Same character, annoyed frustrated scowl, pulling back from the laptop as if it just sparked/failed, one hand up in exasperation |

---

## Doutor Miller (sem arte ainda)

Personagem: lacaio ghoul, médico decadente que vende sangue roubado no
necrotério, jaleco sujo por cima de roupas surradas, óculos, aparência
suja e ganancioso, ambiente de necrotério ao fundo (mas gerar isolado,
sem fundo).

| Arquivo | Expressão | Prompt |
|---|---|---|
| `DrMiller_ganancioso.png` | ganancioso | Grimy ghoul mortician in his 50s, stained lab coat over shabby clothes, thin greasy hair, glasses, greedy calculating smile, rubbing his hands together, standing beside a blood bag |
| `DrMiller_assustado.png` | assustado | Same character, terrified expression, recoiling backward, hands raised defensively, sweating, cowering |
| `DrMiller_arrogante.png` | arrogante | Same character, smug arrogant smirk, chin raised, arms crossed confidently, sneering, feeling protected by a powerful patron |

---

## Mulher de Vestido Vermelho / "dançarina" (sem arte ainda)

Personagem: mortal na pista de dança do clube Velvet, vestido vermelho
justo, dançando de olhos fechados, entregue à música, cabelo solto em
movimento.

| Arquivo | Expressão | Prompt |
|---|---|---|
| `MulherVestidoVermelho_dancando.png` | dançando | Young woman in a tight red dress dancing on a nightclub floor, eyes closed, lost in the music, hair mid-motion, colorful club lighting reflections, sensual carefree pose |
| `MulherVestidoVermelho_sedutora.png` | sedutora | Same character, eyes now open and hypnotized, seductive dreamy smile, leaning close toward the viewer, flushed cheeks, hand reaching toward the viewer's collar |
| `MulherVestidoVermelho_panico.png` | pânico | Same character, sudden panic and fear, eyes wide, mouth open mid-scream, pushing away defensively, makeup slightly smudged |

---

## Mulher no Bar / "executiva" (sem arte ainda)

Personagem: mulher de terninho escuro sentada no bar do clube, girando um
copo de dry martini, olhar cínico e entediado, postura de alta sociedade
fria.

| Arquivo | Expressão | Prompt |
|---|---|---|
| `MulherNoBar_entediada.png` | entediada | Elegant woman in a dark tailored pantsuit sitting at a nightclub bar, spinning an untouched dry martini glass, cynical bored expression, looking down at the crowd with disdain |
| `MulherNoBar_interessada.png` | interessada | Same character, subtle interested smirk, head tilted, eyes now sharp and engaged, leaning slightly toward the viewer |
| `MulherNoBar_panico.png` | pânico | Same character, sudden panic and fear, eyes wide, recoiling off her bar stool, glass knocked over, mouth open mid-gasp |

---

## Bandido no Beco (sem arte ainda)

Personagem: assaltante de beco escuro, roupas escuras baratas, capuz,
postura ameaçadora com uma faca tática.

| Arquivo | Expressão | Prompt |
|---|---|---|
| `BandidoNoBeco_ameacador.png` | ameaçador | Menacing mugger in a dark alley, cheap dark hoodie, brandishing a tactical knife, aggressive threatening stance, rain-soaked alley atmosphere |
| `BandidoNoBeco_ferido.png` | ferido | Same character, wrist broken and bleeding, wincing in pain, knife dropped, defeated defensive posture |

---

## Turista no Beco (sem arte ainda)

Personagem: turista comum encurralado no beco antes de fugir, roupas
casuais de viagem, câmera ou mochila, expressão de pânico.

| Arquivo | Expressão | Prompt |
|---|---|---|
| `TuristaNoBeco_assustado.png` | assustado | Ordinary tourist cornered in a dark alley, casual travel clothes, small backpack or camera around the neck, terrified expression, backing away, about to flee |
| `TuristaNoBeco_aliviado.png` | aliviado | Same character, running away down the alley in profile, glancing back with relief on their face as the danger turns elsewhere |

---

## Resumo de arquivos esperados

```
game/images/personagens/
  Isadora.png                      (já existe)
  Isadora_seria.png
  Isadora_brava.png
  Isadora_medo.png
  Silas.png                        (já existe)
  Silas_dor.png
  Silas_exausto.png
  Rook.png                         (já existe)
  Rook_irritado.png
  Rook_preocupado.png
  Moto_neutro.png
  Moto_tenso.png
  Moto_alerta.png
  Slick_concentrada.png
  Slick_surpresa.png
  Slick_irritada.png
  DrMiller_ganancioso.png
  DrMiller_assustado.png
  DrMiller_arrogante.png
  MulherVestidoVermelho_dancando.png
  MulherVestidoVermelho_sedutora.png
  MulherVestidoVermelho_panico.png
  MulherNoBar_entediada.png
  MulherNoBar_interessada.png
  MulherNoBar_panico.png
  BandidoNoBeco_ameacador.png
  BandidoNoBeco_ferido.png
  TuristaNoBeco_assustado.png
  TuristaNoBeco_aliviado.png
```
