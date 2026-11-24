import sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
OUT = sys.argv[1]
R = "Marília Macêdo · Psicóloga e Neuropsicóloga · CRP 06/229488"
CAPA = {"24": "18uLs0lE1_SPG0gtTiEKgySie26HXsQRK", "25": "1U02R1Tl_uGFv-gLOLSH6meUisK2oZyKG", "26": "17mr5q7PhCX3kkvEv8Q6NC8qtrmqg5hGJ",
        "27": "1wczOzvC68NYrZ6Bl-PpOPKxyWtJoQzXv", "28": "1pqg0b9VVlN5wImjQvL45MQceb2SMRXZH", "29": "14AiVhMHQKDz1Qx2Ei4l-KWUSu-zJI6cU",
        "30": "1PMyxU8TAetbwI-rxIW1ke9r8R7PerRLD", "01": "1tof2D1WJtHMatRHEds5pA8REblM7ozVt"}
def link(k, txt): return f'=HYPERLINK("https://drive.google.com/file/d/{CAPA[k]}/view","{txt}")'
MUS_FALA = "Instrumental calmo em alta, volume baixo (10 a 15%), por baixo da sua voz"
MUS_SEM = "Música em alta, calma (piano ou violão), volume normal"
HEAD = ["Data", "Dia", "Hora", "Formato", "Reel", "Vídeo (arquivo)", "Capa", "Texto da capa", "Gancho na tela (0 a 3 s)",
        "Legenda (pronta para colar)", "Hashtags", "Música", "Stories do dia", "Depois de 72 h", "Situação"]
POST72 = "Passou da sua média em visualizações e envios? Toque em Compartilhar com seguidores."
rows = [
 ["24/11/2026", "Ter", "20h", "Reel de teste (sem fala)", "Nessa sala você não precisa…", "2026-11-24 Nessa sala.mp4", link("24", "Abrir capa"),
  "Nessa sala você não precisa…", "Nessa sala você não precisa…",
  "Muita gente chega na primeira sessão achando que precisa estar pronta, saber o que dizer, ter um motivo grande. Não precisa.\n\nEssa é a minha sala nova, aqui em Cosmópolis. Montei cada canto pensando em quem chega cansada e só quer um lugar pra respirar.\n\nSe você está adiando porque não sabe por onde começar, a gente começa junto. Me chama no WhatsApp, o link está na bio.\n\nRua Santa Gertrudes, 1230 · Bela Vista IV · Cosmópolis. Também atendo online.\n\n" + R,
  "#psicologacosmopolis #terapiacosmopolis #terapia #saudemental", MUS_SEM,
  "1) Foto da sala inteira com a figurinha de localização Cosmópolis e o texto: Sala nova, Rua Santa Gertrudes, 1230.\n2) Foto da poltrona com caixinha de perguntas: O que te deixaria mais à vontade numa primeira sessão?",
  POST72, "Pronto"],
 ["25/11/2026", "Qua", "20h", "Reel de teste (sem fala)", "Quantas dessas você disse essa semana?", "2026-11-25 Quantas dessas.mp4", link("25", "Abrir capa"),
  "Quantas dessas você disse essa semana?", "Quantas dessas você disse essa semana?",
  "Eu escuto essas frases toda semana, quase sempre de quem está cansada há muito tempo e nem percebe mais.\n\nConta aqui nos comentários: quantas você disse essa semana?\n\nFiz um checklist gratuito com os sinais de que você está segurando peça demais. Manda PAUSA no meu direct que eu te envio.\n\n" + R,
  "#sobrecargafeminina #cansacomental #saudemental #psicologia", MUS_SEM,
  "1) Print do reel com enquete: Quantas você disse? 0 a 3 / 4 a 7.\n2) Texto simples: O checklist da pausa é gratuito. Manda PAUSA no direct.",
  POST72, "Pronto"],
 ["26/11/2026", "Qui", "19h", "Reel de teste (falado)", "Avaliação de TDAH é uma prova?", "2026-11-26 Avaliacao TDAH.mp4", link("26", "Abrir capa"),
  "Avaliação de TDAH é uma prova?", "Avaliação de TDAH é uma prova?",
  "Muita gente adia a avaliação neuropsicológica porque imagina uma prova de escola, com nota e reprovação.\n\nNa prática é uma conversa, algumas atividades e tudo no seu ritmo. No fim, você entende melhor como a sua atenção funciona e o que dá pra fazer com isso.\n\nReconhecer sinais não é diagnóstico. Se quiser saber como funciona, me chama no WhatsApp, o link está na bio.\n\n" + R,
  "#tdahadulto #tdahemmulheres #avaliacaoneuropsicologica #psicologacosmopolis", MUS_FALA,
  "1) Caixinha de perguntas: Qual a sua dúvida sobre a avaliação de TDAH?\n2) No dia seguinte, responda 2 ou 3 perguntas em vídeo curto (sem dar diagnóstico).",
  POST72, "Pronto"],
 ["27/11/2026", "Sex", "17h", "Reel de teste (falado)", "Medo da primeira sessão?", "2026-11-27 Primeira sessao.mp4", link("27", "Abrir capa"),
  "Medo da primeira sessão?", "Medo da primeira sessão?",
  "Se o que te segura é não saber como é lá dentro, eu te conto.\n\nVocê senta, a gente conversa, eu faço algumas perguntas sobre a sua história. Não tem certo nem errado e você não precisa saber por onde começar. E o que é dito na sala fica na sala.\n\nSalva pra quando decidir. Atendo em Cosmópolis e online.\n\n" + R,
  "#terapia #primeirasessao #psicologacosmopolis #terapiaonline", MUS_FALA,
  "1) Enquete: Você já fez terapia? Já fiz / Ainda não.\n2) Vídeo de 5 s da porta da sala abrindo, sem texto.",
  POST72, "Pronto"],
 ["28/11/2026", "Sáb", "19h", "Reel de teste (sem fala)", "Antes e depois da sala", "2026-11-28 Antes e depois.mp4", link("28", "Abrir capa"),
  "Ninguém viu essa sala assim", "Ninguém viu essa sala assim…",
  "Em outubro essa sala era parede manchada, lona no chão e cadeira empilhada. Teve dia em que eu achei que ela não ia ficar pronta.\n\nFui fazendo do jeito que dava, uma parte de cada vez. Hoje ela está pronta pra receber você.\n\nSe você está no meio de um recomeço, ele não precisa estar bonito agora.\n\nRua Santa Gertrudes, 1230 · Bela Vista IV · Cosmópolis\n\n" + R,
  "#psicologacosmopolis #terapiacosmopolis #recomeco #saudemental", MUS_SEM,
  "1) Foto da obra e foto de hoje, lado a lado, com enquete: Você está recomeçando alguma coisa? Estou / Quero.\n2) Caixinha: O que você está construindo aos poucos?",
  POST72, "Pronto"],
 ["29/11/2026", "Dom", "18h", "Reel de teste (falado)", "Você descansa de verdade?", "2026-11-29 Descanso.mp4", link("29", "Abrir capa"),
  "Você descansa de verdade?", "Você descansa de verdade?",
  "Saiu com as amigas e a cabeça ficou na louça, na roupa, na lista de amanhã. O corpo estava lá, a cabeça não.\n\nDescanso de verdade é quando não tem nada pra resolver por dentro. E isso quase nunca acontece sozinho.\n\nFiz um checklist gratuito com os sinais de que você está segurando peça demais. Manda PAUSA no meu direct que eu te envio.\n\n" + R,
  "#descanso #sobrecargafeminina #saudemental #psicologia", MUS_FALA,
  "1) Enquete: Seu domingo foi de descanso? Foi / Que nada.\n2) Texto: Manda PAUSA no direct que eu te envio o checklist.",
  POST72, "Pronto"],
 ["30/11/2026", "Seg", "18h", "Reel de teste (falado)", "Sempre se achou desorganizada?", "2026-11-30 TDAH adulto.mp4", link("30", "Abrir capa"),
  "Sempre se achou desorganizada?", "Sempre se achou desorganizada?",
  "Esquecida, desorganizada, tudo pra cima da hora. Muita mulher ouve isso a vida inteira e nunca teve a chance de investigar o porquê.\n\nReconhecer sinais não é diagnóstico. A avaliação neuropsicológica olha com calma pra como isso aparece no seu dia a dia.\n\nAtendo presencial em Cosmópolis e online pra todo o Brasil. Me chama no WhatsApp, o link está na bio.\n\n" + R,
  "#tdahadulto #tdahemmulheres #avaliacaoneuropsicologica #psicologacosmopolis", MUS_FALA,
  "1) Caixinha: O que você mais esquece no dia a dia?\n2) Enquete: Já pensou em fazer uma avaliação? Já / Nunca.",
  POST72, "Pronto"],
 ["01/12/2026", "Ter", "20h", "Reel de teste (falado)", "Como é a primeira sessão aqui?", "2026-12-01 Primeira sessao aqui.mp4", link("01", "Abrir capa"),
  "Como é a primeira sessão aqui?", "Como é a primeira sessão aqui?",
  "Me perguntam muito como é a primeira sessão. É assim: um café ou uma água, a poltrona e eu te ouvindo, no seu tempo.\n\nNão tem certo nem errado. E o que é dito aqui fica aqui.\n\nMe chama no WhatsApp, o link está na bio. Atendo em Cosmópolis e online.\n\n" + R,
  "#terapia #primeirasessao #psicologacosmopolis #terapiacosmopolis", MUS_FALA,
  "1) Foto do cantinho do café com o texto: Café ou água?\n2) Enquete: Café / Água.",
  POST72, "Pronto"],
]
fila = [
 ["02/12/2026", "Qua", "Psicóloga chora com o paciente?", "Falado (vídeo de 29/10, resposta à caixinha)", "A editar"],
 ["03/12/2026", "Qui", "Quem cuida de você quando você cuida de todo mundo?", "Lista sem fala, escolha um número", "A editar"],
 ["04/12/2026", "Sex", "Seu fim de semana termina como?", "Lista sem fala, escolha um número. Dia do balanço dos testes", "A editar"],
 ["05/12/2026", "Sáb", "Que frase da sua casa ainda mora em você?", "Lista sem fala, escolha um número", "A editar"],
 ["06/12/2026", "Dom", "Sua refeição também entra na lista (almoço em pé)", "Lista sem fala ou gravar 15 s falando", "A gravar"],
 ["07/12/2026", "Seg", "Mais ou menos", "Falado. Falta conferir o IMG_8042", "Aguardando vídeo"],
 ["A definir", "", "Parece preguiça, mas pode ser sobrecarga", "Lista sem fala", "A editar"],
 ["A definir", "", "7 coisas que eu nunca vou te pedir na terapia", "Lista sem fala, cenas da sala", "A editar"],
 ["A definir", "", "Última hora / TDAH (tema do reel Véspera)", "Regravar 15 s falando na sala", "A gravar"],
 ["A definir", "", "Comparação / devagar (tema do reel Devagar)", "Regravar 15 s falando na sala", "A gravar"],
]
outros = [
 ["Anúncio pago (Meta)", "C1 · A distância não é mais desculpa", "Aprovado"],
 ["Anúncio pago (Meta)", "C2 · Esperando sobrar tempo?", "Pronto, aguardando aprovação"],
 ["Anúncio pago (Meta)", "D · Terapia em Cosmópolis", "Pronto, aguardando aprovação"],
 ["Google Meu Negócio", "Vídeo da sala (28 s) e fotos quadradas", "Pronto, subir pelo app"],
 ["Google Meu Negócio", "Post: consultório novo em Cosmópolis", "Aguardando sua aprovação do texto"],
 ["Destaque Sala (Instagram)", "9 fotos tamanho story e capa SALA", "Pronto"],
]
arq = [["24/11 a 02/12", "36 reels de teste de paisagem (conversa, teste, inspirado, guia)", "Pasta 0 AGENDAR HOJE no Drive", "Não postar. Formato antigo: paisagem, sem rosto, 4 por dia e palavras LIMITE e CALMA."],
       ["28/11", "Devagar (reel no feed)", "Metricool, pausado", "Não postar como está. Tema vai para a fila, para regravar."],
       ["03/12", "Véspera (reel no feed)", "Metricool, pausado", "Não postar como está. Tema vai para a fila, para regravar."],
       ["05/12", "Segurar (reel no feed)", "Metricool, pausado", "Não postar. Motivacional genérico."],
       ["06/12 e 13/12", "Stories Sonho e Balanço", "Pasta antiga", "Rever depois do balanço de 04/12."],
       ["12/12", "Acalma (reel no feed)", "Pasta antiga", "Rever depois do balanço de 04/12."]]
wb = Workbook(); NAVY = "1A2146"; GOLD = "F4B860"
hf = Font(name="Arial", bold=True, color="FFFFFF"); hfill = PatternFill("solid", fgColor=NAVY); body = Font(name="Arial", size=10)
wrap = Alignment(wrap_text=True, vertical="top"); thin = Side(style="thin", color="D9D9D9")
def sheet(ws, head, data, widths):
    ws.append(head)
    for r in data: ws.append(r)
    for c in ws[1]: c.font = hf; c.fill = hfill; c.alignment = Alignment(wrap_text=True, vertical="center")
    for row in ws.iter_rows(min_row=2):
        for c in row: c.font = body; c.alignment = wrap; c.border = Border(bottom=thin)
    for i, w in enumerate(widths): ws.column_dimensions[chr(65 + i)].width = w
    ws.freeze_panes = "A2"; ws.row_dimensions[1].height = 30
ws = wb.active; ws.title = "Calendário"
sheet(ws, HEAD, rows, [11, 5, 6, 16, 24, 26, 12, 22, 22, 70, 30, 26, 45, 30, 12])
for r in range(2, len(rows) + 2): ws.cell(r, 7).font = Font(name="Arial", size=10, color="1155CC", underline="single")
dv = DataValidation(type="list", formula1='"Pronto,A editar,A gravar,Agendado,Postado,Compartilhado com seguidores"', allow_blank=True)
ws.add_data_validation(dv); dv.add("O2:O200")
ws2 = wb.create_sheet("Fila"); sheet(ws2, ["Data prevista", "Dia", "Reel", "Formato", "Situação"], fila, [12, 6, 50, 50, 16])
ws3 = wb.create_sheet("Anúncios e Google"); sheet(ws3, ["Onde", "Peça", "Situação"], outros, [26, 50, 34])
ws4 = wb.create_sheet("Não postar"); sheet(ws4, ["Data antiga", "Post", "Onde está", "Decisão"], arq, [14, 50, 30, 60])
ws5 = wb.create_sheet("Como postar")
passos = [["Passo", "O que fazer"],
 ["1", "No Instagram, toque no + e escolha Reels. Escolha o vídeo do dia (está no chat e na pasta Prévias)."],
 ["2", "Toque em Editar capa e escolha a imagem da capa do dia (link na coluna Capa)."],
 ["3", "Adicione a música indicada, no volume da coluna Música."],
 ["4", "Cole a legenda e as hashtags."],
 ["5", "Em Configurações avançadas, ligue Reel de teste."],
 ["6", "Programe para o horário da planilha. Se não der, poste no horário."],
 ["7", "Poste os stories do dia ao longo do dia."],
 ["8", "Depois de 72 h, veja visualizações e envios. Se passou da sua média, toque em Compartilhar com seguidores e mude a Situação."],
 ["Regra", "1 reel de teste por dia até o balanço de 04/12. Palavra no direct: só PAUSA. Nunca texto em cima do rosto."]]
for p in passos: ws5.append(p)
for c in ws5[1]: c.font = hf; c.fill = hfill
for row in ws5.iter_rows(min_row=2):
    for c in row: c.font = body; c.alignment = wrap
ws5.column_dimensions["A"].width = 8; ws5.column_dimensions["B"].width = 100
wb.save(OUT); print("ok")
