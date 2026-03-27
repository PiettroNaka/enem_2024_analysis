import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# Configurar página
st.set_page_config(page_title="Análise ENEM 2024", layout="wide")

# Configurar matplotlib para português
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# Gerar dados de exemplo (simulando dados reais do ENEM)
@st.cache_data
def generate_sample_data():
    np.random.seed(42)
    n_samples = 5000
    
    data = {
        'Idade': np.random.randint(17, 60, n_samples),
        'Nota CN': np.random.normal(500, 100, n_samples),
        'Nota CH': np.random.normal(510, 95, n_samples),
        'Nota LC': np.random.normal(490, 105, n_samples),
        'Nota MT': np.random.normal(480, 120, n_samples),
        'Nota Redação': np.random.normal(550, 150, n_samples),
        'Sexo': np.random.choice(['Masculino', 'Feminino'], n_samples),
        'Cor/Raça': np.random.choice(['Branco', 'Preto', 'Pardo', 'Amarelo', 'Indígena'], n_samples),
        'Tipo Escola': np.random.choice(['Pública', 'Privada'], n_samples),
        'Localização': np.random.choice(['Urbana', 'Rural'], n_samples),
        'UF': np.random.choice(['SP', 'RJ', 'MG', 'BA', 'PR', 'SC', 'RS', 'DF'], n_samples),
        'Região': np.random.choice(['Sudeste', 'Nordeste', 'Sul', 'Centro-Oeste', 'Norte'], n_samples),
    }
    
    df = pd.DataFrame(data)
    df['Nota Média'] = (df['Nota CN'] + df['Nota CH'] + df['Nota LC'] + df['Nota MT'] + df['Nota Redação']) / 5
    
    # Garantir valores válidos
    for col in ['Nota CN', 'Nota CH', 'Nota LC', 'Nota MT', 'Nota Redação']:
        df[col] = df[col].clip(0, 1000)
    
    df['Nota Redação'] = df['Nota Redação'].clip(0, 1000)
    df['Nota Média'] = df['Nota Média'].clip(0, 1000)
    
    return df

# Carregar dados
df = generate_sample_data()

# Sidebar
st.sidebar.title("Menu de Navegação")
page = st.sidebar.radio("Selecione a página:", [
    "📊 Início",
    "📈 Análise Exploratória",
    "📉 Variáveis Qualitativas",
    "📊 Variáveis Quantitativas",
    "🔗 Correlações",
    "🎯 Amostragem",
    "📋 Comparação Amostra vs População"
])

# Página: Início
if page == "📊 Início":
    st.title("Análise Exploratória dos Dados do ENEM 2024")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Participantes", f"{len(df):,}")
    with col2:
        st.metric("Total de Variáveis", len(df.columns))
    with col3:
        st.metric("Nota Média Geral", f"{df['Nota Média'].mean():.2f}")
    
    st.markdown("---")
    st.subheader("Informações Gerais")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Estatísticas Descritivas - Notas:**")
        notas_cols = ['Nota CN', 'Nota CH', 'Nota LC', 'Nota MT', 'Nota Redação', 'Nota Média']
        st.dataframe(df[notas_cols].describe().round(2))
    
    with col2:
        st.write("**Valores Faltantes:**")
        missing = df.isnull().sum()
        if missing.sum() == 0:
            st.success("✓ Nenhum valor faltante detectado")
        else:
            st.dataframe(missing[missing > 0])

# Página: Análise Exploratória
elif page == "📈 Análise Exploratória":
    st.title("Análise Exploratória dos Dados")
    st.markdown("---")
    
    st.subheader("Tabela de Frequência - Idade")
    idade_freq = pd.cut(df['Idade'], bins=10).value_counts().sort_index()
    st.bar_chart(idade_freq)
    
    st.subheader("Distribuição de Notas")
    col1, col2 = st.columns(2)
    
    with col1:
        fig, ax = plt.subplots(figsize=(10, 6))
        notas_cols = ['Nota CN', 'Nota CH', 'Nota LC', 'Nota MT', 'Nota Redação']
        df[notas_cols].boxplot(ax=ax)
        ax.set_title('Distribuição das Notas por Disciplina', fontsize=14, fontweight='bold')
        ax.set_ylabel('Nota')
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(df['Nota Média'], bins=50, color='steelblue', edgecolor='black', alpha=0.7)
        ax.set_title('Distribuição da Nota Média', fontsize=14, fontweight='bold')
        ax.set_xlabel('Nota Média')
        ax.set_ylabel('Frequência')
        plt.tight_layout()
        st.pyplot(fig)

# Página: Variáveis Qualitativas
elif page == "📉 Variáveis Qualitativas":
    st.title("Análise de Variáveis Qualitativas")
    st.markdown("---")
    
    qualitative_cols = ['Sexo', 'Cor/Raça', 'Tipo Escola', 'Localização', 'Região']
    
    for col in qualitative_cols:
        st.subheader(f"Distribuição de {col}")
        
        freq_table = df[col].value_counts()
        freq_pct = (freq_table / len(df) * 100).round(2)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig, ax = plt.subplots(figsize=(10, 6))
            freq_table.plot(kind='bar', ax=ax, color='steelblue', edgecolor='black')
            ax.set_title(f'Frequência de {col}', fontsize=12, fontweight='bold')
            ax.set_ylabel('Frequência')
            ax.set_xlabel(col)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig)
        
        with col2:
            fig, ax = plt.subplots(figsize=(10, 6))
            freq_table.plot(kind='pie', ax=ax, autopct='%1.1f%%', startangle=90)
            ax.set_title(f'Proporção de {col}', fontsize=12, fontweight='bold')
            ax.set_ylabel('')
            plt.tight_layout()
            st.pyplot(fig)
        
        st.write("**Tabela de Frequência:**")
        freq_df = pd.DataFrame({
            'Categoria': freq_table.index,
            'Frequência': freq_table.values,
            'Percentual': freq_pct.values
        })
        st.dataframe(freq_df, use_container_width=True)
        st.markdown("---")

# Página: Variáveis Quantitativas
elif page == "📊 Variáveis Quantitativas":
    st.title("Análise de Variáveis Quantitativas")
    st.markdown("---")
    
    quantitative_cols = ['Idade', 'Nota CN', 'Nota CH', 'Nota LC', 'Nota MT', 'Nota Redação', 'Nota Média']
    
    for col in quantitative_cols:
        st.subheader(f"Análise de {col}")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Média", f"{df[col].mean():.2f}")
        with col2:
            st.metric("Mediana", f"{df[col].median():.2f}")
        with col3:
            st.metric("Desvio Padrão", f"{df[col].std():.2f}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(df[col], bins=50, color='steelblue', edgecolor='black', alpha=0.7)
            ax.axvline(df[col].mean(), color='red', linestyle='--', linewidth=2, label=f'Média: {df[col].mean():.2f}')
            ax.axvline(df[col].median(), color='green', linestyle='--', linewidth=2, label=f'Mediana: {df[col].median():.2f}')
            ax.set_title(f'Histograma de {col}', fontsize=12, fontweight='bold')
            ax.set_xlabel(col)
            ax.set_ylabel('Frequência')
            ax.legend()
            plt.tight_layout()
            st.pyplot(fig)
        
        with col2:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.boxplot(df[col], vert=True)
            ax.set_title(f'Box Plot de {col}', fontsize=12, fontweight='bold')
            ax.set_ylabel(col)
            plt.tight_layout()
            st.pyplot(fig)
        
        st.markdown("---")

# Página: Correlações
elif page == "🔗 Correlações":
    st.title("Análise de Correlações")
    st.markdown("---")
    
    notas_cols = ['Nota CN', 'Nota CH', 'Nota LC', 'Nota MT', 'Nota Redação', 'Nota Média']
    corr_matrix = df[notas_cols].corr()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0, ax=ax, 
                cbar_kws={'label': 'Correlação'}, square=True)
    ax.set_title('Matriz de Correlação - Notas', fontsize=14, fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)
    
    st.write("**Matriz de Correlação:**")
    st.dataframe(corr_matrix.round(3), use_container_width=True)
    
    st.subheader("Interpretação das Correlações")
    st.markdown("""
    - **Correlação próxima a 1**: Forte relação positiva
    - **Correlação próxima a -1**: Forte relação negativa
    - **Correlação próxima a 0**: Fraca ou nenhuma relação
    """)

# Página: Amostragem
elif page == "🎯 Amostragem":
    st.title("Análise de Amostragem")
    st.markdown("---")
    
    # Calcular tamanho da amostra
    N = len(df)
    z = 1.96  # 95% de confiança
    p = 0.5
    e = 0.05  # 5% de erro
    
    n_calc = int((z**2 * p * (1-p)) / (e**2))
    n_20pct = int(N * 0.20)
    
    st.subheader("Cálculo do Tamanho da Amostra")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("População Total (N)", f"{N:,}")
    with col2:
        st.metric("20% da População", f"{n_20pct:,}")
    with col3:
        st.metric("Tamanho Calculado (95% conf.)", f"{n_calc:,}")
    
    # Usar o maior dos dois valores
    sample_size = max(n_20pct, n_calc)
    
    st.markdown("---")
    st.subheader("Tipos de Amostragem")
    
    # 1. Amostra Aleatória Simples
    st.write("**1. Amostra Aleatória Simples**")
    sample_simple = df.sample(n=sample_size, random_state=42)
    st.write(f"Tamanho da amostra: {len(sample_simple):,} ({len(sample_simple)/N*100:.2f}% da população)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("Média de Notas (Amostra):")
        st.dataframe(sample_simple[['Nota CN', 'Nota CH', 'Nota LC', 'Nota MT', 'Nota Redação']].mean().round(2))
    with col2:
        st.write("Média de Notas (População):")
        st.dataframe(df[['Nota CN', 'Nota CH', 'Nota LC', 'Nota MT', 'Nota Redação']].mean().round(2))
    
    st.markdown("---")
    
    # 2. Amostra Sistemática
    st.write("**2. Amostra Sistemática**")
    k = N // sample_size
    start = np.random.randint(0, k)
    sample_systematic = df.iloc[start::k][:sample_size]
    st.write(f"Tamanho da amostra: {len(sample_systematic):,} ({len(sample_systematic)/N*100:.2f}% da população)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("Média de Notas (Amostra):")
        st.dataframe(sample_systematic[['Nota CN', 'Nota CH', 'Nota LC', 'Nota MT', 'Nota Redação']].mean().round(2))
    with col2:
        st.write("Média de Notas (População):")
        st.dataframe(df[['Nota CN', 'Nota CH', 'Nota LC', 'Nota MT', 'Nota Redação']].mean().round(2))
    
    st.markdown("---")
    
    # 3. Amostra Estratificada
    st.write("**3. Amostra Estratificada (por Tipo de Escola)**")
    strata = 'Tipo Escola'
    sample_stratified = df.groupby(strata, group_keys=False).apply(
        lambda x: x.sample(n=max(1, int(len(x) * sample_size / N)), random_state=42)
    )[:sample_size]
    st.write(f"Tamanho da amostra: {len(sample_stratified):,} ({len(sample_stratified)/N*100:.2f}% da população)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("Média de Notas (Amostra):")
        st.dataframe(sample_stratified[['Nota CN', 'Nota CH', 'Nota LC', 'Nota MT', 'Nota Redação']].mean().round(2))
    with col2:
        st.write("Média de Notas (População):")
        st.dataframe(df[['Nota CN', 'Nota CH', 'Nota LC', 'Nota MT', 'Nota Redação']].mean().round(2))

# Página: Comparação Amostra vs População
elif page == "📋 Comparação Amostra vs População":
    st.title("Comparação entre Amostra e População")
    st.markdown("---")
    
    N = len(df)
    n_20pct = int(N * 0.20)
    
    # Gerar amostras
    sample_simple = df.sample(n=n_20pct, random_state=42)
    k = N // n_20pct
    start = np.random.randint(0, k)
    sample_systematic = df.iloc[start::k][:n_20pct]
    sample_stratified = df.groupby('Tipo Escola', group_keys=False).apply(
        lambda x: x.sample(n=max(1, int(len(x) * n_20pct / N)), random_state=42)
    )[:n_20pct]
    
    notas_cols = ['Nota CN', 'Nota CH', 'Nota LC', 'Nota MT', 'Nota Redação']
    
    # Comparar médias
    st.subheader("Comparação de Médias")
    
    comparison_data = []
    for col in notas_cols:
        comparison_data.append({
            'Variável': col,
            'População': df[col].mean(),
            'Amostra Simples': sample_simple[col].mean(),
            'Amostra Sistemática': sample_systematic[col].mean(),
            'Amostra Estratificada': sample_stratified[col].mean(),
        })
    
    comparison_df = pd.DataFrame(comparison_data)
    st.dataframe(comparison_df.round(2), use_container_width=True)
    
    # Visualizar comparação
    st.subheader("Visualização da Comparação")
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    for idx, col in enumerate(notas_cols):
        ax = axes[idx]
        
        data_to_plot = [
            df[col],
            sample_simple[col],
            sample_systematic[col],
            sample_stratified[col]
        ]
        
        bp = ax.boxplot(data_to_plot, labels=['População', 'Simples', 'Sistemática', 'Estratificada'])
        ax.set_title(f'{col}', fontweight='bold')
        ax.set_ylabel('Nota')
        ax.grid(True, alpha=0.3)
    
    # Remover o último subplot vazio
    fig.delaxes(axes[5])
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # Testes estatísticos
    st.subheader("Testes Estatísticos (Teste t de Student)")
    
    test_results = []
    for col in notas_cols:
        # Teste t entre população e amostra simples
        t_stat, p_value = stats.ttest_ind(df[col], sample_simple[col])
        test_results.append({
            'Variável': col,
            'Estatística t': t_stat,
            'p-value': p_value,
            'Significante (α=0.05)': 'Não' if p_value > 0.05 else 'Sim'
        })
    
    test_df = pd.DataFrame(test_results)
    st.dataframe(test_df.round(4), use_container_width=True)

st.markdown("---")
st.markdown("*Análise Exploratória dos Dados do ENEM 2024 | Desenvolvido com Streamlit*")
