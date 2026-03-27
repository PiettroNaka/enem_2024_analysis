"""
Script de Amostragem Estatística para Dados do ENEM 2024
Implementa três técnicas de amostragem e compara com população
"""

import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class AmostragemENEM:
    """Classe para realizar amostragem estatística dos dados do ENEM"""
    
    def __init__(self, df, nivel_confianca=0.95, margem_erro=0.05):
        """
        Inicializa a classe de amostragem
        
        Parameters:
        -----------
        df : DataFrame
            Dados da população
        nivel_confianca : float
            Nível de confiança (padrão: 0.95 = 95%)
        margem_erro : float
            Margem de erro (padrão: 0.05 = 5%)
        """
        self.df = df
        self.N = len(df)
        self.nivel_confianca = nivel_confianca
        self.margem_erro = margem_erro
        
        # Calcular tamanho da amostra
        self.z = stats.norm.ppf((1 + nivel_confianca) / 2)
        self.p = 0.5
        self.n_calculado = int((self.z**2 * self.p * (1-self.p)) / (margem_erro**2))
        self.n_20pct = int(self.N * 0.20)
        self.n = max(self.n_calculado, self.n_20pct)
    
    def amostra_aleatoria_simples(self, random_state=42):
        """
        Gera amostra aleatória simples
        
        Returns:
        --------
        DataFrame
            Amostra aleatória simples
        """
        return self.df.sample(n=self.n, random_state=random_state)
    
    def amostra_sistematica(self, random_state=42):
        """
        Gera amostra sistemática
        
        Returns:
        --------
        DataFrame
            Amostra sistemática
        """
        np.random.seed(random_state)
        k = self.N // self.n
        start = np.random.randint(0, k)
        return self.df.iloc[start::k][:self.n]
    
    def amostra_estratificada(self, estrato, random_state=42):
        """
        Gera amostra estratificada
        
        Parameters:
        -----------
        estrato : str
            Nome da coluna para estratificação
            
        Returns:
        --------
        DataFrame
            Amostra estratificada
        """
        return self.df.groupby(estrato, group_keys=False).apply(
            lambda x: x.sample(n=max(1, int(len(x) * self.n / self.N)), random_state=random_state)
        )[:self.n]
    
    def comparar_amostras(self, variaveis_numericas):
        """
        Compara estatísticas entre população e amostras
        
        Parameters:
        -----------
        variaveis_numericas : list
            Lista de variáveis numéricas para comparação
            
        Returns:
        --------
        DataFrame
            Comparação de médias
        """
        amostra_simples = self.amostra_aleatoria_simples()
        amostra_sistematica = self.amostra_sistematica()
        amostra_estratificada = self.amostra_estratificada('Tipo Escola')
        
        resultados = []
        for var in variaveis_numericas:
            resultados.append({
                'Variável': var,
                'População': self.df[var].mean(),
                'Amostra Simples': amostra_simples[var].mean(),
                'Amostra Sistemática': amostra_sistematica[var].mean(),
                'Amostra Estratificada': amostra_estratificada[var].mean(),
            })
        
        return pd.DataFrame(resultados)
    
    def testes_estatisticos(self, variaveis_numericas):
        """
        Realiza testes t de Student
        
        Parameters:
        -----------
        variaveis_numericas : list
            Lista de variáveis numéricas para teste
            
        Returns:
        --------
        DataFrame
            Resultados dos testes
        """
        amostra_simples = self.amostra_aleatoria_simples()
        
        resultados = []
        for var in variaveis_numericas:
            t_stat, p_value = stats.ttest_ind(self.df[var], amostra_simples[var])
            resultados.append({
                'Variável': var,
                'Estatística t': t_stat,
                'p-value': p_value,
                'Significante (α=0.05)': 'Sim' if p_value < 0.05 else 'Não'
            })
        
        return pd.DataFrame(resultados)
    
    def gerar_relatorio(self, variaveis_numericas):
        """
        Gera relatório completo de amostragem
        
        Parameters:
        -----------
        variaveis_numericas : list
            Lista de variáveis numéricas para análise
        """
        print("=" * 80)
        print("RELATÓRIO DE AMOSTRAGEM ESTATÍSTICA - ENEM 2024")
        print("=" * 80)
        
        print(f"\nTamanho da População: {self.N:,}")
        print(f"Nível de Confiança: {self.nivel_confianca*100:.0f}%")
        print(f"Margem de Erro: {self.margem_erro*100:.0f}%")
        print(f"\nTamanho da Amostra Calculado: {self.n_calculado:,}")
        print(f"20% da População: {self.n_20pct:,}")
        print(f"Tamanho da Amostra Utilizado: {self.n:,}")
        
        print("\n" + "-" * 80)
        print("COMPARAÇÃO DE MÉDIAS - AMOSTRA VS POPULAÇÃO")
        print("-" * 80)
        
        comparacao = self.comparar_amostras(variaveis_numericas)
        print(comparacao.to_string(index=False))
        
        print("\n" + "-" * 80)
        print("TESTES ESTATÍSTICOS (Teste t de Student)")
        print("-" * 80)
        
        testes = self.testes_estatisticos(variaveis_numericas)
        print(testes.to_string(index=False))
        
        print("\n" + "=" * 80)
        print("FIM DO RELATÓRIO")
        print("=" * 80)


if __name__ == "__main__":
    # Gerar dados de exemplo
    np.random.seed(42)
    n_samples = 5000
    
    data = {
        'Nota CN': np.random.normal(500, 100, n_samples),
        'Nota CH': np.random.normal(510, 95, n_samples),
        'Nota LC': np.random.normal(490, 105, n_samples),
        'Nota MT': np.random.normal(480, 120, n_samples),
        'Nota Redação': np.random.normal(550, 150, n_samples),
        'Tipo Escola': np.random.choice(['Pública', 'Privada'], n_samples),
    }
    
    df = pd.DataFrame(data)
    df['Nota Média'] = (df['Nota CN'] + df['Nota CH'] + 
                        df['Nota LC'] + df['Nota MT'] + 
                        df['Nota Redação']) / 5
    
    # Garantir valores válidos
    for col in ['Nota CN', 'Nota CH', 'Nota LC', 'Nota MT', 'Nota Redação']:
        df[col] = df[col].clip(0, 1000)
    
    # Realizar amostragem
    amostragem = AmostragemENEM(df, nivel_confianca=0.95, margem_erro=0.05)
    
    variaveis = ['Nota CN', 'Nota CH', 'Nota LC', 'Nota MT', 'Nota Redação', 'Nota Média']
    amostragem.gerar_relatorio(variaveis)
