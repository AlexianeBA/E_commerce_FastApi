from datetime import datetime, timedelta
from fastapi import HTTPException, status
from infrastructure.api.dto.dto_cart import (
    CartRequest,
    CartResponse,
    CartItemResponse,
    RefundRequest,
)
from infrastructure.api.dto.dto_smtp import EmailRequest
from models import Product, Cart, OrderPassed, OrderStatus, User
from domain.ecommerce.use_case.smtp import send_email_logic


async def add_to_cart_logic(item: CartRequest, current_user) -> CartResponse:
    buyer_id = current_user.id
    user = await User.objects().where(User.id == buyer_id).first().run()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    product = await Product.objects().where(Product.id == item.product_id).first().run()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.stock < item.quantity:
        raise HTTPException(status_code=400, detail="Stock insuffisant")

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
        raise HTTPException(status_code=404, detail="Cart not found")
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
        raise HTTPException(
            status_code=400,
            detail="Aucune commande trouvée",
        )
    return orders


async def checkout_logic(current_user):
    user_id = current_user.id
    cart_items = await Cart.objects().where(Cart.buyer_id == user_id).run()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

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
    email_request = EmailRequest(
        receiver_email=current_user.email,
        subject="Order Summary",
        body=f"Hello {current_user.username},\n\n{order_summary}\n\nYour order will be delivered by {order.delivery_date}.",
    )
    # await send_email(email_request)
    return {"message": "Checkout successful, cart cleared"}


async def mark_order_as_received_logic(order_id: int, current_user):
    order = await OrderPassed.objects().where(OrderPassed.id == order_id).first().run()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.buyer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

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
        raise HTTPException(status_code=404, detail="Order not found")
    if order.buyer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    if order.status != OrderStatus.delivering:
        raise HTTPException(status_code=400, detail="Order cannot be cancelled")

    order.status = OrderStatus.cancelled
    await order.save().run()

    return {"message": "Order cancelled successfully"}


async def refund_order_logic(
    order_id: int, refund_request: RefundRequest, current_user
):
    order = await OrderPassed.objects().where(OrderPassed.id == order_id).first().run()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.buyer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    if order.status != OrderStatus.delivered:
        raise HTTPException(status_code=400, detail="Order cannot be refunded")

    for product_id in refund_request.product_ids:
        product = await Product.objects().where(Product.id == product_id).first().run()
        if product is None:
            raise HTTPException(
                status_code=404, detail=f"Product with id {product_id} not found"
            )

    return {"message": "Refund request received, we will process it shortly"}


async def remove_from_cart_logic(item_index: int, current_user):
    carts = {}
    user_id = current_user.id
    if user_id not in carts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found"
        )
    if item_index >= len(carts[user_id].items) or item_index < 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found in cart"
        )
    del carts[user_id].items[item_index]
    return carts[user_id]


async def clear_cart_logic(current_user):
    user_id = current_user.id
    cart_items = await Cart.objects().where(Cart.buyer_id == user_id).run()
    for cart_item in cart_items:
        await cart_item.delete(force=True).run()

    return {"message": "Cart cleared successfully"}
