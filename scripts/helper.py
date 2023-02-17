from IPython import display
import openai
import itertools
import time


def pretty_print(x):
    return display.display( display.HTML( x.replace("\n","<br>") ) )


def get_API_response(prompt, temperature = 0.9, max_tokens = 150):
    
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[" Human:", " Maple:"]
    )
    return response.choices[0].text

def prompt2str(prompts, show = False):
    
    # test that prompts is a dictionary with keys initial, human and maple
    assert len(set(prompts.keys()).intersection(['initial', 'human', 'maple'])) == 3    

    x = ''
    for maple, human in itertools.zip_longest(prompts['maple'], prompts['human']):
        x += 'Maple: %s\n\n' % maple
        
        if human is not None:
            x += 'Human: %s\n\n' % human

    # add part of the initial prompt that sets up the conversation for OpenAI API prompt
    if not show:
        return prompts['initial'] + x + '\n\nMaple:'
    else:
        return x


def initialize_prompts(vals, debug = False):

    split_prompts = vals['prompt'].split('\n\n')

    prompts = {
        'initial': split_prompts[0],
        'maple': [],
        'human': []
    }

    # extract additional parts of the prompts already given
    if len(split_prompts) > 1:
        for spl in split_prompts[1:]:
            subj = spl[:5].lower()
            prompts[subj].append(spl[6:])
    
    # request AI output
    if not debug:
        prompts['maple'].append(' ' + get_API_response(prompt2str(prompts)))
    else:
        time.sleep(1)
        prompts['maple'].append(' some placeholder text')

    return prompts