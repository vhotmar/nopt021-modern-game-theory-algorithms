import marimo

__generated_with = "0.2.1"
app = marimo.App()


@app.cell
def __():
    import week2
    import numpy as np
    import marimo as mo
    import altair as alt
    import pandas as pd

    data_x, data_y = week2.generate_data_points(np.array([[-1, 0, -0.8], [1, -1, -0.5]]))
    data = data = pd.DataFrame({
        "x": data_x,
        "f(x)": data_y,
    })

    chart = alt.Chart(data).mark_line().encode(
        x='x',
        y='f(x)'
    )


    # Make it reactive ⚡
    mo.ui.altair_chart(chart)
    return alt, chart, data, data_x, data_y, mo, np, pd, week2


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
