"""Main script for ticketreader"""
from ticketreader import config
from ticketreader import mercadona


PDF_FILEPATH = config.DATA_DIR / "20231113 Mercadona 12,79 €.pdf"
PDF_FILEPATH = config.DATA_DIR / "20230807 Mercadona 175,96 €.pdf"

def main() -> None:
    """Main function"""
    ticket = mercadona.parse_mercadona_ticket(file_path=PDF_FILEPATH)

if __name__ == "__main__":
    main()