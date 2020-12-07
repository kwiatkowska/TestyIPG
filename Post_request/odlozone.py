def test_TokenAvailablePaymentMethod(self):
    self.merchant.data.clear()
    self.test_timestamp()
    url = 'https://apiuat.test.secure.eservice.com.pl/token'
    self.merchant.data["merchantId"] = 167885
    self.merchant.data["password"] = "56789"
    self.merchant.data['action'] = "GET_AVAILABLE_PAYSOLS"
    self.merchant.data["timestamp"] = self.timestamp
    self.merchant.data["allowOriginUrl"] = "https://apiuat.test.secure.eservice.com.pl/"
    self.merchant.data['currency'] = 'PLN'
    self.merchant.data['country'] = 'PL'
    self.merchant.data['brandId'] = 1678850000
    self.merchant.post(url)
    self.merchant.response2html()
    print('Odpowiedz dla PaymentMethod  ')
    print(self.merchant.response_content)

# def test_AvailablePaymentMethod(self):
#     self.test_TokenAvailablePaymentMethod()
#     url = "https://cashierui-apiuat.test.secure.eservice.com.pl/"
#     #url = "https://apiuat.test.secure.eservice.com.pl/payments"
#     self.merchant.data["merchantId"] = 167885
#     self.merchant.data["password"] = "56789"
#     self.token1 = self.merchant.response_content['token']
#     self.merchant.post(url)
#     self.merchant.response2json()
#     print('Odpowiedz dla PaymentMethod  ')
#     print(self.merchant.response_content)
