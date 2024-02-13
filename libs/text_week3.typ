#import "@preview/ctheorems:1.1.0": *

#show: thmrules

#set par(justify: true)
#set heading(numbering: "1.1.")

#let definition = thmbox("definition", "Definition")
#let theorem = thmbox("theorem", "Theorem")
#let lemma = thmbox("theorem", "Lemma")
#let proof = thmplain(
  "proof",
  "Proof",
  base: "theorem",
  bodyfmt: body => [#body #h(1fr) $square$]
).with(numbering: none)

#let ri = $R_(i)^(pi_i, pi_(-i))$
#let rpi = $R_(i)^(pi'_i, pi_(-i))$
#let ori = $R_(-i)^(pi_i, pi_(-i))$
#let players = $cal(N)$

#let argmax = math.op("arg max", limits: true)
#let argmin = math.op("arg min", limits: true)

= Nash Equilibrium and Maximin

#definition([Nash Equilibrium])[
  A strategy profile $(pi_i, pi_(-i))$ forms a _Nash equilibrium_ if none of the players benefit by deviating from their policy.

  $
  forall i in players, forall pi'_i : ri >= rpi
  $
] <def:nash-equilibrium>

#lemma[
  Strategy profile $(pi_i, pi_(-i))$ forms a Nash equilibrium if and only if

  $
  forall i in players : pi_i #[is a best response to] pi_(-i)
  $

  Where _best response_ to $pi_(-i)$ is $pi_(i)^star = argmax_(pi_i) ri$.
] <lem:best-response>

#definition([Maximin Policy])[
  Maximin policy of a player $i$ is:

  $
  argmax_(pi_i) min_(pi_(-i)) ri
  $
]

#theorem([Minimax])[
  $
  max_(pi_i) min_(pi_(-i)) ri = min_(pi_(-i)) max_(pi_i) ri
  $
] <thm:minimax>

#let vi = $underline(v_i)$
#let vmi = $underline(v_(-i))$

We will denote $vi = max_(pi_i) min_(pi_(-i)) ri = - max_(pi_i) min_(pi_(-i)) ori = vmi$.

#theorem([Nash is Maximin])[
  For a two player zero-sum game:

  $
  (pi_i, pi_(-i)) #[is a Nash equilibrium] arrow.r.double pi_i #[is a maximin policy] and pi_(-i) #[is a maximin policy]
  $
]

#proof[
  WLOG we will talk only about player $i$.
  First we can see that since $pi_(-i)$ is the best response from @lem:best-response.
  Suppose that there is an another policy $pi'_i$ that does better than $pi_i$ in the worst case. That $min_(pi^star_(-i)) R_i^(pi'_i, pi^star_(-i)) > min_(pi^star_(-i)) R_i^(pi_i, pi^star_(-i))$. So even:

  $
  R_i^(pi'_i, pi_(-i))
  >= min_(pi^star_(-i)) R_i^(pi'_i, pi^star_(-i))
  > min_(pi^star_(-i)) R_i^(pi_i, pi^star_(-i))
  =^#[@lem:best-response] ri
  >=^#[@def:nash-equilibrium] rpi
  $

  This is a contradiction. Which concludes the proof.
]

#theorem([Maximin is Nash])[
  For a two player zero-sum game:

  $
  pi^star_i #[is a maximin policy] and pi^star_(-i) #[is a maximin policy]
  arrow.r.double 
  (pi^star_i, pi^star_(-i)) #[is a Nash equilibrium] 
  $
]

#proof[
  Suppose that $(pi_i, pi_(-i))$ is not Nash equilibrium.
  Then there is a policy $pi'_i$ such that $R_i^(pi'_i, pi^star_(-i)) > R_i^(pi^star_i, pi^star_(-i))$.
  And with that immediately follows:

  $
  vi
  =^#[@thm:minimax] -vmi
  >=^#[$pi^star_(-i)$ is maximin] -R_(-i)^(pi'_i, pi^star_(-i))
  =^#[zero-sum game] R_i^(pi'_i, pi^star_(-i))
  > R_i^(pi^star_i, pi^star_(-i))
  >= vi
  $

  This is a contradiction. Which concludes the proof.
]