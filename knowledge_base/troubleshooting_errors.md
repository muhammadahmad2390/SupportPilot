# Troubleshooting & Error Codes

## Account & Login Errors

**ERR-101: Invalid credentials**
User entered an incorrect email/password combination. Direct to password reset if repeated failures occur.

**ERR-102: Account locked**
Triggered after 5 failed login attempts within 15 minutes. Lock lifts automatically after 30 minutes, or support can manually unlock after identity verification.

**ERR-103: Email not verified**
Account was created but the verification email was never confirmed. Resend verification email; check spam folder if not received within 10 minutes.

## Checkout & Payment Errors

**ERR-201: Payment declined**
Generic decline from the payment processor. Ask customer to verify card details, try an alternate payment method, or contact their bank.

**ERR-202: Address verification failed**
Billing address does not match the card issuer's records. Customer should re-enter the address exactly as it appears on their bank statement.

**ERR-203: Promo code invalid or expired**
Code does not exist, has expired, or has already been used by this account.

**ERR-204: Cart session expired**
Checkout session timed out after 20 minutes of inactivity. Customer needs to re-add items and retry.

## Order Processing Errors

**ERR-301: Inventory conflict**
Item was in stock when ordered but became unavailable before processing completed (rare, occurs with simultaneous high-demand orders). Customer is notified automatically and offered a substitute or refund.

**ERR-302: Duplicate order detected**
System flagged two orders placed within 60 seconds with identical contents and shipping address. One is automatically held pending customer confirmation to prevent accidental double charges.

**ERR-303: Shipping address undeliverable**
Carrier's address validation API rejected the address format. Support should confirm the correct address with the customer before manually releasing the order.

## App/Website Technical Issues

**Page won't load / blank screen**
Ask customer to clear cache, try a different browser, or check the app version is up to date. Escalate to engineering if the issue is reproducible and affects multiple users.

**Order history not showing recent orders**
Usually a caching delay of up to 15 minutes after order placement. If still missing after that, check if the order was placed under a different account or as a guest checkout.
