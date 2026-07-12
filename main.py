import os
import flet as ft

from database import create_tables
from pages.login import login_page


def main(page: ft.Page):
    create_tables()

    page.title = "FinancePro"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    login_page(page)


ft.app(
    target=main,
    view=ft.AppView.WEB_BROWSER,
    host="0.0.0.0",
    port=int(os.environ.get("PORT", "10000")),
)