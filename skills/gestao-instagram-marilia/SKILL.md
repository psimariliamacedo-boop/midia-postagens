---
name: "gestao-instagram-marilia"
description: "Use sempre que for planejar, editar, agendar, postar, anunciar ou medir conteúdo do @mariliamacedo.psi (reels, capas, legendas, stories, Metricool, anúncios Meta, Google Meu Negócio). Reúne todas as decisões da Marília de 23 a 25/11/2026 e prevalece sobre regras antigas."
---

# Gestão do Instagram e anúncios · @mariliamacedo.psi

Marília Macêdo, psicóloga e neuropsicóloga, CRP 06/229488. Responda sempre em português, simples e direto. Ela não gosta de processo demorado: faça, mostre e peça só a decisão que for dela.

Consultório (desde 11/2026): Rua Santa Gertrudes, 1230 · Bela Vista IV · Cosmópolis/SP, perto da Praça do Rodrigo. Atende presencial em Cosmópolis e online para todo o Brasil. WhatsApp (19) 99784-7824. A Carol (MyChatBot) atende o WhatsApp.

## 1. Regras de edição (prevalecem sobre a skill editor-reels-marilia)
- **Só a versão BÁSICA.** Nunca entregar a versão "dinâmica".
- **Nada de texto, faixa ou legenda em cima do rosto ou da testa.** Sem faixa no topo da tela.
- **Gancho:** caixa branca com texto azul-marinho (DM Sans 700, ~70 px), **visível desde o primeiro quadro**, só nos primeiros ~3 s, **abaixo da legenda** (cap_y + 60). Conferir sempre com detector de rosto (YuNet) que o queixo fica acima da legenda em todo o vídeo.
- **Legenda:** DM Sans 500 branca em blocos de 2 a 4 palavras, palavra-chave em mel dourado (#F4B860) numa caixa azul-marinho (#1A2146). Sem rosa.
- **Cortar pausas internas** maiores que 0,3 s (script `tighten.py`).
- **Conferir se as falas fazem sentido juntas.** Cortar frases soltas que não se entendem sozinhas.
- **CTA no vídeo (reels de teste):** "Manda pra amiga que…". Nos anúncios: "Me chama no WhatsApp".
- **Cartão final:** Me chama no WhatsApp · endereço · online para todo o Brasil · nome e CRP.
- **Áudio:** original do microfone, só ganho linear até pico de -1,2 dB.
- **Cor:** HLG → SDR (zscale + tonemap hable desat=0) + LAB L=(L-143,8)·1,12+128, a=(a-128)·0,92+126, b=b+8.
- **Listas sem fala:** cenas reais da sala, com **zoom lento em todas as cenas** (fotos e vídeos) para nada parecer congelado. Nada de cena de planta parada (IMG_7859).
- **Sem IA nos reels.**

## 2. Capas
- Rosto dela **sorrindo**, sem careta, sem olho fechado ou torto. Ela deixa ~3 s sorrindo no começo de cada gravação: pegar o quadro dali (ou de outra tomada com a mesma roupa).
- Caixa branca com texto azul-marinho em Lora 600 (~86 px), em 2 linhas, na altura do peito (y≈1180).
- Bons quadros de sorriso: IMG_7912 (0,8 s e 2,0 s), IMG_7914 (0,0 s), IMG_7907 (2,5 s), IMG_7916 (0,4 s), IMG_8081 (1,2 a 2,0 s), IMG_8063 (0,0 s), IMG_8077 (0,0 s).

## 3. Estratégia orgânica (até o balanço de 04/12/2026)
- **1 Reel de teste (Trial) por dia**, só para quem não segue.
- **Depois de 72 h:** passou da média em visualizações e envios? Ela toca em "Compartilhar com seguidores". Senão, fica fora do feed.
- **Stories todo dia** para os seguidores (estão na planilha).
- **Legenda:** só a palavra **PAUSA** como chamada ("Manda PAUSA no meu direct que eu te envio" o checklist gratuito) por 4 semanas. Nada de "me chama no WhatsApp" na legenda.
- Até 4 hashtags. Ética CFP: "pode ser", nunca "você tem"; sem testes na tela; sem paciente real.
- Música: definida no Metricool (Peaceful Piano, id 2477944699150252; Precious Time, id 280021457045107). Sem fala: volume 100. Falados: volume 12, por baixo da voz.

## 4. Agendamento
- Ferramenta: **Metricool** (blogId 7547062), tipo **TRIAL_REEL**, publicação automática, fuso America/Sao_Paulo.
- O vídeo precisa estar no Google Drive dela, compartilhado como "qualquer pessoa com o link". O conector do Drive daqui só sobe arquivos de até ~3 MB, então ela sobe os vídeos pelo app do Drive e eu compartilho e agendo.
- Stickers (enquete, caixinha, localização) não entram por agendamento: ficam com ela.

## 5. Anúncios Meta (conta 972512623195205, página 752334907962229)
- **Teto: R$ 400 por mês** somando todas as campanhas. A campanha tem spend_cap de R$ 400.
- **Testar 2 anúncios por vez**, R$ 6,50/dia cada (R$ 13/dia), rodadas de 14 dias.
- Campanha "WhatsApp Consultório · Teste de anúncios · nov-dez 2026" (id 120250090449810208), objetivo Engajamento → conversas no WhatsApp.
- Públicos: "COSMÓPOLIS 15 km · Presencial · Mulheres 25-55" (120250090450930208) e "BRASIL · Online · Mulheres 25-55" (120250090451970208).
- **Rodada 1 (25/11 a 08/12):** C1 (120250090458600208, Brasil) e D (120250104563650208, Cosmópolis). **Rodada 2 (09/12 a 22/12):** vencedor contra C2 (120250103617570208) ou E (120250104613290208), pausados até lá.
- Ligar, aumentar orçamento ou criar anúncio que gaste: **só com o "pode ligar" dela.**
- Pagamento pré-pago com recarga automática de R$ 50. A conta tem limite de gastos total (≈R$ 1.490), que pode pausar tudo: conferir em 27/11.
- Ferramenta: Windsor.ai (conector facebook). Capa do anúncio por link `https://lh3.googleusercontent.com/d/<id do Drive>`.

## 6. Google Meu Negócio
- Local `locations/6976211182004459796`. Endereço já correto. Post do endereço novo publicado em 24/11/2026 com foto da sala e botão Ligar.

## 7. Onde está tudo
- Planilha no Drive: pasta "Revisar antes de postar · 24-11 a 01-12" → "Calendário de postagens · Instagram (24-11 a 06-12)".
- Vídeos finais no Drive (pasta 126NKg5t2cgbYGLCajbuu3FHtF2EmjkD9), com a data no nome.
- Registro completo com datas e métricas: arquivo "Registro Instagram e Anúncios" (Drive e iCloud dela).
- Scripts: repositório midia-postagens, pasta `edicao-23-11/scripts/` (render3.py, tighten.py, lista.py, capas*.py, planilha.py).

## 8. Próximos passos
- 27/11: conferir se os anúncios continuam rodando (limite de gastos da conta).
- 02/12: balanço da rodada 1 de anúncios.
- 04/12: balanço dos reels de teste (visualizações, envios, quais foram para o feed).
- Conteúdo pronto até 06/12. Para depois: IMG_8042 ("Mais ou menos") e 3 gravações curtas (almoço em pé, última hora, comparação) + cenas sem fala para listas.
