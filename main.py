"""Main script for ticketreader"""
from ticketreader import config
from ticketreader import mercadona
from ticketreader import output
from ticketreader.schemas import UnitProduct
from ticketreader.output import excel


# PDF_FILEPATH = config.DATA_DIR / "20231113 Mercadona 12,79 €.pdf"
PDF_FILEPATH = config.DATA_DIR / "Paco" / "20230720 Mercadona 200,52 €.pdf"
# PDF_FILEPATH = config.DATA_DIR / "20230807 Mercadona 175,96 €.pdf"
# PDF_FILEPATH = config.DATA_DIR / "20231115 Mercadona 5,04 €.pdf"


def main() -> None:
    """Main function"""
    # ticket = mercadona.parse_mercadona_ticket(file_path=PDF_FILEPATH)
    ticket = mercadona.parse_mercadona_ticket_tabula(file_path=PDF_FILEPATH)
    excel_handler = output.ExcelHandler(PDF_FILEPATH.parent / "tickets.xlsx")
    # excel_handler.save_ticket(ticket)

    # excel_handler.save_workbook()

    # excel_handler.save_ticket(ticket)
    print("Done!")


if __name__ == "__main__":
    main()
