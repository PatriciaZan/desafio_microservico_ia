# Desafio Microserviço Extração de Metadados

Extração de marcas expecificas, tratamento de dados e normalização.

## 📁 Estrutura de Pastas e Arquitetura

O projeto adota uma **Arquitetura em Camadas (Layered Architecture)**, separando responsabilidades de protocolo (API), regras de negócio (Services), modelos de dados (Models) e persistência (Repository):

```text
├── data/                    # Ponto de entrada de respostas-exemplo.json | Base de dados inicial
├── results/                 # Persistência dos dados, por json e por SQLite
├── DOCS/                    # Documementações do processo de criação
├── src/
│   ├── api/                 # Camada de Apresentação (Rotas HTTP e Endpoints)
│   │   └── app.py           # Inicialização do FastAPI e mapeamento de rotas
│   ├── metrics/             # Regras de cálculo estatístico (Share of Voice, Top Citações)
│   ├── models/              # Modelos de dados e schemas Pydantic de validação
│   ├── repository/          # Camada de Persistência (SQLite / manipulação de dados)
│   ├── services/            # Lógica de negócio (Limpeza, normalização, matcher de menções)
│   ├── config.py            # Configurações globais e constantes (marcas monitoradas, etc.)
│   └── main.py              # Ponto de entrada da aplicação
├── tests/                   # Suíte de testes automatizados com Pytest
│   ├── test_clean_response.py
│   ├── test_clean_text.py
│   ├── test_mention.py
│   ├── test_normalize_datetime.py
│   └── test_normalize_platform.py
├── requirements.txt         # Dependências do projeto
├── pyproject.toml           # Configurações de build e dependências
└── README.md                # Documentação do projeto
```

Por que essa estrutura?

1. **Isolamento de Camadas**: A lógica de detecção de marcas e cálculo de métricas (`services/` e `metrics/`) não possui nenhuma dependência do framework web (api/). Isso facilita a manutenção e permite testar as regras de negócio de forma isolada.

2. **Escalabilidade**: Caso seja necessário trocar o framework web no futuro (ex: de FastAPI para Flask) ou o banco de dados (ex: de SQLite para PostgreSQL), a alteração fica restrita à respectiva camada sem impactar o núcleo da aplicação.

3. **Resiliência a Dados Sujos**: Módulos dedicados à limpeza (`clean_response.py`, `normalize_platform.py`) garantem que dados mal formatados provenientes de scraping automático sejam tratados antes de corromperem as análises.

**Diagrama simples**

```Plaintext
================================================================================
                            FLUXO DA APLICAÇÃO
================================================================================

      [ Arquivo respostas.json ]          [ Requisição POST /respostas ]
                  │                                     │
                  ▼                                     ▼
      ┌───────────────────────────┐             ┌─────────────────────────┐
      │     Camada de Ingestão    │             │    Validação Pydantic   │
      │   (Leitura e Carregamento)│             │   (Schema de Validação) │
      └───────────┬───────────────┘             └───────────┬─────────────┘
                  │                                     │
                  └──────────────────┬──────────────────┘
                                     │
                                     ▼
                       ┌───────────────────────────┐
                       │    Serviço de Limpeza     │
                       │ (Tratamento de dados sujos│
                       │  e normalização de datas) │
                       └─────────────┬─────────────┘
                                     │
                                     ▼
                       ┌───────────────────────────┐
                       │     Motor de Menções      │
                       │ (Busca case-insensitive   │
                       │  das marcas monitoradas)  │
                       └─────────────┬─────────────┘
                                     │
                                     ▼
                       ┌───────────────────────────┐
                       │  Camada de Persistência   │
                       │  ( Armazenamento JSON e   │
                       │        SQLite )           │
                       └─────────────┬─────────────┘
                                     │
                                     ▼
                       ┌───────────────────────────┐
                       │     Camada de API (REST)  │
                       │  Endpoints expostos via   │
                       │      FastAPI / Swagger    │
                       └─────────────┬─────────────┘
                                     │
          ┌──────────────────────────┼──────────────────────────┬───────────────────────────┐
          ▼                          ▼                          ▼                           ▼
 ┌─────────────────┐        ┌─────────────────┐        ┌─────────────────┐        ┌───────────────────┐
 │ GET             │        │ GET             │        │ POST            │        │ GET               │
 │ /share-of-voice │        │ /top-citacoes   │        │ /respostas      │        │ /cache/{endpoint} │
 └─────────────────┘        └─────────────────┘        └─────────────────┘        └───────────────────┘

 ┌─────────────────┐        ┌─────────────────┐        ┌───────────────────┐
 │ GET             │        │ POST            │        │ DELETE            │
 │ /health │       │        │ /analyze        │        │ /cache/{endpoint} │
 └─────────────────┘        └─────────────────┘        └───────────────────┘



```

## Entregas e Requisitos Atendidos

### 1. **Ingestão** O arquivo é carregado a partir da pasta `data/` e passa por validação, com a função de "entrada" sendo `analyze_response`

- Validação de tipo
- Validação das informações
- `clean_response.py` / `clean_text.py` / `cleaning.py` - Limpeza dos dados sujos
- `mentions.py` - Identificação das marcas monitoradas
- `normalize_datetime` - Padronização de datas e horários dos registros
- `normalize_platform` - Padronização dos nomes das plataformas de IA
- `remove_duplicates` - Remoção de respostas duplicadas contidas no JSON
- `validate_response` - Validação de registros individuais

Nota: A API também possui um endpoint /analyze que permite o upload direto de arquivos via requisição HTTP para processamento instantâneo.

---

### 2. **Detecção de menções**: A validação é feita por meio da função `mentions`, ele contém:

- Dicionário de Marcas (`BRAND_ALIASES`)
- Ordenação por Tamanho (`key=len, reverse=True`)
- Busca por Expressões Regulares (`re.finditer`)
- Controle de Sobreposição (`occupied_ranges`)
- Geração de Resultados (`Mention`)

Exemplo prático

Se o texto de entrada for:
`"A Acme Corp e a Zenith anunciaram novidades hoje."`

O código vai processar a string, identificar "Acme Corp" como uma menção à marca Acme e "Zenith" como uma menção à marca Zenith, retornando esses dados de forma organizada para o sistema.

---

### 3. Análise, exposta via API HTTP - Escolha fastAPI (já havia usado antes)

- `GET /share-of-voice?marca=Acme`  
  Retorna o percentual de menções da marca (total e por plataforma). Consulta rápida pelo arquivo de cache `results/share-of-voice.json`
- `GET /top-citacoes?n=5`  
  As principais citações foram classificadas utilizando a relevância do número de vezes citadas somada ao peso do sentimento. Respostas frequentes podem perder relevância se possuírem sentimento negativo, por isso usei o metadado para enriquecer a classificação

```
positivo + 1
neutro + 0
negativo - 0.5
```

- `POST /respostas`
  Adiciona uma nova resposta ao final do arquivo local `data/respostas-exemplo.json`  
  Passando pelas validações para garantir a integridade dos dados.

- `GET /cache/{endpoint}` - Retorna a última pesquisa de um endpoint específico.
- `GET /health` - Retorna a súade da API.
- `POST /analyze` - Permite o envio de arquivos de respostas para retorno rápido do processamento.
- `DELETE  /cache/{endpoint}` - Deleta o histórico local de pesquisas.

---

### 4. Persistência, simples JSON + SQLite

Decidi implementar ambas as abordagens por dois motivos: prática e fallback.

- Atualmente, a persistência em JSON oferece uma visualização imediata dos dados, o que facilita muito a etapa de testes.

- Embora seja viável nesta fase de desenvolvimento, manter múltiplos arquivos descentralizados pode gerar dessincronização. Em um ambiente de produção real, utilizaria apenas o SQLite ou migraria para um banco relacional robusto como o PostgreSQL.

---

### 5. Testes, utilizando pytest

(Esta foi a minha primeira experiência com testes em Python!)

- Foco no Core: Priorizei testar a regra de negócio central, concentrando-me na extração, detecção de menções e normalização dos dados.

- Justificativa: Sem o tratamento correto dos dados brutos, a aplicação inteira falha. Portanto, garantir a confiabilidade do motor de processamento era a prioridade. Os testes de contrato de API foram validados diretamente pela interface interativa do Swagger.

## 💡 O que eu faria com mais tempo?

1. **Containerização (Docker)**: Criar um Dockerfile e um docker-compose.yml para empacotar a aplicação e o banco de dados, facilitando o deploy em qualquer ambiente.
2. **Cobertura de Testes de Integração**: Expandir os testes de ponta a ponta (E2E) simulando requisições HTTP completas nos endpoints da API usando o TestClient do FastAPI.
3. **Uso de Sentimento Avançado** para gerar maior qualidade da classificação.
4. **Separaçã ode funções** melhor estrutura dos arquivos, com distinção clara de suas funções dentro de services. Para escalabilidade.

## 📃 DOCS

Dentro da pasta `DOCS/resumos.md` contém um arquivo onde coloquei de forma "cru" meu processo mental de criação, está mal formatado, geralmente faço algo parecido no papel e caneta.

## 🚀 Como Executar o Projeto

### _Recomendo fortemente rodar o projeto utilizando o PyCharm devido à resolução automática de caminhos de importação de módulos._

1. Clonar o repositório e configurar o ambiente virtual

```bash
    # Crie e ative um ambiente virtual Python
    python -m venv venv
    # No Windows:
    venv\Scripts\activate
    # No Linux/macOS:
    source venv/bin/activate
```

2. Instalar as dependências

```bash
    pip install -r requirements.txt
```

3. Rodar a aplicação

```bash
    uvicorn src.api.app:app --reload
```

_A API estará rodando em http://127.0.0.1:8000/docs com a documentação interativa (Swagger UI)._

## 🧪 Executando os Testes Automatizados

O projeto conta com testes unitários focados nas áreas críticas da aplicação (limpeza de dados, normalizações e detecção de menções). Para rodar os testes, execute:

```bash
    python -m pytest
```

Caso encontre algum aviso ou instabilidade com o pacote pytest no seu ambiente, reinstale as dependências com o comando:

```bash
pip install --force-reinstall pytest
```
