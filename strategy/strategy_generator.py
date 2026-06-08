'''
Strategy Generator Module
Connects tactical analysis to the LLM to produce counter-strategies.
'''

import sys
sys.path.insert(0, '.')

from strategy.llm_client import LLMClient
from strategy.prompt_templates import build_strategy_prompt, build_tactical_summary


class StrategyGenerator:
    '''Generates counter-strategies from tactical data using an LLM.'''

    def __init__(self):
        self.llm = LLMClient()
        self.model_loaded = False

    def load(self):
        '''Load the underlying LLM (one-time).'''
        self.llm.load_model()
        self.model_loaded = True

    def generate_counter_strategy(self, team_stats, max_tokens=350):
        '''
        Generate a counter-strategy for a given opponent setup.

        Args:
            team_stats: dict describing the opponent's tactics
            max_tokens: max new tokens to generate (higher = fuller response)

        Returns:
            dict with the situation summary and the generated strategy
        '''
        if not self.model_loaded:
            raise RuntimeError('Call load() before generating strategies.')

        summary = build_tactical_summary(team_stats)
        prompt = build_strategy_prompt(team_stats)

        print('Generating counter-strategy...')
        strategy = self.llm.generate(prompt, max_new_tokens=max_tokens)

        return {
            'situation': summary,
            'counter_strategy': strategy,
        }
