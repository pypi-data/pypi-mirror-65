"""
Contains pytest configuration & fixtures.
"""
import pytest


@pytest.fixture
def portfolio_csv(tmp_path):
    """
    Creates a portfolio.csv in a temporary folder for the
    purposes of testing.
    """
    lines = [
        ('symbol,units,cost\r\n'),
        ('APPL,100,154.23\r\n'),
        ('AMZN,600,1223.43\r\n'),
    ]

    filename = tmp_path / 'portfolio.csv'
    with open(filename, 'w', newline='') as file:
        file.writelines(lines)

    return filename
