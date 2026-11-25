# Registro Instagram e Anúncios: datas, decisões, IDs e colunas de métricas para preencher.
import sys, json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
OUT = sys.argv[1]; AG = json.load(open(sys.argv[2]))
NAVY = "1A2146"; hf = Font(name="Arial", bold=True, color="FFFFFF"); fill = PatternFill("solid", fgColor=NAVY)
body = Font(name="Arial", size=10); wrap = Alignment(wrap_text=True, vertical="top"); inp = Font(name="Arial", size=10, color="0000FF")
thin = Side(style="thin", color="D9D9D9")
def sheet(ws, head, rows, widths, input_from=None):
    ws.append(head)
    for r in rows: ws.append(r)
    for c in ws[1]: c.font = hf; c.fill = fill; c.alignment = Alignment(wrap_text=True, vertical="center")
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.font = inp if (input_from and c.column >= input_from) else body; c.alignment = wrap; c.border = Border(bottom=thin)
    for i, w in enumerate(widths): ws.column_dimensions[chr(65 + i)].width = w
    ws.freeze_panes = "A2"; ws.row_dimensions[1].height = 32
dias = {"24": "Ter", "25": "Qua", "26": "Qui", "27": "Sex", "28": "Sáb", "29": "Dom", "30": "Seg", "01": "Ter", "02": "Qua", "03": "Qui", "04": "Sex", "05": "Sáb", "06": "Dom"}
fala = {"26", "27", "29", "30", "01", "02"}
mus = {"25": "Peaceful Piano (100%)", "28": "Precious Time (100%)", "03": "Peaceful Piano (100%)", "04": "Precious Time (100%)", "05": "Peaceful Piano (100%)", "06": "Precious Time (100%)"}
import datetime as dt
rows = [["24/11/2026", "Ter", "20h", "Nessa sala você não precisa…", "Sem fala", "Postado à mão por ela", "sem música (se não foi colocada no app)", "27/11/2026", "", "", "", "", "", ""]]
for o in AG:
    d = dt.datetime.fromisoformat(o["date"]); k = d.strftime("%d"); c = d + dt.timedelta(days=3)
    rows.append([d.strftime("%d/%m/%Y"), dias[k], d.strftime("%Hh"), o["title"], "Falado" if k in fala else "Sem fala",
                 "Agendado no Metricool (Reel de teste)", "Peaceful Piano (12%, por baixo da voz)" if k in fala else mus[k], c.strftime("%d/%m/%Y"), "", "", "", "", "", ""])
wb = Workbook(); ws = wb.active; ws.title = "Reels"
sheet(ws, ["Data", "Dia", "Hora", "Reel", "Tipo", "Como foi postado", "Música", "Conferir 72 h em", "Visualizações", "Envios", "Salvamentos", "Curtidas", "Foi para o feed? (sim/não)", "Observações"],
      rows, [11, 5, 6, 40, 9, 26, 28, 13, 13, 9, 11, 9, 14, 30], input_from=9)
ads = [["C1", "A distância não é mais desculpa / Sem tempo pra terapia?", "BRASIL · Online · Mulheres 25-55", "Rodada 1", "25/11/2026", "08/12/2026", "6,50", "Ligado", "120250090458600208", "", "", "", "", ""],
       ["D", "Terapia em Cosmópolis (endereço novo)", "COSMÓPOLIS 15 km · Presencial · Mulheres 25-55", "Rodada 1", "25/11/2026", "08/12/2026", "6,50", "Ligado", "120250104563650208", "", "", "", "", ""],
       ["C2", "Esperando sobrar tempo? (horário à noite)", "COSMÓPOLIS 15 km · Presencial · Mulheres 25-55", "Rodada 2", "09/12/2026", "22/12/2026", "6,50", "Pausado", "120250103617570208", "", "", "", "", ""],
       ["E", "Sempre se achou desorganizada? (TDAH)", "BRASIL · Online · Mulheres 25-55", "Rodada 2", "09/12/2026", "22/12/2026", "6,50", "Pausado", "120250104613290208", "", "", "", "", ""]]
ws2 = wb.create_sheet("Anúncios")
sheet(ws2, ["Anúncio", "Tema", "Público", "Rodada", "Início", "Fim", "R$/dia", "Situação", "ID no Meta", "Gasto (R$)", "Alcance", "Conversas no WhatsApp", "Custo por conversa (R$)", "Agendou? / Observações"],
      ads, [8, 38, 36, 10, 11, 11, 8, 10, 20, 11, 10, 12, 13, 30], input_from=10)
for r in range(2, 6): ws2.cell(r, 13).value = f'=IF(L{r}>0,J{r}/L{r},"")'
ws2.append([]); ws2.append(["Campanha", "WhatsApp Consultório · Teste de anúncios · nov-dez 2026 (id 120250090449810208)"])
ws2.append(["Teto", "R$ 400 por mês em todas as campanhas (trava de R$ 400 na campanha). 2 anúncios por vez, R$ 13/dia no total."])
ws2.append(["Pagamento", "Pré-pago, recarga automática de R$ 50 quando o saldo chega a R$ 6. Conta de anúncios 972512623195205."])
dec = [["23/11/2026", "Edição", "Áudio original do microfone, só ganho até -1,2 dB. Cor do iPhone (parede vermelha, pele quente). Sem rosa."],
       ["23/11/2026", "Edição", "Só a versão básica; nada de faixa no topo; nada de texto no rosto ou na testa."],
       ["23/11/2026", "Edição", "Conferir se as falas fazem sentido juntas antes de montar."],
       ["24/11/2026", "Estratégia", "1 Reel de teste por dia; depois de 72 h, o que passar da média vai para o feed. Balanço em 04/12."],
       ["24/11/2026", "Legenda", "Chamada da legenda só com PAUSA (checklist gratuito) por 4 semanas."],
       ["24/11/2026", "Edição", "Gancho grande desde o primeiro quadro, abaixo da legenda; pausas cortadas; CTA 'Manda pra amiga que…'."],
       ["24/11/2026", "Capas", "Rosto sorrindo, sem careta nem olho torto (quadro dos 3 s iniciais)."],
       ["24/11/2026", "Edição", "Listas sem fala com zoom lento em todas as cenas; sem cena de planta parada."],
       ["24/11/2026", "Google", "Post do endereço novo publicado no Google Meu Negócio com foto da sala."],
       ["24/11/2026", "Posts antigos", "Reels Devagar, Véspera e Segurar pausados no Metricool (rascunho). 36 reels de paisagem antigos: não postar."],
       ["25/11/2026", "Agendamento", "12 reels agendados no Metricool como Reel de teste, com música, de 25/11 a 06/12."],
       ["25/11/2026", "Anúncios", "Teto de R$ 400 por mês. Testar 2 anúncios por vez. Rodada 1: C1 + D, ligada em 25/11."],
       ["25/11/2026", "Anúncios", "Nomes claros na campanha, públicos e anúncios (Rodada 1 / Rodada 2)."]]
ws3 = wb.create_sheet("Decisões"); sheet(ws3, ["Data", "Assunto", "Decisão"], dec, [12, 14, 100])
ag = [["27/11/2026", "Conferir se os anúncios continuam rodando (limite de gastos da conta)", "Claude (agendado)"],
      ["27/11/2026 em diante", "Conferir 1 reel por dia, 72 h depois de postado", "Marília"],
      ["02/12/2026", "Balanço da rodada 1 de anúncios (conversas e custo por conversa)", "Claude (agendado)"],
      ["04/12/2026", "Balanço dos reels de teste: mandar visualizações e envios", "Marília + Claude"],
      ["09/12/2026", "Começa a rodada 2 de anúncios", "Claude, com aprovação"],
      ["Até 06/12/2026", "Gravar: almoço em pé, última hora, comparação (15 s cada) + cenas sem fala; mandar IMG_8042", "Marília"]]
ws4 = wb.create_sheet("Próximas datas"); sheet(ws4, ["Quando", "O quê", "Quem"], ag, [20, 80, 22])
arq = [["Planilha de postagens (legendas, stories, capas)", "Google Drive › Revisar antes de postar · 24-11 a 01-12"],
       ["Vídeos finais (reels e anúncios)", "Google Drive, com a data no nome"],
       ["Agendamentos", "App Metricool › Planejamento"],
       ["Anúncios", "Gerenciador de Anúncios do Meta › campanha WhatsApp Consultório"],
       ["Regras e decisões para o Claude", "Skill gestao-instagram-marilia (repositório midia-postagens › skills)"]]
ws5 = wb.create_sheet("Onde está"); sheet(ws5, ["O quê", "Onde"], arq, [45, 80])
wb.save(OUT); print("ok")
