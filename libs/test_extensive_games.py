from week6 import Game, TerminalGameNode, PlayerGameNode, evaluate_policy_profile, best_response_policy

import numpy as np

def rock_paper_scissor_game():
    rock_rock = TerminalGameNode(state=(('R', 'R'), (('R'), ('R'), ())), valuation=np.array([0, 0]))
    rock_paper = TerminalGameNode(state=(('R', 'P'), (('R'), ('P'), ())), valuation=np.array([-1, 1]))
    rock_scissors = TerminalGameNode(state=(('R', 'S'), (('R'), ('S'), ())), valuation=np.array([1, -1]))
    rock = PlayerGameNode(state=((), (('R'), (), ())), player=1, children={'R': rock_rock, 'P': rock_paper, 'S': rock_scissors})
    
    paper_rock = TerminalGameNode(state=(('P', 'R'), (('P'), ('R'), ())), valuation=np.array([1, -1]))
    paper_paper = TerminalGameNode(state=(('P', 'P'), (('P'), ('P'), ())), valuation=np.array([0, 0]))
    paper_scissors = TerminalGameNode(state=(('P', 'S'), (('P'), ('S'), ())), valuation=np.array([-1, 1]))
    paper = PlayerGameNode(state=((), (('P'), (), ())), player=1, children={'R': paper_rock, 'P': paper_paper, 'S': paper_scissors})
    
    scissors_rock = TerminalGameNode(state=(('S', 'R'), (('S'), ('R'), ())), valuation=np.array([-1, 1]))
    scissors_paper = TerminalGameNode(state=(('S', 'P'), (('S'), ('P'), ())), valuation=np.array([1, -1]))
    scissors_scissors = TerminalGameNode(state=(('S', 'S'), (('S'), ('S'), ())), valuation=np.array([0, 0]))
    scissors = PlayerGameNode(state=((), (('S'), (), ())), player=1, children={'R': scissors_rock, 'P': scissors_paper, 'S': scissors_scissors})
    
    root = PlayerGameNode(state=((), ((), (), ())), player=0, children={'R': rock, 'P': paper, 'S': scissors})
    
    game = Game(root, 2)
    
    return game
    
def kuhn_poker():
    root = PlayerGameNode(state=((), ((), (), ())), player='chance', children={})
    
    check = ('ch',)
    call = ('ca',)
    bet = ('b',)
    fold = ('f',)
    
    for card_a, card_b, a_val in (('J', 'Q', -1.), ('J', 'K', -1.), ('Q', 'J', 1.), ('Q', 'K', -1.), ('K', 'J', 1.), ('K', 'Q', 1.)):
        valuation = np.array([a_val, -a_val])
        private_state = ((card_a,), (card_b,))
        player_a_node = PlayerGameNode(state=((), private_state), player=0, children={})

        root.children[(card_a, card_b)] = player_a_node
        
        player_b_c_node = PlayerGameNode(state=((check,), private_state), player=1, children={})
        player_a_node.children[check] = player_b_c_node
        
        terminal_a_cc_node = TerminalGameNode(state=((check, check), private_state), valuation=valuation)
        player_b_c_node.children[check] = terminal_a_cc_node

        player_a_cb_node = PlayerGameNode(state=((check, bet), private_state), player=0, children={})
        player_b_c_node.children[bet] = player_a_cb_node
        
        terminal_cbf_node = TerminalGameNode(state=((check, bet, fold), private_state), valuation=np.array([-1., 1.]))
        player_a_cb_node.children[fold] = terminal_cbf_node
        
        terminal_cbc_node = TerminalGameNode(state=((check, bet, call), private_state), valuation=2. * valuation)
        player_a_cb_node.children[call] = terminal_cbc_node

        player_b_b_node = PlayerGameNode(state=((bet,), private_state), player=1, children={})
        player_a_node.children[bet] = player_b_b_node
        
        terminal_bf_node = TerminalGameNode(state=((bet, fold), private_state), valuation=np.array([1., -1.]))
        player_b_b_node.children[fold] = terminal_bf_node
        
        terminal_bc_node = TerminalGameNode(state=((bet, call), private_state), valuation=2. * valuation)
        player_b_b_node.children[call] = terminal_bc_node
        
    chance = {
        ((), ()): {
            ('J', 'Q'): 1/6,
            ('J', 'K'): 1/6,
            ('Q', 'J'): 1/6,
            ('Q', 'K'): 1/6,
            ('K', 'J'): 1/6,
            ('K', 'Q'): 1/6,
        }
    }
        
    return Game(root, 2, chance), (check, call, bet, fold)

        
        
        