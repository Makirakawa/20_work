import flet as ft


def edit_modal_page(lot):
    farm_rows = connect_to_farms_table()

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