"""
Test para las nuevas herramientas de ventas.
"""

from tools.sales_tools import (
    collect_shipping_info,
    generate_payment_link
)


def test_collect_shipping_info():
    """Test de recolección de información de envío."""
    print("\n=== Test: collect_shipping_info ===")
    
    result = collect_shipping_info(
        full_name="David Victoria",
        email="david@example.com",
        phone="5512345678",
        address="Calle Falsa 123, Col. Centro",
        city="Ciudad de México",
        state="CDMX",
        postal_code="01000"
    )
    
    print(f"✓ Success: {result['success']}")
    print(f"✓ Message: {result['message']}")
    print(f"✓ Shipping Info: {result['shipping_info']}")
    
    assert result['success'] == True
    assert result['shipping_info']['full_name'] == "David Victoria"
    assert result['shipping_info']['email'] == "david@example.com"
    
    print("✓ Test passed!\n")


def test_generate_payment_link():
    """Test de generación de link de pago."""
    print("\n=== Test: generate_payment_link ===")
    
    result = generate_payment_link(
        order_id="FORT-12345",
        customer_name="David Victoria",
        customer_email="david@example.com",
        items=["Sake Ale - 12 Pack"],
        total_amount=433.44,
        discount_code="FORTUNA14-DAV5437"
    )
    
    print(f"✓ Success: {result['success']}")
    print(f"✓ Payment Link: {result['payment_link']}")
    print(f"✓ Order ID: {result['order_id']}")
    print(f"✓ Amount: ${result['amount']} {result['currency']}")
    print(f"✓ Expires in: {result['expires_in']}")
    
    assert result['success'] == True
    assert "checkout.stripe.com" in result['payment_link']
    assert result['amount'] == 433.44
    assert result['currency'] == "MXN"
    
    print("✓ Test passed!\n")


def test_invalid_email():
    """Test de validación de email inválido."""
    print("\n=== Test: invalid email ===")
    
    result = collect_shipping_info(
        full_name="David Victoria",
        email="invalid-email",  # Email sin @
        phone="5512345678",
        address="Calle Falsa 123",
        city="CDMX",
        state="CDMX",
        postal_code="01000"
    )
    
    print(f"✓ Success: {result['success']}")
    print(f"✓ Error: {result['error']}")
    print(f"✓ Message: {result['message']}")
    
    assert result['success'] == False
    assert "email" in result['error'].lower()
    
    print("✓ Test passed!\n")


def test_earned_discount():
    """Test de descuento ganado (10-19%)."""
    print("\n=== Test: earned discount (10-19%) ===")
    
    from tools.sales_tools import generate_discount_code
    
    result = generate_discount_code(
        user_name="David",
        earned_discount=True
    )
    
    print(f"✓ Success: {result['success']}")
    print(f"✓ Code: {result['code']}")
    print(f"✓ Discount: {result['discount_percentage']}%")
    print(f"✓ Earned: {result['earned']}")
    
    assert result['success'] == True
    assert result['discount_percentage'] >= 10
    assert result['discount_percentage'] <= 19
    assert result['earned'] == True
    
    print("✓ Test passed!\n")


def test_basic_discount():
    """Test de descuento básico (5%)."""
    print("\n=== Test: basic discount (5%) ===")
    
    from tools.sales_tools import generate_discount_code
    
    result = generate_discount_code(
        user_name="María",
        earned_discount=False
    )
    
    print(f"✓ Success: {result['success']}")
    print(f"✓ Code: {result['code']}")
    print(f"✓ Discount: {result['discount_percentage']}%")
    print(f"✓ Earned: {result['earned']}")
    
    assert result['success'] == True
    assert result['discount_percentage'] == 5
    assert result['earned'] == False
    
    print("✓ Test passed!\n")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Testing New Sales Tools")
    print("="*60)
    
    try:
        test_collect_shipping_info()
        test_generate_payment_link()
        test_invalid_email()
        test_earned_discount()
        test_basic_discount()
        
        print("="*60)
        print("✓ All tests passed!")
        print("="*60 + "\n")
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}\n")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}\n")
        import traceback
        traceback.print_exc()
