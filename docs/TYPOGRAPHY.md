# Sistema tipográfico — FonteCursiva v0.3

## Referência visual principal

A referência aprovada para o projeto é uma cursiva infantil fluida, leve e contínua, com aparência de escrita manual real. A prioridade é preservar:

- continuidade de gesto;
- ligação natural entre letras;
- pouca ornamentação;
- formas escolares reconhecíveis;
- leve inclinação;
- proporções delicadas;
- versão pontilhada arejada.

A palavra-base de validação continua sendo **Catarina**.

## Mudança estrutural da v0.3

A partir da v0.3, as letras conectadas não são mais desenhadas como glifos independentes apenas aproximados visualmente.

Cada minúscula usa um ponto comum de conexão:

- `JOIN_IN = (0, JOIN_Y)`
- `JOIN_OUT = (advance, JOIN_Y)`

com `JOIN_Y = 72` no sistema de 1000 unidades de projeto.

Isso significa que o ponto final de uma letra coincide geometricamente com o ponto inicial da próxima.

Exemplo:

```text
[a termina] ----●---- [t começa]
                 ^
             mesmo ponto
```

Essa regra deve ser mantida para todas as letras conectáveis.

## Métricas-base

Valores atuais do sistema de desenho em 1000 unidades:

- baseline: `0`
- x-height: `285`
- ascender: `650`
- cap height: `700`
- descender: `-210`
- altura da conexão: `72`

Esses valores ainda podem ser refinados visualmente, mas devem permanecer globais, e não ser ajustados letra por letra sem necessidade.

## Construção dos glifos

Cada minúscula deve ser tratada como um gesto principal contínuo:

1. entrada no ponto comum de conexão;
2. desenvolvimento do corpo da letra;
3. retorno à zona de conexão;
4. saída no ponto geométrico comum.

Traços secundários podem ser separados quando a escrita natural também exige levantamento do lápis, por exemplo:

- ponto do `i`;
- barra do `t`.

## Pares obrigatórios de QA

Antes de aceitar qualquer alteração, verificar:

- `Ca`
- `at`
- `ta`
- `ar`
- `ri`
- `in`
- `na`

Além disso, testar:

- `Catarina`
- `catarina`
- `cat`
- `rat`
- `rain`

O objetivo não é apenas reconhecer as letras, mas observar o **ritmo do conjunto**.

## Versão Trace

A variante pontilhada é derivada exatamente do mesmo esqueleto da versão Model.

Parâmetros iniciais da v0.3:

- espaçamento entre pontos: `76`
- raio do ponto: `10.5`

O espaçamento deve continuar claramente perceptível em 14, 18 e 24 pt impressos.

## Critério de aprovação

Uma letra isolada pode parecer correta e mesmo assim ser rejeitada se quebrar o fluxo da palavra.

A ordem de prioridade é:

1. fluidez da palavra;
2. conexão entre pares;
3. legibilidade escolar;
4. forma isolada do glifo;
5. estética ornamental.

A fonte deve parecer escrita, não montada.
