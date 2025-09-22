from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
import json
import os

# Constants for layout
PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 10 * mm
QR_SIZE = 40 * mm
COLS = 4
ROWS = 6
SPACING = 5 * mm


def create_qr_codes_pdf():
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
                    # Draw border around the QR code
                    c.setStrokeColorRGB(1.0, 0.75, 0.8)  # Pink border
                    c.setLineWidth(0.5)
                    c.rect(x, y, QR_SIZE, QR_SIZE)
                    
                    c.drawImage(
                        f"qr_codes/{qr_files[current_qr]}", x, y, QR_SIZE, QR_SIZE
                    )
                    current_qr += 1
                else:
                    break
        if current_qr < len(qr_files):
            c.showPage()

    c.save()


def create_metadata_pdf():
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
                    # Draw border around the card
                    c.setStrokeColorRGB(1.0, 0.75, 0.8)  # Pink border
                    c.setLineWidth(0.5)
                    c.rect(x, y, QR_SIZE, QR_SIZE)
                    
                    # Load metadata from JSON
                    with open(f"qr_codes/{json_files[current_item]}", "r", encoding="utf-8") as f:
                        metadata = json.load(f)

                    # Draw metadata
                    c.setFont("Helvetica", 6)
                    text_lines = [
                        metadata.get("name", "Unknown"),
                        metadata.get("release_year", "Unknown Release Year"),
                        metadata.get("artists", ["Unknown Artist"])[
                            0
                        ],  # Just first artist
                    ]

                    # Draw text lines (centered)
                    for i, line in enumerate(text_lines):
                        text = line[:30]  # Truncate long text
                        text_width = c.stringWidth(text, "Helvetica", 6)
                        # Center text within the QR code area
                        text_x = x + (QR_SIZE - text_width) / 2
                        c.drawString(text_x, y + QR_SIZE - (i + 1) * 8, text)

                    current_item += 1
                else:
                    break
        if current_item < len(json_files):
            c.showPage()

    c.save()


def main():
    # Create output directory if it doesn't exist
    if not os.path.exists("pdf"):
        os.makedirs("pdf")

    # Generate both PDFs
    create_qr_codes_pdf()
    create_metadata_pdf()
    print("PDFs generated successfully!")
    print(" - QR codes: pdf/qr_codes_front.pdf")
    print(" - Metadata: pdf/metadata_back.pdf")


if __name__ == "__main__":
    main()
