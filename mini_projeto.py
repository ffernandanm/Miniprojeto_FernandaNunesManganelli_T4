''' 
Mini-projeto Avaliativo - Módulo 1 - Semana 07
Aluna: Fernanda Nunes Manganelli
Turma: T4
Análise Exploratória de Dados (AED) da base Varejo

Eu usei pandas porque nas aulas vimos que ele lê CSV, limpa dados
e faz agrupamentos de um jeito parecido com tabela do Excel.
'''

import os
import pandas as pd

# Caminho do CSV na mesma pasta deste script.
# Assim o código funciona no VS Code sem eu colar um caminho fixo do meu PC. Olhei isso no chat e achei que era bom.
pasta_do_projeto = os.path.dirname(os.path.abspath(__file__))
caminho_csv = os.path.join(pasta_do_projeto, "Base Varejo.csv")


print("=" * 70) #Usei isso para separar os prints no terminal. Achei que ficou mais bonito e mais organizado.
print("SPRINT 1 - Importação dos dados")
print("=" * 70)

# sep=";" porque a planilha brasileira usa ponto e vírgula, não vírgula.
# encoding="utf-8" para os acentos dos nomes dos produtos abrirem certo.
df = pd.read_csv(caminho_csv, sep=";", encoding="utf-8")

print("\nPrimeiras linhas da base:")
print(df.head())

print("\nNúmero de registros e colunas (linhas, colunas):")
print(df.shape)

print("\nNomes das colunas:")
print(df.columns.tolist())

print("\nTipos de dados de cada coluna:")
print(df.dtypes)
print("\nO pandas leu DATA como texto (object/str).")
print("Mais abaixo eu converto essa coluna para datetime.")


print("\n" + "=" * 70) 
print("Diagnóstico de qualidade dos dados")
print("=" * 70)

print("\n1) Valores nulos por coluna:")
print(df.isnull().sum())

print("\n2) Quantidade de linhas duplicadas (iguais em todas as colunas):")
qtd_duplicatas = df.duplicated().sum()
print(qtd_duplicatas)

# A categoria vazia nesta base aparece como #N/D, não como célula em branco.
categorias_sem_nome = df["PR_CAT"].astype(str).str.strip().isin(["#N/D", "", "nan"])
print("\n3) Categorias vazias ou sem informação (#N/D):")
print(categorias_sem_nome.sum())

print("\n4) Nomes de produto sem informação (#N/D):")
produtos_sem_nome = df["PR_NOME"].astype(str).str.strip().isin(["#N/D", "", "nan"])
print(produtos_sem_nome.sum())

# Testo se alguma data está em formato inválido.
datas_teste = pd.to_datetime(df["DATA"], dayfirst=True, errors="coerce")
print("\n5) Datas que não dão para converter:")
print(datas_teste.isna().sum())


print("\n" + "=" * 70)
print("SPRINT 2 e 3 - Limpeza (texto, nulos, duplicatas e datas)")
print("=" * 70)

# Colunas Unnamed vieram vazias por causa de ; extras no final do CSV.
# Trato elas como dimensões físicas sem dado: 100% nulas, então eu removo.
colunas_extras = [coluna for coluna in df.columns if str(coluna).startswith("Unnamed")]
print("\nColunas extras (sem dado nenhum):", colunas_extras)
df = df.drop(columns=colunas_extras)

# Função com if/else, como a rubrica pede para categorias vazias.
def tratar_categoria(valor):
    if pd.isna(valor):
        return "Sem Categoria"
    texto = str(valor).strip()
    if texto == "" or texto == "#N/D" or texto.lower() == "nan":
        return "Sem Categoria"
    else:
        return texto


def tratar_nome_produto(valor):
    if pd.isna(valor):
        return "Sem Nome"
    texto = str(valor).strip()
    if texto == "" or texto == "#N/D" or texto.lower() == "nan":
        return "Sem Nome"
    else:
        return texto


# apply percorre cada linha da coluna e aplica a função.
df["PR_CAT"] = df["PR_CAT"].apply(tratar_categoria)
df["PR_NOME"] = df["PR_NOME"].apply(tratar_nome_produto)

# Textos: tiro espaços extras e deixo maiúsculo para ficar padronizado.
df["CL_GENERO"] = df["CL_GENERO"].astype(str).str.strip().str.upper()
df["CL_SEG"] = df["CL_SEG"].astype(str).str.strip().str.upper()
df["PR_CAT"] = df["PR_CAT"].astype(str).str.strip()
df["PR_NOME"] = df["PR_NOME"].astype(str).str.strip()

print("\nPor que eu NÃO apaguei as linhas sem categoria?")
print("A rubrica pede para preencher com 'Sem Categoria'.")
print("Se eu apagasse, perderia compras reais só porque o produto não foi classificado.")

print("\nNulos nas dimensões do cliente (gênero, estado civil, filhos, segmento):")
print(df[["CL_GENERO", "CL_EC", "CL_FHL", "CL_SEG"]].isnull().sum())
print("Essas colunas não tinham nulo. Não precisei imputar (preencher) nada nelas.")

# Duplicatas: a mesma linha repetida não deve contar duas vezes na análise.
print("\nRemovendo duplicatas exatas...")
linhas_antes = len(df)
df = df.drop_duplicates()
linhas_depois = len(df)
print("Linhas removidas por duplicata:", linhas_antes - linhas_depois)

# dayfirst=True porque as datas estão no padrão brasileiro (dia/mês/ano).
df["DATA"] = pd.to_datetime(df["DATA"], dayfirst=True, errors="coerce")

print("\nTipo da coluna DATA depois da conversão:")
print(df["DATA"].dtype)

# Se ainda sobrar data inválida, eu aviso. Nesta base não sobrou.
if df["DATA"].isna().sum() > 0:
    print("Ainda existem datas inválidas. Vou remover essas linhas.")
    df = df.dropna(subset=["DATA"])
else:
    print("Todas as datas foram convertidas com sucesso.")


print("\n" + "=" * 70)
print("Regra de negócio: identificador da compra (CO_ID)")
print("=" * 70)

# Cada linha é um ITEM da compra.
# Várias linhas com o mesmo CO_ID são produtos da MESMA compra.
# Por isso eu NÃO junto as linhas: eu só confiro se a regra está consistente.

compras = df.groupby("CO_ID").agg(
    clientes_diferentes=("CL_ID", "nunique"),
    datas_diferentes=("DATA", "nunique"),
    qtd_itens=("PR_ID", "count"),
)

compras_com_problema = compras[
    (compras["clientes_diferentes"] > 1) | (compras["datas_diferentes"] > 1)
]

print("Quantidade de compras (CO_ID únicos):", df["CO_ID"].nunique())
print("Compras com cliente ou data inconsistente:", len(compras_com_problema))
print("Média de itens por compra:", round(compras["qtd_itens"].mean(), 2))
print("Como a regra está ok, mantenho os registros separados (um item por linha).")


print("\n" + "=" * 70)
print("Conferência depois da limpeza")
print("=" * 70)
print("Dimensões finais:", df.shape)
print("\nTipos de dados:")
print(df.dtypes)
print("\nNulos restantes:")
print(df.isnull().sum())
print("\nCategorias depois do tratamento:")
print(df["PR_CAT"].value_counts())


print("\n" + "=" * 70)
print("SPRINT 4 - Estatística descritiva: número de filhos (CL_FHL)")
print("=" * 70)

# CL_FHL é dado do CLIENTE, não do produto.
# Se eu calcular na tabela inteira, quem compra mais itens pesa mais na média.
# Por isso primeiro pego 1 linha por cliente.
clientes = df.drop_duplicates(subset=["CL_ID"])
filhos = clientes["CL_FHL"]

print("\nEstatísticas do número de filhos (1 linha por cliente):")
print("Média.........:", round(filhos.mean(), 2))
print("Mediana.......:", filhos.median())
print("Desvio padrão.:", round(filhos.std(), 2))
print("Moda..........:", filhos.mode()[0])
print("Máximo........:", filhos.max())
print("Mínimo........:", filhos.min())
print("Contagem......:", filhos.count())

print("\nO que esses números querem dizer, em linguagem simples:")
print("- Média: valor típico se eu somar todos os filhos e dividir pelos clientes.")
print("- Mediana: o valor do meio. Metade tem isso ou menos.")
print("- Desvio padrão: o quanto os clientes se afastam da média.")
print("- Moda: o valor que mais aparece.")
print("- Máximo e mínimo: o maior e o menor número de filhos na base.")
print("- Contagem: quantos clientes entrei na conta.")


print("\n" + "=" * 70)
print("Agrupamentos (groupby e pivot_table)")
print("=" * 70)

# Agrupamento 1: gênero. nunique no CO_ID conta compras, não itens.
print("\n1) Compras e clientes por gênero:")
agrupamento_genero = df.groupby("CL_GENERO").agg(
    qtd_compras=("CO_ID", "nunique"),
    qtd_clientes=("CL_ID", "nunique"),
    qtd_itens=("PR_ID", "count"),
)
print(agrupamento_genero)

# Agrupamento 2: categoria do produto.
print("\n2) Itens vendidos por categoria:")
agrupamento_categoria = (
    df.groupby("PR_CAT")["PR_ID"]
    .count()
    .sort_values(ascending=False)
)
print(agrupamento_categoria)

# Extra da aula: pivot_table cruza duas colunas, como tabela dinâmica no Excel.
print("\n3) Tabela dinâmica: itens por gênero e categoria:")
tabela_dinamica = pd.pivot_table(
    df,
    values="PR_ID",
    index="PR_CAT",
    columns="CL_GENERO",
    aggfunc="count",
    fill_value=0,
)
print(tabela_dinamica)

# Extra operacional: vendas ao longo do tempo (mês).
df["ANO_MES"] = df["DATA"].dt.to_period("M")
print("\n4) Compras por mês (5 primeiros e 5 últimos):")
compras_por_mes = df.groupby("ANO_MES")["CO_ID"].nunique()
print(compras_por_mes.head())
print("...")
print(compras_por_mes.tail())


print("\n" + "=" * 70)
print("SPRINT 5 - Conclusões da análise")
print("=" * 70)
print(
    """
1) A base bruta contém 96.553 duplicatas exatas. Após a remoção, o volume
   cai para 733.447 itens. Indicadores de quantidade devem usar a base limpa.

2) Alimentos concentra o maior número de itens, seguida por Higiene e
   Limpeza. Bebidas, Pet e Acessórios aparecem em menor volume.

3) Produtos originalmente marcados como #N/D foram classificados como
   'Sem Categoria'. As linhas foram mantidas para não excluir compras reais.

4) No número de filhos (calculado por cliente), moda e mediana são 0 e a
   média é 1,14. A maior parte dos clientes não tem filhos registrados;
   o máximo observado é 4.

5) O grupo feminino apresenta um pouco mais de clientes, compras e itens
   do que o masculino. A comparação é de volume, não de faturamento,
   porque a base não possui coluna de valor.

6) Limitação restante: não há preço nem quantidade explícita. Se alguma
   duplicata representasse duas unidades do mesmo produto, essa informação
   se perde na remoção. Também não é possível calcular faturamento.
"""
)


print("=" * 70)
print("Salvando a base limpa (df_limpo.csv)")
print("=" * 70)

caminho_limpo = os.path.join(pasta_do_projeto, "df_limpo.csv")
df.to_csv(caminho_limpo, sep=";", index=False, encoding="utf-8")
print("Arquivo salvo em:", caminho_limpo)
print("\nFim do script. Para rodar de novo: python mini_projeto.py")