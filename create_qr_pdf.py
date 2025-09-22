from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import json
import os


def register_custom_font(font_path, font_name):
    """Register a custom TTF font file"""
    if os.path.exists(font_path):
        try:
            pdfmetrics.registerFont(TTFont(font_name, font_path))
            print(f"Successfully registered custom font: {font_name}")
            return True
        except Exception as e:
            print(f"Failed to register font {font_name}: {e}")
            return False
    else:
        print(f"Font file not found: {font_path}")
        return False


def wrap_text_to_lines(text, font_name, font_size, max_width):
    """Wrap text to fit within max_width, breaking at spaces"""
    if not text:
        return [""]
    
    words = text.split()
    if not words:
        return [""]
    
    lines = []
    current_line = ""
    
    for word in words:
        # Create a canvas to measure text width
        temp_canvas = canvas.Canvas("temp_measure.pdf", pagesize=(100, 100))
        temp_canvas.setFont(font_name, font_size)
        
        # Test if adding this word would exceed max_width
        test_line = current_line + (" " if current_line else "") + word
        test_width = temp_canvas.stringWidth(test_line, font_name, font_size)
        
        if test_width <= max_width:
            current_line = test_line
        else:
            # If current line has content, save it and start new line
            if current_line:
                lines.append(current_line)
                current_line = word
            else:
                # Single word is too long, truncate it
                lines.append(word[:30])  # Fallback truncation
                current_line = ""
        
        temp_canvas.save()
        os.remove("temp_measure.pdf")  # Clean up temp file
    
    # Add the last line if it has content
    if current_line:
        lines.append(current_line)
    
    return lines if lines else [""]

def wrap_text_by_char_limit(text, max_line_chars=10, max_lines=3):
    """Wrap text by character count per line, breaking at spaces.
    Returns up to max_lines lines; does not exceed max_line_chars per line.
    """
    if not text:
        return [""]
    words = text.split()
    if not words:
        return [""]
    lines = []
    current_line = ""
    for word in words:
        candidate = (current_line + (" " if current_line else "") + word)
        if len(candidate) <= max_line_chars:
            current_line = candidate
        else:
            if current_line:
                lines.append(current_line)
                if len(lines) == max_lines:
                    break
                current_line = word if len(word) <= max_line_chars else word[:max_line_chars]
            else:
                # Single word longer than max_line_chars: hard-cut
                lines.append(word[:max_line_chars])
                if len(lines) == max_lines:
                    current_line = ""
                    break
                current_line = ""
    if current_line and len(lines) < max_lines:
        lines.append(current_line)
    return lines if lines else [""]

# Constants for layout
PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 10 * mm
QR_SIZE = 35 * mm  # Shortened card length due to larger font size
COLS = 4
ROWS = 6
SPACING = 5 * mm


def create_qr_codes_pdf(background_images=None):
    """Create PDF with just QR codes"""
    c = canvas.Canvas("pdf/qr_codes_front.pdf", pagesize=A4)

    # Calculate positions
    x_positions = [MARGIN + i * (QR_SIZE + SPACING) for i in range(COLS)]
    y_positions = [
        PAGE_HEIGHT - MARGIN - QR_SIZE - i * (QR_SIZE + SPACING) for i in range(ROWS)
    ]

    qr_files = sorted([f for f in os.listdir("qr_codes") if f.endswith(".png")])
    current_qr = 0

    while current_qr < len(qr_files):
        for y in y_positions:
            for x in x_positions:
                if current_qr < len(qr_files):
                    # Select background image based on QR number (cycle every 10 songs)
                    if background_images and len(background_images) > 0:
                        background_index = (current_qr // 10) % len(background_images)
                        background_image = background_images[background_index]
                        
                        if os.path.exists(background_image):
                            try:
                                # Draw background image with proper scaling to fill the card
                                c.drawImage(background_image, x, y, QR_SIZE, QR_SIZE, 
                                          mask='auto', preserveAspectRatio=True)
                            except:
                                # If image fails to load, draw a colored background
                                c.setFillColorRGB(0.95, 0.95, 0.98)  # Light background
                                c.rect(x, y, QR_SIZE, QR_SIZE, fill=1)
                        else:
                            # Draw default background
                            c.setFillColorRGB(0.95, 0.95, 0.98)  # Light background
                            c.rect(x, y, QR_SIZE, QR_SIZE, fill=1)
                    else:
                        # Draw default background
                        c.setFillColorRGB(0.95, 0.95, 0.98)  # Light background
                        c.rect(x, y, QR_SIZE, QR_SIZE, fill=1)
                    
                    c.drawImage(
                        f"qr_codes/{qr_files[current_qr]}", x, y, QR_SIZE, QR_SIZE
                    )
                    current_qr += 1
                else:
                    break
        if current_qr < len(qr_files):
            c.showPage()

    c.save()


def create_metadata_pdf(background_images=None):
    """Create PDF with metadata"""
    c = canvas.Canvas("pdf/metadata_back.pdf", pagesize=A4)

    # Calculate positions (same as QR codes for alignment)
    x_positions = [MARGIN + i * (QR_SIZE + SPACING) for i in range(COLS)]
    y_positions = [
        PAGE_HEIGHT - MARGIN - QR_SIZE - i * (QR_SIZE + SPACING) for i in range(ROWS)
    ]

    # Get all JSON files with metadata
    json_files = sorted([f for f in os.listdir("qr_codes") if f.endswith(".json")])
    current_item = 0

    while current_item < len(json_files):
        for y in y_positions:
            for x in x_positions[::-1]:
                if current_item < len(json_files):
                    # Select background image based on item number (cycle every 10 songs)
                    if background_images and len(background_images) > 0:
                        background_index = (current_item // 10) % len(background_images)
                        background_image = background_images[background_index]
                        
                        if os.path.exists(background_image):
                            try:
                                # Draw background image with proper scaling to fill the card
                                c.drawImage(background_image, x, y, QR_SIZE, QR_SIZE, 
                                          mask='auto', preserveAspectRatio=True)
                            except:
                                # If image fails to load, draw a colored background
                                c.setFillColorRGB(0.95, 0.95, 0.98)  # Light background
                                c.rect(x, y, QR_SIZE, QR_SIZE, fill=1)
                        else:
                            # Draw default background
                            c.setFillColorRGB(0.95, 0.95, 0.98)  # Light background
                            c.rect(x, y, QR_SIZE, QR_SIZE, fill=1)
                    else:
                        # Draw default background
                        c.setFillColorRGB(0.95, 0.95, 0.98)  # Light background
                        c.rect(x, y, QR_SIZE, QR_SIZE, fill=1)
                    
                    # Load metadata from JSON
                    with open(f"qr_codes/{json_files[current_item]}", "r", encoding="utf-8") as f:
                        metadata = json.load(f)

                    # Draw metadata with text wrapping for song names
                    # Calculate available width (with some padding)
                    available_width = QR_SIZE - 4  # 2mm padding on each side
                    
                    # Enforce hard title length limit
                    title_text = metadata.get("name", "Unknown")
                    if len(title_text) > 30:
                        print(f"Skipping title over 30 chars: {title_text}")
                        current_item += 1
                        continue
                    # Wrap song name using 10-char line rule (space-aware)
                    song_name_lines = wrap_text_by_char_limit(title_text, max_line_chars=10, max_lines=3)
                    # Balance first two lines by moving the last word from line 1 to line 2 if line 1 is much longer
                    if len(song_name_lines) >= 2:
                        measure_font = "BauhausBoldBT"
                        try:
                            _ = pdfmetrics.getFont(measure_font)
                        except:
                            measure_font = "Helvetica-Bold"
                        def line_width(txt):
                            return c.stringWidth(txt, measure_font, 14)
                        first = song_name_lines[0]
                        second = song_name_lines[1]
                        # Move words while second line can accept them and the first line is significantly longer
                        while True:
                            parts = first.rstrip().split(" ")
                            if len(parts) <= 1:
                                break
                            last_word = parts[-1]
                            candidate_first = " ".join(parts[:-1])
                            candidate_second = (last_word + (" " + second if second else ""))
                            if line_width(candidate_second) <= available_width and (line_width(first) - line_width(second)) > (2 * 14):
                                first = candidate_first
                                second = candidate_second
                            else:
                                break
                        song_name_lines[0] = first
                        song_name_lines[1] = second
                    # Constrain to max number of title lines and add ellipsis if needed
                    max_title_lines = 3
                    if len(song_name_lines) > max_title_lines:
                        song_name_lines = song_name_lines[:max_title_lines]
                    
                    # Create text lines with wrapped song name
                    text_lines = []
                    for line in song_name_lines:
                        text_lines.append({"text": line, "font": "BauhausBoldBT", "size": 14, "fallback": "BauhausBoldBT"})
                    
                    # Add year and artist
                    text_lines.extend([
                        {"text": metadata.get("release_year", "Unknown Release Year"), "font": "BauhausBoldBT", "size": 8, "fallback": "BauhausBoldBT"},
                        {"text": metadata.get("artists", ["Unknown Artist"])[0], "font": "BauhausBoldBT", "size": 8, "fallback": "BauhausBoldBT"},  # Just first artist
                    ])
                    
                    # Calculate total height needed for all text
                    total_text_height = 0
                    line_heights = []
                    title_line_count = len(song_name_lines)
                    for idx, line_info in enumerate(text_lines):
                        c.setFont(line_info["font"], line_info["size"])
                        # Tighter spacing between title lines (-1), extra gap before year/artist (+2)
                        if idx < title_line_count:
                            line_height = line_info["size"] + 1
                        elif idx == title_line_count:  # first non-title line (year)
                            line_height = line_info["size"] + 8
                        else:
                            line_height = line_info["size"] + 3
                        line_heights.append(line_height)
                        total_text_height += line_height
                    
                    # Calculate starting Y position to center text vertically
                    start_y = y + (QR_SIZE - total_text_height) / 2 + total_text_height
                    
                    # Draw text lines (centered horizontally and vertically)
                    current_y = start_y
                    for i, line_info in enumerate(text_lines):
                        # Try primary font, fallback to secondary if not available
                        try:
                            c.setFont(line_info["font"], line_info["size"])
                            font_name = line_info["font"]
                        except:
                            c.setFont(line_info["fallback"], line_info["size"])
                            font_name = line_info["fallback"]
                        
                        text = line_info["text"]
                        text_width = c.stringWidth(text, font_name, line_info["size"])
                        # Center text horizontally within the QR code area
                        text_x = x + (QR_SIZE - text_width) / 2
                        c.drawString(text_x, current_y - line_heights[i], text)
                        current_y -= line_heights[i]

                    current_item += 1
                else:
                    break
        if current_item < len(json_files):
            c.showPage()

    c.save()


def main(background_folder="background"):
    # Create output directory if it doesn't exist
    if not os.path.exists("pdf"):
        os.makedirs("pdf")

    # Register custom font if available
    custom_font_available = register_custom_font("font.ttf", "BauhausBoldBT")
    if not custom_font_available:
        # Try alternative font file names
        alternative_names = [
            "fonts/BauhausBoldBT.ttf",
            "fonts/BauhausBoldBT.otf",
            "fonts/BauhausBoldBT.woff",
            "fonts/bauhaus_bold_bt.ttf",
            "fonts/bauhaus_bold_bt.otf",
            "BauhausBoldBT.ttf",
            "BauhausBoldBT.otf"
        ]
        for alt_name in alternative_names:
            if register_custom_font(alt_name, "BauhausBoldBT"):
                custom_font_available = True
                break

    # Load background images from folder
    background_images = []
    if os.path.exists(background_folder):
        # Get all PNG files from the background folder and sort them
        bg_files = sorted([f for f in os.listdir(background_folder) if f.lower().endswith('.png')])
        background_images = [os.path.join(background_folder, f) for f in bg_files]
        print(f"Found {len(background_images)} background images: {bg_files}")
    else:
        print(f"Background folder '{background_folder}' not found, using default backgrounds")

    # Generate both PDFs
    create_qr_codes_pdf(background_images)
    create_metadata_pdf(background_images)
    print("PDFs generated successfully!")
    print(" - QR codes: pdf/qr_codes_front.pdf")
    print(" - Metadata: pdf/metadata_back.pdf")
    if background_images:
        print(f" - Background cycling: Every 10 songs switches between {len(background_images)} images")


if __name__ == "__main__":
    # Use background folder for cycling backgrounds
    main("background")
