from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
import os

# Constants for layout (same as main file)
PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 10 * mm
QR_SIZE = 40 * mm
COLS = 4
ROWS = 6
SPACING = 5 * mm


class TestPDFGenerator:
    """Test class with mock data for PDF generation"""
    
    def __init__(self):
        self.mock_tracks = [
            {
                "name": "Bohemian Rhapsody",
                "artists": ["Queen"],
                "release_year": "1975",
                "album": "A Night at the Opera"
            },
            {
                "name": "Stairway to Heaven",
                "artists": ["Led Zeppelin"],
                "release_year": "1971",
                "album": "Led Zeppelin IV"
            },
            {
                "name": "Hotel California",
                "artists": ["Eagles"],
                "release_year": "1976",
                "album": "Hotel California"
            },
            {
                "name": "Imagine",
                "artists": ["John Lennon"],
                "release_year": "1971",
                "album": "Imagine"
            },
            {
                "name": "Sweet Child O' Mine",
                "artists": ["Guns N' Roses"],
                "release_year": "1987",
                "album": "Appetite for Destruction"
            },
            {
                "name": "Smells Like Teen Spirit",
                "artists": ["Nirvana"],
                "release_year": "1991",
                "album": "Nevermind"
            },
            {
                "name": "Wonderwall",
                "artists": ["Oasis"],
                "release_year": "1995",
                "album": "(What's the Story) Morning Glory?"
            },
            {
                "name": "Creep",
                "artists": ["Radiohead"],
                "release_year": "1992",
                "album": "Pablo Honey"
            },
            {
                "name": "Losing My Religion",
                "artists": ["R.E.M."],
                "release_year": "1991",
                "album": "Out of Time"
            },
            {
                "name": "Black",
                "artists": ["Pearl Jam"],
                "release_year": "1991",
                "album": "Ten"
            },
            {
                "name": "Come As You Are",
                "artists": ["Nirvana"],
                "release_year": "1991",
                "album": "Nevermind"
            },
            {
                "name": "Under the Bridge",
                "artists": ["Red Hot Chili Peppers"],
                "release_year": "1991",
                "album": "Blood Sugar Sex Magik"
            },
            {
                "name": "Jeremy",
                "artists": ["Pearl Jam"],
                "release_year": "1991",
                "album": "Ten"
            },
            {
                "name": "Alive",
                "artists": ["Pearl Jam"],
                "release_year": "1991",
                "album": "Ten"
            },
            {
                "name": "Lithium",
                "artists": ["Nirvana"],
                "release_year": "1991",
                "album": "Nevermind"
            },
            {
                "name": "Even Flow",
                "artists": ["Pearl Jam"],
                "release_year": "1991",
                "album": "Ten"
            },
            {
                "name": "In Bloom",
                "artists": ["Nirvana"],
                "release_year": "1991",
                "album": "Nevermind"
            },
            {
                "name": "Breed",
                "artists": ["Nirvana"],
                "release_year": "1991",
                "album": "Nevermind"
            },
            {
                "name": "Polly",
                "artists": ["Nirvana"],
                "release_year": "1991",
                "album": "Nevermind"
            },
            {
                "name": "Territorial Pissings",
                "artists": ["Nirvana"],
                "release_year": "1991",
                "album": "Nevermind"
            },
            {
                "name": "Drain You",
                "artists": ["Nirvana"],
                "release_year": "1991",
                "album": "Nevermind"
            },
            {
                "name": "Lounge Act",
                "artists": ["Nirvana"],
                "release_year": "1991",
                "album": "Nevermind"
            },
            {
                "name": "Stay Away",
                "artists": ["Nirvana"],
                "release_year": "1991",
                "album": "Nevermind"
            },
            {
                "name": "On a Plain",
                "artists": ["Nirvana"],
                "release_year": "1991",
                "album": "Nevermind"
            },
            {
                "name": "Something in the Way",
                "artists": ["Nirvana"],
                "release_year": "1991",
                "album": "Nevermind"
            }
        ]
    
    def create_test_qr_codes_pdf(self):
        """Create test PDF with mock QR code placeholders"""
        c = canvas.Canvas("pdf/test_qr_codes_front.pdf", pagesize=A4)
        
        # Calculate positions
        x_positions = [MARGIN + i * (QR_SIZE + SPACING) for i in range(COLS)]
        y_positions = [
            PAGE_HEIGHT - MARGIN - QR_SIZE - i * (QR_SIZE + SPACING) for i in range(ROWS)
        ]
        
        current_track = 0
        
        while current_track < len(self.mock_tracks):
            for y in y_positions:
                for x in x_positions:
                    if current_track < len(self.mock_tracks):
                        # Draw border around the QR code
                        c.setStrokeColorRGB(1.0, 0.75, 0.8)  # Pink border
                        c.setLineWidth(0.5)
                        c.rect(x, y, QR_SIZE, QR_SIZE)
                        
                        # Draw placeholder rectangle for QR code
                        c.setFillColorRGB(0.9, 0.9, 0.9)  # Light gray
                        c.rect(x + 2, y + 2, QR_SIZE - 4, QR_SIZE - 4, fill=1)
                        
                        # Draw track number
                        c.setFillColorRGB(0, 0, 0)  # Black text
                        c.setFont("Helvetica-Bold", 12)
                        c.drawString(x + QR_SIZE/2 - 10, y + QR_SIZE/2 - 6, f"#{current_track + 1}")
                        
                        current_track += 1
                    else:
                        break
            if current_track < len(self.mock_tracks):
                c.showPage()
        
        c.save()
    
    def create_test_metadata_pdf(self):
        """Create test PDF with mock metadata"""
        c = canvas.Canvas("pdf/test_metadata_back.pdf", pagesize=A4)
        
        # Calculate positions (same as QR codes for alignment)
        x_positions = [MARGIN + i * (QR_SIZE + SPACING) for i in range(COLS)]
        y_positions = [
            PAGE_HEIGHT - MARGIN - QR_SIZE - i * (QR_SIZE + SPACING) for i in range(ROWS)
        ]
        
        current_track = 0
        
        while current_track < len(self.mock_tracks):
            for y in y_positions:
                for x in x_positions[::-1]:
                    if current_track < len(self.mock_tracks):
                        track = self.mock_tracks[current_track]
                        
                        # Draw border around the card
                        c.setStrokeColorRGB(1.0, 0.75, 0.8)  # Pink border
                        c.setLineWidth(0.5)
                        c.rect(x, y, QR_SIZE, QR_SIZE)
                        
                        # Draw metadata
                        c.setFont("Helvetica", 6)
                        text_lines = [
                            track["name"],
                            track["release_year"],
                            track["artists"][0],  # Just first artist
                        ]
                        
                        # Draw text lines (centered)
                        for i, line in enumerate(text_lines):
                            text = line[:30]  # Truncate long text
                            text_width = c.stringWidth(text, "Helvetica", 6)
                            # Center text within the QR code area
                            text_x = x + (QR_SIZE - text_width) / 2
                            c.drawString(text_x, y + QR_SIZE - (i + 1) * 8, text)
                        
                        current_track += 1
                    else:
                        break
            if current_track < len(self.mock_tracks):
                c.showPage()
        
        c.save()
    
    def run_test(self):
        """Run the test PDF generation"""
        # Create output directory if it doesn't exist
        if not os.path.exists("pdf"):
            os.makedirs("pdf")
        
        # Generate test PDFs
        self.create_test_qr_codes_pdf()
        self.create_test_metadata_pdf()
        print("Test PDFs generated successfully!")
        print(" - QR codes: pdf/test_qr_codes_front.pdf")
        print(" - Metadata: pdf/test_metadata_back.pdf")


if __name__ == "__main__":
    TestPDFGenerator().run_test()
