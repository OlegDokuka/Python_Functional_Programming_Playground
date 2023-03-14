from typing import Dict, Union, Any

PRICE_FIELDS = [
    ("TYPE", 0x0),  # hex for binary 0, it is a special case of fields that are always there
    ("MARKET", 0x0),  # hex for binary 0, it is a special case of fields that are always there
    ("FROMSYMBOL", 0x0),  # hex for binary 0, it is a special case of fields that are always there
    ("TOSYMBOL", 0x0),  # hex for binary 0, it is a special case of fields that are always there
    ("FLAGS", 0x0),  # hex for binary 0, it is a special case of fields that are always there
    ("PRICE", 0x1),  # hex for binary 1
    ("BID", 0x2),  # hex for binary 10
    ("OFFER", 0x4),  # hex for binary 100
    ("LASTUPDATE", 0x8),  # hex for binary 1000
    ("AVG", 0x10),  # hex for binary 10000
    ("LASTVOLUME", 0x20),  # hex for binary 100000
    ("LASTVOLUMETO", 0x40),  # hex for binary 1000000
    ("LASTTRADEID", 0x80),  # hex for binary 10000000
    ("VOLUMEHOUR", 0x100),  # hex for binary 100000000
    ("VOLUMEHOURTO", 0x200),  # hex for binary 1000000000
    ("VOLUME24HOUR", 0x400),  # hex for binary 10000000000
    ("VOLUME24HOURTO", 0x800),  # hex for binary 100000000000
    ("OPENHOUR", 0x1000),  # hex for binary 1000000000000
    ("HIGHHOUR", 0x2000),  # hex for binary 10000000000000
    ("LOWHOUR", 0x4000),  # hex for binary 100000000000000
    ("OPEN24HOUR", 0x8000),  # hex for binary 1000000000000000
    ("HIGH24HOUR", 0x10000),  # hex for binary 10000000000000000
    ("LOW24HOUR", 0x20000),  # hex for binary 100000000000000000
    ("LASTMARKET", 0x40000)
    # hext for binary 1000000000000000000, this is a special case and will only appear on CCCAGG messages
]

TRADE_FIELDS = [
    ("TYPE", 0x0),  # hex for binary 0, it is a special case of fields that are always there          TYPE
    ("MARKET", 0x0),  # hex for binary 0, it is a special case of fields that are always there        MARKET
    ("FROMSYMBOL", 0x0),  # hex for binary 0, it is a special case of fields that are always there     FROM SYMBOL
    ("TOSYMBOL", 0x0),  # hex for binary 0, it is a special case of fields that are always there       TO SYMBOL
    ("FLAGS", 0x0),  # hex for binary 0, it is a special case of fields that are always there          FLAGS
    ("ID", 0x1),  # hex for binary 1                                                                   ID
    ("TIMESTAMP", 0x2),  # hex for binary 10                                                           TIMESTAMP
    ("QUANTITY", 0x4),  # hex for binary 100                                                           QUANTITY
    ("PRICE", 0x8),  # hex for binary 1000                                                              PRICE
    ("TOTAL", 0x10)  # hex for binary 10000                                                            TOTAL
]


def unpack_price(message: str) -> dict[str, Union[str, float]]:
    valuesArray = message.split("~")
    mask = valuesArray[-1]
    maskInt = int(mask, 16)
    unpackedCurrent: dict[Any, Union[str, float]] = {}
    currentField = 0
    for k, v in PRICE_FIELDS:
        if v == 0:
            unpackedCurrent[k] = valuesArray[currentField]
            currentField += 1
        elif (maskInt & v) > 0:
            # i know this is a hack, for cccagg, future code please don't hate me:(, i did this to avoid
            # subscribing to trades as well in order to show the last market
            if k == "LASTMARKET" or k == "LASTTRADEID":
                unpackedCurrent[k] = valuesArray[currentField]
            else:
                unpackedCurrent[k] = float(valuesArray[currentField])  # type: ignore
            currentField += 1

    return unpackedCurrent


def unpack_trade(message: str) -> dict[str, Union[str, float]]:
    valuesArray = message.split("~")

    mask = valuesArray[-1]
    maskInt = int(mask, 16)
    unpackedTrade: dict[str, Union[str, float]] = {}
    currentField = 0

    for k, v in TRADE_FIELDS:
        if v == 0:
            unpackedTrade[k] = valuesArray[currentField]
            currentField += 1
        elif (maskInt & v) > 0:
            unpackedTrade[k] = float(valuesArray[currentField])  # type: ignore
            currentField += 1

    return unpackedTrade
