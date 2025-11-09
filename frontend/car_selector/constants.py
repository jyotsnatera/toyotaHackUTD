"""Style constants for the Car Selector application."""

# Color constants
COLORS = {
    "red": "#DC2626",
    "red_dark": "#B91C1C",
    "red_light": "#D32F2F",
    "red_darker": "#B71C1C",
    "red_bg": "#FFF5F5",
    "white": "#FFFFFF",
    "black": "#000000",
    "gray": "#666666",
    "gray_light": "#E0E0E0",
    "gray_bg": "#F5F5F5",
    "error": "#FF6B6B",
    "placeholder": "#999999",
}

# Style constants
STYLES = {
    "heading": {"font_size": "48px", "line_height": "56px", "font_weight": "600", "color": COLORS["black"], "margin_bottom": "8"},
    "subtext": {"font_size": "16px", "color": COLORS["gray"], "margin_bottom": "32"},
    "option_card": {
        "border_radius": "16px",
        "padding": "16px 18px",
        "width": "100%",
        "min_height": "48px",
        "transition": "all 0.25s ease-out",
        "cursor": "pointer",
    },
    "option_card_hover": {"bg": COLORS["red_bg"], "border": f"2px solid {COLORS['red_light']}", "box_shadow": "0 2px 8px rgba(211,47,47,0.2)", "transform": "translateY(-2px)"},
    "text_area": {
        "max_length": 120,
        "bg": COLORS["white"],
        "border": f"1px solid {COLORS['gray_light']}",
        "border_radius": "12px",
        "padding": "20px 16px",
        "color": COLORS["black"],
        "min_height": "100px",
        "_focus": {"border": f"2px solid {COLORS['red_light']}", "outline": "none"},
        "width": "100%",
    },
}

