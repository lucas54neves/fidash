import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

df = pd.read_excel("app/data/data.xlsx")

df.fillna({"installments": 1}, inplace=True)

df = df[df.natureza == "PF"]


def categorize(description):
    category_dict = {
        "Apple": "Assinaturas",
        "Pelé Lanches": "Lanchonetes e Restaurantes",
        "Bendito Cookie": "Lanchonetes e Restaurantes",
        "Drogaria Minas Mais": "Saúde",
        "Peg Lev Supermercados": "Alimentação",
        "Alfa Carnes": "Alimentação",
        "Clube Japa": "Lanchonetes e Restaurantes",
        "Panificadora Arte Sabor": "Padarias",
        "Mart Minas": "Alimentação",
        "Floricultura": "Presentes",
        "Panificadora Big Pão": "Padarias",
        "Stratus Internet": "Contas da casa",
        "Ovo Caipira": "Alimentação",
        "Google One": "Assinaturas",
        "Sacolão Popular": "Alimentação",
        "IOF Compra Internacional": "Tarifas bancárias",
        "GitHub": "Assinaturas",
        "Loom Subscription": "Assinaturas",
        "Vivo Easy": "Telefonia",
        "Distribuidora de Gás WM": "Contas da casa",
        "Max": "Assinaturas",
        "Tarifa 2ª via de cartão": "Tarifas bancárias",
        "Godaddy": "Assinaturas",
        "Plano de saúde - Unimed": "Saúde",
        "Amicão": "Pets",
        "Nubank Vida": "Seguros",
        "Google Workspace": "Assinaturas",
        "Rede Tupy": "Transporte",
        "Churrascaria do Gaúcho": "Lanchonetes e Restaurantes",
        "Magazine Luiza - Geladeira": "Eletrodomésticos",
        "Nutrieats": "Lanchonetes e Restaurantes",
        "De Grão em Grão": "Alimentação",
        "Meliplus": "Assinaturas",
        "Ebenezer Pizzaria": "Lanchonetes e Restaurantes",
        "Solyd": "Investimentos",
        "Reforma Casa - Exp. 243": "Manutenção da casa de aluguel",
        "Curso Maia Santos": "Educação",
        "Supermercado ABC": "Alimentação",
        "Rocketseat Anual": "Educação",
    }

    for keyword, category in category_dict.items():
        if keyword in description:
            return category
    return "Outros"


df["category"] = df["description"].apply(categorize)

df = df[["date", "description", "amount", "category"]]

# Convert the date column to datetime if it's not already
df["date"] = pd.to_datetime(df["date"])

df = df[df["date"].dt.month == 8]

# Group by 'category' and count occurrences of 'description'
grouped_df = df.groupby("category")["amount"].sum().reset_index()

grouped_df = grouped_df.sort_values(by="amount", ascending=False)

# Plotar gráfico de barras usando Matplotlib
fig, ax = plt.subplots()
ax.bar(grouped_df["category"], grouped_df["amount"])
bars = ax.bar(grouped_df["category"], grouped_df["amount"])
ax.set_xlabel("Categoria")
ax.set_ylabel("Valor Total")
ax.set_title("Valor Total de Transações por Categoria")

# Inclinando as labels do eixo X
plt.xticks(rotation=45, ha="right")  # Inclinação de 45 graus

# Adicionando os valores em cima de cada barra
for bar in bars:
    yval = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        yval,
        round(yval, 2),
        ha="center",
        va="bottom",
        rotation=45,  # Inclinação das labels em cima das barras
    )

# Exibir o gráfico no Streamlit
st.pyplot(fig)

# Opcional: Exibir o dataframe agrupado
st.dataframe(
    df[df["category"] == "Lanchonetes e Restaurantes"],
)
