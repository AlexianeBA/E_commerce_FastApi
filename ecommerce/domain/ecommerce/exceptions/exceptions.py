class UserNotFoundException(Exception):
    pass


class ProductNotFoundException(Exception):
    pass


class ServerError(Exception):
    pass


class StockNotFoundException(Exception):
    pass


class CartNotFoundException(Exception):
    pass


class NoOrderException(Exception):
    pass


class CartEmptyException(Exception):
    pass


class OrderNotFoundException(Exception):
    pass


class UnauthorizedException(Exception):
    pass


class OrderCancellationException(Exception):
    pass


class ReviewNotFoundException(Exception):
    pass


class OrderRefundException(Exception):
    pass


class ItemNotFoundException(Exception):
    pass


class InvalidTokenException(Exception):
    pass


class PromoCodeCreationException(Exception):
    pass


class EmailSendingException(Exception):
    pass


class UserAlreadyExistsException(Exception):
    pass
