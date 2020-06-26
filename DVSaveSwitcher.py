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
        print('[D]elete save')
        print('[E]xit program')
        try:
            while True:
                choice = input('Input: ').upper()
                if(choice in ('B','BACK-UP', 'BACKUP')):
                    return self.CopyActive()
                elif(choice in ('L', 'LOAD')):
                    return self.LoadInactive()
                elif(choice in ('D', 'DELETE')):
                    return self.DeleteSave()
                elif(choice in ('E', 'EXIT')):
                    exit()
                else:
                    print('Invalid input.')
        except Exception as err:
            print('Uh oh! The program broke somewhere generic. Please report this bug!')
            print("Technical details: {0}".format(err))

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

        try:
            newSave = shutil.copy2(copyfrom, copyto)
        except PermissionError:
            print('Uh oh! We tried to copy your back-up but encountered a permission issue.')
            print('Run this program as an administrator and try again.')
            return
        except Exception as err:
            print('Uh oh! The program broke while trying to copy a file. Please report this bug!')
            print("Technical details: {0}".format(err))
            return
        print('Created back-up: %s' % newSave)
        self.MainMenu()

    def LoadInactive(self):
        print('\n-- Load Back-up --')
        print('!!!WARNING!!!')
        print('This overrides the current active save file, back up first!\n')

        # Prepare the list.
        listOfFiles = self.GetListOfFiles()
        listOfFiles.remove('savegame')

        # List it to the user
        for i in range(0, len(listOfFiles)):
            print("%d)%s" % (i, listOfFiles[i]))

        sel = self.RepeatNumericalSelection('Select save (leave blank to cancel): ', listOfFiles)
        if(len(sel)==0):
            print('Cancelled')
            return self.MainMenu()

        # Load save.
        copyfrom = os.path.join(config.saveLocation, sel)
        copyto = os.path.join(config.saveLocation,'savegame')
        try:
            shutil.copy2(copyfrom, copyto)
        except PermissionError:
            print('Uh oh! We tried to copy your back-up but encountered a permission issue.')
            print('Run this program as an administrator and try again.')
            return
        except Exception as err:
            print('Uh oh! The program broke while trying to copy a file. Please report this bug!')
            print("Technical details: {0}".format(err))
            return
        print('Back-up restored.')
        self.MainMenu()

    def DeleteSave(self):
        print('\n-- Delete Save --')
        print('!!!WARNING!!!')
        print('Files deleted here will be unrecoverable!')

        # Get the list of savegames
        listOfFiles = self.GetListOfFiles()

        # Print to screen.
        for i in range(0, len(listOfFiles)):
            print("%d)%s" % (i, listOfFiles[i]))

        # User selection
        save = self.RepeatNumericalSelection('Select save (leave blank to cancel): ', self.GetListOfFiles())
        if(save == ''):
            return self.MainMenu()

        # User confirmation
        confirm = input('Are you SURE you want to irreversably DELETE %s? [Y]es, [N]o' % save).lower()
        if(confirm not in ('y','yes')):
            print('Cancelled')
            return self.DeleteSave()

        # Deletion
        try:
            os.remove(os.path.join(config.saveLocation, save))
        except PermissionError:
            print('Uh oh! We tried to delete a save but encountered a permission issue.')
            print('Run this program as an administrator and try again.')
            return
        except Exception as err:
            print('Uh oh! The program broke while trying to copy a file. Please report this bug!')
            print("Technical details: {0}".format(err))
            return
        print('Save deleted.')
        self.MainMenu()

    def GetListOfFiles(self):
        listOfFiles = [f for f in os.listdir(config.saveLocation) if os.path.isfile(os.path.join(config.saveLocation, f))]
        listOfFiles.remove('ControllerAnchors.json')
        listOfFiles.remove('GamePreferences.ini')
        return listOfFiles

    def RepeatNumericalSelection(self, query, selections):
        while True:
            selstr = input(query)
            if(len(selstr)==0):
                return ''
            try:
                sel = int(selstr)
            except ValueError as e:
                print('Please enter a number')
                continue
            if(sel >= len(selections)):
                print('Selection out of range.')
                continue
            confirm = input('Is %s correct? [Y]es, [N]o: ' % selections[int(sel)]).lower()
            if(confirm in ('yes','y')):
                return selections[int(sel)]

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

    # TODO Check if Derail Valley is running.
    # If it is, warn the user, maybe even prevent making changes?
    SaveSwitcher()

