import os
import json

def control_dir(option = 'read'):
    """
    Control directory (dir) where articles are saved.
    Depending on option either check if dir exists ('check'),
    read dir path ('read') or change dir ('change').
    """
    with open('data', mode='r') as f:
        save_data = json.load(f)
        save_dir = save_data["save_dir"]
    if option == 'read':
        return save_dir
    elif option == 'check':
        return os.path.exists(save_dir)
    elif option == 'change':
        new_dir = ''
        #while os.path.exists(new_dir) == False:
        while control_dir('check') == False:
            new_dir = str(input('Please enter a valid (absolute) directory path'
                                ' to save your arXiv articles.'))
            # TODO: so far only macOS...
        else:
            save_data['save_dir'] = new_dir
            with open('data', 'w') as f:
                json.dump(save_data, f)
            print('Your articles will now be downloaded to {}.'.format(new_dir))
