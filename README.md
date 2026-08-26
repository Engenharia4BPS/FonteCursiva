# FonteCursiva

Projeto de desenvolvimento de uma fonte cursiva infantil para treino de caligrafia no Windows.

## Objetivo

Criar uma família tipográfica cursiva com foco pedagógico, especialmente para atividades de alfabetização e caligrafia:

- **Model** — versão sólida, usada como referência visual de escrita cursiva;
- **Trace** — versão pontilhada, usada para a criança escrever por cima;
- conexões naturais entre letras, como em escrita cursiva real;
- pontilhado suficientemente espaçado para continuar legível em tamanhos menores;
- suporte futuro a português brasileiro, incluindo acentos e cedilha.

## Direção visual

A fonte deve combinar:

- elegância suave de uma caligrafia manuscrita;
- construção simples e escolar;
- entrada e saída de traço pensadas para conexão entre letras;
- baixa ornamentação para não atrapalhar o aprendizado;
- boa leitura impressa em folhas de exercício.

## Estado atual

Protótipo em desenvolvimento. A primeira palavra usada para validar a cursividade é **Catarina**.

Caracteres experimentais atuais:

`C c a t r i n`

## Estrutura

```text
FonteCursiva/
├── .github/workflows/build-font.yml
├── README.md
├── CHANGELOG.md
├── requirements.txt
├── docs/
│   ├── BUILD.md
│   └── DESIGN.md
└── src/
    └── generate_font.py
```

Os arquivos gerados ficam em `dist/` e não são versionados diretamente.

## Build automático

O GitHub Actions gera automaticamente:

- `FonteCursivaModel-v0.2.3.ttf`
- `FonteCursivaTrace-v0.2.3.ttf`
- `preview-v0.2.3.png`

O resultado é publicado como artifact do workflow **Build font**.

Para detalhes do build local, consulte [`docs/BUILD.md`](docs/BUILD.md).

## Próximas etapas

1. estabilizar a cursividade e as conexões da palavra `Catarina`;
2. validar a densidade do pontilhado em impressão;
3. expandir o alfabeto minúsculo;
4. expandir o alfabeto maiúsculo;
5. adicionar números, pontuação e acentos;
6. criar fichas pedagógicas de treino.

## Uso

Projeto privado e experimental. As fontes de terceiros usadas apenas como referências visuais não devem ser incorporadas ou redistribuídas neste repositório sem verificação das respectivas licenças.
