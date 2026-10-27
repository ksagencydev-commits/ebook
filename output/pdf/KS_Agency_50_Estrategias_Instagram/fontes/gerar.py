from pathlib import Path
import json, shutil, subprocess, math
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image, ImageDraw, ImageFilter
ROOT=Path(__file__).resolve().parent.parent
A=ROOT/'fontes/assets'
pdfmetrics.registerFont(TTFont('M',str(A/'manrope-regular.ttf')))
pdfmetrics.registerFont(TTFont('B',str(A/'manrope-semibold.ttf')))
NAVY='#080E1B'; BLUE='#4384F5'; INK='#17243A'; MUTED='#52647A'; LIGHT='#EAF1FC'
W,H=595.2756,841.8898
C=canvas.Canvas(str(ROOT/'KS_Agency_50_Estrategias_Instagram.pdf'),pagesize=(W,H))
C.setTitle('50 Estratégias para Atrair Clientes pelo Instagram | KS Agency'); C.setAuthor('KS Agency'); C.setSubject('Guia prático para pequenos negócios')
page=0; y=0; bounds=[]; md=[]
groups=['Otimização do perfil','Conteúdo que atrai clientes','Reels e vídeos curtos','Stories e relacionamento','Autoridade e confiança','Estratégias locais','Engajamento e comunidade','Promoções e ofertas','Conversão em clientes','Crescimento e melhoria contínua']
def txt(s,x,y,size=11,color=INK,font='M'):
 C.setFillColor(HexColor(color)); C.setFont(font,size); C.drawString(x,y,s)
def para(s,size=11.5,color=INK,space=12,width=487,x=54,font='M'):
 global y
 p=Paragraph(s,ParagraphStyle('p',fontName=font,fontSize=size,leading=size*1.48,textColor=HexColor(color)))
 _,h=p.wrap(width,720); p.drawOn(C,x,y-h); bounds.append((page,y-h,y,s[:45])); y-=h+space
 if y<65: raise ValueError(('overflow',page,y,s))
def new(label='',dark=False,key=None):
 global page,y
 if page: C.showPage()
 page+=1; C.setFillColor(HexColor(NAVY if dark else '#FFFFFF')); C.rect(0,0,W,H,fill=1,stroke=0)
 if key: C.bookmarkPage(key); C.addOutlineEntry(label,key,0,False)
 txt('KS AGENCY / GUIA DE AÇÃO',54,H-36,8,'#A0AABB' if dark else MUTED,'B')
 txt(label.upper(),54,H-53,8,'#A0AABB' if dark else MUTED)
 C.setStrokeColor(HexColor('#24324A' if dark else '#DFE6F0')); C.line(54,49,W-54,49)
 txt('KS Agency',54,31,8,'#A0AABB' if dark else MUTED); txt(f'{page:02}',W-73,31,9,'#A0AABB' if dark else MUTED)
 if page>2:
  C.linkRect('', 'sumario',(W-130,22,W-85,43),relative=0,thickness=0); txt('SUMÁRIO',W-133,31,7,'#A0AABB' if dark else MUTED)
 y=H-96

def heading(k,title,subtitle=None):
 para(k.upper(),9,BLUE,14,font='B'); para(title,29,INK,20,font='B')
 if subtitle: para(subtitle,12,MUTED,22)
def block(label,text,fill=LIGHT):
 global y
 p=Paragraph(text,ParagraphStyle('box',fontName='M',fontSize=11,leading=16,textColor=HexColor(INK)))
 _,h=p.wrap(455,600); height=h+48
 C.setFillColor(HexColor(fill)); C.roundRect(54,y-height,487,height,7,fill=1,stroke=0)
 txt(label,70,y-20,8,BLUE,'B'); p.drawOn(C,70,y-36-h); y-=height+15
 bounds.append((page,y+15,y+15+height,label))
 if y<65: raise ValueError(('box overflow',page,y,label))
def opener(num,title,line,key):
 global y
 new(title,True,key); txt(num,52,610,120,BLUE,'B'); y=470
 para(title,36,'#FFFFFF',28,font='B'); para(line,16,'#BDCCE2',30,width=420)
 C.setStrokeColor(HexColor(BLUE)); C.line(54,180,230,180)

new('Capa / 2026',True,'capa')
C.setFillColor(HexColor(NAVY)); C.rect(0,0,W,H,fill=1,stroke=0)
C.drawImage(str(A/'capa-fornecida.png'),0,0,width=W,height=H,preserveAspectRatio=True,anchor='c')
# Searchable title behind the supplied raster cover.
t=C.beginText(54,400); t.setFont('M',12); t.setTextRenderMode(3)
t.textLine('50 Estratégias para Atrair Clientes pelo Instagram')
t.textLine('KS Agency - Guia prático para pequenos negócios - Edição 2026')
C.drawText(t)
new('Navegação',key='sumario'); heading('Seu mapa de leitura','Da primeira visita<br/>à próxima oportunidade.','Clique nos tópicos para ir à página. Use “Sumário” no rodapé para voltar.')
toc=[('01 / Boas-vindas',3,'welcome'),('02 / Preparando seu perfil',4,'prep'),('03 / As 50 estratégias',6,'estrategias')]
for i,g in enumerate(groups): toc.append((f'{i*5+1:02}-{i*5+5:02} / {g}',7+i*5,f'g{i}'))
toc += [('04 / Materiais bônus',57,'bonus'),('Checklist de perfil profissional',58,'check'),('Plano de ação de 30 dias',59,'plano'),('20 ideias de posts',61,'ideias'),('Acompanhamento de resultados',65,'resultados'),('Notas e referências',66,'refs'),('KS Agency / Próximos passos',67,'fim')]
for label,p,k in toc:
 txt(label,54,y,10,INK); txt(str(p),515,y,10,BLUE,'B'); C.linkRect('',k,(54,y-6,541,y+13),relative=0,thickness=0); y-=23
new('01 / Boas-vindas',key='welcome'); heading('01 / Boas-vindas','Seu perfil tem uma função: facilitar conexões úteis.')
para('Um guia prático para transformar seu perfil comercial em uma ferramenta de atração, relacionamento e vendas.',12,MUTED,20)
para('Bem-vindo ao guia da KS Agency. Este material foi criado para quem precisa divulgar o próprio negócio e conciliar conteúdo com produção, atendimento e gestão. Você não precisa aplicar tudo de uma vez.')
para('O Instagram pode ser um canal de descoberta, relacionamento e oportunidades comerciais. Uma pessoa encontra uma publicação, visita seu perfil, entende o que você oferece e decide se deseja conversar. Cada etapa precisa de informação clara e de um atendimento preparado.')
block('COMO USAR ESTE GUIA','Prepare o perfil, escolha três estratégias ligadas ao seu maior desafio e coloque-as em prática por um período definido. Registre o que aconteceu antes de ampliar a rotina.')
para('Se o negócio ainda é pouco conhecido, comece por dúvidas, demonstrações e contexto local. Se as pessoas chegam, mas não entram em contato, revise a apresentação e o caminho para o atendimento. Se há conversas sem avanço, investigue informações ausentes e adequação da oferta.')
block('ERRO COMUM','Medir sucesso apenas por seguidores. Um público menor e compatível com sua oferta pode gerar conversas mais pertinentes, mas nenhuma ação deste guia garante vendas ou crescimento.')
para('Todos os exemplos de negócios são hipotéticos e servem para adaptação. Não representam clientes, resultados ou depoimentos da KS Agency.',10,MUTED)
new('02 / Preparando seu perfil',key='prep'); heading('02 / Preparação','Uma vitrine que explica<br/>o que você faz.','Antes de atrair mais visitas, organize o básico.')
for title,text in [('Tipo de conta','Avalie uma conta profissional apropriada ao negócio e confira as ferramentas disponíveis no seu painel. Recursos e elegibilidade variam; não é necessário decorar caminhos de menus.'),('Foto e identificação','Use a logo legível ou um retrato profissional, conforme a forma como o negócio é reconhecido. Mantenha nome de usuário simples e nome de exibição que ajude a entender sua atividade.'),('Biografia e região','Diga o que oferece, para quem e onde atende. Para serviços remotos, informe a modalidade. Evite descrições genéricas que poderiam servir para qualquer empresa.'),('Contato e confiança','Defina o destino do link, explique a próxima ação e mantenha horários e informações comerciais atualizados. Não exponha dados pessoais sem necessidade.')]:
 para(title,15,INK,6,font='B'); para(text)
block('COLOQUE EM PRÁTICA','Peça a alguém que não conhece o negócio para localizar sua oferta, região e contato. Observe onde a pessoa hesita antes de explicar qualquer coisa.')
new('02 / Checklist inicial'); heading('Antes de publicar','Deixe a casa pronta.')
checks=['Foto reconhecível mesmo em tamanho pequeno.','Nome e usuário fáceis de ler e lembrar.','Bio com serviço, público e região ou modalidade.','Link principal testado no celular.','Destaques com serviços, dúvidas e forma de comprar.','Identidade visual com contraste e textos legíveis.','Feed com exemplos, explicações e ofertas atuais.','Localização e horários conferidos.','Serviços e condições descritos com clareza.','Rotina de resposta compatível com sua disponibilidade.']
for s in checks: para('[  ] '+s,12,INK,14)
block('DICA DA KS AGENCY','Consistência não exige um feed em mosaico. Repita cores e estilos de títulos, mantenha boa leitura e preserve a liberdade de publicar informações úteis.')
opener('03','50 estratégias.<br/>Um passo por vez.','Escolha o grupo que resolve seu desafio atual. Cada página termina com uma tarefa pequena e executável.','estrategias')
rows=[]
for i,line in enumerate((ROOT/'fontes/conteudo.txt').read_text().splitlines(),1):
 parts=line.split('|'); assert len(parts)==7,(i,len(parts)); title,what,why,steps,example,tip,task=parts
 rows.append(dict(numero=i,titulo=title,o_que_e=what,por_que_funciona=why,como_aplicar=steps.split(';'),exemplo=example,dica=tip,tarefa=task))
 gi=(i-1)//5; new(f'{gi+1:02} / {groups[gi]}',key=f'g{gi}' if (i-1)%5==0 else None)
 heading(f'ESTRATÉGIA {i:02} / {groups[gi]}',title)
 for label,text in [('O que é?',what),('Por que funciona?',why)]:
  para(label,11,BLUE,4,font='B'); para(text,11.5,INK,14)
 para('Como aplicar',11,BLUE,7,font='B')
 for j,step in enumerate(steps.split(';'),1): para(f'{j}. {step}.',11.5,INK,6)
 y-=8; block('EXEMPLO PRÁTICO / HIPOTÉTICO',example)
 para('DICA DA KS AGENCY',8,BLUE,5,font='B'); para(tip,11,INK,12)
 block('COLOQUE EM PRÁTICA',task)
 md.append(f'## Estratégia {i:02} - {title}\n\n### O que é?\n{what}\n\n### Por que funciona?\n{why}\n\n### Como aplicar\n'+ '\n'.join(f'{j}. {s}.' for j,s in enumerate(steps.split(';'),1))+f'\n\n### Exemplo prático (hipotético)\n{example}\n\n### Dica da KS Agency\n{tip}\n\n### Coloque em prática\n{task}\n')
assert len(rows)==50
opener('04','Da leitura<br/>para a rotina.','Quatro ferramentas para organizar o perfil, planejar ações e acompanhar o que merece atenção.','bonus')
new('Bônus 1 / Checklist profissional',key='check'); heading('Bônus 01','Checklist de perfil<br/>profissional','Marque apenas depois de testar. Revise quando mudar sua oferta.')
for title,items in [('Identificação',['Foto e nome reconhecíveis','Atividade e público claros na bio','Região, modalidade e horários atualizados']),('Percurso de compra',['Link funcional com destino claro','Serviços e condições compreensíveis','Destaques organizados e atualizados','Publicações de apresentação fáceis de encontrar']),('Conteúdo e atendimento',['Contraste, legendas e leitura conferidos','Imagens e depoimentos com autorização','Respostas com contexto e próxima ação','Registro de contatos e resultados organizado'])]:
 para(title,14,BLUE,9,font='B')
 for s in items: para('[  ] '+s,11.5,INK,9)
block('TESTE FINAL','Abra o perfil no celular, percorra o caminho até o contato e registre um ajuste prioritário. Data da revisão: ____ / ____ / ______.')
actions=['Defina público, oferta principal e região atendida.','Revise nome, usuário e foto do perfil.','Reescreva a bio com uma ação clara.','Teste o link principal até a tela de atendimento.','Organize um destaque sobre como comprar.','Escolha conteúdos de apresentação para destacar.','Registre os indicadores iniciais disponíveis.','Liste cinco dúvidas recebidas no atendimento.','Escreva um post respondendo à dúvida principal.','Registre uma etapa dos bastidores com segurança.','Prepare uma demonstração de produto ou serviço.','Grave uma resposta curta com legendas revisadas.','Publique uma enquete com propósito definido.','Revise respostas e anote uma hipótese de conteúdo.','Organize o que será publicado na próxima semana.','Monte um carrossel educativo de cinco telas.','Peça autorização para divulgar uma avaliação real.','Apresente um trabalho com contexto e limites.','Publique uma orientação sobre a região atendida.','Liste parceiros locais e desenhe uma colaboração.','Reserve uma pausa para revisar esforço e agenda.','Reescreva uma oferta com condições transparentes.','Atualize uma ficha de produto ou serviço.','Prepare três respostas adaptáveis para o atendimento.','Revise interessados e faça só as retomadas combinadas.','Planeje um teste com uma variável e um indicador.','Produza uma sequência de stories com uma ação final.','Preencha o quadro de resultados do período.','Compare sinais e escolha um ajuste prioritário.','Monte o calendário do próximo mês com o que aprendeu.']
for half in range(2):
 new('Bônus 2 / Plano de 30 dias',key='plano' if half==0 else None); heading('Bônus 02',f'30 dias de ação / {half+1} de 2','Reserve cerca de 15 a 30 minutos por tarefa. Adapte o ritmo à operação; os dias de revisão também fazem parte do plano.')
 for d in range(half*15,(half+1)*15):
  para(f'<font color="{BLUE}"><b>{d+1:02}</b></font>  {actions[d]}',11.5,INK,13)
 para('Não é necessário publicar todos os dias. Use as tarefas de produção para formar uma reserva de conteúdo e publique quando puder atender a demanda.',10,MUTED)
ideas=[('A dúvida que mais aparece','Carrossel','Esclarecer','Você também tem esta dúvida?','Salve para consultar.'),('Um produto em uso','Vídeo curto','Demonstrar','Veja como este item funciona na rotina.','Envie sua dúvida sobre o uso.'),('O que está incluído','Carrossel','Apresentar escopo','O que você recebe ao contratar?','Consulte as opções pelo contato do perfil.'),('Um cuidado de bastidor','Stories','Gerar confiança','Este detalhe acontece antes da entrega.','Responda se quer conhecer outra etapa.'),('Como escolher entre duas opções','Carrossel','Apoiar decisão','Qual opção combina com sua necessidade?','Conte qual é seu uso previsto.'),('Como chegar ou consultar a região','Foto e legenda','Orientar','Atendemos sua região? Veja como confirmar.','Informe seu bairro no atendimento.'),('Pergunta sobre preferência','Enquete','Ouvir','Qual destas situações acontece com você?','Vote na opção mais próxima.'),('História de uma decisão','Foto e legenda','Aproximar','Mudamos este processo por um motivo.','Compartilhe sua experiência nos comentários.'),('Avaliação real autorizada','Post estático','Gerar confiança','Uma experiência de quem já comprou.','Veja como funciona nosso atendimento.'),('Três cuidados de conservação','Carrossel','Educar','Como cuidar do seu produto depois da compra.','Salve estas orientações.'),('Uma etapa do serviço','Vídeo curto','Explicar processo','O que acontece nesta parte do trabalho?','Envie uma dúvida sobre a etapa.'),('Dúvida sobre prazo','Stories','Reduzir incerteza','De que depende o prazo da sua encomenda?','Consulte o prazo para sua necessidade.'),('Um erro frequente de escolha','Carrossel','Orientar','Antes de escolher, confira este detalhe.','Envie o post a quem está pesquisando.'),('Oferta com condições claras','Post estático','Apresentar oferta','Uma opção para quem precisa de [necessidade].','Consulte a disponibilidade atual.'),('Checklist antes de contratar','Carrossel','Preparar contato','O que separar antes de pedir um orçamento.','Salve e envie as informações pelo contato.'),('Apresentação de quem atende','Foto e legenda','Humanizar','Quem conversa com você por aqui?','Conte o que gostaria de saber sobre o serviço.'),('Novidade com demonstração','Reel','Apresentar lançamento','Veja os detalhes da nova opção.','Peça medidas e condições no atendimento.'),('Uma parceria útil','Publicação conjunta','Ampliar descoberta','Duas soluções para organizar a mesma ocasião.','Conheça os serviços de cada participante.'),('Antes e depois contextualizado','Carrossel','Mostrar trabalho','O que mudou neste projeto e por quê?','Consulte a avaliação para o seu caso.'),('Resumo de dúvidas da semana','Stories','Relacionar','Reunimos respostas que podem ajudar você.','Envie uma pergunta para a próxima edição.')]
for part in range(4):
 new('Bônus 3 / Ideias de posts',key='ideias' if part==0 else None); heading('Bônus 03',f'20 ideias de posts / {part+1} de 4','Adapte os ganchos à sua oferta. Os convites são sugestões, sem obrigação de pedir engajamento em toda publicação.')
 for j in range(part*5,(part+1)*5):
  theme,fmt,obj,hook,cta=ideas[j]; para(f'{j+1:02} / {theme}',14,BLUE,6,font='B'); para(f'<b>Formato:</b> {fmt} · <b>Objetivo:</b> {obj}<br/><b>Gancho:</b> “{hook}”<br/><b>CTA:</b> {cta}',11,INK,20)
new('Bônus 4 / Resultados',key='resultados'); heading('Bônus 04','Acompanhe o percurso<br/>completo.','Período: ____ / ____ a ____ / ____     |     Objetivo: __________________')
metrics=['Visitas ao perfil','Alcance','Interações','Cliques no link','Conversas iniciadas','Orçamentos solicitados','Vendas atribuíveis ao Instagram']
top=y; col=[54,315,390,465,541]
C.setFillColor(HexColor(LIGHT)); C.rect(54,top-31,487,31,fill=1,stroke=0)
txt('INDICADOR',64,top-20,9,BLUE,'B')
for i in range(3): txt(f'PER. {i+1}',col[i+1]+8,top-20,8,BLUE,'B')
y-=31
for name in metrics:
 C.setStrokeColor(HexColor('#DFE6F0')); C.line(54,y-24,541,y-24); txt(name,64,y-16,9.2); y-=24
for x in col: C.line(x,top,x,y)
y-=22
para('Use semanas ou meses de mesma duração. Identifique as datas de cada coluna e anote separadamente publicações impulsionadas, mudanças de oferta e feriados.',11)
para('Visitas, alcance, interações e cliques devem seguir a definição exibida no painel da conta. Interações podem reunir ações diferentes: registre o que você está somando. Nem todas as métricas estarão disponíveis da mesma forma em todas as contas.',11)
para('Conte conversas e orçamentos com um critério estável e sem duplicar o mesmo pedido. Para vendas, pergunte como a pessoa chegou e registre apenas as identificáveis. Uma venda pode envolver vários canais; não atribua toda a receita ao Instagram.',11)
block('LEIA EM CONJUNTO','Mais alcance sem contatos? Investigue adequação do público e clareza da oferta. Mais contatos sem orçamentos? Revise a qualificação e as respostas. Trate isso como pistas, não como prova de causa.')
new('Notas e referências',key='refs'); heading('Notas de uso','Um guia para adaptar<br/>e revisar.')
para('Este material reúne recomendações editoriais e de marketing, sem estatísticas de desempenho ou garantias de resultado. Os exemplos são hipotéticos. A execução depende da oferta, da região, da capacidade de atendimento e do contexto de cada negócio.')
para('Funcionalidades, nomes de métricas, disponibilidade de áudio e regras do Instagram podem mudar por conta, região ou versão. Confira as informações na Central de Ajuda e no próprio aplicativo antes de usar um recurso. Este produto é independente e não possui vínculo ou parceria oficial com Instagram ou Meta.')
para('Consulta oficial',15,BLUE,10,font='B')
para('Instagram / Central de Ajuda. Referência para verificar ferramentas profissionais, publicações e métricas disponíveis.<br/><link href="https://help.instagram.com/" color="#326FE2">https://help.instagram.com/</link>',11)
para('Identidade e fontes',15,BLUE,10,font='B')
para('Logo fornecida pela usuária para esta edição, preservada integralmente e aplicada sem recorte ou redesenho. Paleta editorial derivada do site: azul-marinho #080E1B e azul #4384F5. A aplicação mantém a proporção da marca, sem redesenho.',11)
para('Tipografia Manrope, distribuída com a licença SIL Open Font License no pacote de fontes. Arquivo de licença incluído nos arquivos-fonte. Conteúdo original desenvolvido para este produto.',11)
block('ANTES DA COMERCIALIZAÇÃO','Confirme os contatos institucionais e preencha a última página no arquivo-fonte. Faça a revisão editorial final e valide as condições da oferta na plataforma de venda. Edição: outubro de 2026.')
new('KS Agency',True,'fim'); C.drawImage(str(A/'logo-ks-agency-fornecida.png'),54,650,width=147,height=147*691/838,mask='auto',preserveAspectRatio=True); y=605
para('SEU NEGÓCIO PODE IR ALÉM DO INSTAGRAM.',34,'#FFFFFF',26,font='B')
para('O Instagram é uma parte da presença digital do seu negócio. A KS Agency desenvolve soluções digitais para ajudar empresas a se apresentarem profissionalmente, organizarem seus processos e criarem novas oportunidades.',14,'#BDCCE2',30)
for s in ['Criação de sites profissionais','Desenvolvimento de sistemas personalizados','Soluções para presença digital','Marketing e estratégias digitais']: para('• '+s,13,'#FFFFFF',12)
y-=10
for s in ['Instagram oficial: __________________________________','Site oficial: _______________________________________','WhatsApp comercial: _______________________________']: para(s,11,'#BDCCE2',14)
para('QR Code / área reservada para inclusão após confirmar o destino oficial.',9,'#BDCCE2',10,width=360)
C.setStrokeColor(HexColor(BLUE)); C.rect(466,108,66,66,stroke=1,fill=0); txt('QR CODE',474,137,8,'#BDCCE2')
assert page==67,page
C.save()
(ROOT/'fontes/estrategias.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
(ROOT/'fontes/estrategias.md').write_text('# 50 Estratégias para Atrair Clientes pelo Instagram\n\nKS Agency\n\n'+'\n'.join(md))
(ROOT/'fontes/bonus.json').write_text(json.dumps({'plano_30_dias':actions,'ideias_de_posts':[dict(tema=a,formato=b,objetivo=c,gancho=d,cta=e) for a,b,c,d,e in ideas]},ensure_ascii=False,indent=2))
(ROOT/'fontes/limites_layout.json').write_text(json.dumps(bounds))
print('PDF criado:',page,'páginas;',len(rows),'estratégias')
