---
name: "stories-marilia"
description: "Use quando a Marília pedir stories, programação de stories, arte de story, enquete, caixinha ou análise de stories do @mariliamacedo.psi. Define a rotina de 2 a 3 stories por dia, o estilo pessoal, as cores e a edição das artes, e como medir."
---

# Stories · @mariliamacedo.psi

Marília Macêdo, psicóloga e neuropsicóloga, CRP 06/229488. Consultório: Rua Santa Gertrudes, 1230 · Bela Vista IV · Cosmópolis/SP. Responda em português, simples e direto.

## 1. O que os números dela mostram (Metricool, ago a nov/2026)
- **Melhores stories (100 a 133 pessoas, 3 a 4 respostas): ela sendo pessoa.** Humor ("Estou suspeitando que minha mãe pensa que está fazendo terapia 😅"), bastidor da vida ("Fim de noite sempre eu e ele 😍 meu Squishy"), frase sincera ("Que venha o novo, com leveza e propósito 🤍") e a sala com endereço ("Um lugar pra você respirar 📍 Rua Santa Gertrudes, 1230").
- **Stories sem texto ou em sequência longa: 17 a 89 pessoas.** Do 3º story seguido em diante, o alcance despenca.
- **Respostas são raras** (máximo 4). Enquete e caixinha servem para aumentar isso.
- Conclusão: **menos e mais pessoal.** Nada que pareça propaganda.

## 2. Rotina: 2 a 3 stories por dia
| Momento | O quê | Como |
|---|---|---|
| **Manhã (8h a 10h)** | **Pessoal e real**: café, caminho, porta do consultório, selfie, domingo no sofá, o Squishy | Foto ou vídeo de 5 s feito por ela + 1 frase curta e leve, de preferência com humor. Pode citar o tema do reel do dia ("hoje às 19h eu conto…"). |
| **Tarde (12h a 14h)** | **Interação**: enquete (2 opções curtas) ou caixinha | Arte com a pergunta + figurinha colocada por ela no app. Pergunta ligada ao reel do dia. |
| **Noite (hora do reel)** | **O reel do dia** | Abrir o reel → aviãozinho → Adicionar ao story. Opcional 1 vez por semana: arte PAUSA (checklist gratuito). |

Regras fixas:
- **Máximo 3 por dia.** Se ela não tiver foto pessoal no dia, faça só tarde + noite (2).
- **1 emoji por story, no máximo.** Texto de até 2 linhas.
- **Figurinha de localização "Cosmópolis"** sempre que aparecer a sala.
- **Chamada só com PAUSA** ("Manda PAUSA no meu direct que eu te envio o checklist") até o fim das 4 semanas de teste. Nada de "me chama no WhatsApp" nos stories orgânicos.
- **Ética CFP:** nunca paciente (rosto, nome, história reconhecível), nunca prontuário; "pode ser", nunca "você tem"; sem teste psicológico na tela.
- Enquete, caixinha, localização e música **não entram por agendamento**: ficam com ela. Só a arte sem figurinha pode ser agendada (Metricool, tipo STORY), e só se ela pedir.

## 3. Cores e edição das artes
- **Formato:** 1080x1920. Área segura: nada importante nos 250 px do topo nem nos 340 px da base. Deixe um espaço livre (meio ou parte de baixo) para a figurinha.
- **Paleta:** azul-marinho #1A2146 (texto e caixas), mel dourado #F4B860 (destaque sobre o azul), branco (caixas e texto sobre azul). **Sem rosa** (ela acha infantil). Sem vinho.
- **Frase principal:** caixa branca retangular com texto azul-marinho em **Lora 600** (~74 px), até 3 linhas, centralizada.
- **Linha de apoio** (ex.: "Hoje às 19h"): caixa azul-marinho arredondada com texto mel dourado em **DM Sans 700** (~44 px), logo abaixo da frase.
- **Arte PAUSA:** fundo azul-marinho, "PAUSA" grande em mel dourado (Lora 700), texto branco em DM Sans, nome e CRP pequenos embaixo.
- **Nada de texto em cima do rosto ou da testa.** Quando a foto tem o rosto dela no alto, a caixa vai para baixo (y≈1180). Conferir sempre.
- **Rosto:** só sorrindo ou natural, sem careta e sem olho fechado ou torto.
- **Cor das fotos e vídeos do iPhone:** HLG → SDR (zscale + tonemap hable, desat=0) e ajuste LAB L=(L-143,8)·1,12+128, a=(a-128)·0,92+126, b=b+8. Parede vermelha, pele quente.
- **Fotos da sala prontas** (tamanho story): destaque-sala_sala-inteira, poltrona-acolhimento, poltrona-janela, cantinho-cafe, canto-terracota, prateleira, sala-mesinhas, sala-poltronas, mesinha-infantil.
- Script: `edicao-23-11/scripts/stories.py` no repositório midia-postagens (função `story(fundo, frase, apoio, saída, y)` e `pausa(saída)`). Rodar dentro de uma pasta com `fonts/` (DM Sans e Lora do npm @fontsource, convertidas para TTF).
- Nome dos arquivos: `Story AAAA-MM-DD manha|tarde ENQUETE|tarde CAIXINHA|noite PAUSA.jpg`.

## 4. Como medir
- Metricool (blogId 7547062) → `getAnalyticsDataByMetrics` com IGST01 (data), IGST03 (texto), IGST10 (alcance orgânico), IGST11 (respostas), IGST08 (saídas), IGST13 (toques para avançar).
- **Meta por story: 100 pessoas ou mais e 3 respostas ou mais** (o melhor dela até 25/11/2026).
- Toda semana (e no balanço de 04/12): listar os stories, marcar os que bateram a meta, repetir o estilo deles e trocar o que ficou abaixo.
- Enquete: conferir também quantos votaram (no app, ela vê em "Visualizações").

## 5. Ao montar a programação
1. Ver o calendário de reels da semana (planilha "Calendário de postagens · Instagram") para amarrar manhã e tarde ao tema do reel.
2. Para cada dia, entregar: o que ela deve fotografar de manhã + a frase; a arte da tarde (pergunta + tipo de figurinha + opções da enquete); o horário do reel da noite.
3. Mandar as artes no chat com o dia no nome e a tabela resumida. Não agendar sem ela pedir.
