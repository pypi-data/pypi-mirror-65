import csv
import datetime
from typing import Dict, Iterator, List, Optional

from investments.currency import Currency
from investments.dividend import Dividend
from investments.money import Money
from investments.ticker import Ticker, TickerKind
from investments.trade import Trade

import xml.etree.ElementTree as ET


def _parse_datetime(strval: str):
    return datetime.datetime.strptime(strval, '%Y-%m-%dT%H:%M:%S')


def _parse_tickerkind(strval: str):
    if strval in {'Акции', 'ПАИ'}:
        return TickerKind.Stock
    if strval == 'РДР':
        return TickerKind.RDR
    if strval == 'опционы':
        return TickerKind.Option
    if strval == 'Фьючерсы/Форварды/Свопы':
        return TickerKind.Futures
    if strval == 'Облигации':
        return TickerKind.Bond
    raise ValueError(strval)

class OpenBrokerParser(object):
    def __init__(self):
        self._trades = []
        # self._dividends = []
        # self._deposits_and_withdrawals = []
        self._tickers = {}

    @property
    def trades(self):
        return self._trades

    @property
    def dividends(self):
        return self._dividends

    def parse_xml(self, xml_file_name: str):
        tree = ET.parse(xml_file_name)
        self._parse_tickers(tree)
        self._parse_trades(tree)
        self._parse_not_trade_operations(tree)

        self._trades.sort(key=lambda x: x.datetime)
        # self._dividends.sort(key=lambda x: x.date)
        # self._deposits_and_withdrawals.sort(key=lambda x: x[0])

    def _parse_tickers(self, xml_tree: ET.ElementTree):
        for rec in xml_tree.findall('spot_portfolio_security_params/item'):
            f = rec.attrib

            ticker = Ticker(symbol=f['ticker'], kind=_parse_tickerkind(f['security_type']))

            # <item security_name="Русал рдр " security_grn_code="5-01-01481-B" board_name="ПАО Московская биржа" issuer_name="ПАО Сбербанк" isin="RU000A0JR5Z5" security_type="РДР" securyty_type_add="RD " nominal_curr="RUB" lot_size="10" ticker="RUALR" market_price="0.000000" />
            # <item security_name="RUSAL plc " security_grn_code="" board_name="ПАО Московская биржа" issuer_name="United Company RUSAL PLC" isin="JE00B5BCW814" security_type="Акции" securyty_type_add="АО " nominal="0.010000" nominal_curr="USD" lot_size="10" ticker="RUAL" market_price="24.845000" />

            # security_grn_codegcc

            assert f['security_name'] not in self._tickers

            self._tickers[f['security_name']] = ticker

    def _parse_not_trade_operations(self, xml_tree: ET.ElementTree):
        # <item operation_date="2019-05-15T00:00:00" currency_code="RUB" amount="13364.00" comment="Выплата дохода клиент 63861 (НКД 11 ОФЗ 26216) налог к удержанию 0.00 рублей"/>
        bonds_redemption = []

        for rec in xml_tree.findall('spot_non_trade_security_operations/item'):
            f = rec.attrib
            if 'Снятие ЦБ с учета. Погашение облигаций' in f['comment']:
                bonds_redemption.append(f)

        for xrec in xml_tree.findall('spot_non_trade_money_operations/item'):
            f = xrec.attrib
            if '(Погашение' not in f['comment']:
                continue

            found_idx = None
            for i, bd in enumerate(bonds_redemption):
                if (bd['operation_date'] == f['operation_date']) and (bd['security_name'] in f['comment']):
                    found_idx = i
                    qnty = float(bd['quantity'])
                    assert float(int(qnty)) == qnty
                    dt = _parse_datetime(f['operation_date'])
                    self._trades.append(Trade(
                        ticker=self._tickers[bd['security_name']],
                        datetime=dt,
                        settle_date=dt,
                        quantity=int(qnty),
                        price=Money(f['amount'], Currency.parse(f['currency_code'])),
                        fee=Money(0, Currency.parse(f['currency_code'])),
                    ))
                    break

            if found_idx is None:
                raise Exception('not found')
            else:
                bonds_redemption.pop(found_idx)

        assert not bonds_redemption, 'not empty'


    def _parse_trades(self, xml_tree: ET.ElementTree):
        for rec in xml_tree.findall('spot_main_deals_conclusion/item'):
            f = rec.attrib
            qnty = -1 * float(f['sell_qnty']) if 'sell_qnty' in f else float(f['buy_qnty'])
            assert float(int(qnty)) == qnty
            self._trades.append(Trade(
                ticker=self._tickers[f['security_name']],
                datetime=_parse_datetime(f['conclusion_time']),
                settle_date=_parse_datetime(f['execution_date']),
                quantity=int(qnty),
                price=Money(f['price'], Currency.parse(f['price_currency_code'])),
                fee=Money(f['broker_commission'], Currency.parse(f['broker_commission_currency_code'])),
            ))

        for rec in xml_tree.findall('common_deal/item'):
            f = rec.attrib
            ticker = Ticker(symbol=f['security_code'], kind=_parse_tickerkind(f['security_type_text']))

            assert f['deal_sign'] in {'-1', '1'}
            assert str(int(f['quantity'])) == f['quantity']

            self._trades.append(Trade(
                ticker=ticker,
                datetime=_parse_datetime(f['deal_date']),
                settle_date=_parse_datetime(f['execution_date']),
                quantity=int(f['quantity']) * int(f['deal_sign']),
                price=Money(f['price_rur'], Currency.RUB),
                fee=Money(f['comm_trade'], Currency.RUB) + Money(f['comm_stock'], Currency.RUB)
            ))
