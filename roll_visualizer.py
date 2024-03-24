
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math

from data_model import EngagementDataModel

class VisualizeRollEstimation:
    def __init__(self, data: EngagementDataModel):
        self.data = data

    @staticmethod
    def _visualize_rolls(total_dice, successful_rolls, wounds_inflicted):
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
    
    # TODO: Refactor the visualization part to another file
    @staticmethod
    def visualize_dice_outcomes(total_dice, successful_rolls, wounds_inflicted):
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
            hovertemplate='<b>Total Dice</b>: %{x}<extra></extra>'
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
                hovertemplate='<b>Hits</b>: %{x}<extra></extra>'
            ))
        
        fig.add_trace(go.Bar(
            x=[wounds_inflicted_proportion],
            y=[1],
            orientation='h',
            name='Wounds',
            marker=dict(color=colors[2]),
            text=[wounds_inflicted],  # Display the number on the bar
            textposition='inside',  # Position the text inside the bar
            hovertemplate='<b>Wounds</b>: %{x}<extra></extra>'
        ))
        
        # Customize layout to remove x-axis title and hide the legend
            # Adjust layout for a snug fit
        fig.update_layout(
            barmode='stack',
            xaxis=dict(title='', showticklabels=False, zeroline=False),
            yaxis=dict(title='', showticklabels=False, zeroline=False),
            margin=dict(l=0, r=0, t=0, b=0),  # Minimize margins
            height=200,  # Adjust for a tighter fit vertically
            paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
            plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
            showlegend=False,
            hoverlabel=dict(
                bgcolor="white",
                font_color='black',
                font_size=13,
            )
        )

        # fig.update_yaxes(automargin=True)
        fig.update_traces(marker_line_width=0)    # Optional: Adjust bar thickness and plot height for a tighter fit
        # fig.update_traces(width=1000)  # Adjusting the bar width for a tighter fit
    
        return fig
    
    def visualize_hits(self):
        fig = self.visualize_dice_outcomes(
            round(self.data.active_number_of_attacks, 2), 
            round(self.data.expected_hits, 2), 
            round(self.data.expected_wounds_from_hits, 2)
        )
        return fig

    def visualize_morale(self):
        fig = self.visualize_dice_outcomes(
            round(self.data.expected_wounds_from_hits, 2), 
            0,
            round(self.data.expected_wounds_from_morale, 2)
        )
        return fig
    
    def visualize_hits_and_morale(self):
        titles = ["To hit", "Morale"]
    
        # Create a subplot layout: 2 rows, 1 column
        fig = make_subplots(rows=2, cols=1, subplot_titles=titles, vertical_spacing=0.15)
        
        # Generate and add each subplot. Adjust these parameters as per your actual data
        action1_fig = self.visualize_hits()
        action2_fig = self.visualize_morale()
        
        # Since we cannot directly add figures to subplots, we extract data and layout from each and add to the main figure
        for trace in action1_fig.data:
            fig.add_trace(trace, row=1, col=1)
            
        for trace in action2_fig.data:
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
            showlegend=False,
            hoverlabel=dict(
                bgcolor="white",
                font_color='black',
                font_size=13,
            )
        )
        # Apply layout of individual plots if needed, or make further adjustments
        
        return fig