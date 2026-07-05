# --- 1. DEFINIÇÕES DE IMAGENS E PERSONAGENS ---

init python:
    import random

image bg_refugio = At("images/bg_refugio.jpg", Transform(xsize=config.screen_width, ysize=config.screen_height))
image sala_de_guerra = At("images/bg_rook.png", Transform(xsize=config.screen_width, ysize=config.screen_height))
image  bg_beco= At("images/bg_beco.png", Transform(xsize=config.screen_width, ysize=config.screen_height))
image bg_beco = Solid("#0a0a0f")
image bg_clube = Solid("#1a001a")
image black= Solid("#000")

define i = Character("Mulher Misteriosa", color="#c8c8c8")
define isadora = Character("Isadora Vane", color="#8b0000")
define p = Character("[nome_jogador]", color="#831b1b")
define silas = Character("Silas", color="#556b2f")
define rook = Character("Rook", color="#b5651d")
define marcus = Character("Marcus Deverell", color="#c77dff")
define dr_miller = Character("Doutor Miller", color="#708090")
define slick = Character("Slick", color="#19255e")
define moto = Character("Moto", color="#a3f708")
# --- Sprites dos personagens ---
# Onde existe arte real (game/images/personagens/), ela é usada.
# Onde não existe, entra um placeholder sólido na cor do personagem,
# só para marcar presença em cena até a arte definitiva chegar.
image isadora = "images/personagens/Isadora.png"
image silas = "images/personagens/Silas.png"
image rook = "images/personagens/Rook.png"
image marcus = "images/personagens/Marcus.png"
image dr_miller = Solid("#708090", xsize=500, ysize=850)

# HUD de Status
screen hud_vampiro():
    key "c" action Show("ficha_personagem")

    vbox:
        align (0.02, 0.02)
        spacing 5
        if mostrar_fome:
            text "FOME: [fome]" size 25 color "#ff3333" outlines [(2, "#000", 0, 0)]
        if mostrar_humanidade:
            text "HUMANIDADE: [humanidade]" size 25 color "#33ff33" outlines [(2, "#000", 0, 0)]

        null height 10

        if mostrar_fome:
            textbutton "VER FICHA (C)":
                action Show("ficha_personagem")
                background Solid("#1a1a1a")
                padding (5, 5)
                text_size 18

            textbutton "MELHORAR (XP)":
                action Show("tela_experiencia")
                background Solid("#1a1a1a")
                padding (5, 5)
                text_size 18

# --- 2. VARIÁVEIS DO JOGO ---
default fome = 4
default humanidade = 7
default cla = "Nenhum"
default nome_jogador = "Cria"
default mostrar_fome = False
default mostrar_humanidade = False

default confianca_isadora = 0
default faccao = "Nenhuma"
default rota_investigacao = ""

# Variáveis de Consequência da Caça e Ato 1
default divida_primogenito = False
default camarilla_marcado = False
default nome_traidor = ""
default empresa_suspeita = ""
default final_tipo = ""
default camarilla_ameaca = False
default alvo_caca = ""

# --- 3. O JOGO ---

label start:
    scene black with dissolve

    "Feche os olhos por um instante. Pense no frio. Dizem que o momento da morte é uma transição pacífica. Mentiram para você."
    
    "Para você, a morte teve som: o barulho da chuva batendo nas latas de lixo de um beco sujo de Chicago. O cheiro de asfalto molhado e do seu próprio sangue escorrendo, levando embora seu nome, sua humanidade e tudo o que você costumava ser."
    
    "Você estava desaparecendo. Apenas mais uma estatística esquecida na sarjeta. Mas alguém viu valor nos seus destroços. Alguém te puxou de volta do abismo com o 'Beijo'. E o preço dessa passagem de volta é uma sede que nunca, jamais, vai acabar. Abra os olhos."

    show bg_refugio with fade

    "O porão é gótico, forrado de livros antigos e iluminado por velas tremeluzentes. A fumaça do incenso mascara um cheiro metálico no ar."

    show isadora at center with dissolve

    isadora "Olha só quem voltou. Seja muito bem-vinda ao seu primeiro e último pesadelo."

    "Isadora se aproxima. Ela é incrivelmente bela, com olhos que parecem ler seus pecados mais íntimos."

    isadora "Eu sou Isadora Vane. Fui eu quem te deu o Abraço. Mas antes de decidir o que fazer com você, pequena cria, me diga... o que você sente fervendo nas suas veias agora? Qual é o instinto que te domina?"

    "É aqui que o seu Sangue define quem você é. A maldição de Caim tem muitas faces. O que grita mais alto dentro de você?"

    menu:
        "Qual instinto te domina?"

        "Sinto uma fúria incontrolável, a vontade de quebrar o mundo (Brujah)":
            $ cla = "Brujah"
        "Sinto as sombras do quarto sussurrando e se curvando a mim (Lasombra)":
            $ cla = "Lasombra"
        "Sinto uma necessidade fria de comandar, nasci para governar (Ventrue)":
            $ cla = "Ventrue"
        "Ouço vozes que ninguém mais ouve, vejo verdades ocultas (Malkaviano)":
            $ cla = "Malkaviano"
        "Sinto uma obsessão avassaladora pelos detalhes e beleza (Toreador)":
            $ cla = "Toreador"
        "Sinto repulsa e poder crescendo juntos, escondidos (Nosferatu)":
            $ cla = "Nosferatu"

    isadora "Entendo. O sangue nunca mente sobre o que somos por baixo da pele. Mas conversar dá sede."

    "Antes de Isadora testar o seu controle, precisamos definir do que você é feita. Distribua seus pontos de ficha."

    call criacao_personagem

    "Você sente seu corpo se ajustar. Músculos se contraem, seus sentidos se expandem. Mas junto com o poder, vem o Defeito do seu Clã."

    if cla == "Brujah":
        "A chama das velas irrita seus olhos. Uma raiva latente ferve sob a sua pele, pronta para explodir ao menor insulto."
    elif cla == "Lasombra":
        "Você olha para uma poça de água no chão e o seu reflexo não está lá. A luz elétrica pisca quando você respira."
    elif cla == "Ventrue":
        "O cheiro de sangue comum revira seu estômago. Seu paladar aristocrático exigirá presas específicas a partir de hoje."
    elif cla == "Malkaviano":
        "Um zumbido de estática ecoa no seu ouvido esquerdo. A parede de pedra parece respirar. A loucura já sussurra seu nome."
    elif cla == "Toreador":
        "Você fica paralisada encarando o padrão perfeito da cera da vela derretendo. Um mundo sem beleza causará dor física em você."
    else:
        "Seus ossos estalam. A pele coça e repuxa, deformando-se para sempre. As sombras serão suas únicas amigas a partir de agora."

    $ mostrar_fome = True
    $ mostrar_humanidade = True
    show screen hud_vampiro

    "Isadora pega uma faca de prata e faz um corte limpo no próprio pulso. Uma gota de sangue espesso cai no chão. O som ecoa como um trovão."

    "Suas entranhas se contorcem. É um incêndio exigindo o único combustível capaz de apagá-lo. Faça o seu primeiro teste: Resolução + Autocontrole (Dificuldade 2)."

    $ reserva_teste_inicial, comp_teste_inicial = montar_pool((atributos, "Resolução"), (atributos, "Compostura"))
    call rolar_teste(reserva_teste_inicial, 2, comp_teste_inicial)
    
    if _return >= 2:
        "Você segura o pulso dela com delicadeza. O gosto é o céu e o inferno juntos, mas você para de beber antes de enlouquecer."
        "Isadora sorri, orgulhosa do seu refinamento. A sua Fome recua."
        $ fome = 1
        $ confianca_isadora += 1
    else:
        "A Besta vence. Você avança nela com um rosnado gutural, derrubando-a e lambendo o sangue desesperadamente."
        "Isadora te empurra com força, decepcionada com seu estado animalesco. Você perde um pedaço da sua Humanidade."
        $ fome = 3
        $ humanidade -= 1


    # --- O ATAQUE ---
    scene bg_refugio with vpunch
    show isadora at left with dissolve
    show silas at right with dissolve
    "A porta do porão é arrombada. Silas, um aliado de Isadora, entra tropeçando, coberto de queimaduras fumegantes."

    silas "(Cuspindo cinzas) Isadora... fomos vendidos. A Inquisição atacou a Zona Norte. Eles tinham as plantas..."
    isadora "Quem, Silas? Quem entregou as plantas?"

    "Silas está à beira do coma vampírico. Sirenes já cortam a rua lá em cima"
    "Isadora olha pra você, e pela primeira vez naquela noite, é possível ver o medo em seus olhos"
    
    isadora "São os inquisitores. Precisamos sair daqui"
    silas "Pelos tuneis...eu conheço um caminho até o refugio do Rook"

    "Vocês vão se dirigindo ao fundo do quarto, com o som de passos se aproximando"


# --- A SALA DE GUERRA ---

label sala_de_guerra:
    scene black with fade
    "A chuva lá fora parece tentar lavar o cheiro de cinzas de Silas, mas o terror da noite impregnou as paredes de concreto."
    
    show sala_de_guerra with fade
    show isadora at left with dissolve
    show rook at right with dissolve

    "O refúgio dos Anarquistas é um caos organizado. Caixotes de armamento pesado, monitores empilhados e motocicletas desmontadas. Vampiros de jaqueta de couro e feições endurecidas avaliam você sob a luz fraca. O bando de Rook."

    rook "Quem é a garota, Vane? Meu armazém não é creche para recém-criadas."
    
    isadora "Ela é minha cria. E a única razão de Silas ainda estar respirando. [nome_jogador], este é Rook, o dono deste buraco. E a equipe dele..."
    
    "Isadora aponta sutilmente para dois Anarquistas no fundo: um homem corpulento limpando uma escopeta e uma garota pálida digitando furiosamente em um laptop cheio de adesivos."

    rook "Vocês trouxeram a Inquisição para o meu quintal, Isadora. Isso é péssimo pros negócios."

    p "Inquisição? Achei que isso fosse lenda medieval com tochas e ancinhos."

    isadora "A Segunda Inquisição, [nome_jogador]. Agências governamentais, o Vaticano, operações negras financiadas por orçamentos que não existem. Eles não usam tochas. Usam satélites, drones térmicos e munição de fósforo branco. Eles caçam nossa espécie para nos apagar do mapa."
    
    show silas at center with dissolve
    "Silas se apoia na mesa de metal. A pele queimada dele regenera lentamente em um chiado doentio. A voz dele é áspera."

    silas "E eles sabiam... eles sabiam exatamente onde estávamos. Ignoraram nossos carniçais de segurança e foram direto para o cofre do refúgio."
    
    silas "Eu ouvi o rádio tático do líder deles antes da granada de luz explodir. Ele disse: 'Alvo assegurado. Pagamento da Galeria confirmado. O Corvo de Ouro canta.' Foi a última coisa antes do fogo."

    "A sala fica em silêncio. O peso da realidade esmaga o ar. Um traidor, alguém de dentro de Chicago, entregou o refúgio por dinheiro."

    rook "Slick! Joga isso na rede. O que diabos é o 'Corvo de Ouro'?"

    "A garota no laptop ('Slick') não para de digitar. O estalar das teclas preenche o vazio."
    
    slick "Achei. 'Corvo de Ouro' não é uma pessoa. É uma escultura raríssima roubada há décadas. E adivinha? Ela vai ser leiloada hoje à noite. Um evento super restrito da alta sociedade no Elysium da Camarilla."

    "A porta pesada do armazém se abre com um rangido estridente. O homem da escopeta se aproxima sacudindo a água do casaco de couro."
    
    moto "Rook, o porto sul está fervendo. Contrabandistas movendo caixas de chumbo pesadas. Cheiro forte de munição ultravioleta e dinheiro sujo, vivo, não rastreável."

    isadora "O tal 'pagamento da Galeria'..."

    silas "Ainda tem mais." 
    
    "Ele coloca um celular de carcaça militar, completamente rachado, sobre a mesa. A tela pisca erraticamente em vermelho."
    
    silas "É o telefone de um dos caçadores. Eu consegui arrancar do colete dele enquanto fugíamos. Tem um rastreador embutido ligado a uma rede privada. Se revertermos o sinal, achamos os servidores da offshore que pagou a operação toda."

    rook "A segurança dessa rede deve ser nível Pentágono. Slick não consegue quebrar uma criptografia militar sozinha sem torrar a localização do meu armazém."

    "Você observa o telefone sobre a mesa. É tecnologia de ponta. Uma verdadeira muralha de código."

    # Mini-game opcional de Tecnologia (Requer Tecnologia >= 2)
    if habilidades["Tecnologia"] >= 2:
        "Mas, com seus conhecimentos avançados em Tecnologia da sua vida mortal, você enxerga os padrões. Há uma falha no protocolo de boot do aparelho. Você pode tentar ajudar."
        
        menu:
            "Eu posso quebrar a primeira camada":
                $ res_tech_silas, comp_tech_silas = montar_pool((atributos, "Inteligência"), (habilidades, "Tecnologia"))
                "A criptografia morde de volta. É uma dificuldade brutal (Dificuldade 4). Role os dados."
                
                call rolar_teste(res_tech_silas, 4, comp_tech_silas)
                if _return >= 4:
                    "Seus dedos voam sobre o teclado de Slick. Você isola o firewall da Inquisição e o contorna com um script fantasma. A tela verde revela o endereço IP de um servidor físico escondido no distrito financeiro."
                    slick "Puta merda... Você é bom, garoto. Temos o endereço de acesso do servidor!"
                    $ confianca_isadora += 1
                    $ xp_disponivel += 1
                    "A confiança de Isadora em você aumenta, e os Anarquistas te olham com novo respeito. (+1 XP)"
                else:
                    "Você insere um comando invasivo, mas o sistema detecta a anomalia. O celular superaquece nas suas mãos e a tela morre com um estalo elétrico cheirando a ozônio."
                    slick "Merda! O sistema de segurança fritou a placa-mãe. Perdemos o acesso direto, e quase fomos rastreados."
                    rook "Ótimo. Tentar brincar de hacker nos custou o atalho. Agora vamos ter que invadir a rede às cegas através dos cabos subterrâneos."
            
            "Melhor deixar para lá. Não vale o risco de fritar o aparelho e nos expor.":
                "Você recua da mesa. Melhor focar no trabalho de campo que vocês já sabem fazer."
    else:
        "O jargão técnico deles soa como uma língua alienígena para você. Hackear um aparelho da Inquisição está muito além das suas capacidades atuais."

        "A mesa de guerra está posta. Isadora volta o olhar afiado para você. Ela sabe que, neste momento, você é a maior vantagem tática deles."

        isadora "Você é nosso fantasma, [nome_jogador]. A Segunda Inquisição ainda não tem o seu rosto ou o seu nome no banco de dados deles. Você é o único que pode andar lá fora sem ser reconhecido imediatamente."

        isadora "Você precisa escolher qual fio dessa teia nós vamos puxar esta noite."

    menu:
        "O Leilão no Elysium (Onde a Elite esconde o 'Corvo de Ouro')":
            $ rota_investigacao = "leilao"
        "As Docas de Contrabando (Onde a Inquisição recebe o dinheiro e as armas)":
            $ rota_investigacao = "docas"
        "A Invasão Digital (Rastrear e hackear os servidores fisicamente)":
            $ rota_investigacao = "rastreio"

    # --- A FOME NAS RUAS (MINI-GAME DE CAÇA) ---
    "O estresse da fuga ativou sua Besta. Sua Fome subiu para 3. Ir para a missão famint0 é suicídio. Você precisa caçar. Como vai saciar essa sede hoje?"
    $ fome = max(fome, 3)

    menu:
        "A Abordagem do Beco: Você irá espreitar em algum beco da cidade, provavelmente proximo a algum bar, para encuralar algum bebado desavizado que aparecer":
            jump caca_beco
        "O Clube Noturno: Clubs e Pubs são sempre um excelente local de caça para um membro, o jogo da sedução sempre funciona":
            jump caca_clube
        "O Comerciante de Sangue: Rook tem o contato de um contrabandista que consegue bolsas de sangue desviadas de hospitais":
            jump caca_comerciante

# --- AS ROTAS DE CAÇA ---

label caca_beco:
    scene bg_beco with fade
    "Você espreita um assaltante num beco. Ele encurralou um turista. O turista foge, e o caçador vira a presa. Faça um teste de Destreza + Furtividade (Dificuldade 2)."

    $ res_furt, comp_furt = montar_pool((atributos, "Destreza"), (habilidades, "Furtividade"))
    call rolar_teste(res_furt, 2, comp_furt)

    if _return >= 2:
        "Você se move como o abismo. Sua mão tapa a boca dele e você o puxa para as sombras. O sangue quente inunda sua garganta. A cidade está mais segura."
        $ fome = 0
        jump inicio_investigacao
    else:
        "Seus sapatos raspam no chão. Ele vira com uma faca tática. Ele acha que você é apenas uma vítima comum. Teste Força + Briga (Dificuldade 2)."
        $ res_briga, comp_briga = montar_pool((atributos, "Força"), (habilidades, "Briga"))
        call rolar_teste(res_briga, 2, comp_briga)
        
        if _return >= 2:
            "Você quebra o pulso dele e bebe rápido e sem cuidado. Foi sujo e deixou marcas, mas você sobreviveu."
            $ fome = max(0, fome - 2)
            $ saude_atual -= 1
            jump inicio_investigacao
        else:
            "Ele é rápido demais. A lâmina rasga seu estômago. Pior: os gritos dele ecoaram. A polícia chegou na entrada do beco."
            $ fome = max(0, fome - 1)
            $ saude_atual -= 2
            call escalar_conflito(3, "Você está encurralado pela polícia. É hora de forçar a saída.")
            jump inicio_investigacao

label caca_clube:
    scene bg_clube with fade

    "A porta pesada do clube Velvet se fecha atrás de você, abafando o som da chuva e substituindo-o pelas batidas graves do Tech House. O som vibra no seu peito, simulando um coração que você não tem mais."

    "O lugar é um labirinto de luzes estroboscópicas azuis e vermelhas. Pessoas dançam apertadas, suadas, perdidas no ritmo e na fumaça de gelo seco. Para um mortal, cheira a gin, suor e perfumes caros."

    "Para você, o ar cheira a um banquete. O sangue pulsando nas veias daquelas pessoas pinta a sala em tons de calor térmico na sua visão predatória. A sua Besta ronrona, ansiosa. É hora de escolher."

    "Você caminha pelo salão, os olhos afiados cortando a multidão. Duas presas em potencial se destacam na penumbra."

    "A primeira é uma mulher no meio da pista de dança. Ela usa um vestido vermelho colado e dança de olhos fechados, totalmente entregue à música. A pulsação dela é rápida, cheia de adrenalina e vida. O sangue dela deve ter o gosto de energia pura."

    "A segunda está sentada no bar. Uma mulher de terninho escuro, girando um copo de dry martini intocado. O olhar dela é cínico, entediado, avaliando todo mundo com desdém. A respiração é lenta e controlada. O sangue dela deve ser complexo, denso, com o sabor maduro da melancolia."

    menu:
        "A mulher de vestido vermelho na pista de dança":
            $ alvo_caca = "dancarina"
            "Você desliza para o meio da pista. A música consome os sentidos dela, o que facilita a sua aproximação. Você se move no mesmo ritmo, o corpo encostando levemente no dela. Quando ela abre os olhos e te vê, a surpresa se transforma quase imediatamente em desejo hipnotizado."

            p "A música está alta, mas eu consigo ouvir o seu coração daqui..."

            "Ela sorri, a respiração falhando. \"Me leva pra um lugar mais calmo\", ela sussurra no seu ouvido."

        "A mulher de terninho no bar":
            $ alvo_caca = "executiva"
            "Você se senta no banco vazio ao lado dela. Você pede ao barman um copo de uísque que não vai beber, apenas para segurá-lo."

            p "Lugar cheio, mas você parece que preferia estar em qualquer outro canto do mundo."

            "Ela vira o rosto para você. Os olhos dela são afiados. \"Pessoas me entediam. Mas você... você não tem a mesma expressão desesperada que o resto do bar\", ela diz, sorrindo de canto. \"Estou no camarote VIP. Quer companhia para ignorar essa festa?\""

    "Faça um teste de Carisma + Persuasão (Dificuldade 2) para envolvê-la completamente."

    $ res_pers, comp_pers = montar_pool((atributos, "Carisma"), (habilidades, "Persuasão"))
    call rolar_teste(res_pers, 2, comp_pers)

    if _return >= 2:
        "A teia se fecha. Perfeitamente."

        if alvo_caca == "dancarina":
            "Vocês tropeçam rindo para dentro de uma cabine de banheiro ampla. A luz fria do espelho ilumina o rosto ruborizado dela. Ela te puxa pela gola do casaco, os lábios quentes buscando os seus."
        else:
            "O camarote VIP está vazio, isolado por pesadas cortinas de veludo. Ela senta no sofá de couro e te puxa pelo cinto, o olhar cínico substituído por uma luxúria sombria e silenciosa."

        "O beijo mortal de um vampiro não é um ato de violência pura. O veneno na sua saliva paralisa a presa em um estado de euforia absoluta. O Beijo é o paraíso na Terra para os mortais."

        "Você inclina a cabeça dela para o lado, sentindo o pulso forte contra os seus lábios. Você abre a boca. Seus caninos deslizam para fora com um estalo inaudível. E então, você morde."

        "A perfuração é limpa. O sangue inunda a sua boca — quente, elétrico, perfeito. A garota arfa, os olhos revirando de prazer enquanto você suga a vida dela a goles longos e lentos. O corpo frio do seu cadáver começa a se aquecer com o calor humano roubado. A cor volta às bochechas dela. A Besta no seu estômago ronrona, saciada e submissa."

        "Você para no momento exato antes de tirar demais. Você lambe a ferida, o seu sangue selando os dois furos no pescoço dela como se nunca tivessem existido."

        "Ela suspira, encostando a cabeça na parede, completamente entorpecida pela endorfina."

        p "Foi maravilhoso. Descanse um pouco..."

        "Você ajusta o casaco, limpa uma gota solitária de sangue do canto do lábio e sai do ambiente."

        $ fome = 0
        "A Fome desapareceu. Você está no auge do seu poder. Chicago está pronta para ser quebrada."
        jump inicio_investigacao
    else:
        "Sua Besta rosnou alto demais no meio do beijo. Ela sente o erro — um puxão forte demais, um som gutural baixo demais para ser humano — e entra em pânico, empurrando você com toda a força que o medo empresta."
        "O grito dela morre abafado pela música, mas não morre rápido o suficiente. Dois seguranças imensos já vêm na direção de vocês, e a Máscara, pela primeira vez esta noite, racha de verdade."
        $ humanidade -= 1
        $ camarilla_marcado = True

        $ res_fuga_correr, comp_fuga_correr = montar_pool((atributos, "Destreza"), (habilidades, "Atletismo"))
        $ res_fuga_medo, comp_fuga_medo = montar_pool((atributos, "Carisma"), (habilidades, "Intimidação"))

        "Fuja. Como você sai dessa?"
        menu:
            "Fugir correndo  ⚂ [res_fuga_correr]":
                $ res_fuga, comp_fuga = res_fuga_correr, comp_fuga_correr
            "Aterrorizar guardas  ⚂ [res_fuga_medo]":
                $ res_fuga, comp_fuga = res_fuga_medo, comp_fuga_medo

        call rolar_teste(res_fuga, 3, comp_fuga)
        if _return >= 3:
            "Você escapa pela porta dos fundos. Mas não conseguiu beber, e um informante da Camarilla te viu. Você fez inimigos hoje."
            jump inicio_investigacao
        else:
            "Eles te agarram. Você joga um longe, quebrando uma parede de vidro. Câmeras te filmam. A polícia é acionada."
            $ saude_atual -= 1
            call escalar_conflito(4, "O caos é total. Fuja antes que a Inquisição intercepte o rádio da polícia.")
            jump inicio_investigacao

label caca_comerciante:
    scene black with fade
    show dr_miller at center with dissolve
    "Você vai até o necrotério onde o Doutor Miller vende bolsas de sangue roubadas."
    dr_miller "O sangue tá em falta, mocinho. Não quero dinheiro. Quero que fique me devendo um favor."
    
    "Ficar devendo a um lacaio é assinar um cheque em branco. Tente baixar o tom dele: Manipulação + Intimidação (Dificuldade 2)."
    $ res_int, comp_int = montar_pool((atributos, "Manipulação"), (habilidades, "Intimidação"))
    call rolar_teste(res_int, 2, comp_int)

    if _return >= 2:
        "Você prensa a mão dele na mesa. Sua voz sai como gelo. Miller recua e entrega as bolsas, aterrorizado. Sangue de graça."
        $ fome = 0
        jump inicio_investigacao
    else:
        "Ele ri da sua tentativa. 'Meu mestre é do Primogênito. Ou aceita a Dívida de Vida, ou sai vazio'."
        menu:
            "Aceitar a Dívida Primogênita":
                $ divida_primogenito = True
                $ fome = 0
                "Você engole o orgulho e toma o sangue frio. A Fome some, mas a dívida cobrará seu preço no futuro."
            "Recusar e sair faminto":
                "Você cospe no chão e sai. Nenhuma dívida, mas você começará a investigação faminto e agressivo."
        jump inicio_investigacao

label inicio_investigacao:
    "A noite não perdoa os fracos. Com os dentes manchados ou a garganta em chamas, vamos à investigação."

    $ xp_disponivel += 3
    $ xp_total_ganho += 3
    "Sobreviver à primeira noite depois do Abraço já ensina alguma coisa. (+3 XP)"

    jump rotas_ato1
