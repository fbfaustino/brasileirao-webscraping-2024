# Web Scraping do Sofascore - Campeonato Brasileiro 2024

Este projeto realiza o scraping de dados estatísticos de partidas do Campeonato Brasileiro 2024 a partir do site Sofascore, utilizando a API pública disponibilizada pela plataforma. O código é implementado em Python, utilizando Selenium para realizar as requisições e manipular o conteúdo da web.

## Funcionalidades

- Coleta dados de partidas de cada rodada do Campeonato Brasileiro 2024.
- Obtém informações detalhadas sobre as estatísticas de cada jogo, como gols, posse de bola, finalizações, entre outros.
- Armazena os dados coletados em uma base de dados Snowflake.

## Tecnologias Utilizadas

- **Python 3.x**
- **Selenium**: Para automação do navegador e interação com a página.
- **Pandas**: Para manipulação e organização dos dados.
- **SQLAlchemy**: Para interação com o banco de dados Snowflake.
- **dotenv**: Para carregamento de variáveis de ambiente (credenciais e configurações).
- **JSON**: Para manipulação dos dados retornados pela API.

## Pré-Requisitos

Antes de rodar o código, certifique-se de ter as seguintes dependências instaladas:

```bash
pip install selenium pandas sqlalchemy python-dotenv
