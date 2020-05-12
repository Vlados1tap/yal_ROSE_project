import sqlite3

from bs4 import BeautifulSoup
import requests
from datetime import date
from datetime import datetime
from flask import Flask, url_for, request, render_template

app = Flask(__name__)


@app.route('/form_sample', methods=['POST', 'GET'])
def form_sample():
    global nmp
    nmp = 0
    if request.method == 'GET':
        return f'''<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                            <link rel="stylesheet"
                            href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
                            integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh"
                            crossorigin="anonymous">
                            <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}"/>
                            <title>Пример формы</title>
                          </head>
                          <body>
                            <h1>Форма для участия в рассылке новостей</h1>
                            <div>
                                <form class="login_form" method="post">
                                    <input type="text" class="form-control" id="text" aria-describedby="emailHelp" placeholder="Введите фамилию" name="text">
                                    <input type="text" class="form-control" id="text" placeholder="Введите имя" name="text">
                                    <input type="email" class="form-control" id="email" aria-describedby="emailHelp" placeholder="Введите адрес почты" name="email">
                                    <div class="form-group">
                                        <label for="form-check">Выбор основной темы предлагаемых новостей</label>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="sex" id="male" value="finance_news" checked>
                                          <label class="form-check-label" for="male">
                                            Финансовые новости
                                          </label>
                                        </div>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="sex" id="male" value="world_news">
                                          <label class="form-check-label" for="female">
                                            Мировые новости
                                          </label>
                                        </div>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="sex" id="female" value="politic_news">
                                          <label class="form-check-label" for="female">
                                            Новости о политике
                                          </label>
                                     </div>
                                    <div>
                                <form class="login_form" method="post">
                                        <label for="classSelect">Выберите актуальность новостей</label>
                                        <select class="form-control" id="classSelect" name="class">
                                          <option>1 день</option>
                                          <option>2 дня</option>
                                          <option>3 дня</option>
                                        </select>
                                     </div>
                                     </div>
                                    <button type="submit" class="btn btn-primary">Отправить</button>
                                </form>
                            </div>
                          </body>
                        </html>'''
    elif request.method == 'POST':
        global email
        global news_type
        global actual
        email = request.form['email']
        news_type = request.form['sex']
        actual = request.form['class']
        print(actual)

        def super_parser():
            def parse():
                global a
                global b
                a = []
                b = []
                current_datetime = date.today()
                current_datetime2 = datetime.now()
                print(current_datetime)
                URL = 'https://www.rbc.ru/'
                HEADERS = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
                }

                response = requests.get(URL, headers=HEADERS)
                soup = BeautifulSoup(response.content, 'html.parser')
                items = soup.findAll('div', class_='main__feed js-main-reload-item')
                comps = []
                for item in items:
                    comps.append({
                        'title': item.find('a', class_='main__feed__link js-yandex-counter').get_text(strip=True),
                        'link': item.find('a', class_='main__feed__link js-yandex-counter').get('href')
                    })
                for comp in comps:
                    print(f'{comp["title"]} ->> Link: {comp["link"]}' + ' ' + str(current_datetime2))
                    a.append(comp["title"])
                    b.append(comp["link"])

            parse()

            def sqlite_create():
                con = sqlite3.connect('RBKgg.sqlite')

                cur = con.cursor()
                cur.execute('CREATE TABLE IF NOT EXISTS adjustments(first_news TEXT, '
                            'second_news STRING, '
                            'third_news STRING, '
                            'fourth_news STRING, '
                            'fifth_news STRING, '
                            'sixth_news STRING, '
                            'seventh_news STRING, '
                            'eighth_news STRING, '
                            'ninth_news STRING, '
                            'tenth_news STRING, '
                            'eleventh_news STRING, '
                            'twelfth_news STRING, '
                            'thirteenth_news STRING, '
                            'fourteens_news STRING, '
                            'fifteenth_news STRING) ')
                cur.execute('CREATE TABLE IF NOT EXISTS links(first_news TEXT, '
                            'second_news STRING, '
                            'third_news STRING, '
                            'fourth_news STRING, '
                            'fifth_news STRING, '
                            'sixth_news STRING, '
                            'seventh_news STRING, '
                            'eighth_news STRING, '
                            'ninth_news STRING, '
                            'tenth_news STRING, '
                            'eleventh_news STRING, '
                            'twelfth_news STRING, '
                            'thirteenth_news STRING, '
                            'fourteens_news STRING, '
                            'fifteenth_news STRING) ')
                for i in range(len(a)):
                    if a[i] != data[len(data) - 1][i]:
                        cur.execute('INSERT INTO adjustments VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', a)
                        break
                for i in range(len(b)):
                    if b[i] != data2[len(data2) - 1][i]:
                        cur.execute('INSERT INTO links VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', b)
                        break

                con.commit()
                cur.close()
                con.close()

            def sqlite_read(database, table, column_name=None):
                global data
                con = sqlite3.connect(database)
                cur = con.cursor()
                columns = 'pragma table_info(' + table + ')'
                cur.execute(columns)
                col_disc = cur.fetchall()
                if column_name is None:
                    query = 'SELECT * FROM ' + table
                    cur.execute(query)
                    data = cur.fetchall()

            def sqlite_read2(database, table2, column_name2=None):
                global data2
                con = sqlite3.connect(database)
                cur = con.cursor()
                columns = 'pragma table_info(' + table2 + ')'
                cur.execute(columns)
                col_disc = cur.fetchall()
                if column_name2 is None:
                    query = 'SELECT * FROM ' + table2
                    cur.execute(query)
                    data2 = cur.fetchall()

            def comparison():
                global kf_saver
                kf_saver = 0
                global save_news
                save_news = []
                global save_links
                save_links = []
                global x
                x = []
                global y
                y = []
                global z
                z = []
                global x_links
                x_links = []
                global y_links
                y_links = []
                global z_links
                z_links = []
                if actual == '1 день':
                    kf_saver = 0
                elif actual == '2 дня':
                    kf_saver = 8
                elif actual == '3 дня':
                    kf_saver = 17
                if kf_saver != 0:
                    for i in range(len(data) - 1 - kf_saver, len(data) - 1):
                        for j in range(len(data[i])):
                            save_news.append(data[i][j])
                    for i in range(len(data2) - 1 - kf_saver, len(data2) - 1):
                        for j in range(len(data2[i])):
                            save_links.append(data2[i][j])
                else:
                    if news_type == 'finance_news':
                        currency = ['доллар', 'евро', 'рубль', 'гривна', 'кризис', '$', '₽', '€', 'банк', 'финанс',
                                    'акци']
                        for i in range(len(data[len(data) - 1])):
                            for j in range(len(currency)):
                                if currency[j] in data[len(data) - 1][i]:
                                    x.append(data[len(data) - 1][i])
                                    x_links.append(data2[len(data2) - 1][i])
                        if len(x) == 0:
                            print('Актуальных новостей на сегодняшнее число нету')
                        else:
                            print((set(x)))
                    elif news_type == 'world_news':
                        world_words = ['Коронавирус', 'Илон Маск', 'Лондон', 'COVID-19', 'коронавирус', 'пандемия',
                                       'США', 'штаты', 'бой', 'смерт', 'взрыв', 'умер', 'Росси', 'Власти']
                        for i in range(len(data[len(data) - 1])):
                            for j in range(len(world_words)):
                                if world_words[j] in data[len(data) - 1][i]:
                                    y.append(data[len(data) - 1][i])
                                    y_links.append(data2[len(data2) - 1][i])
                        if len(y) == 0:
                            print('Актуальных новостей на сегодняшнее число нету')
                        else:
                            print((set(y)))
                            print((set(y_links)))
                    elif news_type == 'politic_news':
                        politic_names_and_best_themes = ['Путин', 'Трамп', 'Кремль', 'Собянин']
                        for i in range(len(data[len(data) - 1])):
                            for j in range(len(politic_names_and_best_themes)):
                                if politic_names_and_best_themes[j] in data[len(data) - 1][i]:
                                    z.append(data[len(data) - 1][i])
                                    z_links.append(data2[len(data2) - 1][i])
                        if len(z) == 0:
                            print('Актуальных новостей на сегодняшнее число нету')
                        else:
                            print((set(z)))
                            print((set(z_links)))
                print(set(save_links))
                print(set(save_news))
                if kf_saver != 0:
                    if news_type == 'finance_news':
                        currency = ['доллар', 'евро', 'рубль', 'гривна', 'кризис', '$', '₽', '€', 'банк', 'финанс',
                                    'акци']
                        for i in range(len(save_news)):
                            for j in range(len(currency)):
                                if currency[j] in save_news[i]:
                                    x.append(save_news[i])
                                    x_links.append(save_links[i])
                        if len(x) == 0:
                            print('Актуальных новостей на сегодняшнее число нету')
                        else:
                            print((set(x)))
                    elif news_type == 'world_news':
                        world_words = ['Коронавирус', 'Илон Маск', 'Лондон', 'COVID-19', 'коронавирус', 'пандемия',
                                       'США', 'штаты', 'бой', 'смерт', 'взрыв', 'умер', 'Росси', 'Власти']
                        for i in range(len(save_news)):
                            for j in range(len(world_words)):
                                if world_words[j] in save_news[i]:
                                    y.append(save_news[i])
                                    y_links.append(save_links[i])
                        if len(y) == 0:
                            print('Актуальных новостей на сегодняшнее число нету')
                        else:
                            print((set(y)))
                            print((set(y_links)))
                    elif news_type == 'politic_news':
                        politic_names_and_best_themes = ['Путин', 'Трамп', 'Кремль', 'Собянин']
                        for i in range(len(save_news)):
                            for j in range(len(politic_names_and_best_themes)):
                                if politic_names_and_best_themes[j] in save_news[i]:
                                    z.append(save_news[i])
                                    z_links.append(save_links[i])
                        if len(z) == 0:
                            print('Актуальных новостей на сегодняшнее число нету')
                        else:
                            print((set(z)))
                            print((set(z_links)))

                if kf_saver == 17:
                    if news_type == 'finance_news':
                        currency = ['доллар', 'евро', 'рубль', 'гривна', 'кризис', '$', '₽', '€', 'банк', 'финанс', 'акци']
                        for i in range(len(data[len(data) - 1])):
                            for j in range(len(currency)):
                                if currency[j] in data[len(data) - 1][i]:
                                    x.append(data[len(data) - 1][i])
                                    x_links.append(data2[len(data2) - 1][i])
                        if len(x) == 0:
                            print('Актуальных новостей на сегодняшнее число нету')
                        else:
                            print((set(x)))
                    elif news_type == 'world_news':
                        world_words = ['Коронавирус', 'Илон Маск', 'Лондон', 'COVID-19', 'коронавирус', 'пандемия', 'США', 'штаты', 'бой', 'смерт', 'взрыв', 'умер', 'Росси', 'Власти']
                        for i in range(len(data[len(data) - 1])):
                            for j in range(len(world_words)):
                                if world_words[j] in data[len(data) - 1][i]:
                                    y.append(data[len(data) - 1][i])
                                    y_links.append(data2[len(data2) - 1][i])
                        if len(y) == 0:
                            print('Актуальных новостей на сегодняшнее число нету')
                        else:
                            print((set(y)))
                            print((set(y_links)))
                    elif news_type == 'politic_news':
                        politic_names_and_best_themes = ['Путин', 'Трамп', 'Кремль', 'Собянин']
                        for i in range(len(data[len(data) - 1])):
                            for j in range(len(politic_names_and_best_themes)):
                                if politic_names_and_best_themes[j] in data[len(data) - 1][i]:
                                    z.append(data[len(data) - 1][i])
                                    z_links.append(data2[len(data2) - 1][i])
                        if len(z) == 0:
                            print('Актуальных новостей на сегодняшнее число нету')
                        else:
                            print((set(z)))
                            print((set(z_links)))

            if __name__ == '__main__':
                database = 'RBKgg.sqlite'
                table = 'adjustments'
                table2 = 'links'
                sqlite_read(database, table)
                sqlite_read2(database, table2)
                sqlite_create()
                comparison()

        super_parser()
        if news_type == 'finance_news' and len(x) != 0:
            return render_template('base.html', user_list=set(x), general=set(x_links))
        elif news_type == 'world_news' and len(y) != 0:
            return render_template('base.html', user_list=set(y), general=set(y_links))
        elif news_type == 'politic_news' and len(z) != 0:
            return render_template('base.html', user_list=set(z), general=set(z_links))
        else:
            return render_template('base2.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')