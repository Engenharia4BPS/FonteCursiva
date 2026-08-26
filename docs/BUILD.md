# Como gerar a fonte

## Build automático no GitHub

O repositório possui um workflow em `.github/workflows/build-font.yml`.

A cada alteração em `src/`, `requirements.txt` ou no próprio workflow, o GitHub Actions:

1. prepara Python 3.12;
2. instala `fonttools` e `Pillow`;
3. instala DejaVu Sans como fonte-base estrutural;
4. executa `src/generate_font.py`;
5. gera os arquivos em `dist/`;
6. publica um artifact chamado `FonteCursiva-v0.2.3`.

Arquivos gerados:

- `FonteCursivaModel-v0.2.3.ttf`
- `FonteCursivaTrace-v0.2.3.ttf`
- `preview-v0.2.3.png`

## Build local

### 1. Criar ambiente Python

```bash
python -m venv .venv
```

No Windows:

```powershell
.venv\Scripts\activate
```

No Linux/macOS:

```bash
source .venv/bin/activate
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Escolher uma fonte-base TrueType

O gerador atual preserva a estrutura completa de uma fonte TTF existente e substitui apenas os glifos experimentais. Isso evita o problema observado no Microsoft Word com fontes TTF mínimas.

No GitHub Actions usamos:

```text
/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf
```

No Windows, informe o caminho de uma fonte TrueType que contenha os caracteres básicos necessários.

### 4. Gerar

```bash
python src/generate_font.py --base-font CAMINHO_PARA_FONTE.ttf --output-dir dist
```

## Estado do protótipo

A versão atual substitui apenas:

`C c a t r i n`

O restante da fonte é mantido a partir da fonte-base. Isso é proposital enquanto validamos o desenho, a cursividade e a compatibilidade com Word.

## Critério de aprovação

Antes de expandir o alfabeto, testar `Catarina` em:

- 48 pt;
- 36 pt;
- 24 pt;
- 18 pt;
- 14 pt.

Os tamanhos menores devem ser avaliados também em impressão para verificar a separação visual dos pontos.
