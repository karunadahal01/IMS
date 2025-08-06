# utils/helpers.py

import random
import string
import logging

logger = logging.getLogger(__name__)


def generate_random_invoice_number(prefix="INV-", length=6):
    """Generate a random invoice number with given prefix and length."""
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    return f"{prefix}{random_part}"


def generate_random_refno(length=8):
    """Generate a random reference number."""
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choices(letters_and_digits, k=length))


def generate_random_quantity(min_qty=10, max_qty=200):
    """Generate a random quantity within given range."""
    return random.randint(min_qty, max_qty)


def generate_random_discount(min_discount=1, max_discount=50):
    """Generate a random discount percentage."""
    return random.randint(min_discount, max_discount)


def generate_random_price(min_price=50, max_price=500):
    """Generate a random price."""
    return random.randint(min_price, max_price)