# pylint: disable=missing-docstring
"""
The test module for portfolio_report
"""
from pathlib import Path
from collections import OrderedDict
import argparse
import pytest
import requests
from portfolio import portfolio_report

#read_portfolio test (functionality tested in test_io.py)
def test_read_non_path():
    with pytest.raises(ValueError):
        portfolio_report.read_portfolio("egg")

#save_portfolio test (functionality tested in test_io.py)
def test_save_port_non_dict_list():
    with pytest.raises(ValueError):
        portfolio_report.save_portfolio("egg")

def test_save_port_non_path():
    with pytest.raises(ValueError):
        data = [{'symbol': 'MSFT', 'units': 10, 'cost': 99.66}]
        portfolio_report.save_portfolio(data, filename="egg")

#get_market_price_tests
def test_get_price_non_dict_list():
    with pytest.raises(ValueError):
        portfolio_report.get_market_price("egg")

def test_get_price_404(requests_mock):
    with pytest.raises(requests.HTTPError):
        input_dict = [
            OrderedDict([
                ('symbol', 'ICE'),
                ('units', '600'),
                ('cost', '1223.43')
            ])
        ]
        requests_mock.get("https://api.iextrading.com/1.0/tops/last?symbols=ICE", status_code=404)
        portfolio_report.get_market_price(input_dict)

def test_get_price_500(requests_mock):
    with pytest.raises(requests.HTTPError):
        input_dict = [
            OrderedDict([
                ('symbol', 'ICE'),
                ('units', '600'),
                ('cost', '1223.43')
            ])
        ]
        requests_mock.get("https://api.iextrading.com/1.0/tops/last?symbols=ICE", status_code=500)
        portfolio_report.get_market_price(input_dict)

def test_get_price_connection(requests_mock):
    with pytest.raises(requests.ConnectionError):
        input_dict = [
            OrderedDict([
                ('symbol', 'ICE'),
                ('units', '600'),
                ('cost', '1223.43')
            ])
        ]
        uri = "https://api.iextrading.com/1.0/tops/last?symbols=ICE"
        requests_mock.get(uri, exc=requests.exceptions.ConnectionError)
        portfolio_report.get_market_price(input_dict)

def test_get_price_timeout(requests_mock):
    with pytest.raises(requests.Timeout):
        input_dict = [
            OrderedDict([
                ('symbol', 'ICE'),
                ('units', '600'),
                ('cost', '1223.43')
            ])
        ]
        uri = "https://api.iextrading.com/1.0/tops/last?symbols=ICE"
        requests_mock.get(uri, exc=requests.exceptions.Timeout)
        portfolio_report.get_market_price(input_dict)

def test_get_price_return(requests_mock):
    input_dict = [
        OrderedDict([
            ('symbol', 'ICE'),
            ('units', '600'),
            ('cost', '1223.43')
        ])
    ]
    expected = [
        OrderedDict([
            ('symbol', 'ICE'),
            ('price', '84.985'),
            ('size', '404'),
            ('time', '1565352854915')
        ])
    ]
    requests_mock.get("https://api.iextrading.com/1.0/tops/last?symbols=ICE", json=expected)
    portfolio_report.get_market_price(input_dict)
    assert float(input_dict[0]["latest_price"]) == 84.985

def test_get_price_invalid_symbol(requests_mock):
    input_dict = [
        OrderedDict([
            ('symbol', 'EGG'),
            ('units', '100'),
            ('cost', '154.23'),
        ]),
        OrderedDict([
            ('symbol', 'ICE'),
            ('units', '600'),
            ('cost', '1223.43')
        ])
    ]
    expected = [
        OrderedDict([
            ('symbol', 'ICE'),
            ('price', '84.985'),
            ('size', '404'),
            ('time', '1565352854915')
        ])
    ]
    requests_mock.get("https://api.iextrading.com/1.0/tops/last?symbols=EGG,ICE", json=expected)
    portfolio_report.get_market_price(input_dict)
    assert input_dict[0]["symbol"] == "ICE" and len(input_dict) == 1

#calculate_book_value tests
def test_book_value_non_dict_list():
    with pytest.raises(ValueError):
        portfolio_report.calculate_book_value("egg")

def test_book_value_calculation():
    input_dict = [
        OrderedDict([
            ('symbol', 'ICE'),
            ('units', '600'),
            ('cost', '1223.43'),
            ('latest_price', '84.985')
        ])
    ]
    portfolio_report.calculate_book_value(input_dict)
    assert input_dict[0]["book_value"] == 734058

#calculate_market_value tests
def test_market_value_non_dict_list():
    with pytest.raises(ValueError):
        portfolio_report.calculate_market_value("egg")

def test_market_value_calculation():
    input_dict = [
        OrderedDict([
            ('symbol', 'ICE'),
            ('units', '600'),
            ('cost', '1223.43'),
            ('latest_price', '84.985'),
            ('book_value', '734058.0')
        ])
    ]
    portfolio_report.calculate_market_value(input_dict)
    assert input_dict[0]["market_value"] == 50991

#calculate_gain_loss tests
def test_gain_loss_non_dict_list():
    with pytest.raises(ValueError):
        portfolio_report.calculate_gain_loss("egg")

def test_gain_loss_calculation():
    input_dict = [
        OrderedDict([
            ('symbol', 'ICE'),
            ('units', '600'),
            ('cost', '1223.43'),
            ('latest_price', '84.985'),
            ('book_value', '734058.0'),
            ('market_value', '50991.0')
        ])
    ]
    portfolio_report.calculate_gain_loss(input_dict)
    assert input_dict[0]["gain_loss"] == -683067

#calculate_percent_change tests
def test_change_non_dict_list():
    with pytest.raises(ValueError):
        portfolio_report.calculate_percent_change("egg")

def test_change_calculation():
    input_dict = [
        OrderedDict([
            ('symbol', 'ICE'),
            ('units', '600'),
            ('cost', '1223.43'),
            ('latest_price', '84.985'),
            ('book_value', '734058.0'),
            ('market_value', '50991.0'),
            ('gain_loss', '-683067.0')
        ])
    ]
    portfolio_report.calculate_percent_change(input_dict)
    assert input_dict[0]["change"] == -.93

#save_report tests
def test_save_rep_non_dict_list():
    with pytest.raises(ValueError):
        portfolio_report.save_report("egg")

def test_save_rep_non_path(portfolio_csv):
    with pytest.raises(ValueError):
        portfolio_report.save_report(portfolio_csv, filename="egg")

def test_save_report(portfolio_csv):
    data = [
        OrderedDict([
            ('symbol', 'ICE'),
            ('units', '600'),
            ('cost', '1223.43'),
            ('latest_price', '84.985'),
            ('book_value', '734058.0'),
            ('market_value', '50991.0'),
            ('gain_loss', '-683067.0'),
            ('change', '-0.931')
        ])
    ]
    portfolio_report.save_report(data, filename=portfolio_csv)
    expected = "symbol,units,cost,latest_price,book_value,market_value,gain_loss,change\r\n"
    expected += "ICE,600,1223.43,84.985,734058.0,50991.0,-683067.0,-0.931\r\n"
    with open(portfolio_csv, "r", newline='') as file:
        result = file.read()
        assert result == expected, (
            f'Expecting the file to contain: \n{result}'
        )

#string_to_path tests
def test_non_string():
    with pytest.raises(ValueError):
        portfolio_report.string_to_path(3515380)

def test_string_to_path():
    path = portfolio_report.string_to_path("portfolio.csv")
    assert isinstance(path, Path) and path == Path.cwd() / "portfolio.csv"

def test_string_to_path_no_suffix():
    path = portfolio_report.string_to_path("portfolio")
    assert path == Path.cwd() / "portfolio.csv"

def test_string_to_path_bad_chars():
    path = portfolio_report.string_to_path(r'\/e:g*g?<l>e|g".csv')
    assert path.name == "eggleg.csv"

def test_string_to_path_all_bad():
    path = portfolio_report.string_to_path(r'*|\/?<>:"')
    assert path.name == "new.csv"

#dictionary_list_check tests
def test_dict_list_non_list():
    with pytest.raises(ValueError):
        portfolio_report.dictionary_list_check("egg")

def test_dict_list_all_bad():
    input_dict = [
        "egg",
        "leg"
    ]
    with pytest.raises(ValueError):
        portfolio_report.dictionary_list_check(input_dict)

def test_dict_list_some_bad():
    input_dict = [
        OrderedDict([
            ('symbol', 'ICE'),
            ('units', '600'),
            ('cost', '1223.43')
        ]),
        "egg",
        "leg"
    ]
    portfolio_report.dictionary_list_check(input_dict)
    assert len(input_dict) == 1 and input_dict[0]["symbol"] == "ICE"

def test_dict_list_all_good():
    input_dict = [
        OrderedDict([
            ('symbol', 'ICE'),
            ('units', '600'),
            ('cost', '1223.43')
        ]),
        OrderedDict([
            ('symbol', 'ENX'),
            ('units', '255'),
            ('cost', '404.01')
        ])
    ]
    portfolio_report.dictionary_list_check(input_dict)
    assert len(input_dict) == 2

def test_dict_list_missing_value():
    input_dict = [
        OrderedDict([
            ('symbol', 'ICE'),
            ('units', '600'),
            ('cost', '1223.43')
        ]),
        OrderedDict([
            ('symbol', 'ENX'),
            ('units', '255'),
            ('cost', None)
        ])
    ]
    portfolio_report.dictionary_list_check(input_dict)
    assert len(input_dict) == 1

def test_dict_list_empty_value():
    input_dict = [
        OrderedDict([
            ('symbol', 'ICE'),
            ('units', '600'),
            ('cost', '1223.43')
        ]),
        OrderedDict([
            ('symbol', 'ENX'),
            ('units', '255'),
            ('cost', '')
        ])
    ]
    portfolio_report.dictionary_list_check(input_dict)
    assert len(input_dict) == 1

def test_dict_list_missing_column():
    with pytest.raises(ValueError):
        input_dict = [
            OrderedDict([
                ('symbol', 'ICE'),
                ('units', '600')
            ]),
            OrderedDict([
                ('symbol', 'ENX'),
                ('units', '255')
            ])
        ]
        portfolio_report.dictionary_list_check(input_dict)

#get_args tests
def test_get_args_input():
    args = portfolio_report.get_args(["-in", "portfolio.csv"])
    assert args.input == "portfolio.csv"

def test_get_args_output():
    args = portfolio_report.get_args(["-out", "report.csv"])
    assert args.output == "report.csv"

#create_report tests
def test_create_report(portfolio_csv, requests_mock, tmp_path):
    returned = [
        OrderedDict([
            ('symbol', 'APPL'),
            ('price', '1478.19'),
            ('size', '404'),
            ('time', '1565352854915')
        ]),
        OrderedDict([
            ('symbol', 'AMZN'),
            ('price', '84.985'),
            ('size', '404'),
            ('time', '1565352854915')
        ])
    ]
    requests_mock.get("https://api.iextrading.com/1.0/tops/last?symbols=APPL,AMZN", json=returned)
    expected = "symbol,units,cost,latest_price,book_value,market_value,gain_loss,change\r\n"
    expected += "APPL,100,154.23,1478.19,15423.0,147819.0,132396.0,8.58\r\n"
    expected += "AMZN,600,1223.43,84.985,734058.0,50991.0,-683067.0,-0.93\r\n"
    portfolio_report.create_report(argparse.Namespace(input=str(portfolio_csv),
                                                      output=str(tmp_path / "report.csv")))
    with open((tmp_path / "report.csv"), "r", newline='') as file:
        result = file.read()
        assert result == expected, (
            f'Expecting the file to contain: \n{result}'
        )
