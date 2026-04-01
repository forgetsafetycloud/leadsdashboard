import streamlit as st
import pandas as pd
import plotly.express as px
import calendar
import base64
import datetime
import requests
import json
import hmac
import hashlib

# Variáveis de SK
url = st.secrets["N8N_URL"]
api_key = st.secrets["API_KEY"]
secret = st.secrets["API_SECRET"]

# Converter imagem para base64
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Certifique-se de que 'toplogo.png' e 'bottomlogo.png' estão pasta img na raiz do projeto
try:
    logo_top_base64 = get_base64_image("img/toplogo.png")
except FileNotFoundError:
    st.error("Erro: 'toplogo.png' não encontrado. Verifique o caminho da imagem.")
    logo_top_base64 = ""

try:
    logo_bottom_base64 = get_base64_image("img/bottomlogo.png")
except FileNotFoundError:
    st.error("Erro: 'bottomlogo.png' não encontrado. Verifique o caminho da imagem.")
    logo_bottom_base64 = ""

# --- Configurações da Página ---
st.set_page_config(
    page_title="Dashboard de Desempenho - Leads",
    page_icon="📲",
    layout="wide",
)

# CSS customizado para estilização
st.markdown(
    """
    <style>
    /* Estilo para o título principal (st.title) */
    h1 {
        font-size: 2.0em !important; /* Ajuste este valor para diminuir/aumentar a fonte */
        color: #202535; /* Cor para o título */
    }

    /* Estilo para o fundo da barra lateral (onde ficam os filtros) */
    [data-testid="stSidebar"] > div:first-child {
        background-color: #202535; /* Cor para o fundo da barra lateral */
        color: white; /* Garante que o texto na sidebar seja legível */
    }

    [data-testid="stWidgetLabel"] > div:first-child {
        color: white; /* Garante que o texto na sidebar seja legível */
    }

    .st-bn {
        background-color: #202535;
    }

    /* Você pode precisar de CSS adicional para customizar widgets específicos dentro da sidebar,
    como o próprio st.multiselect. Por exemplo, para o campo de entrada do multiselect:
    .stMultiSelect > div:first-child > div:first-child {
        background-color: #333333; /* Uma cor um pouco diferente para contraste */
        color: white;
    }
    */

    /* Para o texto geral dentro da sidebar */
    .stSidebar {
        color: white;
    }

    /* Estilo para o logo principal no sidebar */
    #minha-logo-sidebar {
        display: block;
        max-width: 70%; /* Ajuste o tamanho da logo (ex: 70% da largura do sidebar) */
        height: auto;
        margin-left: auto;
        margin-right: auto;
        margin-bottom: 20px; /* Espaço abaixo da logo */
        padding: 10px; /* Padding interno à logo */
        /* background-color: #ffffff; Fundo branco para a logo */
        border-radius: 5px;
    }

    /* Estilo para o logo no final do sidebar */
    #logo-bottom-sidebar {
        display: block;
        max-width: 40%; /* Ajuste o tamanho da logo (ex: 70% da largura do sidebar) */
        height: auto;
        margin-left: auto;
        margin-right: auto;
        margin-top: 25vh;
        padding: 10px; /* Padding interno à logo */
        border-radius: 5px;
    }

    /* Margem da Logo Bottom e Label da IA no Mobile */
    @media only screen and (max-width: 768px) {
        #logo-bottom-sidebar { margin-top: 5vh; }

        [data-testid="stWidgetLabel"] > div:first-child {
            color: white; /* Cor da Label */
        }

    }

    /* Prompt IA */
    [data-testid="stWidgetLabel"] > div:first-child {
        color: #202535; /* Cor da Label */
    }

    [data-testid="stTextAreaRootElement"] > div:first-child {
        background-color: #202535; /* Cor do Fundo na TextArea */
        height: 300px;
    }

    [data-testid="stTextAreaRootElement"] > div:first-child > .st-b6 {
        color: #fff!important; /* Cor do Texto na TextArea */
    }

    </style>
    """,
    unsafe_allow_html=True
)

# --- Carregamento dos dados ---
df = pd.read_csv("Leads_Clidec_Mar26.csv")

# --- Convertendo a coluna chegada em DT ---
df['Chegada'] = pd.to_datetime(df['Chegada'], format='%d/%m/%Y, %H:%M:%S', errors='coerce')

# Adiciona o logo principal no sidebar
if logo_top_base64:
    st.sidebar.markdown(
        f"<img id='minha-logo-sidebar' src='data:image/png;base64,{logo_top_base64}'>",
        unsafe_allow_html=True
    )

# --- Barra Lateral (Filtros) ---
st.sidebar.header("🔍 Filtros")

# Cria um dicionário para mapear os números dos meses em nomes em Português
mes_map = {
    1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',
    7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
}

# Extraia períodos únicos de ano e mês e ordene-os (os objetos de período podem são classificados cronologicamente).
unique_month_years = sorted(df['Chegada'].dt.to_period('M').dropna().unique())

meses_com_ano = []
for period in unique_month_years:
    month_name = mes_map[period.month]
    year_short = str(period.year)[-2:] # Get last two digits of the year
    meses_com_ano.append(f"{month_name} {year_short}")

# Filtro de Mês/Ano
anos_selecionados = st.sidebar.multiselect("Ano", meses_com_ano, default=meses_com_ano)

# Adiciona a segunda logo no final do sidebar
if logo_bottom_base64:
    st.sidebar.markdown(
        f"<img id='logo-bottom-sidebar' src='data:image/png;base64,{logo_bottom_base64}'>",
        unsafe_allow_html=True
    )

# --- Filtragem do DataFrame ---
# Crie a coluna auxiliar 'Chegada_Mes_Ano' novamente, para a filtragem, lidando com NaT
df['Chegada_Mes_Ano'] = df['Chegada'].apply(
    lambda x: f"{mes_map[x.month]} {str(x.year)[-2:]}" if pd.notna(x) else None
)

# Agora, o dataframe principal é filtrado usando a coluna auxiliar 'Chegada_Mes_Ano'
df_filtrado = df[df['Chegada_Mes_Ano'].isin(anos_selecionados)]

# --- Conteúdo Principal ---
st.title("🎲 Dashboard de Desempenho - Leads")
st.markdown("Explore os dados nos últimos meses. Utilize os filtros no menu lateral para refinar sua análise.")

# --- Métricas Principais (KPIs) ---
st.subheader("Métricas gerais")

if not df_filtrado.empty:
    total_registros = df_filtrado.shape[0]
    status_mais_frequente = df_filtrado['Status'].mode()[0] if not df_filtrado['Status'].mode().empty else 'N/A'
    origem_mais_frequente = df_filtrado['Origem'].mode()[0] if not df_filtrado['Origem'].mode().empty else 'N/A'
    campanha_mais_frequente = df_filtrado['Campanha'].mode()[0] if not df_filtrado['Campanha'].mode().empty else 'N/A'
else:
    total_registros = 0
    status_mais_frequente = 'N/A'
    origem_mais_frequente = 'N/A'
    campanha_mais_frequente = 'N/A'

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Leads", f"{total_registros:,}")
col2.metric("Status Mais Frequente", status_mais_frequente)
col3.metric("Origem Mais Comum", origem_mais_frequente)
col4.metric("Campanha Mais Relevante", campanha_mais_frequente)

st.markdown("---")

# Defina a função de análise sintática externamente para que seja acessível.
def parse_preferred_time(time_str):
    if pd.isna(time_str):
        return None, None
    parts = time_str.replace('h', '').replace(' ', '').split('às')
    if len(parts) == 2:
        try:
            start_hour = int(parts[0])
            end_hour = int(parts[1])
            return pd.to_datetime(f'{start_hour:02d}:00:00').time(), pd.to_datetime(f'{end_hour:02d}:00:00').time()
        except ValueError:
            return None, None
    return None, None

# Defina a função de verificação externamente para que seja acessível.
def check_preferred_time_contact(row):
    if pd.isna(row['Preferred_Start_Time']) or pd.isna(row['Preferred_End_Time']):
        return False
    call_time = row['1ª Ligação'].time()
    return row['Preferred_Start_Time'] <= call_time <= row['Preferred_End_Time']

# --- Inicialização das Métricas Adicionais ---
pendente_leads_filtrado = 0
count_na_hora_certa_filtrado = 0
horario_preferencial_mais_frequente = 'N/A'
soma_conversao_filtrado = 0

# --- Cálculo das Métricas Adicionais ---
# Somente procede se o df_filtrado não estiver vazio
if not df_filtrado.empty:
    pendente_leads_filtrado = df_filtrado[df_filtrado['Status'] == 'Pendente'].shape[0]

    # Para evitar SettingWithCopyWarning e garantir que estamos trabalhando com uma cópia
    df_temp = df_filtrado.copy()

    # Aplique a função de análise sintática.
    df_temp[['Preferred_Start_Time', 'Preferred_End_Time']] = df_temp['H.Preferencial'].apply(lambda x: pd.Series(parse_preferred_time(x)))

    # Certificar que as colunas de ligação são datetime
    df_temp['1ª Ligação'] = pd.to_datetime(df_temp['1ª Ligação'], errors='coerce')

    # Filtrar leads com 1ª Chamada e contacto no próprio dia
    leads_com_primeira_ligacao_filtrado = df_temp[df_temp['1ª Ligação'].notna()].copy()
    leads_mesmo_dia_filtrado = leads_com_primeira_ligacao_filtrado[
        leads_com_primeira_ligacao_filtrado['Chegada'].dt.date == leads_com_primeira_ligacao_filtrado['1ª Ligação'].dt.date
    ].copy()

    leads_contatados_na_hora_certa_filtrado = leads_mesmo_dia_filtrado[leads_mesmo_dia_filtrado.apply(check_preferred_time_contact, axis=1)]
    count_na_hora_certa_filtrado = leads_contatados_na_hora_certa_filtrado.shape[0]

    # Horário Preferencial mais frequente
    if not df_temp['H.Preferencial'].mode().empty:
        horario_preferencial_mais_frequente = df_temp['H.Preferencial'].mode()[0]

    # Soma total da coluna 'Conversão'
    if not df_temp['Conversão'].isnull().all():
        soma_conversao_filtrado = df_temp['Conversão'].sum()

# --- Cálculo da Métrica: Horário Preferencial Mais Utilizado (com base nas ligações) ---

horario_preferencial_mais_utilizado_em_ligacao = 'N/A'

# Verifica se df_filtrado não está vazio antes de prosseguir
if not df_filtrado.empty:
    # Identificar leads que tiveram pelo menos uma ligação
    leads_com_ligacao = df_filtrado[
        df_filtrado['1ª Ligação'].notna() |
        df_filtrado['2ª Ligação'].notna() |
        df_filtrado['3ª Ligação'].notna()
    ]

    # Encontrar o Horário Preferencial mais frequente entre esses leads
    if not leads_com_ligacao.empty and not leads_com_ligacao['H.Preferencial'].mode().empty:
        horario_preferencial_mais_utilizado_em_ligacao = leads_com_ligacao['H.Preferencial'].mode()[0]

# --- Exibição de Métricas em 4 Colunas ---
st.subheader("Desempenho")

col5, col6, col7, col8 = st.columns(4)
col5.metric("Leads 'Pendente' (Desperdício)", pendente_leads_filtrado)
col6.metric("Contactos no H. Pref. em 24h", count_na_hora_certa_filtrado)
col7.metric("Horário Preferencial + Freq. (Cliente)", horario_preferencial_mais_frequente)
col8.metric("Horário Preferencial + Utilizado (Gestor)", horario_preferencial_mais_utilizado_em_ligacao)

st.markdown("---")

# --- Análises Visuais com Plotly ---
st.subheader("Análise Gráfica")

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    if not df_filtrado.empty:
        # Gráfico de Distribuição dos Status dos Leads
        status_counts = df_filtrado['Status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']

        fig_status = px.pie(status_counts, values='Count', names='Status', title='Distribuição dos Status dos Leads')
        fig_status.update_layout(title_x=0.1) # Centraliza o título
        st.plotly_chart(fig_status, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de Status dos Leads.")

with col_graf2:
    if not df_filtrado.empty:
        # Lógica para o Gráfico de Distribuição de Leads Contactados por Tempo de Resposta
        # Certifique-se que as colunas 'Chegada' e '1ª Ligação' estão em formato datetime no df_filtrado
        # Criar uma cópia para não alterar o df_filtrado diretamente ao adicionar 'Tempo_Resposta'
        df_temp_chart = df_filtrado.copy()
        df_temp_chart['Chegada'] = pd.to_datetime(df_temp_chart['Chegada'], format='%d/%m/%Y, %H:%M:%S', errors='coerce')
        df_temp_chart['1ª Ligação'] = pd.to_datetime(df_temp_chart['1ª Ligação'], errors='coerce')

        df_temp_chart['Tempo_Resposta'] = (df_temp_chart['1ª Ligação'] - df_temp_chart['Chegada']).dt.total_seconds()

        # Filtrar apenas os leads que tiveram a 1ª Ligação (Tempo_Resposta não nulo e positivo)
        leads_contactados_chart = df_temp_chart[df_temp_chart['Tempo_Resposta'].notnull() & (df_temp_chart['Tempo_Resposta'] >= 0)]

        # Definir os limites de tempo em segundos
        cinco_minutos = 5 * 60
        uma_hora = 60 * 60
        vinte_e_quatro_horas = 24 * 60 * 60

        # Contar leads em cada categoria
        contactados_5min_filtrado = leads_contactados_chart[leads_contactados_chart['Tempo_Resposta'] <= cinco_minutos].shape[0]
        contactados_1h_filtrado = leads_contactados_chart[(leads_contactados_chart['Tempo_Resposta'] > cinco_minutos) & (leads_contactados_chart['Tempo_Resposta'] <= uma_hora)].shape[0]
        contactados_24h_filtrado = leads_contactados_chart[(leads_contactados_chart['Tempo_Resposta'] > uma_hora) & (leads_contactados_chart['Tempo_Resposta'] <= vinte_e_quatro_horas)].shape[0]
        contactados_depois_24h_filtrado = leads_contactados_chart[leads_contactados_chart['Tempo_Resposta'] > vinte_e_quatro_horas].shape[0]

        data_tempos_resposta = {
            'Intervalo de Tempo': [
                'Primeiros 5 minutos',
                'Primeira hora (depois de 5 minutos)',
                'Em 24h (depois de 1 hora)',
                'Depois de 24h'
            ],
            'Quantidade de Leads': [
                contactados_5min_filtrado,
                contactados_1h_filtrado,
                contactados_24h_filtrado,
                contactados_depois_24h_filtrado
            ]
        }
        df_tempos_resposta_filtrado = pd.DataFrame(data_tempos_resposta)

        color_map = {
            'Primeiros 5 minutos': 'green',
            'Primeira hora (depois de 5 minutos)': 'gold',
            'Em 24h (depois de 1 hora)': 'purple',
            'Depois de 24h': 'red'
        }

        fig_tempos = px.bar(df_tempos_resposta_filtrado, x='Intervalo de Tempo', y='Quantidade de Leads',
                             title='Distribuição de Leads Contactados por Tempo de Resposta',
                             labels={'Intervalo de Tempo': 'Intervalo de Tempo', 'Quantidade de Leads': 'Número de Leads'},
                             color='Intervalo de Tempo',
                             color_discrete_map=color_map
                            )
        fig_tempos.update_layout(xaxis_title='Intervalo de Tempo', yaxis_title='Número de Leads', title_x=0.1) # Centraliza o título
        st.plotly_chart(fig_tempos, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de Tempo de Resposta.")

st.markdown("---")

# 1. Inicializar variáveis
date_range_filtered = 0
count_weekdays_not_worked_filtered = 0

# 2. Verifique se o df_filtrado está vazio
if not df_filtrado.empty:
    # Crie uma cópia para evitar o aviso SettingWithCopyWarning.
    df_temp_filtered = df_filtrado.copy()

    # 3a. Converter colunas de data para datetime
    df_temp_filtered['Chegada'] = pd.to_datetime(df_temp_filtered['Chegada'], errors='coerce')
    df_temp_filtered['1ª Ligação'] = pd.to_datetime(df_temp_filtered['1ª Ligação'], errors='coerce')
    df_temp_filtered['2ª Ligação'] = pd.to_datetime(df_temp_filtered['2ª Ligação'], errors='coerce')
    df_temp_filtered['3ª Ligação'] = pd.to_datetime(df_temp_filtered['3ª Ligação'], errors='coerce')

    # Filtre as linhas em que 'Chegada' é NaT após a conversão, uma vez que não podem ser utilizadas para o cálculo do intervalo de datas.
    df_temp_filtered = df_temp_filtered.dropna(subset=['Chegada'])

    if not df_temp_filtered.empty:
        # 3b. Encontre as datas mínimas e máximas de 'Chegada'.
        min_chegada_date_filtered = df_temp_filtered['Chegada'].min()
        max_chegada_date_filtered = df_temp_filtered['Chegada'].max()

        # 3c. Calcule o número total de dias.
        date_range_filtered = (max_chegada_date_filtered - min_chegada_date_filtered).days

        # 3d. Gere todas as datas dentro do intervalo (normalizadas para a meia-noite)
        all_dates_in_filtered_range = pd.date_range(
            start=min_chegada_date_filtered.normalize(), 
            end=max_chegada_date_filtered.normalize()
        )

        # 3e. Filtrar por dias da semana (segunda-feira=0, domingo=6)
        weekdays_in_range_filtered = all_dates_in_filtered_range[all_dates_in_filtered_range.dayofweek < 5]

        # 3f. Consolidar datas exclusivas das colunas de tentativas de chamada
        # Garantir que concatenemos apenas séries não nulas
        called_dates_series = pd.concat([ 
            df_temp_filtered['1ª Ligação'].dropna(), 
            df_temp_filtered['2ª Ligação'].dropna(), 
            df_temp_filtered['3ª Ligação'].dropna()
        ])
        
        # Normalize apenas para datas e obtenha valores únicos, depois converta para um conjunto para uma pesquisa eficiente.
        called_dates_set_filtered = set(called_dates_series.dt.normalize().unique())

        # 3g. Determine quais os dias da semana que não foram trabalhados.
        weekdays_not_worked_filtered_list = [
            d for d in weekdays_in_range_filtered if d.normalize() not in called_dates_set_filtered
        ]

        # 3h. Conte esses dias úteis não trabalhados
        count_weekdays_not_worked_filtered = len(weekdays_not_worked_filtered_list)

col_graf3, col9, col10 = st.columns([0.6, 0.2, 0.4])

col9.metric("Dias Úteis / Ñ Trabalhados", f"{len(weekdays_in_range_filtered)} / {count_weekdays_not_worked_filtered}")

# 1. Inicializar variáveis
total_nao_atendeu_filtered = 0
tiveram_2a_ligacao_filtered = 0
tiveram_3a_ligacao_filtered = 0

# 2. Verifique se o df_filtrado não está vazio.
if not df_filtrado.empty:
    # 3a. Calcular total_nao_atendeu_filtered
    nao_atendeu_df_filtered = df_filtrado[df_filtrado['Status'] == 'Não Atendeu'].copy()
    total_nao_atendeu_filtered = nao_atendeu_df_filtered.shape[0]

    # 3b-c. Calcular tiveram_2a_ligacao_filtered
    tiveram_2a_ligacao_filtered = nao_atendeu_df_filtered['2ª Ligação'].notnull().sum()

    # 3d-e. Calcular tiveram_3a_ligacao_filtered
    quem_teve_2a_ligacao_filtered = nao_atendeu_df_filtered[nao_atendeu_df_filtered['2ª Ligação'].notnull()].copy()
    tiveram_3a_ligacao_filtered = quem_teve_2a_ligacao_filtered['3ª Ligação'].notnull().sum()

# 4. Criar df_funil_filtered
funnel_data_filtered = {
    'Etapa': [
        'Não Atendeu (Total)',
        'Tiveram 2ª Ligação',
        'Tiveram 3ª Ligação'
    ],
    'Contagem': [
        total_nao_atendeu_filtered,
        tiveram_2a_ligacao_filtered,
        tiveram_3a_ligacao_filtered
    ]
}

df_funil_filtered = pd.DataFrame(funnel_data_filtered)

with col_graf3:
    # st.subheader("Funil de Leads 'Não Atendeu'")
    # Verifique se df_filtrado está vazio ou se todas as contagens em df_funil_filtered são zero.
    if df_filtrado.empty or df_funil_filtered['Contagem'].sum() == 0:
        st.warning("Nenhum dado disponível para o funil de leads com os filtros selecionados.")
    else:
        # Crie o gráfico de funil
        fig_funnel_filtered = px.funnel(df_funil_filtered, x='Contagem', y='Etapa',
                                        title="Funil de Leads 'Não Atendeu' por Tentativa de Ligação",
                                        labels={'Contagem': 'Número de Leads', 'Etapa': 'Etapa da Ligação'})

        fig_funnel_filtered.update_layout(xaxis_title='Número de Leads', yaxis_title='Etapa da Ligação')
        st.plotly_chart(fig_funnel_filtered, use_container_width=True)

# --- Coluna Conversão, DESABILITADA ---
#valor_formatado = f"{soma_conversao_filtrado:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
#col10.metric("Total de Conversão", f"{valor_formatado}€")

# --- Coluna LT3 ---
# 1. Iniciando variáveiis
total_worked_days = 0
days_with_calls_all_periods = 0

# 2. Verifique se o df_filtrado não está vazio.
if not df_filtrado.empty:
    # Crie uma cópia para evitar o aviso SettingWithCopyWarning.
    df_temp_filtered_calls = df_filtrado.copy()

    # 3. Converter colunas de tentativas de chamada para o formato datetime.
    df_temp_filtered_calls['1ª Ligação'] = pd.to_datetime(df_temp_filtered_calls['1ª Ligação'], errors='coerce')
    df_temp_filtered_calls['2ª Ligação'] = pd.to_datetime(df_temp_filtered_calls['2ª Ligação'], errors='coerce') # Corrected typo
    df_temp_filtered_calls['3ª Ligação'] = pd.to_datetime(df_temp_filtered_calls['3ª Ligação'], errors='coerce')

    # 4. Concatenar e extrair datas únicas.
    all_call_dates = pd.concat([
        df_temp_filtered_calls['1ª Ligação'].dropna(),
        df_temp_filtered_calls['2ª Ligação'].dropna(),
        df_temp_filtered_calls['3ª Ligação'].dropna()
    ]).dt.normalize().unique()

    # 5. Conte o número de datas únicas.
    total_worked_days = len(all_call_dates)

    # Crie um DataFrame temporário para análise de chamadas.
    df_calls = df_filtrado.copy()

    # Converter colunas de tentativas de chamada para datetime.
    df_calls['1ª Ligação'] = pd.to_datetime(df_calls['1ª Ligação'], errors='coerce')
    df_calls['2ª Ligação'] = pd.to_datetime(df_calls['2ª Ligação'], errors='coerce')
    df_calls['3ª Ligação'] = pd.to_datetime(df_calls['3ª Ligação'], errors='coerce')

    # Definir intervalos de tempo.
    morning_start = datetime.time(8, 0, 0)
    morning_end = datetime.time(12, 0, 0)
    afternoon_start = datetime.time(12, 0, 1)
    afternoon_end = datetime.time(16, 0, 0)
    evening_start = datetime.time(16, 0, 1)
    evening_end = datetime.time(21, 0, 0)

    # Recolha datas exclusivas para cada período.
    unique_morning_dates = set()
    unique_afternoon_dates = set()
    unique_evening_dates = set()

    call_columns = ['1ª Ligação', '2ª Ligação', '3ª Ligação']

    for col in call_columns:
        valid_calls = df_calls[col].dropna()
        for call_timestamp in valid_calls:
            call_time = call_timestamp.time()
            call_date = call_timestamp.date()

            if morning_start <= call_time <= morning_end:
                unique_morning_dates.add(call_date)
            if afternoon_start <= call_time <= afternoon_end:
                unique_afternoon_dates.add(call_date)
            if evening_start <= call_time <= evening_end:
                unique_evening_dates.add(call_date)

    # Encontre as datas que existem nos três conjuntos.
    days_with_calls_all_periods = len(unique_morning_dates.intersection(unique_afternoon_dates, unique_evening_dates))

    # 6. Exibir coluna LT3
    col10.metric("LT3 - D. Leads / D. Trabalhados / 3 Períodos", f"{date_range_filtered} / {total_worked_days} / {days_with_calls_all_periods}")

# --- Prompt para análise de IA ---
resumo_status = []

for _, row in status_counts.iterrows():
    resumo_status.append(f"{row[0]}: {row[1]}")

resumo_status_final = ", ".join(resumo_status)

prompt = f'''
Tivemos um total de {total_registros} leads entre {min_chegada_date_filtered} e {max_chegada_date_filtered}.
O Status mais frequente é {status_mais_frequente}.
A origem mais comum é {origem_mais_frequente}.
A campanha mais relevante é {campanha_mais_frequente}.
{pendente_leads_filtrado} leads não foram contactadas.
{count_na_hora_certa_filtrado} leads foram contactadas no horário pretendido nas primeiras 24h.
O horário preferencial mais frequente é {horario_preferencial_mais_frequente}.
O horário com mais frequência de ligações pelo Gestor de clientes é {horario_preferencial_mais_utilizado_em_ligacao}.
A distribuição por Status é: {resumo_status_final}.
{contactados_5min_filtrado} leads foram contactadas nos primeiros 5 minutos.
{contactados_1h_filtrado} leads foram contactadas na primeira hora e depois de 5 minutos.
{contactados_24h_filtrado} leads foram contactadas nas primeiras 24h e depois de 1 hora.
{contactados_depois_24h_filtrado} leads foram contactadas depois de 24h.
{total_nao_atendeu_filtered} leads não atenderam a ligação na primeira tentativa.
De {total_nao_atendeu_filtered} leads que não atenderam, foi feito a segunda tentativa em {tiveram_2a_ligacao_filtered} leads.
De {tiveram_2a_ligacao_filtered} que continuaram sem atender, foi feito a terceira tentativa em {tiveram_3a_ligacao_filtered} leads.
Entre a primeira e última data que chegaram Leads, temos {len(weekdays_in_range_filtered)} dias úteis (Seg. a Sex.), e destes, {count_weekdays_not_worked_filtered} dias não tem ligações feitas pelo Gestor.
De {date_range_filtered} dias com novas Leads, o Gestor trabalhou {total_worked_days} dias.
Dos {total_worked_days} dias trabalhados, {days_with_calls_all_periods} dias foram feitas ligações nos 3 períodos do dia, (08h às 12h, 12h às 16h e 16h às 20h).
'''

claudIA = "Clique no botão acima para gerar a análise. 😉"

st.markdown("---")
st.subheader("Análise de IA")
st.markdown("Agente especialista em análise de dados.")

#st.button("Gerar análise")

if st.button("Gerar análise"):

    payload = {
        "prompt": prompt
    }

    body = json.dumps(payload, separators=(',', ':'))

    signature = hmac.new(
        secret.encode(),
        body.encode(),
        hashlib.sha256
    ).hexdigest()

    headers = {
        "X-API-KEY": api_key,
        "X-SIGNATURE": signature,
        "X-API-SECRET": secret,
        "Content-Type": "application/json"
    }

    try:
        with st.spinner("A ClaudIA está pensando..."):
            response = requests.post(url, data=body, headers=headers, timeout=(60, 300))
            response.raise_for_status()

            claudIA = response.json()

        st.success("Geração de Análise Concluída")
        #st.write(claudIA["text"])
        claudIA = claudIA["text"]

    except Exception as e:
        #st.error(str(e))
        st.error("Não foi possível conectar ao servidor de IA.")
        st.stop()

copy = "Powered by: FS ClaudIA©"

st.text_area(copy, claudIA)

# --- FOLLOW UP [Receção] ---
st.markdown("---")
st.subheader("113 / 0")
st.markdown("De 113 Marcações a Receção fez 0 Follow Ups")

# --- LEADS IA [Ary] ---
st.markdown("---")
st.subheader("25 / 3")
st.markdown("De 25 Conversas iniciadas a IA marcou 3")

# --- Tabela de Dados Detalhados ---
st.markdown("---")
st.subheader("Dados Detalhados")
st.markdown("DataFrame completo")
st.dataframe(df_filtrado)

# Powered by Forget Safety - EU
# Codec by Rodrigo Perazoli
