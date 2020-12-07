import unittest
from Post_request.Response import MerchantPost
from selenium.webdriver.common.by import By
from selenium import webdriver
from decimal import Decimal
from datetime import datetime

class Zwroty(unittest.TestCase):
    merchant = MerchantPost()

    def test_timestamp(self):
        now = datetime.now()
        self.timestamp = int(datetime.timestamp(now))
        self.timestamp = int(self.timestamp * 1000)


    # pobieramy token do akcji tokenizacji karty płatniczej
    def test_SessionTokenRequest(self):
        self.test_timestamp()
        url = 'https://apiuat.test.secure.eservice.com.pl/token'
        self.merchant.data["merchantId"] = 167885
        self.merchant.data["password"] = "56789"
        self.merchant.data["action"] = "TOKENIZE"
        self.merchant.data["timestamp"] = self.timestamp
        self.merchant.post(url)
        self.merchant.response2json()
        print("response for Session Token Request")
        print(self.merchant.response_content)
        self.token1 = self.merchant.response_content['token']
        print(self.token1)
        assert self.merchant.response_content['result'] == 'success'

    # dokonujemy tokenizacji katy w celu jej uwierzytelnienia
    def test_Tokenize(self):
        url = 'https://apiuat.test.secure.eservice.com.pl/payments'
        self.test_SessionTokenRequest()
        self.merchant.data["token"] = self.token1
        self.merchant.data["number"] = '4123640000000197'
        self.merchant.data["nameOnCard"] = "Jaś Wędrowniczek"
        self.merchant.data["expiryMonth"] = "12"
        self.merchant.data["expiryYear"] = "2022"
        self.merchant.post(url)
        self.merchant.response2json()
        print("response for Tokenize")
        print(self.merchant.response_content)
        self.cardToken = self.merchant.response_content['cardToken']
        print(self.cardToken)

    # generowanie tokenu do Purchase
    def test_SessionTokenPurchase(self):
        self.test_Tokenize()
        self.test_timestamp()
        url = 'https://apiuat.test.secure.eservice.com.pl/token'
        self.merchant.data.clear()
        self.merchant.data["merchantId"] = 167885
        self.merchant.data["password"] = "56789"
        self.merchant.data['action'] = "PURCHASE"
        self.merchant.data["timestamp"] = self.timestamp
        self.merchant.data["channel"] = "ECOM"
        self.merchant.data['country'] = 'PL'
        self.merchant.data["allowOriginUrl"] = "https://apiuat.test.secure.eservice.com.pl/"
        self.merchant.data['merchantNotificationUrl'] = 'https://s1.lmx.com.pl/ppe/IPG-auto/resultToFile.php'
        self.merchant.data['paymentSolutionId'] = 500
        self.merchant.data['amount'] = Decimal(1)
        self.merchant.data['currency'] = 'PLN'
        self.merchant.data['specinCreditCardToken'] = self.cardToken
        self.merchant.data["merchantLandingPageUrl"] = 'https://ptsv2.com/t/66i1s-1534805666'
        self.merchant.data["customerFirstName"] = "Jaś"
        self.merchant.data["customerLastName"] = "Wędrowniczek"
        self.merchant.data["forceSecurePayment"] = ""
        print('request data ses tok purch')
        print(self.merchant.data)
        self.merchant.post(url)
        self.merchant.response2json()
        print("response for Session Token Purchase")
        print(self.merchant.response_content)
        self.token1 = self.merchant.response_content['token']

    # wykonanie akcji Purchase
    def test_ActionPurchase(self):
        self.test_SessionTokenPurchase()
        self.merchant.data.clear()
        self.merchant.data["merchantId"] = 167885
        url = "https://apiuat.test.secure.eservice.com.pl/payments"
        self.merchant.data["token"] = self.token1
        self.merchant.data["merchantTxId"] = "order-123123"
        self.merchant.data["customerId"] = "Xo3HJvpSoPMTgpuLtX0r"
        self.merchant.data["specinCreditCardCVV"] = "992"
        self.merchant.data['paymentSolutionId'] = 500
        self.merchant.data['CustomIPAddress'] = '85.115.35.180'
        self.merchant.data['specinCreditCardToken'] = self.cardToken
        print(self.merchant.data)
        self.merchant.post(url)
        self.merchant.response2html()
        print("response for Purchase")
        print(self.merchant.response_content)
        self.redirectionUrl = self.merchant.response_content['redirectionUrl']
        self.orderId = self.merchant.response_content['merchantTxId']

    def test_DS3SecureTerminal(self):
        self.test_ActionPurchase()
        self.driver = webdriver.Chrome(executable_path='../drivers/chromedriver.exe')
        self.driver.get(self.redirectionUrl)
        self.driver.find_element(By.CSS_SELECTOR, ".buttonAction:nth-child(1)").click()

    def test_TokenizeRefund(self):
        self.test_DS3SecureTerminal()
        self.merchant.data.clear()
        self.test_timestamp()
        url = 'https://apiuat.test.secure.eservice.com.pl/token'
        self.merchant.data['action'] = "REFUND"
        self.merchant.data["merchantId"] = 167885
        self.merchant.data["password"] = "56789"
        self.merchant.data['action'] = "REFUND"
        self.merchant.data["timestamp"] = self.timestamp
        self.merchant.data["channel"] = "ECOM"
        self.merchant.data['country'] = 'PL'
        self.merchant.data['originalMerchantTxId'] = self.orderId
        self.merchant.data["allowOriginUrl"] = "https://apiuat.test.secure.eservice.com.pl/"
        self.merchant.data['merchantNotificationUrl'] = 'https://s1.lmx.com.pl/ppe/IPG-auto/resultToFile.php'
        self.merchant.data['paymentSolutionId'] = 500
        self.merchant.data['amount'] = Decimal(1)
        self.merchant.data['currency'] = 'PLN'
        self.merchant.data["merchantLandingPageUrl"] = 'https://ptsv2.com/t/66i1s-1534805666'
        self.merchant.post(url)
        self.merchant.response2json()
        print("response for Token REFUND")
        print(self.merchant.response_content)
        self.token1 = self.merchant.response_content['token']

    def test_Refund(self):
        self.test_TokenizeRefund()
        self.merchant.data.clear()
        url = "https://apiuat.test.secure.eservice.com.pl/payments"
        self.merchant.data["merchantId"] = 167885
        self.merchant.data['token'] = self.token1
        self.merchant.post(url)
        self.merchant.response2json()
        print("response for REFUND")
        print(self.merchant.response_content)





if __name__ == '__main__':
    unittest.main()
