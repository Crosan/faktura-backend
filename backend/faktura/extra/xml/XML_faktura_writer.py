import xml.etree.ElementTree as ET
from datetime import datetime
from backend.faktura.models import Faktura, Parsing, Analyse, Rekvirent
from xml.dom import minidom
from django.conf import settings


class XMLFakturaWriter:

    def __init__(self, testing=False):
        # self.root = ET.Element(
        #     'Emessage', {'xmlns': 'http://rep.oio.dk/medcom.dk/xml/schemas/2014/10/08/'})
        # self.root = ET.Element(r'ns1:GenericSAPOrder xmlns:ns1="urn:RegH:SalesOrderMgt:SCS:nonsap"')
        self.root = ET.Element('ns1:GenericSAPOrder', attrib={ 'xmlns:ns1' : 'urn:RegH:SalesOrderMgt:SCS:nonsap'})
        # self.parsing = None
        self.qs = None

        self.SenderBusinessSystemID = "RHDIA"
        self.BillingCompanyCode = "2200"
        self.debitorType = "6"
        self.ProfitCenter = "222252300"
        self.testing = testing

    def __str__(self):
        return ET.tostring((self.root), encoding='UTF-8')

    def __add_subtag(self, parent, tag, attrib={}):
        return ET.SubElement(parent, tag, attrib)

    def __test_and_set_or_fail(self, parent, tag, value, attrib={}):
        if not value:
            raise Exception("Missing mandatory value " + tag)
        else:
            self.__add_subtag(parent, tag, attrib).text = value

    def prettify(self, elem):
        """Return a pretty-printed XML string for the Element. """
        rough_string = ET.tostring(elem, encoding='UTF-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="\t")

    def old_create(self, parsing: Parsing):
        ''' Deprecated '''
        self.parsing = parsing

        sap_order = self.__add_subtag(self.root, 'GenericSAPOrder')
        self.__add_message_header(sap_order)
        self.__add_order_header_lst(sap_order)

        if True: #settings.DEVELOPMENT:
            print('outputting')
            # with open('out.xml', 'w') as f:
            with open('C:\\Users\\RSIM0016\\Documents\\faktura\\test.xml', 'w', encoding='utf-8') as f:
                f.write(self.prettify(self.root))

        return self.prettify(self.root)

    def create(self, faktura: Faktura):
        self.faktura = faktura

        # sap_order = self.__add_subtag(self.root, 'GenericSAPOrder')
        self.__add_message_header(self.root)
        # self.__add_order_header_lst(self.root)
        self.__add_order_header(self.root, faktura)

        if False:# settings.DEVELOPMENT:
            print('outputting')
            # with open('out.xml', 'w') as f:
            with open('C:\\Users\\RSIM0016\\Documents\\faktura\\test2.xml', 'w') as f:
                f.write(self.prettify(self.root))

        return self.prettify(self.root)


    def __add_message_header(self, parent):
        message_header = self.__add_subtag(parent, 'messageHeader')
        self.__test_and_set_or_fail(message_header, 'senderBusinessSystemID', self.SenderBusinessSystemID)
        self.__test_and_set_or_fail(message_header, 'creationDateTime', datetime.today().strftime('%Y-%m-%dT%H:%M:%S'))

        d = datetime.now()
        timestamp = "{}/{}/{}_{}:{}:{}.{}".format(d.year, d.month, d.day, d.hour, d.minute, d.second, d.microsecond)
        unique_name = "DIAOrder_" + timestamp

        self.__test_and_set_or_fail(message_header, 'originalLoadFileName', unique_name)  # lav unikt navn


    def __add_order_header_lst(self, parent):
        for faktura in self.qs:
            self.__add_order_header(parent, faktura)

    def __add_order_header(self, parent, faktura):
        order_header = self.__add_subtag(parent, 'orderHeader')

        self.__test_and_set_or_fail(order_header, 'BillingCompanyCode', self.BillingCompanyCode)
        # self.__test_and_set_or_fail(order_header, 'DebtorType', self.debitorType)

        # self.__test_and_set_or_fail(order_header, 'Debitor', "222252300")
        self.__test_and_set_or_fail(order_header, 'Debitor', faktura.rekvirent.debitor_nr, {'DebitorType' : self.debitorType}) #XXX
        # self.__test_and_set_or_fail(order_header, 'GlobalLocationNumber', faktura.rekvirent.GLN_nummer)
        self.__test_and_set_or_fail(order_header, 'PreferedInvoiceDate', datetime.today().strftime('%Y-%m-%dT%H:%M:%S'))
        self.__test_and_set_or_fail(order_header, 'OrderNumber', str(faktura.id))
        self.__test_and_set_or_fail(order_header, 'OrderText1', "For spørgsmål, kontakt Brian Schmidt 35453341")  # selv generer
        self.__test_and_set_or_fail(order_header, 'ProfitCenterHdr', self.ProfitCenter)

        self.__add_item_lines_lst(order_header, faktura)

    def __add_item_lines_lst(self, parent, faktura: Faktura):
        line_number = 1
        for analyse in faktura.analyser.all():
            self.__add_item_lines(parent, analyse, line_number)
            line_number = line_number + 1

    def __add_item_lines(self, parent, analyse: Analyse, line_number):
        # print('item line added')
        item_lines = self.__add_subtag(parent, 'itemLines')

        self.__test_and_set_or_fail(item_lines, 'LineNumber', str(line_number))
        # self.__test_and_set_or_fail(item_lines, 'ItemNumber', "901363")
        if settings.TESTING:
            self.__test_and_set_or_fail(item_lines, 'ItemNumber', "900395")
        else:
            self.__test_and_set_or_fail(item_lines, 'ItemNumber', "902991")
        # self.__test_and_set_or_fail(item_lines, 'NumberOrdered', str(analyse.antal))
        self.__test_and_set_or_fail(item_lines, 'NumberOrdered', "1")
        self.__test_and_set_or_fail(item_lines, 'UnitPrice', str(analyse.samlet_pris))
        self.__test_and_set_or_fail(item_lines, 'PriceCurrency', "DKK")

        months = ["jan", "feb", "mar", "apr", "maj", "jun", "jul", "aug", "sep", "okt", "nov", "dec"]
        date = analyse.svar_dato

        CPR = '123467-8912' if settings.TESTING else analyse.CPR
        itemtext = "{} - {} - {} ({})".format(CPR, str(date.day) + "-" + months[date.month-1] + "-" + str(date.year), analyse.analyse_type.ydelses_kode, analyse.analyse_type.ydelses_navn)
        itemtext = itemtext[:131] # Må max være 132 tegn lang


        self.__test_and_set_or_fail(item_lines, 'ItemText1', itemtext)
        self.__test_and_set_or_fail(item_lines, 'ProfitCenterItem', self.ProfitCenter)
