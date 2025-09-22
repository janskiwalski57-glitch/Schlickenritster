from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import json
import os
import PIL
import numpy as np


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
        candidate = current_line + (" " if current_line else "") + word
        if len(candidate) <= max_line_chars:
            current_line = candidate
        else:
            if current_line:
                lines.append(current_line)
                if len(lines) == max_lines:
                    break
                current_line = (
                    word if len(word) <= max_line_chars else word[:max_line_chars]
                )
            else:
                # Single word longer than max_line_chars: hard-cut
                lines.append(word[:max_line_chars])
                if len(lines) == max_lines:
                    current_line = ""
                    break
                current_line = ""
    if current_line and len(lines) < max_lines:
        lines.append(current_line)
    return lines


# Constants for layout
PAGE_WIDTH, PAGE_HEIGHT = A4
QR_SIZE = 50 * mm  # Shortened card length due to larger font size
COLS = 4
ROWS = 5
SPACING = 0 * mm

MARGIN = int((A4[0] - (COLS * QR_SIZE + (COLS - 1) * SPACING)) / 2)


def calc_positions():
    """Calculate positions for QR codes and metadata"""
    x_positions = [MARGIN + i * (QR_SIZE + SPACING) for i in range(COLS)]
    y_positions = [
        PAGE_HEIGHT - MARGIN - QR_SIZE - i * (QR_SIZE + SPACING) for i in range(ROWS)
    ]
    return x_positions, y_positions


def create_qr_codes_pdf(background_images=None):
    """Create PDF with just QR codes"""
    c = canvas.Canvas("pdf/qr_codes_front.pdf", pagesize=A4)

    x_positions, y_positions = calc_positions()

    qr_files = sorted([f for f in os.listdir("qr_codes") if f.endswith(".png")])
    qr_files = [f for f in qr_files if not f.endswith("_combined.png")]
    current_qr = 0

    while current_qr < len(qr_files):
        for y in y_positions:
            for x in x_positions:
                if current_qr < len(qr_files):
                    # Select background image based on QR number (cycle every 10 songs)
                    if background_images and len(background_images) > 0:
                        background_index = (current_qr // 10) % len(background_images)
                        background_image = background_images[background_index]

                        # Draw background image with proper scaling to fill the card
                        qr_pil = PIL.Image.open(
                            f"qr_codes/{qr_files[current_qr]}"
                        ).convert("RGB")
                        background_pil = (
                            PIL.Image.open(background_image)
                            .convert("RGB")
                            .resize(qr_pil.size)
                        )

                        # Replace white pixels in QR with background
                        array_bg = np.array(background_pil)
                        array_qr = np.array(qr_pil)  # Ensure QR is RGB
                        # Make white pixels transparent in QR code
                        white = array_qr.sum(axis=(2)) > 300
                        array_qr[white] = array_bg[white]

                        PIL.Image.fromarray(array_qr).save(
                            f"qr_codes/{qr_files[current_qr]}_combined.png"
                        )

                        c.drawImage(
                            f"qr_codes/{qr_files[current_qr]}_combined.png",
                            x,
                            y,
                            QR_SIZE,
                            QR_SIZE,
                            mask="auto",
                            preserveAspectRatio=True,
                        )
                    current_qr += 1
                else:
                    break

        if current_qr < len(qr_files):
            c.showPage()

    c.save()


def remove_metainfo_text(title_text):
    # Enforce hard title length limit
    title_text = title_text.split("-")[0].strip()
    temp = title_text.split(".")
    if len(temp) <= 2:
        title_text = temp[0].strip()
    title_text = title_text.split(",")[0].strip()
    title_text = title_text.split("(")
    if len(title_text) > 1:
        if len(title_text[0]) > 5:
            title_text = title_text[0]
        else:
            title_text = title_text[1]
    else:
        title_text = title_text[0]
    return title_text


def create_metadata_pdf(background_images=None):
    """Create PDF with metadata"""
    c = canvas.Canvas("pdf/metadata_back.pdf", pagesize=A4)

    # Calculate positions (same as QR codes for alignment)
    x_positions, y_positions = calc_positions()

    # Get all JSON files with metadata
    json_files = sorted([f for f in os.listdir("qr_codes") if f.endswith(".json")])
    current_item = 0

    while current_item < len(json_files):
        for y in y_positions:
            for x in x_positions[::-1]:  # Reverse for back side alignment
                if current_item < len(json_files):
                    # Select background image based on item number (cycle every 10 songs)
                    if background_images and len(background_images) > 0:
                        background_index = (current_item // 10) % len(background_images)
                        background_image = background_images[background_index]

                        if os.path.exists(background_image):
                            # Draw background image with proper scaling to fill the card
                            c.drawImage(
                                background_image,
                                x,
                                y,
                                QR_SIZE,
                                QR_SIZE,
                                mask="auto",
                                preserveAspectRatio=True,
                            )

                    # Load metadata from JSON
                    with open(
                        f"qr_codes/{json_files[current_item]}", "r", encoding="utf-8"
                    ) as f:
                        metadata = json.load(f)

                    # Sizes
                    title_artist_size = 12
                    year_size = 24
                    gap = 3  # margin from year

                    center_x = x + QR_SIZE / 2
                    center_y = y + QR_SIZE / 2 - MARGIN / 2

                    year_text = metadata.get("release_year", "Unknown Release Year")
                    # Draw year at the middle
                    c.setFont("BauhausBoldBT", year_size)
                    c.drawCentredString(center_x, center_y, year_text)
                    # Draw artist below year

                    title_text = remove_metainfo_text(metadata.get("name", "Unknown"))

                    # Wrap song name using 10-char line rule (space-aware)
                    song_name_lines = wrap_text_by_char_limit(
                        title_text, max_line_chars=15, max_lines=3
                    )

                    c.setFont("BauhausBoldBT", title_artist_size)
                    for idx, line in enumerate(reversed(song_name_lines)):
                        baseline_text = (
                            center_y + gap + idx * (title_artist_size + 1) + year_size
                        )
                        c.drawCentredString(center_x, baseline_text, line)

                    artist_text = remove_metainfo_text(
                        metadata.get("artists", ["Unknown Artist"])[0]
                    )
                    # Wrap artist name using 10-char line rule (space-aware)
                    artist_name_lines = wrap_text_by_char_limit(
                        artist_text, max_line_chars=15, max_lines=3
                    )
                    for idx, line in enumerate(artist_name_lines):
                        baseline_text = (
                            center_y
                            - gap
                            - idx * (title_artist_size + 1)
                            - title_artist_size
                        )
                        c.drawCentredString(center_x, baseline_text, line)

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
            "BauhausBoldBT.otf",
        ]
        for alt_name in alternative_names:
            if register_custom_font(alt_name, "BauhausBoldBT"):
                custom_font_available = True
                break

    # Load background images from folder
    background_images = []
    if os.path.exists(background_folder):
        # Get all PNG files from the background folder and sort them
        bg_files = sorted(
            [f for f in os.listdir(background_folder) if f.lower().endswith(".png")]
        )
        background_images = [os.path.join(background_folder, f) for f in bg_files]
        print(f"Found {len(background_images)} background images: {bg_files}")
    else:
        print(
            f"Background folder '{background_folder}' not found, using default backgrounds"
        )

    # Generate both PDFs
    create_qr_codes_pdf(background_images)
    create_metadata_pdf(background_images)
    print("PDFs generated successfully!")
    print(" - QR codes: pdf/qr_codes_front.pdf")
    print(" - Metadata: pdf/metadata_back.pdf")
    if background_images:
        print(
            f" - Background cycling: Every 10 songs switches between {len(background_images)} images"
        )


if __name__ == "__main__":
    # Use background folder for cycling backgrounds
    main("background")
