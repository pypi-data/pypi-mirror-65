# -*- coding: utf-8 -*-
from .api import ListoAPI, WrongDataFormat


class CfdiPayments(ListoAPI):
    def __init__(self, token, base_url):
        super(CfdiPayments, self).__init__(token, base_url)

    def cfdi_payments(self, **kwargs):
        """CFDI Payments
        Note: Size larger than 200 causes 500 Error

        """
        kwargs.setdefault("offset", 0)
        size = kwargs.setdefault("size", 100)
        while True:
            r = self.make_request(
                method="GET", path="/cfdi_payments/payments/",
                params=kwargs).json()["hits"]
            if not r:
                break
            for i in r:
                yield i
            kwargs["offset"] += size

    def cfdi_receipts(self, **kwargs):
        """CFDI Receipts
        Note: Size larger than 200 causes 500 Error

        """
        kwargs.setdefault("offset", 0)
        size = kwargs.setdefault("size", 100)
        while True:
            r = self.make_request(
                method="GET", path="/cfdi_payments/receipts/",
                params=kwargs).json()["hits"]
            if not r:
                break
            for i in r:
                yield i
            kwargs["offset"] += size
    
    def cfdi_payments_detail(self, id_pago):
        try:
            assert (type(id_pago) is int), 'El campo `id_pago` debe ser tipo `int`'
            return self.make_request(method="GET", path="/cfdi_payments/payments/" + str(id_pago)) \
                .json()
        except WrongDataFormat:
            pass

    def cfdi_receipts_detail(self, id_recibo):
        try:
            assert (type(id_recibo) is int), 'El campo `id_recibo` debe ser tipo `int`'
            return self.make_request(method="GET", path="/cfdi_payments/receipts/" + str(id_recibo)) \
                .json()
        except WrongDataFormat:
            pass        
