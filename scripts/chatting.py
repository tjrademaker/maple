from ipywidgets import *
from IPython import display
import functools
from .helper import *


def select_intent(debug = False):

    vals = dict(initial_prompt = 'This is a conversation between an AI puppy called Maple and a 20-30 year old human looking to X. Maple is friendly, playful, and has a strong personality. Maple will randomly interject "woof", "ruff" or other dog sounds. Maple gives short responses of two sentences or less. Maple helps the human to X by Y. \n\nMaple: Woof! What can I help you with today?\n\nHuman: X')

    intent_dict = {
        'get some advice': 'listening and providing solutions',
        'vent': 'giving encouragement to say more',
        'reflect': 'asking open-ended questions',
        'explore an emotion': 'inquiring about their feelings', 
        'talk about change': 'listening carefully'
    }
    out = Output()

    @out.capture()
    def _on_submit(b, vals):
        vals['prompt'] = vals['initial_prompt'].replace('X', b.description).replace('Y', intent_dict[b.description])
        out.clear_output()
        
        get_chatting(vals, debug)

    # create the buttons
    buttons = [Button(description = k) for k, _ in intent_dict.items()]
    
    # call the on_reset_clicked function when the reset_button is clicked
    for button in buttons:
        button.on_click(functools.partial(_on_submit, vals = vals))

    display.display(out)
    
    with out:
        pretty_print("Maple: Woof! What can I help you with today?")
        pretty_print('\n')
        display.display(VBox(buttons))


def get_chatting(vals, debug = False):
    
    # create the output widget
    out2 = Output()

    # initialize prompts dictionary to collect conversation
    prompts = initialize_prompts(vals, debug)
    
    # widgets
    text_box = Text(
        placeholder='Enter your response here',
        layout = Layout(width = '100%')
    )
    submit_button = Button(
        description = 'Submit', 
        layout = Layout(width = '75px'),
        style = dict(button_color = 'green', text_color = 'white')
    )
    reset_button = Button(
        description='Reset', 
        layout = Layout(width = '75px'),
        button_style = 'danger',
        style = dict(text_color = 'white')
    )
    
    # define a function that will be called when the user submits a prompt
    def on_submit(text):

        # add human prompt
        prompts['human'].append(text_box.value)
        prompts['maple'].append(' ...')

        # update output
        update_output()

        # request AI output
        if not debug:
            prompts['maple'][-1] = get_API_response(prompt2str(prompts))
        else:
            time.sleep(1)
            prompts['maple'][-1] = ' Some placeholder text'

        update_output()

    # when reset button is clicked restart conversation
    @out2.capture()
    def on_reset_clicked(b):
        out2.clear_output()
        select_intent(debug)        

    # when updating output: clear outputs, print collected prompts and display fresh text widget
    @out2.capture()
    def update_output():
        out2.clear_output()
        pretty_print(prompt2str(prompts, show = True))
        display.display(hbox)
        text_box.value = ''
        text_box.focus()
    
    # set callbacks
    text_box.on_submit(on_submit)
    submit_button.on_click(on_submit)
    reset_button.on_click(on_reset_clicked)
            
    # create a horizontal box layout to arrange the text_box and reset_button next to each other
    hbox = HBox([text_box, submit_button, reset_button], layout = Layout(width = '100%'))

    display.display(out2)
    update_output()