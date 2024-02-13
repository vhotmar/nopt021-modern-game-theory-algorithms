#import "@preview/ctheorems:1.1.0": *
#import "@preview/algo:0.3.3": algo, i, d, comment, code, no-emph
#show: thmrules

#set par(justify: true)
#set heading(numbering: "1.1.")

#let theorem = thmbox("theorem", "Theorem")
#let lemma = thmbox("lemma", "Lemma")
#let observation = thmbox("observation", "Observation")
#let proof = thmplain(
  "proof",
  "Proof",
  base: "theorem",
  bodyfmt: body => [#body #h(1fr) $square$]
).with(numbering: none)
#let definition = thmbox("definition", "Definition")

#let example = thmplain("example", "Example").with(numbering: none)

#let argmax = math.op("arg max", limits: true)
#let argmin = math.op("arg min", limits: true)

#let players = $cal(N)$
#let profile = $bold(pi)$
#let utility = $bold(u)$
#let strategy = $pi$
#let actions = $bold(A)$
#let game = $(players, actions, utility)$
#let action = $bold(a)$
#let bestresponses = $bb(B R)$
#let reward = $R$
#let sequence = $sigma$
#let realizationp = $x$
#let realizationps = $x_strategy$

#let playeri = (
  action: $a_i$,
  actions: $A_i$,
  utility: $u_i$,
  bestresponses: $bestresponses_i$,
  strategy: $strategy_i$,
  strategya: $strategy^a_i$,
  strategyb: $strategy^b_i$,
  strategyc: $strategy^c_i$,
  reward: $reward_(i)^(profile)$,
  rewardgiven: (strategy) => $reward_(i)^(strategy, profile_(-i))$,
  rewardothers: $reward_(i)^(strategy_i, profile_(-i))$,
  sequence: $sequence_(i)$,
  futurereward: $v^(profile)_(i)$,
  futurerewardc: $v^(profile)_(i, c)$,
  realizationp: $x_(strategy_(i))$
)

#let playeroi = (
  rewardgiveni: $reward_(-i)^(strategy_i, profile_(-i))$
)

#let others = (
  profile: $profile_(-i)$,
  action: $action_(-i)$,
  reachp: $P^(profile_(-i))$
)

#let playersc = $players_c$
#let histories = (
  all: [$cal(H)$],
  terminal: [$cal(Z)$],
  nonterminal: [$cal(H) backslash cal(Z)$],
  sequenceh: $sequence_h$,
  sequenceI: $sequence_I$,
  sequenceha: $sequence_(h a)$,
)
#let information = (partition: [$cal(I)$])
#let strategyc = $strategy_c$
#let reachp = $P^(profile)$

= Modern Games Theory

== Normal Form Games


#definition([Normal Form Game])[
  A _Norma Form Game_ is a tuple $game$, where $players$ is finite set of _players_. Then $actions = times_(i in players) playeri.actions$ are tuples of _actions_ of all players, where $playeri.actions$ are actions of player $i$. The $utility = (playeri.utility)_(i in players)$ are players _utility functions_ such that $playeri.utility: actions arrow.r RR$.
]

If there are only two players we can fully describe the game with a table where each row and column represents the actions of player 1 and player 2 respectively and the value in the cell is the tuple of utility of the players.

#definition([Constant sum game])[
  The normal form game $game$ is called _constant sum game_ if for all $action in actions$ holds that $sum_(i in players) playeri.utility (action) = c$, for some constant $c in RR$.
]

#definition([Zero sum game])[
  The constant sum game $game$ is called _zero sum game_ if for all $action in actions$ holds that $sum_(i in players) playeri.utility (action) = 0$.
]

#definition([Pure Strategy])[
  We will call the action $playeri.action in playeri.actions$ a _pure strategy_ of player $i$.
]

#definition([Mixed Strategy])[
  The _mixed strategy_ of player $i$ is a probability distribution~$playeri.strategy in Delta(playeri.actions)$ over the set of actions $playeri.actions$.
]

#definition([Strategy Profile])[
  The _strategy profile_ is a tuple $profile = (playeri.strategy)_(i in players)$, where~$playeri.strategy in Delta(playeri.actions)$ is the mixed strategy of player $i$.
]

We will use the symbol $others.profile$ to denote the strategy profile of all players except player $i$.

Since all players are choosing their actions independently of others, the probability probability of action $action in actions$ happening, given strategy profile $profile$, is $P^(profile)(action) = product_(i in players) playeri.strategy (playeri.action)$.
Thus the expected value for player $i$ is $playeri.reward = sum_(action in actions) playeri.strategy (action) playeri.utility (action)$ .

#definition([Best Response])[
  The _best response_ of player $i$ to the strategy profile $others.profile$ of all players except player $i$ is $argmax_(playeri.strategy in Delta(playeri.actions)) playeri.rewardothers$. We will use $playeri.bestresponses (others.profile)$ to denote the set of all best responses of player $i$ to the strategy profile $others.profile$.
]


Note that in two player zero-sum games, player maximizing his expected utility is minimizing the expected utility of the other player.
$
argmax_(playeri.strategy in Delta(playeri.actions)) playeri.rewardothers = argmin_(playeri.strategy in Delta(playeri.actions)) playeroi.rewardgiveni
$

#definition([Support])[
  The _support_ of the mixed strategy $playeri.strategy$ is the set of actions with non-zero probability ${playeri.action in playeri.actions | playeri.strategy (playeri.actions) > 0}$.
]

#lemma([Best Response Lemma])[
  For any best response strategy $playeri.strategy in playeri.bestresponses (others.profile)$ to the strategy profile $others.profile$ it holds that the actions in the support of $playeri.strategy$ have the same expected value.
]

#proof[
  If this was not the case, then there would be two actions that have different expected value.
  Player $i$ would then be able to increase his expected value by moving the probability from the action with lower expected value to the action with higher expected value.
  This would mean that the strategy $playeri.strategy$ is not the best response to the strategy profile $others.profile$.
]

#lemma([Best Reponse Set is Convex])[
  The set $playeri.bestresponses (others.profile)$ is a convex set.
]

#let sa = playeri.strategya
#let sb = playeri.strategyb
#let sc = playeri.strategyc

#let rc = (playeri.rewardgiven)(sc)
#let ra = (playeri.rewardgiven)(sa)
#let rb = (playeri.rewardgiven)(sb)

#proof[

  Let $sa, sb in playeri.bestresponses (others.profile)$ be two best response strategies to the strategy profile $others.profile$ and $sc = lambda sa + (1 - lambda) sb$ be their convex combination.
  It simply follows that

  $
  rc
  &= sum_(action in actions) (lambda sa (playeri.action) + (1 - lambda) sb (playeri.action)) others.profile (others.action) \
  &= lambda sum_(action in actions) sa (playeri.action) others.profile (others.action) + (1 - lambda) sum_(action in actions) sb (playeri.action) others.profile (others.action) \
  &= lambda ra + (1 - lambda) rb.
  $

  It is clear that for each strategy $strategy in playeri.bestresponses (others.profile)$ we get the same expected value so even the convex combination of them is the same.
  In fact this should be proven for every finite set of strategies, but it simply follows using induction.
]

#definition([Nash Equilibrium])[
  The strategy profile $profile$ forms a _Nash Equilibrium_ if:

  $
  forall i in players, forall playeri.strategya in Delta(playeri.actions) : playeri.rewardothers >= ra
  $

  In other words for no player it is beneficial to deviate from their strategy in the profile $profile$.
]

#definition([Dominance])[
  We say that the strategy $sa$ _strictly dominates_ the strategy $sb$ if for all $others.profile$ holds that $ra > rb$.
  The strategy $sa$ _weakly dominates_ the strategy $sb$ if for all $others.profile$ holds that $ra >= rb$ and for at least one $others.profile$ the inequality is strict.
  Also the strategy $sa$ is _weakly/strongly dominated_ if there exists a strategy $sb$ such that $sb$ weakly/strongly dominates $sa$.
  The strategies $sa, sb$ are intransitive if one neither dominates nor is dominated by the other.
]

#observation[
  In two players game a strategy $sa$ of player $i$, is weakly dominated by strategy $sb$ if and only if for every pure strategy $others.profile$ of the oponent the expected reward $rb >= ra$ and for at least one it holds that $rb > ra$.
] <obs:dominated>

#algo(title: "GetWeaklyDominatedPureStrategy", parameters: ("game", "player"))[
  for $strategy^a$ in $playeri.actions$: #i #comment[Where $playeri.actions$ are actions of _player_] \
    for $strategy^b$ in $playeri.actions backslash {strategy^a}$: #i #comment[We are checking only pure strategies] \
      if $strategy^b$ weakly dominates $strategy^a$: #i #comment[Based on @obs:dominated]\
        return $strategy^a$ #d #d #d \
  return fail
]

We can see that if we are checking that the strategy $strategy^a$ is dominated only by pure strategies, we can be possibly missing cases where the strategy $strategy^a$ is dominated by mixed strategy.
As can be seen in the following example #footnote[https://en.wikipedia.org/wiki/Strategic_dominance#Iterated_elimination_of_strictly_dominated_strategies_(IESDS)]:

$
mat(
  (3, -1), (-1, 1);
  (0, 0), (0, 0);
  (-1, 0), (2, -1)
)
$

In this scenario there is no pure strategy that dominates another pure strategy.
But it is obious that the strategy $strategy_1^a = (1/2, 0, 1/2)$ strictly dominates the strategy $strategy_2^b = (0, 1, 0)$.
Thus the function #smallcaps([GetWeaklyDominatedPureStrategy]) is not sufficient to find all dominated strategies, but it is good enough for us.

#algo(title: "IteratedEliminationOfDominatedStrategies", parameters: ("game",))[
  while $s <- $ #smallcaps([GetWeaklyDominatedPureStrategy]) (_game_, player $1$ or player $2$): #i \
    remove $s$ from _game_ #d \

  if #no-emph[only one strategy for each player left in _game_]: #i \
    return #no-emph[the only left pure strategies left for player $1$ and $2$] #d \
  else: #i \
    return fail
]

The strategies returned by the function #smallcaps([IteratedEliminationOfDominatedStrategies]) or #smallcaps([Ieds]) will be _weakly dominant_ for each player.
The _weakly dominant_ strategy will be a Nash equilibrium, but beware that it does not have to be the only one.
Consider the following minimal example #footnote[https://en.wikipedia.org/wiki/Strategic_dominance#Dominance_and_Nash_equilibria]:

$
mat(
  (1, 1), (0, 0);
  (0, 0), (0, 0)
)
$

If we will consider the pure strategy profiles $((1, 0), (1, 0))$ and $((0, 1), (0, 1))$, then both of those are Nash equilibria, but only the first one is weakly dominant.

== Extensive Form Games

#let actions = [$cal(A)$]

To use the formalism of the _extensive form games_ we will need the following definitions.

Let $players = {1, 2, dots, n}$ be a finite set of _players_ and also let $playersc=players union {c}$ bet the set of players and a~_chance_ player $c$.
The~finite set~$histories.all$ will denote the set of _histories_ representing sequences of actions.
It holds that $forall (h, a) in histories.all arrow.r.double h in histories.all$ and we call $a$ an _action_.
We also use $h' subset.sq.eq h$ to denote that $h'$ is equal to or the prefix of $h$.
The terminal histories $histories.terminal$ are histories, that are not prefixes of any other history.
The~set~of~actions $cal(A)(h) = {a | (h, a) in histories.all}$ is the set of actions available at a non-terminal history~$h$.
The~function~$p: histories.nonterminal arrow.r playersc$ assigns each non-terminal history a player or the chance player.
It creates a partition over the non-terminal histories.
We will denote each of the partitions~$histories.all_i$ as _histories of player $i$_.
The~function~$strategyc: h in histories.all_c arrow.r.bar Delta(actions(h))$ which associates with each history of the chance player a~probability distribution over the available actions.
Let the _information partition_ be~$information.partition=(information.partition_i)_(i in players)$, where for each player $i$ the set $information.partition_i$ is a partition of the player histories $histories.all_i$.
The set $I in information.partition$ is the _information set_.
Each two histories $h, h' in I$ are indistinguishable for player $i$, so $actions(h) = actions(h')$ and we use~$actions(I)$ to denote the set of actions available at information set $I$. Let~$utility = (playeri.utility)_(i in profile)$, where~$playeri.utility : histories.terminal arrow.r RR$ is the utility function of player $i$.

The _extensive form game_ is defined as the following tuple $(histories.all, histories.terminal, actions, players, p, strategyc, utility, information.partition)$.

For the following discussion it needs to be mentioned that game in this form, forms a tree since the finiteness condition on the histories enforces the graph of the game to be acyclic.

The _behavioral strategy_ of player $i$ is a mapping $playeri.strategy : I in information.partition_i arrow.r.bar Delta(actions(I))$ that for each information set~$I in information.partition_i$ assigns a probability distribution over the available actions at $I$.
We note that the $strategyc$ is a behavioral strategy of the chance player.
The _behavioral profile_ is $profile = (playeri.strategy)_(i in players)$.
It is freely extended with the chance player's strategy $strategyc$ when needed and in that case we denote the behavioral profile as~$profile_c$.
We use the notation $playeri.strategy (I, a)$ to denote the probability of action $a$ at information set $I$ under the behavioral policy $playeri.strategy$. Also we use $profile(I, a) = strategy_(p(I))(I, a)$.

The _reach probability_ of a history $h in histories.all$ given behavioral profile $profile$ is $reachp (h) = product_((h', a) subset.sq.eq h) profile(h', a)$.
With this we are able to define the _expected utility_ of player $i$ given behavioral profile $profile$ as~$playeri.reward = sum_(h in histories.terminal) reachp (h) playeri.utility (h)$.

We will also introduce the notion of _sequence_ for each player~$i$ the $playeri.sequence (h)$, which is the sequence of actions of player~$i$ to a history $h in histories.all$, disregarding the actions of the other players.

Player $i$ has _perfect recall_ if for each two histories $h, h' in I, I in information.partition_i$ it holds that $playeri.sequence (h) = playeri.sequence (h')$.
In a game of _perfect recall_ each player has perfect recall.
Since each non-terminal history is assigned a specific player we will use $sequence_h$ instead of $playeri.sequence (h)$ freely.
Also in game of perfect recall for each $h, h' in I, sequence_(h) = sequence_(h')$ so we will use $sequence_I$ to denote the sequence of actions at information set $I$.
It is clear that in such games each sequence is uniquely determined by the last move in the last information set $I$, so $sequence = sequence_I a$.
This also holds for any non-empty history $h in histories.all, sequence_h = sequence_I a$ for some information set $I$.

From that we can define the _realization probability_ $realizationps (sequence_h)$ given a behavioral policy $strategy$ as~$realizationps (sequence_h) = product_(sequence_(h')a subset.sq.eq sequence_h) strategy(h', a)$.  
It is clear that such function must satisfy the folllowing constraints~$x(emptyset) = 1$ and $realizationps (sequence_h) = sum_(a in actions(h)) x(sequence_h a)$.
Function satisfying these constraints also gives us a the behavioral policy $strategy$, since $strategy(h, a) = (realizationps (sequence_(h a))) / realizationp_strategy(sequence_h)$ is a well defined probability distribution over actions $a in actions(h)$ for each history $ h in I, I in information.partition_i$.
Also the reach probability has simple equivalent in the realization probabilities, $reachp (h) = product_(i in playersc) playeri.realizationp (sequence_h)$.
From this we can see that the expected utility of player~$i$ may be written as

$
playeri.reward
&= sum_(h in histories.terminal) reachp(h) playeri.utility (h) \
&= sum_(h in histories.terminal)(product_(j in playersc) realizationp_(strategy_j)(sequence_h)) playeri.utility (h).
$


To simplify some of the future equations we will use the following notation, in the following form corresponds to the _counterfactual reach_ for player $i$, given a historyr $h$.

$
others.reachp (h) = product_(j in playersc backslash {i}) realizationp_(strategy_j)(sequence_h).
$

So we can write $reachp (h) = realizationp_(pi_i)(sequence_h) others.reachp (h)$.

We are now interested in averaging of two policies $sa$ and $sb$ for player $i$.
The property that we want from the~averaging is for any behavioral profile $profile$ to hold~$rc = 0.5 ra + 0.5 rb$.
With behavioral policies this is tricky to do right, but with realization probabilities it is fairly simple.
We will create a new averaged policy~$sc$ from policies $sa$ and $sb$ of player $i$ as policy $sc$, for which the following holds~$realizationp_sc (sequence_h) = 0.5 realizationp_sa (sequence_h) + 0.5 realizationp_sb (sequence_h)$.
Since this satisfy the consraints of the realization probabilities it also represents a behavioral policy. We can quickly inquire that the required property really holds for any behavioral profile $profile$.

$
rc
&= sum_(h in histories.terminal) reachp (h) playeri.utility (h) \
&= sum_(h in histories.terminal) realizationp_sc (sequence_h) others.reachp (h) playeri.utility (h) \
&= sum_(h in histories.terminal) (1/2 realizationp_(sa)(sequence_h) + 1/2 realizationp_(sb)(sequence_h)) others.reachp (h) playeri.utility (h) \
&= 1/2 ra + 1/2 rb
$

We will represent $playeri.futurereward (h) = sum_(h a, a in actions(h)) profile (h, a) playeri.futurereward (h a)$ for non-terminal history $h$ and $playeri.futurereward (h) = playeri.utility (h)$ for terminal ones.
We could also write $playeri.futurereward (h) = sum_(z in histories.terminal) reachp (z | h) playeri.utility (z)$.
Where $reachp (z | h)$ is the probability of reaching the terminal history $z$ given we are at history $h$ and we are following the behavioral profile $profile$.
It is easy to see that $playeri.reward = playeri.futurereward (emptyset)$.
We will call $playeri.futurereward (h)$, the _expected future reward_ under behavioural profile~$profile$ to player~$i$, given the history $h$.

We focus on a games of a perfect recall.
For a player $i$ let $I in information.partition_i$, $playeri.strategy$ be theirs behavioral policy and~$others.profile$ be the behavioral profile of the other players.
Set $profile = (playeri.strategy, others.profile)$.
It is clear that the contribution of the state $h$ to the value~$playeri.futurereward (emptyset)$ is~$reachp (h) playeri.futurereward (h)$.
Also since we are in game of perfect recall it holds that each two histories in the information set $I$ have disjoint subtrees, meaning that their contribution to the value $playeri.futurereward (emptyset)$ is independent of each other and we can sum them up.
Since for each $h, h' in I$ it holds that $sequence_h = sequence_h'$, we get that~$realizationps (sequence_h) = realizationps (sequence_h')$ and we will use $realizationps (sequence_I)$ to denote that realization probability of information set $I$.
So the contribution of the information set $I$ to the value $playeri.futurereward (emptyset)$ is

$
reachp (h) playeri.futurereward (I)&= sum_(h in I) reachp (h) playeri.futurereward (h) \
&= sum_(h in I) playeri.realizationp (sequence_h) others.reachp (h) playeri.futurereward (h) \
&= playeri.realizationp (sequence_I) sum_(h in I) others.reachp (h) playeri.futurereward (h).
$.

That means that each history in the information set $I$ contributes equally to the value $playeri.futurereward (emptyset)$ from the point of view of player $i$, since he can't make any of the two histories more likely to be reached.
We can also see that if we want to maximize the players $i$ expected future reward at information set $I$ we can maximize the two values $playeri.realizationp (sequence_I)$ and $sum_(h in I) others.reachp (h) playeri.futurereward (h)$ separately.
We note that the second value is dependent only on the subtree induced by the information set $I$, the behavioral profile $others.profile$ of the other players and player $i$ actions in following histories. Thus if we want to find the best policy for player $i$ we can form it bottom up, by first finding the best policy at the lower information sets and then using the best policies at the lower information sets to find the best policy at the higher information sets.

We will also use the $q_i^(profile)(h, a)$, which is the expected future reward of player $i$ given the history $h$ and choosing the action $a$ under the behavioral profile $profile$.
It is defined as $q_i^(profile)(h, a) = playeri.futurereward (h a)$, which would not be in itself interesting, but in the perfect information games we can define it for the information set $I in information.partition_i$ as $q_i^(profile)(I, a) = sum_(h in I) q_i^(profile)(h, a)$.
Now when deciding what action is the best response in information set $I$ to the behavioral profile $profile$ is we can succintly ask $a^star = argmax_{a in actions (I)} q_i^(profile)(I,a)$.



=== Counterfactual regret
Now we have already defined the counterfactual reach $others.reachp$, using this we can ask the following question. Given that player $i$ tries to reach the information set $I in information.partition_i$, what is his expected future reward at this information set $I$? And what would be his expected future reward if he was to choose the action $a$ at this information set $I$? The first question is answered by $playeri.futurerewardc = $