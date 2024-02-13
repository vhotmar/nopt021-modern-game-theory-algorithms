import numpy as np
from week6 import BehavioralPolicy, GameNode, _A, _S_pub, _S_priv, GamePlayer, GameResult, InformationSet, InformationSetNode, PoliciesAveraging, PolicyProfile, TerminalGameNode, PlayerGameNode, Game, compute_counterfactual_reach_probabilities, compute_exploitability, sum_dicts_of_dicts

Regret = dict[InformationSet[_S_pub, _S_priv], dict[_A, float]]

def calculate_regret(game: Game[_A, _S_pub, _S_priv], policy_profile: PolicyProfile[_S_pub, _S_priv, _A], player: GamePlayer):
    regret: Regret[_S_pub, _S_priv, _A] = dict()
    counterfactual_reach_probability = compute_counterfactual_reach_probabilities(game, policy_profile, player)

    def traverse_information_set(information_set_node: InformationSetNode[_A, _S_pub, _S_priv]):
        """
        Compute the regret for the information set and its children.
        """
        for information_set_child in information_set_node.children.values():
            traverse_information_set(information_set_child)
        
        # The value of the information set is the sum of the values of the histories in the information set weighted
        # by the counterfactual reach probability (by the probability "if I wanted to reach this information set, how
        # likely would I be to reach it")
        values_sum = 0.
        action_values: dict[_A, GameResult] = dict()

        for node in game.information_partition[player][information_set_node.information_set]:
            node_weight = counterfactual_reach_probability[node.state]
            values_sum += traverse(node) * node_weight

            for action, child in node.children.items():
                if action not in action_values:
                    action_values[action] = 0.

                action_values[action] += traverse(child) * node_weight
        
        regret[information_set_node.information_set] = {k: v - values_sum for k, v in action_values.items()}

    def traverse(node: GameNode[_A, _S_pub, _S_priv]) -> GameResult:
        """
        Compute the value of the node for the player, given the policy profile.
        """
        if isinstance(node, TerminalGameNode):
            return node.valuation[player]
        elif isinstance(node, PlayerGameNode):
            information_set = node.get_information_set()
            
            node_policy = policy_profile[node.player][information_set]

            value = 0.
            
            for action, child in node.children.items():
                prob = (node_policy[action] if action in node_policy else 0.)

                value += prob * traverse(child)

            return value
        else:
            assert False, f"Unexpected node type: {type(node)}"
            
    for node in game.information_set_tree[player].children:
        traverse_information_set(node)
            
    return regret

def regret_matching(regret: Regret[_S_pub, _S_priv, _A]) -> BehavioralPolicy[_S_pub, _S_priv, _A]:
    policy: PolicyProfile[_S_pub, _S_priv, _A] = dict()

    for information_set, action_regret in regret.items():
        total_positive_regret = sum([max(0., r) for r in action_regret.values()])

        if np.isclose(total_positive_regret, 0.):
            policy[information_set] = {action: 1. / len(action_regret) for action in action_regret}
        else:
            policy[information_set] = {action: max(0., r) / total_positive_regret for action, r in action_regret.items()}

    return policy

def fictitious_self_play_regret(game: Game[_A, _S_pub, _S_priv], steps: int = 100):
    policy_average: PoliciesAveraging[_A, _S_pub, _S_priv] = PoliciesAveraging(game)
    policy_average.init_from_uniform()

    regret: dict[GamePlayer, Regret[_S_pub, _S_priv, _A]] = dict()
    
    for player in range(game.number_of_players):
        regret[player] = dict()
        
        for information_set in game.information_partition[player]:
            regret[player][information_set] = dict()

            for action in game.information_set_actions[player][information_set]:
                regret[player][information_set][action] = 0.
    
    exploitability = []
    
    for _ in range(steps):
        current_profile = policy_average.average_profile()
        
        for player in range(game.number_of_players):
            # Given regret get current policy
            current_profile[player] = regret_matching(regret[player])
            
            policy_average.add_policy(player, current_profile[player])
                   
            
        for player in range(game.number_of_players):
            
            # Get regert wrt to current policy
            current_regret = calculate_regret(game, current_profile, player)
            
            # Update regret
            regret[player] = sum_dicts_of_dicts(regret[player], current_regret)
            
        
        # Given average policy get exploitability
        exploitability.append(compute_exploitability(game, policy_average.average_profile()))

    return exploitability, policy_average.average_profile()