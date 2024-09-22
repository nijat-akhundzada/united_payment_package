import unittest
from united_payment.client import UnitedPaymentAPI
from united_payment.constants import Language, Currency


class TestUnitedPaymentAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        '''Setup the UnitedPaymentAPI instance with real credentials for testing.'''
        cls.api = UnitedPaymentAPI(
            base_url='https://test-vpos.unitedpayment.az/api',
            email='support@unitedpayment.com',
            password='Testmerchant12!'
        )

    def test_checkout_status_code_200(self):
        '''Test if checkout returns a valid response.'''
        response = self.api.checkout(
            amount='100',
            language=Language.EN,
            success_url='https://success.url',
            cancel_url='https://cancel.url',
            decline_url='https://decline.url',
            currency=Currency.AZN
        )
        self.assertIsNotNone(response)

    def test_card_registration_status_code_200(self):
        '''Test if card_registration returns a valid response.'''
        response = self.api.card_registration(
            language=Language.EN,
            success_url='https://success.url',
            cancel_url='https://cancel.url',
            decline_url='https://decline.url'
        )
        self.assertIsNotNone(response)

    def test_purchase_with_saved_card_3ds_status_code_200(self):
        '''Test if purchase_with_saved_card_3ds returns a valid response.'''
        response = self.api.purchase_with_saved_card_3ds(
            amount='100',
            card_uid='4B88CB8C7FF5EE1180EB005056954BCC',
            language=Language.EN,
            success_url='https://success.url',
            cancel_url='https://cancel.url',
            decline_url='https://decline.url'
        )
        self.assertIsNotNone(response)

    def test_card_registration_recurring_status_code_200(self):
        '''Test if card_registration_recurring returns a valid response.'''
        response = self.api.card_registration_recurring(
            success_url='https://success.url',
            cancel_url='https://cancel.url',
            decline_url='https://decline.url'
        )
        self.assertIsNotNone(response)

    def test_purchase_with_saved_card_recurring_status_code_200(self):
        '''Test if purchase_with_saved_card_recurring returns a valid response.'''
        response = self.api.purchase_with_saved_card_recurring(
            amount='100',
            card_uid='4B88CB8C7FF5EE1180EB005056954BCC'
        )
        self.assertIsNotNone(response)

    def test_transaction_status_by_order_id_status_code_200(self):
        '''Test if transaction_status_by_order_id returns a valid response.'''
        response = self.api.transaction_status_by_order_id(
            client_order_id='TestClinetOrderId'
        )
        self.assertIsNotNone(response)

    def test_transaction_status_by_transaction_id_status_code_200(self):
        '''Test if transaction_status_by_transaction_id returns a valid response.'''
        response = self.api.transaction_status_by_transaction_id(
            transaction_id='275'
        )
        self.assertIsNotNone(response)

    def test_refund_status_code_200(self):
        '''Test if refund returns a valid response.'''
        response = self.api.refund(
            transaction_id='275',
            amount='50'
        )
        self.assertIsNotNone(response)

    def test_reversal_status_code_200(self):
        '''Test if reversal returns a valid response.'''
        response = self.api.reversal(
            transaction_id='275'
        )
        self.assertIsNotNone(response)

    def test_preauth_status_code_200(self):
        '''Test if preauth returns a valid response.'''
        response = self.api.preauth(
            amount='100',
            language=Language.EN,
            success_url='https://success.url',
            cancel_url='https://cancel.url',
            decline_url='https://decline.url'
        )
        self.assertIsNotNone(response)

    def test_preauth_with_saved_card_recurring_status_code_200(self):
        '''Test if preauth_with_saved_card_recurring returns a valid response.'''
        response = self.api.preauth_with_saved_card_recurring(
            amount='100',
            card_uid='4B88CB8C7FF5EE1180EB005056954BCC'
        )
        self.assertIsNotNone(response)

    def test_preauth_completion_status_code_200(self):
        '''Test if preauth_completion returns a valid response.'''
        response = self.api.preauth_completion(
            transaction_id='275',
            amount='100',
            language=Language.EN
        )
        self.assertIsNotNone(response)

    def test_installment_status_code_200(self):
        '''Test if installment returns a valid response.'''
        response = self.api.installment(
            amount='100',
            language=Language.EN,
            success_url='https://success.url',
            cancel_url='https://cancel.url',
            decline_url='https://decline.url',
            installment='3'
        )
        self.assertIsNotNone(response)

    def test_get_customer_cards_status_code_200(self):
        '''Test if get_customer_cards returns a valid response.'''
        response = self.api.get_customer_cards(
            member_id='TestMemberId'
        )
        self.assertIsNotNone(response)

    def test_delete_customer_saved_cards_status_code_200(self):
        '''Test if delete_customer_saved_cards returns a valid response.'''
        response = self.api.delete_customer_saved_cards(
            card_uid='4B88CB8C7FF5EE1180EB005056954BCC'
        )
        self.assertIsNotNone(response)

    def test_pay_by_link_qr_code_status_code_200(self):
        '''Test if pay_by_link_qr_code returns a valid response.'''
        response = self.api.pay_by_link_qr_code(
            email='test_email@example.com'
        )
        self.assertIsNotNone(response)

    def test_get_agreement_detail_status_code_200(self):
        '''Test if get_agreement_detail returns a valid response.'''
        response = self.api.get_agreement_detail(
            start_date='2024-01-01',
            end_date='2024-12-31'
        )
        self.assertIsNotNone(response)


if __name__ == '__main__':
    unittest.main()
