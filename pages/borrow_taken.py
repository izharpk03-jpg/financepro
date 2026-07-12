import flet as ft
from datetime import date
from database import get_connection


def borrow_taken_page(page):
    page.clean()
    page.title = "FinancePro - Borrow Taken"

    name = ft.TextField(label="Lender Name", width=300)
    date_field = ft.TextField(label="Date", value=str(date.today()), width=300)
    amount = ft.TextField(label="Amount", keyboard_type=ft.KeyboardType.NUMBER, width=300)
    due_date = ft.TextField(label="Due Date", width=300)
    payment_status = ft.Dropdown(
        label="Payment Status",
        width=300,
        value="Pending",
        options=[
            ft.dropdown.Option("Pending"),
            ft.dropdown.Option("Paid")
        ]
    )
    notes = ft.TextField(label="Notes", multiline=True, width=300)
    message = ft.Text()

    def save_taken(e):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO borrow_taken
                (name, date, amount, due_date, payment_status, notes)
                VALUES (?,?,?,?,?,?)
                """,
                (
                    name.value,
                    date_field.value,
                    float(amount.value),
                    due_date.value,
                    payment_status.value,
                    notes.value
                )
            )
            conn.commit()
            conn.close()
            message.value = "✅ Borrow Taken saved"
            name.value = ""
            amount.value = ""
            due_date.value = ""
            payment_status.value = "Pending"
            notes.value = ""
            load_taken()
        except Exception as ex:
            message.value = f"Error: {ex}"
        page.update()

    def delete_taken(e, record_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM borrow_taken WHERE id=?", (record_id,))
        conn.commit()
        conn.close()
        message.value = "🗑️ Borrow Taken entry deleted"
        load_taken()
        page.update()

    def go_back(e):
        from pages.dashboard import dashboard_page
        dashboard_page(page)

    taken_list = ft.Column()

    def load_taken():
        taken_list.controls.clear()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, name, date, amount, due_date, payment_status, notes
            FROM borrow_taken
            ORDER BY id DESC
            """
        )
        records = cursor.fetchall()
        conn.close()
        for row in records:
            taken_list.controls.append(
                ft.Card(
                    content=ft.ListTile(
                        title=ft.Text(f"{row[1]} - {row[3]:,.2f} AED"),
                        subtitle=ft.Text(f"Date: {row[2]} | Due: {row[4]} | Status: {row[5]}"),
                        trailing=ft.IconButton(
                            icon=ft.Icons.DELETE,
                            tooltip="Delete",
                            on_click=lambda e, record_id=row[0]: delete_taken(e, record_id)
                        )
                    )
                )
            )

    load_taken()

    page.add(
        ft.Text("Borrow Taken", size=32, weight="bold"),
        ft.Text("Track amounts you have borrowed from others.", size=16, color="#666"),
        ft.Divider(),
        name,
        date_field,
        amount,
        due_date,
        payment_status,
        notes,
        ft.Row(
            [
                ft.ElevatedButton("Save", icon=ft.Icons.SAVE, on_click=save_taken),
                ft.ElevatedButton("Back", icon=ft.Icons.ARROW_BACK, on_click=go_back)
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND
        ),
        message,
        ft.Divider(),
        ft.Text("Borrow Taken History", size=24, weight="bold"),
        taken_list
    )
