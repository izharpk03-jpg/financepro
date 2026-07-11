import flet as ft
from database import get_connection


def settings_page(page):

    page.clean()
    page.title = "FinancePro - Settings"

    def go_back(e):
        from pages.dashboard import dashboard_page
        dashboard_page(page)

    page.add(
        ft.Text("⚙️ Settings", size=30, weight="bold"),
        ft.Text("User settings and app preferences can be configured here."),
        ft.Divider(),
        ft.Text("Coming soon: password update, theme settings, notifications."),
        ft.Divider(),
        ft.ElevatedButton(
            "Back",
            icon=ft.Icons.ARROW_BACK,
            on_click=go_back
        )
    )
