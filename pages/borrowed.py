import flet as ft
from datetime import date
from database import get_connection


def borrowed_page(page):

    page.clean()
    page.title = "FinancePro - Borrowed Amount"

    name = ft.TextField(
        label="Lender / Borrower Name",
        width=300
    )

    date_field = ft.TextField(
        label="Date",
        value=str(date.today()),
        width=300
    )

    amount = ft.TextField(
        label="Amount",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=300
    )

    due_date = ft.TextField(
        label="Due Date",
        width=300
    )

    notes = ft.TextField(
        label="Notes",
        multiline=True,
        width=300
    )

    message = ft.Text()

    def save_borrowed(e):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO borrowed
                (name, date, amount, due_date, notes)
                VALUES (?,?,?,?,?)
                """,
                (
                    name.value,
                    date_field.value,
                    float(amount.value),
                    due_date.value,
                    notes.value
                )
            )
            conn.commit()
            conn.close()
            message.value = "✅ Borrowed amount saved"
            name.value = ""
            amount.value = ""
            due_date.value = str(date.today())
            notes.value = ""
        except Exception as ex:
            message.value = f"Error: {ex}"
        page.update()

    def delete_borrowed(e, record_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM borrowed WHERE id=?",
            (record_id,)
        )
        conn.commit()
        conn.close()
        message.value = "🗑️ Borrowed entry deleted"
        load_borrowed()
        page.update()

    def go_back(e):
        from pages.dashboard import dashboard_page
        dashboard_page(page)

    borrowed_list = ft.Column()

    def load_borrowed():
        borrowed_list.controls.clear()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, name, date, amount, due_date, notes
            FROM borrowed
            ORDER BY id DESC
            """
        )
        records = cursor.fetchall()
        conn.close()
        for row in records:
            borrowed_list.controls.append(
                ft.Card(
                    content=ft.ListTile(
                        title=ft.Text(f"{row[1]} - {row[3]} AED"),
                        subtitle=ft.Text(f"{row[2]} | Due: {row[4]} | {row[5]}"),
                        trailing=ft.IconButton(
                            icon=ft.Icons.DELETE,
                            tooltip="Delete",
                            on_click=lambda e, record_id=row[0]: delete_borrowed(e, record_id)
                        )
                    )
                )
            )

    load_borrowed()

    page.add(
        ft.Text("💸 Borrowed Amount", size=30, weight="bold"),
        name,
        date_field,
        amount,
        due_date,
        notes,
        ft.Row(
            [
                ft.ElevatedButton(
                    "Save Borrowed",
                    icon=ft.Icons.SAVE,
                    on_click=save_borrowed
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
        ft.Text("Borrowed History", size=25, weight="bold"),
        borrowed_list
    )
