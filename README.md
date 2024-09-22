# UnitedPayment API Integration Package

A Python package for integrating with the UnitedPayment API, allowing easy access to payment functionalities like checkout, card registration, transaction status, and more.

## Features

- Checkout processing
- Card registration
- Transaction status inquiries
- Refunds and reversals
- Recurring payments
- Installment options
- Customer card management
- Payment by link with QR code

## Installation

You can install the package via pip. Run the following command:

```bash
pip install united-payment
```

## Usage

To use the UnitedPayment API package, first import the main class and initialize it with your credentials:

```python
from united_payment.client import UnitedPaymentAPI, Language, Currency

# Initialize the API client
api = UnitedPaymentAPI(
    base_url='https://test-vpos.unitedpayment.az/api',
    email='support@unitedpayment.com',
    password='Testmerchant12!'
)
```

### Example: Checkout

Here's how to perform a checkout:

```python
response = api.checkout(
    amount='100',
    language=Language.EN,
    success_url='https://success.url',
    cancel_url='https://cancel.url',
    decline_url='https://decline.url',
    currency=Currency.AZN
)
print(response)
```

## Documentation

For detailed API documentation, refer to the following link: [UnitedPayment API Documentation](https://documenter.getpostman.com/view/17619441/2s83ziP4Yc#08f68b71-b2de-4c56-b76d-6b554a3b885f)

## Testing

To run the tests, use the following command:

```bash
python -m unittest discover -s tests
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.
