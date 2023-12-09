from matplotlib import pyplot as plt
import plotly.graph_objs as go
from plotly.offline import iplot, init_notebook_mode
import matplotlib.ticker as ticker
import numpy as np
import scipy as scipy
from optuna.trial import TrialState


class OPlot:
    def __init__(self, study, objective_names=[], inlinePlotting=False):
        """Initialize class with study.
        If objective_names is empty, no objectives can be shown.
        :param study: Optuna study object
        :param inlinePlotting: If True, plots will be shown in the notebook and stored in the notebook file.
        :param objective_names: List of objective names to show,
                                the string names of the objectives i
                                returned from the objective function
        """
        self.study = study
        self.inlinePlotting = inlinePlotting
        self.objective_names = objective_names
        init_notebook_mode(connected=True)  # Plots remain in Notebook

    def parameters(self, wherefrom=True):
        """List all the parameters in the study. Includes parameters, user attributes, and objectives.
        :param wherefrom: If True, print the type of parameter '"Accuacy": [Objective]', if false, just the strings.
        :return: List of parameter names
        """
        params = (
            {}
        )  # Keys are parameters, values are the string representing the source
        for trial in self.study.trials:
            for key in trial.params.keys():
                params[key] = "Parameter"
            for key in trial.user_attrs.keys():
                params[key] = "User Attribute"
            for index, key in enumerate(self.objective_names):
                params[key] = "Objective"
        if wherefrom:
            return params
        else:
            return list(params.keys())

    def get_values(self, trials, name):
        """Get the values of a parameter, user attribute, or objective.
        :param trials: List of trials to get values from
        :param name: Name of parameter, user attribute, or objective
        :return: List of values
        """
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
        """Format a value for display in a plot.
        Tries to be reasonable and use exponential notation for very small or large numbers.
        :param value: Value to format
        :return: Formatted value
        """
        if isinstance(value, (int, float)) and (value < 0.001 or value > 10000):
            return f"{value:.2e}"
        if isinstance(value, (float)):
            return f"{value:.4f}"
        else:
            return f"{value}"

    def describe_trials(self, trials):
        """Describe a list of trials with their parameters, user attributes, and objectives.
        This is used for the mouseovers in the plots.
        :param trials: List of trials to describe
        :return: List of descriptions
        """
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
        """Create a plot of two parameters, user attributes, or objectives.
        :param x_name: Name of parameter, user attribute, or objective for x axis
        :param y_name: Name of parameter, user attribute, or objective for y axis
        :param z_name: Name of parameter, user attribute, or objective for z axis
        :param x_range: Range for x axis (optional
        :param y_range: Range for y axis (optional)
        :param z_clip: Range for z axis (optional). This clips the colors and contours of the plot, so that
                       you can see the shape of the plot more easily. It compresses everything beyond the extremes to the respective extreme.
        :param interpol: Interpolation method for the contour plot. See scipy.interpolate.griddata for options.
        :return: Plotly plot
        """
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
        if self.inlinePlotting:
            iplot(fig)
        else:
            plot(fig)
