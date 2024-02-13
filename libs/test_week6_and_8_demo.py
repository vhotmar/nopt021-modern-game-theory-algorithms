import marimo

__generated_with = "0.2.1"
app = marimo.App()


@app.cell
def __():
    import marimo as mo
    import altair as alt
    import pandas as pd

    from test_extensive_games import rock_paper_scissor_game, kuhn_poker

    from week6 import fictitious_self_play
    from week8 import fictitious_self_play_regret
    return (
        alt,
        fictitious_self_play,
        fictitious_self_play_regret,
        kuhn_poker,
        mo,
        pd,
        rock_paper_scissor_game,
    )


@app.cell
def __(mo):
    mo.md(
        """
        # Week 6 - Fictitious Self Play + CFR in EFG
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        """
        ## Kuhn Poker
        """
    )
    return


@app.cell
def __():
    steps = 200
    return steps,


@app.cell
def __(
    alt,
    fictitious_self_play,
    fictitious_self_play_regret,
    kuhn_poker,
    mo,
    pd,
    steps,
):
    _game = kuhn_poker()[0]

    _exploit_fic = fictitious_self_play(_game, steps)[0]
    _exploit_reg = fictitious_self_play_regret(_game, steps)[0]

    _data_x = list(range(steps))
    _data = pd.DataFrame({
        "Step": _data_x + _data_x,
        "Exploitablity": _exploit_reg + _exploit_fic,
        "Type": (["CFR"] * steps) + (["Fictitious Self Play"] * steps)
    })


    _chart = alt.Chart(_data).mark_line().encode(
        x='Step',
        y='Exploitablity',
        color='Type'
    )


    mo.ui.altair_chart(_chart)
    return


@app.cell
def __(mo):
    mo.md(
        """
        ## Rock Paper Scissor
        """
    )
    return


@app.cell
def __(
    alt,
    fictitious_self_play,
    fictitious_self_play_regret,
    mo,
    pd,
    rock_paper_scissor_game,
    steps,
):
    _game = rock_paper_scissor_game()

    _exploit_fic = fictitious_self_play(_game, steps)[0]
    _exploit_reg = fictitious_self_play_regret(_game, steps)[0]

    _data_x = list(range(steps))
    _data = pd.DataFrame({
        "Step": _data_x + _data_x,
        "Exploitablity": _exploit_reg + _exploit_fic,
        "Type": (["CFR"] * steps) + (["Fictitious Self Play"] * steps)
    })


    _chart = alt.Chart(_data).mark_line().encode(
        x='Step',
        y='Exploitablity',
        color='Type'
    )


    mo.ui.altair_chart(_chart)
    return


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
