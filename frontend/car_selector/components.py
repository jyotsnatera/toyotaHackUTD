"""Reusable component functions for the Car Selector application."""
import reflex as rx
from .constants import COLORS, STYLES
from .state import State


def create_option_card(text: str, state_var, toggle_func, subtitle: str = None, disabled_cond=None, min_height="48px") -> rx.Component:
    """Create a reusable option card component."""
    content = rx.hstack(
        rx.text(text, font_size="16px", color=COLORS["black"], font_weight="500"),
        rx.cond(state_var, rx.text("✓", font_size="18px", color=COLORS["red_light"], font_weight="bold")),
        spacing="3",
        align_items="center",
        width="100%",
        justify_content="space-between",
    )
    if subtitle:
        content = rx.vstack(
            content,
            rx.text(subtitle, font_size="14px", color=COLORS["gray"], margin_top="4"),
            spacing="0",
            align_items="flex-start",
            width="100%",
        )
    props = {
        **STYLES["option_card"],
        "on_click": toggle_func,
        "bg": rx.cond(state_var, COLORS["red_bg"], COLORS["white"]),
        "border": rx.cond(state_var, f"2px solid {COLORS['red_light']}", f"2px solid {COLORS['gray_light']}"),
        "min_height": min_height,
        "_hover": STYLES["option_card_hover"],
    }
    if disabled_cond is not None:
        props["disabled"] = disabled_cond
    return rx.button(content, **props)


def create_chip(text: str, state_var, remove_func) -> rx.Component:
    """Create a reusable chip component."""
    return rx.cond(
        state_var,
        rx.hstack(
            rx.text(text, font_size="14px", color=COLORS["black"]),
            rx.button(
                rx.text("×", font_size="18px", color=COLORS["gray"], font_weight="bold"),
                on_click=remove_func,
                bg="transparent",
                _hover={"bg": COLORS["gray_light"]},
                padding="0",
                min_width="20px",
                height="20px",
            ),
            spacing="2",
            align_items="center",
            bg=COLORS["gray_bg"],
            border=f"1px solid {COLORS['gray_light']}",
            border_radius="12px",
            padding="6px 12px",
        ),
    )


def create_custom_input(value_var, on_change_func, length_var, placeholder="Type your answer...") -> rx.Component:
    """Create a reusable custom input section."""
    return rx.vstack(
        rx.text("Or enter your own answer", font_size="16px", color=COLORS["black"], font_weight="500", margin_bottom="8"),
        rx.hstack(
            rx.text_area(placeholder=placeholder, value=value_var, on_change=on_change_func, **STYLES["text_area"]),
            rx.text(f"{length_var}/120", font_size="12px", color=COLORS["gray"], margin_left="8"),
            spacing="2",
            align_items="center",
            width="100%",
        ),
        spacing="2",
        width="100%",
        margin_bottom="24",
    )


def create_question_layout(title: str, subtitle: str, option_cards: list, custom_input=None, chips=None) -> rx.Component:
    """Create a reusable question layout."""
    rows = []
    for i in range(0, len(option_cards), 2):
        row_cards = [rx.box(card, width="50%") for card in option_cards[i:i+2]]
        if len(row_cards) == 1:
            row_cards.append(rx.box(width="50%"))
        rows.append(rx.hstack(*row_cards, spacing="4", width="100%"))
    
    content = [
        rx.heading(title, **STYLES["heading"]),
        rx.text(subtitle, **STYLES["subtext"]),
    ]
    
    if chips:
        content.append(
            rx.cond(
                State.can_proceed,
                rx.vstack(
                    rx.hstack(*[chip() if callable(chip) else chip for chip in chips], spacing="2", wrap="wrap"),
                    spacing="2",
                    margin_bottom="24",
                ),
            )
        )
    
    content.extend([
        rx.box(
            rx.vstack(*rows, spacing="4", width="100%"),
            width="100%",
            margin_bottom="32",
        ),
    ])
    
    if custom_input:
        content.append(custom_input)
    
    content.append(
        rx.cond(
            State.validation_error != "",
            rx.text(State.validation_error, font_size="14px", color=COLORS["error"], margin_bottom="16"),
        )
    )
    
    return rx.vstack(*content, spacing="4", width="100%")


def create_nav_button(text: str) -> rx.Component:
    """Create a reusable navbar button."""
    return rx.button(
        text,
        bg=COLORS["red"],
        color="white",
        border_radius="8px",
        padding_x="2rem",
        padding_y="1.25rem",
        font_size="1.1rem",
        font_weight="600",
        _hover={"bg": COLORS["red_dark"], "transform": "translateY(-2px)", "box_shadow": "0 4px 12px rgba(220, 38, 38, 0.3)"},
        transition="all 0.3s ease",
        cursor="pointer",
    )

