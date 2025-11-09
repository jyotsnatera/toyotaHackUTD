# Car Selector - Modern Frontend

A sleek, modern car selector website built with Python Reflex.

## Features

- Clean white navigation bar with logo placeholder
- Four interactive black buttons (Home, About, Cars, Contact)
- Hero section with image placeholder
- Overlay text: "choose a car that fits your life"
- Red call-to-action button: "find your perfect car"
- Smooth hover animations and transitions
- Responsive design

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Initialize Reflex:
```bash
reflex init
```

3. Run the app:
```bash
reflex run
```

The app will be available at `http://localhost:3000`

## Adding Your Photo

To add your photo to the hero section:

1. Place your image file (jpg, png, etc.) in the `assets/` folder
2. In `car_selector/car_selector.py`, find the hero_section function
3. Replace the `bg` gradient with an image:
   - Change `bg="linear-gradient(...)"` to use `rx.image` or set `background_image="url('/your-image.jpg')"`

Example:
```python
background_image="url('/your-image.jpg')",
```

