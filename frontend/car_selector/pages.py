"""Page components for the Car Selector application."""
import reflex as rx
from .constants import COLORS, STYLES
from .state import State
from .components import create_option_card, create_chip, create_custom_input, create_question_layout, create_nav_button


def navbar() -> rx.Component:
    """Navigation bar component."""
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.image(src="/logofr.png", height="80px", max_width="400px", object_fit="contain", alt="Logo"),
                rx.image(src="/poyo.png", height="80px", max_width="400px", object_fit="contain", alt="Poyo"),
                spacing="3", align_items="center", padding="4",
            ),
            rx.box(width="200px"),
            rx.hstack(
                *[create_nav_button(btn) for btn in ["Home", "About", "Cars", "Contact"]],
                spacing="4", align_items="center", padding_right="0", margin_left="700px", margin_top="20px"
            ),
            align_items="flex-start", width="100%", padding_x="8", padding_y="6", padding_left="40px",
        ),
        bg="white", width="100%", box_shadow="0 2px 8px rgba(0,0,0,0.1)", position="sticky", top="0", z_index="1000", min_height="70px",
    )


def hero_section() -> rx.Component:
    """Hero section with image and text overlay."""
    return rx.box(
        rx.box(
            rx.image(src="/p4.png", width="100%", height="100%", object_fit="cover", position="absolute", top="0", left="0", z_index="1"),
            rx.box(
                rx.vstack(
                    rx.heading("Choose a Car That Fits YOUR Life!", font_size="3.5rem", font_weight="bold", color="black", text_align="left", text_shadow="2px 2px 8px rgba(0,0,0,0.5)", line_height="1.2"),
                    rx.link(
                        rx.button("Find the Perfect Toyota", bg=COLORS["red"], color="white", font_size="1.5rem", font_weight="600", padding_x="4rem", padding_y="1.5rem", border_radius="50px", margin_top="2rem", _hover={"bg": COLORS["red_dark"], "transform": "scale(1.05)", "box_shadow": "0 8px 24px rgba(220, 38, 38, 0.4)"}, transition="all 0.3s ease", cursor="pointer"),
                        href="/quiz",
                    ),
                    align_items="flex-start", spacing="4",
                ),
                position="absolute", left="10%", top="50%", transform="translateY(-50%)", z_index="10", max_width="600px",
            ),
            width="100%", min_height="calc(100vh - 80px)", position="relative", overflow="hidden",
        ),
        width="100%",
    )


# Question 1 components
def option_card_city(): return create_option_card("City streets / stop-and-go traffic", State.city_streets, State.toggle_city_streets)
def option_card_highways(): return create_option_card("Highways / long-distance", State.highways, State.toggle_highways)
def option_card_rain(): return create_option_card("Heavy rain or storms", State.heavy_rain, State.toggle_heavy_rain)
def option_card_terrain(): return create_option_card("Rough terrain / off-road", State.rough_terrain, State.toggle_rough_terrain)
def option_card_snow(): return create_option_card("Snowy or icy roads", State.snowy_roads, State.toggle_snowy_roads)

def chip_city(): return create_chip("City streets / stop-and-go traffic", State.city_streets, State.remove_selection("city_streets"))
def chip_highways(): return create_chip("Highways / long-distance", State.highways, State.remove_selection("highways"))
def chip_rain(): return create_chip("Heavy rain or storms", State.heavy_rain, State.remove_selection("heavy_rain"))
def chip_terrain(): return create_chip("Rough terrain / off-road", State.rough_terrain, State.remove_selection("rough_terrain"))
def chip_snow(): return create_chip("Snowy or icy roads", State.snowy_roads, State.remove_selection("snowy_roads"))
def chip_custom():
    return rx.cond(
        State.custom_road_condition.strip() != "",
        rx.hstack(
            rx.text(State.custom_road_condition, font_size="14px", color=COLORS["black"]),
            rx.button(
                rx.text("×", font_size="18px", color=COLORS["gray"], font_weight="bold"),
                on_click=State.remove_selection("custom"),
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


# Question 2 components
def option_card_daily_commuting(): return create_option_card("Daily commuting", State.daily_commuting, State.toggle_daily_commuting)
def option_card_weekend_getaways(): return create_option_card("Weekend getaways or road trips", State.weekend_getaways, State.toggle_weekend_getaways)
def option_card_family_activities(): return create_option_card("Family activities and errands", State.family_activities, State.toggle_family_activities)
def option_card_outdoor_hobby(): return create_option_card("Outdoor or hobby trips", State.outdoor_hobby, State.toggle_outdoor_hobby)
def option_card_business_delivery(): return create_option_card("Business or delivery use", State.business_delivery, State.toggle_business_delivery)


# Question 3 components
def option_card_compact_modern(): return create_option_card("Compact & modern", State.compact_modern, State.toggle_compact_modern, "city-friendly, sleek, and easy to park", min_height="60px")
def option_card_suv_adventurous(): return create_option_card("SUV & adventurous", State.suv_adventurous, State.toggle_suv_adventurous, "practical with space for family or weekend getaways", min_height="60px")
def option_card_sedan_elegant(): return create_option_card("Sedan & elegant", State.sedan_elegant, State.toggle_sedan_elegant, "refined, comfortable, and efficient for everyday drives", min_height="60px")
def option_card_truck_bold(): return create_option_card("Truck & bold", State.truck_bold, State.toggle_truck_bold, "capable, outdoorsy, and ready for tough jobs or adventures", min_height="60px")
def option_card_minivan_family(): return create_option_card("Minivan & family-focused", State.minivan_family, State.toggle_minivan_family, "roomy, reliable, and built for comfort on long trips", min_height="60px")


# Question 4 components
def _create_feature_card(text, state_var, toggle_func, subtitle):
    return create_option_card(text, state_var, toggle_func, subtitle, 
                             rx.cond(rx.cond(state_var, False, State.feature_selection_count >= 2), True, False), min_height="60px")

def option_card_heated_seats(): return _create_feature_card("Heated front seats", State.heated_seats, State.toggle_heated_seats, "stay warm on cold mornings")
def option_card_blind_spot(): return _create_feature_card("Blind spot monitor", State.blind_spot_monitor, State.toggle_blind_spot_monitor, "extra awareness for lane changes")
def option_card_panoramic_roof(): return _create_feature_card("Panoramic roof", State.panoramic_roof, State.toggle_panoramic_roof, "more light and open feel inside")
def option_card_wireless_carplay(): return _create_feature_card("Wireless Apple CarPlay", State.wireless_carplay, State.toggle_wireless_carplay, "easy connection without cables")
def option_card_adaptive_cruise(): return _create_feature_card("Adaptive cruise control", State.adaptive_cruise, State.toggle_adaptive_cruise, "less effort on long drives")
def option_card_ventilated_seats(): return _create_feature_card("Ventilated front seats", State.ventilated_seats, State.toggle_ventilated_seats, "comfort in hot weather")
def option_card_premium_seating(): return _create_feature_card("Leather or premium seating", State.premium_seating, State.toggle_premium_seating, "upgraded interior feel")
def option_card_power_liftgate(): return _create_feature_card("Power liftgate", State.power_liftgate, State.toggle_power_liftgate, "hands-free loading for groceries or luggage")


def progress_header() -> rx.Component:
    """Create sticky progress header."""
    step_labels = {1: "How You Drive", 2: "Car Usage", 3: "Vehicle Type", 4: "Comfort & Features", 5: "Budget"}
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(step_labels.get(State.current_step, "Quiz"), font_size="14px", color=COLORS["gray"], font_weight="500"),
                rx.spacer(),
                rx.text(f"Step {State.current_step} of {State.total_steps}", font_size="14px", color=COLORS["gray"], font_weight="500"),
                width="100%", align_items="center",
            ),
            rx.box(
                rx.box(width=f"{State.progress_percentage}%", height="8px", bg=COLORS["red_light"], border_radius="4px", transition="width 0.25s ease-out"),
                width="100%", height="8px", bg=COLORS["gray_light"], border_radius="4px", overflow="hidden",
            ),
            spacing="3", width="100%",
        ),
        position="sticky", top="0", z_index="100", bg=COLORS["white"], padding="24px", border_bottom=f"1px solid {COLORS['gray_light']}", box_shadow="0 2px 4px rgba(0,0,0,0.1)",
    )


def question_1_content() -> rx.Component:
    """Question 1: Road conditions."""
    return create_question_layout(
        "What kind of roads or conditions do you often drive in?",
        "(Select all that apply)",
        [option_card_city(), option_card_highways(), option_card_rain(), option_card_terrain(), option_card_snow()],
        create_custom_input(State.custom_road_condition, State.set_custom_road_condition, State.custom_input_length),
        [chip_city, chip_highways, chip_rain, chip_terrain, chip_snow, chip_custom],
    )


def question_2_content() -> rx.Component:
    """Question 2: Car usage."""
    return create_question_layout(
        "What do you mainly use your car for?",
        "(Select all that apply)",
        [option_card_daily_commuting(), option_card_weekend_getaways(), option_card_family_activities(), option_card_outdoor_hobby(), option_card_business_delivery()],
        create_custom_input(State.custom_car_usage, State.set_custom_car_usage, State.custom_car_usage_length),
    )


def question_3_content() -> rx.Component:
    """Question 3: Vehicle type."""
    return create_question_layout(
        "What kind of vehicle fits your lifestyle and vibe best?",
        "(Select all that apply)",
        [option_card_compact_modern(), option_card_suv_adventurous(), option_card_sedan_elegant(), option_card_truck_bold(), option_card_minivan_family()],
        create_custom_input(State.custom_vehicle_type, State.set_custom_vehicle_type, State.custom_vehicle_type_length),
    )


def question_4_content() -> rx.Component:
    """Question 4: Comfort & Features."""
    content = [
        rx.heading("Which features would make your driving experience better?", **STYLES["heading"]),
        rx.text("(Select up to 2)", **STYLES["subtext"]),
        rx.cond(State.feature_selection_count > 0, rx.text(f"{State.feature_selection_count} of 2 selected", font_size="14px", color=COLORS["gray"], margin_bottom="16")),
    ]
    cards = [option_card_heated_seats(), option_card_blind_spot(), option_card_panoramic_roof(), option_card_wireless_carplay(),
            option_card_adaptive_cruise(), option_card_ventilated_seats(), option_card_premium_seating(), option_card_power_liftgate()]
    rows = [rx.hstack(rx.box(cards[i], width="50%"), rx.box(cards[i+1], width="50%"), spacing="4", width="100%") for i in range(0, len(cards), 2)]
    content.extend([
        rx.box(rx.vstack(*rows, spacing="4", width="100%"), width="100%", margin_bottom="32"),
        create_custom_input(State.custom_features, State.set_custom_features, State.custom_features_length),
        rx.cond(State.validation_error != "", rx.text(State.validation_error, font_size="14px", color=COLORS["error"], margin_bottom="16")),
    ])
    return rx.vstack(*content, spacing="4", width="100%")


# Question 5 components
def option_card_msrp_under_25k(): return create_option_card("Under $25,000", State.msrp_under_25k, State.toggle_msrp_under_25k)
def option_card_msrp_25k_35k(): return create_option_card("$25,000 - $35,000", State.msrp_25k_35k, State.toggle_msrp_25k_35k)
def option_card_msrp_35k_45k(): return create_option_card("$35,000 - $45,000", State.msrp_35k_45k, State.toggle_msrp_35k_45k)
def option_card_msrp_45k_55k(): return create_option_card("$45,000 - $55,000", State.msrp_45k_55k, State.toggle_msrp_45k_55k)
def option_card_msrp_over_55k(): return create_option_card("Over $55,000", State.msrp_over_55k, State.toggle_msrp_over_55k)
def option_card_msrp_no_preference(): return create_option_card("Doesn't matter / No preference", State.msrp_no_preference, State.toggle_msrp_no_preference)

def question_5_content() -> rx.Component:
    """Question 5: MSRP Price Range."""
    return create_question_layout(
        "What is your MSRP price preference?",
        "(Select one)",
        [option_card_msrp_under_25k(), option_card_msrp_25k_35k(), option_card_msrp_35k_45k(), option_card_msrp_45k_55k(), option_card_msrp_over_55k(), option_card_msrp_no_preference()],
    )


def quiz_page() -> rx.Component:
    """Quiz page component."""
    return rx.vstack(
        navbar(),
        progress_header(),
        rx.center(
            rx.vstack(
                rx.cond(
                    State.current_step == 1, question_1_content(),
                    rx.cond(
                        State.current_step == 2, question_2_content(),
                        rx.cond(
                            State.current_step == 3, question_3_content(),
                            rx.cond(
                                State.current_step == 4, question_4_content(),
                                rx.cond(State.current_step == 5, question_5_content(), question_1_content()),
                            ),
                        ),
                    ),
                ),
                rx.box(
                    rx.hstack(
                        rx.button("Back", variant="ghost", color=COLORS["gray"], _hover={"bg": COLORS["gray_bg"]}, padding_x="24", padding_y="12",
                                 on_click=State.go_back, disabled=rx.cond(State.current_step == 1, True, False)),
                        rx.spacer(),
                        rx.vstack(
                            rx.button("Next", bg=rx.cond(State.can_proceed, COLORS["red_light"], COLORS["gray_light"]), color="white",
                                     _hover=rx.cond(State.can_proceed, {"bg": COLORS["red_darker"]}, {}), padding_x="32", padding_y="12",
                                     border_radius="8px", on_click=State.validate_and_next, disabled=rx.cond(State.can_proceed, False, True),
                                     cursor=rx.cond(State.can_proceed, "pointer", "not-allowed")),
                            spacing="0", align_items="center",
                        ),
                        spacing="4", width="100%", align_items="center",
                    ),
                    position="sticky", bottom="0", bg="transparent", padding="24px", width="100%",
                ),
                spacing="6", width="100%", max_width="880px", padding_x="24", padding_y="40",
            ),
            width="100%", min_height="calc(100vh - 80px)",
        ),
        spacing="0", width="100%", min_height="100vh", align_items="stretch", bg=COLORS["white"],
    )


def index() -> rx.Component:
    """Main page component."""
    return rx.vstack(navbar(), hero_section(), spacing="0", width="100%", min_height="100vh", align_items="stretch")

