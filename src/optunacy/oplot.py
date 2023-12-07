from matplotlib import pyplot as plt
import plotly.graph_objs as go
import matplotlib.ticker as ticker
import numpy as np
import scipy as scipy


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

    def get_values(name):
        values = []
        for trial in self.study.trials:
            if trial.state == optuna.trial.TrialState.COMPLETE:
                combined_dict = {**trial.params, **trial.user_attrs}
                for index, key in enumerate(objective_names):
                    combined_dict[key] = trial.values[index]
                if name in combined_dict:
                    values.append(combined_dict[name])
                else:
                    raise ValueError(
                        f"Parameter '{name}' not found in trial parameters or user attributes."
                    )
        return values

    def describe_trials(trials):
        i = 0
        results = []
        for trial in self.study.trials:
            desc = f"Trial: {trial.number}"
            for key, value in trial.params.items():
                if isinstance(value, (int, float)) and (value < 0.001 or value > 10000):
                    desc += f"<br>{key}: {value:.2e}"
                if isinstance(value, (float)):
                    desc += f"<br>{key}: {value:.4f}"
                else:
                    desc += f"<br>{key}: {value}"
            results.append(desc)
        return results

    def doIt(self):
        print("testing")

    def plot(x_name, y_name, z_name=None, x_range=None, y_range=None):
        trials = [
            trial
            for trial in study.trials
            if trial.state == optuna.trial.TrialState.COMPLETE
        ]
        x_values = self.get_values(x_name, trials)
        y_values = self.get_values(y_name, trials)
        z_values = self.get_values(z_name, trials) if z_name else None
        descriptions = self.describe_trials(trials)
        layout = 0
        if z_name:
            z_values = self.get_values(z_name, trials)

            # Create a grid for the contour plot
            xi = np.linspace(min(x_values), max(x_values), 100)
            yi = np.linspace(min(y_values), max(y_values), 100)
            X, Y = np.meshgrid(xi, yi)
            Z = scipy.interpolate.griddata(
                (x_values, y_values), z_values, (X, Y), method="cubic"
            )

            # Create contour plot
            contour = go.Contour(x=xi, y=yi, z=Z, colorscale="Viridis")

            # Create scatter plot with mouseovers for data points
            scatter = go.Scatter(
                x=x_values,
                y=y_values,
                mode="markers",
                marker=dict(color="black", size=5),
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
            # Create scatter plot with mouseovers
            scatter = go.Scatter(
                x=x_values,
                y=y_values,
                mode="markers",
                marker=dict(color="blue"),
                text=descriptions,  # Mouseover descriptions for each point
                hoverinfo="x+y+z+text",
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
        return fig
