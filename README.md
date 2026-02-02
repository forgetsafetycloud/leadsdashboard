# Leads Dashboard by Forget Safety
Dashboard Python (StreamLit) para acompanhar métricas de desempenho de Leads a partir de um CSV preenchido através do Google Sheets pelo Gestor de Leads.  
Usando o Google Sheets com a estrutura indicada abaixo, pode-se exportar um CSV, colocar na pasta do projeto e acompanhar métricas importantes de avaliação e tomadas de decição para o melhor aproveitamento de Leads.  
----------------------------  
# Importação do DataFrame
----------------------------  
Carregue o seu CSV na parta raiz do App, lembre-se de alterar o Nome do Arquivo e/ou Path para corresponder com o seu CSV e altere a linha 100. 👇🏼  
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
💰 Conversão -> 1000 (String) / 'Sem casas decimais, pontos e vírgulas. O Código formata.' / Se precisar de preencher casas decimais, retire a formatação no código.  

# Métricas disponíveis para análise (13)
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

Se quiser alterar para a sua moeda local como R$ ou $ edite a linha 446. 👇🏼  
```py
col10.metric("Total de Conversão", f"{valor_formatado}€")
```

# Privacidade
--------------  
Tabela real de Leads recebidas em uma Clínica Dentária situada em Lisboa / Portugal entre a última semana de Novembro 25 e o último dia de Janeiro 26.  
Por motivos de privacidade, todos os Nomes, Contatos e Emails foram substituídos por 'Jane Doe'.  

Se quiser compartilhar um projeto real, garantindo a privacidade, pode converter o seu CSV e gerar um arquivo com anonimato usando o código Python. 👇🏼  
```py
# Certifique-se que a variável 'df' tem o seu DataFrame original carregado.
df_anon = df.copy()
df_anon['Nome'] = 'Jane Doe'
df_anon['Contato'] = '351999111222'
df_anon['Email'] = 'janedoe@gmail.com'
df_anon.to_csv('DataFrame_Anon.csv', index=False)
# Agora é só alterar o DataFrame na linha 100, apagar o antigo, e está pronto para compartilhar usando o Streamlit Community Cloud
```

# Personalização
--------------  
-> Logos / Pode alterar as logos do Sidebar nas linhas 14 e 20 do app.py / Certifique-se de colocar o caminho correto. 👇🏼  
```py
logo_top_base64 = get_base64_image("img/toplogo.png")
logo_bottom_base64 = get_base64_image("img/bottomlogo.png")
```
-> CSS / Da linha 32 a 97, pode estilizar o seu Dashboard usando CSS / Use o Developer Tools do seu navegador para encontrar IDs ou Classes das tags HTML renderizadas.

# Regra rigorosa
----------------  
Se seguir a estrutura recomendada na tabela, não precisa fazer nenhuma alteração no código alem de subir o seu CSV, rodar o StreamLit e ser feliz.
