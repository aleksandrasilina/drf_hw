import stripe

from config import settings

stripe.api_key = settings.STRIPE_API_KEY


def create_stripe_product(product):
    """Создает продукт в страйпе."""

    return stripe.Product.create(name=product.title)


def create_stripe_price(product, amount):
    """Создает цену в страйпе."""

    return stripe.Price.create(
        currency="rub",
        product=product,
        unit_amount=amount * 100,
    )


def create_stripe_session(price):
    """Создает сессию на оплату в страйпе."""

    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")


def get_stripe_status(session_id):
    """Создает информацию о сессии на оплату в страйпе."""

    return stripe.checkout.Session.retrieve(session_id).get("payment_status")
