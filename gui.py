import flet as ft
import psycopg2 as pg

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
                ft.Button("Фермы", on_click=lambda _: farms_record_page()),
                ft.Button("Пушнина на аукционе", on_click=lambda _: lots_record_page()),
                ft.Button("Результаты аукциона", on_click=lambda _:...() ),
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
                    cursor.execute(
                        f"INSERT INTO farm_table(addres, director, phone) VALUES('{adress_textfield.value}','{director_textfield.value}','{phone_textfield.value}')")
                page.update()
            except Exception as _ex:
                print("Error connecting to farms table", _ex)
            finally:
                page.pop_dialog()
                page.clean()
                farms_record_page()
                if conn:
                    conn.close()

        def delete_on_farm_table(farm_id):
            conn = database_connect()
            if conn is None:
                return conn
            try:
                with conn.cursor() as cursor:
                    cursor.execute(f"DELETE FROM farm_table WHERE farm_id = (%s)", (farm_id,))
                    conn.commit()
            except Exception as _ex:
                print("Error connecting to farms table", _ex)
            finally:
                page.pop_dialog()
                page.clean()
                farms_record_page()
                if conn:
                    conn.close()

        def edit_on_farm_table(farm_id, addres, director, phone):
            conn = database_connect()
            if conn is None:
                return conn
            try:
                with conn.cursor() as cursor:
                    cursor.execute(f"UPDATE farm_table SET addres=%s, director=%s, phone=%s WHERE farm_id=%s",
                                   ( addres, director, phone, farm_id))
                    conn.commit()
            except Exception as _ex:
                print("Error connecting to farms table", _ex)
            finally:
                page.pop_dialog()
                page.clean()
                farms_record_page()
                if conn:
                    conn.close()


        def edit_modal_page(farm):
            print("Открываю диалог", farm)
            address = ft.TextField(label="Адрес", value=farm[1])
            director = ft.TextField(label="Директор", value=farm[2])
            phone = ft.TextField(label="Номер телефона", value=farm[3])
            modal_dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Редактировать запись"),
                content=ft.Column([
                    address,
                    director,
                    phone
                ]),
                actions=[
                    ft.TextButton("Сохранить",
                                  on_click=lambda e: edit_on_farm_table(farm[0], address.value, director.value,
                                                                        phone.value)
                                  ),
                    ft.TextButton("Отмена", on_click=lambda e: page.pop_dialog())
                ]
            )
            page.show_dialog(modal_dialog)
            page.update()
            print("Диалог открыт")

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

                        ft.DataCell(
                            ft.IconButton(icon=ft.Icons.DELETE, icon_color="red",on_click=lambda e, id=farm[0]: delete_on_farm_table(id))
                        ),
                        ft.DataCell(
                            ft.IconButton(icon=ft.Icons.EDIT,icon_color="green",on_click=lambda e, farm=farm: edit_modal_page(farm)
                                          )
                        )
                    ])
                )
        modal_page = ft.AlertDialog(
            modal=True,
            title=ft.Text("Добавить запись"),
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
                ft.Button("Назад", width=100, height=50, on_click=lambda _: menu_page()),
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
                            ft.DataColumn(label=ft.Text("Удалить")),
                            ft.DataColumn(label=ft.Text("Редактировать")),
                        ],
                        rows=rows,
                    )
                ]),
                ft.Column([
                    ft.Button(content="Insert", on_click=lambda _: page.show_dialog(modal_page)),
                ])
            ])

        )
            #________________________________________________________________________________________________________________lots_record_page
    def lots_record_page():
        page.clean()
        page.update()
        page.window.height = 900
        page.window.wight = 1600

        def connect_to_lots_table():
            conn = database_connect()
            if conn is None:
                return conn
            try:
                with conn.cursor() as cursor:
                    cursor.execute('''SELECT * FROM lots;''')
                    return cursor.fetchall()

            except Exception as _ex:
                print("Error connecting to farms table", _ex)
            finally:
                if conn:
                    conn.close()

        def insert_to_lots_table():
            conn = database_connect()
            if conn is None:
                return conn
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        f"INSERT INTO lots(fur_name, quantity, declared_price) VALUES('{fur_name.value}','{quantity.value}','{declared_price.value}')")
                page.update()
            except Exception as _ex:
                print("Error connecting to farms table", _ex)
            finally:
                page.pop_dialog()
                page.clean()
                lots_record_page()
                if conn:
                    conn.close()

        def delete_on_lots_table(lot_id):
            conn = database_connect()
            if conn is None:
                return conn
            try:
                with conn.cursor() as cursor:
                    cursor.execute(f"DELETE FROM lots WHERE farm_id = (%s)", (lot_id,))
                    conn.commit()
            except Exception as _ex:
                print("Error connecting to farms table", _ex)
            finally:
                page.pop_dialog()
                page.clean()
                lots_record_page()
                if conn:
                    conn.close()

        def edit_on_lots_table(lot_id, fur_name, quantity, declared_price):
            conn = database_connect()
            if conn is None:
                return conn
            try:
                with conn.cursor() as cursor:
                    cursor.execute(f"UPDATE lots SET fur_name=%s, quantity=%s, declared_price=%s WHERE lot_id=%s",(fur_name, quantity, declared_price, lot_id))
                    conn.commit()
            except Exception as _ex:
                print("Error connecting to farms table", _ex)
            finally:
                page.pop_dialog()
                page.clean()
                lots_record_page()
                if conn:
                    conn.close()

        def edit_modal_page(lot):
            print("Открываю диалог", lot)
            fur_name = ft.TextField(label="Номер зверофермы", value=lot[1])
            quantity = ft.TextField(label="Адрес", value=lot[2])
            declared_price = ft.TextField(label="Фамилия директора", value=lot[3])
            modal_dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Редактировать запись"),
                content=ft.Column([
                    fur_name,
                    quantity,
                    declared_price
                ]),
                actions=[
                    ft.TextButton("Сохранить", on_click=lambda e: edit_on_lots_table(lot[0], fur_name.value, quantity.value, declared_price.value)),
                    ft.TextButton("Отмена", on_click=lambda e: page.pop_dialog())
                ]
            )
            page.show_dialog(modal_dialog)
            page.update()
            print("Диалог открыт")

        lots = connect_to_lots_table()

        rows = []
        if lots:
            for lot in lots:
                print(lot, len(lot))
                rows.append(
                    ft.DataRow([
                        ft.DataCell(ft.Text(str(lot[0]))),
                        ft.DataCell(ft.Text(str(lot[1]))),
                        ft.DataCell(ft.Text(str(lot[2]))),
                        ft.DataCell(ft.Text(str(lot[3]))),
                        ft.DataCell(ft.Text(str(lot[4]))),

                        ft.DataCell(
                            ft.IconButton(icon=ft.Icons.DELETE, icon_color="red",
                                          on_click=lambda e, id=lot[0]: delete_on_lots_table(id))),
                        ft.DataCell(
                            ft.IconButton(icon=ft.Icons.EDIT, icon_color="green",
                                          on_click=lambda e, lot=lot: edit_modal_page(lot)))
                    ])
                )
        modal_page = ft.AlertDialog(
            modal=True,
            title=ft.Text("Добавить запись"),
            content=ft.Column([
                fur_name := ft.TextField(label="Название шерсти"),
                quantity := ft.TextField(label="Количество"),
                declared_price := ft.TextField(label="Заявленная цена за единицу"),
            ]),
            actions=[
                ft.Row([
                    ft.Button("Применить", on_click=lambda _: insert_to_lots_table()),
                    ft.Button("Отмена", on_click=lambda e: page.pop_dialog()),
                ])
            ]
        )
        page.add(
            ft.Row([
                ft.Button("Назад", width=100, height=50, on_click=lambda _: menu_page()),
            ]),
            ft.Row([
                ft.Text("Пушнина на аукционе", size=20)
            ]),
            ft.Row([
                ft.Column([
                    ft.DataTable(
                        columns=[
                            ft.DataColumn(label=ft.Text("Номер лота")),
                            ft.DataColumn(label=ft.Text("Номер зверофермы")),
                            ft.DataColumn(label=ft.Text("Название меха")),
                            ft.DataColumn(label=ft.Text("Количество единиц")),
                            ft.DataColumn(label=ft.Text("Заявленная цена за единицу")),
                            ft.DataColumn(label=ft.Text("Удалить")),
                            ft.DataColumn(label=ft.Text("Редактировать"))
                        ],
                        rows=rows,
                    )
                ]),
                ft.Column([
                    ft.Button(content="Insert", on_click=lambda _: page.show_dialog(modal_page)),
                ])
            ])

        )


    menu_page()


ft.run(main)
