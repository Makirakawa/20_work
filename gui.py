import flet as ft
import psycopg2 as pg
from flet import Column

from db_conf import dbname, user, password, host, port


def database_connect():
    try:
        connection = pg.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        connection.autocommit = True
        return connection

    except Exception as _ex:
        print(f"Error connecting to PostgreSQL database", _ex)
        return None


def main(page: ft.Page):
    page.clean()
    page.window.height = 100
    page.window.wight = 100

    def menu_page():
        page.clean()
        page.window.height = 900
        page.window.wight = 1600
        page.add(
            ft.Column([
                ft.Button("Фермы", on_click= lambda _: farms_record_page() ),
                ft.Button("Пушнина на аукционе", on_click= lambda _: lots_record_page() ),
                ft.Button("Результаты аукциона", on_click= lambda _: auction_results() ),
            ])
        )

    def farms_record_page():
        page.clean()
        page.update()
        page.window.height = 900
        page.window.wight = 1600

        def connect_to_farms_table():
            conn = database_connect()
            if conn is None:
                return conn
            try:
                with conn.cursor() as cursor:
                    cursor.execute('''SELECT * FROM farm_table;''')
                    return cursor.fetchall()

            except Exception as _ex:
                print("Error connecting to farms table", _ex)
            finally:
                if conn:
                    conn.close()

        def insert_to_farm_table():
            conn = database_connect()
            if conn is None:
                return conn
            try:
                with conn.cursor() as cursor:
                    cursor.execute(f"INSERT INTO farm_table(addres, director, phone) VALUES('{adress_textfield.value}','{director_textfield.value}','{phone_textfield.value}')")
                page.update()
            except Exception as _ex:
                print("Error connecting to farms table", _ex)
            finally:
                page.pop_dialog()
                page.update()
                if conn:
                    conn.close()

        farms = connect_to_farms_table()

        rows = []
        if farms:
            for farm in farms:
                rows.append(
                    ft.DataRow([
                        ft.DataCell(ft.Text(str(farm[0]))),
                        ft.DataCell(ft.Text(str(farm[1]))),
                        ft.DataCell(ft.Text(str(farm[2]))),
                        ft.DataCell(ft.Text(str(farm[3]))),
                    ])
                )
        modal_page = ft.AlertDialog(
            modal=True,
            title=ft.Text("Добавить пользователя"),
            content=ft.Column([
                adress_textfield := ft.TextField(label="Адрес"),
                director_textfield := ft.TextField(label="Директор"),
                phone_textfield := ft.TextField(label="Номер телефона"),
            ]),
            actions=[
                ft.Row([
                    ft.Button("Применить", on_click=lambda _: insert_to_farm_table()),
                    ft.Button("Отмена", on_click=lambda e: page.pop_dialog()),
                ])
            ]
        )
        page.add(
            ft.Row([
                ft.Button("Назад",width=100, height=50, on_click=lambda _: menu_page()),
            ]),
            ft.Row([
                ft.Text("Зверофермы", size=20)
            ]),
            ft.Row([
                ft.Column([
                    ft.DataTable(
                        columns=[
                            ft.DataColumn(label=ft.Text("ID фермы")),
                            ft.DataColumn(label=ft.Text("Адрес")),
                            ft.DataColumn(label=ft.Text("Фамилия директора")),
                            ft.DataColumn(label=ft.Text("Телефон")),
                        ],
                        rows=rows,
                    )
                ]),
                ft.Column([
                    ft.Button(content="Insert", on_click=lambda _: page.show_dialog(modal_page)),
                ])
            ])

        )

    def lots_record_page():
        page.clean()
        page.window.height = 900
        page.window.wight = 1600

        page.add(
            ft.Row([
                ft.Button("Назад", on_click=lambda _: menu_page()),
            ]),
            ft.Row([
                ft.Text("Пушнина на аукционе", size=20)
            ])

        )

    def auction_results():
        page.clean()
        page.window.height = 900
        page.window.wight = 1600
        page.add(
            ft.Row([
                ft.Button("Назад", on_click=lambda _: menu_page()),
            ]),
            ft.Row([
                ft.Test("Результаты аукциона", size=20)
            ]),
        )
    menu_page()


ft.run(main)
