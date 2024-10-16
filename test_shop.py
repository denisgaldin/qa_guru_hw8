import pytest
from models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


class TestProducts:
    def test_product_check_quantity(self, product):
        assert product.check_quantity(100) is True
        assert product.check_quantity(1000) is True
        assert product.check_quantity(1001) is False
        assert product.check_quantity(0) is True

    def test_product_buy(self, product):
        product.buy(100)
        assert product.quantity == 900  # Remaining quantity after purchase
        product.buy(200)
        assert product.quantity == 700  # Remaining quantity after another purchase

    def test_product_buy_more_than_available(self, product):
        with pytest.raises(ValueError, match='Продукта недостаточно на складе!'):
            product.buy(1001)  # Attempting to buy more than available


class TestCart:
    @pytest.fixture
    def cart(self):
        return Cart()

    def test_add_product(self, cart, product):
        cart.add_product(product, 2)
        assert product in cart.products
        assert cart.products[product] == 2

    def test_add_existing_product(self, cart, product):
        cart.add_product(product, 2)
        cart.add_product(product, 3)
        assert cart.products[product] == 5  # Count should be updated

    def test_remove_product(self, cart, product):
        cart.add_product(product, 5)
        cart.remove_product(product, 2)
        assert cart.products[product] == 3

    def test_remove_product_completely(self, cart, product):
        cart.add_product(product, 5)
        cart.remove_product(product)
        assert product not in cart.products  # Product should be removed completely

    def test_clear_cart(self, cart, product):
        cart.add_product(product, 5)
        cart.clear()
        assert len(cart.products) == 0  # Cart should be empty

    def test_get_total_price(self, cart, product):
        cart.add_product(product, 3)
        assert cart.get_total_price() == 300  # 3 books at 100 each

    def test_buy_success(self, cart, product):
        cart.add_product(product, 2)
        assert product.quantity == 1000  # Initial quantity
        cart.buy()
        assert product.quantity == 998  # Quantity after purchase
        assert len(cart.products) == 0  # Cart should be empty after purchase

    def test_buy_insufficient_stock(self, cart, product):
        cart.add_product(product, 1001)  # More than available
        with pytest.raises(ValueError, match='Товара недостаточно'):
            cart.buy()  # Should raise an error due to insufficient stock
