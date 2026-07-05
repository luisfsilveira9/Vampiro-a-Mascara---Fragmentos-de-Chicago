# ============================================================
# SISTEMA DE PROGRESSÃO — VAMPIRO A MÁSCARA 5ª EDIÇÃO
# ============================================================
# Implementação simplificada das regras oficiais de criação de
# personagem (Atributos 7/5/3, Habilidades 11/7/4, Disciplinas)
# e da tabela de custos de experiência (XP) do livro básico.
#
# Não implementado nesta versão: Tipo de Predador, Vantagens
# (Vantagens/Defeitos), Antecedentes, Marcos e Convicções.

init python:

    LISTA_ATRIBUTOS = {
        "Físicos": ["Força", "Destreza", "Vigor"],
        "Sociais": ["Carisma", "Manipulação", "Compostura"],
        "Mentais": ["Inteligência", "Raciocínio", "Resolução"],
    }

    LISTA_HABILIDADES = {
        "Físicas": ["Atletismo", "Briga", "Ofício", "Condução", "Armas de Fogo", "Roubo", "Combate Corpo a Corpo", "Furtividade", "Sobrevivência"],
        "Sociais": ["Adestramento", "Etiqueta", "Percepção Social", "Intimidação", "Liderança", "Performance", "Persuasão", "Malandragem", "Lábia"],
        "Mentais": ["Acadêmicos", "Prontidão", "Finanças", "Investigação", "Medicina", "Ocultismo", "Política", "Ciência", "Tecnologia"],
    }

    DISCIPLINAS_POR_CLA = {
        "Brujah": ["Celeridade", "Potência", "Presença"],
        "Malkaviano": ["Auspício", "Dominação", "Ofuscação"],
        "Ventrue": ["Dominação", "Fortitude", "Presença"],
        "Lasombra": ["Dominação", "Potência", "Tenebrosidade"],
        "Toreador": ["Auspício", "Celeridade", "Presença"],
        "Nosferatu": ["Animalismo", "Ofuscação", "Potência"],
    }

    # Nomes dos poderes oficiais de cada nível de Disciplina (1 a 5),
    # usados apenas como referência de flavor na ficha (vale conferir
    # contra o livro-base para nomenclatura exata).
    PODERES_DISCIPLINA = {
        "Potência":     ["Ímpeto / Salto Prodigioso", "Força Prodigiosa", "Alimentação Brutal", "Elixir do Vigor", "Punho de Caim"],
        "Auspício":     ["Sentidos Aguçados / Sentir o Oculto", "Premonição", "Ler a Alma", "Toque Espiritual", "Possessão"],
        "Dominação":    ["Comandar / Nublar a Mente", "Mesmerizar", "A Mente Esquecediça", "Diretriz Submersa", "Manipulação em Massa"],
        "Celeridade":   ["Graça Felina / Reflexos Rápidos", "Agilidade", "Travessia", "Elixir da Elegância", "Vislumbre"],
        "Presença":     ["Temor / Pavor", "Beijo Duradouro", "Olhar Aterrorizante", "Chamado", "Majestade"],
        "Fortitude":    ["Resiliência / Mente Inabalável", "Robustez", "Desafiar a Maldição", "Fortificar a Fachada", "Elixir da Resistência"],
        "Ofuscação":    ["Manto de Sombras / Silêncio da Morte", "Passagem Invisível", "Fantasma na Máquina", "Desaparecer", "Manto do Grupo"],
        "Tenebrosidade": ["Cinzas às Cinzas / Visão do Abismo", "Manto Sombrio", "Precognição Fatal", "Aura de Decadência", "Perspectiva das Sombras"],
        "Animalismo":   ["Vínculo com Fâmulo / Sentir a Besta", "Sussurros Selvagens", "Suculência Animal", "Submergir o Espírito", "Domínio Animal"],
    }

    # Defeito/Maldição de clã: um resumo jogável da fraqueza oficial de
    # cada clã, exibido na ficha e usado como flavor na cena do Abraço.
    DEFEITOS_POR_CLA = {
        "Brujah":    ("Fúria Cega", "Uma raiva latente ferve sob a pele, pronta para explodir ao menor insulto — resistir a Frenesi de Raiva é sempre mais difícil."),
        "Lasombra":  ("Sem Reflexo", "Espelhos, câmeras e qualquer superfície reflexiva não mostram sua imagem — ou a mostram horrivelmente distorcida."),
        "Ventrue":   ("Paladar Restrito", "O paladar aristocrático rejeita a maioria dos mortais; alimentar-se fora do tipo de presa preferido custa Fome extra."),
        "Malkaviano": ("Aflição Derradeira", "Uma forma de loucura permanente acompanha cada Malkaviano, aflorando sob estresse ou Fome alta."),
        "Toreador":  ("Fixação Estética", "Diante de algo genuinamente belo ou horrendo, é preciso vencer a própria natureza para não ficar paralisado em contemplação."),
        "Nosferatu": ("Deformidade Amaldiçoada", "Uma aparência monstruosa torna impossível se passar por humano sem Ofuscação — a Máscara depende inteiramente das sombras."),
    }

    def custo_xp(categoria, nivel_atual):
        base = max(nivel_atual, 1)
        multiplicadores = {
            "atributo": 5,
            "habilidade": 3,
            "disciplina_cla": 5,
            "disciplina_fora": 7,
            "potencia_sangue": 10,
        }
        return base * multiplicadores[categoria]

    def recalcular_derivados():
        saude_estava_cheia = (store.saude_atual >= store.saude_maxima)
        vontade_estava_cheia = (store.vontade_atual >= store.vontade_maxima)

        store.saude_maxima = store.atributos["Vigor"] + 3
        store.vontade_maxima = store.atributos["Resolução"] + store.atributos["Compostura"]

        if saude_estava_cheia or store.saude_atual > store.saude_maxima:
            store.saude_atual = store.saude_maxima
        if vontade_estava_cheia or store.vontade_atual > store.vontade_maxima:
            store.vontade_atual = store.vontade_maxima

    class AjustarDot(Action):
        # Usado na criação de personagem, para distribuir pontos de prioridade
        # (Atributos: 7/5/3, Habilidades: 11/7/4, Disciplinas: 3).
        def __init__(self, dic, chave, delta, minimo, maximo):
            self.dic = dic
            self.chave = chave
            self.delta = delta
            self.minimo = minimo
            self.maximo = maximo

        def get_sensitive(self):
            novo = self.dic[self.chave] + self.delta
            if novo < self.minimo or novo > self.maximo:
                return False
            if self.delta > 0 and store.pontos_restantes <= 0:
                return False
            if self.delta < 0 and store.pontos_restantes >= store.pontos_totais_etapa:
                return False
            return True

        def __call__(self):
            self.dic[self.chave] += self.delta
            store.pontos_restantes -= self.delta
            renpy.restart_interaction()

    class ComprarXP(Action):
        # Usado após a criação, para gastar XP subindo Atributos/Habilidades/Disciplinas.
        def __init__(self, dic, chave, categoria):
            self.dic = dic
            self.chave = chave
            self.categoria = categoria

        def get_sensitive(self):
            nivel = self.dic[self.chave]
            if nivel >= 5:
                return False
            return store.xp_disponivel >= custo_xp(self.categoria, nivel)

        def __call__(self):
            nivel = self.dic[self.chave]
            custo = custo_xp(self.categoria, nivel)
            self.dic[self.chave] = nivel + 1
            store.xp_disponivel -= custo
            recalcular_derivados()
            renpy.restart_interaction()

    class ComprarPotenciaSangue(Action):
        def get_sensitive(self):
            if store.potencia_sangue >= 5:
                return False
            return store.xp_disponivel >= custo_xp("potencia_sangue", store.potencia_sangue)

        def __call__(self):
            custo = custo_xp("potencia_sangue", store.potencia_sangue)
            store.potencia_sangue += 1
            store.xp_disponivel -= custo
            renpy.restart_interaction()

    def calcular_pool_confronto(escolha):
        # Junta Atributo + Habilidade + Disciplina relevante para as cenas
        # de confronto condicionadas ao clã (Capítulos 2 e 4).
        if escolha == "forca":
            return atributos["Força"] + habilidades["Briga"] + disciplinas["Potência"]
        elif escolha == "percepcao":
            return atributos["Raciocínio"] + habilidades["Prontidão"] + disciplinas["Auspício"]
        elif escolha == "comando":
            return atributos["Manipulação"] + habilidades["Liderança"] + disciplinas["Dominação"]
        return 1

    def distribuir_pontos_aleatorio(itens, dic, pontos, minimo, maximo):
        # Preenche uma ficha de teste: zera os itens no mínimo e depois
        # sorteia onde cada ponto extra vai, respeitando o teto de cada um.
        for item in itens:
            dic[item] = minimo
        pontos_restantes_local = pontos
        tentativas = 0
        while pontos_restantes_local > 0 and tentativas < 500:
            item = random.choice(itens)
            if dic[item] < maximo:
                dic[item] += 1
                pontos_restantes_local -= 1
            tentativas += 1

    def gerar_ficha_teste():
        categorias_attr = ["Físicos", "Sociais", "Mentais"]
        random.shuffle(categorias_attr)
        for categoria, pontos in zip(categorias_attr, [7, 5, 3]):
            distribuir_pontos_aleatorio(LISTA_ATRIBUTOS[categoria], atributos, pontos, 1, 4)

        categorias_hab = ["Físicas", "Sociais", "Mentais"]
        random.shuffle(categorias_hab)
        for categoria, pontos in zip(categorias_hab, [11, 7, 4]):
            distribuir_pontos_aleatorio(LISTA_HABILIDADES[categoria], habilidades, pontos, 0, 3)

        distribuir_pontos_aleatorio(DISCIPLINAS_POR_CLA[cla], disciplinas, 3, 0, 3)

        recalcular_derivados()
        store.saude_atual = store.saude_maxima
        store.vontade_atual = store.vontade_maxima


# --- Variáveis padrão da ficha ---

default atributos = {
    "Força": 1, "Destreza": 1, "Vigor": 1,
    "Carisma": 1, "Manipulação": 1, "Compostura": 1,
    "Inteligência": 1, "Raciocínio": 1, "Resolução": 1,
}

default habilidades = {
    "Atletismo": 0, "Briga": 0, "Ofício": 0, "Condução": 0, "Armas de Fogo": 0,
    "Roubo": 0, "Combate Corpo a Corpo": 0, "Furtividade": 0, "Sobrevivência": 0,
    "Adestramento": 0, "Etiqueta": 0, "Percepção Social": 0, "Intimidação": 0,
    "Liderança": 0, "Performance": 0, "Persuasão": 0, "Malandragem": 0, "Lábia": 0,
    "Acadêmicos": 0, "Prontidão": 0, "Finanças": 0, "Investigação": 0, "Medicina": 0,
    "Ocultismo": 0, "Política": 0, "Ciência": 0, "Tecnologia": 0,
}

default disciplinas = {
    "Potência": 0, "Auspício": 0, "Dominação": 0,
    "Celeridade": 0, "Presença": 0, "Fortitude": 0, "Ofuscação": 0,
    "Tenebrosidade": 0, "Animalismo": 0,
}

default potencia_sangue = 1
default saude_maxima = 4
default saude_atual = 4
default vontade_maxima = 2
default vontade_atual = 2

default xp_disponivel = 0
default xp_total_ganho = 0

default pontos_restantes = 0
default pontos_totais_etapa = 0

default prioridade_principal = ""
default prioridade_secundaria = ""
default prioridade_terciaria = ""

default modo_criacao = ""


# --- Tela reutilizável de distribuição de pontos ---

screen distribuir_pontos(titulo, itens, dic, minimo, maximo):
    modal True
    zorder 200
    add Solid("#000000ee")

    frame:
        align (0.5, 0.5)
        xsize 950
        ysize 700
        background Solid("#1a1a1a")
        padding (40, 40)

        vbox:
            spacing 12
            text titulo size 34 color "#8b0000" xalign 0.5
            text "Pontos restantes: [pontos_restantes]" size 24 color "#ffffff" xalign 0.5

            null height 10

            for item in itens:
                hbox:
                    spacing 15
                    text item size 22 color "#ffffff" xsize 320
                    text ("●" * dic[item]) + ("○" * (maximo - dic[item])) size 22 color "#8b0000" xsize 150
                    textbutton "-" action AjustarDot(dic, item, -1, minimo, maximo)
                    textbutton "+" action AjustarDot(dic, item, 1, minimo, maximo)

            null height 20
            textbutton "CONFIRMAR":
                xalign 0.5
                sensitive (pontos_restantes == 0)
                action Return()


# --- Tela de gasto de XP ---

screen tela_experiencia():
    modal True
    zorder 210
    add Solid("#000000ee")

    frame:
        align (0.5, 0.5)
        xsize 1100
        ysize 750
        background Solid("#1a1a1a")
        padding (30, 30)

        vbox:
            spacing 10
            text "MELHORIAS (XP)" size 36 color "#8b0000" xalign 0.5
            text "XP Disponível: [xp_disponivel]" size 24 color "#ffcc00" xalign 0.5

            viewport:
                xsize 1040
                ysize 560
                scrollbars "vertical"
                mousewheel True
                draggable True

                vbox:
                    spacing 6

                    text "ATRIBUTOS" size 26 color "#8b0000"
                    for categoria in ["Físicos", "Sociais", "Mentais"]:
                        for nome in LISTA_ATRIBUTOS[categoria]:
                            hbox:
                                spacing 10
                                text nome size 18 color "#ffffff" xsize 260
                                text ("●" * atributos[nome]) + ("○" * (5 - atributos[nome])) size 18 color "#8b0000" xsize 120
                                text ("Custo: %d" % custo_xp("atributo", atributos[nome])) size 16 color "#aaaaaa" xsize 100
                                textbutton "+" action ComprarXP(atributos, nome, "atributo")

                    null height 15
                    text "HABILIDADES" size 26 color "#8b0000"
                    for categoria in ["Físicas", "Sociais", "Mentais"]:
                        for nome in LISTA_HABILIDADES[categoria]:
                            hbox:
                                spacing 10
                                text nome size 18 color "#ffffff" xsize 260
                                text ("●" * habilidades[nome]) + ("○" * (5 - habilidades[nome])) size 18 color "#8b0000" xsize 120
                                text ("Custo: %d" % custo_xp("habilidade", habilidades[nome])) size 16 color "#aaaaaa" xsize 100
                                textbutton "+" action ComprarXP(habilidades, nome, "habilidade")

                    null height 15
                    text "DISCIPLINAS" size 26 color "#8b0000"
                    for nome in disciplinas:
                        $ categoria_disc = "disciplina_cla" if nome in DISCIPLINAS_POR_CLA.get(cla, []) else "disciplina_fora"
                        hbox:
                            spacing 10
                            text nome size 18 color "#ffffff" xsize 260
                            text ("●" * disciplinas[nome]) + ("○" * (5 - disciplinas[nome])) size 18 color "#8b0000" xsize 120
                            text ("Custo: %d" % custo_xp(categoria_disc, disciplinas[nome])) size 16 color "#aaaaaa" xsize 100
                            textbutton "+" action ComprarXP(disciplinas, nome, categoria_disc)

                    null height 15
                    text "OUTROS" size 26 color "#8b0000"
                    hbox:
                        spacing 10
                        text "Potência de Sangue" size 18 color "#ffffff" xsize 260
                        text ("●" * potencia_sangue) + ("○" * (5 - potencia_sangue)) size 18 color "#8b0000" xsize 120
                        text ("Custo: %d" % custo_xp("potencia_sangue", potencia_sangue)) size 16 color "#aaaaaa" xsize 100
                        textbutton "+" action ComprarPotenciaSangue()

            textbutton "FECHAR":
                xalign 0.5
                action Hide("tela_experiencia")


# --- Ficha de Personagem completa ---

screen ficha_personagem():
    modal True
    zorder 200
    add Solid("#000000ee")

    frame:
        align (0.5, 0.5)
        xsize 1150
        ysize 780
        background Solid("#1a1a1a")
        padding (35, 35)

        vbox:
            spacing 15
            text "FICHA DE PERSONAGEM" size 42 color "#8b0000" xalign 0.5

            hbox:
                spacing 60
                text "NOME: [nome_jogador]" size 20 color "#ffffff"
                text "CLÃ: [cla]" size 20 color "#ffffff"
                text "FACÇÃO: [faccao]" size 20 color "#ffffff"

            $ nome_defeito, descricao_defeito = DEFEITOS_POR_CLA.get(cla, ("", ""))
            if nome_defeito:
                text "DEFEITO DE CLÃ: [nome_defeito]" size 18 color "#ff6666" italic True
                text "[descricao_defeito]" size 15 color "#cccccc"

            hbox:
                spacing 40
                text "FOME: [fome]" size 20 color "#ff3333"
                text "HUMANIDADE: [humanidade]" size 20 color "#33ff33"
                text "VONTADE: [vontade_atual]/[vontade_maxima]" size 20 color "#ffffff"
                text "SAÚDE: [saude_atual]/[saude_maxima]" size 20 color "#ffffff"
                text "P. SANGUE: [potencia_sangue]" size 20 color "#ffffff"
                text "XP: [xp_disponivel]" size 20 color "#ffcc00"

            viewport:
                xsize 1080
                ysize 480
                scrollbars "vertical"
                mousewheel True
                draggable True

                vbox:
                    spacing 10

                    text "ATRIBUTOS" size 28 bold True color "#8b0000"
                    for categoria in ["Físicos", "Sociais", "Mentais"]:
                        hbox:
                            spacing 30
                            for nome in LISTA_ATRIBUTOS[categoria]:
                                text (nome + ": " + "●" * atributos[nome] + "○" * (5 - atributos[nome])) size 18 color "#ffffff"

                    null height 10
                    text "HABILIDADES" size 28 bold True color "#8b0000"
                    $ habilidades_treinadas = {k: v for k, v in habilidades.items() if v > 0}
                    if habilidades_treinadas:
                        for nome, valor in sorted(habilidades_treinadas.items()):
                            text (nome + ": " + "●" * valor + "○" * (5 - valor)) size 18 color "#ffffff"
                    else:
                        text "Nenhuma habilidade treinada" size 18 italic True color "#aaaaaa"

                    null height 10
                    text "DISCIPLINAS" size 28 bold True color "#8b0000"
                    $ disciplinas_ativas = {k: v for k, v in disciplinas.items() if v > 0}
                    if disciplinas_ativas:
                        for nome, valor in disciplinas_ativas.items():
                            text (nome + ": " + "●" * valor + "○" * (5 - valor) + "  —  " + PODERES_DISCIPLINA[nome][valor - 1]) size 18 color "#ffffff"
                    else:
                        text "Nenhuma Disciplina Desperta" size 18 italic True color "#aaaaaa"

            hbox:
                spacing 40
                xalign 0.5

                textbutton "MELHORAR (XP)":
                    action Show("tela_experiencia")
                    padding (20, 10)
                    background Solid("#4a0000")
                    hover_background Solid("#8b0000")

                textbutton "VOLTAR AO JOGO":
                    action Hide("ficha_personagem")
                    padding (20, 10)
                    background Solid("#4a0000")
                    hover_background Solid("#8b0000")


# --- Fluxo de criação de personagem (chamado logo após a escolha de clã) ---

label criacao_personagem:

    menu:
        "Como você quer montar a ficha?"

        "Criar manualmente (distribuir pontos você mesmo)":
            $ modo_criacao = "manual"

        "Ficha rápida de teste (aleatória, pronta pro walkthrough)":
            $ modo_criacao = "teste"

    if modo_criacao == "teste":

        $ gerar_ficha_teste()

        "Uma ficha de teste foi gerada automaticamente: atributos, habilidades e disciplinas sorteados dentro das regras oficiais. Pronta pra jogar."

        return

    "◆ ATRIBUTOS ◆"

    menu:
        "Escolha sua prioridade PRINCIPAL de Atributos (7 pontos):"
        "Físicos (Força, Destreza, Vigor)":
            $ prioridade_principal = "Físicos"
        "Sociais (Carisma, Manipulação, Compostura)":
            $ prioridade_principal = "Sociais"
        "Mentais (Inteligência, Raciocínio, Resolução)":
            $ prioridade_principal = "Mentais"

    $ restantes_attr = [c for c in ["Físicos", "Sociais", "Mentais"] if c != prioridade_principal]
    $ opcao_attr_a = restantes_attr[0]
    $ opcao_attr_b = restantes_attr[1]

    menu:
        "Escolha sua prioridade SECUNDÁRIA de Atributos (5 pontos):"
        "[opcao_attr_a]":
            $ prioridade_secundaria = opcao_attr_a
        "[opcao_attr_b]":
            $ prioridade_secundaria = opcao_attr_b

    $ prioridade_terciaria = [c for c in restantes_attr if c != prioridade_secundaria][0]

    "Prioridade Principal: [prioridade_principal] (7 pontos)\nPrioridade Secundária: [prioridade_secundaria] (5 pontos)\nPrioridade Terciária: [prioridade_terciaria] (3 pontos)"

    $ pontos_restantes = 7
    $ pontos_totais_etapa = 7
    call screen distribuir_pontos("ATRIBUTOS: " + prioridade_principal, LISTA_ATRIBUTOS[prioridade_principal], atributos, 1, 4)

    $ pontos_restantes = 5
    $ pontos_totais_etapa = 5
    call screen distribuir_pontos("ATRIBUTOS: " + prioridade_secundaria, LISTA_ATRIBUTOS[prioridade_secundaria], atributos, 1, 4)

    $ pontos_restantes = 3
    $ pontos_totais_etapa = 3
    call screen distribuir_pontos("ATRIBUTOS: " + prioridade_terciaria, LISTA_ATRIBUTOS[prioridade_terciaria], atributos, 1, 4)

    $ recalcular_derivados()
    $ saude_atual = saude_maxima
    $ vontade_atual = vontade_maxima

    "◆ HABILIDADES ◆"

    menu:
        "Escolha sua prioridade PRINCIPAL de Habilidades (11 pontos):"
        "Físicas":
            $ prioridade_principal_hab = "Físicas"
        "Sociais":
            $ prioridade_principal_hab = "Sociais"
        "Mentais":
            $ prioridade_principal_hab = "Mentais"

    $ restantes_hab = [c for c in ["Físicas", "Sociais", "Mentais"] if c != prioridade_principal_hab]
    $ opcao_hab_a = restantes_hab[0]
    $ opcao_hab_b = restantes_hab[1]

    menu:
        "Escolha sua prioridade SECUNDÁRIA de Habilidades (7 pontos):"
        "[opcao_hab_a]":
            $ prioridade_secundaria_hab = opcao_hab_a
        "[opcao_hab_b]":
            $ prioridade_secundaria_hab = opcao_hab_b

    $ prioridade_terciaria_hab = [c for c in restantes_hab if c != prioridade_secundaria_hab][0]

    $ pontos_restantes = 11
    $ pontos_totais_etapa = 11
    call screen distribuir_pontos("HABILIDADES: " + prioridade_principal_hab, LISTA_HABILIDADES[prioridade_principal_hab], habilidades, 0, 3)

    $ pontos_restantes = 7
    $ pontos_totais_etapa = 7
    call screen distribuir_pontos("HABILIDADES: " + prioridade_secundaria_hab, LISTA_HABILIDADES[prioridade_secundaria_hab], habilidades, 0, 3)

    $ pontos_restantes = 4
    $ pontos_totais_etapa = 4
    call screen distribuir_pontos("HABILIDADES: " + prioridade_terciaria_hab, LISTA_HABILIDADES[prioridade_terciaria_hab], habilidades, 0, 3)

    "◆ DISCIPLINAS ◆"

    "O Abraço trouxe mais que fome — trouxe poder. Seu Clã concede acesso a três Disciplinas. Distribua 3 pontos entre elas."

    $ pontos_restantes = 3
    $ pontos_totais_etapa = 3
    call screen distribuir_pontos("DISCIPLINAS DE " + cla.upper(), DISCIPLINAS_POR_CLA[cla], disciplinas, 0, 3)

    return
