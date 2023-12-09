from matplotlib import pyplot as plt
import plotly.graph_objs as go
from plotly.offline import iplot, init_notebook_mode
import matplotlib.ticker as ticker
import numpy as np
import scipy as scipy
from optuna.trial import TrialState


class OPlot:
    def __init__(self, study, objective_names=[]):
        """Initialize class with study.
        If objective_names is empty, no objectives can be shown.
        :param study: Optuna study object
        :param objective_names: List of objective names to show,
                                the string names of the objectives i
                                returned from the objective function
        """
        self.study = study
        self.objective_names = objective_names
        init_notebook_mode(connected=True)  # Plots remain in Notebook

    def get_values(self, trials, name):
        values = []
        for trial in trials:
            if trial.state == TrialState.COMPLETE:
                combined_dict = {**trial.params, **trial.user_attrs}
                for index, key in enumerate(self.objective_names):
                    combined_dict[key] = trial.values[index]
                if name in combined_dict:
                    values.append(combined_dict[name])
                else:
                    raise ValueError(
                        f"Parameter '{name}' not found in trial parameters or user attributes."
                    )
        return values

    def format_value(self, value):
        if isinstance(value, (int, float)) and (value < 0.001 or value > 10000):
            return f"{value:.2e}"
        if isinstance(value, (float)):
            return f"{value:.4f}"
        else:
            return f"{value}"

    def describe_trials(self, trials):
        i = 0
        results = []
        for trial in trials:
            desc = f"Trial: {trial.number}"
            for key, value in trial.params.items():
                valstr = self.format_value(value)
                desc += f"<br>{key}: {valstr}"
            for idx, key in enumerate(self.objective_names):
                valstr = self.format_value(trial.values[idx])
                desc += f"<br><i>{key}: {valstr}</i>"
            results.append(desc)
        return results

    def plot(
        self,
        x_name,
        y_name,
        z_name=None,
        x_range=None,
        y_range=None,
        z_clip=None,
        interpol="linear",
    ):
        trials = [
            trial for trial in self.study.trials if trial.state == TrialState.COMPLETE
        ]
        x_values = self.get_values(trials, x_name)
        y_values = self.get_values(trials, y_name)
        descriptions = self.describe_trials(trials)

        layout = 0
        if z_name:
            z_values = self.get_values(trials, z_name)

            # Create a grid for the contour plot
            xi = np.linspace(min(x_values), max(x_values), 100)
            yi = np.linspace(min(y_values), max(y_values), 100)
            X, Y = np.meshgrid(xi, yi)
            Z = scipy.interpolate.griddata(
                (x_values, y_values), z_values, (X, Y), method=interpol
            )
            if z_clip:
                Z = np.clip(Z, z_clip[0], z_clip[1])

            # Create contour plot
            contour = go.Contour(x=xi, y=yi, z=Z, colorscale="Viridis")

            # Create scatter plot with mouseovers for data points
            scatter = go.Scatter(
                x=x_values,
                y=y_values,
                mode="markers",
                marker=dict(color="white", size=5, line=dict(color="black", width=3)),
                text=descriptions,
                hoverinfo="x+y+z+text",
            )

            layout = go.Layout(
                title=f"{x_name} vs {y_name}" + (f" with {z_name}" if z_name else ""),
                xaxis=dict(title=x_name, range=x_range),
                yaxis=dict(title=y_name, range=y_range),
                hovermode="closest",  # Configure hover mode
                annotations=[
                    dict(
                        text=z_name,  # Text you want to display
                        showarrow=False,
                        xref="paper",  # Use 'paper' for relative positioning
                        yref="paper",
                        x=1.03,  # X position (just right of the colorbar)
                        y=0.5,  # Y position (center vertically)
                        textangle=-90,  # Angle of the text (vertical)
                    )
                ],
            )

            data = [contour, scatter]
        else:
            # Filter out the undesired ones
            # Much optimization can be done here; later.
            x_n = []
            y_n = []
            d_n = []

            # Create scatter plot with mouseovers
            scatter = go.Scatter(
                x=x_values,
                y=y_values,
                mode="markers",
                marker=dict(color="blue"),
                text=descriptions,  # Mouseover descriptions for each point
                hoverinfo="x+y+text",
            )

            data = [scatter]

            # Create layout
            layout = go.Layout(
                title=f"{x_name} vs {y_name}" + (f" with {z_name}" if z_name else ""),
                xaxis=dict(title=x_name, range=x_range),
                yaxis=dict(title=y_name, range=y_range),
                hovermode="closest",  # Configure hover mode
            )

        # Create figure and add data
        fig = go.Figure(data=data, layout=layout)
        iplot(fig)
