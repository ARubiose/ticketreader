"""Main script for ticketreader"""
from ticketreader import api
from ticketreader import config
from ticketreader import mercadona


def main() -> None:
    """Main function"""
    # api.parse_mercadona_directory(
    #     ticket_directory=config.DATA_DIR /,
    #     destination=config.DATA_DIR / 'tickets-template.xlsx'
    # )
    ticket = mercadona.parse_mercadona_ticket_tabula(
        file_path=config.DATA_DIR / 'Madrid' / 'Saved' / 'my-ticket.pdf')
    print(ticket)


if __name__ == "__main__":
    main()
