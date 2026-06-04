'''
Prompt Templates Module
Builds structured prompts that describe a team's tactical setup,
to be sent to the LLM for counter-strategy generation.
'''


def build_tactical_summary(team_stats):
    '''
    Convert raw tactical data into a readable summary.

    Args:
        team_stats: dict with keys like formation, possession,
                    playing_style, attack_side

    Returns:
        A human-readable summary string.
    '''
    formation = team_stats.get('formation', 'unknown')
    possession = team_stats.get('possession', 0)
    style = team_stats.get('playing_style', 'balanced')
    attack_side = team_stats.get('attack_side', 'central')

    summary = (
        f'The opponent is playing a {formation} formation '
        f'with {possession}% ball possession. '
        f'Their playing style is {style}, '
        f'attacking primarily through the {attack_side}.'
    )
    return summary


def build_strategy_prompt(team_stats):
    '''
    Build the full prompt asking the LLM for a counter-strategy.

    Args:
        team_stats: dict describing the opponent

    Returns:
        A prompt string ready for the LLM.
    '''
    summary = build_tactical_summary(team_stats)

    prompt = (
        f'{summary}\n\n'
        f'As a football tactics expert, suggest a specific counter-strategy. '
        f'Recommend a formation and 3 key tactical adjustments to beat this opponent. '
        f'Be concise and practical.'
    )
    return prompt
