import json
from pprint import pprint
import threading

import sqlite3 as sq

import cloudscraper

scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'android',
        'desktop': False
    }
)

cookies = {
    '__Secure-ab-group': '46;',
    'ob_theme': 'DARK;',
    'ADDRESSBOOKBAR_WEB_CLARIFICATION': '1716216895;',
    'is_cookies_accepted': '1;',
    'xcid': 'af3e5f0ce15183783bfe1512b44f9fca;',
    'is_adult_confirmed': 'true;',
    'rfuid': 'NjkyNDcyNDUyLDEyNC4wNDM0NjYwNzExNDcxMiwtMjc5NTk3MzQzLC0xLC0xNTg0NDY5MTQxLFczc2libUZ0WlNJNklsQkVSaUJXYVdWM1pYSWlMQ0prWlhOamNtbHdkR2x2YmlJNklsQnZjblJoWW14bElFUnZZM1Z0Wlc1MElFWnZjbTFoZENJc0ltMXBiV1ZVZVhCbGN5STZXM3NpZEhsd1pTSTZJbUZ3Y0d4cFkyRjBhVzl1TDNCa1ppSXNJbk4xWm1acGVHVnpJam9pY0dSbUluMHNleUowZVhCbElqb2lkR1Y0ZEM5d1pHWWlMQ0p6ZFdabWFYaGxjeUk2SW5Ca1ppSjlYWDBzZXlKdVlXMWxJam9pUTJoeWIyMWxJRkJFUmlCV2FXVjNaWElpTENKa1pYTmpjbWx3ZEdsdmJpSTZJbEJ2Y25SaFlteGxJRVJ2WTNWdFpXNTBJRVp2Y20xaGRDSXNJbTFwYldWVWVYQmxjeUk2VzNzaWRIbHdaU0k2SW1Gd2NHeHBZMkYwYVc5dUwzQmtaaUlzSW5OMVptWnBlR1Z6SWpvaWNHUm1JbjBzZXlKMGVYQmxJam9pZEdWNGRDOXdaR1lpTENKemRXWm1hWGhsY3lJNkluQmtaaUo5WFgwc2V5SnVZVzFsSWpvaVEyaHliMjFwZFcwZ1VFUkdJRlpwWlhkbGNpSXNJbVJsYzJOeWFYQjBhVzl1SWpvaVVHOXlkR0ZpYkdVZ1JHOWpkVzFsYm5RZ1JtOXliV0YwSWl3aWJXbHRaVlI1Y0dWeklqcGJleUowZVhCbElqb2lZWEJ3YkdsallYUnBiMjR2Y0dSbUlpd2ljM1ZtWm1sNFpYTWlPaUp3WkdZaWZTeDdJblI1Y0dVaU9pSjBaWGgwTDNCa1ppSXNJbk4xWm1acGVHVnpJam9pY0dSbUluMWRmU3g3SW01aGJXVWlPaUpOYVdOeWIzTnZablFnUldSblpTQlFSRVlnVm1sbGQyVnlJaXdpWkdWelkzSnBjSFJwYjI0aU9pSlFiM0owWVdKc1pTQkViMk4xYldWdWRDQkdiM0p0WVhRaUxDSnRhVzFsVkhsd1pYTWlPbHQ3SW5SNWNHVWlPaUpoY0hCc2FXTmhkR2x2Ymk5d1pHWWlMQ0p6ZFdabWFYaGxjeUk2SW5Ca1ppSjlMSHNpZEhsd1pTSTZJblJsZUhRdmNHUm1JaXdpYzNWbVptbDRaWE1pT2lKd1pHWWlmVjE5TEhzaWJtRnRaU0k2SWxkbFlrdHBkQ0JpZFdsc2RDMXBiaUJRUkVZaUxDSmtaWE5qY21sd2RHbHZiaUk2SWxCdmNuUmhZbXhsSUVSdlkzVnRaVzUwSUVadmNtMWhkQ0lzSW0xcGJXVlVlWEJsY3lJNlczc2lkSGx3WlNJNkltRndjR3hwWTJGMGFXOXVMM0JrWmlJc0luTjFabVpwZUdWeklqb2ljR1JtSW4wc2V5SjBlWEJsSWpvaWRHVjRkQzl3WkdZaUxDSnpkV1ptYVhobGN5STZJbkJrWmlKOVhYMWQsV3lKeWRTSmQsMCwxLDAsMzAsMTQyNzUsOCwyMjcxMjY1MjAsMCwxLDAsLTQ5MTI3NTUyMyxSMjl2WjJ4bElFbHVZeTRnVG1WMGMyTmhjR1VnUjJWamEyOGdUV0ZqU1c1MFpXd2dOUzR3SUNoTllXTnBiblJ2YzJnN0lFbHVkR1ZzSUUxaFl5QlBVeUJZSURFd1h6RTFYemNwSUVGd2NHeGxWMlZpUzJsMEx6VXpOeTR6TmlBb1MwaFVUVXdzSUd4cGEyVWdSMlZqYTI4cElFTm9jbTl0WlM4eE1qQXVNQzR3TGpBZ1dXRkNjbTkzYzJWeUx6STBMakV1TUM0d0lGTmhabUZ5YVM4MU16Y3VNellnTWpBd016QXhNRGNnVFc5NmFXeHNZUT09LGV5SmphSEp2YldVaU9uc2lZWEJ3SWpwN0ltbHpTVzV6ZEdGc2JHVmtJanBtWVd4elpTd2lTVzV6ZEdGc2JGTjBZWFJsSWpwN0lrUkpVMEZDVEVWRUlqb2laR2x6WVdKc1pXUWlMQ0pKVGxOVVFVeE1SVVFpT2lKcGJuTjBZV3hzWldRaUxDSk9UMVJmU1U1VFZFRk1URVZFSWpvaWJtOTBYMmx1YzNSaGJHeGxaQ0o5TENKU2RXNXVhVzVuVTNSaGRHVWlPbnNpUTBGT1RrOVVYMUpWVGlJNkltTmhibTV2ZEY5eWRXNGlMQ0pTUlVGRVdWOVVUMTlTVlU0aU9pSnlaV0ZrZVY5MGIxOXlkVzRpTENKU1ZVNU9TVTVISWpvaWNuVnVibWx1WnlKOWZTd2lhVEU0YmlJNmUzMTlMQ0o1WVc1a1pYZ2lPbnNpYldWa2FXRWlPbnQ5TENKeVpXRmtZV0pwYkdsMGVTSTZlMzBzSW5CMVlteHBZMFpsWVhSMWNtVWlPbnNpVkhWeVltOUJjSEJUZEdGMFpTSTZleUpJUVZOZlFrVlVWRVZTWDFaRlVsTkpUMDRpT2lKb1lYTkNaWFIwWlhKV1pYSnphVzl1SWl3aVNVNWZVRkpQUjBWVFV5STZJbWx1VUhKdloyVnpjeUlzSWtsT1UxUkJURXhCVkVsUFRsOUZVbEpQVWlJNkltbHVjM1JoYkd4aGRHbHZia1Z5Y205eUlpd2lUa0ZXU1VkQlZFbFBUbDlVVDE5VlRrdE9UMWRPWDBGUVVFeEpRMEZVU1U5T0lqb2libUYyYVdkaGRHbHZibFJ2Vlc1cmJtOTNia0Z3Y0d4cFkyRjBhVzl1SWl3aVRrOVVYMGxPVTFSQlRFeEZSQ0k2SW01dmRFbHVjM1JoYkd4bFpDSXNJbEpGUVVSWlgwWlBVbDlWVTBVaU9pSnlaV0ZrZVVadmNsVnpaU0o5ZlgxOSw2NSwtMTI4NTU1MTMsMSwxLC0xLDE2OTk5NTQ4ODcsMTY5OTk1NDg4Nyw2MzU3ODA1MjYsOA', }


def get_product_data():
    '''Парсим сайт WB получаем данные о нашем товаре'''

    a = 'nike'
    b = 'кроссовки'
    c = '226312550'
    html = scraper.get(
        f"https://search.wb.ru/exactmatch/ru/common/v5/search?ab_testing=false&appType=1&curr=rub&dest=-1257786&query={a}%{b}%{c}&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false",
        cookies=cookies).text
    res = json.loads(html)

    product_id = ''
    price = ''
    brand = ''
    name = ''

    for i in res['data']['products']:
        if i['id'] == int(c):
            product_id = i['id']
            name = i['name']
            brand = i['brand']
            price = i['sizes'][0]['price']['product']

    return product_id, name, brand, price



def create_table():
    '''Создаем базу данных и таблицу'''
    with sq.connect('db_wb') as con:
        cursor = con.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS wb_data(
        product_id TEXT INTEGER PRIMARY KEY,
        name TEXT,
        brand TEXT,
        price INTEGER)''')
create_table()

def prepare():
    '''заполняем таблицу данными с сайта  wb'''
    create_table()
    product_id, name, brand, price = get_product_data()
    with sq.connect('db_wb') as con:
        cursor = con.cursor()
        cursor.execute('INSERT INTO wb_data(product_id,name,brand,price) VALUES(?,?,?,?)',
                       (product_id, name, brand, price))
        cursor.execute('SELECT product_id,price FROM wb_data')
        c = cursor.fetchone()
        id = c[0]
        current_price = c[1]
        print(id,current_price)
        return id, current_price

prepare()

def check_price():
    product_id, name, brand, price = get_product_data()

    with sq.connect('db_wb') as con:
        cursor = con.cursor()
        cursor.execute('SELECT product_id,price FROM wb_data')
        c = cursor.fetchone()
        p_id = c[0]
        new_price = c[1]
        price=22
        if new_price !=price:

            with sq.connect('db_wb') as con:
                cursor=con.cursor()
                cursor.execute("UPDATE wb_data SET price=3210 WHERE product_id='product_id'")
                cursor.execute('SELECT * FROM wb_data')
                f=cursor.fetchall()
                print(f)

        else:
            print('значение не изменилось')

check_price()
