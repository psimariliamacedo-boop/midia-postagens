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
2. **"Neuropsicóloga"**: DECIDIDO 26/11/2026 — MANTER (decisão da Marília; risco CFP já avisado). Não perguntar de novo.
3. Card 2 sem mensagem pronta: opcional adicionar texto.

## Registro de alterações no site
| Data | Alteração | Aprovado por |
|---|---|---|
| 25/11/2026 | Revisão completa; nenhuma alteração publicada ainda | — |
| 25/11/2026 | Botão fixo do WhatsApp adicionado ao index.html (testado em iPhone e desktop); publicação na Netlify feita pela Marília | Marília |

## Ideia futura
- Página própria de Avaliação Neuropsicológica (para o grupo de anúncios de avaliação). Avaliar após o Dia 30/60 da campanha.

## Google Search Console
- **ATIVADO** para mariliamacedopsi.com.br (confirmado pela Marília em 26/11/2026). NÃO perguntar de novo.
- Próximos passos: enviar sitemap.xml (quando o pacote de SEO for publicado) e usar "Inspeção de URL".
- Para ler os dados daqui: conector `searchconsole` do Windsor.ai (teste até ~25/12/2026) ou prints da Marília.

## Regra geral
- Antes de perguntar algo à Marília, consultar as skills site-marilia, google-ads-marilia, dados-profissionais-marilia e carol-assistente-marilia e o arquivo estrategias-marketing.md. Todo fato novo confirmado por ela deve ser anotado na skill correspondente.

## Pacote do site (26/11/2026) — entregas/site-pacote/ (zip: entregas/site-pacote.zip)
- index.html com botão fixo do WhatsApp + canonical + Open Graph (imagem img/compartilhar.jpg) + dados estruturados (ProfessionalService/LocalBusiness: endereço Santa Gertrudes 1230, telefone, horários ter–sex 8–21h e sáb 8–12h, áreas atendidas, Instagram e Google).
- 7 fotos tiradas de dentro da página e comprimidas em WebP: página caiu de 387 KB para 24 KB + 172 KB de imagens.
- robots.txt e sitemap.xml novos. Testado no iPhone (Playwright): 0 imagens quebradas, botão ok.
- Publicar: Netlify → Deploys → arrastar a PASTA site-pacote inteira (substitui o site; tudo está dentro). Depois: Search Console → Sitemaps → enviar "sitemap.xml" e Inspeção de URL da página inicial.

## Site com páginas por tópico (26/11/2026) — entregas/site-pacote/ (zip ignorado no git)
- Menu fixo no topo (☰) em todas as páginas: Início · Terapia para adultos (terapia.html) · Crianças e adolescentes (criancas-e-adolescentes.html) · Terapia de casal (terapia-de-casal.html, só presencial) · Avaliação neuropsicológica (avaliacao-neuropsicologica.html) · Perguntas frequentes (perguntas-frequentes.html, com dados estruturados FAQPage, 13 perguntas reais do Google).
- Botão do WhatsApp agora REDONDO (60 px, verde, canto inferior direito), igual ao exemplo que a Marília mandou (site da Isadora Mattos). Cada página tem botão com mensagem pronta do tema.
- sitemap.xml com as 6 páginas. Sem preço em nenhuma página (CFP). Testado no iPhone: 0 imagens quebradas, menu com 6 links.
- AINDA NÃO PUBLICADO: a Marília precisa arrastar a pasta na Netlify e enviar o sitemap no Search Console.
- Fotos do site (img/foto-1..7): 1 retrato blusa branca; 2 sorrindo com tablet; 3 e 4 café (mãos); 5 livros na mão; 6 sentada com notebook; 7 livros de TCC. Não há foto do consultório novo nem de criança.
