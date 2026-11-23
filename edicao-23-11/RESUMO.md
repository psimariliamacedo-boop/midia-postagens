# Edição 23/11/2026 · Resumo da sessão "Gravações de hoje"

## Contexto
- Perfil: @mariliamacedo.psi (psicóloga e neuropsicóloga, CRP 06/229488).
- Consultório novo: **Rua Santa Gertrudes, 1230 · Bela Vista IV · Cosmópolis**, perto da Praça do Rodrigo. A Carol (MyChatBot) já tem o endereço novo.
- Gravação feita hoje (23/11), com microfone, na sala nova. Fundo: parede terracota com prateleiras (planta, relógio e um ursinho de Natal).

## Decisões de estratégia (valem a partir de hoje)
- Segue o plano de 20/11: **regra 4 + 1**, com **1 reel de teste por dia** (gravado ou de dicas). Primeiro balanço em 04/12.
- **Sem IA nos reels.** A série **Fantasma** parou (a Marília arquiva no app os #1, #2 e #3). Os eventos do Fantasma 4 a 7 e do Glitter com IA foram tirados da agenda.
- Reels de teste sem resultado não foram para o feed, então não precisam ser arquivados.
- CTA: no vídeo, "Manda pra amiga que…". Na legenda, só a palavra **PAUSA** (checklist da pausa) por 4 semanas.
- Ferramenta de postagem (Meta Business Suite ou outra): decidir depois.
- Dados: os melhores reels têm o rosto dela (agosto e setembro, entre 600 e 1.558 visualizações). Bastidor da psicóloga e listas em "você" funcionam. O gargalo são os 3 primeiros segundos (65% a 87% de pulos em novembro).

## Roteiros de hoje
Documento no Drive: "Gravação 23-11 · Roteiros do consultório novo" (id 1ZUohXnS04xCBuuss4AZo4gixB6HuE_F11ozDWB2dLSw), com 20 roteiros. Na conversa também houve uma versão frase por frase. Principais:
- Anúncios: **C1** (releitura do campeão "A distância não é mais desculpa"), **C2** ("Esperando sobrar tempo?"), **D** (consultório novo, sentada), **E** (TDAH adulto).
- Falados: Você descansa trabalhando; Avaliação de TDAH não é prova; Mais ou menos; Primeira sessão; Mudei de endereço.
- Sem fala: Parece preguiça, mas pode ser sobrecarga; 7 frases; 7 coisas que eu nunca vou te pedir; Parece bagunça, mas pode ser atenção; 7 coisas que você acha que é seu jeito; Glitter real; Nessa sala você não precisa…; Mesinha da avaliação infantil.
- A Marília **nem sempre seguiu o roteiro**: transcrever tudo e identificar as falas.

## Vídeos já recebidos (todos do C1)
IMG_7887 (teste de som), 7889, 7891, 7892, 7893, 7896, 7897, 7898, 7899, 7900, 7901, 7902, 7903 e 7904.
- Os outros vídeos de hoje estão em ~/Downloads no notebook dela. A sessão do notebook "Acesso aos downloads do notebook" recebeu o pedido de copiar os .MOV de hoje para a pasta do Drive **"Gravação 23-11 brutos"**. **Use somente os vídeos de hoje.**

## C1 aprovado (montagem)
1. IMG_7893, de 1,20 a 6,45 s: "A falta de tempo não é mais uma desculpa para você, nem a distância."
2. IMG_7901, de 1,52 a 6,46 s: "Eu atendo online para todo o Brasil e presencialmente em Cosmópolis."
3. IMG_7893, de 6,62 a 8,36 s: "Eu estou com o meu consultório novo,"
4. IMG_7893, de 9,62 a 13,80 s: "perto da Praça do Rodrigo, e vai ser uma satisfação atender você."

O "aqui em Cosmópolis" foi cortado porque **ela não gostou de "Cosmópolis" repetido**. Duração final: 17,7 s, mais o cartão final de 1,5 s.

## Padrão de edição aprovado
- **Som:** usar o áudio original do microfone, **sem filtro de ruído, sem EQ e sem compressor**. Só ganho linear até o pico ficar em -1,2 dB (no C1 foram +4,5 dB). O tratamento anterior ficou ruim.
- **Cor:** iPhone HDR (HLG). Converter com `zscale + tonemap=hable:desat=0` e depois em LAB: L = (L-143,8)·1,12+128; a = (a-128)·0,92+126; b = b+8. Referência: a foto do iPhone dela (parede vermelha real, pele quente). A transferência antiga da skill deixou a parede alaranjada, e ela não gostou.
- **Sem rosa** ("infantil"). Paleta: azul-marinho #1A2146, mel dourado #F4B860 e branco.
- **Legenda:** DM Sans 500, branca, com sombra suave e **sem contorno preto**. A palavra de destaque vai em DM Sans 700 **mel dourado dentro de uma caixa azul-marinho arredondada** (opção 4, escolhida por ela, porque o dourado solto some no cabelo loiro).
- **Básico:** título "Sem tempo pra terapia?" numa caixa azul-marinho no alto; legenda em blocos de 2 a 4 palavras; CTA "Me chama no WhatsApp" numa caixa azul-marinho sobre a última fala; cartão final de 1,5 s.
- **Dinâmico:** gancho numa caixa branca com texto azul-marinho (DM Sans 700); rótulo "CONSULTÓRIO NOVO EM COSMÓPOLIS"; frases-resumo em Montserrat ExtraBold itálico com destaque dourado e emoji; legenda palavra por palavra em DM Sans; @mariliamacedo.psi na tela; botão azul-marinho; cartão final.
- **Cartão final:** "Me chama no WhatsApp" + "Clica no botão e agenda" (dourado) + endereço + "Online para todo o Brasil" + nome e CRP.
- **Capa:** caixa branca com texto escuro em Lora (estilo que já funciona no perfil). Para o C1, foram geradas 3 opções; a recomendada é a 1 (sorriso leve).
- **Pendente:** ela ainda não escolheu entre a versão básica e a dinâmica para os próximos (até agora, entregar as duas).

## Técnico
- Os scripts estão em `edicao-23-11/scripts/`. `render.py` é o C1 completo (estilo `basic` ou `dynamic`); `tr.py` faz a transcrição; `cover.py` faz as capas.
- Transcrição: `pip install faster-whisper opencv-python-headless fonttools brotli`, rodar com `HF_HUB_DISABLE_XET=1` e passar o áudio como numpy (o `av` dá erro). O ambiente "Criação Vídeo" já libera o Hugging Face.
- Fontes: `npm pack @fontsource/dm-sans@5 @fontsource/montserrat@5 @fontsource/lora@5` e converter WOFF para TTF com fontTools.
- O Whisper adianta as palavras entre 0,1 e 0,4 s: alinhar pelo silêncio e pela energia do áudio.
- Ética CFP: sem testes psicológicos na imagem, "pode ser" e nunca "você tem", sem paciente real.

## Próximos passos
1. Pegar os brutos de hoje no Drive ("Gravação 23-11 brutos") ou pedir que a Marília envie no chat.
2. Transcrever tudo e mapear as falas por roteiro (incluindo as improvisadas).
3. Mandar a lista de vídeos possíveis, depois uma prévia, aprovação e o restante.
4. Opcional: versões extras do anúncio (local para Cosmópolis com IMG_7891; curta com IMG_7896).
