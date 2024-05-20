from datetime import datetime, timedelta

from infrastructure.api.dto.dto_cart import (
    CartRequest,
    CartResponse,
    CartItemResponse,
    RefundRequest,
)
from infrastructure.api.dto.dto_smtp import EmailRequest
from models.product_models import Product
from models.cart_models import Cart
from models.order_models import OrderPassed, OrderStatus
from models.users_models import User
from domain.ecommerce.use_case.smtp import send_email_logic
from domain.ecommerce.exceptions.exceptions import (
    ProductNotFoundException,
    UserNotFoundException,
    StockNotFoundException,
    CartNotFoundException,
    NoOrderException,
    CartEmptyException,
    OrderNotFoundException,
    UnauthorizedException,
    OrderCancellationException,
    OrderRefundException,
    ItemNotFoundException,
)


async def add_to_cart_logic(item: CartRequest, current_user) -> CartResponse:
    buyer_id = current_user.id
    user = await User.objects().where(User.id == buyer_id).first().run()
    if user is None:
        raise UserNotFoundException("User not found")

    product = await Product.objects().where(Product.id == item.product_id).first().run()
    if product is None:
        raise ProductNotFoundException("Product not found")
    if product.stock < item.quantity:
        raise StockNotFoundException("Stock insuffisant")

    product.stock -= item.quantity
    await product.save().run()

    cart = Cart(
        buyer_id=buyer_id,
        product_id=item.product_id,
        quantity=item.quantity,
        total=int(product.price) * item.quantity,
        created_at=datetime.now(),
    )

    await cart.save().run()

    return CartResponse(
        id=cart.id,
        buyer_id=cart.buyer_id,
        items=[item],
        total=cart.total,
        created_at=cart.created_at,
        promotional_code=cart.promotional_code,
    )


async def get_cart_logic(current_user):
    user_id = current_user.id
    cart = await Cart.objects().where(Cart.buyer_id == user_id).first().run()
    if cart is None:
        raise CartNotFoundException("Cart not found")
    items = await Cart.objects().where(Cart.buyer_id == user_id).run()
    items_response = [
        CartItemResponse(
            product_id=item.product_id if item.product_id is not None else 0,
            quantity=item.quantity,
            promotional_code=cart.promotional_code,
        ).dict()
        for item in items
    ]
    return {
        "id": cart.id,
        "buyer_id": cart.buyer_id,
        "items": items_response,
        "total": cart.total,
        "created_at": cart.created_at,
        "promotional_code": cart.promotional_code,
    }


async def get_past_orders_logic(current_user):
    user_id = current_user.id
    orders = await OrderPassed.objects().where(OrderPassed.buyer_id == user_id).run()
    if not orders:
        raise NoOrderException(
            "Aucune commande trouvée",
        )
    return orders


async def checkout_logic(current_user):
    user_id = current_user.id
    cart_items = await Cart.objects().where(Cart.buyer_id == user_id).run()

    if not cart_items:
        raise CartEmptyException("Cart is empty")

    order_summary = "Order Summary:\n"
    total = 0
    for cart_item in cart_items:
        product = (
            await Product.objects()
            .where(Product.id == cart_item.product_id)
            .first()
            .run()
        )
        if product is not None:
            product.stock -= cart_item.quantity
            await product.save().run()
            total += cart_item.total
            order_summary += (
                f"Product: {product.name}, Quantity: {cart_item.quantity}\n"
            )
        await cart_item.delete(force=True).run()

    order = OrderPassed(
        buyer_id=user_id,
        status=OrderStatus.delivering,
        delivery_date=datetime.now() + timedelta(days=3),
        total=total,
    )
    await order.save().run()
    # email_request = EmailRequest(
    #     receiver_email=current_user.email,
    #     subject="Order Summary",
    #     body=f"Hello {current_user.username},\n\n{order_summary}\n\nYour order will be delivered by {order.delivery_date}.",
    # )
    # await send_email(email_request)
    return {"message": "Checkout successful, cart cleared"}


async def mark_order_as_received_logic(order_id: int, current_user):
    order = await OrderPassed.objects().where(OrderPassed.id == order_id).first().run()
    if order is None:
        raise OrderNotFoundException("Order not found")
    if order.buyer_id != current_user.id:
        raise UnauthorizedException("Not authorized")

    order.status = OrderStatus.delivered
    await order.save().run()

    email_request = EmailRequest(
        receiver_email=current_user.email,
        subject="We value your feedback",
        body=f"Hello {current_user.username},\n\nWe noticed that you received your order. We would love to hear your thoughts on the products you purchased. Please add your review at http://localhost:8000/docs#/reviews.\n\nThank you for your time.",
    )
    await send_email_logic(email_request)

    return {"message": "Order marked as received"}


async def cancel_order_logic(order_id: int, current_user):
    order = await OrderPassed.objects().where(OrderPassed.id == order_id).first().run()
    if order is None:
        raise OrderNotFoundException("Order not found")
    if order.buyer_id != current_user.id:
        raise UnauthorizedException("Not authorized")

    if order.status != OrderStatus.delivering:
        raise OrderCancellationException("Order cannot be cancelled")

    order.status = OrderStatus.cancelled
    await order.save().run()

    return {"message": "Order cancelled successfully"}


async def refund_order_logic(
    order_id: int, refund_request: RefundRequest, current_user
):
    order = await OrderPassed.objects().where(OrderPassed.id == order_id).first().run()
    if order is None:
        raise OrderNotFoundException("Order not found")
    if order.buyer_id != current_user.id:
        raise UnauthorizedException("Not authorized")

    if order.status != OrderStatus.delivered:
        raise OrderRefundException("Order cannot be refunded")

    for product_id in refund_request.product_ids:
        product = await Product.objects().where(Product.id == product_id).first().run()
        if product is None:
            raise ProductNotFoundException(f"Product with id {product_id} not found")

    return {"message": "Refund request received, we will process it shortly"}


async def remove_from_cart_logic(item_index: int, current_user):
    carts = {}
    user_id = current_user.id
    if user_id not in carts:
        raise CartNotFoundException("Cart not found")
    if item_index >= len(carts[user_id].items) or item_index < 0:
        raise ItemNotFoundException("Item not found in cart")
    del carts[user_id].items[item_index]
    return carts[user_id]


async def clear_cart_logic(current_user):
    user_id = current_user.id
    cart_items = await Cart.objects().where(Cart.buyer_id == user_id).run()
    for cart_item in cart_items:
        await cart_item.delete(force=True).run()

    return {"message": "Cart cleared successfully"}
