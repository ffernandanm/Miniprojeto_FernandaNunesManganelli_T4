# Instruções de execução

**Aluna:** Fernanda Nunes Manganelli  
**Turma:** T4  
**Arquivo principal:** `mini_projeto.py`

## Visual Studio Code

1. Abra a pasta `Miniprojeto_FernandaNunesManganelli_T4`.
2. Verifique se o arquivo `Base Varejo.csv` está no mesmo diretório do script.
3. Instale o pandas, caso ainda não esteja disponível: `pip install pandas`
4. Execute no terminal:

```text
python mini_projeto.py
```

5. Acompanhe os resultados impressos no terminal. Ao final da execução, o arquivo `df_limpo.csv` é gerado nesta pasta.

## Google Colab

1. Envie os arquivos `mini_projeto.py` e `Base Varejo.csv` para o ambiente do Colab.
2. Execute o script (ou copie o conteúdo para uma célula e rode em sequência).
3. O CSV precisa estar acessível no mesmo diretório em que o código for executado.

## Resultados apresentados na execução

- Número de registros, colunas e tipos de dados
- Diagnóstico de nulos, duplicatas e categorias `#N/D`
- Etapas de limpeza (categoria, datas e duplicatas)
- Estatísticas descritivas da coluna de número de filhos
- Agrupamentos por gênero e por categoria
- Conclusões da análise