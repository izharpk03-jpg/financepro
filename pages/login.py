import flet as ft
import sqlite3


def check_login(username, password):

    conn = sqlite3.connect("database/finance.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cursor.fetchone()

    conn.close()

    return user



def login_page(page):

    page.clean()

    username = ft.TextField(
        label="Username",
        width=300,
        prefix_icon=ft.Icons.PERSON
    )

    password = ft.TextField(
        label="Password",
        password=True,
        width=300,
        prefix_icon=ft.Icons.LOCK
    )

    message = ft.Text(
        color="red"
    )


    def login_click(e):

        user = check_login(
            username.value,
            password.value
        )

        if user:

            message.value = "Login Successful"

            page.update()

            from pages.dashboard import dashboard_page
            dashboard_page(page)

        else:

            message.value = "Invalid Username or Password"
            page.update()


    login_button = ft.ElevatedButton(
        "Login",
        width=300,
        on_click=login_click
    )


    page.add(

        ft.Column(

            [
                ft.Icon(
                    ft.Icons.ACCOUNT_BALANCE_WALLET,
                    size=90
                ),

                ft.Text(
                    "FinancePro",
                    size=32,
                    weight=ft.FontWeight.BOLD
                ),

                username,

                password,

                login_button,

                message

            ],

            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

            alignment=ft.MainAxisAlignment.CENTER

        )

    )