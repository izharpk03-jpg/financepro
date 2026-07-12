import flet as ft
from datetime import date
from database import get_connection


def investment_page(page):

    page.clean()
    page.title = "FinancePro - Investment"

    name = ft.TextField(
        label="Investment Name",
        width=300
    )

    purchase_date = ft.TextField(
        label="Purchase Date",
        value=str(date.today()),
        width=300
    )

    amount = ft.TextField(
        label="Amount",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=300
    )

    current_value = ft.TextField(
        label="Current Value",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=300
    )

    message = ft.Text()

    def save_investment(e):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO investments
                (name, purchase_date, amount, current_value)
                VALUES (%s,%s,%s,%s)
                """,
                (
                    name.value,
                    purchase_date.value,
                    float(amount.value),
                    float(current_value.value)
                )
            )
            conn.commit()
            conn.close()
            message.value = "✅ Investment Added Successfully"
            name.value = ""
            amount.value = ""
            current_value.value = ""
        except Exception as ex:
            message.value = f"Error: {ex}"
        page.update()

    def delete_investment(e, record_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM investments WHERE id=?",
            (record_id,)
        )
        conn.commit()
        conn.close()
        message.value = "🗑️ Investment deleted"
        load_investments()
        page.update()

    def go_back(e):
        from pages.dashboard import dashboard_page
        dashboard_page(page)

    investment_list = ft.Column()

    def load_investments():
        investment_list.controls.clear()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, name, purchase_date, amount, current_value
            FROM investments
            ORDER BY id DESC
            """
        )
        records = cursor.fetchall()
        conn.close()
        for row in records:
            investment_list.controls.append(
                ft.Card(
                    content=ft.ListTile(
                        title=ft.Text(f"{row[1]} - {row[4]} AED"),
                        subtitle=ft.Text(f"Bought: {row[2]} | Cost: {row[3]} AED"),
                        trailing=ft.IconButton(
                            icon=ft.Icons.DELETE,
                            tooltip="Delete",
                            on_click=lambda e, record_id=row[0]: delete_investment(e, record_id)
                        )
                    )
                )
            )

    load_investments()

    page.add(
        ft.Text("📈 Add Investment", size=30, weight="bold"),
        name,
        purchase_date,
        amount,
        current_value,
        ft.Row(
            [
                ft.ElevatedButton(
                    "Save Investment",
                    icon=ft.Icons.SAVE,
                    on_click=save_investment
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
        ft.Text("Investment History", size=25, weight="bold"),
        investment_list
    )
