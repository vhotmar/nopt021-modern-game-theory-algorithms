from dataclasses import dataclass, field
from typing import Generic, Literal, Optional, TypeVar, Self
from functools import cached_property
from pprint import pprint

import numpy as np

_T = TypeVar('_T')
_S = TypeVar('_S')
_A = TypeVar('_A')
_S_pub = TypeVar('_S_pub')
_S_priv = TypeVar('_S_priv')

GamePlayer = int | Literal['chance']
Probability = float
GameResult = float

# Should identify any game node/history (no two histories can have the same game state)
GameState = tuple[_S_pub, tuple[_S_priv, ...]]
# Each information set should be identified by its player, its public state and player private state
InformationSet = tuple[_S_pub, _S_priv]
BehavioralPolicy = dict[InformationSet[_S_pub, _S_priv], dict[_A, Probability]]
PolicyProfile = dict[GamePlayer, BehavioralPolicy[_S_pub, _S_priv, _A]]
PolicyRealizationProbabilities = dict[GameState[_S_pub, _S_priv], dict[_A, Probability]]

@dataclass
class GameNode(Generic[_A, _S_pub, _S_priv]):
    state: GameState[_S_pub, _S_priv]

@dataclass
class TerminalGameNode(GameNode[_A, _S_pub, _S_priv]):
    valuation: np.ndarray

@dataclass
class PlayerGameNode(GameNode[_A, _S_pub, _S_priv]):
    player: GamePlayer
    children: 'dict[_A, GameNode[_A, _S_pub, _S_priv]]'

    def get_information_set(self: Self) -> InformationSet[_S_pub, _S_priv]:
        return self.state[0], self.state[1][(self.player if self.player != 'chance' else -1)]

@dataclass
class InformationSetNode(Generic[_A, _S_pub, _S_priv]):
    information_set: InformationSet[_S_pub, _S_priv] 
    children: 'dict[_A, InformationSetNode[_A, _S_pub, _S_priv]]'

@dataclass
class InformationSetTree(Generic[_A, _S_pub, _S_priv]):
    children: list[InformationSetNode[_A, _S_pub, _S_priv]]

@dataclass
class Game(Generic[_A, _S_pub, _S_priv]):
    root: GameNode[_A, _S_pub, _S_priv]
    number_of_players: int
    chance: BehavioralPolicy[_S_pub, _S_priv, _A] = field(default_factory=lambda: dict())
    
    @property
    def players_with_chance(self: Self) -> list[GamePlayer]:
        return list(range(self.number_of_players)) + ['chance']
    
    @cached_property
    def uniform_profile(self: Self) -> PolicyProfile[_S_pub, _S_priv, _A]:
        policy: PolicyProfile[_S_pub, _S_priv, _A] = dict()
        
        for player in range(self.number_of_players):
            policy[player] = dict()
            
            for information_set in self.information_partition[player]:
                policy[player][information_set] = dict()
                
                for action in self.information_set_actions[player][information_set]:
                    policy[player][information_set][action] = 1. / len(self.information_set_actions[player][information_set])
        
        return policy
    
    @cached_property
    def information_partition(self: Self):
        partition: dict[GamePlayer, dict[InformationSet[_S_pub, _S_priv], list[PlayerGameNode[_A, _S_pub, _S_priv]]]] = dict()
        
        def traverse(node: GameNode[_A, _S_pub, _S_priv]):
            if isinstance(node, TerminalGameNode):
                return
            elif isinstance(node, PlayerGameNode):
                if node.player not in partition:
                    partition[node.player] = dict()

                information_set = node.get_information_set()
                
                if information_set not in partition[node.player]:
                    partition[node.player][information_set] = []
                    
                partition[node.player][information_set].append(node)
                
                for node in node.children.values():
                    traverse(node)
            else:
                assert False, f"Unexpected node type: {type(node)}"
                
        traverse(self.root)
                
        return partition
    
    @cached_property
    def information_set_actions(self: Self):
        result: dict[GamePlayer, dict[InformationSet[_S_pub, _S_priv], set[_A]]] = dict()

        for player in range(self.number_of_players):
            result[player] = dict()
            
            for information_set in self.information_partition[player]:
                actions = set()
                
                for node in self.information_partition[player][information_set]:
                    actions |= set(node.children.keys())
                
                result[player][information_set] = actions
        
        return result
    
    @cached_property
    def information_set_tree(self: Self):
        trees: dict[GamePlayer, InformationSetTree[_A, _S_pub, _S_priv]] = dict()
        information_set_to_node: dict[GamePlayer, dict[InformationSet[_S_pub, _S_priv], InformationSetNode[_A, _S_pub, _S_priv]]] = dict()
        
        def collect_information_tree(
            node: GameNode[_A, _S_pub, _S_priv],
            player: GamePlayer,
            current_information_set_node: InformationSetTree[_A, _S_pub, _S_priv] | InformationSetNode[_A, _S_pub, _S_priv],
            last_action: Optional[_A]
        ):
            if isinstance(node, TerminalGameNode):
                return
            elif isinstance(node, PlayerGameNode):
                information_set = node.get_information_set()
                
                next_information_set_node = current_information_set_node

                if node.player == player:
                    if information_set not in information_set_to_node[node.player]:
                        information_set_to_node[node.player][information_set] = InformationSetNode(information_set, dict())

                        if isinstance(current_information_set_node, InformationSetTree):
                            assert last_action is None
                            
                            current_information_set_node.children.append(information_set_to_node[node.player][information_set])
                        else:
                            assert last_action is not None
                            
                            current_information_set_node.children[last_action] = information_set_to_node[node.player][information_set]
                    
                    next_information_set_node = information_set_to_node[node.player][information_set]

                for action, child in node.children.items():
                    collect_information_tree(child, player, next_information_set_node, action if node.player == player else last_action)
            else:
                assert False, f"Unexpected node type: {type(node)}"
                
        for player in range(self.number_of_players):
            trees[player] = InformationSetTree([])
            information_set_to_node[player] = dict()
            collect_information_tree(self.root, player, trees[player], None)
            
        return trees

def evaluate_policy_profile(game: Game[_A, _S_pub, _S_priv], policy_profile: PolicyProfile[_S_pub, _S_priv, _A]) -> np.ndarray:
    def traverse(node: GameNode[_A, _S_pub, _S_priv]):
        if isinstance(node, TerminalGameNode):
            return node.valuation
        elif isinstance(node, PlayerGameNode):
            node_policy = policy_profile[node.player][node.get_information_set()]
            
            value: Optional[np.ndarray] = None

            for action, child in node.children.items():
                prob = (node_policy[action] if action in node_policy else 0.)

                new_value = prob * traverse(child)

                if value is None:
                    value = new_value
                else:
                    value += new_value

            assert value is not None

            return value
        else:
            assert False, f"Unexpected node type: {type(node)}"
            
    return traverse(game.root)

def compute_counterfactual_reach_probabilities(game: Game[_A, _S_pub, _S_priv], policy_profile: PolicyProfile[_S_pub, _S_priv, _A], player: GamePlayer):
    """
    Probability of arriving at a given state, given the policy profile when player is trying to reach that state
    """
    probabilities: dict[GameState[_S_pub, _S_priv], Probability] = dict()
    
    def compute_probabilities(node: GameNode[_A, _S_pub, _S_priv], probability: Probability):
        probabilities[node.state] = probability

        if isinstance(node, TerminalGameNode):
            return
        elif isinstance(node, PlayerGameNode):
            for action, child in node.children.items():
                prob_to_use = 0.
                
                if player == node.player:
                    prob_to_use = 1.
                else:
                    node_policy = policy_profile[node.player][node.get_information_set()]

                    if action in node_policy:
                        prob_to_use = node_policy[action]
                
                compute_probabilities(child, probability * prob_to_use)
        else:
            assert False, f"Unexpected node type: {type(node)}"
            
    compute_probabilities(game.root, 1)
            
    return probabilities

def best_response_policy(game: Game[_A, _S_pub, _S_priv], policy_profile: PolicyProfile[_S_pub, _S_priv, _A], player: GamePlayer):
    behavioral_policy: BehavioralPolicy[_S_pub, _S_priv, _A] = dict()
    counterfactual_reach_probability = compute_counterfactual_reach_probabilities(game, policy_profile, player)

    def traverse_information_set(information_set_node: InformationSetNode[_A, _S_pub, _S_priv]):
        for information_set_child in information_set_node.children.values():
            traverse_information_set(information_set_child)
        
        action_values: dict[_A, GameResult] = dict()

        for node in game.information_partition[player][information_set_node.information_set]:
            for action, child in node.children.items():
                if action not in action_values:
                    action_values[action] = 0.

                action_values[action] += traverse(child) * counterfactual_reach_probability[node.state]
        
        max_action = max(action_values, key=action_values.get)

        behavioral_policy[information_set_node.information_set] = { max_action: 1. }

    def traverse(node: GameNode[_A, _S_pub, _S_priv]) -> GameResult:
        if isinstance(node, TerminalGameNode):
            return node.valuation[player]
        elif isinstance(node, PlayerGameNode):
            information_set = node.get_information_set()
            
            node_policy = policy_profile[node.player][information_set] if node.player != player else behavioral_policy[information_set]

            value = 0.
            
            for action, child in node.children.items():
                prob = (node_policy[action] if action in node_policy else 0.)

                value += prob * traverse(child)

            return value
        else:
            assert False, f"Unexpected node type: {type(node)}"
    
    for node in game.information_set_tree[player].children:
        traverse_information_set(node)
            
    return behavioral_policy

def compute_exploitability(game: Game[_A, _S_pub, _S_priv], policy_profile: PolicyProfile[_S_pub, _S_priv, _A]):
    evaluation = -evaluate_policy_profile(game, policy_profile)

    for player in range(game.number_of_players):
        best_response = best_response_policy(game, policy_profile, player)

        profile_copy = policy_profile.copy()
        profile_copy[player] = best_response

        best_response_value = evaluate_policy_profile(game, profile_copy)[player]

        evaluation[player] += best_response_value

    return evaluation.sum()

def compute_sequence_realization_probabilities(game: Game[_A, _S_pub, _S_priv], behavioral_policy: BehavioralPolicy[_S_pub, _S_priv, _A], player: GamePlayer):
    probabilities: BehavioralPolicy[_S_pub, _S_priv, _A] = dict()
    
    def traverse(node: InformationSetNode[_A, _S_pub, _S_priv], probability: Probability):
        probabilities[node.information_set] = dict()
        
        for action, policy_probability in behavioral_policy[node.information_set].items():
            prob = probability * policy_probability
            
            probabilities[node.information_set][action] = prob

            if action in node.children:
                traverse(node.children[action], prob)
        
    for node in game.information_set_tree[player].children:
        traverse(node, 1)
        
    return probabilities

def realization_probabilities_to_behavioral_policy(realization_probabilities: BehavioralPolicy[_S_pub, _S_priv, _A]):
    behavioral_policy: BehavioralPolicy[_S_pub, _S_priv, _A] = dict()
    
    for state, action_probabilities in realization_probabilities.items():
        probabilities_sum = sum(action_probabilities.values())
        behavioral_policy[state] = dict()
        
        for action, probability in action_probabilities.items():
            behavioral_policy[state][action] = probability / probabilities_sum
            
    return behavioral_policy

def sum_dicts(x: dict[_T, float], y: dict[_T, float]) -> dict[_T, float]:
    return {k: x.get(k, 0) + y.get(k, 0) for k in set(x) | set(y)}

def sum_dicts_of_dicts(x: dict[_T, dict[_S, float]], y: dict[_T, dict[_S, float]]) -> dict[_T, dict[_S, float]]:
    result: dict[_T, dict[_S, float]] = dict()
    
    for state in set(x) | set(y):
        result[state] = sum_dicts(x.get(state, dict()), y.get(state, dict()))
        
    return result

@dataclass
class PoliciesAveraging(Generic[_A, _S_pub, _S_priv]):
    game: Game[_A, _S_pub, _S_priv]
    sums: PolicyProfile[_S_pub, _S_priv, _A] = field(init=False, default_factory=lambda: dict())
    
    def init_from_uniform(self: Self):
        for player in range(self.game.number_of_players):
            self.add_policy(player, self.game.uniform_profile[player])
    
    def add_policy(self: Self, player: GamePlayer, policy: BehavioralPolicy[_S_pub, _S_priv, _A]):
        assert player != 'chance'

        if player not in self.sums:
            self.sums[player] = dict()

        self.sums[player] = sum_dicts_of_dicts(self.sums[player], compute_sequence_realization_probabilities(self.game, policy, player))
        
    def average_policy(self: Self, player: GamePlayer) -> BehavioralPolicy[_S_pub, _S_priv, _A]:
        if player == 'chance':
            return self.game.chance

        if player not in self.sums:
            return self.game.uniform_profile[player]

        return realization_probabilities_to_behavioral_policy(self.sums[player])
    
    def average_profile(self: Self) -> PolicyProfile[_S_pub, _S_priv, _A]:
        return {player: self.average_policy(player) for player in self.game.players_with_chance}
        

def fictitious_self_play(game: Game[_A, _S_pub, _S_priv], steps: int = 100):
    policy_average: PoliciesAveraging[_A, _S_pub, _S_priv] = PoliciesAveraging(game)
    policy_average.init_from_uniform()

    exploitability = []

    for _ in range(steps):
        current_policy = policy_average.average_profile()

        for player in range(game.number_of_players):
            new_best_policy = best_response_policy(game, current_policy, player)
            
            policy_average.add_policy(player, new_best_policy)

        exploitability.append(compute_exploitability(game, policy_average.average_profile()))


    return exploitability, policy_average.average_profile()