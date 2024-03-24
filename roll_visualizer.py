
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
            hovertemplate='<b>Total Dice</b>: %{text}<extra></extra>',
            textfont=dict(size=18, color='#0e1117', family='Droid Sans')
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
                textfont=dict(size=18, color='#0e1117', family='Droid Sans')
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
            textfont=dict(size=18, color='#0e1117', family='Droid Sans')
        ))

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
        hits_fig = self.visualize_hits()
        morale_fig = self.visualize_morale()
        
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
                yanchor="top",  # Anchors the y position of the legend from its top.
                traceorder='reversed'
            ),
            legend_itemclick=False,
            legend_itemdoubleclick=False,
        )
        # Apply layout of individual plots if needed, or make further adjustments
        
        return fig