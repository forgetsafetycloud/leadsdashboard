# Leads Dashboard by Forget Safety™️
Dashboard Python (StreamLit) com integração com IA para acompanhar métricas de desempenho de Leads a partir de um CSV preenchido através do Google Sheets ou similar pelo Gestor de Leads.  
Usando a tabela com a estrutura indicada abaixo, pode-se exportar um CSV, colocar na pasta do projeto, converter dados sensíveis em dados anônimos e acompanhar métricas importantes de avaliação e tomadas de decisão para o melhor aproveitamento de Leads.  
  
Veja em Produção: https://leadsdashboard.streamlit.app/
----------------------------  
# Atualizações V1.1.1:
------------------------------  
Integração ClaudIA by Forget Safety©  
Resumo de IA por agente especialista em análise de dados. Crie um resumo de todos os dados analisados com uma opnião crítica.  

# Como conectar a sua IA
----------------------------  
1. Configure no Streamlit as variáveis com as chaves e url. 👇🏼  
```toml
API_URL = "https://agentedeia/webhook/"
API_KEY = "sk_streamlit_APIKEY"
API_SECRET = "SECRETKEY"
```
2. Para testes locais, crie .streamlit/secrets.toml e coloque as suas chaves e url.
3. Protocolos de segurança para uma conexão segura com a IA foram estabelecidos na linha 596. 👇🏼
```py
signature = hmac.new(
    secret.encode(),
    body.encode(),
    hashlib.sha256
).hexdigest()
```
4. Espera-se um retorno em JSON com a saída "text": "analise"
5. Se não tiver acesso ao nosso agente, pode facilmente configurar a URL e Chaves da sua API de referência, se deseja acessar o nosso agente, contacte-nos via info@forgetsafety.cloud

# Importação do DataFrame
----------------------------  
Carregue o seu CSV na parta raiz do App, lembre-se de alterar o Nome do Arquivo e/ou Path para corresponder com o seu CSV e altere a linha 134. 👇🏼  
```py
df = pd.read_csv("Leads_3M_anon_vals.csv")
```  

# Estrutura do Google Sheets:
------------------------------  
Colunas:  
From | Status | Data / Hora | Campanha | Nome Completo | Contato | Melhor Horário | Email | D/H - 1ª Ligação | D/H - 2ª Ligação | D/H - 3ª Ligação | Anotações | Conversão

# Como Preencher (Exemplos)
----------------------------  
🛜 From  -> Facebook / Insta (String)  
⚡️ Status -> Marcada (String)  
📆 Data / Hora -> 01/01/2026 00:32:06 / (Timestamp) 'dd/MM/yyyy HH:mm:ss'  
📝 Campanha -> Geral (String)  
🙋🏻‍♂️ Nome Completo -> Jane Doe (String)  
📞 Contato -> 351999111222 (String) 'DDI + Número'  
⏰ Melhor Horário -> 9 às 13h (String) 'Opções de Intervalo do Dia, sempre XX às XX'  
✉️ Email -> janedoe@gmail.com (String)  
📞 D/H - 1ª Ligação -> 01/01/2026 00:32:06 / (Timestamp) 'dd/MM/yyyy HH:mm:ss'  
📞 D/H - 2ª Ligação -> 01/01/2026 00:32:06 / (Timestamp) 'dd/MM/yyyy HH:mm:ss'  
📞 D/H - 3ª Ligação -> 01/01/2026 00:32:06 / (Timestamp) 'dd/MM/yyyy HH:mm:ss'  
🗒️ Anotações -> Mora longe, não quer se deslocar. (String)  
💰 Conversão -> 1000 (String) / 'Sem casas decimais, pontos e vírgulas. O Código formata.'  
Se precisar de preencher casas decimais, retire a formatação no código. 👇🏼  
```py
valor_formatado = f"{soma_conversao:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
```

# Métricas disponíveis para análise (16)
--------------  
-> Total de Leads  
-> Status Mais Frequente  
-> Origem Mais Comum  
-> Campanha Mais Relevante  
-> Leads 'Pendente' (Desperdício)  
-> Contactos realizados no Horário Preferencial (Do cliente) nas primeiras 24h  
-> Horário Preferencial + Frequente (Cliente)  
-> Horário Preferencial + Utilizado (Gestor)  
-> Distribuição dos Status dos Leads (Gráfico)  
-> Distribuição de Leads Contactados por Tempo de Resposta (Gráfico)  
-> Funil de Leads 'Não Atendeu' por Tentativa de Ligação (Gráfico)  
-> Contagem de Dias Úteis (Entre 1ª e última Lead) Vs. Dias não Trabalhados (Neste Range)  
-> Total de Conversão (Formatado com . nos milheiros e , nos decimais, em Euros)  
-> LT3 - Nº de dias que tiveram Leads / Nº de dias Trabalhados / Nº de dias Trabalhados nos 3 Períodos (08h às 12h - 12h às 16h - 16h às 21h)  
-> Análise de IA - Agente especialista em análise de dados. Powered by: FS ClaudIA©  
-> Tabela de Dados Detalhados  

Se quiser alterar para a sua moeda local como R$ ou $ edite a linha 481. 👇🏼  
```py
col10.metric("Total de Conversão", f"{valor_formatado}€")
```

# Privacidade - Dados Anônimos
--------------  
Caso esteja usando o Streamlit Cloud no plano gratuito, é necessário um projeto público no GitHub, como este. Portanto, pode usar o código abaixo, ajustando para as necessidades da sua tabela, e transformar os dados sensíveis em dados anônimos em ambiente local, antes de subir para o GitHub. No exemplo abaixo anonimizámos as colunas 'Nome', 'Contato' e 'Email', garantindo a privacidade dos clientes. 👇🏼  
Tabela real de Leads recebidas em uma Clínica Dentária situada em Lisboa / Portugal entre a última semana de Novembro 25 e o último dia de Janeiro 26.  
Por motivos de privacidade, todos os Nomes, Contatos e Emails foram substituídos por 'Jane Doe'.  
Se quiser compartilhar um projeto real, garantindo a privacidade, pode converter o seu CSV e gerar um arquivo com anonimato usando o código abaixo. 👇🏼  
```py
# Certifique-se que a variável 'df' tem o seu DataFrame original carregado.
df_anon = df.copy()
df_anon['Nome'] = 'Jane Doe'
df_anon['Contato'] = '351999111222'
df_anon['Email'] = 'janedoe@gmail.com'
df_anon.to_csv('DataFrame_Anon.csv', index=False)
# Agora é só alterar o DataFrame na linha 134, apagar o antigo, e está pronto para compartilhar usando o Streamlit Community Cloud
```

# Personalização
--------------  
-> Logos / Pode alterar as logos do Sidebar nas linhas 24 e 30 do app.py / Certifique-se de colocar o caminho correto. 👇🏼  
```py
logo_top_base64 = get_base64_image("img/toplogo.png")
logo_bottom_base64 = get_base64_image("img/bottomlogo.png")
```
-> CSS / Da linha 44 a 131, pode estilizar o seu Dashboard usando CSS / Use o Developer Tools do seu navegador para encontrar IDs ou Classes das tags HTML renderizadas.

# Regra rigorosa
----------------  
Se seguir a estrutura recomendada na tabela, não precisa fazer nenhuma alteração no código alem de subir o seu CSV, rodar o StreamLit e ser feliz.
