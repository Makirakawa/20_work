import flet as ft
from gui import *



def main (page:ft.Page):
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
    def auction_result_page():
        page.clean()
        page.update()
        page.window.wight = 1600
        page.window.height = 900
        page.title = "Страница результатов аукционов"
        connect_to_auction_results_table()

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

        def insert_into_results_table():
            conn = database_connect()
            if conn is None:
                return
            try:
                pass
            except Exception as e:
                print("[PAGE: actions_result] [FUNCTION: insert_into_results_table] error: ", e)
            finally:
                conn.close()
                page.update()

        def delete_into_results_table(result_id):
            conn = database_connect()
            if conn is None:
                return
            try:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM results WHERE id = %s", (result_id))
                    conn.commit()
            except Exception as e:
                print("[PAGE: actions_result] [FUNCTION: delete_into_results_table] error: ", e)
            finally:
                conn.close()
                page.update()

        def edit_into_results_table(farm_id, fur_name, grade, sold_quantity, sale_price, buyer_category):
            conn = database_connect()
            if conn is None:
                return
            try:
                with conn.cursor() as cursor:
                    cursor.execute("", )
                    conn.commit()
            except Exception as e:
                print("[PAGE: actions_result] [FUNCTION: edit_into_results_table] error: ", e)
            finally:
                conn.close()
                page.update()

        def edit_modal_page(res, lot, farm):
            farm_rows = connect_to_farms_table()
            lots_rows = connect_to_lots_table()

            fur_name = ft.TextField(label="Название меха", value=str(res[3]))
            grade = ft.TextField(label="Сорт", value=str(res[4]))
            sold_quantity = ft.TextField(label="Количество проданных единиц", value=str(res[5]))
            sale_price = ft.TextField(label="Продажная цена за единицу", value=str(res[6]))
            buyer_category = ft.TextField(label="Категория покупателя", value=str(res[7]))

            farm_dropdown = ft.Dropdown(
                label="Номер зверофермы",
                value=str(farm[1]) if farm[1] is not None else None,
                options=[
                    ft.dropdown.Option(key=str(farm[0]), text=f"f{farm[0]} - {farm[1]}")
                    for farm in farm_rows
                ] if farm_rows else [],
            )
            lots_dropdown = ft.Dropdown(
                label="Номер лота",
                value=str(lot[1]) if lot[1] is not None else None,
                options=[
                    ft.dropdown.Option(key=str(lot[0]), text=f"f{lot[0]} - {lot[1]}")
                    for lot in lots_rows
                ] if lots_rows else [],
            )
            modal_dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Редактировать запись"),
                content=ft.Column([
                    lots_dropdown,
                    farm_dropdown,
                    fur_name,
                    grade,
                    grade,
                    sold_quantity,
                    sale_price,
                    buyer_category
                ]),
                actions=[
                    ft.TextButton("Сохранить", on_click=lambda e: edit_into_results_table(res[0], lots_dropdown.value,
                                                                                          farm_dropdown.value, )),
                    ft.TextButton("Отмена", on_click=lambda e: page.pop_dialog())
                ]
            )
            page.show_dialog(modal_dialog)
            page.update()

        rests = connect_to_auction_results_table()

        rows = []
        if rests:
            for res in rests:
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
                            ft.IconButton(icon=ft.Icons.EDIT, icon_color="green",
                                          on_click=lambda e, res=res: edit_modal_page(res))),
                        ft.DataCell(
                            ft.IconButton(icon=ft.Icons.DELETE, icon_color="red",
                                          on_click=lambda e, id=res[0]: delete_into_results_table(id))
                        )

                    ])
                )
        page.add(
            ft.Row([
                ft.Text("Результаты аукциона", size=20)
            ]),
            ft.Row([
                ft.Column([
                    ft.DataTable(
                        columns=[
                            ft.DataColumn(label=ft.Text("Номер аукциона", width=70)),
                            ft.DataColumn(label=ft.Text("Ссылка на лот", width=70)),
                            ft.DataColumn(label=ft.Text("Номер зверовермы", width=85)),
                            ft.DataColumn(label=ft.Text("Название меха", width=70)),
                            ft.DataColumn(label=ft.Text("Сорт", width=40)),
                            ft.DataColumn(label=ft.Text("Количество проданных единиц", width=90)),
                            ft.DataColumn(label=ft.Text("Цена за единицу", width=70)),
                            ft.DataColumn(label=ft.Text("категория покупателя", width=80)),
                            ft.DataColumn(label=ft.Text("Изменить", width=70)),
                            ft.DataColumn(label=ft.Text("Удалить", width=65)),
                        ],
                    rows=rows,
                    )
                ]),

            ]),
            ft.Row([
                ft.Column([
                    ft.Button(content="Insert", on_click=lambda _: page.show_dialog(...)),
                ])
            ])
        )