import csv
import os
from datetime import datetime

import flet as ft
from database import get_connection


def reports_page(page):

    page.clean()
    page.title = "FinancePro - Reports"

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
    total_borrow_given = get_total_amount("SELECT SUM(amount) FROM borrow_given")
    total_borrow_taken = get_total_amount("SELECT SUM(amount) FROM borrow_taken")
    due_borrow_given = get_total_amount("SELECT SUM(COALESCE(outstanding, amount)) FROM borrow_given WHERE payment_status != 'Paid'")
    due_borrow_taken = get_total_amount("SELECT SUM(amount) FROM borrow_taken WHERE payment_status != 'Paid'")
    net_balance = total_income - total_expenses

    def format_currency(value):
        return f"{value:,.2f} AED"

    export_message = ft.Text()

    def export_report(e):
        os.makedirs("exports", exist_ok=True)
        export_date = datetime.now()
        filename = f"exports/FinancePro_Report_{export_date.strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Report Name", "FinancePro Report"])
            writer.writerow(["Export Date", export_date.strftime('%Y-%m-%d %H:%M:%S')])
            writer.writerow([])
            writer.writerow(["Metric", "Value"])
            writer.writerow(["Total Income", format_currency(total_income)])
            writer.writerow(["Total Expenses", format_currency(total_expenses)])
            writer.writerow(["Total Investments", format_currency(total_investments)])
            writer.writerow(["Borrow Given", format_currency(total_borrow_given)])
            writer.writerow(["Borrow Taken", format_currency(total_borrow_taken)])
            writer.writerow(["Due Given", format_currency(due_borrow_given)])
            writer.writerow(["Due Taken", format_currency(due_borrow_taken)])
            writer.writerow(["Net Balance", format_currency(net_balance)])
        export_message.value = f"Report exported to {filename}"
        page.update()

    def go_back(e):
        from pages.dashboard import dashboard_page
        dashboard_page(page)

    page.add(
        ft.Text("📊 Reports", size=30, weight="bold"),
        ft.Divider(),
        ft.Row(
            [
                ft.Container(
                    content=ft.Column([
                        ft.Text("Income", size=16),
                        ft.Text(format_currency(total_income), size=22)
                    ]),
                    padding=10,
                    border_radius=10,
                    width=180,
                    height=120
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Expenses", size=16),
                        ft.Text(format_currency(total_expenses), size=22)
                    ]),
                    padding=10,
                    border_radius=10,
                    width=180,
                    height=120
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Investments", size=16),
                        ft.Text(format_currency(total_investments), size=22)
                    ]),
                    padding=10,
                    border_radius=10,
                    width=180,
                    height=120
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Borrow Given", size=16),
                        ft.Text(format_currency(total_borrow_given), size=22)
                    ]),
                    padding=10,
                    border_radius=10,
                    width=180,
                    height=120
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Borrow Taken", size=16),
                        ft.Text(format_currency(total_borrow_taken), size=22)
                    ]),
                    padding=10,
                    border_radius=10,
                    width=180,
                    height=120
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Due Given", size=16),
                        ft.Text(format_currency(due_borrow_given), size=22)
                    ]),
                    padding=10,
                    border_radius=10,
                    width=180,
                    height=120
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Due Taken", size=16),
                        ft.Text(format_currency(due_borrow_taken), size=22)
                    ]),
                    padding=10,
                    border_radius=10,
                    width=180,
                    height=120
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Net", size=16),
                        ft.Text(format_currency(net_balance), size=22)
                    ]),
                    padding=10,
                    border_radius=10,
                    width=180,
                    height=120
                )
            ],
            wrap=True
        ),
        ft.Divider(),
        ft.Row(
            [
                ft.ElevatedButton(
                    "Export Report",
                    icon=ft.Icons.FILE_DOWNLOAD,
                    on_click=export_report
                ),
                ft.ElevatedButton(
                    "Back",
                    icon=ft.Icons.ARROW_BACK,
                    on_click=go_back
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND
        ),
        export_message
    )
