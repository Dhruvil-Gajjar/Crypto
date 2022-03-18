from subscription.models import OrderHistory


def create_order_history(queryset, subscription, product):
    try:
        for obj in queryset:
            OrderHistory.objects.create(
                user=obj.user,
                stripeCustomerId=obj.stripeCustomerId,
                stripeSubscriptionId=obj.stripeSubscriptionId,
                productName=product.name,
                subscriptionStartDate=subscription.current_period_start,
                subscriptionEndDate=subscription.current_period_end,
                order_created_at=obj.created_at
            )
    except Exception as e:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>> Error in creating order history")
        print(e)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>> Error in creating order history")
