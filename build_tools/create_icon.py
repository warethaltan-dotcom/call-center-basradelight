#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Listener Professional v4.0 - Create Application Icon
Generates application icon for the executable
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("PIL not available - creating placeholder icon")

import os
from pathlib import Path

def create_icon():
    """Create application icon"""
    icons_dir = Path('icons')
    icons_dir.mkdir(exist_ok=True)
    
    if not PIL_AVAILABLE:
        # Create empty ico file as placeholder
        ico_path = icons_dir / 'listener.ico'
        ico_path.touch()
        print(f"Created placeholder icon: {ico_path}")
        return str(ico_path)
    
    # Create professional looking icon
    img = Image.new('RGBA', (256, 256), (0, 0, 0, 0))  # Transparent background
    draw = ImageDraw.Draw(img)
    
    # Colors
    primary_color = (0, 120, 212, 255)    # Microsoft Blue
    secondary_color = (255, 255, 255, 255) # White
    accent_color = (0, 204, 102, 255)      # Green
    
    # Draw background circle
    draw.ellipse([20, 20, 236, 236], fill=primary_color)
    
    # Draw phone handset
    # Handset body
    points = [
        (80, 70), (176, 70), (186, 80), (186, 176),
        (176, 186), (80, 186), (70, 176), (70, 80)
    ]
    draw.polygon(points, fill=secondary_color, outline=(50, 50, 50, 255), width=2)
    
    # Earpiece
    draw.ellipse([90, 85, 166, 105], fill=(30, 30, 30, 255))
    for i in range(3):
        y = 90 + i * 5
        draw.line([95, y, 161, y], fill=(100, 100, 100, 255), width=1)
    
    # Microphone
    draw.ellipse([90, 151, 166, 171], fill=(30, 30, 30, 255))
    for i in range(3):
        y = 156 + i * 5
        draw.line([95, y, 161, y], fill=(100, 100, 100, 255), width=1)
    
    # Keypad
    for row in range(3):
        for col in range(3):
            x = 95 + col * 22
            y = 115 + row * 12
            draw.ellipse([x, y, x+8, y+8], fill=(200, 200, 200, 255), outline=(150, 150, 150, 255))
    
    # Status indicator (green dot)
    draw.ellipse([200, 40, 220, 60], fill=accent_color)
    
    # Add subtle shadow
    shadow = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.ellipse([25, 25, 241, 241], fill=(0, 0, 0, 30))
    
    # Composite shadow with main image
    result = Image.alpha_composite(shadow, img)
    
    # Save in multiple sizes
    ico_path = icons_dir / 'listener.ico'
    result.save(ico_path, format='ICO', sizes=[
        (256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)
    ])
    
    # Also save as PNG for other uses
    png_path = icons_dir / 'listener.png'
    result.save(png_path, format='PNG')
    
    print(f"Created icon: {ico_path}")
    print(f"Created PNG: {png_path}")
    
    return str(ico_path)

if __name__ == "__main__":
    create_icon()