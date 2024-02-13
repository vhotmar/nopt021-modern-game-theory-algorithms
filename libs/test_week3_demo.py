import marimo

__generated_with = "0.2.1"
app = marimo.App()


@app.cell
def __():
    import marimo as mo
    import altair as alt
    import pandas as pd

    from test_utils import rock_paper_scissors
    from week3 import naive_fictitious_self_play, fictitious_self_play
    from week5 import fictitious_self_play as fictitious_self_play_regret, get_strategy_best_response, get_strategy_regret_matching

    import numpy as np
    return (
        alt,
        fictitious_self_play,
        fictitious_self_play_regret,
        get_strategy_best_response,
        get_strategy_regret_matching,
        mo,
        naive_fictitious_self_play,
        np,
        pd,
        rock_paper_scissors,
    )


@app.cell
def __(mo):
    mo.md(
        """
        # Week 3 and 5 - Normal Form Games
        """
    )
    return


@app.cell
def __():
    steps = 50
    return steps,


@app.cell
def __(mo):
    mo.md(
        """
        ## Rock Paper Scissors
        This result is expected, since for CFR we basically start with the uniform strategy that is the Nash Equilibria and in the Naive Fictitious Self Play we oscillate between the strategies.
        """
    )
    return


@app.cell
def __(
    alt,
    fictitious_self_play,
    fictitious_self_play_regret,
    get_strategy_best_response,
    get_strategy_regret_matching,
    mo,
    naive_fictitious_self_play,
    pd,
    steps,
):
    def plot_game(game):
        exploit_fic = fictitious_self_play(game, steps)[0]
        exploit_nai = naive_fictitious_self_play(game, steps)[0]
        exploit_reg, exploit_reg_cur, _ = fictitious_self_play_regret(game, -game, steps, strategy=get_strategy_regret_matching)
        exploit_fic_2, exploit_fic_2_cur, _ = fictitious_self_play_regret(game, -game, steps, strategy=get_strategy_best_response)

        data_x = list(range(steps))
        data = pd.DataFrame({
            "Step": data_x * 6,
            "Exploitablity": exploit_reg + exploit_reg_cur + exploit_fic + exploit_nai + exploit_fic_2 + exploit_fic_2_cur,
            "Type": (["CFR"] * steps) + (["CFR cur"] * steps) + (["Fictitious Self Play"] * steps) + (["Naive Fictitious Self Play"] * steps) + (["Fictitious Self Play 2"] * steps) + (["Fictitious Self Play 2 cur"] * steps)
        })


        chart = alt.Chart(data).mark_line().encode(
            x='Step',
            y='Exploitablity',
            color='Type'
        )


        return mo.ui.altair_chart(chart)
    return plot_game,


@app.cell
def __(plot_game, rock_paper_scissors):
    plot_game(rock_paper_scissors)
    return


@app.cell
def __(mo):
    mo.md(
        """
        ## Other games
        """)
    return


@app.cell
def __(np, plot_game):
    plot_game(np.array([[30, -10, 20], [-10, 20, -20]]))
    return


@app.cell
def __(np, plot_game):
    plot_game(np.array([[10, -2], [-3, 5]]))
    return


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
