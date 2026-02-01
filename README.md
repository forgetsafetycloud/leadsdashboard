# leadsdashboard
----------------------------  
Dashboard Python (StreamLit) para acompanhar métricas de desempenho de Leads a partir de um CSV preenchido através do Google Sheets pelo Gestor de Leads.
Usando o Google Sheets com a estrutura indicada abaixo, pode-se exportar um CSV, colocar na pasta do projeto e acompanhar métricas importantes de avaliação e tomadas de decição para o melhor aproveitamento de Leads.

# Estrutura do Google Sheets:
------------------------------  
Colunas -> 🛜 From | ⚡️ Status | 📆 Data / Hora | 📝 Campanha | 🙋🏻‍♂️ Nome Completo | 📞 Contato | ⏰ Melhor Horário | ✉️ Email | D/H - 1ª Ligação | D/H - 2ª Ligação | D/H - 3ª Ligação | 🗒️ Anotações | 💰 Conversão

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
D/H - 1ª Ligação -> 01/01/2026 00:32:06 / (Timestamp) 'dd/MM/yyyy HH:mm:ss'  
D/H - 2ª Ligação -> 01/01/2026 00:32:06 / (Timestamp) 'dd/MM/yyyy HH:mm:ss'  
D/H - 3ª Ligação -> 01/01/2026 00:32:06 / (Timestamp) 'dd/MM/yyyy HH:mm:ss'  
🗒️ Anotações -> Mora longe, não quer se deslocar. (String)  
💰 Conversão -> 1.000,00€ (String) / 'Formato moeda local.'  
