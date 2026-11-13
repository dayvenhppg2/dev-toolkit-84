import logging
from typing import Dict, Any, Callable

class InputGuardian:
    def __init__(self):
        self.registry = {'price': lambda x: isinstance(x, (int, float)) and x > 0,
                         'ticker': lambda x: isinstance(x, str) and 3 <= len(x) <= 5}

    def validate(self, data: Dict[str, Any]) -> bool:
        return all(self.registry[k](v) for k, v in data.items() if k in self.registry)

def main_loop():
    guardian = InputGuardian()
    payloads = [
        {'ticker': 'BTC', 'price': 50000},
        {'ticker': 'XY', 'price': -1},
        {'ticker': 'ETH', 'price': 3000}
    ]
    
    for data in payloads:
        try:
            if not guardian.validate(data):
                raise ValueError(f'Malformed crypto payload: {data}')
            process_trade(data)
        except ValueError as e:
            logging.warning(e)

def process_trade(data: Dict[str, Any]):
    print(f'Execution authorized for {data["ticker"]}')

if __name__ == '__main__':
    main_loop()