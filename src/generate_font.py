#!/usr/bin/env python3
"""FonteCursiva v0.3.2 — connected cursive system prototype.

Design rule: every connected glyph begins at JOIN_IN=(0, JOIN_Y) and ends at
JOIN_OUT=(advance, JOIN_Y). This makes the baseline connector geometrically
continuous across glyph boundaries instead of relying on visual overlap.
"""
from __future__ import annotations
import argparse, math
from pathlib import Path
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

UPM=2048
S=UPM/1000.0
VERSION='0.3.2'
BASELINE=0
X_HEIGHT=285
ASCENDER=650
CAP_HEIGHT=700
DESCENDER=-210
JOIN_Y=72
TRACE_SPACING=76
TRACE_RADIUS=10.0
MODEL_SPACING=9
MODEL_RADIUS=22

ADV={'C':560,'c':350,'a':405,'t':300,'r':350,'i':225,'n':420}

def cubic(p0,p1,p2,p3,n=55):
    out=[]
    for i in range(n+1):
        t=i/n;u=1-t
        out.append((u**3*p0[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t**3*p3[0],
                    u**3*p0[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t**3*p3[1]))
    return out

def seg(a,b,c,d): return cubic(a,b,c,d)
def chain(*segments):
    out=[]
    for s in segments:
        out.extend(s if not out else s[1:])
    return out

def ln(a,b,n=24): return [(a[0]+(b[0]-a[0])*i/n,a[1]+(b[1]-a[1])*i/n) for i in range(n+1)]

def scpath(path): return [(x*S,y*S) for x,y in path]

def rs(path,spacing):
    if not path: return []
    pts=[path[0]]; remain=spacing; prev=path[0]
    for cur in path[1:]:
        while True:
            dx,dy=cur[0]-prev[0],cur[1]-prev[1]; d=math.hypot(dx,dy)
            if d<1e-9: break
            if d<remain:
                remain-=d; prev=cur; break
            q=remain/d; prev=(prev[0]+dx*q,prev[1]+dy*q); pts.append(prev); remain=spacing
    if math.hypot(pts[-1][0]-path[-1][0],pts[-1][1]-path[-1][1]) > spacing*0.42:
        pts.append(path[-1])
    return pts

def circle(pen,x,y,r,steps=18):
    ps=[(x+math.cos(2*math.pi*i/steps)*r,y+math.sin(2*math.pi*i/steps)*r) for i in range(steps)]
    pen.moveTo(ps[0])
    for p in ps[1:]: pen.lineTo(p)
    pen.closePath()

# One continuous main stroke per lowercase glyph. Separate strokes only for dot/crossbar.
# All main strokes start at x=0,y=JOIN_Y and terminate exactly at x=advance,y=JOIN_Y.
STROKES={}

STROKES['c']=[chain(
    seg((0,JOIN_Y),(38,86),(75,125),(102,170)),
    seg((102,170),(137,232),(198,260),(258,248)),
    seg((258,248),(205,267),(130,247),(86,190)),
    seg((86,190),(43,134),(48,60),(116,31)),
    seg((116,31),(195,0),(274,26),(350,JOIN_Y)),
)]

STROKES['a']=[chain(
    seg((0,JOIN_Y),(35,88),(70,122),(98,165)),
    seg((98,165),(132,225),(193,260),(255,248)),
    seg((255,248),(319,235),(340,169),(318,103)),
    seg((318,103),(294,37),(222,8),(151,34)),
    seg((151,34),(86,59),(76,149),(120,204)),
    seg((120,204),(170,263),(266,263),(307,194)),
    seg((307,194),(326,160),(307,108),(319,78)),
    seg((319,78),(338,47),(370,48),(405,JOIN_Y)),
)]

STROKES['t']=[chain(
    seg((0,JOIN_Y),(40,90),(75,127),(102,173)),
    seg((102,173),(122,280),(145,490),(163,635)),
    seg((163,635),(169,682),(190,684),(191,627)),
    seg((191,627),(180,447),(166,238),(168,112)),
    seg((168,112),(171,88),(192,72),(216,69)),
    seg((216,69),(239,67),(265,69),(300,JOIN_Y)),
), ln((102,392),(254,405))]

STROKES['r']=[chain(
    seg((0,JOIN_Y),(38,90),(72,128),(100,174)),
    seg((100,174),(118,228),(132,281),(145,314)),
    seg((145,314),(158,268),(184,235),(220,228)),
    seg((220,228),(256,221),(282,232),(294,258)),
    seg((294,258),(289,206),(261,151),(229,111)),
    seg((229,111),(248,84),(278,69),(311,70)),
    seg((311,70),(326,70),(338,72),(350,JOIN_Y)),
)]

STROKES['i']=[chain(
    seg((0,JOIN_Y),(37,90),(70,132),(98,194)),
    seg((98,194),(111,152),(115,101),(110,61)),
    seg((110,61),(123,39),(153,45),(181,59)),
    seg((181,59),(196,67),(210,71),(225,JOIN_Y)),
), [(111,401),(111,401)]]

STROKES['n']=[chain(
    seg((0,JOIN_Y),(37,90),(72,128),(100,174)),
    seg((100,174),(114,226),(128,281),(140,313)),
    seg((140,313),(145,236),(147,149),(146,73)),
    seg((146,73),(160,198),(222,288),(292,286)),
    seg((292,286),(356,284),(371,214),(359,139)),
    seg((359,139),(351,94),(374,65),(420,JOIN_Y)),
)]

# Capital C has a continuous exit at the same connection height.
STROKES['C']=[chain(
    seg((0,JOIN_Y),(48,79),(85,134),(105,235)),
    seg((105,235),(123,505),(271,702),(447,690)),
    seg((447,690),(514,686),(550,644),(530,598)),
    seg((530,598),(506,559),(462,554),(432,580)),
    seg((432,580),(403,607),(405,650),(428,675)),
), chain(
    seg((105,235),(92,110),(156,16),(284,0)),
    seg((284,0),(398,-7),(485,28),(560,JOIN_Y)),
)]

def make_glyph(ch,dotted):
    pen=TTGlyphPen(None)
    spacing=(TRACE_SPACING if dotted else MODEL_SPACING)*S
    radius=(TRACE_RADIUS if dotted else MODEL_RADIUS)*S
    for stroke in STROKES[ch]:
        if len(stroke)==2 and stroke[0]==stroke[1]:
            x,y=stroke[0]; circle(pen,x*S,y*S,radius); continue
        path=scpath(stroke)
        for x,y in rs(path,spacing): circle(pen,x,y,radius)
    return pen.glyph()

def rename(font,family):
    vals={1:family,2:'Regular',3:f'{family};{VERSION}',4:family,5:f'Version {VERSION}',6:family.replace(' ',''),16:family,17:'Regular'}
    table=font['name']
    for rec in table.names:
        if rec.nameID in vals:
            try: rec.string=vals[rec.nameID].encode(rec.getEncoding())
            except Exception: rec.string=vals[rec.nameID].encode('utf-16-be')
    for nid,text in vals.items():
        table.setName(text,nid,3,1,0x409); table.setName(text,nid,1,0,0)

def build(base,out,family,dotted):
    font=TTFont(str(base)); glyf=font['glyf']; hmtx=font['hmtx'].metrics
    cmap={}
    for t in font['cmap'].tables:
        if t.isUnicode(): cmap.update(t.cmap)
    for ch in 'Ccatrin':
        name=cmap[ord(ch)]; glyf[name]=make_glyph(ch,dotted); hmtx[name]=(int(ADV[ch]*S),0)
    font['hhea'].ascent=int(800*S); font['hhea'].descent=int(-220*S)
    font['OS/2'].sTypoAscender=int(800*S); font['OS/2'].sTypoDescender=int(-220*S)
    font['OS/2'].usWinAscent=int(820*S); font['OS/2'].usWinDescent=int(240*S)
    rename(font,family); font.save(str(out))

def preview(base,model,trace,out):
    im=Image.new('RGB',(2000,1280),'white'); d=ImageDraw.Draw(im)
    title=ImageFont.truetype(str(base),38); fm=ImageFont.truetype(str(model),180); ft=ImageFont.truetype(str(trace),180); fs=ImageFont.truetype(str(trace),100)
    d.text((60,25),f'FonteCursiva v{VERSION} — sistema de conexão',font=title,fill='black')
    d.text((60,100),'Catarina',font=fm,fill='black'); d.text((60,330),'Catarina',font=ft,fill='gray')
    d.text((60,590),'Ca   at   ta   ar   ri   in   na',font=fs,fill='gray')
    d.text((60,760),'catarina   Catarina   cat   rat   rain',font=fs,fill='gray')
    y0=1110
    d.line((60,y0,1940,y0),fill='gray',width=1)
    d.line((60,y0-int(X_HEIGHT*S*0.48),1940,y0-int(X_HEIGHT*S*0.48)),fill='lightgray',width=1)
    d.text((60,1020),'join: mesma altura e mesmo ponto geométrico entre glifos',font=title,fill='black')
    im.save(out)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--base-font',type=Path,required=True); ap.add_argument('--output-dir',type=Path,default=Path('dist')); a=ap.parse_args(); a.output_dir.mkdir(parents=True,exist_ok=True)
    model=a.output_dir/f'FonteCursivaModel-v{VERSION}.ttf'; trace=a.output_dir/f'FonteCursivaTrace-v{VERSION}.ttf'; prev=a.output_dir/f'preview-v{VERSION}.png'
    build(a.base_font,model,'FonteCursiva Model 032',False); build(a.base_font,trace,'FonteCursiva Trace 032',True); preview(a.base_font,model,trace,prev)
    print(model); print(trace); print(prev)
if __name__=='__main__': main()
