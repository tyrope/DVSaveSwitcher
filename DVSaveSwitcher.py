import json, os, shutil

class Config(object):

    def __init__(self):
        self.saveLocation = ''

    # Create a config file.
    def create(self, f):
        print('No configuration file detected, starting initial set-up')

        # Install location.
        DVLocation = RepeatInput('Derail Valley installation location: ')

        self.saveLocation = os.path.join(
            DVLocation,
            'DerailValley_Data',
            'SaveGameData'
        )

        # Save the config.
        json.dump({'saveLocation': self.saveLocation}, f)

    # Load existing config file.
    def load(self, data):
        print('Config file found.')
        cfg = json.loads(data)
        self.saveLocation = cfg['saveLocation']
        print('Savegame location: '+self.saveLocation)


class SaveSwitcher():
    def __init__(self):
        self.MainMenu()

    def MainMenu(self):
        print('\n-- Main Menu --')
        print('Please select an option')
        print('[B]ack-up active save')
        print('[L]oad backed up save')
        print('[D]elete save (Not implemented)')
        print('[E]xit program')
        while True:
            choice = input('Input: ').upper()
            if(choice == 'B'):
                return self.CopyActive()
            elif(choice == 'L'):
                return self.LoadInactive()
            elif(choice == 'E'):
                exit()
            else:
                print('Invalid input.')

    def CopyActive(self):
        print('\n-- Create Back-up --')
        name = RepeatInput('Back-up name (leave blank to cancel): ', blankCancels=True)
        if(len(name) == 0):
            return self.MainMenu()

        copyfrom = os.path.join(config.saveLocation, 'savegame')
        copyto = os.path.join(config.saveLocation, name)

        # Are we trying to override a file?
        if(os.path.exists(copyto)):
            confirm = input('%s already exists, overwrite? [Y]es, [N]o: ' % name).lower()
            if(confirm not in ('yes','y')):
                return self.CopyActive()

        newSave = shutil.copy2(copyfrom, copyto)
        print('Created back-up: %s' % newSave)
        self.MainMenu()

    def LoadInactive(self):
        print('\n-- Load Back-up --')
        print('!!!WARNING!!!')
        print('This overrides the current active save file, back up first!\n')

        # Prepare the list.
        listOfFiles = [f for f in os.listdir(config.saveLocation) if os.path.isfile(os.path.join(config.saveLocation, f))]
        listOfFiles.remove('savegame')
        listOfFiles.remove('ControllerAnchors.json')
        listOfFiles.remove('GamePreferences.ini')

        # List it to the user
        for i in range(0, len(listOfFiles)):
            print("%d)%s" % (i, listOfFiles[i]))

        # Special case of RepeatInput
        while True:
            sel = input("Select save (leave blank to cancel): ")
            if(len(sel) == 0):
                return self.MainMenu()
            confirm = input('Is %s correct? [Y]es, [N]o: ' % listOfFiles[int(sel)]).lower()
            if(confirm in ('yes','y')):
                break

        # Load save.
        copyfrom = os.path.join(config.saveLocation, listOfFiles[int(sel)])
        copyto = os.path.join(config.saveLocation,'savegame')
        shutil.copy2(copyfrom, copyto)
        print('Back-up restored.')
        self.MainMenu()

def RepeatInput(query, blankCancels=False):
    while True:
        ret = input(query)
        if(len(ret) == 0 and blankCancels):
            return ''

        confirm = input('Is %s correct? [Y]es, [N]o: ' % ret).lower()
        if(confirm in ('yes','y')):
            return ret

if __name__ == '__main__':
    print('----------------------------------------')
    print('--  Derail Valley Savegame Switcher   --')
    print('-- (c)2020 Dimitri "Tyrope" Molenaars --')
    print('--  See LICENSE for more information  --')
    print('----------------------------------------')
    print('Loading configuration...')
    global config
    config = Config()
    if not os.path.exists('dvSaveSwitcher.cfg'):
        with open('dvSaveSwitcher.cfg', 'w') as f:
            config.create(f)
    else:
        with open('dvSaveSwitcher.cfg') as f:
            config.load(f.read())
    print('Configuration complete.')
    SaveSwitcher()

