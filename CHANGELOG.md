# Changelog

## v0.3.2 — refinamento da base cursiva

- `t` com retorno inferior mais fechado e saída mais suave;
- `r` com saída mais longa para melhorar a transição para `i`;
- `i` com subida mais alta antes do retorno;
- `n` com arco um pouco mais aberto;
- leve redução do diâmetro dos pontos da variante Trace;
- mantido o sistema geométrico comum de conexão entre glifos;
- validada em teste visual no Microsoft Word em 48 pt e 72 pt.

## v0.3.0 — sistema cursivo conectado

- referência visual consolidada em uma cursiva infantil fluida, leve e contínua;
- definição de métricas globais de baseline, x-height, ascender, cap height, descender e altura de conexão;
- cada minúscula conectável passa a começar e terminar no mesmo ponto geométrico de junção;
- versão Model e Trace passam a derivar do mesmo esqueleto de traço;
- QA passa a incluir pares `Ca`, `at`, `ta`, `ar`, `ri`, `in`, `na` e palavras de teste;
- prioridade de aprovação passa a ser fluidez da palavra antes da beleza isolada do glifo.

## v0.2.3 — protótipo Word

- estrutura TrueType mais compatível com Microsoft Word;
- nomes internos separados para evitar cache de versões anteriores;
- glifos experimentais para `C c a t r i n`;
- foco em validar a palavra `Catarina`.

## v0.2.2

- redesenho do `c` minúsculo em estilo cursivo escolar mais simples;
- prévia limitada aos glifos efetivamente desenhados.

## v0.2.1

- inclusão de `c` minúsculo para melhorar os testes no visualizador do Windows.

## v0.2

- primeira tentativa de ligação cursiva entre as letras de `Catarina`;
- versões sólida e pontilhada.

## v0.1

- prova de conceito de fonte pontilhada instalável no Windows;
- validação do formato TTF e da densidade inicial dos pontos.
