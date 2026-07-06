# ============================================================
# ATO I — AS TRÊS ROTAS DE INVESTIGAÇÃO
# ============================================================

define jax = Character("Jax", color="#c0762c")
define madamek = Character("Madame K", color="#8b7d6b")
define blink = Character("Blink", color="#d63384")
define vargas = Character("Xerife Vargas", color="#a68a3c")
define arthur = Character("Arthur", color="#5f9ea0")
define nia = Character("Nia", color="#7a6a53")
define sasha = Character("Sasha", color="#6699cc")
define veronica = Character("Veronica Vance", color="#cc9966")
define abernathy = Character("Sr. Abernathy", color="#8a8a5c")
define jimmy = Character("\"Mãos-de-Graxa\" Jimmy", color="#8b5a2b")

# --- Sprites dos personagens deste arquivo ---
# A arte antiga de Madame K (MadameK.png) não está mais na pasta e nenhuma
# substituta foi gerada; cai no placeholder colorido até chegar arte nova.
# O resto usa um placeholder sólido na cor do personagem, sem arte ainda.
image madamek = retrato("MadameK.png", "Madame K", "neutro", "#8b7d6b", 1080, 1080)
image jax = Solid("#c0762c", xsize=500, ysize=850)
image blink = Solid("#d63384", xsize=500, ysize=850)
image vargas = Solid("#a68a3c", xsize=500, ysize=850)
image arthur = Solid("#5f9ea0", xsize=500, ysize=850)
image nia = Solid("#7a6a53", xsize=500, ysize=850)
image sasha = Solid("#6699cc", xsize=500, ysize=850)
image veronica = Solid("#cc9966", xsize=500, ysize=850)
image abernathy = Solid("#8a8a5c", xsize=500, ysize=850)
image jimmy = Solid("#8b5a2b", xsize=500, ysize=850)

default veronica_estado = ""
default alvo_laranja = ""
default aliado_arthur = False
default aliada_nia = False
default aliada_sasha = False
default isadora_intimidade_feita = False

label rotas_ato1:
    if rota_investigacao == "docas":
        jump ato1_docas
    elif rota_investigacao == "leilao":
        jump ato1_leilao
    else:
        jump ato1_rastreio

# --- ROTA A: DOCAS DE CONTRABANDO ---
label ato1_docas:
    scene black with dissolve
    show jax at center with dissolve
    "As docas sul. Chove fino. Você não pode invadir sozinho. Você encontra Jax, um traficante de armas."
    
    jax "Querem entrar no galpão da Inquisição? Custa um favor. Explodam um contêiner rival pra mim e eu dou o mapa."
    
    menu:
        "Aceitar e explodir o contêiner rival":
            $ favores_jax = True
            $ diff_docas = 2
            "Jax entrega um mapa perfeito. Mas você irritou uma facção local."
        "Recusar e ir às cegas":
            $ favores_jax = False
            $ diff_docas = 3
            "Jax te dá apenas um esboço grosseiro."

    "Os cães e mercenários rondam os galpões. Teste de Destreza + Furtividade (Dificuldade [diff_docas])."
    $ res_furt, comp_furt = montar_pool((atributos, "Destreza"), (habilidades, "Furtividade"))
    call rolar_teste(res_furt, diff_docas, comp_furt)

    if _return >= diff_docas:
        "Você quebra pescoços silenciosamente, movendo-se como fumaça até o escritório central."
    else:
        "Um cão late. Alarmes soam. Mercenários abrem fogo."
        $ saude_atual -= 1
        call escalar_conflito(3, "O pátio inteiro está atirando. Abra caminho à força.")

    $ res_luta, comp_luta = montar_pool((atributos, "Força"), (habilidades, "Briga"))
    $ res_terror, comp_terror = montar_pool((atributos, "Carisma"), (habilidades, "Intimidação"), (disciplinas, "Potência"))

    "No escritório, o Chefe dos mercenários aponta uma escopeta de fósforo branco para você. O que você faz?"
    menu:
        "Lutar  ⚂ [res_luta]":
            $ res_chefe, comp_chefe = res_luta, comp_luta
        "Aterrorizar  ⚂ [res_terror]":
            $ res_chefe, comp_chefe = res_terror, comp_terror

    call rolar_teste(res_chefe, 3, comp_chefe)
    if _return >= 3:
        "O chefe cai de joelhos e aponta para o cofre. Dentro, recibos das armas UV assinados por 'Corvo Dourado Holdings'."
        $ empresa_suspeita = "Corvo Dourado Holdings"
    else:
        "Ele dispara. O fósforo queima sua pele como ácido."
        $ saude_atual -= 2
        call escalar_conflito(4, "Ele pediu reforços pelo rádio. Pegue os papéis no cofre e fuja antes de virar cinzas!")
        $ empresa_suspeita = "Corvo Dourado Holdings"

    $ xp_disponivel += 2
    $ xp_total_ganho += 2
    "Sobreviver às docas armado só com os próprios reflexos vale experiência. (+2 XP)"

    jump beco_sem_saida

# --- ROTA B: O LEILÃO DO CORVO DE OURO ---
label ato1_leilao:
    scene bg_clube with dissolve
    show madamek at center with dissolve
    "O Elysium. Refúgio da alta sociedade vampírica. Para entrar, você procurou Madame K, a forjadora Nosferatu."

    madamek "Forjo seu convite VIP, novato. Mas quero um favor: humilhe publicamente um lacaio Ventrue que me irritou hoje."
    
    menu:
        "Aceitar e criar um inimigo Ventrue":
            $ favor_madamek = True
            $ diff_leilao = 2
            "Você recebe roupas impecáveis e um nome falso à prova de falhas."
        "Recusar e usar uma identidade fraca":
            $ favor_madamek = False
            $ diff_leilao = 4
            "Sua entrada será perigosa e qualquer olhar das Harpias pode te expor."

    "O salão brilha com lustres de cristal. Você precisa navegar pelas Harpias. Manipulação + Etiqueta (Dificuldade [diff_leilao])."
    $ res_etiq, comp_etiq = montar_pool((atributos, "Manipulação"), (habilidades, "Etiqueta"))
    call rolar_teste(res_etiq, diff_leilao, comp_etiq)

    if _return >= diff_leilao:
        "Você flutua pelo salão perfeitamente. Ninguém suspeita."
    else:
        "Você usa o garfo de sobremesa errado, metafórica ou literalmente. As Harpias marcam seu rosto."
        $ camarilla_marcado = True

    "Você acha o leiloeiro assistente. Ele tem os registros do 'Corvo de Ouro'. Isole-o na sacada: Carisma + Lábia (Dificuldade 3)."
    $ res_labia, comp_labia = montar_pool((atributos, "Carisma"), (habilidades, "Lábia"))
    call rolar_teste(res_labia, 3, comp_labia)

    if _return >= 3:
        "Fascinado por você, ele entrega a chave do escritório. O registro lista o doador como 'Corvo Dourado Holdings'."
        $ empresa_suspeita = "Corvo Dourado Holdings"
    else:
        "Ele percebe a armadilha e ameaça gritar pelos seguranças do Elysium."
        call escalar_conflito(3, "Quebrar a paz do Elysium é morte certa. Você precisa apagá-lo rápido e roubar as chaves à força.")
        $ empresa_suspeita = "Corvo Dourado Holdings"

    $ xp_disponivel += 2
    $ xp_total_ganho += 2
    "Sobreviver ao Elysium sem quebrar a Máscara de vez também é uma forma de perícia. (+2 XP)"

    jump beco_sem_saida

# --- ROTA C: A INVASÃO DIGITAL ---
label ato1_rastreio:
    scene black with dissolve
    show blink at center with dissolve
    "A Inquisição tem firewalls brutais. Você visita Blink, uma hacker Malkaviana."
    
    blink "Eu dou o software militar. Mas você planta esse vírus na rede dos Anarquistas do Rook pra mim. Sim?"
    
    menu:
        "Aceitar e trair a rede de Rook":
            $ favor_blink = True
            $ diff_hack = 3
            "Software perfeito. Mas se Rook descobrir, você perde seu teto."
        "Recusar a chantagem":
            $ favor_blink = False
            $ diff_hack = 5
            "Ela te dá um software instável e cheio de bugs."

    "Para conectar, você precisa acessar os cabos sob o distrito financeiro, vigiados por drones da Inquisição. Raciocínio + Prontidão."
    $ res_pront, comp_pront = montar_pool((atributos, "Raciocínio"), (habilidades, "Prontidão"))
    call rolar_teste(res_pront, 3, comp_pront)

    if _return >= 3:
        "Você desvia dos escaneamentos térmicos sem problemas."
    else:
        "Um drone atira um feixe incandescente na sua direção."
        $ saude_atual -= 1
        "Você quebra a câmera do drone, mas sabe que patrulhas físicas vêm aí."

    "Conectado ao painel. Cães de guarda digitais tentam te rastrear. Inteligência + Tecnologia (Dificuldade [diff_hack])."
    $ res_tech, comp_tech = montar_pool((atributos, "Inteligência"), (habilidades, "Tecnologia"))
    call rolar_teste(res_tech, diff_hack, comp_tech)

    if _return >= diff_hack:
        "A tela fica verde. Você puxa os dados das Ilhas Cayman. A conta pertence a 'Corvo Dourado Holdings'."
        $ empresa_suspeita = "Corvo Dourado Holdings"
    else:
        "O firewall reverte a conexão. Passos de coturnos militares ecoam no túnel. A Inquisição te achou."
        call escalar_conflito(4, "Você é forçado a arrancar o disco rígido do painel à força bruta enquanto foge sob fogo cruzado.")
        $ empresa_suspeita = "Corvo Dourado Holdings"

    $ xp_disponivel += 2
    $ xp_total_ganho += 2
    "Burlar a segurança digital da Inquisição e sair inteiro também conta como experiência. (+2 XP)"

    jump beco_sem_saida


# --- CONVERGÊNCIA: A SALA DE GUERRA (O BECO SEM SAÍDA) ---
label beco_sem_saida:
    scene black with fade
    show isadora imponente at left with dissolve
    show rook intimacao at right with dissolve
    "Você retorna ao armazém de Rook com a chuva lavando o sangue das suas mãos. Quer você tenha vindo das docas cheirando a pólvora, do leilão com gosto de champanhe no paladar, ou dos esgotos com os olhos ardendo das telas de computador, o resultado que você joga na mesa de Rook é o mesmo."

    isadora "\"Corvo Dourado Holdings\"."

    rook "(Ri, um som amargo e sem humor) Vocês arriscaram o pescoço, quase quebraram a Máscara, e voltaram com um fantasma. Corvo Dourado é uma casca corporativa. Não tem rosto, não tem CPF. É um buraco negro jurídico sediado nas Ilhas Cayman."

    isadora "Mas buracos negros puxam as coisas para dentro. Alguém assina os cheques. Alguém contrata os mercenários."

    rook "Sim, mas são \"laranjas\". Mortais ou carniçais pagos para não fazer perguntas. Leva tempo para rastrear um laranja. Vão dormir. O sol já está nascendo. Sobrevivemos hoje, amanhã caçamos os laranjas."

    # --- O DESPERTAR: A MALDIÇÃO DO SANGUE ---
    scene bg_refugio with dissolve
    "A noite cai sobre Chicago, mas você acorda sentindo que algo foi arrancado de você. A Fome não é apenas um vazio no estômago; ela amplifica a maldição ancestral do seu Clã. O mundo parece distorcido."

    "Antes de sair para a rua, a sua Besta te cobra o pedágio por existir."

    if cla == "Brujah":
        "Um Anarquista esbarra no seu ombro no armazém e murmura um insulto. Sua visão fica vermelha. Você precisa lutar contra o Frenesi de Raiva para não arrancar a cabeça do seu aliado."
    elif cla == "Lasombra":
        "Você olha para uma poça de água suja. Não há reflexo. As sombras do armazém parecem se esticar na sua direção, sussurrando as falhas do seu passado mortal. A paranoia tenta te dominar."
    elif cla == "Ventrue":
        "Rook te oferece uma bolsa de sangue roubada de um morador de rua. O cheiro te dá náuseas violentas. A Besta exige sangue de qualidade, sangue de alguém com poder, deixando você fraco até conseguir o que quer."
    elif cla == "Malkaviano":
        "A estática no seu ouvido vira uma voz clara. Ela narra a sua própria morte repetidas vezes. Você precisa focar na realidade para distinguir o que é intuição e o que é pura esquizofrenia."
    elif cla == "Toreador":
        "Um grafite na parede do armazém — uma arte crua e dolorosamente bela de um anjo chorando sangue — te hipnotiza. A feiura do mundo ao redor te causa dor física, e você precisa se forçar a desviar o olhar para agir."
    else:
        "Seus ossos estalam em um novo espasmo de mutação. A dor é excruciante. Você percebe que um mortal passava na rua e quase viu seu rosto distorcido na fresta da porta. Você precisa se esconder."

    "Teste de Maldição de Clã: Resolução + Compostura (Dificuldade 2)."
    $ res_maldicao, comp_maldicao = montar_pool((atributos, "Resolução"), (atributos, "Compostura"))
    call rolar_teste(res_maldicao, 2, comp_maldicao)

    if _return < 2:
        "A Besta ganha esta rodada. A exaustão mental de conter o que restou dela te custa caro."
        $ vontade_atual = max(0, vontade_atual - 1)
    else:
        "Você prende a Besta de volta na jaula, ao menos por enquanto."

    # --- A CONSEQUÊNCIA: O OLHO DA CAMARILLA ---
    if camarilla_marcado:
        scene bg_beco with fade
        "Você limpa o suor frio do rosto e sai para os becos molhados. Mas você foi descuidado ontem — a Máscara rachou, e a cidade já sabe o seu rosto."

        "Um carro preto e blindado bloqueia a saída do beco. Os faróis cegam você. Um homem desce. Ele veste um sobretudo de couro. Seus olhos são amarelos como os de um lobo. É Vargas, o Xerife Gangrel da Camarilla."

        show vargas at center with dissolve

        vargas "(Voz que soa como cascalho sendo moído) O cria de Isadora. Me disseram que você era barulhento. Ontem à noite, mortais sussurraram sobre presas e olhos brilhantes. O Príncipe Jackson está limpando a cidade da escória de Lodin, e você está sujando o tapete dele."

        "Vargas encosta você na parede de tijolos com uma força que faria um caminhão parecer leve. Ele não quer te matar. Ele quer te aterrorizar."

        vargas "Considere isso um aviso de cortesia. Se eu ouvir seu nome de novo em um relatório de violação da Máscara, eu não venho conversar. Eu venho com fogo."

        "As rotas sociais estarão vigiadas esta noite. Qualquer passo em falso vai trazer a ira do Xerife Vargas atrás de você outra vez."
    else:
        scene bg_refugio with fade
        "A noite começa em silêncio, ao menos. Seja lá o que a Camarilla saiba sobre a cidade, ainda não sabe o seu nome."

    jump atmosfera_chicago


# ============================================================
# TRANSIÇÃO: A ATMOSFERA DE CHICAGO
# ============================================================
label atmosfera_chicago:
    scene black with fade

    "Chicago não é uma cidade. É um cemitério vertical com luzes de neon."

    "O vento que sopra do Lago Michigan corta como vidro quebrado. A chuva fina não lava a sujeira dos becos; ela apenas mistura o cheiro de ozônio, escapamento de carros e o suor frio do medo que paira no ar."

    "Desde a morte do antigo Príncipe, a tensão é palpável. Você pode sentir isso na sua pele morta. Os mortais andam mais apressados. As sombras entre os arranha-céus parecem mais densas, escondendo coisas que agora você sabe que existem."

    "A Segunda Inquisição ronda essas ruas. Caminhonetes pretas sem placa dobram as esquinas devagar. Câmeras com lentes térmicas piscam nos semáforos. Você não é mais o topo da cadeia alimentar. Você é a caça."

    "Você puxa a gola do casaco. A água da chuva escorre pelo seu rosto, mas você não sente frio. Seu corpo é um cadáver animado por magia e maldição, e a única coisa que te aquece é a fornalha da Besta no seu estômago, exigindo ser alimentada."

    menu:
        "Como você caminha por essas ruas?"

        "De cabeça erguida. Eu sou o predador aqui.":
            "Você ajusta a postura. A chuva bate nos seus ombros, mas seus olhos brilham com uma arrogância silenciosa. Os mortais desviam do seu caminho por puro instinto animal."

        "Nas sombras. Cauteloso e invisível.":
            "Você se encolhe contra as paredes de tijolos, evitando os postes de luz. A paranoia é sua melhor amiga agora. Quem não é visto, não é queimado."

    jump noite_de_caca


# ============================================================
# FASE 1: A CAÇADA E A TEIA — CONSTRUINDO SUA REDE DE APOIO
# ============================================================
label noite_de_caca:
    scene black with fade
    "Você tem Fome e precisa de pistas sobre os \"laranjas\" da Corvo Dourado Holdings. Você vai passar a noite rondando Chicago, matando dois coelhos com uma cajadada só. O local que você escolher para caçar vai ditar as amizades que fará e as pistas que vai encontrar."

    menu:
        "O Parque Universitário (foco mental — alvos fáceis, vigilância alta)":
            jump caca_campus
        "Os Trilhos Abandonados da Zona Sul (foco físico — violência atrai violência)":
            jump caca_trilhos
        "O Galpão de Arte Underground (foco social — o playground dos Toreador)":
            jump caca_westloop
        "Voltar ao armazém — Isadora ainda está acordada" if not isadora_intimidade_feita:
            jump isadora_intimidade


# ============================================================
# CENA OPCIONAL: A INTIMIDADE COM O CRIADOR
# ============================================================
# Não afeta rotas, pistas ou dificuldade — existe só para aprofundar
# o vínculo entre os dois antes que a noite recomece.
label isadora_intimidade:
    scene bg_refugio with dissolve
    show isadora pensativa at center with dissolve

    "A fogueira improvisada em um tambor de óleo projeta sombras dançantes nas paredes do armazém. Longe dos Anarquistas que discutem do outro lado do galpão, Isadora está de pé, observando a chuva cair por uma janela quebrada."

    "Ela parece exausta, mas a beleza dela é estonteante e imutável — um quadro renascentista perdido em um mundo de concreto e ferrugem. O cheiro do perfume dela, sândalo e poeira de livros antigos com um toque indescritível de sangue por baixo, atrai você para mais perto antes que a razão opine."

    "Você se aproxima silenciosamente."

    menu:
        "Parar ao lado dela, ombro a ombro, olhando a chuva":
            "Você não diz nada no início. Apenas compartilha o silêncio. Isadora não vira o rosto, mas a respiração dela — um mero hábito, não uma necessidade — falha por um milissegundo. Ela nota sua presença."

        "Ficar de frente para ela, invadindo seu espaço pessoal":
            "Você dá a volta e se coloca entre ela e a janela. Os olhos escuros dela sobem para encontrar os seus. Há perigo nessa proximidade, mas também uma atração gravitacional inegável."

    isadora "(Voz baixa, rouca) Chicago costumava ser linda à noite. Agora... só consigo ver uma armadilha se fechando."

    "Ela suspira, cruzando os braços. A pose impenetrável dela racha por um segundo."

    p "Por que eu, Isadora?"

    "A pergunta sai da sua boca antes que você possa contê-la."

    isadora "O quê?"

    p "Por que me escolheu? Naquele beco. Naquela noite. Chicago tem milhões de pessoas. Por que me dar o Abraço? Por que me arrastar para esse inferno?"

    "Isadora Vane, uma criatura que já caminhou pela Terra por séculos, desvia o olhar. O silêncio se estende. Você pode sentir o peso do vínculo de sangue que conecta vocês vibrando no ar."

    isadora "Você acha que foi um acidente?"

    "Ela dá um passo na sua direção. A proximidade faz sua pele formigar."

    isadora "Eu observei você por semanas antes de decidir."

    isadora "Eu vi como você lutava no seu dia a dia. Vi a raiva nos seus olhos quando as coisas davam errado, e a resiliência absurda de se levantar no dia seguinte. Você tinha... uma faísca. O mundo estava te matando aos poucos, e eu não suportei ver esse fogo se apagar no meio da mediocridade mortal."

    show isadora sorrindo at center with dissolve
    "Ela levanta a mão, os dedos frios e pálidos roçando levemente a linha do seu maxilar."

    isadora "Eu te dei a eternidade. E sim, te dei a Fome e o inferno junto. Mas eu te dei poder. Nunca me peça desculpas por isso. E nunca duvide de por que eu te quis ao meu lado."

    menu:
        "Encostar o rosto na mão dela, aceitando o vínculo":
            "Você fecha os olhos por um segundo. A pele dela é fria como mármore, mas traz um conforto sombrio. Isadora sorri levemente, um sorriso triste e possessivo. Vocês dois estão ligados para sempre, e por um instante isso não parece uma sentença — parece um lar."
            $ confianca_isadora += 1

        "Dar um passo para trás, mantendo a independência":
            show isadora imponente at center with dissolve
            "Você recua. Não por repulsa, mas por autopreservação. Isadora abaixa a mão lentamente. Ela respeita o seu espaço, percebendo que o cria dela tem vontade própria. O olhar dela se torna analítico, misturando aprovação e cautela."

    isadora "Vá. Faça o que tem que ser feito esta noite. Mas volte inteiro para mim."

    $ isadora_intimidade_feita = True

    jump noite_de_caca


label caca_campus:
    scene black with fade
    show arthur at center with dissolve
    "Estudantes estressados caminham sozinhos essa hora da noite — alvos fáceis, mas a vigilância do campus é implacável. Entre eles, você encontra Arthur, um carniçal leal à Camarilla: um humano que bebe do Sangue de algum Kindred e, em troca, acredita de corpo e alma que a ordem do Príncipe Jackson é a única coisa entre Chicago e o caos da Inquisição."

    arthur "Vocês, cria nova, não entendem. Sem o Príncipe, sem as leis, é só a Besta comendo a Besta até não sobrar nada. Alguém precisa manter a ordem."

    "Ele tem informações internas do sistema — se você souber como puxar. Como você lida com Arthur?"

    $ pool_seduzir, comp_seduzir = montar_pool((atributos, "Carisma"), (habilidades, "Persuasão"))
    $ pool_ameacar, comp_ameacar = montar_pool((atributos, "Manipulação"), (habilidades, "Intimidação"))
    $ pool_convencer, comp_convencer = montar_pool((atributos, "Inteligência"), (habilidades, "Política"))

    menu:
        "Seduzi-lo, baixando as defesas dele aos poucos  ⚂ [pool_seduzir]":
            call rolar_teste(pool_seduzir, 2, comp_seduzir)
            $ sucesso_arthur = _return >= 2
            if sucesso_arthur:
                "Ele relaxa, lisonjeado pela atenção. A conversa desliza para lugares que ele não pretendia revelar."
            else:
                "Ele gosta da conversa, mas mantém a guarda no fundo dos olhos — carniçais leais não confiam fácil."

        "Ameaçá-lo, deixando claro o que acontece se ele mentir  ⚂ [pool_ameacar]":
            call rolar_teste(pool_ameacar, 2, comp_ameacar)
            $ camarilla_marcado = True
            $ sucesso_arthur = _return >= 2
            if sucesso_arthur:
                "O medo funciona rápido. Arthur fala mais do que gostaria, os olhos baixos."
            else:
                "Ele se fecha feito ostra. Ameaçar o cão de guarda de outra pessoa raramente é sutil, e alguém decerto vai ouvir falar disso."

        "Debater política com ele, tratando-o como um igual capaz de argumentar  ⚂ [pool_convencer]":
            call rolar_teste(pool_convencer, 2, comp_convencer)
            $ sucesso_arthur = _return >= 2
            if sucesso_arthur:
                "Ele passa a te respeitar mesmo discordando de você — e gente que respeita fala mais do que gente que teme."
            else:
                "Ele discorda de tudo o que você diz, mas ao menos continua falando."

        "Usar um poder do Sangue" if any(disciplinas[_d] > 0 for _d in disciplinas):
            call uso_disciplina_social(2)
            $ sucesso_arthur = _return >= 2

    if sucesso_arthur:
        $ aliado_arthur = True
        arthur "Você é diferente. Talvez a gente possa se ajudar de novo, no futuro."
        "Arthur se torna uma fonte de informações internas do sistema — e menciona, quase de passagem, ter visto movimentações bancárias suspeitas sendo validadas por um contador chamado Sr. Abernathy, que sempre janta tarde em um restaurante de luxo na Magnificent Mile."
    else:
        "Arthur não confia em você o bastante para virar um aliado, mas ainda deixa escapar um nome: Sr. Abernathy, um contador que valida movimentações bancárias suspeitas e sempre janta tarde em um restaurante de luxo na Magnificent Mile."

    $ alvo_laranja = "abernathy"
    $ fome = 0

    if camarilla_marcado:
        "Se você fez barulho ou deixou marcas, sabe que alguém, em algum lugar, está anotando."

    $ xp_disponivel += 2
    $ xp_total_ganho += 2
    "Tecer uma rede de contatos em Chicago também é experiência acumulada. (+2 XP)"

    jump fase2_interrogatorio


label caca_trilhos:
    scene black with fade
    show nia at center with dissolve
    "Os trilhos abandonados da Zona Sul são acampamentos de sem-teto, gangues e traficantes menores. Violência atrai violência aqui. Você esbarra em Nia, uma Sangue-Ralo — uma vampira de geração tão alta que quase não tem poderes, rejeitada por todos. Ela odeia a Camarilla e os Anarquistas por igual, e sobrevive sendo invisível."

    nia "(Sem levantar os olhos) Você não é daqui. Cheira a sangue bom. O que quer, cria de Primogênito?"

    "Ela viu coisas que ninguém mais repararia. Como você lida com Nia?"

    $ pool_seduzir, comp_seduzir = montar_pool((atributos, "Carisma"), (habilidades, "Persuasão"))
    $ pool_ameacar, comp_ameacar = montar_pool((atributos, "Manipulação"), (habilidades, "Intimidação"))
    $ pool_convencer, comp_convencer = montar_pool((atributos, "Compostura"), (habilidades, "Persuasão"))

    menu:
        "Seduzi-la, oferecendo companhia que ela raramente tem  ⚂ [pool_seduzir]":
            call rolar_teste(pool_seduzir, 2, comp_seduzir)
            $ sucesso_nia = _return >= 2
            if sucesso_nia:
                "Ela baixa a guarda devagar, sem acreditar direito que alguém quer só conversar com ela."
            else:
                "Ela ri, seca. \"Ninguém quer companhia de um Sangue-Ralo. Quer alguma coisa. Fala logo.\""

        "Ameaçá-la, deixando claro que ela não tem escolha  ⚂ [pool_ameacar]":
            call rolar_teste(pool_ameacar, 2, comp_ameacar)
            $ camarilla_marcado = True
            $ sucesso_nia = _return >= 2
            if sucesso_nia:
                "Ela entrega o que sabe, tremendo, sem tentar disfarçar o ódio nos olhos."
            else:
                "Ela grita — um som agudo que ecoa entre os vagões enferrujados — antes de fugir para dentro da escuridão."

        "Tratá-la como uma igual e proteger as costas dela durante a caça  ⚂ [pool_convencer]":
            call rolar_teste(pool_convencer, 2, comp_convencer)
            $ sucesso_nia = _return >= 2
            if sucesso_nia:
                "Ela percebe, aos poucos, que você não está fingindo. Ninguém nunca tratou um Sangue-Ralo como gente antes."
            else:
                "Ela aceita a ajuda, desconfiada, mas ainda mantém distância."

        "Usar um poder do Sangue" if any(disciplinas[_d] > 0 for _d in disciplinas):
            call uso_disciplina_social(2)
            $ sucesso_nia = _return >= 2

    if sucesso_nia:
        $ aliada_nia = True
        nia "Ninguém nunca... tá. Você me tratou como gente. Isso conta comigo. Se precisar de novo, eu tô por aí."
        "Nia jura lealdade a você como uma aliada leal nas ruas — e diz ter visto vans da Inquisição sendo alugadas. O cara que falsificou as placas é um despachante do submundo conhecido como \"Mãos-de-Graxa\" Jimmy, escondido em um ferro-velho."
    else:
        "Nia não confia em você o bastante para virar uma aliada, mas ainda solta um nome antes de sumir na escuridão: \"Mãos-de-Graxa\" Jimmy, um despachante que falsifica placas para quem paga bem — e vive escondido em um ferro-velho."

    $ alvo_laranja = "jimmy"
    $ fome = 0

    if camarilla_marcado:
        "Se você fez barulho ou deixou marcas, sabe que alguém, em algum lugar, está anotando."

    $ xp_disponivel += 2
    $ xp_total_ganho += 2
    "Tecer uma rede de contatos em Chicago também é experiência acumulada. (+2 XP)"

    jump fase2_interrogatorio


label caca_westloop:
    scene bg_clube with fade
    show sasha at center with dissolve
    "Festas secretas, drogas, artistas mortais em busca de inspiração sombria — o paraíso dos Toreador. Você encontra Sasha, uma jornalista investigativa mortal farejando dinheiro sujo sem fazer ideia de que está lidando com vampiros."

    "Ela murmura algo sobre \"lavagem de dinheiro\" para o próprio gravador. O pulso dela bate rápido. Ela é uma fonte de informações e um jantar em potencial. Como você lida com Sasha?"

    $ pool_seduzir, comp_seduzir = montar_pool((atributos, "Carisma"), (habilidades, "Persuasão"))
    $ pool_ameacar, comp_ameacar = montar_pool((atributos, "Manipulação"), (habilidades, "Intimidação"))
    $ pool_convencer, comp_convencer = montar_pool((atributos, "Manipulação"), (habilidades, "Lábia"))

    menu:
        "Seduzi-la, puxando conversa sobre arte e detalhes  ⚂ [pool_seduzir]":
            call rolar_teste(pool_seduzir, 2, comp_seduzir)
            $ sucesso_sasha = _return >= 2
            if sucesso_sasha:
                "Você a envolve em uma teia de charme até que ela confie os segredos a você — e o pescoço também."
            else:
                sasha "Você... você tem certeza que a gente já não se conheceu antes?"
                "Ela hesita, tonta, mas acaba cedendo mesmo assim."

        "Ameaçá-la, deixando claro que ela mexeu com gente perigosa  ⚂ [pool_ameacar]":
            call rolar_teste(pool_ameacar, 2, comp_ameacar)
            $ camarilla_marcado = True
            $ sucesso_sasha = _return >= 2
            if sucesso_sasha:
                "O terror puro faz o resto do trabalho. Ela entrega tudo o que sabe, tremendo."
            else:
                "Ela solta um grito curto antes de você conseguir calá-la. Alguém, em algum lugar próximo, vira a cabeça na direção do som."

        "Usar charme profissional para direcionar a investigação dela sem quebrar a Máscara  ⚂ [pool_convencer]":
            call rolar_teste(pool_convencer, 2, comp_convencer)
            $ sucesso_sasha = _return >= 2
            if sucesso_sasha:
                "Você não precisa nem mencionar o que é. Só aponta a direção certa, e o instinto de jornalista dela faz o resto — sem nunca desconfiar de quem está puxando os fios."
            else:
                "Ela concorda em investigar, mas fica claramente desconfiada de quão bem informada você parece estar."

        "Usar um poder do Sangue" if any(disciplinas[_d] > 0 for _d in disciplinas):
            call uso_disciplina_social(2)
            $ sucesso_sasha = _return >= 2

    "Seja roubando, seduzindo ou aterrorizando, você consegue a informação. Sasha registrou conexões bancárias obscuras e cita o nome da relações-públicas que assina pela Corvo Dourado: Veronica Vance, uma socialite que está dando um baile de caridade beneficente amanhã."

    if sucesso_sasha:
        $ aliada_sasha = True
        sasha "Se você topar me dar mais furos como esse, eu não faço perguntas demais. Trato feito?"
        "Você ganha um \"cão de guarda\" na mídia mortal — alguém disposto a fechar os olhos, e abrir portas, quando você precisar."

    $ alvo_laranja = "veronica"
    $ fome = 0

    if camarilla_marcado:
        "A sua caçada sacia sua Fome, mas não sem deixar rastros. Um homem de sobretudo de couro observa do outro lado da rua. Os olhos dele brilham com um amarelo animalesco. Você foi visto pelos cães de caça da Camarilla."

    $ xp_disponivel += 2
    $ xp_total_ganho += 2
    "Tecer uma rede de contatos em Chicago também é experiência acumulada. (+2 XP)"

    jump fase2_interrogatorio


# ============================================================
# FASE 2: O INTERROGATÓRIO DOS LARANJAS
# ============================================================
label fase2_interrogatorio:
    scene black with fade
    "Você volta a Isadora e Rook com o nome do seu alvo, dependendo de onde caçou na noite anterior. O relógio corre. Vocês precisam quebrar esse laranja para descobrir quem é o por trás dele."

    if alvo_laranja == "abernathy":
        jump interrogatorio_abernathy
    elif alvo_laranja == "jimmy":
        jump interrogatorio_jimmy
    else:
        jump interrogatorio_veronica


# --- ROTA A: O CONTADOR ---
label interrogatorio_abernathy:
    scene black with fade
    show abernathy at center with dissolve
    "O Sr. Abernathy janta sozinho no The Signature Room, no alto de um dos prédios mais altos da Magnificent Mile. O lugar está cheio demais de mortais importantes para uma cena."

    "Como você quebra o contador?"

    $ pool_seduzir, comp_seduzir = montar_pool((atributos, "Carisma"), (habilidades, "Persuasão"))
    $ pool_ameacar, comp_ameacar = montar_pool((atributos, "Manipulação"), (habilidades, "Intimidação"))
    $ pool_convencer, comp_convencer = montar_pool((atributos, "Inteligência"), (habilidades, "Persuasão"))

    menu:
        "Sentar-se à mesa dele e seduzi-lo, arrancando a verdade em voz baixa  ⚂ [pool_seduzir]":
            call rolar_teste(pool_seduzir, 3, comp_seduzir)
            $ sucesso_abernathy = _return >= 3
            if sucesso_abernathy:
                "Ele se apoia na mesa, encantado demais para perceber o perigo, e murmura os números que não deveria."
            else:
                "Ele sorri, educado, mas os olhos dele nunca param de vasculhar o salão em busca de uma saída."

        "Segui-lo até o carro no estacionamento e ameaçá-lo abertamente  ⚂ [pool_ameacar]":
            call rolar_teste(pool_ameacar, 3, comp_ameacar)
            $ sucesso_abernathy = _return >= 3
            if sucesso_abernathy:
                "Você o prensa contra o próprio carro. O medo faz o resto do trabalho — ele confessa tudo antes que você precise erguer a voz."
            else:
                "Ele grita por ajuda antes que você consiga silenciá-lo."

        "Argumentar com ele, mostrando que cooperar é a única saída racional  ⚂ [pool_convencer]":
            call rolar_teste(pool_convencer, 3, comp_convencer)
            $ sucesso_abernathy = _return >= 3
            if sucesso_abernathy:
                "Você apresenta os fatos com frieza cirúrgica — ele é só um contador, não um mártir. Ele cede antes de terminar de fazer as contas."
            else:
                "Ele acha que está blefando e chama o chefe de segurança do restaurante para \"resolver um mal-entendido\"."

        "Usar um poder do Sangue" if any(disciplinas[_d] > 0 for _d in disciplinas):
            call uso_disciplina_social(3)
            $ sucesso_abernathy = _return >= 3

    if sucesso_abernathy:
        abernathy "Tá bem, tá bem! E-mails, transferências, tudo isso passa por mim, mas eu só conheço o cara de cima por um apelido — \"o Colecionador\". É só isso que sei, juro!"
    else:
        "O chefe de segurança do restaurante chega rápido demais para ser mortal comum — ele se move como alguém treinado para lidar com Kindred descuidados."
        call escalar_conflito(4, "Você percebe tarde demais: a segurança do Signature Room não protege só clientes ricos. Protege segredos de outra facção vampírica inteira — e ela não gosta de intrusos.")
        "Você escapa com o que precisa, mas o preço foi alto."

    $ empresa_suspeita = "Corvo Dourado Holdings"

    $ xp_disponivel += 3
    $ xp_total_ganho += 3
    "Quebrar um homem sem quebrar a própria Máscara é uma lição e tanto. (+3 XP)"

    jump verdade_sombras


# --- ROTA B: O DESPACHANTE ---
label interrogatorio_jimmy:
    scene bg_beco with fade
    show jimmy at center with dissolve
    "O ferro-velho de \"Mãos-de-Graxa\" Jimmy fica cercado por rottweilers soltos e armadilhas de sucata empilhada. Ele vive escondido ali por um motivo."

    "Como você chega até ele?"

    $ pool_seduzir, comp_seduzir = montar_pool((atributos, "Carisma"), (habilidades, "Persuasão"))
    $ pool_ameacar, comp_ameacar = montar_pool((atributos, "Força"), (habilidades, "Intimidação"))
    $ pool_convencer, comp_convencer = montar_pool((atributos, "Inteligência"), (habilidades, "Persuasão"))

    menu:
        "Tentar acalmá-lo com uma oferta boa demais para recusar  ⚂ [pool_seduzir]":
            call rolar_teste(pool_seduzir, 3, comp_seduzir)
            $ sucesso_jimmy = _return >= 3
            if sucesso_jimmy:
                "Os cães nem latem — Jimmy os chama de volta assim que ouve o valor que você oferece, e abre o cofre sem discutir."
            else:
                jimmy "Ninguém paga bem o suficiente pra isso, cria."

        "Ameaçá-lo abertamente, deixando claro o que acontece se ele não cooperar  ⚂ [pool_ameacar]":
            call rolar_teste(pool_ameacar, 3, comp_ameacar)
            $ sucesso_jimmy = _return >= 3
            if sucesso_jimmy:
                "Você entra sem se esconder dos cães, deixando-os latir. Jimmy vê o que você é antes de ver o que você quer, e isso já é o suficiente para ele abrir o cofre com as mãos tremendo."
            else:
                "Os cães avançam antes de Jimmy dizer qualquer coisa, e ele usa o caos para sacar uma arma escondida atrás de um barril."

        "Argumentar com ele, mostrando que os patrões dele o abandonariam sem pensar duas vezes  ⚂ [pool_convencer]":
            call rolar_teste(pool_convencer, 3, comp_convencer)
            $ sucesso_jimmy = _return >= 3
            if sucesso_jimmy:
                "Você não precisa nem levantar a voz — só apontar o óbvio: ele é descartável, e sabe disso. Jimmy abre o cofre resignado."
            else:
                "Ele finge não entender do que você está falando, ganhando tempo enquanto a mão dele se aproxima de um botão de alarme."

        "Usar um poder do Sangue" if any(disciplinas[_d] > 0 for _d in disciplinas):
            call uso_disciplina_social(3)
            $ sucesso_jimmy = _return >= 3

    if sucesso_jimmy:
        "No cofre improvisado dentro de um freezer industrial quebrado, Jimmy guarda os nomes de todo mundo que já pagou por documentos falsos. Um nome se repete nos contratos mais recentes: um intermediário conhecido só como \"o Colecionador\"."
    else:
        "Um dos cães acerta seu braço antes que Jimmy consiga fugir — e ele aperta um botão de alarme escondido embaixo do balcão."
        $ saude_atual -= 1
        call escalar_conflito(4, "Luzes de longo alcance se acendem no fim do pátio de sucata. Não são policiais. São informantes da Segunda Inquisição, esperando exatamente por um barulho como esse.")
        "Você sai dali com os papéis, mas por pouco."

    $ empresa_suspeita = "Corvo Dourado Holdings"

    $ xp_disponivel += 3
    $ xp_total_ganho += 3
    "Quebrar um homem sem quebrar a própria Máscara é uma lição e tanto. (+3 XP)"

    jump verdade_sombras


# --- ROTA C: A SOCIALITE ---
label interrogatorio_veronica:
    scene bg_clube with fade

    if aliada_sasha:
        "Sasha, a jornalista que agora te deve um favor, arranja seu nome na lista de convidados do baile beneficente de Veronica Vance sem fazer perguntas demais."
    elif disciplinas["Ofuscação"] > 0:
        "Sem convite e sem aliados na festa, você usa o próprio Sangue para atravessar a segurança do hotel como uma sombra entre sombras, invisível aos olhos que deveriam barrar sua entrada."
    else:
        "Sem convite e sem favores para cobrar, você arrisca uma entrada não autorizada pela cozinha do hotel, torcendo para que ninguém pergunte seu nome."

    "Veronica Vance está isolada nos aposentos VIP no topo, enquanto a festa acontece no salão principal. O tablet pessoal dela guarda as transações que ligam o Primogênito ao massacre de Silas — mas dois seguranças bloqueiam o corredor até lá."

    $ pool_furtivo, comp_furtivo = montar_pool((atributos, "Destreza"), (habilidades, "Furtividade"))
    $ pool_enganar, comp_enganar = montar_pool((atributos, "Manipulação"), (habilidades, "Lábia"))
    $ pool_forca, comp_forca = montar_pool((atributos, "Força"), (habilidades, "Combate Corpo a Corpo"))

    menu:
        "Contorná-los completamente, escalando ou se esgueirando por onde ninguém olha  ⚂ [pool_furtivo]":
            call rolar_teste(pool_furtivo, 3, comp_furtivo)
            $ sucesso_guarda = _return >= 3
            if sucesso_guarda:
                "Você ignora os guardas por completo, entrando por uma janela destrancada dois andares acima."
            else:
                "Uma telha solta escorrega sob a sua mão na fachada molhada e cai andares abaixo, estilhaçando no chão."

        "Enganá-los, se passando por alguém que tem toda razão de estar ali  ⚂ [pool_enganar]":
            call rolar_teste(pool_enganar, 3, comp_enganar)
            $ sucesso_guarda = _return >= 3
            if sucesso_guarda:
                "Você arruma a postura, sorri, e convence os guardas de que é a assistente pessoal de Veronica com uma emergência vital."
            else:
                "Um dos guardas reconhece a farsa rápido demais e leva a mão ao rádio."

        "Avançar com força antes que eles reajam  ⚂ [pool_forca]":
            call rolar_teste(pool_forca, 3, comp_forca)
            $ sucesso_guarda = _return >= 3
            if sucesso_guarda:
                "Não há tempo para conversa. Você nocauteia os dois antes que eles alcancem os rádios."
            else:
                "O sangue na sua bota te faz escorregar no piso de mármore. Um dos guardas dispara antes de cair, e o estrondo ecoa pelo andar inteiro."
                $ saude_atual -= 1

        "Usar um poder do Sangue" if any(disciplinas[_d] > 0 for _d in disciplinas):
            call uso_disciplina_social(3)
            $ sucesso_guarda = _return >= 3

    if not sucesso_guarda:
        call escalar_conflito(4, "O alarme do hotel dispara. Seu elemento surpresa foi para o lixo, e a segurança inteira do prédio está subindo as escadas atrás de você.")

    "Você entra nos aposentos VIP. Veronica Vance está de costas, servindo um drink. Ao ver você, ela deixa o copo cair. A máscara de socialite derrete — e algo nos olhos dela não é inteiramente humano."

    show veronica at center with dissolve

    veronica "Quem te mandou?"

    "Ela sussurra, recuando em direção à gaveta da mesa. O tablet está brilhando em cima da cama. O que ela busca na gaveta não é uma arma comum."

    $ pool_desarmar, comp_desarmar = montar_pool((atributos, "Destreza"), (habilidades, "Briga"))
    $ pool_gritar, comp_gritar = montar_pool((atributos, "Carisma"), (habilidades, "Intimidação"))
    $ pool_escapar, comp_escapar = montar_pool((atributos, "Destreza"), (habilidades, "Atletismo"))

    menu:
        "Saltar sobre ela e desarmá-la antes que alcance a gaveta  ⚂ [pool_desarmar]":
            call rolar_teste(pool_desarmar, 3, comp_desarmar)
            $ veronica_estado = "inconsciente"
            $ sucesso_veronica = _return >= 3
            if sucesso_veronica:
                "Você é mais rápido. Um golpe seco e ela desaba, inconsciente, sobre o tapete, antes de alcançar o que quer que fosse."
            else:
                "Vocês dois caem lutando pelo controle da gaveta. Ela é forte demais para ser só uma socialite."

        "Gritar uma intimidação gutural o bastante para congelá-la de puro medo  ⚂ [pool_gritar]":
            call rolar_teste(pool_gritar, 3, comp_gritar)
            $ veronica_estado = "aterrorizada"
            $ humanidade -= 1
            $ sucesso_veronica = _return >= 3
            if sucesso_veronica:
                "O som que sai da sua garganta não tem nada de humano. Veronica congela no meio do movimento, os olhos vidrados de terror."
            else:
                "Ela grita de volta, mais em fúria do que em obediência, e continua avançando para a gaveta."

        "Pegar o tablet e escapar pela janela, sem se arriscar a lutar  ⚂ [pool_escapar]":
            call rolar_teste(pool_escapar, 3, comp_escapar)
            $ veronica_estado = "esquecida"
            $ sucesso_veronica = _return >= 3
            if sucesso_veronica:
                "Você agarra o tablet da cama e atravessa o vidro da janela num único movimento fluido, sumindo na chuva antes que ela complete o giro."
            else:
                "O vidro corta mais fundo do que devia. Você aterrissa mal no beco abaixo, mas o tablet continua na sua mão."
                $ saude_atual -= 1

        "Usar um poder do Sangue" if any(disciplinas[_d] > 0 for _d in disciplinas):
            call uso_disciplina_social(3)
            $ veronica_estado = "inconsciente"
            $ sucesso_veronica = _return >= 3

    if not sucesso_veronica:
        "Veronica chega à gaveta primeiro. O que ela puxa de lá não é uma arma de fogo — é um dispositivo de emergência que libera pela sala inteira uma névoa espessa e ardente, um composto incendiário forte demais para ser ignorado."
        "Ela é rápida demais, forte demais, resistente demais para ser só mortal. Veronica Vance é uma Serva de Sangue — uma Ghoul — e ela não vai deixar você sair vivo com o que sabe."
        call escalar_conflito(4, "O ar começa a queimar dentro dos seus próprios pulmões mortos. Saia daqui, de um jeito ou de outro, antes que o fogo termine o que Veronica não conseguiu.")

    $ empresa_suspeita = "Corvo Dourado Holdings"

    $ xp_disponivel += 3
    $ xp_total_ganho += 3
    "Sobreviver a uma Ghoul e sair com o tablet é uma lição e tanto. (+3 XP)"

    jump verdade_sombras


# ============================================================
# A GRANDE REVELAÇÃO
# ============================================================
label verdade_sombras:
    "Seja quebrando os dedos de Jimmy, lendo a mente do contador Abernathy, ou hackeando os aposentos de Veronica Vance, a verdade não pode mais ser escondida. Você está no escuro, lendo a prova final — um e-mail direto, um contrato assinado com sangue e tinta digital."

    scene black with fade

    if alvo_laranja == "abernathy":
        "Isadora Vane surge das sombras do estacionamento vazio, aparecendo atrás de você sem fazer nenhum som."
    elif alvo_laranja == "jimmy":
        "Isadora Vane surge de trás de uma pilha de sucata enferrujada, os olhos refletindo a luz fraca do ferro-velho."
    else:
        if veronica_estado == "inconsciente":
            "Isadora Vane entra no quarto VIP silenciosamente pelo terraço, observando o corpo desacordado de Veronica no chão."
        elif veronica_estado == "aterrorizada":
            "Isadora Vane entra no quarto VIP silenciosamente pelo terraço, observando Veronica encolhida no canto, ainda tremendo de puro terror."
        else:
            "Isadora Vane entra no quarto VIP silenciosamente pelo terraço. A suíte está vazia além de você — Veronica nunca vai saber que esteve aqui."

    show isadora brava at center with hpunch

    "(Surgindo das sombras atrás de você, a voz transbordando veneno)"

    isadora "Marcus Deverell. O Primogênito Toreador. Aquele pedaço de lixo engravatado vendeu a própria raça."

    "A peça final do tabuleiro se encaixa. Marcus é realeza em Chicago, intocável, e agora sabe que há sobreviventes farejando o rastro dele. Você tem a prova. Mas o que uma caçadora recém-criada fará quando for bater de frente com a elite da Camarilla?"

    $ empresa_suspeita = "Corvo Dourado Holdings"

    jump investigacao_empresa

# --- O CLÍMAX ---
label investigacao_empresa:

    scene bg_refugio with fade
    show isadora imponente at left with dissolve
    show marcus at right with moveinright
    "Você e Isadora invadem a cobertura de Deverell. Ele está lá, sereno, bebendo sangue de uma taça de cristal."

    marcus "Sacrifiquei o peso morto para manter Chicago limpa. E agora, vira-lata? O que você vai fazer?"

    "O destino dele, e a sua lenda em Chicago, são selados agora."
    
    menu:
        "Execução Bruta (Arrancar a cabeça dele)":
            $ final_tipo = "poder"
            $ camarilla_ameaca = True
            show isadora predatoria at left with hpunch
            "Você o decapita no tapete persa. O submundo te temerá, mas a Camarilla jurará sua morte."

        "A Justiça do Elysium (Entregar as provas para a Camarilla)":
            $ final_tipo = "humanidade"
            show isadora sorrindo at left with dissolve
            "Você o expõe. O próprio clã dele o condena. Você é visto como justo, mas como uma engrenagem do sistema."

        "O Contrato Corrupto (Extorquir a fortuna dele)":
            $ final_tipo = "besta"
            $ humanidade -= 1
            show isadora pensativa at left with dissolve
            "Você toma o dinheiro e o silencia. Fica rico e influente, mas Marcus será uma cobra encurralada esperando para dar o bote."

    isadora "Bem jogado. Muito bem jogado."

    "O Sol ameaça nascer no horizonte de Chicago. A exaustão da sua primeira noite te puxa para a escuridão."

    $ xp_disponivel += 8
    $ xp_total_ganho += 8
    "Sobreviver à primeira noite depois da Queda — sozinho, contra a elite intocável da Camarilla — ensina mais do que qualquer Disciplina que você já despertou. (+8 XP)"

    "FIM DE FRAGMENTOS DE CHICAGO — Fragmento Final"

    $ renpy.force_autosave(take_screenshot=True)
    return