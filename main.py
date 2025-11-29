import requests
import json
import datetime
import psycopg
from psycopg.rows import dict_row

email = "sleepwalking1113@gmail.com"
password = "Yoquesetio1"


class RequestEngine():
    def __init__(self):
        self.token = None
        self.id = None
        self.name = None
        self.email = None
        self.current_league_id = '2039584' # SELECCIONAR LIGA
        self.current_user_id_league = '13299804' # COGER ID DEL USUARIO EN LA LIGA

    

    def get_login(self, email, password):
        url = "https://biwenger.as.com/api/v2/auth/login"
        headers = {
            # "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
            # "Content-Type": "application/json; charset=UTF-8",
            # "Accept": "application/json",
            # "X-Lang": "en"
        }
        data = {
            "email": email,
            "password": password
        }

        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            print("\033[91mLogin Failed\033[0m")
            raise Exception("Login Failed")
        else:
            print("\033[92mLogin Succeeded\033[0m")

        data_dict = response.json()
        self.token = data_dict['token']
        if not self.token:
            raise Exception("Login succeeded but no token was returned.")
        return None

    def get_account_info(self):
        url = "https://biwenger.as.com/api/v2/account"
        headers = {
            "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOjI3NzU4MDQ1LCJpYXQiOjE3NjM4NDY2Njd9.QHoySfb3vBGV8yR4SETnfCJTlwZ4eYwIsG9tK0ASYxo",
            # "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
            # "X-Version": "629",
            # "X-Lang": "en",
            # "Accept": "application/json"
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print("\033[91mAccount Info Failed\033[0m")
            raise Exception("Account Info Failed")
        else:
            print("\033[92mAccount Info Succeeded\033[0m")
        response_dict = response.json()
        # Account Info
        self.id = response_dict['data']['account']['id']
        self.name = response_dict['data']['account']['name']
        self.email = response_dict['data']['account']['email']
       

    def get_leagues_info(self):
        url = "https://biwenger.as.com/api/v2/account"
        headers = {
            "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOjI3NzU4MDQ1LCJpYXQiOjE3NjM4NDY2Njd9.QHoySfb3vBGV8yR4SETnfCJTlwZ4eYwIsG9tK0ASYxo",
            # "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
            # "X-Version": "629",
            # "X-Lang": "en",
            # "Accept": "application/json"
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print("\033[91mLeague Info Failed\033[0m")
            raise Exception("League Info Failed")
        else:
            print("\033[92mLeague Info Succeeded\033[0m")
        response_dict = response.json()   
        # Leagues Info
        # MORE INFO CAN BE OBTAINED HERE FROM LEAGUES
        leagues_data = []
        for league in response.json()['data']['leagues']:
            league_data = {
                'league_name' : league['name'],
                'league_id' : league['id'],
                'competition' : league['competition'],
                'creation_date' : datetime.datetime.fromtimestamp(league['created']).strftime("%Y-%m-%d")
            }
            leagues_data.append(league_data)
        # [print(league) for league in leagues_data]
        return leagues_data

    def get_global_player_info(self):
        url = "https://cf.biwenger.com/api/v2/competitions/la-liga/data"
        params = {
        # "lang": "en",
        # "score": "5",
        # "callback": "jsonp_1912703209"
        }
        headers = {
        #   "Host": "cf.biwenger.com",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
        #  "Accept": "*/*",
        #  "Accept-Language": "en-GB,en;q=0.9",
        #  "Referer": "https://biwenger.as.com/",
        #  "Accept-Encoding": "gzip, deflate, br",
        #  "Sec-Ch-Ua": '"Chromium";v="141", "Not?A_Brand";v="8"',
        #  "Sec-Ch-Ua-Mobile": "?0",
        #  "Sec-Ch-Ua-Platform": '"Linux"',
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print("\033[91mGlobal Player Info Failed\033[0m")
            raise Exception("Global Player Info Failed")
        else:
            print("\033[92mGlobal player Info Succeeded\033[0m")
        response_dict = response.json()
        # print(response_dict['data']['season']) AQUI HAY INFO DE SI LA JORNADA HA TERMINADO
        players_info = []
        value_sum = 0 # TOTAL MARKET VALUE
        for key in response_dict['data']['players']:
            players_info.append(response_dict['data']['players'][key])
            value_sum += int(response_dict['data']['players'][key]['price'])

        # [print(info, '\n') for info in players_info]
        # print(value_sum)
        return players_info

    def get_my_players_league(self):
        url = "https://biwenger.as.com/api/v2/user"
        params = {
            "fields": "*,lineup(type,playersID,reservesID,captain,striker,coach,date),"
                    "players(id,owner),market,offers,-trophies"
        }
        headers = {
            "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOjI3NzU4MDQ1LCJpYXQiOjE3NjM4NDY3NDZ9.50VWJ9afeXey3fS49LeN6uluJNUK-FN9Kz4p4Wy-zp4",
            "X-User": self.current_user_id_league,
            "X-League": self.current_league_id,
            # "X-Version": "629",
            # "X-Lang": "en",
            # "Accept": "application/json",
            # "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print("\033[91mLeague Players Info Failed\033[0m")
            raise Exception("League Players Info Failed")
        else:
            print("\033[92mLeague players Info Succeeded\033[0m")
        response_dict = response.json()
        player_list = []
        for player in response_dict['data']['players']:
            player_list.append(player['id'])
        return player_list

    def get_others_team_info(self):
        url = "https://biwenger.as.com/api/v2/league"
        params = {
            "include": "all,-lastAccess",
            "fields": "*,standings,tournaments,group,settings(description)"
        }

        headers = {
            "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOjI3NzU4MDQ1LCJpYXQiOjE3NjM4NDY3NDZ9.50VWJ9afeXey3fS49LeN6uluJNUK-FN9Kz4p4Wy-zp4",
            "X-User": self.current_user_id_league,
            "X-League": self.current_league_id,
            # "X-Version": "629",
            # "X-Lang": "en",
            # "Accept": "application/json",
            # "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print("\033[91mOther Team Info Failed\033[0m")
            raise Exception("Other Team Info Failed")
        else:
            print("\033[92mOther Team Info Succeeded\033[0m")
        response_dict = response.json()
        # [print(player) for player in response_dict['data']['standings']]
        players_info = []
        for player in response_dict['data']['standings']:
            player_info = {
                'id' : player['id'],
                'name' : player['name'],
                'team_value' : player['teamValue'],
                'n_players' : player['teamSize'],
                'team_value_variation' : player['teamValueInc']
            }
            players_info.append(player_info)
        return players_info


    def get_transfer_info(self):
        url = "https://biwenger.as.com/api/v2/home"
        headers = {
            "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOjI3NzU4MDQ1LCJpYXQiOjE3NjM4NDY3NDZ9.50VWJ9afeXey3fS49LeN6uluJNUK-FN9Kz4p4Wy-zp4",
            "X-User": self.current_user_id_league,
            "X-League": self.current_league_id,
            # "X-Version": "629",
            # "X-Lang": "en",
            # "Accept": "application/json",
            # "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print("\033[91Transfer Info Failed\033[0m")
            raise Exception("Transfer Info Failed")
        else:
            print("\033[92mTransfer Info Succeeded\033[0m")
        response_dict = response.json()
        transfer_list = response_dict['data']['league']['board']
        transfers = []
        for transfer in transfer_list:
            if transfer['type'] == 'market':
                transfers.append(transfer['content'])
        return transfers


class HandleDatabase():
    def __init__(self, host="localhost", port=5432, user="postgres", password="", dbname=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.dbname = dbname
        self.conn = None
    
    def create_database(self, database_name):
        try:
            with psycopg.connect(
                dbname="postgres",
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
            ) as conn:
                conn.autocommit = True

                with conn.cursor() as cur:
                    cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{database_name}';")
                    exists = cur.fetchone()

                    if exists:
                        print(f"Database '{database_name}' already exists.")
                    else:
                        cur.execute(f"CREATE DATABASE {database_name};")
                        print(f"Database '{database_name}' created successfully.")

        except Exception as e:
            print("Error creating database:", e)

    def connect(self):
        """Establece conexión a la base de datos objetivo."""
        try:
            self.conn = psycopg.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                row_factory=dict_row  # devolver diccionarios
            )
            print(f"Connected to database '{self.dbname}'.")
        except Exception as e:
            print("Error connecting:", e)

    def close(self):
        """Cierra la conexión."""
        if self.conn:
            self.conn.close()
            self.conn = None
            print("Connection closed.")

    def create_tables(self):
        queries = [
            """
            CREATE TABLE IF NOT EXISTS players (
                player_id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                team VARCHAR(100),
                position VARCHAR(20)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS player_prices (
                player_id INT REFERENCES players(player_id),
                date DATE NOT NULL,
                price NUMERIC NOT NULL,
                PRIMARY KEY (player_id, date)
            );
            """,
            # Este índice se crea para optimizar las consultas del precio de todos los jugadores para un día concreto
            """
            CREATE INDEX IF NOT EXISTS idx_player_prices_date
            ON player_prices (date);
            """
        ]

        try:
            with self.conn.cursor() as cur:
                for q in queries:
                    cur.execute(q)
            self.conn.commit()
            print("Tables created successfully.")
        except Exception as e:
            print("Error creating tables:", e)
            self.conn.rollback()

    def execute_query(self, query, params=None, fetch=False):
        """Ejecuta una query SQL genérica."""
        try:
            with self.conn.cursor() as cur:
                cur.execute(query, params or ())
                if fetch:
                    return cur.fetchall()
                self.conn.commit()
        except Exception as e:
            print("❌ Query error:", e)
            self.conn.rollback()


    def insert_many(self, query, rows):
        """Inserta múltiples filas (bulk insert)."""
        try:
            with self.conn.cursor() as cur:
                cur.executemany(query, rows)
            self.conn.commit()
        except Exception as e:
            print("❌ Bulk insert error:", e)
            self.conn.rollback()

    def insert_one(self, query, params):
        """Inserta una sola fila."""
        self.execute_query(query, params)



def insert_player_info(request_engine, database_engine):
    player_info = request_engine.get_global_player_info()
    query = """
        INSERT INTO players (player_id, name, team, position)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (player_id) DO UPDATE
        SET name = EXCLUDED.name,
            team = EXCLUDED.team,
            position = EXCLUDED.position;
    """

    rows = [
        ]
    
    for player in player_info:
        data = (player['id'], player['name'], player['position'], player['teamID'])
        rows.append(data)
    database_engine.insert_many(query, rows)        


if __name__ == "__main__":
    request_engine = RequestEngine()
    # engine.get_login(email, password)
    # engine.get_account_info()
    # engine.get_leagues_info()
    # engine.get_global_player_info()
    # engine.get_my_players_league()
    # engine.get_others_team_info()
    # engine.get_transfer_info()

    database_engine = HandleDatabase(password="Yoquesetio1", dbname='mark_database')
    # database_engine.create_database('mark_database')
    database_engine.connect()
    # database_engine.create_tables()
    # database_engine.close()

    insert_player_info(request_engine, database_engine)

    