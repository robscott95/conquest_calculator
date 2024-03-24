import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class EngagementDataModel:
    def __init__(
            self,
            active_input_target_value,
            active_input_number_of_attacks_value,
            active_input_stands,
            active_input_attacking_stands,
            active_input_special_abilities,
            target_input_defense_value,
            target_input_evasion_value,
            target_input_resolve_value,
            target_input_stands,
            target_input_special_abilities,
            encounter_params,
        ):
        self.active_input_target_value = active_input_target_value
        self.active_input_number_of_attacks_value = active_input_number_of_attacks_value
        self.active_input_stands = active_input_stands
        self.active_input_attacking_stands = active_input_attacking_stands
        self.target_input_defense_value = target_input_defense_value
        self.target_input_evasion_value = target_input_evasion_value
        self.target_input_resolve_value = target_input_resolve_value
        self.target_input_stands = target_input_stands

        self.encounter_params = encounter_params

        self.active_input_special_abilities = active_input_special_abilities
        self.target_input_special_abilities = target_input_special_abilities

        self.active_input_supporting_stands = active_input_stands - active_input_attacking_stands
    
    @property
    def target_regiment_size_resolve_bonus(self):
        if 4 <= self.target_input_stands <= 6:
            return 1
        elif 7 <= self.target_input_stands <= 9:
            return 2
        elif 9 <= self.target_input_stands:
            return 3
        else:
            return 0
        
    def _get_rerolls_dict_hits(self):
        rerolls_dict = {
            key.replace("is_", ""): ability["value"] for key, ability in self.active_input_special_abilities.items()
            if "reroll" in key and ability.get("value") is True
        }
        
        # Apply negation logic
        # If is_reroll_misses is True, negate is_reroll_6s
        if 'reroll_misses' in rerolls_dict:
            rerolls_dict.pop('reroll_6s', None)  # Remove 'reroll_6s' if it exists
        
        # If is_reroll_hits is True, negate is_reroll_1s
        if 'reroll_hits' in rerolls_dict:
            rerolls_dict.pop('reroll_1s', None)  # Remove 'reroll_1s' if it exists
        
        return rerolls_dict
        
    def _calc_expected_success(self, number_of_die, target, invert_p=False, reroll_1s=False, reroll_6s=False, reroll_hits=False, reroll_misses=False):
        p_success = target / 6
        p_fail = 1 - p_success

        if invert_p:
            p_success, p_fail = p_fail, p_success

        # Adjust probabilities for rerolling 1s and 6s
        if reroll_6s:
            # If rerolling 6s, effectively reduce the failure probability by the chance of failing and then succeeding.
            p_fail -= (1/6) * p_success
            p_success += (1/6) * p_success

        if reroll_1s:
            # If rerolling 1s, effectively reduce the success probability by the chance of succeeding and then failing.
            p_success -= (1/6) * p_fail
            p_fail += (1/6) * p_fail

        # Calculate initial expected successes and failures
        expected_success = number_of_die * p_success
        expected_fail = number_of_die * p_fail

        # Adjust for rerolling hits or misses
        if reroll_hits:
            # Rerolling hits means taking the expected_success, applying the fail probability, and adding those successes back in
            expected_success -= expected_success * p_fail

        if reroll_misses:
            # Rerolling misses means taking the expected_fail, applying the success probability, and adding those successes
            expected_success += expected_fail * p_success

        return expected_success

    @property
    def active_number_of_attacks(self):
        if self.encounter_params['action_type'] == "Clash":
            support_mod =  max(self.active_input_special_abilities['support_mod']['value'], 1)
        elif self.encounter_params['action_type'] == "Volley":
            support_mod = 0
        
        support_to_hits = (self.active_input_supporting_stands * support_mod)
        number_of_attacks = (self.active_input_number_of_attacks_value * self.active_input_attacking_stands)
        number_of_attacks = number_of_attacks + support_to_hits + self.active_input_special_abilities['is_leader']['value']

        if self.active_input_special_abilities['is_double_hits_on_1s']['value']:
            number_of_attacks += number_of_attacks * 1/6

        return number_of_attacks
    
    @property
    def target_resolve(self):
        if self.target_input_special_abilities['broken']:
            return self.target_input_resolve_value
        return self.target_input_resolve_value + self.target_regiment_size_resolve_bonus

    @property
    def active_target(self):
        return self.active_input_target_value
    
    @property
    def target_defense(self):
        defense_value = self.target_input_defense_value
        if self.active_input_special_abilities['cleave']['value'] > 0:
            defense_value -= self.active_input_special_abilities['cleave']['value']

        return max(defense_value, self.target_input_evasion_value)

    @property
    def expected_hits(self):
        rerolls_params = self._get_rerolls_dict_hits()
        return self._calc_expected_success(self.active_number_of_attacks, self.active_input_target_value, **rerolls_params)

    @property
    def expected_wounds_from_hits(self):
        return self._calc_expected_success(self.expected_hits, self.target_defense, invert_p=True)
    
    @property
    def expected_wounds_from_morale(self):
        if self.encounter_params['action_type'] == "Clash":
            expected_wounds = self._calc_expected_success(self.expected_wounds_from_hits, self.target_resolve, invert_p=True)
        elif self.encounter_params['action_type'] == "Volley":
            expected_wounds = 0
        
        return expected_wounds

    @property
    def expected_wounds_from_all(self):
        hit_wounds = self.expected_wounds_from_hits
        morale_wounds = self.expected_wounds_from_morale

        return hit_wounds + morale_wounds
    
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
        
        fig = go.Figure()

        # Add traces for Total Dice Thrown, Successful Rolls, and Wounds Inflicted
        fig.add_trace(go.Bar(
            x=[total_dice],
            y=[1],
            orientation='h',
            name='Total Dice',
            marker=dict(color=colors[0]),
            text=[total_dice],  # Display the number on the bar
            textposition='inside',  # Position the text inside the bar
            hovertemplate='<b>Total Dice</b>: %{x}<extra></extra>'
        ))
        
        fig.add_trace(go.Bar(
            x=[successful_rolls],
            y=[1],
            orientation='h',
            name='Hits',
            marker=dict(color=colors[1]),
            text=[successful_rolls],  # Display the number on the bar
            textposition='inside',  # Position the text inside the bar
            hovertemplate='<b>Hits</b>: %{x}<extra></extra>'
        ))
        
        fig.add_trace(go.Bar(
            x=[wounds_inflicted],
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
            round(self.active_number_of_attacks, 2), 
            round(self.expected_hits, 2), 
            round(self.expected_wounds_from_hits, 2)
        )
        return fig

    def visualize_morale(self):
        fig = self.visualize_dice_outcomes(
            round(self.expected_wounds_from_hits, 2), 
            0,
            round(self.expected_wounds_from_morale, 2)
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





