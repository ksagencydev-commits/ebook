from pathlib import Path
from pypdf import PdfReader
from PIL import Image,ImageDraw,ImageFilter
import json
R=Path(__file__).resolve().parent.parent
pdf=PdfReader(R/'KS_Agency_50_Estrategias_Instagram.pdf')
assert len(pdf.pages)==67
for i in range(50):
 t=pdf.pages[i+6].extract_text()
 assert f'ESTRATÉGIA {i+1:02}' in t
 for x in ['O que é?','Por que funciona?','Como aplicar','EXEMPLO PRÁTICO','DICA DA KS AGENCY','COLOQUE EM PRÁTICA']: assert x in t,(i,x)
links=pdf.pages[1]['/Annots']; assert len(links)==20,len(links)
for i in range(50): assert f'{i//5+1:02} / ' in pdf.pages[i+6].extract_text()
for start in range(0,67,18):
 sheet=Image.new('RGB',(6*310,3*460),'#C9D2DF'); d=ImageDraw.Draw(sheet)
 for idx in range(start,min(start+18,67)):
  im=Image.open(R/f'previas/pagina-{idx+1:02}.png'); im.thumbnail((294,420)); x=(idx-start)%6*310+8; y=(idx-start)//6*460+8; sheet.paste(im,(x,y)); d.text((x,y+425),str(idx+1),fill='#17243A')
 sheet.save(R/f'previas/contato-{start//18+1}.jpg')
# Render a physical book mockup from the actual cover, preserving its design.
cover=Image.open(R/'capa.png').convert('RGB'); cover.thumbnail((690,976))
base=Image.new('RGB',(1600,1200),'#EAF0F9'); shadow=Image.new('RGBA',base.size); sd=ImageDraw.Draw(shadow); sd.rounded_rectangle((447,153,1175,1138),30,fill=(8,14,27,70)); shadow=shadow.filter(ImageFilter.GaussianBlur(28)); base=Image.alpha_composite(base.convert('RGBA'),shadow)
d=ImageDraw.Draw(base); d.polygon([(420,122),(449,105),(449,1081),(420,1102)],fill='#14233C'); d.polygon([(449,1081),(1139,1081),(1110,1102),(420,1102)],fill='#B5BDCB')
for yy in range(1085,1100,3): d.line((445,yy,1112,yy),fill='#DEE4EE')
base.paste(cover,(449,105)); base.convert('RGB').save(R/'mockup_ebook.png')
report={'paginas':67,'estrategias':50,'campos_obrigatorios_por_estrategia':6,'links_no_sumario':len(links),'texto_selecionavel':True,'formato':'A4 vertical','limite_inferior_texto':min(v[1] for v in json.loads((R/'fontes/limites_layout.json').read_text()))}
(R/'fontes/validacao.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)); print(report)
