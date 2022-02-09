from dadata import Dadata
import click
import sqlite3


def dbConnect(name=0, count=0, token=0, language=0, baseurl=0):
        conn = sqlite3.connect('settings.db')
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS settings (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name     STRING,
                                count    INTEGER,
                                token    STRING,
                                language STRING,
                                baseurl  STRING
                            );
                            ''')
        if count and name and token and language and baseurl:
            apiset = (None,  name, count, token, language, baseurl)
            cur.execute("INSERT INTO settings VALUES(?, ?, ?, ?, ?, ?);", apiset)
            conn.commit()
            return apiset
        else:
            cur.execute('''SELECT * FROM Settings ORDER BY id DESC LIMIT 1;''')
            apiset = cur.fetchone()
            return apiset


def daAPI(apisetting):

    ddt = Dadata(apisetting[3])

    ddt._suggestions.BASE_URL = apisetting[5]

    while True:
        query = click.prompt('Введите адрес или \'exit\' для выхода', type=str)
        print(apisetting)
        if query != 'exit':
            result = ddt.suggest(name=apisetting[1], query=query, count=apisetting[2], language=apisetting[4])
        else:
            ddt.close()
            break

        for i in range(len(result)):
            click.echo(str(i) + ' ' + result[i]['value'])

        while True:
            address_number = click.prompt('Введите номер нужного адреса', type=int, default=0)
            if isinstance(address_number, int):
                result = ddt.suggest(name=apisetting[1], query=result[address_number]['unrestricted_value'], count=1,
                                     language=apisetting[4])
                click.echo(result[0]['unrestricted_value'])
                click.echo('latitude:' + result[0]['data']['geo_lat'])
                click.echo('longitude:' + result[0]['data']['geo_lon'])
                break


@click.command()
@click.option('--name', '-n', default='str', help='Что искать: точный адрес(address), почтовое отделение(postal_unit), компанию(party)')
@click.option('--count', '-c',  default=1, help='Количество записей возвращаемых запросов (max 20)')
@click.option('--token', '-t', help='API ключ')
@click.option('--language', '-lan', default='str', help='Язык на котором будет возвращаться запрос')
@click.option('--baseurl', '-bu', default='str', help='')
def main(name=0, count=0, token=0, language=0, baseurl=0):
    '''
    Скрипт используется для определения координат введённого адреса
    '''
    settings = dbConnect(name, count, token, language, baseurl)
    daAPI(settings)


if __name__ == '__main__':
    main()
