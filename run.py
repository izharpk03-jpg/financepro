import os, sys

# Make FinancePro folder importable from repository root
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
FINANCE_DIR = os.path.join(ROOT_DIR, 'FinancePro')
sys.path.insert(0, FINANCE_DIR)

from main import main
import flet as ft

ft.app(
    target=main,
    view=ft.AppView.WEB_BROWSER,
    host='0.0.0.0',
    port=int(os.environ.get('PORT', '10000')),
)
