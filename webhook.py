import os
import stripe
from fastapi import FastAPI, Request, Header, HTTPException
from supabase import create_client
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta

load_dotenv()

# Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

# Supabase (SERVICE KEY)
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")
)

app = FastAPI()


def ts(unix_ts):
    """Convert Stripe timestamp → ISO UTC"""
    if not unix_ts:
        return None
    return datetime.fromtimestamp(unix_ts, tz=timezone.utc).isoformat()


@app.post("/webhook")
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None)
):
    payload = await request.body()

    try:
        event = stripe.Webhook.construct_event(
            payload,
            stripe_signature,
            endpoint_secret
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    event_type = event["type"]
    subscription = event["data"]["object"]

    # ---------------------------------------------------
    # SUBSCRIPTION CREATED
    # ---------------------------------------------------
    if event_type == "customer.subscription.created":
        user_id = subscription.get("metadata", {}).get("user_id")

        if not user_id:
            return {"status": "ignored", "reason": "no user_id"}

        supabase.table("profiles").update({
            "plan": "premium",
            "is_premium": True,
            "stripe_subscription_id": subscription.get("id"),
            "stripe_customer_id": subscription.get("customer"),
            "subscription_start": datetime.now(timezone.utc).isoformat(),
            "subscription_end": (
                datetime.now(timezone.utc) + timedelta(days=30)
            ).isoformat(),
            "subscription_status": True,
        }).eq("user_id", user_id).execute()

    # ---------------------------------------------------
    # SUBSCRIPTION UPDATED
    # ---------------------------------------------------
    elif event_type == "customer.subscription.updated":
        is_active = subscription.get("status") == "active"
        cancel_at_period_end = subscription.get("cancel_at_period_end", False)

        update_data = {
            "is_premium": is_active,
        }

        # Mise à jour des dates UNIQUEMENT si pas d'annulation prévue
        if is_active and not cancel_at_period_end:
            start_ts = subscription.get("current_period_start")
            end_ts = subscription.get("current_period_end")

            if start_ts:
                update_data["subscription_start"] = ts(start_ts)
            if end_ts:
                update_data["subscription_end"] = ts(end_ts)

        # Annulation programmée
        if cancel_at_period_end:
            update_data["subscription_status"] = False

        supabase.table("profiles").update(update_data).eq(
            "stripe_subscription_id",
            subscription.get("id")
        ).execute()

    # ---------------------------------------------------
    # SUBSCRIPTION DELETED (fin réelle)
    # ---------------------------------------------------
    elif event_type == "customer.subscription.deleted":
        supabase.table("profiles").update({
            "subscription_status": False,
            "is_premium": False,
        }).eq(
            "stripe_subscription_id",
            subscription.get("id")
        ).execute()

    return {"status": "ok"}
