import xml.etree.ElementTree as ET
from datetime import datetime
from backend.faktura.models import Faktura, Parsing, Analyse, Rekvirent
from xml.dom import minidom


class XMLFaktura:

    def __init__(self, parsing: Parsing):
        self.root = ET.Element(
            'Emessage', {'xmlns': 'http://rep.oio.dk/medcom.dk/xml/schemas/2014/10/08/'})
        self.parsing = parsing

        self.SenderBusinessSystemID = "Genmed2200"
        self.BillingCompanyCode = "2200"
        self.debtorType = "1"

    def __str__(self):
        return ET.tostring((self.root), encoding='ISO-8859-1')

    def __add_subtag(self, parent, tag):
        return ET.SubElement(parent, tag)

    def __test_and_set_or_fail(self, parent, tag, value):
        if not value:
            raise Exception("Missing mandatory value " + tag)
        else:
            self.__add_subtag(parent, tag).text = value

    def prettify(self, elem):
        """Return a pretty-printed XML string for the Element. """
        rough_string = ET.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="\t")

    def create(self):
        sap_order = self.__add_subtag(self.root, 'GenericSAPOrder')
        self.__add_message_header(sap_order)
        self.__add_order_header_lst(sap_order)

        with open('out.xml', 'w') as f:
            f.write(self.prettify(self.root))

    def __add_message_header(self, parent):
        message_header = self.__add_subtag(parent, 'messageHeader')
        self.__test_and_set_or_fail(message_header, 'SenderBusinessSystemID', self.SenderBusinessSystemID)
        self.__test_and_set_or_fail(message_header, 'CreationDateTime', datetime.today().strftime('%Y-%m-%d;%H:%M'))

        # Tekst (Filnavn for faktura eks. DIAOrder_20141007.xml)
        self.__test_and_set_or_fail(message_header, 'OriginalLoadFileName', "PLACEHOLDER")  # lav unikt navn


    def __add_order_header_lst(self, parent):
        for faktura in self.parsing.fakturaer.all():
            self.__add_order_header(parent, faktura)

    def __add_order_header(self, parent, faktura):
        order_header = self.__add_subtag(parent, 'orderHeader')

        self.__test_and_set_or_fail(order_header, 'BillingCompanyCode', self.BillingCompanyCode)
        self.__test_and_set_or_fail(order_header, 'DebtorType', self.debtorType)
        self.__test_and_set_or_fail(order_header, 'GlobalLocationNumber', faktura.rekvirent.GLN_nummer)
        self.__test_and_set_or_fail(order_header, 'PreferedInvoiceDate', datetime.today().strftime('%Y-%m-%d;%H:%M'))
        self.__test_and_set_or_fail(order_header, 'OrderNumber', str(faktura.id))
        self.__test_and_set_or_fail(order_header, 'OrderText1', "Her skal der skrives noget brødtekst om faktura header")  # selv generer

        self.__add_item_lines_lst(order_header, faktura)

    def __add_item_lines_lst(self, parent, faktura: Faktura):
        line_number = 1
        for analyse in faktura.analyser.all():
            self.__add_item_lines(parent, analyse, line_number)
            line_number = line_number + 1

    def __add_item_lines(self, parent, analyse: Analyse, line_number):
        item_lines = self.__add_subtag(parent, 'itemLines')

        self.__test_and_set_or_fail(item_lines, 'LineNumber', str(line_number))
        self.__test_and_set_or_fail(item_lines, 'ItemNumber', "PLACEHOLDER")
        self.__test_and_set_or_fail(item_lines, 'NumberOrdered', str(analyse.antal))
        self.__test_and_set_or_fail(item_lines, 'UnitPrice', str(analyse.styk_pris))
        self.__test_and_set_or_fail(item_lines, 'PriceCurrency', "DKK")
        self.__test_and_set_or_fail(item_lines, 'ItemText1', "Her skal der skrives noget brødtekst om denne ydelse")

"""
    <?xml version="1.0" encoding="utf-8"?>
    <GenericSAPOrder>
    <messageHeader>
        <senderBusinessSystemID>str1234</senderBusinessSystemID>
        <creationDateTime>str1234</creationDateTime>
        <originalLoadFileName>str1234</originalLoadFileName>
    </messageHeader>
    <orderHeader>
        <BillingCompanyCode>str1</BillingCompanyCode>
        <DebtorType>s</DebtorType>
        <GlobalLocationNumber>str1234</GlobalLocationNumber>
        <CVRNumber>str1234</CVRNumber>
        <CPRNumber>str1234000</CPRNumber>
        <VATNumber>str1234</VATNumber>
        <SAPDebtorNumber>str1234</SAPDebtorNumber>
        <PreferedInvoiceDate>str1234</PreferedInvoiceDate>
        <OrderNumber>str1234</OrderNumber>
        <OrderText1>str1234</OrderText1>
        <AttachedDocument>AAAAZg==</AttachedDocument>
        <itemLines>
        <LineNumber>str1234</LineNumber>
        <ItemNumber>str1234</ItemNumber>
        <NumberOrdered>str1234</NumberOrdered>
        <UnitPrice>str1234</UnitPrice>
        <PriceCurrency>str1234</PriceCurrency>
        <ItemText1>str1234</ItemText1>
        </itemLines>
    </orderHeader>
    </GenericSAPOrder>
"""