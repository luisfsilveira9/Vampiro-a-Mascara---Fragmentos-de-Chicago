# ============================================================
# DADOS — SPRITES E ANIMAÇÃO DE ROLAGEM
# ============================================================
# Sem assets externos disponíveis, os "sprites" dos dados são
# construídos por composição (moldura + face + número) e animados
# via ATL. Dados normais lembram ossos entalhados; dados de Fome
# usam o vermelho já estabelecido na identidade visual do jogo.

# --- Monta um pool de dados a partir de (dicionário, chave) e já devolve
# a lista de componentes (nome, valor) usada tanto no número exibido no
# menu de escolha quanto no detalhamento mostrado na tela de rolagem. ---
init python:
    def montar_pool(*pares):
        componentes = [(chave, dic[chave]) for dic, chave in pares]
        total = max(1, sum(valor for _, valor in componentes))
        return total, componentes


transform dado_entrada(atraso=0.0):
    rotate (renpy.random.choice([-20, 20]))
    zoom 0.3
    alpha 0.0
    pause atraso
    parallel:
        easein 0.2 alpha 1.0
    parallel:
        easein 0.35 rotate 0
    parallel:
        easein 0.22 zoom 1.15
        easeout 0.15 zoom 1.0


screen dado(valor, cor_borda, cor_face, cor_texto, atraso=0.0, tamanho=72):
    frame:
        at dado_entrada(atraso)
        xsize tamanho
        ysize tamanho
        background Solid(cor_borda)
        padding (4, 4)
        frame:
            background Solid(cor_face)
            xfill True
            yfill True
            text "[valor]" size int(tamanho * 0.5) color cor_texto bold True xalign 0.5 yalign 0.5


screen dado_costas(cor, tamanho=26):
    frame:
        xsize tamanho
        ysize tamanho
        background Solid(cor)


screen confirma_teste(reserva, fome_atual, componentes=None):
    modal True
    zorder 100
    add Solid("#000000aa")

    frame:
        align (0.5, 0.5)
        padding (40, 40)
        background Solid("#1a1a1a")

        vbox:
            spacing 18
            xalign 0.5

            text "TESTE DE RESISTÊNCIA" xalign 0.5 size 40 color "#8b0000"

            if componentes:
                text " + ".join("%s (%d)" % (nome, valor) for nome, valor in componentes) xalign 0.5 size 22 color "#cccccc"

            python:
                dados_normais = max(0, reserva - fome_atual)

            text "[reserva] dados na reserva" xalign 0.5 size 22 color "#ffffff"

            hbox:
                spacing 8
                xalign 0.5
                for _i in range(dados_normais):
                    use dado_costas("#e8e0d0")
                for _i in range(fome_atual):
                    use dado_costas("#8b0000")

            text "[dados_normais] normais  •  [fome_atual] de fome" xalign 0.5 size 18 color "#aaaaaa"

            textbutton "ROLAR DADOS":
                action Return(True)
                xalign 0.5
                padding (24, 12)
                background Solid("#4a0000")
                hover_background Solid("#8b0000")


screen resultado_teste(lista_normais, lista_fome, sucessos, dificuldade):
    modal True
    zorder 101
    add Solid("#000000cc")

    $ total_dados = lista_normais + lista_fome
    $ dez_normais = lista_normais.count(10)
    $ dez_fome = lista_fome.count(10)
    $ critico = (dez_normais + dez_fome) >= 2
    $ critico_sujo = critico and dez_fome > 0
    $ falha_bestial = (sucessos == 0) and (1 in lista_fome)
    $ atraso_texto = len(total_dados) * 0.12 + 0.25

    vbox:
        align (0.5, 0.4)
        spacing 25

        hbox:
            spacing 10
            xalign 0.5
            for i, d in enumerate(lista_normais):
                use dado(d, "#5a5040", "#f2ecd8", "#000000", atraso=i * 0.12)

        hbox:
            spacing 10
            xalign 0.5
            for i, d in enumerate(lista_fome):
                use dado(d, "#3a0000", "#8b0000", "#ffffff", atraso=(len(lista_normais) + i) * 0.12)

        if falha_bestial:
            text "FALHA BESTIAL" color "#ff3333" size 70 xalign 0.5 outlines [(4, "#000", 0, 0)] at dado_entrada(atraso_texto)
        elif critico_sujo:
            text "CRÍTICO SUJO" color "#ffcc00" size 70 xalign 0.5 outlines [(4, "#000", 0, 0)] at dado_entrada(atraso_texto)
        elif critico and sucessos >= dificuldade:
            text "SUCESSO CRÍTICO" color "#33ff33" size 70 xalign 0.5 outlines [(4, "#000", 0, 0)] at dado_entrada(atraso_texto)
        elif sucessos >= dificuldade:
            text "SUCESSO" color "#33ff33" size 80 xalign 0.5 outlines [(4, "#000", 0, 0)] at dado_entrada(atraso_texto)
        else:
            text "FALHA" color "#ff3333" size 80 xalign 0.5 outlines [(4, "#000", 0, 0)] at dado_entrada(atraso_texto)

        text "[sucessos] sucessos (Dificuldade [dificuldade])" xalign 0.5 size 20 color "#ffffff"

        if sucessos < dificuldade and vontade_atual > 0:
            textbutton "Gastar 1 de Vontade para tentar novamente até 3 dados normais que falharam? ([vontade_atual] restante(s))":
                action Return("rerolar")
                xalign 0.5
                text_size 18
                background Solid("#2a2a4a")
                hover_background Solid("#3a3a6a")
                padding (16, 8)

        textbutton "PROSSEGUIR":
            action Return("prosseguir")
            xalign 0.5
            background Solid("#333")
            hover_background "#555"
            padding (20, 10)


# --- Uso livre de Disciplina em cenas sociais/investigativas ---
# Em vez de travar a cena em uma única Disciplina "correta" pré-anunciada,
# esta rotina olha para a ficha do próprio jogador e oferece só as
# Disciplinas que ele realmente despertou, deixando a escolha por conta
# do jogador — sem revelar a fórmula do teste na tela.

init python:
    FLAVOR_DISCIPLINA_SOCIAL = {
        "Presença":      ("Carisma", "Você deixa sua presença sobrenatural encher o ambiente — uma gravidade que ninguém ao redor sabe nomear, mas que todos sentem na pele."),
        "Dominação":     ("Manipulação", "Seus olhos prendem os dela por um instante longo demais para ser natural, e sua vontade escorrega para dentro da mente alheia."),
        "Auspício":      ("Raciocínio", "Seus sentidos se esticam além do humano, lendo o que a pessoa tenta esconder antes mesmo que ela abra a boca."),
        "Potência":      ("Força", "Você deixa a força sobre-humana transparecer só o suficiente — um aperto de mão que quase estala ossos, uma ameaça que não precisa de palavras."),
        "Ofuscação":     ("Destreza", "Você se torna quase invisível aos olhos e à atenção alheia, uma sombra entre sombras, ouvindo o que não deveria."),
        "Animalismo":    ("Manipulação", "Você desperta o instinto mais profundo da vítima — calma ou puro terror animal diante do predador que ela sente, mas não consegue ver."),
        "Fortitude":     ("Resolução", "Você permanece imperturbável, uma parede viva diante de qualquer ameaça ou argumento, esperando a vítima ceder primeiro."),
        "Tenebrosidade": ("Manipulação", "As sombras ao seu redor parecem se inclinar na sua direção, sussurrando de volta os medos mais profundos da vítima."),
        "Celeridade":    ("Destreza", "Seus movimentos ficam rápidos demais para o olho mortal acompanhar — você já tem o que precisa antes que a vítima perceba que você se moveu."),
    }

screen escolha_disciplina(opcoes):
    modal True
    zorder 150
    add Solid("#000000cc")

    frame:
        align (0.5, 0.5)
        padding (40, 40)
        background Solid("#1a1a1a")

        vbox:
            spacing 14
            text "QUAL PODER DO SEU SANGUE VOCÊ DESPERTA?" size 26 color "#8b0000" xalign 0.5

            for nome in opcoes:
                $ _attr_opcao = FLAVOR_DISCIPLINA_SOCIAL[nome][0]
                $ _pool_opcao = max(1, atributos[_attr_opcao] + disciplinas[nome])
                textbutton "%s  ⚂ %d" % (nome, _pool_opcao):
                    action Return(nome)
                    xalign 0.5
                    text_size 20
                    padding (20, 8)
                    background Solid("#333")
                    hover_background Solid("#555")


label uso_disciplina_social(dificuldade=2):
    python:
        _discs_disponiveis = sorted([d for d in disciplinas if disciplinas[d] > 0], key=lambda d: -disciplinas[d])
        _disc_escolhida = renpy.call_screen("escolha_disciplina", opcoes=_discs_disponiveis)
        _attr_disc, _flavor_disc = FLAVOR_DISCIPLINA_SOCIAL[_disc_escolhida]
        _pool_disciplina = max(1, atributos[_attr_disc] + disciplinas[_disc_escolhida])
        _componentes_disc = [(_attr_disc, atributos[_attr_disc]), (_disc_escolhida, disciplinas[_disc_escolhida])]

    "[_flavor_disc]"

    call rolar_teste(_pool_disciplina, dificuldade, _componentes_disc)

    return _return


# --- Ponto único de rolagem, usado por todos os capítulos ---
# Centraliza dados de Fome, sucessos/críticos e o reroll pago com
# Vontade (regra oficial: 1 Vontade rerola até 3 dados normais que
# falharam; dados de Fome nunca podem ser rerolados).

label rolar_teste(reserva, dificuldade, componentes=None):

    $ jogador_confirmou = renpy.call_screen("confirma_teste", reserva=reserva, fome_atual=fome, componentes=componentes)

    python:
        dados_fome_qtd = min(fome, reserva)
        dados_normais_qtd = max(0, reserva - dados_fome_qtd)
        lista_normais = [random.randint(1, 10) for _ in range(dados_normais_qtd)]
        lista_fome = [random.randint(1, 10) for _ in range(dados_fome_qtd)]
        sucessos = sum(1 for d in lista_normais + lista_fome if d >= 6)

    $ continuar_rolando = True
    while continuar_rolando:
        $ resultado_acao = renpy.call_screen("resultado_teste", lista_normais=lista_normais, lista_fome=lista_fome, sucessos=sucessos, dificuldade=dificuldade)

        if resultado_acao == "rerolar":
            $ vontade_atual -= 1
            python:
                falhas_normais = [i for i, d in enumerate(lista_normais) if d < 6]
                for i in falhas_normais[:3]:
                    lista_normais[i] = random.randint(1, 10)
                sucessos = sum(1 for d in lista_normais + lista_fome if d >= 6)
        else:
            $ continuar_rolando = False

    return sucessos


# ============================================================
# ESCALADA DE CONFLITO E GAME OVER
# ============================================================
# Usado sempre que uma infiltração/confronto falha e a situação
# vira perigo real: lutar, fugir, ou ser capturado (fim de jogo,
# com opção de carregar o último save automático).

init python:

    def carregar_ultimo_save():
        slot = renpy.newest_slot()
        if slot:
            renpy.load(slot)
        else:
            renpy.notify("Nenhum save automático encontrado ainda.")


screen tela_game_over():
    modal True
    zorder 300
    add Solid("#000000ee")

    frame:
        align (0.5, 0.5)
        xsize 750
        padding (40, 40)
        background Solid("#1a1a1a")

        vbox:
            spacing 25
            xalign 0.5

            text "FIM DE JOGO" size 50 color "#ff3333" xalign 0.5
            text "Nem todo Kindred sobrevive à própria arrogância." size 20 color "#ffffff" xalign 0.5

            textbutton "CARREGAR ÚLTIMO SAVE AUTOMÁTICO":
                xalign 0.5
                padding (20, 10)
                background Solid("#4a0000")
                hover_background Solid("#8b0000")
                action Function(carregar_ultimo_save)

            textbutton "IR PARA A TELA DE CARREGAMENTO":
                xalign 0.5
                padding (20, 10)
                background Solid("#333")
                hover_background Solid("#555")
                action ShowMenu("load")

            textbutton "MENU PRINCIPAL":
                xalign 0.5
                padding (20, 10)
                background Solid("#333")
                hover_background Solid("#555")
                action MainMenu()


label conflito_capturado:

    scene black with dissolve

    "Os passos ficam mais altos, as luzes mais brancas, e não importa o quanto você se mova — desta vez, não é rápido o suficiente."

    "Mãos enluvadas prendem uma agulha carregada de sedativo contra o seu pescoço. O mundo desmorona em estática branca antes que você consiga reagir."

    "Quem quer que tenha te encontrado não faz prisioneiros por gentileza — faz por curiosidade. E você não vai gostar do que vem a seguir."

    "FIM DE JOGO"

    call screen tela_game_over

    return


label escalar_conflito(dificuldade=3, motivo="A situação desanda de vez. Vozes gritam, passos se aproximam — não há mais espaço para sutileza."):
    # Chamado quando uma infiltração ou confronto falha e a cena
    # precisa de uma saída real: lutar, fugir, ou ser capturado.
    # Se retornar, a missão continua (com custo). Se não retornar,
    # foi porque o jogo terminou em conflito_capturado.

    "[motivo]"

    $ reserva_lutar, comp_lutar = montar_pool((atributos, "Força"), (habilidades, "Combate Corpo a Corpo"))
    $ reserva_fugir, comp_fugir = montar_pool((atributos, "Destreza"), (habilidades, "Furtividade"))

    menu:
        "O que você faz?"

        "Lutar para sair dessa (Força + Combate Corpo a Corpo)  ⚂ [reserva_lutar]":
            call rolar_teste(reserva_lutar, dificuldade, comp_lutar)

            if _return >= dificuldade:
                $ saude_atual = max(1, saude_atual - 2)
                "Você abre caminho à força bruta, saindo machucado, mas vivo — e, de algum jeito, ainda de posse do que veio buscar."
            else:
                jump conflito_capturado

        "Tentar fugir (Destreza + Furtividade)  ⚂ [reserva_fugir]":
            call rolar_teste(reserva_fugir, dificuldade, comp_fugir)

            if _return >= dificuldade:
                $ fome = min(5, fome + 1)
                $ humanidade = max(0, humanidade - 1)
                "Você escapa por pouco, o pânico raspando contra o que resta do seu controle — mas escapa, e ainda com o que veio buscar."
            else:
                jump conflito_capturado

    return
