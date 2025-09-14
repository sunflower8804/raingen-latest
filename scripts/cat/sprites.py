import os
from copy import copy

import pygame
import ujson

from scripts.game_structure.game_essentials import game

image_cache = {}

def load_sprite(path):
    global image_cache
    if path not in image_cache:
        image_cache[path] = pygame.image.load(path).convert_alpha()
    return image_cache[path]

def build_sprite_index(sprite_folders):
    sprite_index = {}
    for folder in sprite_folders:
        for fname in os.listdir(folder):
            if fname.endswith('.png'):
                sprite_name = os.path.splitext(fname)[0]
                sprite_index[sprite_name] = os.path.join(folder, fname)
    return sprite_index

sprite_folders = ["sprites/lineart", "sprites/accs", "sprites/eyes", "sprites/parts", "sprites/pelts"]
SPRITE_INDEX = build_sprite_index(sprite_folders)

class Sprites:
    cat_tints = {}
    white_patches_tints = {}
    clan_symbols = []
    
    
    def __init__(self):
        """Class that handles and hold all spritesheets. 
        Size is normally automatically determined by the size
        of the lineart. If a size is passed, it will override 
        this value. """
        self.symbol_dict = None
        self.size = None
        self.spritesheets = {}
        self.images = {}
        self.sprites = {}

        # Shared empty sprite for placeholders
        self.blank_sprite = None
        
        self.load_tints()

    def make_sprite_groups(self, groupname, color_rows, prefix, row_override=None, col_override=None, **kwargs):
        """
        OPTIMIZATIONS ARE TASTY.
    
        groupname: str, the spritesheet/group name
        color_rows: list of lists, each inner list is a row of sprite names
        prefix: str, the string to prepend to each sprite name
        kwargs: any extra arguments to pass to make_group (e.g., sprites_x, sprites_y, no_index)
        """
        for row, colors in enumerate(color_rows):
            for col, color in enumerate(colors):
                actual_row = row_override if row_override is not None else row
                actual_col = col_override if col_override is not None else col
                self.make_group(groupname, (actual_col, actual_row), f'{prefix}{color}', **kwargs)

    def load_tints(self):
        try:
            with open("sprites/dicts/tint.json", 'r') as read_file:
                self.cat_tints = ujson.loads(read_file.read())
        except IOError:
            print("ERROR: Reading Tints")

        try:
            with open("sprites/dicts/white_patches_tint.json", 'r') as read_file:
                self.white_patches_tints = ujson.loads(read_file.read())
        except IOError:
            print("ERROR: Reading White Patches Tints")

    def spritesheet(self, a_file, name):
        """
        Add spritesheet called name from a_file.

        Parameters:
        a_file -- Path to the file to create a spritesheet from.
        name -- Name to call the new spritesheet.
        """
        self.spritesheets[name] = load_sprite(a_file)

    def make_group(self,
                   spritesheet,
                   pos,
                   name,
                   sprites_x=3,
                   sprites_y=7,
                   no_index=False):  # pos = ex. (2, 3), no single pixels

        """
        Divide sprites on a spritesheet into groups of sprites that are easily accessible
        :param spritesheet: Name of spritesheet file
        :param pos: (x,y) tuple of offsets. NOT pixel offset, but offset of other sprites
        :param name: Name of group being made
        :param sprites_x: default 3, number of sprites horizontally
        :param sprites_y: default 3, number of sprites vertically
        :param no_index: default False, set True if sprite name does not require cat pose index
        """

        group_x_ofs = pos[0] * sprites_x * self.size
        group_y_ofs = pos[1] * sprites_y * self.size
        i = 0

        # splitting group into singular sprites and storing into self.sprites section
        for y in range(sprites_y):
            for x in range(sprites_x):
                if no_index:
                    full_name = f"{name}"
                else:
                    full_name = f"{name}{i}"

                try:
                    new_sprite = pygame.Surface.subsurface(
                        self.spritesheets[spritesheet],
                        group_x_ofs + x * self.size,
                        group_y_ofs + y * self.size,
                        self.size, self.size
                    )

                except ValueError:
                    # Fallback for non-existent sprites
                    print(f"WARNING: nonexistent sprite - {full_name}")
                    if not self.blank_sprite:
                        self.blank_sprite = pygame.Surface(
                            (self.size, self.size),
                            pygame.HWSURFACE | pygame.SRCALPHA
                        )
                    new_sprite = self.blank_sprite

                self.sprites[full_name] = new_sprite
                i += 1

    def load_all(self):
        # get the width and height of the spritesheet
        lineart = pygame.image.load('sprites/lineart/lineart.png')
        width, height = lineart.get_size()
        del lineart  # unneeded

        #grab the json lists
        with open("sprites/dicts/sprites_py_lists.json", "r") as f:
            sprites_py_dict = ujson.loads(f.read())

        # if anyone changes lineart for whatever reason update this
        if isinstance(self.size, int):
            pass
        elif width / 3 == height / 7:
            self.size = width / 3
        else:
            self.size = 50  # default, what base clangen uses
            print(f"lineart.png is not 3x7, falling back to {self.size}")
            print(f"if you are a modder, please update scripts/cat/sprites.py and "
                  f"do a search for 'if width / 3 == height / 7:'")

        if self.blank_sprite is None:
            self.blank_sprite = pygame.Surface((self.size, self.size), pygame.HWSURFACE | pygame.SRCALPHA)


        del width, height  # unneeded

        sprite_folders = sprites_py_dict['sprite_folders']
        
        sprite_names = sprites_py_dict['sprite_names']
        
        for x in sprite_names:
            loaded = False
            if 'lineart' in x and game.config['fun']['april_fools']:
                path = f"sprites/lineart/aprilfools{x}.png"
                if os.path.exists(path):
                    self.spritesheet(path, x)
                    loaded = True
            else:
                for folder in sprite_folders:
                    path = os.path.join(folder, f"{x}.png")
                    if os.path.exists(path):
                        self.spritesheet(path, x)
                        loaded = True
                        break 

            if not loaded:
                print(f"Warning: Sprite for '{x}' not found in any folder.")

        # Line art
        self.make_group('lineart', (0, 0), 'lines')
        self.make_group('shadersnewwhite', (0, 0), 'shaders')
        self.make_group('lightingnew', (0, 0), 'lighting')

        self.make_group('lineartdead', (0, 0), 'lineartdead')
        self.make_group('lineartdf', (0, 0), 'lineartdf')

        # Fading Fog
        for i in range(0, 3):
            self.make_group('fademask', (i, 0), f'fademask{i}')
            self.make_group('fadestarclan', (i, 0), f'fadestarclan{i}')
            self.make_group('fadedarkforest', (i, 0), f'fadedf{i}')

        # Define eye colors
        eye_colors = sprites_py_dict['eye_colors']
        self.make_sprite_groups('eyes', eye_colors, 'eyes')
        self.make_sprite_groups('eyes2', eye_colors, 'eyes2')

        #generating multieyes
        multieye_colors = [[f"MULTI{color}" for color in row] for row in eye_colors]
        self.make_sprite_groups('multieyes', multieye_colors, 'multieyes')

        #generating bobaeyes
        bobaeye_colors = [[f"BOBA{color}" for color in row] for row in eye_colors]
        self.make_sprite_groups('bobaeyes', bobaeye_colors, 'bobaeyes')
        self.make_sprite_groups('bobaeyes2', bobaeye_colors, 'bobaeyes2')

        #rain's eyes
        raineye_colors = sprites_py_dict['raineye_colors']
        self.make_sprite_groups('raineyes', raineye_colors, 'raineyes')
        self.make_sprite_groups('raineyes2', raineye_colors, 'raineyes2')
        
        #generating multieyes
        multiraineye_colors = [[f"MULTI{color}" for color in row] for row in raineye_colors]
        self.make_sprite_groups('multiraineyes', multiraineye_colors, 'multiraineyes')

        #lars' eyes
        larseye_colors = sprites_py_dict['larseye_colors']
        self.make_sprite_groups('larseyes', larseye_colors, 'larseyes')
        self.make_sprite_groups('larseyes2', larseye_colors, 'larseyes2')

        #lars' multi eyes
        multilarseye_colors = sprites_py_dict['multilarseye_colors']
        self.make_sprite_groups('multilarseyes', multilarseye_colors, 'multilarseyes')
                    
        rivuleteye_colors = sprites_py_dict['rivuleteye_colors']
        self.make_sprite_groups('rivuleteyes', rivuleteye_colors, 'rivuleteyes')
        self.make_sprite_groups('rivuleteyes2', rivuleteye_colors, 'rivuleteyes2')
                     
        buttoneye_colors = sprites_py_dict['buttoneye_colors']
        self.make_sprite_groups('buttoneyes', buttoneye_colors, 'buttoneyes')
        self.make_sprite_groups('buttoneyes2', buttoneye_colors, 'buttoneyes2')

        #lars boba eyes seperate due to being behind the main list
        bobaeyeslars_colors = sprites_py_dict['bobaeyeslars_colors']
        self.make_sprite_groups('bobaeyeslars', bobaeyeslars_colors, 'bobaeyeslars')
        self.make_sprite_groups('bobaeyeslars2', bobaeyeslars_colors, 'bobaeyeslar2')
        
        # Define white patches
        white_patches = sprites_py_dict['white_patches']
        self.make_sprite_groups('whitepatches', white_patches, 'white')

        # Define colors and categories
        color_categories = sprites_py_dict['color_categories']
        color_types = sprites_py_dict['color_types']
        for color_type in color_types:
            self.make_sprite_groups(color_type, color_categories, color_type[:-7])

        # tortiepatchesmasks
        tortiepatchesmasks = sprites_py_dict['tortiepatchesmasks']
        self.make_sprite_groups('tortiepatchesmasks', tortiepatchesmasks, 'tortiemask')
                
        # Empty skins
        skin_colors = sprites_py_dict['skin_colors']
        self.make_sprite_groups('skin', skin_colors, 'skin')
                
        # Gills, Tongues, Quills
        gilltongue_rows = sprites_py_dict['gilltongue_rows']

        # Determine group name per row
        if game.settings["bea_gilltongue"]:
            group_rows = ['gilltongue', 'gilltongue', 'gilltongue', 'beagilltongue', 'beagilltongue', 'beagilltongue']
        else:
            group_rows = ['gilltongue'] * 6

        # Loop through and assign
        for group, colors in zip(group_rows, gilltongue_rows):
            self.make_sprite_groups(group, [colors], 'skin')

        # Horns - Ram, Scav, Elite, Sharp, Dragon, Lancer
        horns_colors = sprites_py_dict['horns_colors']
        self.make_sprite_groups('horns', horns_colors, 'skin')

        #Whiskers - Catfish, Dragon
        whiskers_colors = sprites_py_dict['whiskers_colors']
        self.make_sprite_groups('whiskers', whiskers_colors, 'skin')

        # fancyskin spritesheet
        fancyskin_colors = sprites_py_dict['fancyskin_colors']
        # Handle rows 0-6 with function
        self.make_sprite_groups('fancyskin', fancyskin_colors[:7], 'skin')
        # Handle row 7 seperately because it will suffer alone
        if len(fancyskin_colors) > 8:
            for col, color in enumerate(fancyskin_colors[8]):
                self.make_group('fancyskin', (col, 8), f"muddypaws{color}")

        # data games stuff spritesheet
        datagamesstuff_colors = sprites_py_dict['datagamesstuff_colors']
        self.make_sprite_groups('datagamesstuff', datagamesstuff_colors, 'skin')

        # manes spritesheet
        manes_colors = sprites_py_dict['manes_colors']
        self.make_sprite_groups('manes', manes_colors, 'skin')
                
        # overseertenna spritesheet
        overseertenna_colors = sprites_py_dict['overseertenna_colors']
        self.make_sprite_groups('overseertenna', overseertenna_colors, 'skin')

        # budgiewings spritesheet
        budgiewings_colors = [[f"{color}BUDGIEWINGS" for color in row] for row in color_categories]
        self.make_sprite_groups('budgiewings', budgiewings_colors, 'budgiewings')

        # conurewings spritesheet
        conurewings_colors = [[f"{color}CONUREWINGS" for color in row] for row in color_categories]
        self.make_sprite_groups('conurewings', conurewings_colors, 'skin')

        # lovebirdwings spritesheet
        lovebirdwings_colors = [[f"{color}LOVEBIRDWINGS" for color in row] for row in color_categories]
        self.make_sprite_groups('lovebirdwings', lovebirdwings_colors, 'skin')
                
        # pidgeonwings spritesheet
        pidgeonwings_colors = [[f"{color}PIDGEONWINGS" for color in row] for row in color_categories]
        self.make_sprite_groups('pidgeonwings', pidgeonwings_colors, 'skin')

        # vulturewings spritesheet
        vulturewings_colors = [[f"{color}VULTUREWINGS" for color in row] for row in color_categories]
        self.make_sprite_groups('vulturewings', vulturewings_colors, 'skin')

        # colorwings spritesheet
        colorwings_colors = sprites_py_dict['colorwings_colors']
        self.make_sprite_groups('colorwings', colorwings_colors, 'skin')

        # whitepatchwings spritesheet
        whitepatchwings_colors = sprites_py_dict['whitepatchwings_colors']
        self.make_sprite_groups('whitepatchwings', whitepatchwings_colors, 'skin')

        # whitepatchwingsfade spritesheet
        whitepatchwingsfade_colors = [[f"{color}FADE" for color in row] for row in whitepatchwings_colors]
        self.make_sprite_groups('whitepatchwingsfade', whitepatchwingsfade_colors, 'whitepatchwingsfade')


        self.load_scars()
        self.load_symbols()

    def load_scars(self):
        """
        Loads scar sprites and puts them into groups.
        """

        #load json
        with open("sprites/dicts/sprites_py_lists.json", "r") as f:
            sprites_py_dict = ujson.loads(f.read())
        
        # Define scars
        scars_data = sprites_py_dict['scars_data']

        # define missing parts
        missing_parts_data = sprites_py_dict['missing_parts_data']

        # scars 
        self.make_sprite_groups('scars', scars_data, 'scars')

        # missing parts
        self.make_sprite_groups('missingscars', missing_parts_data, 'scars')

        # accessories
        medcatherbs_data = sprites_py_dict['medcatherbs_data']
        wild_data = sprites_py_dict['wild_data']
        collars_data = sprites_py_dict['collars_data']
        bellcollars_data = sprites_py_dict['bellcollars_data']
        bowcollars_data = sprites_py_dict['bowcollars_data']
        nyloncollars_data = sprites_py_dict['nyloncollars_data']
        rwlizards_data = sprites_py_dict['rwlizards_data']
        drones_data = sprites_py_dict['drones_data']
        muddypaws_data = sprites_py_dict['muddypaws_data']
        herbs2_data = sprites_py_dict['herbs2_data']
        insectwings_data = sprites_py_dict['insectwings_data']
        buddies_data = sprites_py_dict['buddies_data']
        newaccs_data = sprites_py_dict['newaccs_data']
        newaccs2_data = sprites_py_dict['newaccs2_data']
        bodypaint_data = sprites_py_dict['bodypaint_data']
        implant_data = sprites_py_dict['implant_data']
        magic_data = sprites_py_dict['magic_data']
        necklaces_data = sprites_py_dict['necklaces_data']
        drapery_data = sprites_py_dict['drapery_data']
        pridedrapery_data = sprites_py_dict['pridedrapery_data']
        eyepatch_data = sprites_py_dict['eyepatch_data']
        larsaccs_data = sprites_py_dict['larsaccs_data']
        harleyaccs_data = sprites_py_dict['harleyaccs_data']
        featherboas_data = sprites_py_dict['featherboas_data']
        scarves_data = sprites_py_dict['scarves_data']
        neckbandanas_data = sprites_py_dict['neckbandanas_data']
        chains_data = sprites_py_dict['chains_data']
        newaccs3_data = sprites_py_dict['newaccs3_data']
        floatyeyes_data = sprites_py_dict['floatyeyes_data']
        morespears_data = sprites_py_dict['morespears_data']
        flagaccs_data = sprites_py_dict['flagaccs_data']
        haloaccs_data = sprites_py_dict['haloaccs_data']
        ponchoaccs_data = sprites_py_dict['ponchoaccs_data']
        glassesaccs_data = sprites_py_dict['glassesaccs_data']
        orbitals_data = sprites_py_dict['orbitals_data']
        vulturemasks_data = sprites_py_dict['vulturemasks_data']
        iteratormasks_data = sprites_py_dict['iteratormasks_data']

        # medcatherbs
        self.make_sprite_groups('medcatherbs', medcatherbs_data, 'acc_herbs')
        self.make_group('medcatherbs', (5, 2), 'acc_herbsDRY HERBS')

        # wild
        self.make_sprite_groups('medcatherbs', wild_data, 'acc_wild', row_override=2)

        # collars
        self.make_sprite_groups('collars', collars_data, 'collars')

        # bellcollars
        self.make_sprite_groups('bellcollars', bellcollars_data, 'collars')

        # bowcollars
        self.make_sprite_groups('bowcollars', bowcollars_data, 'collars')

        # nyloncollars
        self.make_sprite_groups('nyloncollars', nyloncollars_data, 'collars')

        # rw lizards
        self.make_sprite_groups('rwlizards', rwlizards_data, 'lizards')

        # drones
        self.make_sprite_groups('drones', drones_data, 'collars')

        # muddypaws
        self.make_sprite_groups('muddypaws', muddypaws_data, 'muddypaws')

        # insect wings
        self.make_sprite_groups('insectwings', insectwings_data, 'insectwings')

        # herbs 2
        self.make_sprite_groups('herbs2', herbs2_data, 'herbs2')

        # buddies
        self.make_sprite_groups('buddies', buddies_data, 'buddies')

        # newaccs
        self.make_sprite_groups('newaccs', newaccs_data, 'newaccs')

        # newaccs2
        self.make_sprite_groups('newaccs2', newaccs2_data, 'newaccs2')

        # bodypaint
        self.make_sprite_groups('bodypaint', bodypaint_data, 'bodypaint')

        # implant
        self.make_sprite_groups('implant', implant_data, 'implant')

        # magic
        self.make_sprite_groups('magic', magic_data, 'magic')

        # necklaces
        self.make_sprite_groups('necklaces', necklaces_data, 'necklaces')

        # drapery
        self.make_sprite_groups('drapery', drapery_data, 'drapery')

        # pridedrapery
        self.make_sprite_groups('pridedrapery', pridedrapery_data, 'pridedrapery')

        # eyepatches
        self.make_sprite_groups('eyepatches', eyepatch_data, 'eyepatches')

        # larsaccs
        self.make_sprite_groups('larsaccs', larsaccs_data, 'larsaccs')

        # harleyaccs
        self.make_sprite_groups('harleyaccs', harleyaccs_data, 'harleyaccs')

        # featherboas
        self.make_sprite_groups('featherboas', featherboas_data, 'featherboas')

        # scarves
        self.make_sprite_groups('scarves', scarves_data, 'scarves')

        # neckbandanas
        self.make_sprite_groups('neckbandanas', neckbandanas_data, 'neckbandanas')

        # chains
        self.make_sprite_groups('chains', chains_data, 'chains')

        # newaccs3
        self.make_sprite_groups('newaccs3', newaccs3_data, 'newaccs3')
    
        # floatyeyes
        self.make_sprite_groups('floatyeyes', floatyeyes_data, 'floatyeyes')

        # morespears
        self.make_sprite_groups('morespears', morespears_data, 'morespears')

        # flagaccs
        self.make_sprite_groups('flagaccs', flagaccs_data, 'flagaccs')
    
        # haloaccs
        self.make_sprite_groups('haloaccs', haloaccs_data, 'haloaccs')

        # ponchoaccs
        self.make_sprite_groups('ponchoaccs', ponchoaccs_data, 'ponchoaccs')

        # glassesaccs
        self.make_sprite_groups('glassesaccs', glassesaccs_data, 'glassesaccs')

        # orbitals
        self.make_sprite_groups('orbitals', orbitals_data, 'orbitals')

        # vulture masks
        self.make_sprite_groups('vulturemasks', vulturemasks_data, 'vulturemasks')

        # iterator masks
        self.make_sprite_groups('iteratormasks', iteratormasks_data, 'iteratormasks')

    def load_symbols(self):
        """
        loads clan symbols
        """

        if os.path.exists('resources/dicts/clan_symbols.json'):
            with open('resources/dicts/clan_symbols.json') as read_file:
                self.symbol_dict = ujson.loads(read_file.read())

        # U and X omitted from letter list due to having no prefixes
        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                   "V", "W", "Y", "Z"]

        # sprite names will format as "symbol{PREFIX}{INDEX}", ex. "symbolSPRING0"
        y_pos = 1
        for letter in letters:
            x_mod = 0
            for i, symbol in enumerate([symbol for symbol in self.symbol_dict if
                                        letter in symbol and self.symbol_dict[symbol]["variants"]]):
                if self.symbol_dict[symbol]["variants"] > 1 and x_mod > 0:
                    x_mod += -1
                for variant_index in range(self.symbol_dict[symbol]["variants"]):
                    x_pos = i + x_mod

                    if self.symbol_dict[symbol]["variants"] > 1:
                        x_mod += 1
                    elif x_mod > 0:
                        x_pos += - 1

                    self.clan_symbols.append(f"symbol{symbol.upper()}{variant_index}")
                    self.make_group('symbols',
                                    (x_pos, y_pos),
                                    f"symbol{symbol.upper()}{variant_index}",
                                    sprites_x=1, sprites_y=1, no_index=True)

            y_pos += 1

    def dark_mode_symbol(self, symbol):
        """Change the color of the symbol to dark mode, then return it
        :param Surface symbol: The clan symbol to convert"""
        dark_mode_symbol = copy(symbol)
        var = pygame.PixelArray(dark_mode_symbol)
        var.replace((87, 76, 45), (239, 229, 206))
        del var
        # dark mode color (239, 229, 206)
        # debug hot pink (255, 105, 180)

        return dark_mode_symbol

# CREATE INSTANCE
sprites = Sprites()
