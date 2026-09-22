# Resumos e Anotações Pessoais
Colocando minha "cabeça no papel"

---
### Leitura do desafio
### Analise do Documento .json
## Estruturar a extração/analise e normalização dos dados
1. Preciso normalizar as "sujeiras" como:
- Nomes Inconsistent como:
```
    "plataforma":  ChatGPT | chatgpt | Chat-GPT | chat-gpt | ....
```
- Datas (Transformar para timestamp convencionar = 2026-09-22T10:00:00)
```
    "data_hora": null | 2026-01-15T10:00:00 | 15/01/2026 | ....
```
- Tem um registro duplicado `r003` não posso esquecer disso, pode duplicar o resultado e dar errado
- Respostas vazias ?? no `r005`
Não deve ir para a análise, não faz sentido ir...
```
    "resposta_texto": ""
```
- Cade o modelo do `r004`, mas ainda tem resposta
```
    "modelo": null
```
- Sentimento ausente `r002`
```
    "sentimento": null
```

---

Vou separar em uma camada de limpeza e depois jogar para a análise.
```
                 respostas.json
                       │
                       ▼
                ┌─────────────┐
                │   Ingestão  │
                └──────┬──────┘
                       │
                       ▼
                ┌─────────────┐
                │  Validação  │
                └──────┬──────┘
                       │
                       ▼
                ┌─────────────┐
                │   Limpeza   │
                │ Normalização│
                └──────┬──────┘
                       │
                       ▼
                ┌─────────────┐
                │ Deduplicação│
                └──────┬──────┘
                       │
                       ▼
             dados estruturados
                       │
                       ▼
             ┌──────────────────┐
             │ Análise de       │
             │ menções às marcas│
             └──────────────────┘
```


Terminei uma versão de limpeza e normalizaão que estou satisgeita

---

## Extração dos metadados e informações 

Resposta limpa -> Detector de menções -> Resposta analisada


1. Para extrair as empresas que aparecem eu tenho que considerar:
- Quantas vezes elas aparecem em uma frase
- Como elas aparecem
- Quando aparece mais de 1 
- Tenho que criar um `models` para a resposta desta analize - `analyzed_response.py` OK


## Criação da API com fastAPI

```
GET  /health
POST /analyze
```

- Tenho que liberar a API
- Opção de carregar arquivo
- Opção de retornar os dados processados
- Documentar a API pra deixar legal de usar
---

1. GET /share-of-voice?marca=Acme   
Share of voice mede a presença de uma marca em relação aos concorrentes. (retirado do arquivo json)  
- Preciso do percentual
- Total
- Por plataforma
---

2. GET /top-citacoes?n=5
- usar o sentimento, quando é positivo deve carregar maior peso
- usar o número de menções
- usar o sentimento negativo também pode ser uma boa para "hankiar"

```
    numero de menções 2 + sentimento positivo   = 2 + 1 = 3 
    numero de menções 3 + sentimento neutro     = 3 + 0 = 3 
    numero de menções 1 + sentimento positivo   = 1 + 1 = 2 
    numero de menções 2 + sentimento negativo   = 2 - 0.5 = 1.5
```
---

3. POST /respostas — adicionar uma nova resposta ao conjunto (validando o formato)
- Adicionar uma nova resposta ao JSON - ao final é claro
---

4. Dei uma pausa e vou refatorar o meu app.py contendo a API  
- Separação de Responsabilidades, ta tudo entulhado
- Uso de Injeção de Dependências

## Persistência dos dados
JSOn é bem mais prático para o momento, mas usar o SQLite mostraria que eu sei fazer esta integração....
Vou fazer os dois ?

























