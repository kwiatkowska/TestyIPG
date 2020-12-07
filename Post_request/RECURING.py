import unittest
from Post_request.Response import MerchantPost
from selenium.webdriver.common.by import By
from selenium import webdriver
from decimal import Decimal
from datetime import datetime


class Recurring(unittest.TestCase):
    merchant = MerchantPost()

    def test_timestamp(self):
        now = datetime.now()
        self.timestamp = int(datetime.timestamp(now))
        self.timestamp = int(self.timestamp * 1000)

    def test_TokenizeRecuring(self):
        url = 'https://apiuat.test.secure.eservice.com.pl/token'
        self.test_timestamp()
        self.merchant.data['action'] = "PURCHASE"
        self.merchant.data["merchantTxId"] = "order-323"
        self.merchant.data["merchantId"] = 167885
        self.merchant.data["password"] = "56789"
        self.merchant.data["timestamp"] = self.timestamp
        self.merchant.data["channel"] = "ECOM"
        self.merchant.data['brandId'] = 1678850000
        self.merchant.data['currency'] = 'PLN'
        self.merchant.data['amount'] = Decimal(1)
        self.merchant.data['currency'] = 'PLN'
        self.merchant.data['merchantNotificationUrl'] = 'https://s1.lmx.com.pl/ppe/IPG-auto/resultToFile.php'
        self.merchant.data["merchantLandingPageUrl"] = 'https://ptsv2.com/t/66i1s-1534805666'
        self.merchant.data['paymentSolutionId'] = 500
        self.merchant.data['cardOnFileType'] = 'First'
        self.merchant.data['mmrpBillPayment'] = 'Recurring'
        self.merchant.data['mmrpCustomerPresent'] = 'BillPayment'
        self.merchant.post(url)
        self.merchant.response2json()
        print("response for Session Token Recurring ")
        print(self.merchant.response_content)
        self.token1 = self.merchant.response_content['token']

    def test_FirstPayment(self):
        self.test_TokenizeRecuring()
        url = "https://apiuat.test.secure.eservice.com.pl/payments"
        self.merchant.data["merchantId"] = 167885
        self.merchant.data["customerId"] = "Xo3HJvpSoPMTgpuLtX0r"
        self.merchant.data['specinCreditCardToken'] = 1897744908930197
        self.merchant.data["specinCreditCardCVV"] = "992"
        self.merchant.data['action'] = "PURCHASE"
        self.merchant.data['token'] = self.token1
        self.merchant.data['paymentSolutionId'] = 500
        self.merchant.data["channel"] = "ECOM"
        self.merchant.post(url)
        self.merchant.response2html()
        print("response for Purchase")
        print(self.merchant.response_content)
        self.redirectionUrl = self.merchant.response_content['redirectionUrl']

    def test_DS3SecureTerminal(self):
        self.test_FirstPayment()
        self.driver = webdriver.Chrome(executable_path='../drivers/chromedriver.exe')
        self.driver.get(self.redirectionUrl)
        self.driver.set_window_size(1936, 1056)
        self.driver.find_element(By.CSS_SELECTOR, ".buttonAction:nth-child(1)").click()

    def test_TokenizeSecondPayment(self):
        self.test_timestamp()
        url = 'https://apiuat.test.secure.eservice.com.pl/token'
        self.merchant.data['action'] = "PURCHASE"
        self.merchant.data["merchantTxId"] = "order-323"
        self.merchant.data["merchantId"] = 167885
        self.merchant.data["password"] = "56789"
        self.merchant.data["timestamp"] = self.timestamp
        self.merchant.data["channel"] = "ECOM"
        self.merchant.data['brandId'] = 1678850000
        self.merchant.data['currency'] = 'PLN'
        self.merchant.data['currency'] = 'PLN'
        self.merchant.data['merchantNotificationUrl'] = 'https://s1.lmx.com.pl/ppe/IPG-auto/resultToFile.php'
        self.merchant.data['paymentSolutionId'] = 500
        self.merchant.data["merchantLandingPageUrl"] = 'https://ptsv2.com/t/66i1s-1534805666'
        self.merchant.data['mmrpBillPayment'] = 'Recurring'
        self.merchant.data['mmrpCustomerPresent'] = 'BillPayment'
        self.merchant.data['cardOnFileType'] = 'Repeat'
        self.merchant.data['cardOnFileInitiator'] = 'Merchant'
        self.merchant.data['cardOnFileInitialTransactionId'] = "order-23"
        self.merchant.data['mmrpOriginalMerchantTransactionId'] = "order-23"
        self.merchant.data['amount'] = Decimal(1)
        self.merchant.post(url)
        self.merchant.response2json()
        print("response for Session Token Recurring ")
        print(self.merchant.response_content)
        self.token1 = self.merchant.response_content['token']

    def test_RepeatPayment(self):
        self.test_timestamp()
        self.test_TokenizeSecondPayment()
        url = "https://apiuat.test.secure.eservice.com.pl/payments"
        self.merchant.data['token'] = self.token1
        self.merchant.data["merchantId"] = 167885
        self.merchant.data["customerId"] = "Xo3HJvpSoPMTgpuLtX0r"
        self.merchant.data['specinCreditCardToken'] = 1897744908930197
        self.merchant.data["specinCreditCardCVV"] = "992"
        self.merchant.data['action'] = "PURCHASE"
        self.merchant.data['paymentSolutionId'] = 500
        self.merchant.data["channel"] = "ECOM"
        self.merchant.post(url)
        self.merchant.response2html()
        print("response for Purchase")
        print(self.merchant.response_content)
        #self.redirectionUrl = self.merchant.response_content['redirectionUrl']

    def test_DS3SecureSecond(self):
        self.test_RepeatPayment()
        self.driver = webdriver.Chrome(executable_path='../drivers/chromedriver.exe')
        self.driver.get(self.redirectionUrl)
        self.driver.set_window_size(1936, 1056)
        self.driver.find_element(By.CSS_SELECTOR, ".buttonAction:nth-child(1)").click()


if __name__ == '__main__':
    unittest.main()
