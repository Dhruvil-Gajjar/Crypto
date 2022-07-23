from project.celery import app
from subscription.models import OrderHistory


@app.task()
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

        queryset.delete()
    except Exception as e:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>> Error in creating order history")
        print(e)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>> Error in creating order history")
