from pprint import pprint
import numpy as np

from test_extensive_games import rock_paper_scissor_game, kuhn_poker

from week6 import Game, PoliciesAveraging, TerminalGameNode, PlayerGameNode, evaluate_policy_profile, best_response_policy, fictitious_self_play
from week8 import calculate_regret, fictitious_self_play_regret

def test_rock_paper_scissor():
    game = rock_paper_scissor_game()
    
    rock_strategy = {
        ((), ()): {'R': 1.0},
    }
    
    paper_strategy = {
        ((), ()): {'P': 1.0},
    }
    
    scissors_strategy = {
        ((), ()): {'S': 1.0},
    }
    
    mixed_strategy = {
        ((), ()): {'R': 1/3, 'P': 1/3, 'S': 1/3},
    }
    
    rock_favoring_strategy = {
        ((), ()): {'R': 0.5, 'P': 0.25, 'S': 0.25},
    }

    np.testing.assert_array_equal(evaluate_policy_profile(game, { 0: rock_strategy, 1: paper_strategy }), np.array([-1., 1.]))
    np.testing.assert_array_equal(evaluate_policy_profile(game, { 0: rock_strategy, 1: scissors_strategy }), np.array([1., -1.]))
    np.testing.assert_array_equal(evaluate_policy_profile(game, { 0: rock_strategy, 1: rock_strategy }), np.array([0., 0.]))
    
    np.testing.assert_array_equal(evaluate_policy_profile(game, { 0: mixed_strategy, 1: mixed_strategy }), np.array([0., 0.]))
    np.testing.assert_array_equal(evaluate_policy_profile(game, { 0: rock_favoring_strategy, 1: scissors_strategy }), np.array([0.25, -0.25]))
    np.testing.assert_array_equal(evaluate_policy_profile(game, { 0: rock_favoring_strategy, 1: paper_strategy }), np.array([-0.25, 0.25]))
    
    assert best_response_policy(game, { 0: scissors_strategy }, 1) == rock_strategy
    assert best_response_policy(game, { 0: rock_strategy }, 1) == paper_strategy
    assert best_response_policy(game, { 0: paper_strategy }, 1) == scissors_strategy
    assert best_response_policy(game, { 0: rock_favoring_strategy }, 1) == paper_strategy

def test_policy_average():
    game = Game(PlayerGameNode(state=((), ((), (), ())), player=0, children={
        'L': TerminalGameNode(state=(('L',), ((), (), ())), valuation=np.array([1., -1.])),
        'R': PlayerGameNode(state=(('R',), ((), (), ())), player=1, children={
            'L': TerminalGameNode(state=(('R', 'L'), ((), (), ())), valuation=np.array([-1., 1.])),
            'R': PlayerGameNode(state=(('R', 'R'), ((), (), ())), player=0, children={
                'L': TerminalGameNode(state=(('R', 'R', 'L'), ((), (), ())), valuation=np.array([1., -1.])),
                'R': TerminalGameNode(state=(('R', 'R', 'R'), ((), (), ())), valuation=np.array([0., 0.])),
            }),
        }),
    }), 2)

    strategy_1 = {
        ((), ()): {'L': 0.2, 'R': 0.8},
        (('R', 'R'), ()): {'L': 0.8, 'R': 0.2},
    }
    
    strategy_2 = {
        ((), ()): {'L': 0.8, 'R': 0.2},
        (('R', 'R'), ()): {'L': 0.2, 'R': 0.8},
    }
    
    policies_averaging = PoliciesAveraging(game)
    policies_averaging.add_policy(0, strategy_1)
    policies_averaging.add_policy(0, strategy_2)
    
    average_strategy = policies_averaging.average_policy(0)
    
    assert average_strategy == {
        ((), ()): {'L': 0.5, 'R': 0.5},
        (('R', 'R'), ()): {'L': 0.68, 'R': 0.32},
    }

def test_kuhn_poker():
    game, (check, call, bet, fold) = kuhn_poker()
    
    check_or_fold_strategy = {
        # first player
        ((), ('J',)): {check: 1.0},
        ((), ('Q',)): {check: 1.0},
        ((), ('K',)): {check: 1.0},
        ((check, bet), ('J',)): {fold: 1.0},
        ((check, bet), ('Q',)): {fold: 1.0},
        ((check, bet), ('K',)): {fold: 1.0},
        
        # second player
        ((check,), ('J',)): {check: 1.0},
        ((check,), ('Q',)): {check: 1.0},
        ((check,), ('K',)): {check: 1.0},
        ((bet,), ('J',)): {fold: 1.0},
        ((bet,), ('Q',)): {fold: 1.0},
        ((bet,), ('K',)): {fold: 1.0},
    }
    
    profile = { 0: check_or_fold_strategy, 1: check_or_fold_strategy, 'chance': game.chance }
    
    regret_1 = calculate_regret(game, profile, 0)
    
    assert regret_1 == {((), ('J',)): {('b',): 0.6666666666666666, ('ch',): 0.0}, # we regret not betting, since in this strategy the other player would have folded
        ((), ('K',)): {('b',): 0.0, ('ch',): 0.0}, # we do not regert anything, since we will win (unless we will fold, but that will not happen since in this strategy the other player will always check)
        ((), ('Q',)): {('b',): 0.3333333333333333, ('ch',): 0.0}, # we regret not betting, since in this strategy the other player would have folded
        ((('ch',), ('b',)), ('J',)): {('ca',): 0.0, ('f',): 0.0}, # since the other player will always fold, these states are not possible and we do not regret anything
        ((('ch',), ('b',)), ('K',)): {('ca',): 0.0, ('f',): 0.0},
        ((('ch',), ('b',)), ('Q',)): {('ca',): 0.0, ('f',): 0.0}}
    
    # pprint(evaluate_policy_profile(game, profile))
    # pprint(evaluate_policy_profile(game, { 0: best_response_policy(game, profile, 0), 1: check_or_fold_strategy, 'chance': chance }))
    # pprint(evaluate_policy_profile(game, { 0: check_or_fold_strategy, 1: best_response_policy(game, profile, 1), 'chance': chance }))
    
    # pprint(best_response_policy(game, profile, 0))
    # pprint(best_response_policy(game, profile, 1))
    
    # pprint(compute_exploitability(game, profile))
    # pprint(compute_exploitability(game, { 0: best_response_policy(game, profile, 0), 1: best_response_policy(game, profile, 1), 'chance': chance }))
    
    # pprint(compute_sequence_realization_probabilities(game, check_or_fold_strategy, 0))
    # pprint(realization_probabilities_to_behavioral_policy(compute_sequence_realization_probabilities(game, check_or_fold_strategy, 0)))
    
    # pprint(compute_sequence_realization_probabilities(game, best_response_policy(game, profile, 0), 0))
    # r1 = fictitious_self_play_regret(game, 20)
    # pprint(r1[0][-1])
    # pprint(r1[1])
    
    # r2 = fictitious_self_play(game, 20)
    # pprint(r2[0][-1])
    # pprint(r2[1])
    
    
    # pprint(compute_exploitability(game, profile))
    