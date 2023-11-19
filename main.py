"""Main script for ticketreader"""
from ticketreader import api
from ticketreader import config


def main() -> None:
    """Main function"""
    api.parse_mercadona_directory(
        ticket_directory=config.DATA_DIR / 'Madrid',
        destination=config.DATA_DIR / 'tickets-madrid.xlsx'
    )


if __name__ == "__main__":
    main()
