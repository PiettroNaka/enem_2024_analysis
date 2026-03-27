# Análise Exploratória dos Dados do ENEM 2024

Aplicação Streamlit para análise interativa dos dados do ENEM 2024 com implementação de três técnicas de amostragem estatística.

## 🎯 Funcionalidades

- **Análise Exploratória Completa**: Estatísticas descritivas, tabelas de frequência e gráficos
- **Variáveis Qualitativas**: Análise de distribuições categóricas
- **Variáveis Quantitativas**: Histogramas, box plots e estatísticas
- **Análise de Correlações**: Matriz de correlação entre disciplinas
- **Três Técnicas de Amostragem**:
  - Amostra Aleatória Simples
  - Amostra Sistemática
  - Amostra Estratificada
- **Comparação Amostra vs População**: Testes estatísticos e visualizações

## 📊 Dados

A aplicação utiliza dados do ENEM 2024 armazenados no Big Data-IESB:
- **ed_enem_2024_participantes**: Informações demográficas e socioeconômicas
- **ed_enem_2024_resultados**: Notas das provas

## 🚀 Como Usar

### Localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

### Na Nuvem (Streamlit Cloud)

1. Acesse https://share.streamlit.io/deploy
2. Conecte sua conta GitHub
3. Selecione o repositório `enem_2024_analysis`
4. Configure:
   - **Repository**: PiettroNaka/enem_2024_analysis
   - **Branch**: main
   - **Main file path**: app.py

## 📈 Resultados Principais

| Métrica | Valor |
|---------|-------|
| Nota Média Geral | 505.99 |
| Disciplina com Maior Média | Ciências Humanas (509.06) |
| Disciplina com Menor Média | Matemática (481.98) |
| Maior Variabilidade | Redação (σ = 150.32) |

## 🔗 Conectar com Dados Reais

Para conectar com dados reais do Big Data-IESB, modifique a função `load_data()` em `app.py`:

```python
import psycopg2

def load_data():
    conn = psycopg2.connect(
        host='bigdata.dataiesb.com',
        database='iesb',
        user='data_iesb',
        password='iesb'
    )
    
    query = """
    SELECT 
        nota_cn_ciencias_da_natureza,
        nota_ch_ciencias_humanas,
        nota_lc_linguagens_e_codigos,
        nota_mt_matematica,
        nota_redacao,
        nota_media_5_notas,
        tp_sexo,
        idade_calculada,
        tp_cor_raca,
        tp_dependencia_adm_esc,
        tp_localizacao_esc,
        regiao_nome_prova
    FROM ed_enem_2024_participantes
    WHERE nota_media_5_notas IS NOT NULL
    LIMIT 50000
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
```

## 📚 Arquivos

- `app.py` - Aplicação Streamlit principal
- `amostragem_enem.py` - Classe de amostragem estatística
- `requirements.txt` - Dependências Python
- `README.md` - Este arquivo

## 📖 Documentação

Consulte o relatório técnico completo em `RELATORIO_ENEM_2024.pdf` para:
- Metodologia detalhada
- Análise completa dos resultados
- Interpretação das correlações
- Recomendações e conclusões

## 👨‍💻 Desenvolvido por

Piettro Nakashoji

## 📝 Licença

MIT License

---

**Última atualização**: 27 de Março de 2026
