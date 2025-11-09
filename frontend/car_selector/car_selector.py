"""Car Selector - Modern Frontend"""
import reflex as rx
from .pages import index, quiz_page

app = rx.App(style={"font_family": "Inter, -apple-system, SF Pro Display, system-ui, sans-serif"})
app.add_page(index, route="/", title="Car Selector")
app.add_page(quiz_page, route="/quiz", title="Car Quiz")
