


def is_bullish_engulfing(prev, curr):
    return (
            prev['close'] < prev['open'] and  # vorheriger Tag bärisch
            curr['close'] > curr['open'] and  # aktueller Tag bullisch
            curr['open'] < prev['close'] and  # Körper größer
            curr['close'] > prev['open']
    )

def is_bearish_engulfing(prev, curr):
    return (
        prev['close'] > prev['open'] and     # vorheriger bullisch
        curr['close'] < curr['open'] and     # aktueller bärisch
        curr['open'] > prev['close'] and     # Körper größer
        curr['close'] < prev['open']
    )

def is_piercing(prev, curr):
    return (
        prev['close'] < prev['open'] and     # Vortag bärisch
        curr['close'] > curr['open'] and     # Heute bullisch
        curr['open'] < prev['low'] and       # Gap nach unten
        curr['close'] > (prev['open'] + prev['close']) / 2
    )

def is_hammer(curr):
    body = abs(curr['close'] - curr['open'])
    lower_shadow = min(curr['open'], curr['close']) - curr['low']
    upper_shadow = curr['high'] - max(curr['open'], curr['close'])
    return (
        lower_shadow > 2 * body and   # langer Docht unten
        upper_shadow < body           # kaum Docht oben
    )

def is_dark_cloud_cover(prev, curr):
    return (
        prev['close'] > prev['open'] and         # vorher bullisch
        curr['open'] > prev['high'] and          # Gap nach oben
        curr['close'] < (prev['open'] + prev['close']) / 2 and
        curr['close'] < curr['open']             # bärische Kerze
    )