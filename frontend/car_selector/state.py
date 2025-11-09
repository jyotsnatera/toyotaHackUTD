
"""Application state management."""
import reflex as rx
import json
import os


class State(rx.State):
    """Application state."""
    # Quiz question 1: Road conditions
    city_streets: bool = False
    highways: bool = False
    heavy_rain: bool = False
    rough_terrain: bool = False
    snowy_roads: bool = False
    custom_road_condition: str = ""
    save_message: str = ""
    validation_error: str = ""
    current_step: int = 1
    total_steps: int = 5
    
    # Quiz question 2: Car usage
    daily_commuting: bool = False
    weekend_getaways: bool = False
    family_activities: bool = False
    outdoor_hobby: bool = False
    business_delivery: bool = False
    custom_car_usage: str = ""
    
    # Quiz question 3: Vehicle type
    compact_modern: bool = False
    suv_adventurous: bool = False
    sedan_elegant: bool = False
    truck_bold: bool = False
    minivan_family: bool = False
    custom_vehicle_type: str = ""
    
    # Quiz question 4: Comfort & Features
    heated_seats: bool = False
    blind_spot_monitor: bool = False
    panoramic_roof: bool = False
    wireless_carplay: bool = False
    adaptive_cruise: bool = False
    ventilated_seats: bool = False
    premium_seating: bool = False
    power_liftgate: bool = False
    custom_features: str = ""
    
    # Quiz question 5: MSRP Price Range
    msrp_under_25k: bool = False
    msrp_25k_35k: bool = False
    msrp_35k_45k: bool = False
    msrp_45k_55k: bool = False
    msrp_over_55k: bool = False
    msrp_no_preference: bool = False
    
    def set_custom_road_condition(self, value: str):
        self.custom_road_condition = value
    
    def set_custom_car_usage(self, value: str):
        self.custom_car_usage = value
    
    def set_custom_vehicle_type(self, value: str):
        self.custom_vehicle_type = value
    
    def set_custom_features(self, value: str):
        self.custom_features = value
    
    def toggle_msrp_under_25k(self): 
        self._toggle_msrp_single("msrp_under_25k")
    def toggle_msrp_25k_35k(self): 
        self._toggle_msrp_single("msrp_25k_35k")
    def toggle_msrp_35k_45k(self): 
        self._toggle_msrp_single("msrp_35k_45k")
    def toggle_msrp_45k_55k(self): 
        self._toggle_msrp_single("msrp_45k_55k")
    def toggle_msrp_over_55k(self): 
        self._toggle_msrp_single("msrp_over_55k")
    def toggle_msrp_no_preference(self): 
        self._toggle_msrp_single("msrp_no_preference")
    
    def _toggle_msrp_single(self, selected_option: str):
        """Helper to ensure only one MSRP option is selected at a time."""
        msrp_options = ["msrp_under_25k", "msrp_25k_35k", "msrp_35k_45k", "msrp_45k_55k", "msrp_over_55k", "msrp_no_preference"]
        current_value = getattr(self, selected_option)
        # If clicking the same option, toggle it off; otherwise, set only this one to True
        if current_value:
            setattr(self, selected_option, False)
        else:
            # Set all to False first
            for option in msrp_options:
                setattr(self, option, False)
            # Then set the selected one to True
            setattr(self, selected_option, True)
    
    # Toggle methods
    def toggle_city_streets(self): self.city_streets = not self.city_streets
    def toggle_highways(self): self.highways = not self.highways
    def toggle_heavy_rain(self): self.heavy_rain = not self.heavy_rain
    def toggle_rough_terrain(self): self.rough_terrain = not self.rough_terrain
    def toggle_snowy_roads(self): self.snowy_roads = not self.snowy_roads
    def toggle_daily_commuting(self): self.daily_commuting = not self.daily_commuting
    def toggle_weekend_getaways(self): self.weekend_getaways = not self.weekend_getaways
    def toggle_family_activities(self): self.family_activities = not self.family_activities
    def toggle_outdoor_hobby(self): self.outdoor_hobby = not self.outdoor_hobby
    def toggle_business_delivery(self): self.business_delivery = not self.business_delivery
    def toggle_compact_modern(self): self.compact_modern = not self.compact_modern
    def toggle_suv_adventurous(self): self.suv_adventurous = not self.suv_adventurous
    def toggle_sedan_elegant(self): self.sedan_elegant = not self.sedan_elegant
    def toggle_truck_bold(self): self.truck_bold = not self.truck_bold
    def toggle_minivan_family(self): self.minivan_family = not self.minivan_family
    
    def _toggle_feature(self, feature_name: str, max_count: int = 2):
        """Helper to toggle features with max limit."""
        feature_attrs = ["heated_seats", "blind_spot_monitor", "panoramic_roof", "wireless_carplay", 
                        "adaptive_cruise", "ventilated_seats", "premium_seating", "power_liftgate"]
        current_value = getattr(self, feature_name)
        if not current_value:
            count = sum(getattr(self, attr) for attr in feature_attrs if attr != feature_name)
            if count < max_count:
                setattr(self, feature_name, True)
        else:
            setattr(self, feature_name, False)
    
    def toggle_heated_seats(self): self._toggle_feature("heated_seats")
    def toggle_blind_spot_monitor(self): self._toggle_feature("blind_spot_monitor")
    def toggle_panoramic_roof(self): self._toggle_feature("panoramic_roof")
    def toggle_wireless_carplay(self): self._toggle_feature("wireless_carplay")
    def toggle_adaptive_cruise(self): self._toggle_feature("adaptive_cruise")
    def toggle_ventilated_seats(self): self._toggle_feature("ventilated_seats")
    def toggle_premium_seating(self): self._toggle_feature("premium_seating")
    def toggle_power_liftgate(self): self._toggle_feature("power_liftgate")
    
    def get_quiz_data(self) -> dict:
        """Get all quiz answers as a dictionary."""
        q1_options = [
            ("city_streets", "City streets / stop-and-go traffic"),
            ("highways", "Highways / long-distance"),
            ("heavy_rain", "Heavy rain or storms"),
            ("rough_terrain", "Rough terrain / off-road"),
            ("snowy_roads", "Snowy or icy roads"),
        ]
        q2_options = [
            ("daily_commuting", "Daily commuting"),
            ("weekend_getaways", "Weekend getaways or road trips"),
            ("family_activities", "Family activities and errands"),
            ("outdoor_hobby", "Outdoor or hobby trips"),
            ("business_delivery", "Business or delivery use"),
        ]
        q3_options = [
            ("compact_modern", "🚗 Compact & modern – city-friendly, sleek, and easy to park"),
            ("suv_adventurous", "🚙 SUV & adventurous – practical with space for family or weekend getaways"),
            ("sedan_elegant", "🚘 Sedan & elegant – refined, comfortable, and efficient for everyday drives"),
            ("truck_bold", "🛻 Truck & bold – capable, outdoorsy, and ready for tough jobs or adventures"),
            ("minivan_family", "🚐 Minivan & family-focused – roomy, reliable, and built for comfort on long trips"),
        ]
        q4_options = [
            ("heated_seats", "Heated front seats – stay warm on cold mornings"),
            ("blind_spot_monitor", "Blind spot monitor – extra awareness for lane changes"),
            ("panoramic_roof", "Panoramic roof – more light and open feel inside"),
            ("wireless_carplay", "Wireless Apple CarPlay – easy connection without cables"),
            ("adaptive_cruise", "Adaptive cruise control – less effort on long drives"),
            ("ventilated_seats", "Ventilated front seats – comfort in hot weather"),
            ("premium_seating", "Leather or premium seating – upgraded interior feel"),
            ("power_liftgate", "Power liftgate – hands-free loading for groceries or luggage"),
        ]
        q5_options = [
            ("msrp_under_25k", "Under $25,000"),
            ("msrp_25k_35k", "$25,000 - $35,000"),
            ("msrp_35k_45k", "$35,000 - $45,000"),
            ("msrp_45k_55k", "$45,000 - $55,000"),
            ("msrp_over_55k", "Over $55,000"),
            ("msrp_no_preference", "Doesn't matter / No preference"),
        ]
        
        def get_selected(options):
            return [text for attr, text in options if getattr(self, attr)]
        
        return {
            "question_1": {"question": "What kind of roads or conditions do you often drive in?", "selected_options": get_selected(q1_options), "custom_answer": self.custom_road_condition},
            "question_2": {"question": "What do you mainly use your car for?", "selected_options": get_selected(q2_options), "custom_answer": self.custom_car_usage},
            "question_3": {"question": "What kind of vehicle fits your lifestyle and vibe best?", "selected_options": get_selected(q3_options), "custom_answer": self.custom_vehicle_type},
            "question_4": {"question": "Which features would make your driving experience better?", "selected_options": get_selected(q4_options), "custom_answer": self.custom_features},
            "question_5": {"question": "What is your MSRP price preference?", "selected_options": get_selected(q5_options)},
        }
    
    def save_quiz_to_file(self):
        """Save quiz data to a single JSON file (overwrites existing)."""
        quiz_data = self.get_quiz_data()
        data_dir = "quiz_data"
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        filename = f"{data_dir}/quiz_response.json"
        with open(filename, "w") as f:
            json.dump(quiz_data, f, indent=2)
        self.save_message = f"Quiz saved to {filename}"
    
    def validate_and_next(self):
        """Validate current step and proceed."""
        if self.current_step == 1:
            if not (self.city_streets or self.highways or self.heavy_rain or self.rough_terrain or self.snowy_roads or self.custom_road_condition.strip()):
                self.validation_error = "Pick at least one option or type your own."
                return
            self.validation_error = ""
            self.current_step = 2
        elif self.current_step == 2:
            if not (self.daily_commuting or self.weekend_getaways or self.family_activities or self.outdoor_hobby or self.business_delivery or self.custom_car_usage.strip()):
                self.validation_error = "Pick at least one option or type your own."
                return
            self.validation_error = ""
            self.current_step = 3
        elif self.current_step == 3:
            if not (self.compact_modern or self.suv_adventurous or self.sedan_elegant or self.truck_bold or self.minivan_family or self.custom_vehicle_type.strip()):
                self.validation_error = "Pick at least one option or type your own."
                return
            self.validation_error = ""
            self.current_step = 4
        elif self.current_step == 4:
            count = self.feature_selection_count
            if count == 0 and not self.custom_features.strip():
                self.validation_error = "Pick at least one feature or type your own."
                return
            if count > 2:
                self.validation_error = "You can only select up to 2 features."
                return
            self.validation_error = ""
            self.current_step = 5
        elif self.current_step == 5:
            if not (self.msrp_under_25k or self.msrp_25k_35k or self.msrp_35k_45k or self.msrp_45k_55k or self.msrp_over_55k or self.msrp_no_preference):
                self.validation_error = "Please select a price range."
                return
            self.validation_error = ""
            self.save_quiz_to_file()
    
    def go_back(self):
        """Go back to previous question."""
        if self.current_step > 1:
            self.current_step -= 1
            self.validation_error = ""
    
    def remove_selection(self, option_type: str):
        """Remove a selected option."""
        mapping = {"city_streets": "city_streets", "highways": "highways", "heavy_rain": "heavy_rain", 
                  "rough_terrain": "rough_terrain", "snowy_roads": "snowy_roads", "custom": "custom_road_condition"}
        if option_type in mapping:
            attr = mapping[option_type]
            setattr(self, attr, False if attr != "custom_road_condition" else "")
    
    @rx.var
    def progress_percentage(self) -> str:
        return str(int((self.current_step / self.total_steps) * 100))
    
    @rx.var
    def feature_selection_count(self) -> int:
        return sum([self.heated_seats, self.blind_spot_monitor, self.panoramic_roof, self.wireless_carplay, 
                   self.adaptive_cruise, self.ventilated_seats, self.premium_seating, self.power_liftgate])
    
    @rx.var
    def can_proceed(self) -> bool:
        if self.current_step == 1:
            return (self.city_streets or self.highways or self.heavy_rain or self.rough_terrain or self.snowy_roads or self.custom_road_condition.strip() != "")
        elif self.current_step == 2:
            return (self.daily_commuting or self.weekend_getaways or self.family_activities or self.outdoor_hobby or self.business_delivery or self.custom_car_usage.strip() != "")
        elif self.current_step == 3:
            return (self.compact_modern or self.suv_adventurous or self.sedan_elegant or self.truck_bold or self.minivan_family or self.custom_vehicle_type.strip() != "")
        elif self.current_step == 4:
            count = self.feature_selection_count
            return (count >= 1 and count <= 2) or self.custom_features.strip() != ""
        elif self.current_step == 5:
            return (self.msrp_under_25k or self.msrp_25k_35k or self.msrp_35k_45k or self.msrp_45k_55k or self.msrp_over_55k or self.msrp_no_preference)
        return False
    
    @rx.var
    def custom_input_length(self) -> int:
        return len(self.custom_road_condition) if self.custom_road_condition else 0
    
    @rx.var
    def custom_car_usage_length(self) -> int:
        return len(self.custom_car_usage) if self.custom_car_usage else 0
    
    @rx.var
    def custom_vehicle_type_length(self) -> int:
        return len(self.custom_vehicle_type) if self.custom_vehicle_type else 0
    
    @rx.var
    def custom_features_length(self) -> int:
        return len(self.custom_features) if self.custom_features else 0

