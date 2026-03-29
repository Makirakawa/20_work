import flet as ft
import psycopg2 as pg
database_connect = pg.connect()

def list_of_students(page:ft.Page, user):
    page.window.height = 900
    page.window.width = 1600
    page.window.resizable = False
    page.controls.clear()

    student_column = ft.Column()

    search_name_tf = ft.TextField(label="Имя")
    search_last_tf = ft.TextField(label="Фамилия")
    search_group_tf = ft.TextField(label="Группа")

    def load_students(first_name=None, last_name=None, group=None):
        conn = database_connect()
        if conn is None:
            return conn
        try:
            with conn.cursor() as cursor:
                query = """
                       SELECT first_name, last_name, middle_name, age, gender, group_id, phone
                       FROM students_test WHERE 1=1
                   """
                params = []
                if first_name:
                    query += " AND first_name ILIKE %s"
                    params.append(f"%{first_name}%")
                if last_name:
                    query += " AND last_name ILIKE %s"
                    params.append(f"%{last_name}%")
                if group:
                    query += " AND group_id ILIKE %s"
                    params.append(f"%{group}%")
                cursor.execute(query, params)
                return cursor.fetchall()
        except Exception as ex:
            print("load_students error:", ex)
        finally:
            conn.close()

    def render_students(students):
        student_column.controls.clear()
        for student in students:
            new_row = ft.Row(margin=ft.Margin(left=50),
                             controls=[
                                 ft.Text(student[0], width=170, size=20),
                                 ft.Text(student[1], width=170, size=20),
                                 ft.Text(student[2], width=270, size=20),
                                 ft.Text(str(student[5]), width=300, size=20),
                                 #ft.Button("Подробнее",on_click=lambda _, st=student: student_information(st, user))
                             ])
            student_column.controls.append(new_row)
        page.update()

    def apply_search(_):
        render_students(load_students(
            first_name=search_name_tf.value,
            last_name=search_last_tf.value,
            group=search_group_tf.value
        ))

    render_students(load_students())
    page.add(
        ft.Row([
            ft.Button("back", width=100, height=50, on_click=lambda _: main_window(user))
        ]),
        ft.Row([
            ft.Column([
                ft.Text("Список студентов", size=35),
                student_column
            ]),
            ft.Column(
                margin=ft.Margin(left=50),
                controls=[
                    ft.Text("Поиск:", size=30),
                    ft.Container(ft.Column([ft.Text("По имени", size=20), search_name_tf])),
                    ft.Container(ft.Column([ft.Text("По фамилии", size=20), search_last_tf])),
                    ft.Container(ft.Column([ft.Text("По группе", size=20), search_group_tf])),
                    ft.Row(
                        margin=ft.Margin(top=20),
                        controls=[
                            ft.Button("Применить", width=300, height=50,
                                      on_click=apply_search),
                        ]
                    )
                ]
            )
        ]),
    )
    page.update()