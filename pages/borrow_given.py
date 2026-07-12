import flet as ft
from datetime import date
from database import get_connection


def borrow_given_page(page):
    page.clean()
    page.title = "FinancePro - Borrow Given"

    name = ft.TextField(label="Borrower Name", width=300)
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

    def save_given(e):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO borrow_given
                (name, date, amount, outstanding, due_date, payment_status, notes)
                VALUES (?,?,?,?,?,?,?)
                """,
                (
                    name.value,
                    date_field.value,
                    float(amount.value),
                    float(amount.value),
                    due_date.value,
                    payment_status.value,
                    notes.value
                )
            )
            conn.commit()
            conn.close()
            message.value = "✅ Borrow Given saved"
            name.value = ""
            amount.value = ""
            due_date.value = ""
            payment_status.value = "Pending"
            notes.value = ""
            load_given()
        except Exception as ex:
            message.value = f"Error: {ex}"
        page.update()

    def delete_given(e, record_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM borrow_given WHERE id=?", (record_id,))
        conn.commit()
        conn.close()
        message.value = "🗑️ Borrow Given entry deleted"
        load_given()
        page.update()

    def go_back(e):
        from pages.dashboard import dashboard_page
        dashboard_page(page)

    given_list = ft.Column()

    def load_given():
        given_list.controls.clear()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, name, date, amount, outstanding, due_date, payment_status, notes
            FROM borrow_given
            ORDER BY id DESC
            """
        )
        records = cursor.fetchall()
        conn.close()
        for row in records:
            outstanding_value = row[4] if row[4] is not None else row[3]
            given_list.controls.append(
                ft.Card(
                    content=ft.ListTile(
                        title=ft.Text(f"{row[1]} - {row[3]:,.2f} AED"),
                        subtitle=ft.Text(f"Outstanding: {outstanding_value:,.2f} AED | Date: {row[2]} | Due: {row[5]} | Status: {row[6]} "),
                        trailing=ft.IconButton(
                            icon=ft.Icons.DELETE,
                            tooltip="Delete",
                            on_click=lambda e, record_id=row[0]: delete_given(e, record_id)
                        )
                    )
                )
            )

    load_given()

    page.add(
        ft.Text("Borrow Given", size=32, weight="bold"),
        ft.Text("Track amounts you have lent to others.", size=16, color="#666"),
        ft.Divider(),
        name,
        date_field,
        amount,
        due_date,
        payment_status,
        notes,
        ft.Row(
            [
                ft.ElevatedButton("Save", icon=ft.Icons.SAVE, on_click=save_given),
                ft.ElevatedButton("Back", icon=ft.Icons.ARROW_BACK, on_click=go_back)
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND
        ),
        message,
        ft.Divider(),
        ft.Text("Borrow Given History", size=24, weight="bold"),
        given_list
    )
