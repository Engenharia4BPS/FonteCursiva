#!/usr/bin/env python3
"""Patch experimental para usar Escolar Brasil como base do projeto.

Nesta primeira revisão apenas o glifo `p` minúsculo é substituído. O objetivo é
preservar o restante da fonte original e tornar o `p` inequivocamente cursivo:
haste descendente + bojo inferior + saída para a próxima letra.

Uso pessoal durante o desenvolvimento. Os arquivos TTF originais não são
incluídos neste repositório por este script.
"""
from __future__ import annotations
import argparse, math
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen


def cubic(p0,p1,p2,p3,n=70):
    out=[]
    for i in range(n+1):
        t=i/n; u=1-t
        out.append((u**3*p0[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t**3*p3[0],
                    u**3*p0[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t**3*p3[1]))
    return out


def chain(*segments):
    out=[]
    for s in segments:
        out.extend(s if not out else s[1:])
    return out


CENTER = chain(
    cubic((0,80),(45,95),(90,135),(120,185)),
    cubic((120,185),(145,235),(160,285),(168,325)),
    cubic((168,325),(166,170),(165,-80),(165,-300)),
    cubic((165,-300),(165,-340),(190,-340),(190,-295)),
    cubic((190,-295),(190,-110),(188,95),(186,215)),
    cubic((186,215),(215,285),(290,315),(365,285)),
    cubic((365,285),(425,260),(445,195),(420,135)),
    cubic((420,135),(395,80),(345,40),(285,35)),
    cubic((285,35),(235,30),(205,50),(195,80)),
    cubic((195,80),(220,55),(250,50),(285,52)),
    cubic((285,52),(360,55),(430,78),(500,115)),
)


def resample(path,spacing):
    if not path: return []
    pts=[path[0]]; remain=spacing; prev=path[0]
    for cur in path[1:]:
        while True:
            dx,dy=cur[0]-prev[0],cur[1]-prev[1]
            d=math.hypot(dx,dy)
            if d<1e-9: break
            if d<remain:
                remain-=d; prev=cur; break
            q=remain/d
            prev=(prev[0]+dx*q,prev[1]+dy*q)
            pts.append(prev); remain=spacing
    return pts


def circle(pen,x,y,r,steps=18):
    pts=[(x+math.cos(2*math.pi*i/steps)*r,
          y+math.sin(2*math.pi*i/steps)*r) for i in range(steps)]
    pen.moveTo(pts[0])
    for pt in pts[1:]: pen.lineTo(pt)
    pen.closePath()


def make_p(scale_x=1.0,scale_y=1.0,radius=20,spacing=8):
    pen=TTGlyphPen(None)
    path=[(x*scale_x,y*scale_y) for x,y in CENTER]
    for x,y in resample(path,spacing): circle(pen,x,y,radius)
    return pen.glyph()


def patch(src:Path,dst:Path,kind:str):
    font=TTFont(str(src))
    cmap={}
    for table in font['cmap'].tables:
        if table.isUnicode(): cmap.update(table.cmap)
    gname=cmap[ord('p')]

    if kind=='regular':
        font['glyf'][gname]=make_p(1.05,1.0,20,8)
        font['hmtx'].metrics[gname]=(605,-10)
        family='Escolar Brasil Ajustada P01'
    elif kind=='bold':
        font['glyf'][gname]=make_p(1.00,0.96,31,8)
        font['hmtx'].metrics[gname]=(555,-5)
        family='Escolar Brasil Ajustada Bold P01'
    else:
        font['glyf'][gname]=make_p(1.05,1.0,7.5,42)
        font['hmtx'].metrics[gname]=(605,-10)
        family='Escolar Brasil Trace Ajustada P01'

    names=font['name']
    for nid in (1,4,16):
        names.setName(family,nid,3,1,0x409)
        names.setName(family,nid,1,0,0)
    ps=family.replace(' ','')
    names.setName(ps,6,3,1,0x409)
    names.setName(ps,6,1,0,0)
    font.save(str(dst))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--regular',type=Path,required=True)
    ap.add_argument('--bold',type=Path,required=True)
    ap.add_argument('--trace',type=Path,required=True)
    ap.add_argument('--output-dir',type=Path,default=Path('dist-escolar'))
    args=ap.parse_args()
    args.output_dir.mkdir(parents=True,exist_ok=True)
    patch(args.regular,args.output_dir/'EscolarBrasil-Ajustada-P01.ttf','regular')
    patch(args.bold,args.output_dir/'EscolarBrasil-Bold-Ajustada-P01.ttf','bold')
    patch(args.trace,args.output_dir/'EscolarBrasilTrace-Ajustada-P01.ttf','trace')


if __name__=='__main__':
    main()
