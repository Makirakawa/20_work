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

    # general sql functions, for all pages

    # _____________________________farms________________________________________

    def connect_to_farms_table():  # ______________connect_to_farms_table______________
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

        # _____________________________lots________________________________________

    def connect_to_lots_table():  # ______________connect_to_farms_table______________
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



        # _____________________________auction_results________________________________________

    def connect_to_auction_results_table():  # ______________connect_to_auction_results_table______________
        conn = database_connect()
        if conn is None:
            return conn
        try:
            with conn.cursor() as cursor:
                cursor.execute('''SELECT * FROM auction_results;''')
                return cursor.fetchall()

        except Exception as _ex:
            print("Error connecting to farms table", _ex)
        finally:
            if conn:
                conn.close()

    def menu_page():
        page.clean()
        page.window.height = 900
        page.window.width = 1600
        page.add(
            ft.Column([
                ft.Button("Фермы", on_click=lambda _: farms_record_page()),
                ft.Button("Пушнина на аукционе", on_click=lambda _: lots_record_page()),
                ft.Button("Результаты аукциона", on_click=lambda _: auction_result_page()),
            ])
        )

    def farms_record_page():
        page.title = "Страница фермы"
        page.clean()
        page.update()
        page.window.height = 900
        page.window.wight = 1600
        connect_to_farms_table()

        def insert_to_farm_table():
            conn = database_connect()
            if conn is None:
                return conn
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO farm_table(addres, director, phone) VALUES (%s, %s, %s)",
                        (adress_textfield.value, director_textfield.value, phone_textfield.value)
                    )
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
                    cursor.execute(f"DELETE FROM farm_table WHERE farm_id = %s", (farm_id,))
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
                                   (addres, director, phone, farm_id))
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
                            ft.IconButton(icon=ft.Icons.DELETE, icon_color="red",
                                          on_click=lambda e, id=farm[0]: delete_on_farm_table(id))
                        ),
                        ft.DataCell(
                            ft.IconButton(icon=ft.Icons.EDIT, icon_color="green",
                                          on_click=lambda e, farm=farm: edit_modal_page(farm)
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
        # ________________________________________________________________________________________________________________lots_record_page

    def lots_record_page():
        page.title = "Страница лотов"
        page.clean()
        page.update()
        page.window.height = 900
        page.window.width = 1600
        connect_to_lots_table()

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

        def insert_to_lots_table():
            try:
                quantity_val = int(quantity.value)
                price_val = int(declared_price.value)
            except ValueError:
                page.show_snack_bar(
                    ft.SnackBar(ft.Text("Ошибка: количество и цена должны быть целыми числами!"), open=True))
                return

            conn = database_connect()
            if conn is None:
                return
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO lots(fur_name, quantity, declared_price) VALUES(%s, %s, %s)",
                        (fur_name.value, quantity_val, price_val)
                    )
                    conn.commit()
            except Exception as _ex:
                print("Error inserting into lots table", _ex)
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

        def edit_on_lots_table(lot_id, farm_id, fur_name, quantity, declared_price):
            try:
                farm_id = int(farm_id) if farm_id else None
                quantity = int(quantity)
                declared_price = int(declared_price)
            except ValueError:
                page.show_snack_bar(
                    ft.SnackBar(ft.Text("Ошибка: количество и цена должны быть целыми числами!"), open=True))
                return

            conn = database_connect()
            if conn is None:
                return
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "UPDATE lots SET farm_id=%s, fur_name=%s, quantity=%s, declared_price=%s WHERE lot_id=%s",
                        (farm_id, fur_name, quantity, declared_price, lot_id)
                    )
                    conn.commit()
            except Exception as _ex:
                print("Ошибка обновления:", _ex)
            finally:
                page.pop_dialog()
                page.clean()
                lots_record_page()
                if conn:
                    conn.close()

        def edit_modal_page(lot):
            farm_rows = connect_to_farms_table()
            print("Фермы:", farm_rows)  # проверим что возвращается

            dropdown = ft.Dropdown(
                label="Номер зверофермы",
                value=str(lot[1]) if lot[1] is not None else None,
                options=[
                    ft.dropdown.Option(key=str(r[0]), text=f"{r[0]} - {r[1]}")
                    for r in farm_rows
                ] if farm_rows else [],
            )
            fur_name = ft.TextField(label="Название меха", value=str(lot[2]))
            quantity = ft.TextField(label="Количество", value=str(lot[3]))
            declared_price = ft.TextField(label="Заявленная цена за единицу", value=str(lot[4]))

            modal_dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Редактировать запись"),
                content=ft.Column([
                    dropdown,
                    fur_name,
                    quantity,
                    declared_price
                ]),
                actions=[
                    ft.TextButton("Сохранить", on_click=lambda e: edit_on_lots_table(
                        lot[0], dropdown.value, fur_name.value, quantity.value, declared_price.value
                    )),
                    ft.TextButton("Отмена", on_click=lambda e: page.pop_dialog())
                ]
            )
            page.show_dialog(modal_dialog)
            page.update()

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
        # _________________________________________________________________________auction_result_page

    def auction_result_page():
        page.clean()
        page.window.width = 1600
        page.window.height = 900
        page.title = "Результаты аукциона"

        # ---------------- DB ----------------

        def get_farms():
            conn = database_connect()
            try:
                with conn.cursor() as cur:
                    cur.execute("SELECT farm_id, addres FROM farm_table")
                    return cur.fetchall()
            finally:
                conn.close()

        def get_lots():
            conn = database_connect()
            try:
                with conn.cursor() as cur:
                    cur.execute("SELECT lot_id, fur_name FROM lots")
                    return cur.fetchall()
            finally:
                conn.close()

        def get_results():
            conn = database_connect()
            try:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM auction_results ORDER BY result_id")
                    return cur.fetchall()
            finally:
                conn.close()

        # ---------------- DELETE ----------------

        def delete_result(result_id):
            conn = database_connect()
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        "DELETE FROM auction_results WHERE result_id = %s",
                        (result_id,)
                    )
                    conn.commit()
            finally:
                conn.close()

            page.clean()
            auction_result_page()

        # ---------------- INSERT ----------------

        def insert_modal():
            print("MODAL OPEN")
            farms = get_farms()
            lots = get_lots()

            farm_dd = ft.Dropdown(
                label="Ферма",
                options=[ft.dropdown.Option(str(f[0]), f"{f[0]} - {f[1]}") for f in farms]
            )

            lot_dd = ft.Dropdown(
                label="Лот",
                options=[ft.dropdown.Option(str(l[0]), f"{l[0]} - {l[1]}") for l in lots]
            )

            fur_name = ft.TextField(label="Мех")
            grade = ft.TextField(label="Сорт")
            sold_quantity = ft.TextField(label="Количество")
            sale_price = ft.TextField(label="Цена")

            buyer_category = ft.Dropdown(
                label="Категория",
                options=[
                    ft.dropdown.Option("меховая фабрика"),
                    ft.dropdown.Option("ателье"),
                    ft.dropdown.Option("частное лицо"),
                ]
            )

            def save(e):
                try:
                    qty = int(sold_quantity.value)
                    price = float(sale_price.value)
                except:
                    page.snack_bar = ft.SnackBar(ft.Text("Ошибка ввода чисел"))
                    page.snack_bar.open = True
                    page.update()
                    return

                conn = database_connect()
                try:
                    with conn.cursor() as cur:
                        cur.execute("""
                            INSERT INTO auction_results
                            (lot_id, farm_id, fur_name, grade, sold_quantity, sale_price, buyer_category)
                            VALUES (%s,%s,%s,%s,%s,%s,%s)
                        """, (
                            int(lot_dd.value),
                            int(farm_dd.value),
                            fur_name.value,
                            grade.value,
                            qty,
                            price,
                            buyer_category.value
                        ))
                        conn.commit()
                finally:
                    conn.close()

                dlg.open = False
                page.update()
                auction_result_page()

            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Добавить результат"),
                content=ft.Column([
                    lot_dd,
                    farm_dd,
                    fur_name,
                    grade,
                    sold_quantity,
                    sale_price,
                    buyer_category
                ]),
                actions=[
                    ft.TextButton("Сохранить", on_click=save),
                    ft.TextButton("Отмена", on_click=lambda e: close_dialog(dlg))
                ]
            )

            page.dialog = dlg
            dlg.open = True
            page.update()

        def edit_modal(res):
            print("EDIT CLICKED:", res)

            farms = connect_to_farms_table()
            lots = connect_to_lots_table()

            farm_dd = ft.Dropdown(
                label="Ферма",
                value=str(res[2]),
                options=[ft.dropdown.Option(str(f[0]), f"{f[0]} - {f[1]}") for f in farms]
            )

            lot_dd = ft.Dropdown(
                label="Лот",
                value=str(res[1]),
                options=[ft.dropdown.Option(str(l[0]), f"{l[0]} - {l[1]}") for l in lots]
            )

            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Редактирование"),
                content=ft.Column([
                    lot_dd,
                    farm_dd,
                    ft.TextField(label="Мех", value=res[3]),
                    ft.TextField(label="Сорт", value=res[4]),
                    ft.TextField(label="Количество", value=str(res[5])),
                    ft.TextField(label="Цена", value=str(res[6])),
                ]),
            )

            page.dialog = dlg
            dlg.open = True
            page.update()

        def close_dialog(dlg):
            dlg.open = False
            page.update()

        # ---------------- TABLE ----------------

        results = get_results()

        rows = []
        for res in results:
            rows.append(
                ft.DataRow([
                    ft.DataCell(ft.Text(str(res[0]))),
                    ft.DataCell(ft.Text(str(res[1]))),
                    ft.DataCell(ft.Text(str(res[2]))),
                    ft.DataCell(ft.Text(str(res[3]))),
                    ft.DataCell(ft.Text(str(res[4]))),
                    ft.DataCell(ft.Text(str(res[5]))),
                    ft.DataCell(ft.Text(str(res[6]))),
                    ft.DataCell(ft.Text(str(res[7]))),

                    ft.DataCell(
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            icon_color="green",
                            on_click=lambda e, r=res: edit_modal(r)
                        )
                    ),
                    ft.DataCell(
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            icon_color="red",
                            on_click=lambda e, rid=res[0]: delete_result(rid)
                        )
                    )
                ])
            )

        # ---------------- UI ----------------

        page.add(
            ft.Row([
                ft.Button("Назад", on_click=lambda e: menu_page())
            ]),

            ft.Text("Результаты аукциона", size=22),

            ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("ID")),
                    ft.DataColumn(ft.Text("Лот")),
                    ft.DataColumn(ft.Text("Ферма")),
                    ft.DataColumn(ft.Text("Мех")),
                    ft.DataColumn(ft.Text("Сорт")),
                    ft.DataColumn(ft.Text("Кол-во")),
                    ft.DataColumn(ft.Text("Цена")),
                    ft.DataColumn(ft.Text("Категория")),
                    ft.DataColumn(ft.Text("Изменить")),
                    ft.DataColumn(ft.Text("Удалить")),
                ],
                rows=rows
            ),

            ft.Button("Insert", on_click= insert_modal)
        )
    menu_page()


ft.run(main)
