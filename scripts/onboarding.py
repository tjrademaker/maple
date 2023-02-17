from ipywidgets import *
from IPython import display
import functools
from .helper import *


def select_hobbies(debug = False):
    
    base = "The following is an icebreaker activity between puppy Maple and [nickname]. Maple and [nickname] are trying to get to know each other."
    vals = dict(initial_prompt = [
        base + " After [nickname] has told Maple about what it likes doing, Maple comments on one of these interests and asks one question to learn more.",
        base + " Maple ends the conversation by making a funny statement relating to [nickname]'s interests and her being a dog."
    ])

    hobbies = {
        'glide n slide': ['diving', 'skateboarding', 'downhill skiing', 'roller skating', 'snorkeling', 'snowboarding', 'surfing'], 
        'ball sports': ['basketball', 'cricket', 'dodgeball', 'football', 'soccer', 'tennis', 'volleyball'], 
        'other sports': ['cycling', 'fitness', 'gymnastics', 'rock climbing', 'running', 'swimming', 'trampoline'], 
        'socials': ['facebook', 'instagram', 'snapchat', 'tiktok', 'twitch', 'youtube shorts', 'wechat'],
        'games': ['gaming', 'wordle', '2048', 'hogwarts legacy', 'pokemon', 'minecraft', 'league of legends'], 
        'creation': ['cooking', 'drawing', 'handicraft', 'painting', 'singing', 'theater', 'writing'],
        'interactive': ['friends', 'shopping', 'dogwalking', 'go to the movies', 'netflix', 'volunteering'], 
        'learning': ['coding', 'hacking', 'history', 'maths', 'reading']
    }

    checkboxes = []
    hbox = []
    for k, v in hobbies.items():
        vbox = []
        for hobby in sorted(v):
            vbox.append(Checkbox(value=False, indent = False, description = hobby, layout = dict(margin='0px', max_width='140px')))
        checkboxes += vbox
        hbox.append(VBox([Label(k)] + vbox))

    out = Output()
    display.display(out)

    # submit hobbies
    @out.capture()
    def _on_submit(b, vals):
        hobbies = [cb.description for cb in checkboxes if cb.value]
        text_hobbies = ', '.join(hobbies[:-1]) + ' and ' + hobbies[-1]

        vals['prompt'] = vals['initial_prompt'][0] + '\n\nMaple: So what do you like doing?\n\nHuman: I like %s' % text_hobbies
        out.clear_output()
        get_onboarding(vals, debug)
        
    submit_button = widgets.Button(
        description = 'Submit', 
        layout = widgets.Layout(width = '75px'),
        style = dict(button_color = 'green', text_color = 'white')
    )
    submit_button.on_click(functools.partial(_on_submit, vals = vals))

    with out:
        pretty_print('Maple: So what do you like doing?\n')
        display.display(HBox(hbox))
        display.display(submit_button)

def get_onboarding(vals, debug = False):
    
    # create the output widget
    out2 = Output()

    # initialize prompts dictionary to start off conversation
    prompts = initialize_prompts(vals, debug)

    # immediately end conversation by swapping prompt to the final one
    prompts['initial'] = vals['initial_prompt'][1] + prompts['initial'].split(' to learn more.')[1]

    
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
        select_hobbies(debug)        

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