

__version__ = "0.3.0"

token = None
api_base = 'https://api.figure.co'

# Resources
from figure.resource import (
    Photobooth,
    Printer,
    Place,
    Event,
    TicketTemplate,
    Text,
    TextVariable,
    Image,
    ImageVariable,
    Portrait,
    PosterOrder,
    Code,
    User,
    Auth
)

from figure.error import (
    FigureError,
    APIConnectionError,
    BadRequestError,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    RateLimitError,
    InternalServerError,
    NotAvailableYetError
)




