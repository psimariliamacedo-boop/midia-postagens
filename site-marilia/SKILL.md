---
name: site-marilia
description: Use sempre que a Marília falar do site dela (mariliamacedopsi.com.br), botão de WhatsApp do site, hospedagem/Netlify, textos do site, rastreamento de cliques/conversões ou alterações na página.
---

# Site — mariliamacedopsi.com.br (registro)

Fonte única sobre o site. Contato/CRP: skill `dados-profissionais-marilia`. Anúncios: skill `google-ads-marilia`.

## Básico
- Endereço oficial: **https://mariliamacedopsi.com.br** (o antigo psicologa-marilia-macedo.vercel.app NÃO é mais usado).
- Hospedagem: **Netlify** (servidor "Netlify"). Página única em HTML feita sob medida (não é Wix/WordPress).
- Login: app.netlify.com — confirmar se entra com psi.mariliamacedo@gmail.com (pendente).
- Publicar alteração: editar o index.html e arrastar para a Netlify (Deploys → arrastar arquivo/pasta).
- Em sessões na nuvem, o domínio foi liberado na rede do ambiente "Criação Vídeo" (25/11/2026).
- Endereço do consultório no site: Rua Santa Gertrudes, 1230, Bela Vista IV, Cosmópolis (correto, atualizado).
- Link usado no Perfil da Empresa no Google: https://mariliamacedopsi.com.br/?utm_source=google&utm_medium=perfil-empresa&utm_campaign=gbp

## Conteúdo atual (revisado em 25/11/2026)
- Título da página: "Marília Macêdo Psicóloga".
- Descrição (Google): "Marília Macêdo, psicóloga e neuropsicóloga. Terapia e avaliação neuropsicológica online e presencial em Cosmópolis/SP. CRP 06/229488."
- Topo: CRP 06/229488, foto, "Marília Macêdo", "PSICÓLOGA · NEUROPSICÓLOGA", frase "Nem todo cansaço vem de um lugar ruim.", "Online · Presencial em Cosmópolis/SP · Horários noturnos".
- Seções: Por que fazer terapia comigo · O que dizem no Google · Prazer, Marília · Antes de agendar.
- Página longa no celular (~6.000 px).

## Botões de WhatsApp (todos com o número certo 5519997847824)
1. Card "Agendar terapia — Online ou presencial. Me chama no WhatsApp" → mensagem "Olá, Marília! Quero agendar terapia." (aparece só após rolar; topo do botão ~650 px no iPhone).
2. Card "Me chama no WhatsApp (19) 99784-7824 — Abrir conversa" → sem mensagem pronta (~980 px).
3. "Quero marcar minha primeira conversa" → "Olá, Marília! Quero marcar minha primeira conversa." (no fim, ~5.800 px).
- Número antigo (19) 98180-9621: NÃO aparece (ok).
- Formulário de avaliação: link para tally.so (recebe os UTMs da visita).

## Rastreamento (Google Ads) — FUNCIONANDO no código
- Tags carregadas: AW-18214841341 e AW-18048200069 (ambas da conta 9843545527; manter as duas).
- Clique em qualquer wa.me → conversão **"Clique no WhatsApp (1)"** (send_to AW-18048200069/EICaCOCY27YdEIXbhp5D) + evento clique_whatsapp_*.
- Clique no Tally → conversão **"Formulário de avaliação"** (AW-18048200069/qo0OCOOY27YdEIXbhp5D).
- Conversão antiga **"Clique no WhatsApp"** (id 7652851845, rótulo 2YcbCIWBlcEcEIXbhp5D) não é usada pelo site → remover/marcar secundária no Google Ads (pendente, com ok da Marília).
- Conferir após ativar a campanha: status "Registrando conversões" no Google Ads.
- Correção registrada: em 24/11 foi dito que o rastreamento estava quebrado; em 25/11, lendo o site, confirmou-se que está correto.

## Alterações propostas (aguardando decisão da Marília)
1. **FEITO 25/11 (aguardando publicação):** botão verde "Agendar pelo WhatsApp" fixo no canto inferior direito (mensagem "Olá, Marília! Vim pelo site e quero agendar."; conta como conversão). Arquivo: entregas/site/index.html. Antes era: (celular e computador), com mensagem pronta e contando como conversão — prioridade alta (hoje não há WhatsApp na 1ª tela do celular).
2. **"Neuropsicóloga"** no topo e na descrição: risco com o CFP se não houver título de especialista registrado no CRP. Sugestão: "Psicóloga · Neuropsicologia". Ela não gosta de "Pós em Neuropsicologia". Decisão pendente.
3. Card 2 sem mensagem pronta: opcional adicionar texto.

## Registro de alterações no site
| Data | Alteração | Aprovado por |
|---|---|---|
| 25/11/2026 | Revisão completa; nenhuma alteração publicada ainda | — |
| 25/11/2026 | Botão fixo do WhatsApp adicionado ao index.html (testado em iPhone e desktop); publicação na Netlify feita pela Marília | Marília |

## Ideia futura
- Página própria de Avaliação Neuropsicológica (para o grupo de anúncios de avaliação). Avaliar após o Dia 30/60 da campanha.
