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

        sprite_folders = ['sprites/accs', 'sprites/eyes', 'sprites/lineart', 'sprites/parts', 'sprites/pelts', 'sprites']

        sprite_names = [
            'lineart', 'lineartdf', 'lineartdead',
            'eyes', 'eyes2', 
            'skin', 'gilltongue', 'beagilltongue', 'horns', 'fancyskin', 'whiskers', 'orbitals', 'datagamesstuff',
            'budgiewings', 'colorwings', 'conurewings', 'lovebirdwings', 'manes', 'overseertenna', 'pidgeonwings',
            'vulturewings', 'whitepatchwings', 'whitepatchwingsfade',
            'scars', 'missingscars',
            'medcatherbs',
            'collars', 'bellcollars', 'bowcollars', 'nyloncollars', 'rwlizards', 'drones', 'muddypaws', 
            'herbs2', 'insectwings', 'buddies', 'newaccs', 'bodypaint', 'implant', 'magic', 'necklaces',
            'newaccs2', 'drapery', 'eyepatches', 'pridedrapery', 'larsaccs', 'harleyaccs', 'newaccs3',
            'featherboas', 'scarves', 'chains', 'neckbandanas', 'floatyeyes', 'morespears', 'haloaccs',
            'flagaccs', 'ponchoaccs', 'glassesaccs', 'vulturemasks', 'iteratormasks',
            'singlecolours', 'speckledcolours', 'tabbycolours', 'bengalcolours', 'marbledcolours',
            'rosettecolours', 'smokecolours', 'tickedcolours', 'mackerelcolours', 'classiccolours',
            'sokokecolours', 'agouticolours', 'singlestripecolours', 'maskedcolours', 'bananacolours',
            'centipedecolours', 'collaredcolours', 'concolours', 'gravelcolours', 'cyanlizardcolours',
            'slimemoldcolours', 'lanterncolours', 'vulturecolours', 'lizardcolours', 'leviathancolours',
            'fluffycolours', 'amoebacolours', 'seaslugcolours', 'yeekcolours', 'rustedcolours',
            'envoycolours', 'drizzlecolours', 'solacecolours', 'leafycolours', 'scaledcolours', 
            'dragonfruitcolours', 'necklacecolours', 'dreamercolours', 'duskdawncolours', 
            'seercolours', 'rottencolours', 'firecolours', 'countershadedcolours', 'cherrycolours',
            'oldgrowthcolours', 'sparklecatcolours', 'wolfcolours', 'sunsetcolours', 'hypnotistcolours',
            'ringedcolours', 'skinnycolours', 'sparsecolours', 'impishcolours', 'sportycolours', 
            'fizzycolours', 'skeletoncolours', 'shredcolours', 'glowingcolours', 'moldcolours',
            'swingcolours', 'lovebirdcolours', 'budgiecolours', 'amazoncolours', 'applecolours', 'bobacolours',
            'glittercolours', 'icecolours', 'iggycolours', 'manedcolours', 'patchworkcolours', 'robotcolours',
            'sunkencolours', 'tomocolours', 'whalecolours', 'pidgeoncolours', 'watermeloncolours',
            'dragonetcolours', 'salmoncolours', 'darkechocolours', 'lightechocolours', 'plantaincolours',
            'daenixcolours', 'seltzercolours', 'sworncolours', 'spookycolours', 'conurecolours', 'noblecolours',
            'bettacolours', 'constellationcolours', 'malibucolours', 'claycolours', 'antethisiscolours',
            'citadelcolours', 'gravecolours', 'interlopercolours',
            'raineyes', 'raineyes2', 'multieyes', 'multiraineyes', 'larseyes', 'multilarseyes', 'larseyes2', 
            'rivuleteyes', 'rivuleteyes2', 'buttoneyes', 'buttoneyes2', 'bobaeyes', 'bobaeyes2', 'bobaeyeslars',
            'bobaeyeslars2',
            'shadersnewwhite', 'lightingnew',
            'whitepatches', 'tortiepatchesmasks',
            'fademask', 'fadestarclan', 'fadedarkforest',
            'symbols'
        ]
        
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
        eye_colors = [
            ['YELLOW', 'AMBER', 'HAZEL', 'PALEGREEN', 'GREEN', 'BLUE', 'DARKBLUE', 'GREY', 'CYAN', 'EMERALD', 'HEATHERBLUE', 'SUNLITICE'],
            ['COPPER', 'SAGE', 'COBALT', 'PALEBLUE', 'BRONZE', 'SILVER', 'PALEYELLOW', 'GOLD', 'GREENYELLOW', 'RED', 'PURPLE', 'MAUVE']
        ]

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
        raineye_colors = [
            ['ELECTRICBLUE', 'VIOLET', 'PINK', 'SNOW', 'ORANGE', 'CREAM', 'SEAFOAM', 'CRIMSON', 'NAVY', 'VOIDGOLD', 'COOLBROWN', 'PLUM'],
            ['INDIGO', 'LILAC', 'ACROBLUE', 'ACROGREEN', 'ACROGREY', 'ACROINDIGO', 'ACROAMBER', 'ACROPINK', 'ACRORED', 'ACROTEAL', 'FIRE', 'RUBY'],
            ['RUBYAGAIN', 'ESCAPEE', 'REFORGED', 'FLORAVORE', 'REJECT', 'WAYFARER', 'PISTON', 'EXILED', 'THEIF', 'THEIFDOS', 'MORTICIAN', 'SWAMPY'],
            ['PORTALMAKER', 'PURIFIER', 'CORROSOL', 'SEVENSEVEN', 'ATLAN', 'BASIC', 'BELL', 'BIS', 'BIT', 'CRITTER', 'CUBED', 'DIM'],
            ['DOE', 'FREYR', 'GAMBLE', 'GORB', 'HERO', 'JANE', 'JOHN', 'MATT', 'MESS', 'PE', 'POLE', 'RAT'],
            ['RGB', 'ROT', 'SCRATCH', 'SHED', 'SIEGE', 'SPARK', 'SPARKLE', 'SUNSET', 'TELA', 'USURP', 'WAR', 'XIII']
        ]

        self.make_sprite_groups('raineyes', raineye_colors, 'raineyes')
        self.make_sprite_groups('raineyes2', raineye_colors, 'raineyes2')
        
        #generating multieyes
        multiraineye_colors = [[f"MULTI{color}" for color in row] for row in raineye_colors]

        self.make_sprite_groups('raineyes', multiraineye_colors, 'raineyes')

        #lars' eyes
        larseye_colors = [
            ['ALBA', 'ALBINO', 'ANGEL', 'APPLE', 'AQUA', 'ARID', 'BANANA', 'BLOOD', 'CARNI', 'CHAIN', 'BUTCHER'],
            ['CREAMY', 'DAWN', 'ESES', 'EXILE', 'FAE', 'FALLSTAR', 'FIELD', 'FOAM', 'HOT', 'IRID', 'DREAMER'],
            ['KARMA', 'KIND', 'MARTI', 'MEISTALT', 'MHUNT', 'MELON', 'MESS', 'MEISTER', 'MINT', 'MINV', 'FAKEGOLD'],
            ['MOON', 'MRIV', 'PEACH', 'PEBB', 'PELA', 'PEPPER', 'RETRO', 'RUNT', 'RUST', 'SIG', 'GREENDREAM'],
            ['SIXER', 'SPLIT', 'SUN', 'SWEET', 'TIDE', 'VIVID', 'WAVE', 'WINKS', 'ZENI', 'BEAST', 'HEATSTROKE'],
            ['BROWNTBOI', 'ORANGETBOI', 'BREDTBOI', 'REDTBOI', 'VIBRANCY', 'SIGNAL', 'PURPLEDREAM', 'NOVEMBER', 'LEADER'],
        ]
        
        self.make_sprite_groups('larseyes', larseye_colors, 'larseyes')
        self.make_sprite_groups('larseyes2', larseye_colors, 'larseyes2')

        #lars' multi eyes
        multilarseye_colors = [
            ['MULTIALBA', 'MULTIALBINO', 'MULTIANGEL', 'MULTIAPPLE', 'MULTIAQUA', 'MULTIARID', 'MULTIBANANA', 'MULTIBLOOD', 'MULTICARNI', 'MULTICHAIN'],
            ['MULTICREAMY', 'MULTIDAWN', 'MULTIESES', 'MULTIEXILE', 'MULTIFAE', 'MULTIFALLSTAR', 'MULTIFIELD', 'MULTIFOAM', 'MULTIHOT', 'MULTIIRID'],
            ['MULTIKARMA', 'MULTIKIND', 'MULTIMARTI', 'MULTIMEISTALT', 'MULTIMHUNT', 'MULTIMELON', 'MULTIMESS', 'MULTIMEISTER', 'MULTIMINT', 'MULTIMINV'],
            ['MULTIMOON', 'MULTIMRIV', 'MULTIPEACH', 'MULTIPEBB', 'MULTIPELA', 'MULTIPEPPER', 'MULTIRETRO', 'MULTIRUNT', 'MULTIRUST', 'MULTISIG'],
            ['MULTISIXER', 'MULTISPLIT', 'MULTISUN', 'MULTISWEET', 'MULTITIDE', 'MULTIVIVID', 'MULTIWAVE', 'MULTIWINKS', 'MULTIZENI', 'MULTIBEAST'],
            ['MULTIBROWNTBOI', 'MULTIORANGETBOI', 'MULTIBREDTBOI', 'MULTIREDTBOI'],
        ]
        
        self.make_sprite_groups('larseyes', multilarseye_colors, 'larseyes')
                    
        rivuleteye_colors = [
            ['RIVYELLOW', 'RIVAMBER', 'RIVHAZEL', 'RIVPALEGREEN', 'RIVGREEN', 'RIVBLUE', 'RIVDARKBLUE', 'RIVGREY', 'RIVCYAN', 'RIVEMERALD', 'RIVHEATHERBLUE', 'RIVSUNLITICE'],
            ['RIVCOPPER', 'RIVSAGE', 'RIVCOBALT', 'RIVPALEBLUE', 'RIVBRONZE', 'RIVSILVER', 'RIVPALEYELLOW', 'RIVGOLD', 'RIVGREENYELLOW', 'ALTRIVYELLOW', 'ALTRIVAMBER', 'ALTRIVHAZEL'],
            ['ALTRIVPALEGREEN', 'ALTRIVGREEN', 'ALTRIVBLUE', 'ALTRIVDARKBLUE', 'ALTRIVCYAN', 'ALTRIVEMERALD', 'ALTRIVHEATHERBLUE', 'ALTRIVSUNLITICE', 'ALTRIVCOPPER', 'ALTRIVSILVER', 'ALTRIVPALEYELLOW', 'ALTRIVGOLD'],
            ['ALTRIVGREENYELLOW', 'RIVRED', 'RIVPURPLE', 'RIVMAUVE', 'RIVELECTRICBLUE', 'RIVVIOLET', 'RIVPINK', 'RIVSNOW', 'RIVORANGE', 'RIVCREAM', 'RIVSEAFOAM', 'RIVCRIMSON'],
            ['RIVNAVY', 'RIVVOIDGOLD', 'RIVCOOLBROWN', 'RIVPLUM', 'RIVINDIGO', 'RIVLILAC','RIVALBA', 'RIVALBINO', 'RIVANGEL', 'RIVAPPLE', 'RIVAQUA', 'RIVARID'],
            ['RIVBANANA', 'RIVBLOOD', 'RIVCARNI', 'RIVCHAIN', 'RIVCREAMY', 'RIVDAWN', 'RIVESES', 'RIVEXILE', 'RIVFAE', 'RIVFALLSTAR', 'RIVFIELD', 'RIVFOAM'],
            ['RIVHOT', 'RIVIRID', 'RIVKARMA', 'RIVKIND', 'RIVMARTI', 'RIVMEISTALT', 'RIVMHUNT', 'RIVMELON', 'RIVMESS', 'RIVMEISTER', 'RIVMINT', 'RIVMINV'],
            ['RIVMOON', 'RIVMRIV', 'RIVPEACH', 'RIVPEBB', 'RIVPELA', 'RIVPEPPER', 'RIVRETRO', 'RIVRUNT', 'RIVRUST', 'RIVSIG', 'RIVSIXER', 'RIVSPLIT'],
            ['RIVSUN', 'RIVSWEET', 'RIVTIDE', 'RIVVIVID', 'RIVWAVE', 'RIVWINKS', 'RIVZENI', 'RIVBROWNTBOI', 'RIVORANGETBOI', 'RIVBREDTBOI', 'RIVREDTBOI', 'RIVACROINDIGO'],
            ['RIVACROAMBER', 'RIVACROTEAL', 'RIVACROGREY', 'RIVACROGREEN', 'RIVACROBLUE', 'RIVACRORED', 'RIVACROPINK', 'RIVSPARKLE', 'RIVSUNSET', 'RIVSIEGE', 'RIVROT', 'RIVUSURP'],
            ['RIVPE', 'RIVBIS', 'RIVCRITTER', 'RIVCUBED', 'RIVGAMBLE', 'RIVDIM', 'RIVBLUEORANGE', 'RIVMENACE', 'RIVDEVIOUS', 'RIVGORB', 'RIVSTARSTRUCK', 'RIVAMBERHONEY'],
            ['RIVSUNDOWN', 'RIVPARADISE', 'RIVMOLTENLAVA', 'RIVSILVERMOON', 'RIVSHADOWEDSILVER', 'RIVLACREATURA', 'RIVAWAKENED', 'RIVASCENDED', 'RIVBLUERED', 'RIVWHITESILVER', 'RIVPINKLEMONADE', 'RIVHARVESTMOON'],
            ['RIVPORTALGUN', 'RIVGASLIGHT', 'RIVBRONZEDIRT', 'RIVRBG', 'RIVRUBICON', 'RIVFIREGOLD', 'RIVBLOODRIVER', 'RIVPARTYRGB', 'RIVMIDNIGHTGLOW', 'RIVRBGLIGHTS', 'RIVBUBBLEGUM', 'RIVCYN']
        ]

        self.make_sprite_groups('rivuleteyes', rivuleteye_colors, 'rivuleteyes')
        self.make_sprite_groups('rivuleteyes2', rivuleteye_colors, 'rivuleteyes2')
                     
        buttoneye_colors = [
            ['BUTTONYELLOW', 'BUTTONAMBER', 'BUTTONHAZEL', 'BUTTONPALEGREEN', 'BUTTONGREEN', 'BUTTONBLUE', 'BUTTONDARKBLUE', 'BUTTONGREY', 'BUTTONCYAN', 'BUTTONEMERALD', 'BUTTONHEATHERBLUE', 'BUTTONSUNLITICE'],
            ['BUTTONCOPPER', 'BUTTONSAGE', 'BUTTONCOBALT', 'BUTTONPALEBLUE', 'BUTTONBRONZE', 'BUTTONSILVER', 'BUTTONPALEYELLOW', 'BUTTONGOLD', 'BUTTONGREENYELLOW', 'BUTTONIRED', 'BUTTONPURPLE', 'BUTTONMAUVE'],
            ['BUTTONINDIGO', 'BUTTONLILAC']
        ]

        self.make_sprite_groups('buttoneyes', buttoneye_colors, 'buttoneyes')
        self.make_sprite_groups('buttoneyes2', buttoneye_colors, 'buttoneyes2')

        #lars boba eyes seperate due to being behind the main list
        bobaeyeslars_colors = [
            ['BOBAALBA', 'BOBAALBINO', 'BOBAANGEL', 'BOBAAPPLE', 'BOBAAQUA', 'BOBAARID', 'BOBABANANA', 'BOBABLOOD', 'BOBACARNI', 'BOBACHAIN'],
            ['BOBACREAMY', 'BOBADAWN', 'BOBAESES', 'BOBAEXILE', 'BOBAFAE', 'BOBAFALLSTAR', 'BOBAFIELD', 'BOBAFOAM', 'BOBAHOT', 'BOBAIRID'],
            ['BOBAKARMA', 'BOBAKIND', 'BOBAMARTI', 'BOBAMEISTALT', 'BOBAMHUNT', 'BOBAMELON', 'BOBAMESS', 'BOBAMEISTER', 'BOBAMINT', 'BOBAMINV'],
            ['BOBAMOON', 'BOBAMRIV', 'BOBAPEACH', 'BOBAPEBB', 'BOBAPELA', 'BOBAPEPPER', 'BOBARETRO', 'BOBARUNT', 'BOBARUST', 'BOBASIG'],
            ['BOBASIXER', 'BOBASPLIT', 'BOBASUN', 'BOBASWEET', 'BOBATIDE', 'BOBAVIVID', 'BOBAWAVE', 'BOBAWINKS', 'BOBAZENI', 'BOBABEAST']
        ]

        self.make_sprite_groups('bobaeyelars', bobaeyelars_colors, 'bobaeyelars')
        self.make_sprite_groups('bobaeyelars2', bobaeyelars_colors, 'bobaeyeslar2')
        
        # Define white patches
        white_patches = [
            ['FULLWHITE', 'ANY', 'TUXEDO', 'LITTLE', 'COLOURPOINT', 'VAN', 'ANYTWO', 'MOON', 'PHANTOM', 'POWDER', 'BLEACHED', 'SAVANNAH', 'FADESPOTS', 'PEBBLESHINE'],
            ['EXTRA', 'ONEEAR', 'BROKEN', 'LIGHTTUXEDO', 'BUZZARDFANG', 'RAGDOLL', 'LIGHTSONG', 'VITILIGO', 'BLACKSTAR', 'PIEBALD', 'CURVED', 'PETAL', 'SHIBAINU', 'OWL'],
            ['TIP', 'FANCY', 'FRECKLES', 'RINGTAIL', 'HALFFACE', 'PANTSTWO', 'GOATEE', 'VITILIGOTWO', 'PAWS', 'MITAINE', 'BROKENBLAZE', 'SCOURGE', 'DIVA', 'BEARD'],
            ['TAIL', 'BLAZE', 'PRINCE', 'BIB', 'VEE', 'UNDERS', 'HONEY', 'FAROFA', 'DAMIEN', 'MISTER', 'BELLY', 'TAILTIP', 'TOES', 'TOPCOVER'],
            ['APRON', 'CAPSADDLE', 'MASKMANTLE', 'SQUEAKS', 'STAR', 'TOESTAIL', 'RAVENPAW', 'PANTS', 'REVERSEPANTS', 'SKUNK', 'KARPATI', 'HALFWHITE', 'APPALOOSA', 'DAPPLEPAW'],
            ['HEART', 'LILTWO', 'GLASS', 'MOORISH', 'SEPIAPOINT', 'MINKPOINT', 'SEALPOINT', 'MAO', 'LUNA', 'CHESTSPECK', 'WINGS', 'PAINTED', 'HEARTTWO', 'WOODPECKER'],
            ['BOOTS', 'MISS', 'COW', 'COWTWO', 'BUB', 'BOWTIE', 'MUSTACHE', 'REVERSEHEART', 'SPARROW', 'VEST', 'LOVEBUG', 'TRIXIE', 'SAMMY', 'SPARKLE'],
            ['RIGHTEAR', 'LEFTEAR', 'ESTRELLA', 'SHOOTINGSTAR', 'EYESPOT', 'REVERSEEYE', 'FADEBELLY', 'FRONT', 'BLOSSOMSTEP', 'PEBBLE', 'TAILTWO', 'BUDDY', 'BACKSPOT', 'EYEBAGS'],
            ['BULLSEYE', 'FINN', 'DIGIT', 'KROPKA', 'FCTWO', 'FCONE', 'MIA', 'SCAR', 'BUSTER', 'SMOKEY', 'HAWKBLAZE', 'CAKE', 'ROSINA', 'PRINCESS'],
            ['LOCKET', 'BLAZEMASK', 'TEARS', 'DOUGIE', 'BALLER', 'PAINTSPLAT', 'REVERSETEARS', 'ELDER', 'TREFOIL', 'MANUL', 'REVERSETEARSTWO', 'GLOVE', 'REVERSENECK', 'NECK'],
            ['REVERSEHEAD', 'HEAD', 'DOTS', 'SPARSE', 'BADGER', 'FIVEPEBBLE', 'BELLY', 'CHARCOAL', 'MASK', 'LIGHTNING', 'SIAMESE', 'FROSTBITTEN', 'HEX', 'SNOWBELLY'],
            ['LIMBS', 'STRIPES', 'GLOWSTAR', 'STAR', 'SLICE', 'DEADPIXEL', 'ESCAPEE', 'INSPECTOR', 'FACEDOTS', 'TOONY', 'ACROBAT', 'WPTEARS', 'ONEEARTIP', 'NOSETIP'],
            ['DEFIBULATOR', 'WOLFX', 'TICKEDSPOTS', 'SHREDPATCH', 'TICKEDSTRIPE', 'SHREDONE', 'WOLFINSIDE', 'TICKEDSPOTSSTRIPE', 'SHREDTWO', 'WOLFOUTSIDETWO', 'TICKEDONE', 'WOLDOUTSIDEONE', 'TICKEDTWO', 'WOLFFILLONE'],
            ['TICKEDFILLONE', 'WOLFFILLTWO', 'TICKEDFILLTWO', 'TICKEDFILLTHREE', 'TREEFROG', 'GLOWWOLFX', 'ECHOBELLY', 'SPOOKYBONES',  'LURE', 'WATERMELONWAVE', 'WATERMELONSEEDS', 'FACEMASK', 'DEEP', 'STUFFED'],
            ['PLUSHIE', 'BROW', 'SCALETAIL', 'CARBON', 'SPARKLING', 'TOPFIN', 'LOWFIN', 'RIPPLE', "POPPY", "RISING", "LINE"]
        ]

        self.make_sprite_groups('whitepatches', white_patches, 'white')

        # Define colors and categories
        color_categories = [
            ['WHITE', 'SKY', 'BLUE', 'INDIGO', 'PURPLE', 'GHOST', 'BLACK'],
            ['CREAM', 'YELLOW', 'ORANGE', 'SCARLET', 'RED', 'PINK'],
            ['MINT', 'LIME', 'GREEN', 'MAROON', 'PERIWINKLE', 'LAVENDER']
        ]

        color_types = [
            'singlecolours', 'speckledcolours', 'tabbycolours', 'bengalcolours', 'marbledcolours',
            'rosettecolours', 'smokecolours', 'tickedcolours', 'mackerelcolours', 'classiccolours',
            'sokokecolours', 'agouticolours', 'singlestripecolours', 'maskedcolours', 'bananacolours',
            'centipedecolours', 'collaredcolours', 'concolours', 'gravelcolours', 'cyanlizardcolours',
            'slimemoldcolours', 'lanterncolours', 'vulturecolours', 'lizardcolours', 'leviathancolours',
            'fluffycolours', 'amoebacolours', 'seaslugcolours', 'yeekcolours', 'rustedcolours',
            'envoycolours', 'drizzlecolours', 'solacecolours', 'leafycolours', 'scaledcolours', 
            'dragonfruitcolours', 'necklacecolours', 'dreamercolours', 'duskdawncolours', 
            'seercolours', 'rottencolours', 'firecolours', 'countershadedcolours', 'cherrycolours',
            'oldgrowthcolours', 'sparklecatcolours', 'wolfcolours', 'sunsetcolours', 'hypnotistcolours',
            'ringedcolours', 'skinnycolours', 'sparsecolours', 'impishcolours', 'sportycolours', 
            'fizzycolours', 'skeletoncolours', 'shredcolours', 'glowingcolours', 'moldcolours',
            'swingcolours', 'lovebirdcolours', 'budgiecolours', 'amazoncolours', 'applecolours', 'bobacolours',
            'glittercolours', 'icecolours', 'iggycolours', 'manedcolours', 'patchworkcolours', 'robotcolours',
            'sunkencolours', 'tomocolours', 'whalecolours', 'pidgeoncolours', 'watermeloncolours',
            'dragonetcolours', 'salmoncolours', 'darkechocolours', 'lightechocolours', 'plantaincolours',
            'daenixcolours', 'seltzercolours', 'sworncolours', 'spookycolours', 'conurecolours', 'noblecolours',
            'bettacolours', 'constellationcolours', 'malibucolours', 'claycolours', 'antethisiscolours',
            'citadelcolours', 'gravecolours', 'interlopercolours'
        ]

        for color_type in color_types:
            self.make_sprite_groups(color_type, color_categories, color_type[:-7])

        # tortiepatchesmasks
        tortiepatchesmasks = [
            ['ONE', 'TWO', 'THREE', 'FOUR', 'REDTAIL', 'DELILAH', 'HALF', 'STREAK', 'MASK', 'SMOKE'],
            ['MINIMALONE', 'MINIMALTWO', 'MINIMALTHREE', 'MINIMALFOUR', 'OREO', 'SWOOP', 'CHIMERA', 'CHEST', 'ARMTAIL',
             'GRUMPYFACE'],
            ['MOTTLED', 'SIDEMASK', 'EYEDOT', 'BANDANA', 'PACMAN', 'STREAMSTRIKE', 'SMUDGED', 'DAUB', 'EMBER', 'BRIE'],
            ['ORIOLE', 'ROBIN', 'BRINDLE', 'PAIGE', 'ROSETAIL', 'SAFI', 'DAPPLENIGHT', 'BLANKET', 'BELOVED', 'BODY'],
            ['SHILOH', 'FRECKLED', 'HEARTBEAT', 'SPECKLES', 'TIGER', 'SHROOM', 'MAILBOX', 'GILAMONSTER', 'RINGEDMIMIC',
             'NECKLACEMIMIC']
        ]

        self.make_sprite_groups('tortiepatchesmasks', tortiepatchesmasks, 'tortiemask')
                
        # Empty skins
        skin_colors = [
            ['BLACK', 'PINK', 'DARKBROWN', 'BROWN', 'LIGHTBROWN', 'RED'],
            ['DARK', 'DARKGREY', 'GREY', 'DARKSALMON', 'SALMON', 'PEACH'],
            ['DARKMARBLED', 'MARBLED', 'LIGHTMARBLED', 'DARKBLUE', 'BLUE', 'LIGHTBLUE']
        ]

        self.make_sprite_groups('skin', skin_colors, 'skin')
                
        # Gills, Tongues, Quills
        gilltongue_rows = [
            ['PINKGILLS', 'BLUEGILLS', 'REDGILLS', 'LIMEGILLS', 'YELLOWGILLS', 'WHITEGILLS'],
            ['RAINBOWGILLS', 'FUCHSIATONGUE', 'PASTELTONGUE', 'KOBITONGUE', 'REDTONGUE', 'GREYTONGUE'],
            ['ORANGETONGUE', 'WHITESPOTS', 'BLACKSPOTS', 'MIXSPOTS', 'RAINBOWSPOTS', 'BLACKCLAWS'],
            ['WHITETENNA', 'REDTENNA', 'PINKTENNA', 'ORANGETENNA', 'YELLOWTENNA', 'BLUETENNA'],
            ['GREENTENNA', 'WHITEGLOWSPOTS', 'REDGLOWSPOTS', 'PINKGLOWSPOTS', 'ORANGEGLOWSPOTS', 'YELLOWGLOWSPOTS'],
            ['BLUEGLOWSPOTS', 'GREENGLOWSPOTS', 'GRAYGILLS', 'HOTGILLS', 'COLDGILLS']
        ]

        # Determine group name per row
        if game.settings["bea_gilltongue"]:
            group_rows = ['gilltongue', 'gilltongue', 'gilltongue', 'beagilltongue', 'beagilltongue', 'beagilltongue']
        else:
            group_rows = ['gilltongue'] * 6

        # Loop through and assign
        for group, colors in zip(group_rows, gilltongue_rows):
            self.make_sprite_groups(group, [colors], 'skin')

        # Horns - Ram, Scav, Elite, Sharp, Dragon, Lancer
        horns_colors = [
            ['WHITEHORNSRAM', 'BLACKHORNSRAM', 'REDHORNSRAM', 'YELLOWHORNSRAM', 'GREENHORNSRAM', 'BLUEHORNSRAM', 'ORANGEHORNSRAM', 'BROWNHORNSRAM'],
            ['WHITEHORNSSCAV', 'BLACKHORNSSCAV', 'REDHORNSSCAV', 'YELLOWHORNSSCAV', 'GREENHORNSSCAV', 'BLUEHORNSSCAV', 'ORANGEHORNSSCAV', 'BROWNHORNSSCAV'],
            ['WHITEHORNSELITE', 'BLACKHORNSELITE', 'REDHORNSELITE', 'YELLOWHORNSELITE', 'GREENHORNSELITE', 'BLUEHORNSELITE', 'ORANGEHORNSELITE', 'BROWNHORNSELITE'],
            ['WHITEHORNSSHARP', 'BLACKHORNSSHARP', 'REDHORNSSHARP', 'YELLOWHORNSSHARP', 'GREENHORNSSHARP', 'BLUEHORNSSHARP', 'ORANGEHORNSSHARP', 'BROWNHORNSSHARP'],
            ['WHITEHORNSDRAGON', 'BLACKHORNSDRAGON', 'REDHORNSDRAGON', 'YELLOWHORNSDRAGON', 'GREENHORNSDRAGON', 'BLUEHORNSDRAGON', 'ORANGEHORNSDRAGON', 'BROWNHORNSDRAGON'],
            ['WHITEHORNSLANCER', 'BLACKHORNSLANCER', 'REDHORNSLANCER', 'YELLOWHORNSLANCER', 'GREENHORNSLANCER', 'BLUEHORNSLANCER', 'ORANGEHORNSLANCER', 'BROWNHORNSLANCER']
        ]

        self.make_sprite_groups('horns', horns_colors, 'skin')

        #Whiskers - Catfish, Dragon
        whiskers_colors = [
            ['WHITECATFISHWHISKERS', 'PINKCATFISHWHISKERS', 'REDCATFISHWHISKERS', 'YELLOWCATFISHWHISKERS', 'GREENCATFISHWHISKERS', 'REDYELLOWCATFISHWHISKERS'],
            ['BLUECATFISHWHISKERS', 'PURPLECATFISHWHISKERS', 'BLACKCATFISHWHISKERS', 'BLUEGREENCATFISHWHISKERS', 'BLUEPINKCATFISHWHISKERS', 'BROWNCATFISHWHISKERS'],
            ['WHITEDRAGONWHISKERS', 'PINKDRAGONWHISKERS', 'REDDRAGONWHISKERS', 'YELLOWDRAGONWHISKERS', 'GREENDRAGONWHISKERS', 'REDYELLOWDRAGONWHISKERS'],
            ['BLUEDRAGONWHISKERS', 'PURPLEDRAGONWHISKERS', 'BLACKDRAGONWHISKERS', 'BLUEGREENDRAGONWHISKERS', 'BLUEPINKDRAGONWHISKERS', 'BROWNDRAGONWHISKERS']
        ]

        self.make_sprite_groups('whiskers', whiskers_colors, 'skin')

        # fancyskin spritesheet
        fancyskin_colors = [
            ['WHITEMOTH', 'BLACKMOTH', 'REDMOTH', 'YELLOWMOTH', 'GREENMOTH', 'BLUEMOTH', 'ORANGEMOTH', 'BROWNMOTH'],
            ['WHITEWHISKERS', 'BLACKWHISKERS', 'REDWHISKERS', 'YELLOWWHISKERS', 'GREENWHISKERS', 'BLUEWHISKERS', 'ORANGEWHISKERS', 'BROWNWHISKERS'],
            ['PINKFINS', 'BLUEFINS', 'REDFINS', 'GREENFINS', 'YELLOWFINS', 'WHITEFINS', 'BLACKNEEDLES', 'WHITENEEDLES'],
            ['WHITECYAN', 'ORANGECYAN', 'BROWNCYAN', 'PINKCYAN', 'PINKERCYAN', 'TEALCYAN', 'GREENCYAN', 'BLOODYCYAN'],
            ['LAVENDERCYAN', 'PURPLECYAN', 'CYANCYAN', 'BLUECYAN', 'DARKBLUECYAN', 'DARKPURPLECYAN', 'BLACKCYAN', 'EGGCYAN'],
            ['YELLOWCYAN', 'RAINBOWNEEDLES', 'CYANWINGS', 'ANGLERFISH', 'FIREBUGPART', 'TEARS', 'BLACKTHORNS', 'WHITETHORNS'],
            ['GLASSBACK', 'SEASLUGPAPILLAE', 'GRASSSHEEPBACK', 'SEAANGELWINGS', 'ANTLERS', 'LOACH', 'CENTIPEDEGROWTHS', 'ACROTAIL'],
            ['WHITECLAWS', 'PINKCLAWS', 'BLUECLAWS', 'GREENCLAWS', 'YELLOWCLAWS', 'REDCLAWS', 'GREYCLAWS'],
            ['BLACKSTINGER', 'GREYSTINGER', 'WHITESTINGER', 'GOLDSTINGER', 'PURPLEDROPWIG', 'GREENDROPWIG', 'BLUEDROPWIG']
        ]

        # Handle rows 0-6 with function
        self.make_sprite_groups('fancyskin', fancyskin_colors[:7], 'skin')

        # Handle row 7 seperately because it will suffer alone
        if len(fancyskin_colors) > 7:
            for col, color in enumerate(fancyskin_colors[7]):
                self.make_group('fancyskin', (col, 7), f"muddypaws{color}")

        # data games stuff spritesheet
        datagamesstuff_colors = [
            ['FAMILIARMARK', 'BLUETAILFRILLS', 'ORANGETAILFRILLS', 'GREENTAILFRILLS', 'PURPLETAILFRILLS'],
            ['PINKTAILFRILLS', 'REDTAILFRILLS', 'YELLOWTAILFRILLS', 'CYANTAILFRILLS', 'WHITEQUILLS'],
            ['BLACKQUILLS', 'YELLOWSPIKES', 'GREENSPIKES', 'AQUASPIKES', 'CYANSPIKES'],
            ['BLUESPIKES', 'PURPLESPIKES', 'PINKSPIKES', 'REDSPIKES', 'ORANGESPIKES']
        ]

        self.make_sprite_groups('datagamesstuff', datagamesstuff_colors, 'skin')

        # manes spritesheet
        manes_colors = [
            ['DARKBROWNMANE', 'CHOCOLATEMANE', 'GOLDENMANE'],
            ['BLONDMANE', 'GINGERMANE', 'SILVERMANE']
        ]

        self.make_sprite_groups('manes', manes_colors, 'skin')
                
        # overseertenna spritesheet
        overseertenna_colors = [
            ['WHITEOVERSEERTENNA', 'SKYOVERSEERTENNA', 'BLUEOVERSEERTENNA', 'INDIGOOVERSEERTENNA', 'PURPLEOVERSEERTENNA', 'GHOSTOVERSEERTENNA', 'BLACKOVERSEERTENNA'],
            ['CREAMOVERSEERTENNA', 'YELLOWOVERSEERTENNA', 'ORANGEOVERSEERTENNA', 'SCARLETOVERSEERTENNA', 'REDOVERSEERTENNA', 'PINKOVERSEERTENNA'],
            ['MINTOVERSEERTENNA', 'LIMEOVERSEERTENNA', 'GREENOVERSEERTENNA', 'MAROONOVERSEERTENNA', 'PERIWINKLEOVERSEERTENNA', 'LAVENDEROVERSEERTENNA']
        ]

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
        colorwings_colors = [
            ['WATCHERWINGS', 'ARTIFICERWINGS', 'HUNTERWINGS', 'SAINTWINGS'],
            ['RIVULETWINGS', 'SPEARMASTERWINGS', 'GOURMANDWINGS']
        ]

        self.make_sprite_groups('colorwings', colorwings_colors, 'skin')

        # whitepatchwings spritesheet
        whitepatchwings_colors = [
            ['WHITEWINGS', 'DARKCREAMWINGS', 'CREAMWINGS', 'OFFWHITEWINGS', 'GRAYWINGS', 'PINKWINGS'],
            ['BLACKWINGS', 'POWDERBLUEWINGS', 'SPLASHWINGS', 'PURPLEWINGS', 'BLACKBERRYWINGS', 'SANDWINGS'],
            ['CLAYWINGS', 'BRICKWINGS', 'SALMONWINGS', 'SEAFOAMWINGS', 'MINTWINGS', 'EVERGREENWINGS'],
            ['CRANBERRYWINGS', 'PEARLWINGS', 'ORCHIDWINGS', 'RUBYWINGS', 'CORALWINGS', 'TANWINGS'],
            ['LEMONWINGS', 'CLOVERWINGS', 'CYANWINGS', 'VIOLETWINGS', 'GOLDENWINGS']
        ]

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

        # Define scars
        scars_data = [
            ["ONE", "TWO", "THREE", "MANLEG", "BRIGHTHEART", "MANTAIL", "BRIDGE", "RIGHTBLIND", "LEFTBLIND",
             "BOTHBLIND", "BURNPAWS", "BURNTAIL"],
            ["BURNBELLY", "BEAKCHEEK", "BEAKLOWER", "BURNRUMP", "CATBITE", "RATBITE", "FROSTFACE", "FROSTTAIL",
             "FROSTMITT", "FROSTSOCK", "QUILLCHUNK", "QUILLSCRATCH"],
            ["TAILSCAR", "SNOUT", "CHEEK", "SIDE", "THROAT", "TAILBASE", "BELLY", "TOETRAP", "SNAKE", "LEGBITE",
             "NECKBITE", "FACE"],
            ["HINDLEG", "BACK", "QUILLSIDE", "SCRATCHSIDE", "TOE", "BEAKSIDE", "CATBITETWO", "SNAKETWO", "FOUR", 
             "ROTMARKED", "ROTRIDDEN", "TOPSURGERY"],
            ["CUTOPEN", "LABRATFACE", "VIVISECTION", "LABRATCHEST", "LABRATLIMBS", "NEUTRINO", "MANGLEDARM", 
             "ENVOYCHEST", "HALFFACELEFT", "FULLBODYBURNS", "BESIEGED", "HALFFACERIGHT"],
            ["STARBURN", "ARMBURN", "DOUBLEBITE", "DANGEROUS", "SMOKINGFACE", "NIBBLEDIDIOT", "X-FACE",
             "NIBBEDAGAIN", "MESSIAH", "EXTRACTIONTWO", "RESTITCHEDUPPER", "RESTITCHEDLOWER"],
            ["STITCHEDHEAD", "BURNTLEG", "BURNTARM", "VULTURESHOULDER", "CHEEKCUT", "MIROSNOM", "ARTIRIGHT",
            "ARTIGLOWRIGHT", "ARTILEFT", "ARTIGLOWLEFT", "SPEARWOUND", "PATCHWORK"],
            ["BLIZZARDBLAST", "TAIL", "SHOULDER", "EYE", "ARM"]
        ]

        # define missing parts
        missing_parts_data = [
            ["LEFTEAR", "RIGHTEAR", "NOTAIL", "NOLEFTEAR", "NORIGHTEAR", "NOEAR", "HALFTAIL", "NOPAW"]
        ]

        # scars 
        self.make_sprite_groups('scars', scars_data, 'scars')

        # missing parts
        self.make_sprite_groups('missingscars', missing_parts_data, 'scars')

        # accessories
        medcatherbs_data = [
            ["MAPLE LEAF", "HOLLY", "BLUE BERRIES", "FORGET ME NOTS", "RYE STALK", "LAUREL"],
            ["BLUEBELLS", "NETTLE", "POPPY", "LAVENDER", "HERBS", "PETALS"],
            [],  # Empty row because this is the wild data, except dry herbs.
            ["OAK LEAVES", "SCUGMINT", "MAPLE SEED", "JUNIPER", "SAKURA"]
        ]
        wild_data = [
            ["RED FEATHERS", "BLUE FEATHERS", "JAY FEATHERS", "MOTH WINGS", "CICADA WINGS"]
        ]
        collars_data = [
            ["CRIMSON", "BLUE", "YELLOW", "CYAN", "RED", "LIME"],
            ["GREEN", "RAINBOW", "BLACK", "SPIKES", "WHITE"],
            ["PINK", "PURPLE", "MULTI", "INDIGO"]
        ]
        bellcollars_data = [
            ["CRIMSONBELL", "BLUEBELL", "YELLOWBELL", "CYANBELL", "REDBELL", "LIMEBELL"],
            ["GREENBELL", "RAINBOWBELL", "BLACKBELL", "SPIKESBELL", "WHITEBELL"],
            ["PINKBELL", "PURPLEBELL", "MULTIBELL", "INDIGOBELL"]
        ]
        bowcollars_data = [
            ["CRIMSONBOW", "BLUEBOW", "YELLOWBOW", "CYANBOW", "REDBOW", "LIMEBOW"],
            ["GREENBOW", "RAINBOWBOW", "BLACKBOW", "SPIKESBOW", "WHITEBOW"],
            ["PINKBOW", "PURPLEBOW", "MULTIBOW", "INDIGOBOW"]
        ]
        nyloncollars_data = [
            ["CRIMSONNYLON", "BLUENYLON", "YELLOWNYLON", "CYANNYLON", "REDNYLON", "LIMENYLON"],
            ["GREENNYLON", "RAINBOWNYLON", "BLACKNYLON", "SPIKESNYLON", "WHITENYLON"],
            ["PINKNYLON", "PURPLENYLON", "MULTINYLON", "INDIGONYLON"]
        ]
        rwlizards_data = [
            ["BLUESKY", "BLUESEA", "PINKMAGENTA", "PINKPURPLE", "GREENEMERALD", "GREENLIME", "WHITEHIDDEN", "WHITEREVEALED", "BLACKNEUTRAL", "BLACKALERT"],
            ["YELLOWORANGE", "YELLOWLEMON", "REDTOMATO", "CYANBLUE", "CYANGREEN", "ALBISALAFUSHIA", "ALBISALARED", "MELASALARED", "MELASALAFUSHIA", "MELASALAPURPLE"]
        ]
        drones_data = [
            ["CRIMSONDRONE", "BLUEDRONE", "YELLOWDRONE", "CYANDRONE", "REDDRONE", "LIMEDRONE"],
            ["GREENDRONE", "RAINBOWDRONE", "BLACKDRONE", "SPIKESDRONE", "WHITEDRONE"],
            ["PINKDRONE", "PURPLEDRONE", "MULTIDRONE", "INDIGODRONE"]
        ]
        muddypaws_data = [
            ["MUDDYPAWS"]
        ]
        herbs2_data = [
            ["SPEAR", "PEARLEAR", "KARMAFLOWER", "LILCENTI", "PEARLNECK", "REDBATNIP"], 
            ["LILFLY","BATNIP", "FLASHFRUIT", "REDFLASHFRUIT", "GREENKELP", "REDKELP"], 
            ["VULTMASK", "KINGMASK", "SCAVMASK", "TREESEED", "GLOWSTONE", "BROWNKELP"], 
            ["LILBEETLE", "EXPLOSPEAR", "GREENDRAGFLY", "BLUEDRAGFLY", "ELESPEAR"]
        ]
        insectwings_data = [
            ["DEATHSHEAD", "BLUEBORDERED", "BLOODVEIN", "LARGEEMERALD", "CINNABAR", "LUNA", "ROSYMAPLE"],
            ["ATLAS", "HERCULES", "SUNSET", "PURPLEEMPEROR", "WHITEADMIRAL", "SWALLOWTAIL"]
        ]
        drones_data = [
            ["CRIMSONDRONE", "BLUEDRONE", "YELLOWDRONE", "CYANDRONE", "REDDRONE", "LIMEDRONE"],
            ["GREENDRONE", "RAINBOWDRONE", "BLACKDRONE", "SPIKESDRONE", "WHITEDRONE"],
            ["PINKDRONE", "PURPLEDRONE", "MULTIDRONE", "INDIGODRONE"]
        ]
        buddies_data = [
            ["MOUSEBLUE", "MOUSEYEL", "MOUSEPINK", "MOUSERED", "YEEKRED", "YEEKBLUE"], 
            ["VULTGRUB", "GRAPPLE", "SNAILGREEN", "SNAILBLUE", "SNAILRED", "SNAILPURPLE"],
            ["NOODLERED", "NOODLEPURPLE", "NOODLEGREY", "NOODLEBLUE", "NOODLEWHITE", "NOODLEPINK"],
            ["IGGYYELLOW", "IGGYPURPLE", "IGGYWHITE", "IGGYGREEN", "IGGYRED", "IGGYBLUE"],
            ["SQUIDBLACK", "SQUIDWHITE", "BUBBLE", "WORMGRASSPOT", "POLEPLANTPOT"]
        ]
        newaccs_data = [
            ["BATFLY", "BLUEFRUIT", "EMPTYBAG", "HERBSBAG", "INVEGG", "VOIDSPAWN"],
            ["REDARMOR", "OVERSEEREYE", "SPIDEREAR", "NEURONBLUE", "NEURONRED", "NEURONGREEN"],
            ["NEURONWHITE", "KARMAONE", "KARMATWO", "KARMATHREE", "KARMAFOUR", "SCROLL"],
            ["NECKLACESILVER", "NECKLACEGOLD", "TAILWRAP", "RAINCOAT", "LACESCARF", "TOLLMASK"],
            ["FLOWEREDMOSS", "MOSS", "MUSHROOMS", "MUSHROOMHAT", "GRENADE", "SANTAHAT"],
            ["EYEPATCH", 'INVMOUTH', "MOUSEYELPLUSH", "MOUSEREDPLUSH", "MOUSEBLUEPLUSH", "MOUSEPINKPLUSH"]
        ]
        newaccs2_data = [
            ["GLITCHING", "ROBOTARM", "ROBOTLEG", "SCRAPARMOR", "BLINDFOLD"],
            ["BRONZEPOCKETWATCH", "SILVERPOCKETWATCH", "GOLDPOCKETWATCH", "MURDERPAINT", "BOGMOSSBLUE"],
            ["BOGMOSSGREEN", "BOGMOSSLIME"],
            ["ORANGEPLANTPELT", "LIMEPLANTPELT", "GREENPLANTPELT", "YELLOWPLANTPELT", "BLUEPLANTPELT"]
        ]
        bodypaint_data = [
            ["REDPAINT", "PINKPAINT", "VOIDPAINT", "YELLOWPAINT", "GREENPAINT", "PALEPAINT"],
            ["CYANPAINT", "BLUEPAINT", "PURPLEPAINT", "MAGENTAPAINT", "BLACKPAINT", "WHITEPAINT"]
        ]
        implant_data = [
            ["IMPLANTWHITE", "IMPLANTPURPLE", "IMPLANTGREEN", "IMPLANTYELLOW", "IMPLANTBLUE"],
            ["EYEIMPLANTWHITE", "EYEIMPLANTRED", "EYEIMPLANTGREEN", "EYEIMPLANTYELLOW", "EYEIMPLANTBLUE"],
            ["GLOWWHITE", "GLOWPURPLE", "GLOWGREEN", "GLOWYELLOW", "GLOWBLUE"],
            ["CELLIMPLANT"]
        ]
        magic_data = [
            ["ORANGEFIRE", "GREENFIRE", "BLUEFIRE", "YELLOWFIRE", "WHITEFIRE", "PINKFIRE", "REDFIRE"],
            ["GREENRING", "CYANRING", "SILVERRING", "WHITERING", "YELLOWRING", "VOIDRING", "GOLDRING"],
            ["PETPEBBLE", "PETCLAY", "PETLAPIS", "PETAMETHYST", "PETJADE", "PETGRANITE", "PETSANDSTONE"]
        ]
        necklaces_data = [
            ["NECKLACEWHITE", "NECKLACEPINK", "NECKLACEPURPLE", "NECKLACEYELLOW", "NECKLACECYAN"],
            ["NECKLACEGREEN", "NECKLACERED", "NECKLACEORANGE", "NECKLACEBLUE", "NECKLACEBLACK"]
        ]
        drapery_data = [
            ["DRAPERYWHITE", "DRAPERYORANGE", "DRAPERYTAN", "DRAPERYPALEYELLOW", "DRAPERYYELLOW", "DRAPERYLIGHTMINT", "DRAPERYMINT", "DRAPERYGREEN", "DRAPERYLIGHTAQUA"],
            ["DRAPERYAQUA", "DRAPERYCYAN", "DRAPERYLIGHTGRAY", "DRAPERYPURPLE", "DRAPERYLIGHTINDIGO", "DRAPERYBLUE", "DRAPERYLAVENDER", "DRAPERYLIGHTPINK", "DRAPERYPINK"],
            ["DRAPERYHOTPINK", "DRAPERYGRAY", "DRAPERYDARKGRAY", "DRAPERYPALEPINK", "DRAPERYLIGHTRED", "DRAPERYRED", "DRAPERYPEACH", "DRAPERYLIGHTORANGE"]
        ]
        pridedrapery_data = [
            ["ORIGINALGAYDRAPERY", "TRANSDRAPERY", "GENDERQUEERDRAPERY", "AGENDERDRAPERY", "NONBINARYDRAPERY", "POLYAMDRAPERY", "GENDERFLUIDDRAPERY"],
            ["GENDERFLUXDRAPERY", "GAYDRAPERY", "OMNISEXUALDRAPERY", "OBJECTUMDRAPERY", "RAINBOWDRAPERY", "PHILIDRAPERY", "BISEXUALDRAPERY"],
            ["PANSEXUALDRAPERY", "POLYSEXUALDRAPERY", "ASEXUALDRAPERY", "LESBIANDRAPERY", "INTERSEXDRAPERY", "AROACEDRAPERY", "DEMIGIRLDRAPERY"],
            ["DEMIBOYDRAPERY", "DEMIGENDERDRAPERY", "DEMIFLUIDDRAPERY", "DEMIFLUXDRAPERY", "ABRODRAPERY", "ARODRAPERY", "DEMISEXDRAPERY"],
            ["DEMIRODRAPERY", "ACHILLEANDRAPERY", "SAPPHICDRAPERY", "DIAMORICDRAPERY", "UNLABELEDDRAPERY", "TRANSFEMDRAPERY", "TRANSMASCDRAPERY"],
            ["BIGENDERDRAPERY", "MULTISEXDRAPERY", "ACESPECDRAPERY", "AROSPECDRAPERY"]
        ]
        eyepatch_data = [
            ["EYEPATCHWHITE", "EYEPATCHGREEN", "EYEPATCHAQUA", "EYEPATCHTURQUOISE", "EYEPATCHCYAN", "EYEPATCHBLUE", "EYEPATCHINDIGO"],
            ["EYEPATCHPURPLE", "EYEPATCHMAGENTA", "EYEPATCHPINK", "EYEPATCHROSE", "EYEPATCHLIGHTGRAY", "EYEPATCHDARKGRAY", "EYEPATCHBLACK"],
            ["EYEPATCHRED", "EYEPATCHORANGE", "EYEPATCHAMBER", "EYEPATCHYELLOW", "EYEPATCHLIME"]
        ]
        larsaccs_data = [
            ["ALLSEEINGGOLD", "ALLSEEINGSILVER", "BESIEGEDMASKOG", "BESIEGEDMASKBLUE", "BESIEGEDMASKCYAN"],
            ["BESIEGEDMASKGRAY", "BESIEGEDMASKGREEN", "BESIEGEDMASKINDIGO", "BESIEGEDMASKORANGE", "BESIEGEDMASKPINK"],
            ["BESIEGEDMASKPURPLE", "BESIEGEDMASKRED", "BESIEGEDMASKROSE", "BESIEGEDMASKAQUA", "BESIEGEDMASKYELLOW"],
            ["HANDPEARLBLANK", "HANDPEARLBLUE", "HANDPEARLGREEN", "HANDPEARLORANGE", "HANDPEARLPURPLE"],
            ["HANDPEARLRED", "HANDPEARLYELLOW", "PEARLDRAPERY", "STRAIGHTGOLD", "STRAIGHTSILVER"]
        ]
    
        harleyaccs_data = [
            ["FALLENSTARMASK", "TORNCLOAKFALL", "FALLENSTARPAWS", "TORNCLOAKWINTER"],
            ["TORNCLOAKNIGHT", "TORNCLOAKSHADOW", "TORNCLOAKSILVER", "FAUXMANE"],
            ["SLEEPYROBEPURPLE", "SLEEPYROBEGREEN", "SLEEPYROBEBLACK", "SLEEPYROBERED"],
            ["SLEEPYROBEBLUE", "SLEEPYROBEFLOAH", "ITERATORPEARLNECKLACE", "AMBERJEWLERY"]
        ]

        featherboas_data = [
            ["DPINKFEATHERBOA", "DREDFEATHERBOA", "DGREENFEATHERBOA", "DBLUEFEATHERBOA", "DGREENERFEATHERBOA"],
            ["DORANGEFEATHERBOA", "LWHITEFEATHERBOA", "LPURPLEFEATHERBOA", "LBLUEFEATHERBOA", "LPINKFEATHERBOA"],
            ["DMAGENTAFEATHERBOA", "DCRIMSONFEATHERBOA", "DPURPLEFEATHERBOA"]
        ]

        scarves_data = [
            ["REDSCARF", "ORANGESCARF", "YELLOWSCARF", "LIMESCARF", "GREENSCARF", "CYANSCARF", "WHITESCARF"],
            ["BLUESCARF", "DARKBLUESCARF", "PURPLESCARF", "MAGENTASCARF", "BLACKSCARF", "GRAYSCARF", "BROWNSCARF"],
            ["NSHSCARF", "SAWYERSCARF"]
        ]
        
        neckbandanas_data = [
            ["DICEYNBANDANA", "EOUSNBANDANA", "FLUIDNBANDANA", "GUILDNBANDANA", "SKULLNBANDANA", "SKYNBANDANA", "SPACENBANDANA", "SWEETIENBANDANA"],
            ["TCYANNBANDANA", "TIEDYEMUDDYNBANDANA", "TIEDYENBANDANA", "TSAVNBANDANA", "BLUEGRADNBANDANA", "ORANGEGRADNBANDANA",  "YELLOWGRADNBANDANA", "LIMEGRADNBANDANA"],
            ["TEALGRADNBANDANA", "MAGENTAGRADNBANDANA", "REDGRADNBANDANA", "WHITENBANDANA", "LIGHTGRAYNBANDANA", "DARKGRAYNBANDANA", "BLACKNBANDANA", "PEACHNBANDANA"],
            ["PALEREDNBANDANA", "REDNBANDANA", "MAROONNBANDANA", "PALEORANGENBANDANA", "LIGHTORANGENBANDANA", "ORANGENBANDANA", "BROWNNBANDANA", "PALEYELLOWNBANDANA"],
            ["LIGHTYELLOWNBANDANA", "YELLOWNBANDANA", "PALEGREENNBANDANA", "LIGHTGREENNBANDANA", "GREENNBANDANA", "DARKGREENNBANDANA", "PALETEALNBANDANA", "LIGHTTEALNBANDANA"],
            ["TEALNBANDANA", "DARKTEALNBANDANA", "PALEBLUENBANDANA", "LIGHTBLUENBANDANA", "DARKBLUENBANDANA", "BLUENBANDANA", "LAVENDERNBANDANA", "PURPLENBANDANA"],
            ["DARKPURPLENBANDANA", "PALEPINKNBANDANA", "LIGHTPINKNBANDANA", "PINKNBANDANA", "DARKPINKNBANDANA", "PATCHWORKREDNBANDANA", "PATCHWORKORANGENBANDANA", "PATCHWORKYELLOWNBANDANA"],
            ["PATCHWORKGREENNBANDANA", "PATCHWORKTEALNBANDANA", "PATCHWORKBLUENBANDANA", "PATCHWORKINDIGONBANDANA", "PATCHWORKPURPLENBANDANA", "PATCHWORKPINKNBANDANA"]
        ]
        
        chains_data = [
            ["AMBERCHAIN", "PINKCHAIN", "PURPLECHAIN", "YELLOWCHAIN", "TEALCHAIN"],
            ["GREENCHAIN", "REDCHAIN", "ORANGECHAIN", "BLUECHAIN", "BLACKCHAIN"]
        ]

        newaccs3_data = [
            ["FALLMPAINT", "SCAVMPAINT", "SPEARMPAINT", "BLUECLOUDS", "RIBS"],
            ["YELLOWCLOUDS", "PURPLECLOUDS", "PINKCLOUDS", "GOGGLES", "MODSPEAR"],
            ["PINKPOLEPLANTBUDDY", "ORANGEPOLEPLANTBUDDY", "REDPOLEPLANTBUDDY", "EYEBAGS"],
            ["MAGNATEJEWLERY", "YELLOWKARMAWREATH", "BLUEKARMAWREATH", "PURPLEKARMAWREATH"],
            ["MOTHBUDDY", "BOOMERANG", "MOTHBUDDYTWO", "MIST"]
        ]

        floatyeyes_data = [
            ["YELLOWFLOATYEYES", "REDFLOATYEYES", "ORANGEFLOATYEYES"],
            ["LIMEFLOATYEYES", "GREENFLOATYEYES", "BLUEFLOATYEYES"],
            ["INDIGOFLOATYEYES"]
        ]

        morespears_data = [
            ["PURPLEINDIGOPSPEAR", "INDIGOPSPEAR", "PURPLEPSPEAR", "CYANPSPEAR", "BLUEPSPEAR", "BLUECYANPSPEAR"],
            ["GAYPSPEAR", "TURQUOISEPSPEAR", "TURQUOISEGREENPSPEAR", "LIMEGREENPSPEAR", "LIMEPSPEAR", "GREYPSPEAR"],
            ["GREENPSPEAR", "ORANGEPSPEAR", "REDPSPEAR", "REDPINKPSPEAR", "PURPLEPINKPSPEAR", "PINKPSPEAR"],
            ["MAGENTAPINKPSPEAR", "REDPURPLEPSPEAR", "BLUEPURPLEPSPEAR", "ROSEPINKPSPEAR", "GREENYELLOWPSPEAR", "LIMEYELLOWPSPEAR"],
            ["YELLOWPSPEAR", "REDFIRESPEAR", "ORANGEFIRESPEAR", "YELLOWFIRESPEAR", "PINKFIRESPEAR", "PURPLEFIRESPEAR"],
            ["DARKREDFIRESPEAR", "DARKPINKFIRESPEAR", "DARKORANGEFIRESPEAR", "DARKYELLOWFIRESPEAR"]
        ]

        flagaccs_data = [
            ["BLUEFLAG", "COOLFLAG", "GREENFLAG", "GREYFLAG", "ORANGEFLAG"],
            ["PINKFLAG", "PURPLEFLAG", "RAINBOWFLAG", "REDFLAG", "SINFLAG"],
            ["TEALFLAG", "WARMFLAG", "WHITEFLAG", "YELLOWFLAG"]
        ]

        haloaccs_data = [
            ["REDHALO", "ORANGEHALO", "YELLOWHALO", "GREENHALO", "TEALHALO"],
            ["CYANHALO", "INDIGOHALO", "BLUEHALO", "PURPLEHALO", "MAGENTAHALO"],
            ["PINKHALO", "WHITEHALO", "BLACKHALO"]
        ]

        ponchoaccs_data = [
            ["ORANGEPONCHO", "YELLOWPONCHO", "GREENPONCHO", "TEALPONCHO", "CYANPONCHO"],
            ["BLUEPONCHO", "PURPLEPONCHO", "PINKPONCHO", "REDPONCHO", "WHITEPONCHO"],
            ["BROWNPONCHO", "SILVERPONCHO", "BLACKPONCHO", "MLOCPONCHO", "VSSCPONCHO"],
            ["FAMILIARPONCHO", "NSHPONCHO"]
        ]

        glassesaccs_data = [
            ["SUNGLASSESPINK", "SUNGLASSESRED", "SUNGLASSESORANGE", "SUNGLASSESAMBER", "SUNGLASSESYELLOW", "SUNGLASSESLIME"],
            ["SUNGLASSESGREEN", "SUNGLASSESTEAL", "SUNGLASSESCYAN", "SUNGLASSESBLUE", "SUNGLASSESINDIGO", "SUNGLASSESPURPLE"],
            ["SUNGLASSESWHITE", "SUNGLASSES", "GLASSESRED", "GLASSESORANGE", "GLASSESAMBER", "GLASSESYELLOW"],
            ["GLASSESLIME", "GLASSESGREEN", "GLASSESTEAL", "GLASSESCYAN", "GLASSESBLUE", "GLASSESINDIGO"],
            ["GLASSESPURPLE", "GLASSESPINK"]
        ]

        orbitals_data = [
            ['ORANGEORBITAL', 'YELLOWORBITAL', 'EARTHORBITAL'],
            ['EARTHTWOORBITAL', 'PURPLEORBITAL', 'PINKORBITAL'], 
            ['REDORBITAL']
        ]
        
        vulturemasks_data = [
            ['VULTMASKONE', 'VULTMASKTWO', 'VULTMASK3', 'VULTMASK4', 'VULTMASK5', 'VULTMASK6', 'VULTMASK7', 'VULTMASK8'],
            ['VULTMASK9', 'VULTMASK10', 'VULTMASK11', 'VULTMASK12', 'VULTMASK13', 'VULTMASK14', 'VULTMASK15', 'VULTMASK16'], 
            ['VULTMASK17', 'VULTMASK18', 'VULTMASK19', 'VULTMASK20', 'VULTMASK21', 'VULTMASK22', 'VULTMASK23', 'VULTMASK24']
        ]
        
        iteratormasks_data = [
            ['BLUEITERATOR', 'BLACKITERATOR', 'GREENITERATOR', 'ORANGEITERATOR', 'PINKITERATOR', 'CYANITERATOR'],
            ['PURPLEITERATOR', 'REDITERATOR', 'CREAMITERATOR', 'WHITEITERATOR', 'YELLOWITERATOR']
        ]

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
