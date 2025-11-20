"""
Sales tools for the Beer Tasting Agent.

Provides tools for generating discount codes and managing sales.
"""
import logging
import random
from strands import tool

logger = logging.getLogger(__name__)


@tool
def generate_discount_code(user_name: str = "Cliente", earned_discount: bool = True) -> dict:
    """
    Genera un código de descuento personalizado para incentivar la compra.
    
    Esta herramienta crea un código de descuento único. El porcentaje varía según
    si el usuario completó el proceso de cata/compra guiada o solo pidió un código.
    
    Args:
        user_name: Nombre del usuario para personalizar el código (opcional)
        earned_discount: True si completó cata/proceso (10-19%), False si solo pidió código (5%)
        
    Returns:
        Dictionary containing:
            - code: El código de descuento generado
            - discount_percentage: El porcentaje de descuento
            - message: Mensaje personalizado para el usuario
    """
    try:
        # Determinar porcentaje según si se ganó el descuento
        if earned_discount:
            # Usuario completó cata o proceso de compra guiada: 10-19%
            discount = random.randint(10, 19)
        else:
            # Usuario solo pidió código sin hacer proceso: 5% fijo
            discount = 5
        
        # Generar código único basado en el nombre y un número aleatorio
        name_part = user_name[:3].upper() if user_name != "Cliente" else "VIP"
        random_part = random.randint(1000, 9999)
        code = f"FORTUNA{discount}-{name_part}{random_part}"
        
        logger.info(f"Generated discount code: {code} with {discount}% off (earned: {earned_discount})")
        
        return {
            "success": True,
            "code": code,
            "discount_percentage": discount,
            "earned": earned_discount,
            "message": f"¡Código especial generado! Usa {code} para obtener {discount}% de descuento en tu compra."
        }
    
    except Exception as e:
        logger.error(f"Failed to generate discount code: {e}")
        return {
            "success": False,
            "error": "Failed to generate code",
            "message": str(e)
        }


@tool
def process_purchase_assistance(
    user_name: str,
    beers: list,
    discount_code: str = None
) -> dict:
    """
    Simula el proceso de asistencia de compra para el usuario.
    
    Esta herramienta ayuda al usuario a completar su compra proporcionando
    un resumen del pedido, enlaces directos y confirmación simulada.
    
    Args:
        user_name: Nombre del usuario
        beers: Lista de nombres de cervezas que el usuario quiere comprar
        discount_code: Código de descuento si aplica (opcional)
        
    Returns:
        Dictionary containing:
            - order_id: ID de orden simulado
            - beers: Lista de cervezas en el pedido
            - purchase_links: Enlaces directos de compra
            - total_items: Total de items
            - discount_applied: Si se aplicó descuento
            - message: Mensaje de confirmación
    """
    try:
        # Generar ID de orden simulado
        order_id = f"FORT-{random.randint(10000, 99999)}"
        
        # Crear enlaces de compra para cada cerveza
        base_url = "https://cervezafortuna.com"
        purchase_links = {}
        
        # Mapeo de nombres de cervezas a URLs (simplificado)
        beer_urls = {
            "ippolita": f"{base_url}/producto/ippolita/",
            "pale ale": f"{base_url}/producto/pale-ale/",
            "california ale": f"{base_url}/producto/california-ale/",
            "oat stout": f"{base_url}/producto/oat-stout/",
            "neippolita": f"{base_url}/producto/neippolita/",
            "hazy pale ale": f"{base_url}/producto/hazy-pale-ale/",
            "sake ale": f"{base_url}/producto/sake-ale/",
        }
        
        for beer in beers:
            beer_lower = beer.lower()
            for key, url in beer_urls.items():
                if key in beer_lower:
                    purchase_links[beer] = url
                    break
            if beer not in purchase_links:
                # URL genérica si no se encuentra
                purchase_links[beer] = f"{base_url}/inicio/cervezas/"
        
        logger.info(f"Purchase assistance processed for {user_name}: {len(beers)} beers")
        
        return {
            "success": True,
            "order_id": order_id,
            "beers": beers,
            "purchase_links": purchase_links,
            "total_items": len(beers),
            "discount_applied": discount_code is not None,
            "discount_code": discount_code,
            "message": f"¡Perfecto, {user_name}! Tu pedido está listo para procesar."
        }
    
    except Exception as e:
        logger.error(f"Failed to process purchase assistance: {e}")
        return {
            "success": False,
            "error": "Purchase assistance failed",
            "message": str(e)
        }


@tool
def collect_shipping_info(
    full_name: str,
    email: str,
    phone: str,
    address: str,
    city: str,
    state: str,
    postal_code: str
) -> dict:
    """
    Recolecta y valida la información de envío del cliente.
    
    Esta herramienta almacena los datos de envío del cliente para procesar
    la compra. Valida que todos los campos requeridos estén presentes.
    
    Args:
        full_name: Nombre completo del cliente
        email: Correo electrónico
        phone: Número de teléfono
        address: Dirección completa (calle y número)
        city: Ciudad
        state: Estado
        postal_code: Código postal
        
    Returns:
        Dictionary containing:
            - success: Si la información fue recolectada exitosamente
            - shipping_info: Datos de envío validados
            - message: Mensaje de confirmación
    """
    try:
        # Validaciones básicas
        if not full_name or len(full_name) < 3:
            return {
                "success": False,
                "error": "Nombre inválido",
                "message": "El nombre debe tener al menos 3 caracteres"
            }
        
        if not email or "@" not in email:
            return {
                "success": False,
                "error": "Email inválido",
                "message": "Por favor proporciona un email válido"
            }
        
        if not phone or len(phone) < 10:
            return {
                "success": False,
                "error": "Teléfono inválido",
                "message": "El teléfono debe tener al menos 10 dígitos"
            }
        
        if not address or len(address) < 5:
            return {
                "success": False,
                "error": "Dirección inválida",
                "message": "Por favor proporciona una dirección completa"
            }
        
        shipping_info = {
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "address": address,
            "city": city,
            "state": state,
            "postal_code": postal_code
        }
        
        logger.info(f"Shipping info collected for {full_name}")
        
        return {
            "success": True,
            "shipping_info": shipping_info,
            "message": f"Información de envío confirmada para {full_name}"
        }
    
    except Exception as e:
        logger.error(f"Failed to collect shipping info: {e}")
        return {
            "success": False,
            "error": "Failed to collect info",
            "message": str(e)
        }


@tool
def generate_payment_link(
    order_id: str,
    customer_name: str,
    customer_email: str,
    items: list,
    total_amount: float,
    discount_code: str = None
) -> dict:
    """
    Genera un link de pago simulado de Stripe para completar la compra.
    
    Esta herramienta crea un link de pago simulado que el cliente puede usar
    para completar su compra. En producción, esto se conectaría con Stripe real.
    
    Args:
        order_id: ID único de la orden
        customer_name: Nombre del cliente
        customer_email: Email del cliente
        items: Lista de items en la orden
        total_amount: Monto total a pagar
        discount_code: Código de descuento aplicado (opcional)
        
    Returns:
        Dictionary containing:
            - success: Si el link fue generado exitosamente
            - payment_link: URL del link de pago de Stripe (simulado)
            - order_id: ID de la orden
            - amount: Monto total
            - expires_in: Tiempo de expiración del link
            - message: Mensaje de confirmación
    """
    try:
        # Generar un ID de sesión de Stripe simulado
        session_id = f"cs_test_{random.randint(100000000000, 999999999999)}"
        
        # Crear link de pago simulado de Stripe
        payment_link = f"https://checkout.stripe.com/c/pay/{session_id}"
        
        logger.info(f"Payment link generated for order {order_id}: {payment_link}")
        
        return {
            "success": True,
            "payment_link": payment_link,
            "order_id": order_id,
            "customer_name": customer_name,
            "customer_email": customer_email,
            "items": items,
            "amount": total_amount,
            "currency": "MXN",
            "discount_code": discount_code,
            "expires_in": "24 horas",
            "message": f"Link de pago generado exitosamente para {customer_name}"
        }
    
    except Exception as e:
        logger.error(f"Failed to generate payment link: {e}")
        return {
            "success": False,
            "error": "Failed to generate payment link",
            "message": str(e)
        }
