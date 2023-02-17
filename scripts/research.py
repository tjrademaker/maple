from ipywidgets import *
from IPython import display
import functools
from .helper import *


def research_env(vals, debug = False):
    
    out = widgets.Output()

    @out.capture()
    def _on_submit(b, vals):
        
        prompts = {'initial': text_box1.value, 'maple': [text_box2.value], 'human': [text_box3.value]}
        out.clear_output()
            
        # request AI output
        prompts['maple'].append(' ' + get_API_response(prompt2str(prompts), vals['temperature'], vals['max_tokens']))
        
        print_text = prompt2str(prompts, show = True)
        pretty_print(print_text)
        # pretty_print('\n\n'.join(print_text.split('\n\n')[:-2])) # to avoid printing empty lines \n\nHuman:\n\nMaple:
        display.display(reset_button)
    
    @out.capture()
    def _on_submit2(b, vals):
        out.clear_output()
        research_env(vals, debug)
    
    # create text boxes
    text_box1 = widgets.Textarea(
        description = 'Prompt',
        value = "This is an interaction between an AI puppy called Maple and a human. Maple listens to the human's concerns and briefly reassures them. Maple will also provide the human with additional questions to reflect on or general advice for that kind of problem. Maple does this in a supportive, nurturing and friendly way. Maple answers in 3-4 sentences.",
        layout = widgets.Layout(width = '100%', height = 'auto')
    )
    text_box2 = widgets.Textarea(
        description = 'Maple',
        value = 'Woof! What can I help you with today?',
        layout = widgets.Layout(width = '100%')
    )
    text_box3 = widgets.Textarea(
        description = 'Human',
        placeholder = 'Enter your response here',
        layout = widgets.Layout(width = '100%')
    )
    
    submit_button = widgets.Button(description='Get a response')
    reset_button = widgets.Button(description='Reset')
    
    # call the _on_submit function when the submit_button is clicked
    submit_button.on_click(functools.partial(_on_submit, vals = vals))
    reset_button.on_click(functools.partial(_on_submit2, vals = vals))
    
    display.display(out)
    
    with out:
        display.display(widgets.VBox([text_box1, text_box2, text_box3, submit_button]))