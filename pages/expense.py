import flet as ft
from datetime import date
from database import get_connection


def expense_page(page):

    page.clean()
    page.title = "FinancePro - Expense"

    expense_date = ft.TextField(
        label="Date",
        value=str(date.today()),
        width=300
    )

    category = ft.Dropdown(
        label="Category",
        width=300,
        options=[
            ft.dropdown.Option("Food"),
            ft.dropdown.Option("Bills"),
            ft.dropdown.Option("Transport"),
            ft.dropdown.Option("Shopping"),
            ft.dropdown.Option("Other")
        ]
    )

    amount = ft.TextField(
        label="Amount",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=300
    )

    payment_method = ft.Dropdown(
        label="Payment Method",
        width=300,
        options=[
            ft.dropdown.Option("Cash"),
            ft.dropdown.Option("Card"),
            ft.dropdown.Option("Mobile Wallet")
        ]
    )

    notes = ft.TextField(
        label="Notes",
        multiline=True,
        width=300
    )

    message = ft.Text()

    def save_expense(e):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO expenses
                (date, category, amount, payment_method, notes)
                VALUES (%s,%s,%s,%s)
                """,
                (
                    expense_date.value,
                    category.value,
                    float(amount.value),
                    payment_method.value,
                    notes.value
                )
            )
            conn.commit()
            conn.close()
            message.value = "✅ Expense Added Successfully"
            amount.value = ""
            notes.value = ""
        except Exception as ex:
            message.value = f"Error: {ex}"
        page.update()

    def delete_expense(e, record_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM expenses WHERE id=?",
            (record_id,)
        )
        conn.commit()
        conn.close()
        message.value = "🗑️ Expense deleted"
        load_expenses()
        page.update()

    def go_back(e):
        from pages.dashboard import dashboard_page
        dashboard_page(page)

    expense_list = ft.Column()

    def load_expenses():
        expense_list.controls.clear()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, date, category, amount, payment_method, notes
            FROM expenses
            ORDER BY id DESC
            """
        )
        records = cursor.fetchall()
        conn.close()
        for row in records:
            expense_list.controls.append(
                ft.Card(
                    content=ft.ListTile(
                        title=ft.Text(f"{row[2]} - {row[3]} AED"),
                        subtitle=ft.Text(f"{row[1]} | {row[4]} | {row[5]}"),
                        trailing=ft.IconButton(
                            icon=ft.Icons.DELETE,
                            tooltip="Delete",
                            on_click=lambda e, record_id=row[0]: delete_expense(e, record_id)
                        )
                    )
                )
            )

    load_expenses()

    page.add(
        ft.Text("➖ Add Expense", size=30, weight="bold"),
        expense_date,
        category,
        amount,
        payment_method,
        notes,
        ft.Row(
            [
                ft.ElevatedButton(
                    "Save Expense",
                    icon=ft.Icons.SAVE,
                    on_click=save_expense
                ),
                ft.ElevatedButton(
                    "Back",
                    icon=ft.Icons.ARROW_BACK,
                    on_click=go_back
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND
        ),
        message,
        ft.Divider(),
        ft.Text("Expense History", size=25, weight="bold"),
        expense_list
    )
