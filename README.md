# Mini-projeto avaliativo — Base Varejo

**Aluna:** Fernanda Nunes Manganelli  
**Turma:** T4 — Visualização de Dados e Business Intelligence  
**Módulo 1 · Semana 07**

Este repositório reúne a análise exploratória da base Varejo. O objetivo é preparar os dados para análises posteriores: verificar a qualidade da base, aplicar a limpeza mínima necessária, calcular estatísticas descritivas e registrar os principais achados.

A base original está disponível no Kaggle ([Base Varejo](https://www.kaggle.com/datasets/namespaiva/base-varejo/data)) e foi incluída nesta pasta como `Base Varejo.csv`.

## Reflexão teórica: ETL e qualidade de dados

ETL descreve o caminho dos dados até um formato confiável para análise:

1. **Extract.** A extração foi feita com `pandas.read_csv`, usando `sep=";"` porque o arquivo segue o padrão brasileiro de separador. O encoding utilizado foi `utf-8`, para preservar os nomes dos produtos.

2. **Transform.** Nesta etapa concentram-se as decisões de qualidade. Foram identificados nulos, duplicatas, datas em formato de texto, categorias sem classificação (`#N/D`) e colunas extras sem conteúdo (`Unnamed`), geradas por delimitdores a mais no CSV. A transformação incluiu:
   - preenchimento de categoria vazia ou inválida com `Sem Categoria`;
   - conversão da coluna `DATA` para `datetime` (`dayfirst=True`);
   - remoção de duplicatas exatas;
   - exclusão das colunas 100% nulas;
   - validação da regra de negócio do identificador de compra (`CO_ID`).

3. **Load.** O resultado foi exportado em `df_limpo.csv`, que representa a base pronta para consulta, agrupamento ou carga em uma ferramenta de visualização.

Qualidade de dados, neste contexto, não se resume a abrir o arquivo. É necessário perguntar se cada linha é única, se a categoria está preenchida de forma útil, se a data é de fato uma data e se `CO_ID` identifica a compra ou o item. Sem esse cuidado, indicadores de volume ficam distorcidos.

**Decisões de tratamento.** Linhas sem categoria não foram excluídas. A exclusão reduziria o número de compras reais apenas por falha de cadastro; por isso o valor foi imputado como `Sem Categoria`. Já as duplicatas exatas foram removidas, para não contar o mesmo registro duas vezes. Resta uma ressalva: na ausência de uma coluna de quantidade, não é possível afirmar se alguma duplicata representava duas unidades do mesmo produto. Também não há coluna de preço, o que impede análise de faturamento.

## Arquivos da pasta

| Arquivo | Conteúdo |
|---|---|
| `mini_projeto.py` | Script da análise, comentado e executável no VS Code |
| `Base Varejo.csv` | Base original |
| `df_limpo.csv` | Base após o tratamento |
| `README_FernandaNunesManganelli_T4.md` | Instruções de execução |

## Como executar

No terminal, a partir desta pasta:

```text
python mini_projeto.py
```

Dependências: Python e a biblioteca pandas.

```text
pip install pandas
```

A saída é impressa no terminal, na ordem dos sprints: importação, diagnóstico, limpeza, estatísticas, agrupamentos e conclusões. No final, o script grava `df_limpo.csv`.

## Insights obtidos

1. A base bruta possui **830.000** registros. Destes registros, **96.553** são duplicatas exatas. Após a limpeza, restaram **733.447** itens. Sem a remoção das duplicatas, qualquer indicador de volume ficaria fora da realidade.

2. **Alimentos** concentra a maior quantidade de itens, seguida por Higiene e Limpeza. 
Bebidas, Pet e Acessórios aparecem em menor volume. Também tem o **Sem Categoria** (registros que na tabela original estavam como `#N/D`), o que indicava falha de cadastro, e não o principal problema da base.

3. A base tem **1.000** clientes e **18.471** compras. Cada `CO_ID` corresponde a uma compra com vários itens. A validação mostrou consistência: um identificador de compra está associado a um único cliente e a uma única data. 

4. As estatísticas de **número de filhos** (`CL_FHL`) foram calculadas sobre os 1.000 clientes, e não sobre as linhas de produto. Calcular na tabela completa daria mais peso a quem compra mais itens. Resultado: **moda e mediana iguais a 0**, **média 1,14**, **desvio padrão 1,41**, **mínimo 0** e **máximo 4**. A média fica acima da mediana porque uma parte dos clientes tem até quatro filhos, enquanto a maior parte não tem filhos.

5. Em relação ao gênero, o **feminino** tem mais de clientes, compras e itens do que o **masculino**. 

6. Limitações que permanecem: ausência de preço, de quantidade e de um dicionário das colunas (por exemplo, o significado de `CL_EC` e `CL_SEG`). Com isso, a análise se restringe ao operacional — o que mais sai em quantidade de itens — e não avança para o financeiro.

## Observação

Os resultados podem variar se a versão da base for atualizada ou se a regra de tratamento de duplicatas for alterada.