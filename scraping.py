from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os
import json
import pandas as pd


def get_request_selenium(url):
    try:
        options = Options()
        options.add_argument('window-size=400,800')
        options.add_argument('--headless')
        navegador = webdriver.Chrome(options=options)

        navegador.get(url)
        response_txt = navegador.find_element('tag name', 'body').text

        response_json = json.loads(response_txt)

        navegador.quit()
        return response_json

    except WebDriverException as e:
        return f"Erro de conexão ou falha no driver: {e}"

    except json.JSONDecodeError as e:
        return f"Erro ao decodificar o JSON: {e}"

    except ValueError as e:
        return str(e)

    except Exception as e:
        return f"Erro durante a requisição: {e}"


def championship_round():
    round_end = 38

    for round_num in range(1, round_end + 1):
        print('carrengando rodada numero '+str(round_num))
        url = 'https://www.sofascore.com/api/v1/unique-tournament/325/season/58766/events/round/'+str(round_num)
        response_json = get_request_selenium(url)
        matchs = []
        match_details = []

        for events in response_json.get('events', []):
            if events.get('status', {}).get('description') == 'Ended':
                match_info = {
                    'ID': events.get('id'),
                    'TEAM_HOME': events.get('homeTeam', {}).get('name'),
                    'TEAM_AWAY': events.get('awayTeam', {}).get('name'),
                    'SCORE_HOME': events.get('homeScore', {}).get('normaltime'),
                    'SCORE_AWAY': events.get('awayScore', {}).get('normaltime'),
                    'ROUND': round_num
                }
                matchs.append(match_info)
                match_details.extend(statistics_match(events.get('id')))

        send_database(pd.DataFrame(match_details), 'match_details', round_num)
        send_database(pd.DataFrame(matchs), 'matches', round_num)
        # print(pd.DataFrame(match_details))
        # print(pd.DataFrame(matchs))


def statistics_match(match_id):
    url = f'http://www.sofascore.com/api/v1/event/{match_id}/statistics'
    response_json = get_request_selenium(url)
    all_statistics = []

    for match_stats in response_json.get('statistics', []):
        period = match_stats.get('period')

        for group in match_stats.get('groups', []):
            group_name = group.get('groupName')

            for item in group.get('statisticsItems', []):
                all_statistics.append({
                    'ID_MATCH': match_id,
                    'TIME': period,
                    'GROUP': group_name,
                    'STATISTIC': item.get('name'),
                    'KEY': item.get('key'),
                    'STATS_HOME': item.get('home'),
                    'STATS_AWAY': item.get('away'),
                    'STATS_HOME_VALUE': item.get('homeValue'),
                    'STATS_AWAY_VALUE': item.get('awayValue')
                })

    return all_statistics


def send_database(df: pd.DataFrame, table: str, round_num: int):

    try:
        load_dotenv()

        account = os.getenv('SNOWFLAKE_ACCOUNT')
        user = os.getenv('SNOWFLAKE_USER')
        password = os.getenv('SNOWFLAKE_PASSWORD')
        warehouse = os.getenv('SNOWFLAKE_WAREHOUSE')
        database = os.getenv('SNOWFLAKE_DATABASE')
        schema = os.getenv('SNOWFLAKE_SCHEMA')

        connection_str = (
           f'snowflake://{user}:{password}@{account}/'
           f'{database}/{schema}?warehouse={warehouse}'
        )

        engine = create_engine(connection_str)

        with engine.connect() as connection:
            print("Conexão com o Snowflake realizada com sucesso!")
            if round_num == 1:
                df.to_sql(table, con=connection, index=False, if_exists='replace')
            else:
                df.to_sql(table, con=connection, index=False, if_exists='append')

    except Exception as e:
        print(f"Erro ao conectar ao Snowflake: {e}")


if __name__ == '__main__':
    championship_round()
