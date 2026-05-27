'''
Test script for LLM client.
Verifies TinyLlama model downloads and generates text.
'''

import sys
import time
sys.path.insert(0, '.')

from strategy.llm_client import LLMClient


def test_basic_generation():
    '''Test that the LLM can generate text.'''
    separator = '=' * 60
    dash_line = '-' * 60

    print(separator)
    print('Testing LLM Client - TinyLlama')
    print(separator)

    # Initialize
    client = LLMClient()

    # Load model
    start_load = time.time()
    client.load_model()
    load_time = time.time() - start_load
    print()
    print(f'Load time: {load_time:.1f} seconds')
    print()

    # Test prompts
    prompts = [
        'Briefly explain what a 4-3-3 football formation is.',
        'What is the counter strategy against high press?',
    ]

    for i, prompt in enumerate(prompts, 1):
        print()
        print(separator)
        print(f'Test {i} of {len(prompts)}')
        print(separator)
        print(f'Prompt: {prompt}')
        print()
        print('Generating response...')

        start = time.time()
        response = client.generate(prompt, max_new_tokens=150)
        elapsed = time.time() - start

        print()
        print(f'Response (generated in {elapsed:.1f}s):')
        print(dash_line)
        print(response)
        print(dash_line)

    print()
    print('All tests complete!')


if __name__ == '__main__':
    test_basic_generation()
