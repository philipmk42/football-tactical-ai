'''
Test script for StrategyGenerator.
Feeds sample opponent tactics to the LLM and prints the counter-strategy.
'''

import sys
import time
sys.path.insert(0, '.')

from strategy.strategy_generator import StrategyGenerator


def test_strategy_generation():
    '''Test end-to-end strategy generation.'''
    print('=' * 60)
    print('Testing Strategy Generator')
    print('=' * 60)

    print()
    print('[Test 1] Initializing and loading LLM...')
    print('(First run downloads TinyLlama - may take a few minutes)')
    generator = StrategyGenerator()

    start = time.time()
    generator.load()
    print(f'Model loaded in {time.time() - start:.1f}s')

    print()
    print('[Test 2] Defining sample opponent tactics...')
    opponent = {
        'formation': '4-3-3',
        'possession': 62,
        'playing_style': 'high press possession',
        'attack_side': 'right wing',
    }
    print(f'  Opponent: {opponent}')

    print()
    print('[Test 3] Generating counter-strategy...')
    start = time.time()
    result = generator.generate_counter_strategy(opponent)
    elapsed = time.time() - start

    print()
    print('=' * 60)
    print('RESULT')
    print('=' * 60)
    print()
    print('SITUATION:')
    print(result['situation'])
    print()
    print('COUNTER-STRATEGY:')
    print(result['counter_strategy'])
    print()
    print(f'(Generated in {elapsed:.1f}s)')
    print()
    print('Test complete!')


if __name__ == '__main__':
    test_strategy_generation()
