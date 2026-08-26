# Redesign v1 — recomeço tipográfico

## Decisão

O protótipo v0.x foi útil para validar:

- geração de TTF;
- compatibilidade com Windows/Word;
- variante sólida e pontilhada;
- densidade de pontos;
- necessidade de conexões reais entre glifos.

Porém, a construção visual das letras começou a divergir da caligrafia escolar de referência. O redesign v1 recomeça o desenho dos glifos do zero, preservando apenas a infraestrutura técnica e os aprendizados.

## Referência canônica

A imagem de referência extraída do vídeo de caligrafia passa a ser a principal fonte visual para a construção das minúsculas.

Características que devem ser preservadas:

- cursiva escolar tradicional;
- traço simples e pedagógico;
- inclinação leve à direita;
- letras estreitas e fluídas;
- conexões naturais;
- `e` como pequeno laço/gesto semelhante a um `l` reduzido;
- `o` oval com pequeno laço no topo direito;
- `m` e `n` com arcos arredondados;
- `i`, `u` e `w` compartilhando a mesma família de movimento;
- `l`, `b`, `h` e `k` compartilhando uma gramática de ascendentes com laço;
- descendentes `g`, `j`, `y`, `z` seguindo a referência escolar;
- poucos floreios e nenhuma ornamentação que prejudique o aprendizado.

## Estratégia de desenho

Não desenhar palavras primeiro. Construir o alfabeto como famílias de movimentos coerentes.

### Grupo 1 — formas-base

`a c e i l m n o r t u`

### Grupo 2 — ascendentes

`b d f h k`

### Grupo 3 — descendentes

`g j p q y`

### Grupo 4 — restantes

`s v w x z`

Depois disso:

- maiúsculas;
- acentos e cedilha;
- números e pontuação;
- variante Trace derivada exatamente do mesmo esqueleto da versão Model.

## Regra de conexão

A conexão não deve ser obtida apenas por aproximação geométrica fixa. Cada glifo deve ter:

1. ponto de entrada;
2. gesto principal;
3. ponto de saída;
4. tangente de entrada e saída compatível com a escrita cursiva real.

Os pares de letras serão testados visualmente antes da expansão do grupo seguinte.

## Primeira meta

A primeira prova do redesign deve conter apenas:

`a e i l m n o r t u`

E as palavras de QA:

- `menina`
- `lua`
- `amor`
- `rotina`
- `numero`

O objetivo desta prova não é completar o alfabeto; é acertar o DNA visual da escrita antes de escalar.
