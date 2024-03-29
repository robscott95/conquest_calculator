
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math
import numpy as np

from data_model import EngagementDataModel
from stats import Stats

class VisualizeRollEstimation:
    def __init__(self, data: EngagementDataModel):
        self.data = data
        self.stats = Stats()

    @staticmethod
    def _visualize_expected_rolls(total_dice, successful_rolls, wounds_inflicted):
        # Prepare the data
        data = {
            'Outcome': ['Thrown', 'Hits', 'Wounds'],
            'Count': [total_dice, successful_rolls, wounds_inflicted]
        }
        
        # Create an interactive Plotly figure
        fig = px.bar(data, x='Outcome', y='Count', text='Count',
                    title="Dice Roll Outcomes",
                    color='Outcome', 
                    color_discrete_sequence=px.colors.qualitative.Plotly)
        
        # Add hover data
        fig.update_traces(texttemplate='%{text}', textposition='outside', hoverinfo='x+y')
        
        # Improve layout
        fig.update_layout(xaxis_title="Outcome", yaxis_title="Number of Dice")
        
        return fig
    
    @staticmethod
    def visualize_expected_dice_outcomes(total_dice, successful_rolls, wounds_inflicted):
        colors = ['#AFE07D', '#F4CD54', '#FE8D64']

        # Calculate proportions
        if successful_rolls > 0:
            remaining_dice_proportion = total_dice - successful_rolls
        else:
            remaining_dice_proportion = total_dice - wounds_inflicted
        successful_rolls_proportion = successful_rolls - wounds_inflicted
        wounds_inflicted_proportion = wounds_inflicted

        fig = go.Figure()

        # Add traces for Total Dice Thrown, Successful Rolls, and Wounds Inflicted
        fig.add_trace(go.Bar(
            x=[remaining_dice_proportion],
            y=[1],
            orientation='h',
            name='Total Dice',
            marker=dict(color=colors[0]),
            text=[total_dice],  # Display the number on the bar
            textposition='inside',  # Position the text inside the bar
            hovertemplate='<b>Total Dice</b>: %{text}<extra></extra>',
            textfont=dict(size=18, color='#0e1117')
        ))
        
        if successful_rolls != 0:
            fig.add_trace(go.Bar(
                x=[successful_rolls_proportion],
                y=[1],
                orientation='h',
                name='Hits',
                marker=dict(color=colors[1]),
                text=[successful_rolls],  # Display the number on the bar
                textposition='inside',  # Position the text inside the bar
                hovertemplate='<b>Hits</b>: %{text}<extra></extra>',
                textfont=dict(size=18, color='#0e1117')
            ))
        
        fig.add_trace(go.Bar(
            x=[wounds_inflicted_proportion],
            y=[1],
            orientation='h',
            name='Wounds',
            marker=dict(color=colors[2]),
            text=[f"<b>{wounds_inflicted}</b>"],  # Display the number on the bar
            textposition='inside',  # Position the text inside the bar
            hovertemplate='<b>Wounds</b>: %{text}<extra></extra>',
            textfont=dict(size=18, color='#0e1117')
        ))

        # fig.update_yaxes(automargin=True)
        fig.update_traces(marker_line_width=0)    # Optional: Adjust bar thickness and plot height for a tighter fit
        # fig.update_traces(width=1000)  # Adjusting the bar width for a tighter fit
    
        return fig
    
    def visualize_expected_hits(self):
        fig = self.visualize_expected_dice_outcomes(
            round(self.data.active_number_of_attacks, 2), 
            round(self.data.expected_hits, 2), 
            round(self.data.expected_wounds_from_hits, 2)
        )
        return fig

    def visualize_expected_morale(self):
        fig = self.visualize_expected_dice_outcomes(
            round(self.data.expected_wounds_from_hits, 2), 
            0,
            round(self.data.expected_wounds_from_morale, 2)
        )
        return fig
    
    def visualize_expected_hits_and_morale(self):
        titles = ["To hit", "Morale"]
    
        # Create a subplot layout: 2 rows, 1 column
        fig = make_subplots(rows=2, cols=1, subplot_titles=titles, vertical_spacing=0.15)
        
        # Generate and add each subplot. Adjust these parameters as per your actual data
        hits_fig = self.visualize_expected_hits()
        morale_fig = self.visualize_expected_morale()
        
        # Since we cannot directly add figures to subplots, we extract data and layout from each and add to the main figure
        for trace in hits_fig.data:
            fig.add_trace(trace, row=1, col=1)
            
        for trace in morale_fig.data:
            # remove traces
            trace.showlegend = False  # Disable legend for this trace
            fig.add_trace(trace, row=2, col=1)
        
        # Update layout if necessary
        fig.update_xaxes(title_text='', showticklabels=False, zeroline=False, row=1, col=1)
        fig.update_xaxes(title_text='', showticklabels=False, zeroline=False, row=2, col=1)
        fig.update_yaxes(title_text='', showticklabels=False, zeroline=False, row=1, col=1)
        fig.update_yaxes(title_text='', showticklabels=False, zeroline=False, row=2, col=1)
        fig.update_layout(
            barmode='stack',
            xaxis=dict(title='', showticklabels=False, zeroline=False),
            yaxis=dict(title='', showticklabels=False, zeroline=False),
            margin=dict(l=10, r=10, t=30, b=0),  # Minimize margins
            height=200,  # Adjust for a tighter fit vertically
            paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
            plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
            hoverlabel=dict(
                bgcolor="white",
                font_color='black',
                font_size=20,
            ),
            dragmode=False,
            legend=dict(
                orientation="h",  # Makes the legend horizontal
                xanchor="center",  # Anchors the legend to the center
                x=0.5,  # Positions the legend in the center of the axis (0.5 on a scale of 0 to 1)
                y=-0.2,  # Positions the legend below the x-axis. Adjust as needed.
                yanchor="bottom",  # Anchors the y position of the legend from its top.
            ),
            legend_itemclick=False,
            legend_itemdoubleclick=False,
        )
        # Apply layout of individual plots if needed, or make further adjustments
        
        return fig
    
    def visualize_simulated_discrete_and_cumulative_distributions(self, mode):
        if mode == "hits":
            target = self.data.target_to_hit
            title = f"To Hit | Target: {target})"
        elif mode == "defense":
            target = self.data.target_defense
            title = f"Defense | Target: {target})"
        elif mode == "morale":
            if self.data.encounter_params['action_type'] == "Volley":
                target = 6
            else:
                target = self.data.target_resolve
            title = f"Morale | Target: {target})"

        simulation_results = self.stats.simulate_rolls_by_type(self.data, mode)

        fig = go.Figure()

        # Add traces for discrete and cumulative probabilities
        fig.add_trace(go.Bar(x=simulation_results["full_range"], y=simulation_results["discrete_probabilities"], name='Discrete', marker=dict(color='rgba(55, 128, 191, 0.7)')))
        fig.add_trace(go.Scatter(x=simulation_results["full_range"], y=simulation_results["cumulative_probabilities"], name='Cumulative', xaxis="x", yaxis="y2", mode='lines+markers', marker=dict(color='rgba(219, 64, 82, 0.6)')))

        # Calculate mean or mode for annotation
        mean_value = np.average(simulation_results["full_range"], weights=simulation_results["discrete_probabilities"])

        # Add an annotation for the mean value directly on the x-axis
        fig.add_annotation(
            x=mean_value, y=0,  # Adjust y to place the annotation just below the x-axis
            xref="x", yref="y2",  # Use paper ref for y to position relative to the figure's height
            text=f"Mean: {mean_value:.2f}",
            showarrow=True,
            arrowhead=1,
            arrowsize=1,
            arrowwidth=2,
            ax=0,
            ay=0,
            bgcolor="rgba(255, 255, 255, 0.8)",  # Semi-transparent white background
            bordercolor="Black",
            borderwidth=0.5,
            font=dict(color="Black", size=12)
        )
        fig.add_shape(
            type="line", 
            x0=mean_value, y0=0, x1=mean_value, y1=1.05,  # Adjust these to control the line's direction and length
            line=dict(color="black", width=3),  # Thick white line
            yref="y2"
        )
        fig.add_shape(
            type="line", 
            x0=mean_value, y0=0, x1=mean_value, y1=1.05,  # Adjust these to control the line's direction and length
            line=dict(color="white", width=2),  # Thick white line
            yref="y2"
        )

        # Layout configuration, including manual y-axis settings
        fig.update_layout(
            title=title,
            xaxis_title='Success Count',
            yaxis=dict(title='Discrete Probability (%)', tickformat='.0%', side="left", showgrid=True),
            yaxis2=dict(title='Cumulative Probability (%)', overlaying='y', side='right', range=[0, 1],
                        tickvals=[0.25, 0.5, 0.75], showgrid=True, gridcolor='#BE445B', griddash='dash',
                        tickformat='.0%'),
            showlegend=False,
            hovermode='x unified'
        )

        return fig

    def visualize_simulated_all(self):
        titles = [
            f"To Hit |{self.data.target_to_hit}|", 
            f"Defense |{self.data.target_defense}|",
            f"Morale |{self.data.target_resolve if self.data.encounter_params['action_type'] != 'Volley' else 'WIN'}|"
        ]

        # Initialize subplot with secondary Y-axis configuration for each column.
        fig = make_subplots(rows=1, cols=3, subplot_titles=titles,
                            specs=[[{"secondary_y": True}, {"secondary_y": True}, {"secondary_y": True}]],
                            horizontal_spacing=0.05)  # Adjust spacing as needed

        modes = ["hits", "defense", "morale"]

        for i, mode in enumerate(modes, start=1):
            temp_fig = self.visualize_simulated_discrete_and_cumulative_distributions(mode)
            for trace in temp_fig.data:
                secondary_y = 'yaxis' in trace and trace.yaxis == 'y2'
                trace.hovertemplate = trace.name + ': %{y:.0%}<extra></extra>'
                trace.showlegend = i == 2  # Show legend only for the second plot
                fig.add_trace(trace, row=1, col=i, secondary_y=secondary_y)
                fig.add_annotation(temp_fig.layout.annotations[0], col=i, row=1)
                fig.add_shape(temp_fig.layout.shapes[0], col=i, row=1)
                fig.add_shape(temp_fig.layout.shapes[1], col=i, row=1)

        # # Configure the primary Y-axis (left) to be visible only on the first plot
                
        fig.update_yaxes(title_text='Discrete Probability (%)', tickformat='.0%', showgrid=True, 
                        secondary_y=False, row=1)

        # # Configure the secondary Y-axis (right) to be visible only on the last plot
        fig.update_yaxes(title_text='Cumulative Probability (%)', tickformat='.0%', showgrid=True, range=[0, 1],
                        tickvals=[.25, .5, .75], row=1, secondary_y=True, gridcolor='#BE445B', griddash='dash')

        # Set X-axis titles individually for each subplot
        for i in range(1, 4):
            fig.update_xaxes(title_text='Success Count', row=1, col=i)

        fig.update_layout(
            yaxis2 = dict(
                title = {'text': ''},
                showticklabels=False,
            ),
            yaxis3 = dict(
                title = {'text': ''},
                showticklabels=False,
            ),
            yaxis4 = dict(
                title = {'text': ''},
                showticklabels=False,
            ),
            yaxis5 = dict(
                title = {'text': ''},
                showticklabels=False,
            ),
        )

        fig.update_layout(
            height=300,  # Adjust height as necessary
            width=1200,  # Adjust width as necessary for 3 columns
            hovermode='x unified',
            legend=dict(
                orientation="h",  # Makes the legend horizontal
                xanchor="center",  # Anchors the legend to the center
                x=0.49,  # Positions the legend in the center of the axis (0.5 on a scale of 0 to 1)
                y=1.3,  # Positions the legend below the x-axis. Adjust as needed.
                yanchor="top",  # Anchors the y position of the legend from its top.
            ),
            legend_itemclick=False,
            margin=dict(l=10, r=10, t=30, b=0),  # Minimize margins
        )

        return fig