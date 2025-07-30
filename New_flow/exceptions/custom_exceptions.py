# exceptions/custom_exceptions.py

class LoginFailedError(Exception):
    """Raised when login fails due to invalid credentials or unexpected errors."""
    pass


class ProductAlreadyExistsError(Exception):
    """Raised when trying to create a product that already exists."""
    pass


class WebDriverInitializationError(Exception):
    """Raised when WebDriver initialization fails."""
    pass


class NavigationError(Exception):
    """Raised when navigation to a menu or page fails."""
    pass


class FormFieldNotFoundError(Exception):
    """Raised when a required form field is not found or not interactable."""
    pass


class PopupHandlingError(Exception):
    """Raised when a popup/modal cannot be handled as expected."""
    pass


class SaveInvoiceError(Exception):
    """Raised when saving the invoice fails."""
    pass


class ProductCreationError(Exception):
    """Raised when trying to create a product that already exists."""
    pass


class PurchaseNotSuccessError(Exception):
    """Raised when the purchase transaction does not complete successfully."""
    pass


class SaveSalesInvoiceError(Exception):
    """Raised when saving the sales invoice fails."""
    pass


class ListNotFoundError(Exception):
    """Raised when saving the sales invoice fails."""
    pass