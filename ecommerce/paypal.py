from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersGetRequest, OrdersCaptureRequest

import sys
from os import environ

class PayPalClient:
    def __init__(self):
        self.client_id = environ.get('PAYPAL_CLIENT_ID')
        self.client_secret = environ.get('PAYPAL_CLIENT_SECRET')

        """Set up and return PayPal Python SDK environment with PayPal access credentials.
           This sample uses SandboxEnvironment. In production, use LiveEnvironment."""

        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)

        """ Returns PayPal HTTP client instance with environment that has access
            credentials context. Use this instance to invoke PayPal APIs, provided the
            credentials have access. """
        self.client = PayPalHttpClient(self.environment)

    def object_to_json(self, json_data):
        """
        Function to print all json data in an organized readable manner
        """
        result = {}
        if sys.version_info[0] < 3:
            itr = json_data.__dict__.iteritems()
        else:
            itr = json_data.__dict__.items()
        for key,value in itr:
            # Skip internal attributes.
            if key.startswith("__"):
                continue
            result[key] = self.array_to_json_array(value) if isinstance(value, list) else\
                        self.object_to_json(value) if not self.is_primittive(value) else\
                         value
        return result;
    def array_to_json_array(self, json_array):
        result =[]
        if isinstance(json_array, list):
            for item in json_array:
                result.append(self.object_to_json(item) if  not self.is_primittive(item) \
                              else self.array_to_json_array(item) if isinstance(item, list) else item)
        return result;

    def is_primittive(self, data):
        return isinstance(data, (str, int))

class Order(PayPalClient):
    def get_order(self, order_id):
        """Method to get order"""
        request = OrdersGetRequest(order_id)
        #3. Call PayPal to get the transaction
        response = self.client.execute(request)
        #4. Save the transaction in your database. Implement logic to save transaction to your database for future reference.
        print('Status Code: ', response.status_code)
        print('Status: ', response.result.status)
        print('Order ID: ', response.result.id)
        print('Intent: ', response.result.intent)
        print('Links:')
        for link in response.result.links:
            print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
            print('Gross Amount: {} {}'.format(response.result.purchase_units[0].amount.currency_code,
                            response.result.purchase_units[0].amount.value))
        return response

    def create_order(self, debug=False):
        request = OrdersCreateRequest()
        request.prefer('return=representation')
        #3. Call PayPal to set up a transaction
        request.request_body(self.build_request_body())
        response = self.client.execute(request)
        if debug:
            print('Status Code: ', response.status_code)
            print('Status: ', response.result.status)
            print('Order ID: ', response.result.id)
            print('Intent: ', response.result.intent)
        print('Links:')
        for link in response.result.links:
            print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
        print('Total Amount: {} {}'.format(response.result.purchase_units[0].amount.currency_code,
                            response.result.purchase_units[0].amount.value))

        return response

    def capture_order(self, order_id, debug=False):
        """Method to capture order using order_id"""
        request = OrdersCaptureRequest(order_id)
        #3. Call PayPal to capture an order
        response = self.client.execute(request)
        #4. Save the capture ID to your database. Implement logic to save capture to your database for future reference.
        if debug:
            print('Status Code: ', response.status_code)
            print('Status: ', response.result.status)
            print('Order ID: ', response.result.id)
        print('Links: ')
        for link in response.result.links:
            print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
        print('Capture Ids: ')
        for purchase_unit in response.result.purchase_units:
            for capture in purchase_unit.payments.captures:
                print('\t'), capture.id
        print("Buyer:")
        print("\tEmail Address: {}\n\tName: {}\n".format(response.result.payer.email_address,
            response.result.payer.name.given_name + " " + response.result.payer.name.surname))
        return response
