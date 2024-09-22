import requests
from datetime import datetime, timedelta
from united_payment.exceptions import UnitedPaymentAPIException
from united_payment.constants import Language, Currency


error_codes = UnitedPaymentAPIException.error_codes


class UnitedPaymentAPI:

    '''
    Client class for interacting with the United Payment API.

    Attributes:
        base_url (str): Base URL for the API.
        email (str): Email address for authentication.
        password (str): Password for authentication.
        token (str, optional): Access token obtained after login (initially None).
        token_expiry (datetime, optional): Expiry time of the token (initially None).

    Raises:
        UnitedPaymentException: Exception for general API errors.
    '''

    def __init__(self, base_url: str, email: str, password: str):
        '''
        Initializes the UnitedPaymentAPI client.

        Args:
            base_url (str): Base URL for the API.
            email (str): Email address to authenticate.
            password (str): Password to authenticate.
        '''

        self.base_url = base_url
        self.email = email
        self.password = password
        self.token = None
        self.token_expiry = None
        self.login()

    def login(self) -> None:
        '''
        Authenticate and retrieve token, setting the token and its expiry time.

        Raises:
            UnitedPaymentAPIException: If login fails.
        '''

        login_url = f'{self.base_url}/auth/'
        headers = {'Content-Type': 'application/json'}
        data = {
            'email': self.email,
            'password': self.password
        }

        response = requests.post(login_url, headers=headers, json=data)

        if response.status_code == 200:
            self.token = response.json().get('token')
            self.token_expiry = datetime.now() + timedelta(minutes=57)
        else:
            raise UnitedPaymentAPIException(
                'Failed to login and retrieve token.'
            )

    def is_token_expired(self) -> bool:
        '''
        Check if the token has expired.

        Returns:
            bool: True if the token is expired, False otherwise.
        '''
        if self.token_expiry is None:
            return True
        return datetime.now() >= self.token_expiry

    def update_token(self):
        '''
        Refresh the token if it is expired.
        '''
        if self.is_token_expired():
            self.login()

    def set_headers(self) -> dict[str, str]:
        '''Set headers for the API requests.'''

        if not self.token:
            self.update_token()
        return {
            'x-auth-token': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

    def parse_response(self, response: requests.Response) -> dict[str, str]:
        '''
        Parse the text response from the API.

        Args:
            response (requests.Response): The response object.

        Returns:
            Dict[str, str]: Parsed response as a dictionary.
        '''
        result = response.text.strip()
        parsed_result = {}
        for line in result.split('\n'):
            if ': ' in line:
                key, value = line.split(': ', 1)
                parsed_result[key.strip()] = value.strip()
        return parsed_result

    def handle_response_errors(self, response: requests.Response) -> None:
        '''
        Handle API response and convert error codes to readable messages.

        Args:
            response (requests.Response): The response object.

        Raises:
            UnitedPaymentAPIException: If an error code is found in the response.
        '''

        if response.status_code != 200:
            try:
                response_data = response.json()
                if response_data is dict:
                    error_code = response_data.get(
                        'errorCode') or response_data.get('error')
                    if error_code in error_codes:
                        raise UnitedPaymentAPIException(
                            f"Error {error_code}: {error_codes[error_code]}")
            except ValueError:
                print(UnitedPaymentAPIException(
                    f'Failed to process response: {response.text or "Empty response"}'))

    def make_request(self, endpoint: str, data: dict, method: str) -> dict:
        '''
        Make an authenticated request to the API and handle response parsing and errors.

        Args:
            endpoint (str, required): The API endpoint to request.
            data (dict, required): Payload for POST requests or parameters for GET requests.
            method (str, required): HTTP method to use (GET, POST).

        Returns:
            dict[str,str]: Parsed response from the API.

        Raises:
            UnitedPaymentAPIException: If the request fails or an error is encountered.
        '''

        self.update_token()

        url = f"{self.base_url}{endpoint}"
        headers = self.set_headers()

        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers, params=data)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=headers, json=data)

            self.handle_response_errors(response)
            return self.parse_response(response)
        except requests.RequestException as e:
            raise UnitedPaymentAPIException(f'Request failed: {str(e)}')

    def checkout(self, amount: str, language: Language, success_url: str, cancel_url: str,  decline_url: str, client_order_id: str | None = None, description: str | None = None, member_id: str | None = None, additional_information: str | None = None, email: str | None = None, phone_number: str | None = None, client_name: str | None = None, currency: Currency | None = None, partner_id: str | None = None) -> dict[str, str]:
        '''
        Perform a checkout transaction.

        Args:
            client_order_id (str): Your transaction ID. Must be sent for CheckStatus and countermeasures. (optional)
            amount (str) : Amount. (required*)
            language (Language) : Setting the payment page language from the Language enum. (required*)
            success_url (str) : If the payment is successful, your URL will be redirected with the Get method. (required*)
            cancel_url (str) : Your URL will be redirected with the Get method when payment is refused. (required*)
            decline_url (str) : Your URL will be redirected with the Get method if the payment fails. (required*)
            description (str) : A statement about the operation. It will be reflected on the dashboard that will be given to you. (optional)
            member_id (str) : The unique ID of your customers. Services such as card memorization must be sent if they are to be used. (optional)
            additional_information (str) : Additional information about the transaction. It will be reflected on the dashboard that will be given to you. (optional)
            email (str) : Additional information of the customer. It will be reflected on the dashboard that will be given to you. (optional)
            phone_number (str) : Additional information of the customer. It will be reflected on the dashboard that will be given to you. (optional)
            client_name (str) : Additional information of the customer. It will be reflected on the dashboard that will be given to you. (optional)
            currency (Currency) : The currency code from the Currency enum. (optional)
            partner_id (str) : If the SubMerchant structure is used, the merchant's ID will be given to you beforehand. (optional)

        Returns:
            dict[str, str]: Parsed response as a dictionary.

        Raises:
            UnitedPaymentAPIException: If the request fails or an error is encountered.
        '''

        data = {
            'amount': amount,
            'language': language.value,
            'successUrl': success_url,
            'cancelUrl': cancel_url,
            'declineUrl': decline_url
        }

        if client_order_id:
            data['clientOrderId'] = client_order_id
        if description:
            data['description'] = description
        if member_id:
            data['memberId'] = member_id
        if additional_information:
            data['additionalInformation'] = additional_information
        if email:
            data['email'] = email
        if phone_number:
            data['phoneNumber'] = phone_number
        if client_name:
            data['clientName'] = client_name
        if currency:
            data['currency'] = currency.value
        if partner_id:
            data['partnerId'] = partner_id

        return self.make_request(endpoint='/transactions/checkout', data=data, method='POST')

    def card_registration(self, language: Language, success_url: str, cancel_url: str, decline_url: str, client_order_id: str | None = None, member_id: str | None = None,) -> dict[str, str]:
        '''
        Register a card for future use.

        Args:
            client_order_id (str): Your transaction ID. Must be sent for CheckStatus and countermeasures. (optional)
            language (Language) : Setting the payment page language from the Language enum. (required*)
            member_id (str) - The unique ID of your customers. Services such as card memorization must be sent if they are to be used. (optional)
            success_url (str): If the payment is successful, your URL will be redirected with the Get method. (required*)
            cancel_url (str): Your URL will be redirected with the Get method when payment is refused. (required*)
            decline_url (str): Your URL will be redirected with the Get method if the payment fails. (required*)

        Returns:
            dict[str, str]: Parsed response as a dictionary.

        Raises:
            UnitedPaymentAPIException: If the request fails or an error is encountered.
        '''

        data = {
            'language': language.value,
            'successUrl': success_url,
            'cancelUrl': cancel_url,
            'declineUrl': decline_url
        }

        if client_order_id:
            data['clientOrderId'] = client_order_id
        if member_id:
            data['memberId'] = member_id

        return self.make_request(endpoint='/transactions/card-registration', data=data, method='POST')

    def purchase_with_saved_card_3ds(self, amount: str, card_uid: str, language: Language, success_url: str, cancel_url: str, decline_url: str, client_order_id: str | None = None, member_id: str | None = None,) -> dict[str, str]:
        '''
        Purchase with a saved card.

        Args:
            client_order_id (str): Your transaction ID. Must be sent for CheckStatus and countermeasures. (optional)
            amount (str) : Amount. (required*)
            member_id (str) : The unique ID of your customers. Services such as card memorization must be sent if they are to be used. (optional)
            card_uid (str) : (Unique Identifier) is a unique identifier assigned to a payment card. (required*)
            language (Language) : Setting the payment page language from the Language enum. (required*)
            success_url (str) - If the payment is successful, your URL will be redirected with the Get method. (required*)
            cancel_url (str) - Your URL will be redirected with the Get method when payment is refused. (required*)
            decline_url (str) - Your URL will be redirected with the Get method if the payment fails. (required*)

        Returns:
            dict[str, str]: Parsed response as a dictionary.

        Raises:
            UnitedPaymentAPIException: If the request fails or an error is encountered.
        '''

        data = {
            'amount': amount,
            'cardUID': card_uid,
            'language': language.value,
            'successUrl': success_url,
            'cancelUrl': cancel_url,
            'declineUrl': decline_url
        }

        if client_order_id:
            data['clientOrderId'] = client_order_id
        if member_id:
            data['memberId'] = member_id

        return self.make_request(endpoint='/transactions/purchase-with-saved-card-3ds', data=data, method='POST')

    def card_registration_recurring(self, success_url: str, cancel_url: str, decline_url: str, client_order_id: str | None = None, member_id: str | None = None, language: Language | None = None) -> dict[str, str]:
        '''
        Register a card for recurring payments.

        Args:
            client_order_id (str): Your transaction ID. Must be sent for CheckStatus and countermeasures. (optional)
            language (Language) : Setting the payment page language from the Language enum. (optional)
            member_id (str) : The unique ID of your customers. Services such as card memorization must be sent if they are to be used. (optional)
            success_url (str) - If the payment is successful, your URL will be redirected with the Get method. (required*)
            cancel_url (str) - Your URL will be redirected with the Get method when payment is refused. (required*)
            decline_url (str) - Your URL will be redirected with the Get method if the payment fails. (required*)

        Returns:
            dict[str, str]: Parsed response as a dictionary.

        Raises:
            UnitedPaymentAPIException: If the request fails or an error is encountered.
        '''

        data = {
            'successUrl': success_url,
            'cancelUrl': cancel_url,
            'declineUrl': decline_url
        }

        if client_order_id:
            data['clientOrderId'] = client_order_id
        if member_id:
            data['memberId'] = member_id
        if language:
            data['language'] = language.value

        return self.make_request(endpoint='/transactions/card-registration-recurring', data=data, method='POST')

    def purchase_with_saved_card_recurring(self, amount: str, card_uid: str, client_order_id: str | None = None, member_id: str | None = None) -> dict[str, str]:
        '''
        Purchase with a saved card for recurring payments.

        Args:
            client_order_id (str): Your transaction ID. Must be sent for CheckStatus and countermeasures. (optional)
            amount (str) : Amount. (required*)
            member_id (str) : The unique ID of your customers. Services such as card memorization must be sent if they are to be used. (optional)
            card_uid (str) : (Unique Identifier) is a unique identifier assigned to a payment card. (required*)

        Returns:
            dict[str, str]: Parsed response as a dictionary.

        Raises:
            UnitedPaymentAPIException: If the request fails or an error is encountered.
        '''

        data = {
            'amount': amount,
            'cardUid': card_uid
        }

        if client_order_id:
            data['clientOrderId'] = client_order_id
        if member_id:
            data['memberId'] = member_id

        return self.make_request(endpoint='/transactions/purchase-with-saved-card-recurring', data=data, method='POST')

    def transaction_status_by_order_id(self, client_order_id: str) -> dict[str, str]:
        '''
        Get transaction status by Client Order ID.

        Args:
            client_order_id (str): Your transaction ID. Must be sent for CheckStatus and countermeasures. (required*)

        Returns:
            dict[str, str]: Parsed response as a dictionary.

        Raises:
            UnitedPaymentAPIException: If the request fails or an error is encountered.
        '''

        data = {
            'ClientOrderId': client_order_id
        }

        return self.make_request(endpoint='/transactions/transaction-status-by-order-id', data=data, method='POST')

    def transaction_status_by_transaction_id(self, transaction_id: str) -> dict[str, str]:
        '''
        Get transaction status by Transaction ID.

        Args:
            transaction_id (str) : Search by transaction number (required*)

        Returns:
            dict[str, str]: Parsed response as a dictionary.

        Raises:
            UnitedPaymentAPIException: If the request fails or an error is encountered.
        '''

        data = {
            'transactionId': transaction_id
        }

        return self.make_request(endpoint='/transactions/transaction-status-by-trx-id', data=data, method='POST')

    def refund(self, transaction_id: str, amount: str) -> dict[str, str]:
        '''
        Refund a transaction.

        Args:
            transaction_id (str) : Search by transaction number (required*)
            amount (str) : Amount. (required*)

        Returns:
            dict[str, str]: Parsed response as a dictionary.

        Raises:
            UnitedPaymentAPIException: If the request fails or an error is encountered.
        '''

        data = {
            'transactionId': transaction_id,
            'amount': amount
        }

        return self.make_request(endpoint='/transactions/refund', data=data, method='POST')

    def reversal(self, transaction_id: str) -> dict[str, str]:
        '''
        Reverse a transaction.

        Args:
            transaction_id (str) : Search by transaction number (required*)

        Returns:
            dict[str, str]: Parsed response as a dictionary.  

        Raises:
            UnitedPaymentAPIException: If the request fails or an error is encountered. 
        '''

        data = {
            'transactionId': transaction_id
        }

        return self.make_request(endpoint='/transactions/reverse', data=data, method='POST')

    def preauth(self, amount: str, language: Language, success_url: str, cancel_url: str, decline_url: str, member_id: str | None = None) -> dict[str, str]:
        '''
        Blocking the requested amount from the customer's card. After the goods or services are provided, a Completion request is sent to remove the blocked amount from the account, or if there is no removal, the transaction is Reversal. The Preauth transaction is automatically canceled if there is no deletion within 30 days.

        Args:
            amount (str) : Amount. (required*)
            language (Language) : Setting the payment page language from the Language enum. (required*)
            member_id (str) : The unique ID of your customers. Services such as card memorization must be sent if they are to be used. (optional)
            success_url (str) - If the payment is successful, your URL will be redirected with the Get method. (required*)
            cancel_url (str) - Your URL will be redirected with the Get method when payment is refused. (required*)
            decline_url (str) - Your URL will be redirected with the Get method if the payment fails. (required*)

        Returns:
            dict[str, str]: Parsed response as a dictionary.

        Raises:
            UnitedPaymentAPIException: If the request fails or an error is encountered.
        '''

        data = {
            'amount': amount,
            'language': language.value,
            'successUrl': success_url,
            'cancelUrl': cancel_url,
            'declineUrl': decline_url
        }

        if member_id:
            data['memberId'] = member_id

        return self.make_request(endpoint='/transactions/preauth', data=data, method='POST')

    def preauth_with_saved_card_recurring(self, amount: str, card_uid: str, client_order_id: str | None = None, member_id: str | None = None) -> dict[str, str]:
        '''
        Blocking the amount requested from the customer's card with a saved card. After the goods or services are provided, a Completion request is sent to remove the blocked amount from the account, or if there is no removal, the transaction is Reversal. The Preauth transaction is automatically canceled if there is no deletion within 30 days.

        Args:
            client_order_id (str): Your transaction ID. Must be sent for CheckStatus and countermeasures. (optional)
            amount (str) : Amount. (required*)
            member_id (str) : The unique ID of your customers. Services such as card memorization must be sent if they are to be used. (optional)
            card_uid (str) : (Unique Identifier) is a unique identifier assigned to a payment card. (required*)

        Returns:
            dict[str, str]: Parsed response as a dictionary.

        Raises:
            UnitedPaymentAPIException: If the request fails or an error is encountered.
        '''

        data = {
            'amount': amount,
            'cardUid': card_uid
        }

        if client_order_id:
            data['clientOrderId'] = client_order_id
        if member_id:
            data['memberId'] = member_id

        return self.make_request(endpoint='/transactions/preauth-with-saved-card-recurring', data=data, method='POST')

    def preauth_completion(self, transaction_id: str, amount: str, language: Language, member_id: str | None = None,  partner_id: str | None = None) -> dict[str, str]:
        '''
        Deletion of the blocked (Preauth) amount from the customer. A full or partial write-off can be made.

        Args:
            transaction_id (str) : Search by transaction number (required*)
            amount (str) : Amount. (required*)
            member_id (str) : The unique ID of your customers. Services such as card memorization must be sent if they are to be used. (optional)
            language (Language) : Setting the payment page language from the Language enum. (required*)
            partner_id (str) - If the SubMerchant structure is used, the merchant's ID will be given to you beforehand. (optional)

        Returns:
            dict[str, str]: Parsed response as a dictionary.

        Raises:
            UnitedPaymentAPIException: If the request fails or an error is encountered.
        '''

        data = {
            'transactionId': transaction_id,
            'amount': amount,
            'language': language.value
        }

        if member_id:
            data['memberId'] = member_id
        if partner_id:
            data['partnerId'] = partner_id

        return self.make_request(endpoint='/transactions/preauth-completion', data=data, method='POST')

    def installment(self, amount: str, language: Language, success_url: str, cancel_url: str, decline_url: str, installment: str, member_id: str | None = None) -> dict[str, str]:
        '''
        Make a payment in installments.

        Args:
            amount (str) : Amount. (required*)
            member_id (str) : The unique ID of your customers. Services such as card memorization must be sent if they are to be used. (optional)
            language (Language) : Setting the payment page language from the Language enum. (required*)
            success_url (str) - If the payment is successful, your URL will be redirected with the Get method. (required*)
            cancel_url (str) - Your URL will be redirected with the Get method when payment is refused. (required*)
            decline_url (str) - Your URL will be redirected with the Get method if the payment fails. (required*)
            installment (str) : To carry out installment operations, the number of installments is added to the installment cell (2, 3, 6 or 12). (optional)

        Returns:
            dict[str, str]: Parsed response as a dictionary.

        Raises:
            UnitedPaymentAPIException: If the request fails or an error is encountered.
        '''

        data = {
            'amount': amount,
            'language': language.value,
            'successUrl': success_url,
            'cancelUrl': cancel_url,
            'declineUrl': decline_url,
        }

        if member_id:
            data['memberId'] = member_id
        if installment:
            data['installment'] = installment

        return self.make_request(endpoint='/transactions/taksit', data=data, method='POST')

    def get_customer_cards(self, partner_id: str | None = None, member_id: str | None = None) -> dict[str, str]:
        '''
        Retrieve saved customer cards.

        Args:
            partner_id (str) - If the SubMerchant structure is used, the merchant's ID will be given to you beforehand. (required*)
            member_id (str) : The unique ID of your customers. Services such as card memorization must be sent if they are to be used. (optional)

        Returns:
            dict[str, str]: Parsed response as a dictionary.

        Raises:
            UnitedPaymentAPIException: If the request fails or an error is encountered.
        '''
        data = {}

        if member_id:
            data['memberId'] = member_id
        if partner_id:
            data['partnerId'] = partner_id

        return self.make_request(endpoint='/KapitalBank/GetCustomerCards', data=data, method='POST')

    def delete_customer_saved_cards(self, card_uid: str, member_id: str | None = None, partner_id: str | None = None) -> dict[str, str]:
        '''
        Delete a saved customer card.

        Args:
            member_id (str) : The unique ID of your customers. Services such as card memorization must be sent if they are to be used. (optional)
            card_uid (str) : (Unique Identifier) is a unique identifier assigned to a payment card. (required*)
            partner_id (str) - If the SubMerchant structure is used, the merchant's ID will be given to you beforehand. (optional)

        Returns:
            dict[str, str]: Parsed response as a dictionary.

        Raises:
            UnitedPaymentAPIException: If the request fails or an error is encountered.
        '''

        data = {
            'cardUID': card_uid,
        }

        if member_id:
            data['memberId'] = member_id
        if partner_id:
            data['partnerId'] = partner_id

        return self.make_request(endpoint='/KapitalBank/DeleteCustomerSavedCards', data=data, method='POST')

    def pay_by_link_qr_code(self, email: str, amount: str | None = None, installment: str | None = None, telephone: str | None = None, member_id: str | None = None, order_id: str | None = None, description: str | None = None) -> str:
        '''
        Create a pay link or QR code.

        Args:
            amount (str) : Amount. (optional)
            installment (str) : To carry out installment operations, the number of installments is added to the installment cell (2, 3, 6 or 12). (optional) 
            description (str) : A statement about the operation. It will be reflected on the dashboard that will be given to you. (optional)
            email (str) - Additional information of the customer. It will be reflected on the dashboard that will be given to you. (required*)
            telephone (str) - Additional information of the customer. It will be reflected on the dashboard that will be given to you. (optional)
            member_id (str) : The unique ID of your customers. Services such as card memorization must be sent if they are to be used. (optional)
            order_id (str) : The orderId acts as a unique identifier for the order on the merchant's side. (optional)

        Returns:
            dict[str, str]: Parsed response as a dictionary.

        Raises:
            UnitedPaymentAPIException: If the request fails or an error is encountered.
        '''

        url = f"{self.base_url}/transactions/create-pay-link"
        headers = self.set_headers()
        data = {
            "email": email,
        }

        if installment:
            data['installment'] = installment
        if description:
            data['description'] = description
        if telephone:
            data['telephone'] = telephone
        if member_id:
            data['memberId'] = member_id
        if order_id:
            data['orderId'] = order_id
        if amount:
            data['amount'] = amount

        response = requests.post(url, headers=headers, json=data)
        self.handle_response_errors(response)

        return response.text

    def get_agreement_detail(self, start_date: str, end_date: str) -> dict[str, str]:
        '''
        Retrieve agreement details within a specified date range.

        Args:
            start_date (str): The start date in format dd/mm/yyyy.
            end_date (str): The end date in format dd/mm/yyyy.

        Returns:
            dict: Parsed response from the API containing agreement details.

        Raises:
            UnitedPaymentAPIException: If the request fails or an error is encountered.
        '''

        params = {
            'startDate': start_date,
            'endDate': end_date
        }

        return self.make_request(endpoint='/aggrement/GetAggrementDetail', data=params, method='GET')
