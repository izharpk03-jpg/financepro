import flet as ft
from database import get_connection
from pages.expense import expense_page
from pages.income import income_page
from pages.investment import investment_page
from pages.reports import reports_page
from pages.borrow_given import borrow_given_page
from pages.borrow_taken import borrow_taken_page
from pages.settings import settings_page


def dashboard_page(page):

    page.clean()

    page.title = "FinancePro Dashboard"


    # -------- OPEN INCOME PAGE --------

    def open_income(e):
        income_page(page)


    def open_expense(e):
        expense_page(page)


    def open_investment(e):
        investment_page(page)


    def open_reports(e):
        reports_page(page)


    def open_borrow_given(e):
        borrow_given_page(page)


    def open_borrow_taken(e):
        borrow_taken_page(page)


    def open_settings(e):
        settings_page(page)


    # -------- CARD DESIGN --------

    def card(title, value, on_click=None):

        return ft.Container(

            content=ft.Column(
                [
                    ft.Text(
                        "💰",
                        size=30
                    ),

                    ft.Text(
                        title,
                        size=16
                    ),

                    ft.Text(
                        value,
                        size=22
                    )
                ],

                spacing=5

            ),

            width=180,
            height=120,

            padding=10,

            border_radius=10,
            on_click=on_click,
            tooltip="View details",
            ink=True

        )


    def format_currency(value):

        return f"{value:,.2f} AED"


    def get_total_amount(query):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(query)
        result = cursor.fetchone()[0]

        conn.close()

        return result or 0


    total_income = get_total_amount("SELECT SUM(amount) FROM income")
    total_expenses = get_total_amount("SELECT SUM(amount) FROM expenses")
    total_investments = get_total_amount("SELECT SUM(current_value) FROM investments")
    total_given = get_total_amount("SELECT SUM(amount) FROM borrow_given")
    total_taken = get_total_amount("SELECT SUM(amount) FROM borrow_taken")
    due_given = get_total_amount("SELECT SUM(COALESCE(outstanding, amount)) FROM borrow_given WHERE payment_status != 'Paid'")
    due_taken = get_total_amount("SELECT SUM(amount) FROM borrow_taken WHERE payment_status != 'Paid'")
    total_balance = total_income - total_expenses


    # -------- TITLE --------

    title = ft.Text(
        "FinancePro Dashboard",
        size=30
    )


    # -------- SUMMARY --------

    summary = ft.Row(

        [
            card(
                "Total Balance",
                format_currency(total_balance)
            ),

            card(
                "Income",
                format_currency(total_income),
                on_click=open_income
            ),

            card(
                "Expenses",
                format_currency(total_expenses),
                on_click=open_expense
            ),

            card(
                "Investments",
                format_currency(total_investments),
                on_click=open_investment
            ),

            card(
                "Borrow Given",
                format_currency(total_given),
                on_click=open_borrow_given
            ),

            card(
                "Borrow Taken",
                format_currency(total_taken),
                on_click=open_borrow_taken
            ),

            card(
                "Due Given",
                format_currency(due_given),
                on_click=open_borrow_given
            ),

            card(
                "Due Taken",
                format_currency(due_taken),
                on_click=open_borrow_taken
            )

        ],

        wrap=True

    )


    # -------- BUTTONS --------

    buttons = ft.Row(

        [

            ft.ElevatedButton(

                "Add Income",

                icon=ft.Icons.ADD,

                bgcolor=ft.Colors.LIGHT_GREEN_200,

                on_click=open_income

            ),


            ft.ElevatedButton(

                "Add Expense",

                icon=ft.Icons.REMOVE,
                bgcolor=ft.Colors.LIGHT_GREEN_200,
                on_click=open_expense

            ),


            ft.ElevatedButton(

                "Investment",

                icon=ft.Icons.ACCOUNT_BALANCE,
                bgcolor=ft.Colors.LIGHT_GREEN_200,
                on_click=open_investment

            ),


            ft.ElevatedButton(

                "Reports",

                icon=ft.Icons.BAR_CHART,
                bgcolor=ft.Colors.LIGHT_GREEN_200,
                on_click=open_reports

            ),


            ft.ElevatedButton(

                "Borrow Given",

                icon=ft.Icons.ATTACH_MONEY,
                bgcolor=ft.Colors.LIGHT_GREEN_200,
                on_click=open_borrow_given

            ),


            ft.ElevatedButton(

                "Borrow Taken",

                icon=ft.Icons.PAYMENT,
                bgcolor=ft.Colors.LIGHT_GREEN_200,
                on_click=open_borrow_taken

            ),


            ft.ElevatedButton(

                "Settings",

                icon=ft.Icons.SETTINGS,
                bgcolor=ft.Colors.LIGHT_GREEN_200,
                on_click=open_settings

            )

        ],

        wrap=True

    )


    # -------- PAGE --------

    page.add(

        ft.Column(

            [

                title,


                ft.Divider(),


                summary,


                ft.Divider(),


                ft.Text(

                    "Quick Actions",

                    size=20

                ),


                buttons

            ]

        )

    )