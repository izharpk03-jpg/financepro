import flet as ft
from datetime import date
from database import get_connection


def income_page(page):

    page.clean()

    page.title = "FinancePro - Income"


    # ---------------- INPUT FIELDS ----------------

    income_date = ft.TextField(
        label="Date",
        value=str(date.today()),
        width=300
    )


    amount = ft.TextField(
        label="Amount",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=300
    )


    source = ft.Dropdown(

        label="Source",
        width=300,

        options=[

            ft.dropdown.Option("Salary"),
            ft.dropdown.Option("Freelance"),
            ft.dropdown.Option("Business"),
            ft.dropdown.Option("Borrow Received"),
            ft.dropdown.Option("Other")

        ]
    )


    notes = ft.TextField(

        label="Notes",
        multiline=True,
        width=300

    )


    message = ft.Text()



    # ---------------- SAVE FUNCTION ----------------

    def apply_borrow_received(amount_value):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, amount, outstanding
            FROM borrow_given
            WHERE payment_status != 'Paid'
            ORDER BY id ASC
            """
        )
        records = cursor.fetchall()
        remaining = amount_value
        for row in records:
            if remaining <= 0:
                break
            record_id, original_amount, outstanding = row
            if outstanding is None:
                outstanding = original_amount
            if remaining >= outstanding:
                remaining -= outstanding
                cursor.execute(
                    "UPDATE borrow_given SET outstanding=0, payment_status='Paid' WHERE id=?",
                    (record_id,)
                )
            else:
                new_outstanding = outstanding - remaining
                remaining = 0
                cursor.execute(
                    "UPDATE borrow_given SET outstanding=? WHERE id=?",
                    (new_outstanding, record_id)
                )
        conn.commit()
        conn.close()

    def save_income(e):

        try:

            amount_value = float(amount.value)
            conn = get_connection()
            cursor = conn.cursor()


            cursor.execute(
                """
                INSERT INTO income
                (date, amount, source, notes)
                VALUES (?,?,?,?)
                """,

                (
                    income_date.value,
                    amount_value,
                    source.value,
                    notes.value
                )

            )

            conn.commit()
            conn.close()

            if source.value == "Borrow Received":
                apply_borrow_received(amount_value)
                message.value = "✅ Income added and borrow given adjusted"
            else:
                message.value = "✅ Income Added Successfully"


            amount.value = ""
            notes.value = ""


        except Exception as ex:

            message.value = f"Error: {ex}"


        page.update()


    def delete_income(e, record_id):

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM income WHERE id=?",
            (record_id,)
        )
        conn.commit()
        conn.close()

        message.value = "🗑️ Income deleted"
        load_income()
        page.update()


    def go_back(e):

        from pages.dashboard import dashboard_page
        dashboard_page(page)


    # ---------------- LOAD RECORDS ----------------


    income_list = ft.Column()



    def load_income():

        income_list.controls.clear()


        conn = get_connection()
        cursor = conn.cursor()


        cursor.execute(
            """
            SELECT id, date, amount, source, notes
            FROM income
            ORDER BY id DESC
            """
        )


        records = cursor.fetchall()

        conn.close()



        for row in records:

            income_list.controls.append(

                ft.Card(

                    content=ft.ListTile(

                        title=ft.Text(
                            f"{row[3]} - {row[2]} AED"
                        ),

                        subtitle=ft.Text(
                            f"{row[1]} | {row[4]}"
                        ),

                        trailing=ft.IconButton(
                            icon=ft.Icons.DELETE,
                            tooltip="Delete",
                            on_click=lambda e, record_id=row[0]: delete_income(e, record_id)
                        )

                    )

                )

            )



    load_income()



    # ---------------- PAGE DESIGN ----------------


    page.add(

        ft.Text(
            "➕ Add Income",
            size=30,
            weight="bold"
        ),


        income_date,
        amount,
        source,
        notes,


        ft.Row(
            [
                ft.ElevatedButton(

                    "Save Income",
                    icon=ft.Icons.SAVE,
                    on_click=save_income

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


        ft.Text(
            "Income History",
            size=25,
            weight="bold"
        ),


        income_list

    )