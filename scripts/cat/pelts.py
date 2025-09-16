import random
from random import choice
from re import sub

import ujson

from scripts.cat.sprites import sprites
from scripts.game_structure.game_essentials import game


class Pelt:

    with open("sprites/dicts/sprite_names.json", "r") as f:
            sprite_names_dict = ujson.loads(f.read())
    
    sprites_names = sprite_names_dict['sprites_names']

    eye_colours = sprite_names_dict['eye_colours']
    yellow_eyes = sprite_names_dict['yellow_eyes']
    blue_eyes = sprite_names_dict['blue_eyes']
    green_eyes = sprite_names_dict['green_eyes']
    red_eyes = sprite_names_dict['red_eyes']
    pupil_eyes = sprite_names_dict['pupil_eyes']
    yellow_pupil_eyes = sprite_names_dict['yellow_pupil_eyes']
    blue_pupil_eyes = sprite_names_dict['blue_pupil_eyes']
    green_pupil_eyes = sprite_names_dict['green_pupil_eyes']
    red_pupil_eyes = sprite_names_dict['red_pupil_eyes']
    riveye_colours = sprite_names_dict['riveye_colours']
    yellow_riv_eyes = sprite_names_dict['yellow_riv_eyes']
    blue_riv_eyes = sprite_names_dict['blue_riv_eyes']
    green_riv_eyes = sprite_names_dict['green_riv_eyes']
    red_riv_eyes = sprite_names_dict['red_riv_eyes']
    buttoneye_colours = sprite_names_dict['buttoneye_colours']
    yellow_button_eyes = sprite_names_dict['yellow_button_eyes']
    blue_button_eyes = sprite_names_dict['blue_button_eyes']
    green_button_eyes = sprite_names_dict['green_button_eyes']
    red_button_eyes = sprite_names_dict['red_button_eyes']
    bobaeye_colours = sprite_names_dict['bobaeye_colours']
    yellow_boba_eyes = sprite_names_dict['yellow_boba_eyes']
    blue_boba_eyes = sprite_names_dict['blue_boba_eyes']
    green_boba_eyes = sprite_names_dict['green_boba_eyes']
    red_boba_eyes = sprite_names_dict['red_boba_eyes']
    multi_eyes = sprite_names_dict['multi_eyes']
    geckoeyes_colors = sprite_names_dict['geckoeyes_colors']
    yellow_gecko_eyes = sprite_names_dict['yellow_gecko_eyes']
    blue_gecko_eyes = sprite_names_dict['blue_gecko_eyes']
    green_gecko_eyes = sprite_names_dict['green_gecko_eyes']
    red_gecko_eyes = sprite_names_dict['red_gecko_eyes']

    tabbies = sprite_names_dict['tabbies']
    spotted = sprite_names_dict['spotted']
    plain = sprite_names_dict['plain']
    exotic = sprite_names_dict['exotic']
    torties = sprite_names_dict['torties']

    pelt_categories = [tabbies, spotted, plain, exotic, torties]

    plant_accessories = sprite_names_dict['plant_accessories']
    wild_accessories = sprite_names_dict['wild_accessories']
    tail_accessories = sprite_names_dict['tail_accessories']
    collars = sprite_names_dict['collars']
    lizards = sprite_names_dict['lizards']
    muddypaws = sprite_names_dict['muddypaws']
    insectwings = sprite_names_dict['insectwings']
    herbs2 = sprite_names_dict['herbs2']
    buddies = sprite_names_dict['buddies']
    newaccs = sprite_names_dict['newaccs']
    newaccs2 = sprite_names_dict['newaccs2']
    bodypaint = sprite_names_dict['bodypaint']
    implant = sprite_names_dict['implant']
    magic = sprite_names_dict['magic']
    necklaces = sprite_names_dict['necklaces']
    drapery = sprite_names_dict['drapery']
    pridedrapery = sprite_names_dict['pridedrapery']
    eyepatches = sprite_names_dict['eyepatches']
    larsaccs = sprite_names_dict['larsaccs']
    harleyaccs = sprite_names_dict['harleyaccs']
    featherboas = sprite_names_dict['featherboas']
    scarves = sprite_names_dict['scarves']
    neckbandanas = sprite_names_dict['neckbandanas']
    chains = sprite_names_dict['chains']
    newaccs3 = sprite_names_dict['newaccs3']
    floatyeyes = sprite_names_dict['floatyeyes']
    morespears = sprite_names_dict['morespears']
    flagaccs = sprite_names_dict['flagaccs']
    haloaccs = sprite_names_dict['haloaccs']
    ponchoaccs = sprite_names_dict['ponchoaccs']
    glassesaccs = sprite_names_dict['glassesaccs']
    orbitals = sprite_names_dict['orbitals']
    vulturemasks = sprite_names_dict['vulturemasks']
    iteratormasks = sprite_names_dict['iteratormasks']
    basecollars = sprite_names_dict['basecollars']
    pearlcollars = sprite_names_dict['pearlcollars']
    studdedcollars = sprite_names_dict['studdedcollars']
    newaccs4 = sprite_names_dict['newaccs4']
    newaccs5 = sprite_names_dict['newaccs5']

        #list for stuff that should logically be behind a long tongue   
    closest_accs = (
        lizards + bodypaint + collars + implant + drapery + 
        pridedrapery + scarves + featherboas + chains + ponchoaccs + morespears + floatyeyes +
        harleyaccs + neckbandanas + basecollars + pearlcollars + studdedcollars +
        ["MUDDYPAWS", "CELLIMPLANT", "GOGGLES", "FALLMPAINT", "SCAVMPAINT", "SPEARMPAINT", "EYEBAGS", "MAGNATEJEWLERY", "YELLOWKARMAWREATH", "BLUEKARMAWREATH", "PURPLEKARMAWREATH",
        "MURDERPAINT", "BOGMOSSBLUE", "BOGMOSSGREEN", "BOGMOSSLIME", "ORANGEPLANTPELT", "LIMEPLANTPELT", "GREENPLANTPELT", "YELLOWPLANTPELT", "BLUEPLANTPELT", "FAUXMANE",
        "BLACKKARMAFLOWERWREATH", "GREENKARMAFLOWERWREATH", "PURPLEKARMAFLOWERWREATH", "REDKARMAFLOWERWREATH", "BLUEFLAMEMANE", "COOLFLAMEMANE", "COLORFULKARMAFLOWERWREATH",
        "MOONPEARLNECKLACE", "NSHPEARLNECKLACE", "BLOODYPAWS", "INKYPAWS", "INKTEARS", "REDBOW", "GREYBOW", "WHITEBOW", "BROWNBOW", "ORANGEBOW", "YELLOWBOW", "GREENBOW", 
        "TEALBOW", "BLUEBOW", "PURPLEBOW", "PINKBOW", "BLACKBOW"]
)
    scars1 = sprite_names_dict['scars1']
    scars2 = sprite_names_dict['scars2']
    scars3 = sprite_names_dict['scars3']

    skin_weights = game.config["feature_generation"]["feature_chances"]
    
    single_colours = sprite_names_dict['single_colours']
    warm_colours = sprite_names_dict['warm_colours']
    black_colours = sprite_names_dict['black_colours']
    white_colours = sprite_names_dict['white_colours']
    cool_colours = sprite_names_dict['cool_colours']
        # SPRITE NAMES
    colour_categories = [warm_colours, black_colours, white_colours, cool_colours]
    

    little_white = sprite_names_dict['little_white']
    mid_white = sprite_names_dict['mid_white']
    high_white = sprite_names_dict['high_white']
    mostly_white = sprite_names_dict['mostly_white']
    point_markings = sprite_names_dict['point_markings']
    vit = sprite_names_dict['vit']

    white_sprites = [little_white, mid_white, high_white, mostly_white, point_markings, vit, 'FULLWHITE']  

    tortiepatterns = sprite_names_dict['tortiepatterns']
    tortiebases = sprite_names_dict['tortiebases']

    pelt_length = sprite_names_dict['pelt_length']

    empty = sprite_names_dict['empty']
    claws = sprite_names_dict['claws']
    whiskers = sprite_names_dict['whiskers']
    antennae = sprite_names_dict['antennae']
    sharphorns = sprite_names_dict['sharphorns']
    ramhorns = sprite_names_dict['ramhorns']
    scavhorns = sprite_names_dict['scavhorns']
    elitehorns = sprite_names_dict['elitehorns']
    unihorns = sprite_names_dict['unihorns']
    antlers = sprite_names_dict['antlers']
    dragonhorns = sprite_names_dict['dragonhorns']
    moth = sprite_names_dict['moth']
    seaslugpapillae = sprite_names_dict['seaslugpapillae']
    tailfrills = sprite_names_dict['tailfrills']
    thorns = sprite_names_dict['thorns']
    glowspots = sprite_names_dict['glowspots']
    gills = sprite_names_dict['gills']
    tongues = sprite_names_dict['tongues']
    lizardneedles = sprite_names_dict['lizardneedles']
    spikes = sprite_names_dict['spikes']
    lizardfins = sprite_names_dict['lizardfins']
    catfishwhiskers = sprite_names_dict['catfishwhiskers']
    dragonwhiskers = sprite_names_dict['dragonwhiskers']
    quills = sprite_names_dict['quills']
    centipedegrowths = sprite_names_dict['centipedegrowths']
    stinger = sprite_names_dict['stinger']
    fangs = sprite_names_dict['fangs']
    anglerfish = sprite_names_dict['anglerfish']
    spearholes = sprite_names_dict['spearholes']
    cyanfeatures = sprite_names_dict['cyanfeatures']
    cyanwings = sprite_names_dict['cyanwings']
    firebugpart = sprite_names_dict['firebugpart']
    seaangelwings = sprite_names_dict['seaangelwings']
    loach = sprite_names_dict['loach']
    glassback = sprite_names_dict['glassback']
    grasssheepback = sprite_names_dict['grasssheepback']
    familiar = sprite_names_dict['familiar']
    acrotail = sprite_names_dict['acrotail']
    tears = sprite_names_dict['tears']
    manes = sprite_names_dict['manes']
    overseertenna = sprite_names_dict['overseertenna']
    budgiewings = sprite_names_dict['budgiewings']
    conurewings = sprite_names_dict['conurewings']
    lovebirdwings = sprite_names_dict['lovebirdwings']
    pidgeonwings = sprite_names_dict['pidgeonwings']
    vulturewings = sprite_names_dict['vulturewings']
    colorwings = sprite_names_dict['colorwings']
    whitefadewings = sprite_names_dict['whitefadewings']
    wings = sprite_names_dict['wings']
    dropwig = sprite_names_dict['dropwig']
    bodyeyes = sprite_names_dict['bodyeyes']
    limbfades = sprite_names_dict['limbfades']
    roboticspines = sprite_names_dict['roboticspines']
    chimneytail = sprite_names_dict['chimneytail']
    slimetraits = sprite_names_dict['slimetraits']
    kingtendrils = sprite_names_dict['kingtendrils']
    mechanical = sprite_names_dict['mechanical']
    wool = sprite_names_dict['wool']
    skin_categories = [ empty, claws, whiskers, antennae, sharphorns, ramhorns, scavhorns, elitehorns, unihorns, antlers,
                        dragonhorns, moth, seaslugpapillae, tailfrills, thorns, glowspots, gills, tongues, lizardneedles,
                        spikes, lizardfins, catfishwhiskers, dragonwhiskers, quills, centipedegrowths, stinger, fangs, anglerfish,
                        spearholes, cyanfeatures, cyanwings, firebugpart, seaangelwings, loach, dropwig, glassback, grasssheepback,
                        familiar, acrotail, tears, manes, overseertenna, budgiewings, conurewings, lovebirdwings, pidgeonwings,
                        vulturewings, colorwings, whitefadewings, wings, bodyeyes, limbfades, chimneytail, slimetraits, kingtendrils,
                        mechanical, wool
                    ]
    #list for stuff that should logically be behind a cloak
    closest_skin = sprite_names_dict['closest_skin']

    """Holds all appearance information for a cat. """

    def __init__(self,
                 name: str = "SingleColour",
                 length: str = "short",
                 colour: str = "WHITE",
                 white_patches: str = None,
                 eye_color: str = "BLUE",
                 eye_colour2: str = None,
                 tortiebase: str = None,
                 tortiecolour: str = None,
                 pattern: str = None,
                 tortiepattern: str = None,
                 vitiligo: str = None,
                 points: str = None,
                 accessory: str = None,
                 paralyzed: bool = False,
                 opacity: int = 100,
                 scars: list = None,
                 tint: str = "none",
                 skin: str = "BLACK",
                 white_patches_tint: str = "none",
                 kitten_sprite: int = None,
                 adol_sprite: int = None,
                 adult_sprite: int = None,
                 senior_sprite: int = None,
                 para_adult_sprite: int = None,
                 reverse: bool = False,
                 accessories:list=None,
                 inventory:list=[]
                 ) -> None:
        self.name = name
        self.colour = colour
        self.white_patches = white_patches
        self.eye_colour = eye_color
        self.eye_colour2 = eye_colour2
        self.tortiebase = tortiebase
        self.pattern = pattern
        self.tortiepattern = tortiepattern
        self.tortiecolour = tortiecolour
        self.vitiligo = vitiligo
        self.length = length
        self.points = points
        self.accessory = accessory
        self.accessories = accessories if accessories is not None else []
        self.inventory = inventory if inventory is not None else []
        self.paralyzed = paralyzed
        self.opacity = opacity
        self.scars = scars if isinstance(scars, list) else []
        self.tint = tint
        self.white_patches_tint = white_patches_tint
        self.cat_sprites = {"kitten": kitten_sprite if kitten_sprite is not None else 0,
                            "adolescent": adol_sprite if adol_sprite is not None else 0,
                            "young adult": adult_sprite if adult_sprite is not None else 0,
                            "adult": adult_sprite if adult_sprite is not None else 0,
                            "senior adult": adult_sprite if adult_sprite is not None else 0,
                            "senior": senior_sprite if senior_sprite is not None else 0,
                            "para_adult": para_adult_sprite if para_adult_sprite is not None else 0,
                            'newborn': 20,
                            'para_young': 17,
                            "sick_adult": 18,
                            "sick_young": 19}

        self.reverse = reverse
        self.skin = skin

    @staticmethod
    def generate_new_pelt(gender: str, parents: tuple = (), age: str = "adult"):
        new_pelt = Pelt()

        pelt_white = new_pelt.init_pattern_color(parents, gender)
        new_pelt.init_white_patches(pelt_white, parents)
        new_pelt.init_sprite()
        new_pelt.init_scars(age)
        new_pelt.init_accessories(age)
        new_pelt.init_eyes(parents)
        new_pelt.init_pattern()
        new_pelt.init_tint()
        new_pelt.common_combinations()

        return new_pelt

    def check_and_convert(self, convert_dict):
        """Checks for old-type properties for the appearance-related properties
        that are stored in Pelt, and converts them. To be run when loading a cat in. """
        
        # First, convert from some old names that may be in white_patches. 
        
        if self.name == "Conductor":
            self.name = "Con"
        if self.tortiebase == "conductor":
            self.tortiebase = "con"
        if self.tortiepattern == "conductor":
            self.tortiepattern = "con"

        if self.white_patches == 'POINTMARK':
            self.white_patches = "SEALPOINT"
        elif self.white_patches == 'PANTS2':
            self.white_patches = 'PANTSTWO'
        elif self.white_patches == 'ANY2':
            self.white_patches = 'ANYTWO'
        elif self.white_patches == "VITILIGO2":
            self.white_patches = "VITILIGOTWO"
            
        if self.vitiligo == "VITILIGO2":
            self.vitiligo = "VITILIGOTWO"

        # color conversions 
        if self.colour == 'PALEGREY':
            self.colour = 'SKY'
        elif self.colour == 'SILVER':
            self.colour = 'BLUE'
        elif self.colour == 'GREY':
            self.colour = 'INDIGO'
        elif self.colour == 'DARKGREY':
            self.colour = 'PURPLE'
        elif self.colour == 'PALEGINGER':
            self.colour = 'YELLOW'
        elif self.colour == 'GOLDEN':
            self.colour = 'ORANGE'
        elif self.colour == 'GINGER':
            self.colour = 'SCARLET'
        elif self.colour == 'DARKGINGER':
            self.colour = 'RED'
        elif self.colour == 'SIENNA':
            self.colour = 'PINK'
        elif self.colour == 'LIGHTBROWN':
            self.colour = 'MINT'
        elif self.colour == 'LILAC':
            self.colour = 'LIME'
        elif self.colour == 'BROWN':
            self.colour = 'GREEN'
        elif self.colour == 'GOLDEN-BROWN':
            self.colour = 'MAROON'
        elif self.colour == 'DARKBROWN':
            self.colour = 'PERIWINKLE'
        elif self.colour == 'CHOCOLATE':
            self.colour = 'LAVENDER'
            
        if self.tortiecolour:
            if self.tortiecolour == 'PALEGREY':
                self.tortiecolour = 'SKY'
            elif self.tortiecolour == 'SILVER':
                self.tortiecolour = 'BLUE'
            elif self.tortiecolour == 'GREY':
                self.tortiecolour = 'INDIGO'
            elif self.tortiecolour == 'DARKGREY':
                self.tortiecolour = 'PURPLE'
            elif self.tortiecolour == 'PALEGINGER':
                self.tortiecolour = 'YELLOW'
            elif self.tortiecolour == 'GOLDEN':
                self.tortiecolour = 'ORANGE'
            elif self.tortiecolour == 'GINGER':
                self.tortiecolour = 'SCARLET'
            elif self.tortiecolour == 'DARKGINGER':
                self.tortiecolour = 'RED'
            elif self.tortiecolour == 'SIENNA':
                self.tortiecolour = 'PINK'
            elif self.tortiecolour == 'LIGHTBROWN':
                self.tortiecolour = 'MINT'
            elif self.tortiecolour == 'LILAC':
                self.tortiecolour = 'LIME'
            elif self.tortiecolour == 'BROWN':
                self.tortiecolour = 'GREEN'
            elif self.tortiecolour == 'GOLDEN-BROWN':
                self.tortiecolour = 'MAROON'
            elif self.tortiecolour == 'DARKBROWN':
                self.tortiecolour = 'PERIWINKLE'
            elif self.tortiecolour == 'CHOCOLATE':
                self.tortiecolour = 'LAVENDER'

        # tint conversions
        #if self.tint in convert_dict["old_tints"]:
        #    self.tint = convert_dict["old_tints"][self.tint]

        if self.white_patches_tint in convert_dict["old_white_patch_tints"]:
            self.white_patches_tint = convert_dict["old_white_patch_tints"][self.white_patches_tint]
        
        # Move white_patches that should be in vit or points. 
        if self.white_patches in Pelt.vit:
            self.vitiligo = self.white_patches
            self.white_patches = None
        elif self.white_patches in Pelt.point_markings:
            self.points = self.white_patches
            self.white_patches = None

        if self.tortiepattern and "tortie" in self.tortiepattern:
            self.tortiepattern = sub("tortie", "", self.tortiepattern.lower())
            if self.tortiepattern == "solid":
                self.tortiepattern = "single"

        if self.white_patches in convert_dict["old_creamy_patches"]:
            self.white_patches = convert_dict["old_creamy_patches"][self.white_patches]
            self.white_patches_tint = "darkcream"
        elif self.white_patches in ['SEPIAPOINT', 'MINKPOINT', 'SEALPOINT']:
            self.white_patches_tint = "none"

        # Eye Color Convert Stuff
        if self.eye_colour == "BLUE2":
            self.eye_colour = "COBALT"
        if self.eye_colour2 == "BLUE2":
            self.eye_colour2 = "COBALT"

        if self.eye_colour in ["BLUEYELLOW", "BLUEGREEN"]:
            if self.eye_colour == "BLUEYELLOW":
                self.eye_colour2 = "YELLOW"
            elif self.eye_colour == "BLUEGREEN":
                self.eye_colour2 = "GREEN"
            self.eye_colour = "BLUE"
            
        # Convert the old skin
        if self.skin in convert_dict["old_sharphorns"]:
            self.skin = convert_dict["old_sharphorns"][self.skin]

        if self.length == 'long':
            if self.cat_sprites['adult'] not in [9, 10, 11]:
                if self.cat_sprites['adult'] == 0:
                    self.cat_sprites['adult'] = 9
                elif self.cat_sprites['adult'] == 1:
                    self.cat_sprites['adult'] = 10
                elif self.cat_sprites['adult'] == 2:
                    self.cat_sprites['adult'] = 11
                self.cat_sprites['young adult'] = self.cat_sprites['adult']
                self.cat_sprites['senior adult'] = self.cat_sprites['adult']
                self.cat_sprites['para_adult'] = 16
        else:
            self.cat_sprites['para_adult'] = 15
        if self.cat_sprites['senior'] not in [12, 13, 14]:
            if self.cat_sprites['senior'] == 3:
                self.cat_sprites['senior'] = 12
            elif self.cat_sprites['senior'] == 4:
                self.cat_sprites['senior'] = 13
            elif self.cat_sprites['senior'] == 5:
                self.cat_sprites['senior'] = 14
        
        if self.pattern in convert_dict["old_tortie_patches"]:
            old_pattern = self.pattern
            self.pattern = convert_dict["old_tortie_patches"][old_pattern][1]

            # If the pattern is old, there is also a chance the base color is stored in
            # tortiecolour. That may be different from the pelt color ("main" for torties)
            # generated before the "ginger-on-ginger" update. If it was generated after that update,
            # tortiecolour and pelt_colour will be the same. Therefore, let's also re-set the pelt color
            self.colour = self.tortiecolour
            self.tortiecolour = convert_dict["old_tortie_patches"][old_pattern][0]
            
        if self.pattern == "MINIMAL1":
            self.pattern = "MINIMALONE"
        elif self.pattern == "MINIMAL2":
            self.pattern = "MINIMALTWO"
        elif self.pattern == "MINIMAL3":
            self.pattern = "MINIMALTHREE"
        elif self.pattern == "MINIMAL4":
            self.pattern = "MINIMALFOUR"
        
    def init_eyes(self, parents):
        if not parents:
            self.eye_colour = choice(Pelt.eye_colours)
        else:
            self.eye_colour = choice([i.pelt.eye_colour for i in parents] + [choice(Pelt.eye_colours)])

        multieyenum = game.config["cat_generation"]["base_multieyes"]
        riveyenum = game.config["cat_generation"]["base_riveyes"]
        buttoneyenum = game.config["cat_generation"]["base_buttoneyes"]
        bobaeyenum = game.config["cat_generation"]["base_bobaeyes"]
        geckoeyenum = game.config["cat_generation"]["base_geckoeyes"]

        if not random.randint(0, riveyenum):
            self.eye_colour = choice(Pelt.riveye_colours)
        elif not random.randint(0, buttoneyenum):
            self.eye_colour = choice(Pelt.buttoneye_colours)
        elif not random.randint(0, bobaeyenum):
            self.eye_colour = choice(Pelt.bobaeye_colours)
        elif not random.randint(0, geckoeyenum):
            self.eye_colour = choice(Pelt.geckoeyes_colors)

        # White patches must be initalized before eye color.
        num = game.config["cat_generation"]["base_heterochromia"]
        if self.white_patches in [Pelt.high_white, Pelt.mostly_white, 'FULLWHITE'] or self.colour == 'WHITE':
            num = num - 20
        if self.eye_colour in Pelt.buttoneye_colours:
            num -= 5
        for _par in parents:
            if _par.pelt.eye_colour2:
                num -= 10

        if num < 0:
            num = 1

        if not random.randint(0, num):
            if self.eye_colour in Pelt.pupil_eyes:
                colour_wheel = [Pelt.yellow_pupil_eyes, Pelt.blue_pupil_eyes, Pelt.green_pupil_eyes, Pelt.red_pupil_eyes]
            elif self.eye_colour in Pelt.riveye_colours:
                colour_wheel = [Pelt.yellow_riv_eyes, Pelt.blue_riv_eyes, Pelt.green_riv_eyes, Pelt.red_riv_eyes]
            elif self.eye_colour in Pelt.buttoneye_colours:
                colour_wheel = [Pelt.yellow_button_eyes, Pelt.blue_button_eyes, Pelt.green_button_eyes, Pelt.red_button_eyes]
            elif self.eye_colour in Pelt.bobaeye_colours:
                colour_wheel = [Pelt.yellow_boba_eyes, Pelt.blue_boba_eyes, Pelt.green_boba_eyes, Pelt.red_boba_eyes]
            elif self.eye_colour in Pelt.geckoeyes_colors:
                colour_wheel = [Pelt.yellow_gecko_eyes, Pelt.blue_gecko_eyes, Pelt.green_gecko_eyes, Pelt.red_gecko_eyes]
            else:
                colour_wheel = [Pelt.yellow_eyes, Pelt.blue_eyes, Pelt.green_eyes, Pelt.red_eyes]
            for colour in colour_wheel[:]:
                if self.eye_colour in colour:
                    colour_wheel.remove(colour) # removes the selected list from the options
                    self.eye_colour2 = choice(choice(colour_wheel)) # choose from the remaining 3 lists
                    break

        elif 'MULTI'+self.eye_colour in Pelt.multi_eyes and not random.randint(0, multieyenum):
            self.eye_colour2 = 'MULTI'+self.eye_colour

    def pattern_color_inheritance(self, parents: tuple = (), gender="female"):
        # setting parent pelt categories
        # We are using a set, since we don't need this to be ordered, and sets deal with removing duplicates.
        par_peltlength = set()
        par_peltcolours = set()
        par_peltnames = set()
        par_pelts = []
        par_white = []
        for p in parents:
            if p:
                # Gather pelt color.
                par_peltcolours.add(p.pelt.colour)

                # Gather pelt length
                par_peltlength.add(p.pelt.length)

                # Gather pelt name
                if p.pelt.name in Pelt.torties:
                    par_peltnames.add(p.pelt.tortiebase.capitalize())
                else:
                    par_peltnames.add(p.pelt.name)

                # Gather exact pelts, for direct inheritance.
                par_pelts.append(p.pelt)

                # Gather if they have white in their pelt.
                par_white.append(p.pelt.white)
            else:
                # If order for white patches to work correctly, we also want to randomly generate a "pelt_white"
                # for each "None" parent (missing or unknown parent)
                par_white.append(bool(random.getrandbits(1)))

                # Append None
                # Gather pelt color.
                par_peltcolours.add(None)
                par_peltlength.add(None)
                par_peltnames.add(None)

        # If this list is empty, something went wrong.
        if not par_peltcolours:
            print("Warning - no parents: pelt randomized")
            return self.randomize_pattern_color(gender)

        # There is a 1/10 chance for kits to have the exact same pelt as one of their parents
        if not random.randint(0, game.config["cat_generation"]["direct_inheritance"]):  # 1/10 chance
            selected = choice(par_pelts)
            self.name = selected.name
            self.length = selected.length
            self.colour = selected.colour
            self.tortiebase = selected.tortiebase
            return selected.white

        # ------------------------------------------------------------------------------------------------------------#
        #   PELT
        # ------------------------------------------------------------------------------------------------------------#

        # Determine pelt.
        weights = [0, 0, 0, 0]  # Weights for each pelt group. It goes: (tabbies, spotted, plain, exotic)
        for p_ in par_peltnames:
            if p_ in Pelt.tabbies:
                add_weight = (50, 10, 5, 7)
            elif p_ in Pelt.spotted:
                add_weight = (10, 50, 5, 5)
            elif p_ in Pelt.plain:
                add_weight = (5, 5, 50, 0)
            elif p_ in Pelt.exotic:
                add_weight = (15, 15, 1, 45)
            elif p_ is None:  # If there is at least one unknown parent, a None will be added to the set.
                add_weight = (35, 20, 30, 15)
            else:
                add_weight = (0, 0, 0, 0)

            for x in range(0, len(weights)):
                weights[x] += add_weight[x]

        # A quick check to make sure all the weights aren't 0
        if all([x == 0 for x in weights]):
            weights = [1, 1, 1, 1]

        # Now, choose the pelt category and pelt. The extra 0 is for the tortie pelts,
        chosen_pelt = choice(
            random.choices(Pelt.pelt_categories, weights=weights + [0], k=1)[0]
        )

        # Tortie chance
        tortie_chance_f = game.config["cat_generation"][
            "base_female_tortie"]  # There is a default chance for female tortie
        tortie_chance_m = game.config["cat_generation"]["base_male_tortie"]
        for p_ in par_pelts:
            if p_.name in Pelt.torties:
                tortie_chance_f = int(tortie_chance_f / 2)
                tortie_chance_m = tortie_chance_m - 1
                break

        # Determine tortie:
        if gender == "female":
            torbie = random.getrandbits(tortie_chance_f) == 1
        else:
            torbie = random.getrandbits(tortie_chance_m) == 1

        chosen_tortie_base = None
        if torbie:
            # If it is tortie, the chosen pelt above becomes the base pelt.
            chosen_tortie_base = chosen_pelt
            if chosen_tortie_base in ["TwoColour", "SingleColour"]:
                chosen_tortie_base = "Single"
            chosen_tortie_base = chosen_tortie_base.lower()
            chosen_pelt = random.choice(Pelt.torties)

        # ------------------------------------------------------------------------------------------------------------#
        #   PELT COLOUR
        # ------------------------------------------------------------------------------------------------------------#
        # Weights for each colour group. It goes: (ginger_colours, black_colours, white_colours, brown_colours)
        weights = [0, 0, 0, 0]
        for p_ in par_peltcolours:
            if p_ in Pelt.warm_colours:
                add_weight = (40, 0, 0, 10)
            elif p_ in Pelt.black_colours:
                add_weight = (0, 40, 2, 5)
            elif p_ in Pelt.white_colours:
                add_weight = (0, 5, 40, 0)
            elif p_ in Pelt.cool_colours:
                add_weight = (10, 5, 0, 35)
            elif p_ is None:
                add_weight = (40, 40, 40, 40)
            else:
                add_weight = (0, 0, 0, 0)

            for x in range(0, len(weights)):
                weights[x] += add_weight[x]

            # A quick check to make sure all the weights aren't 0
            if all([x == 0 for x in weights]):
                weights = [1, 1, 1, 1]

        chosen_pelt_color = choice(
            random.choices(Pelt.colour_categories, weights=weights, k=1)[0]
        )

        # ------------------------------------------------------------------------------------------------------------#
        #   PELT LENGTH
        # ------------------------------------------------------------------------------------------------------------#

        weights = [0, 0, 0]  # Weights for each length. It goes (short, medium, long)
        for p_ in par_peltlength:
            if p_ == "short":
                add_weight = (50, 10, 2)
            elif p_ == "medium":
                add_weight = (25, 50, 25)
            elif p_ == "long":
                add_weight = (2, 10, 50)
            elif p_ is None:
                add_weight = (10, 10, 10)
            else:
                add_weight = (0, 0, 0)

            for x in range(0, len(weights)):
                weights[x] += add_weight[x]

        # A quick check to make sure all the weights aren't 0
        if all([x == 0 for x in weights]):
            weights = [1, 1, 1]

        chosen_pelt_length = random.choices(Pelt.pelt_length, weights=weights, k=1)[0]

        # ------------------------------------------------------------------------------------------------------------#
        #   PELT WHITE
        # ------------------------------------------------------------------------------------------------------------#

        # There are 94 percentage points that can be added by
        # parents having white. If we have more than two, this
        # will keep that the same.
        percentage_add_per_parent = int(94 / len(par_white))
        chance = 3
        for p_ in par_white:
            if p_:
                chance += percentage_add_per_parent

        chosen_white = random.randint(1, 100) <= chance

        # Adjustments to pelt chosen based on if the pelt has white in it or not.
        if chosen_pelt in ["TwoColour", "SingleColour"]:
            if chosen_white:
                chosen_pelt = "TwoColour"
            else:
                chosen_pelt = "SingleColour"
        elif chosen_pelt == "Calico":
            if not chosen_white:
                chosen_pelt = "Tortie"

        # SET THE PELT
        self.name = chosen_pelt
        self.colour = chosen_pelt_color
        self.length = chosen_pelt_length
        self.tortiebase = chosen_tortie_base  # This will be none if the cat isn't a tortie.
        return chosen_white

    def randomize_pattern_color(self, gender):
        # ------------------------------------------------------------------------------------------------------------#
        #   PELT
        # ------------------------------------------------------------------------------------------------------------#

        # Determine pelt.
        chosen_pelt = choice(
            random.choices(Pelt.pelt_categories, weights=(35, 20, 30, 15, 0), k=1)[0]
        )

        # Tortie chance
        # There is a default chance for female tortie, slightly increased for completely random generation.
        tortie_chance_f = game.config["cat_generation"]["base_female_tortie"] - 1
        tortie_chance_m = game.config["cat_generation"]["base_male_tortie"]
        if gender == "female":
            torbie = random.getrandbits(tortie_chance_f) == 1
        else:
            torbie = random.getrandbits(tortie_chance_m) == 1

        chosen_tortie_base = None
        if torbie:
            # If it is tortie, the chosen pelt above becomes the base pelt.
            chosen_tortie_base = chosen_pelt
            if chosen_tortie_base in ["TwoColour", "SingleColour"]:
                chosen_tortie_base = "Single"
            chosen_tortie_base = chosen_tortie_base.lower()
            chosen_pelt = random.choice(Pelt.torties)

        # ------------------------------------------------------------------------------------------------------------#
        #   PELT COLOUR
        # ------------------------------------------------------------------------------------------------------------#

        chosen_pelt_color = choice(
            random.choices(Pelt.colour_categories, k=1)[0]
        )

        # ------------------------------------------------------------------------------------------------------------#
        #   PELT LENGTH
        # ------------------------------------------------------------------------------------------------------------#

        chosen_pelt_length = random.choice(Pelt.pelt_length)

        # ------------------------------------------------------------------------------------------------------------#
        #   PELT WHITE
        # ------------------------------------------------------------------------------------------------------------#

        chosen_white = random.randint(1, 100) <= 40

        # Adjustments to pelt chosen based on if the pelt has white in it or not.
        if chosen_pelt in ["TwoColour", "SingleColour"]:
            if chosen_white:
                chosen_pelt = "TwoColour"
            else:
                chosen_pelt = "SingleColour"
        elif chosen_pelt == "Calico":
            if not chosen_white:
                chosen_pelt = "Tortie"

        self.name = chosen_pelt
        self.colour = chosen_pelt_color
        self.length = chosen_pelt_length
        self.tortiebase = chosen_tortie_base  # This will be none if the cat isn't a tortie.
        return chosen_white

    def init_pattern_color(self, parents, gender) -> bool:
        """Inits self.name, self.colour, self.length, 
            self.tortiebase and determines if the cat 
            will have white patche or not. 
            Return TRUE is the cat should have white patches, 
            false is not. """

        if parents:
            # If the cat has parents, use inheritance to decide pelt.
            chosen_white = self.pattern_color_inheritance(parents, gender)
        else:
            chosen_white = self.randomize_pattern_color(gender)

        return chosen_white

    def init_sprite(self):
        self.cat_sprites = {
            'newborn': 20,
            'kitten': random.randint(0, 2),
            'adolescent': random.randint(3, 5),
            'senior': random.randint(12, 14),
            'sick_young': 19,
            'sick_adult': 18
        }
        self.reverse = bool(random.getrandbits(1))
        # skin chances
        self.skin = choice(
            random.choices(Pelt.skin_categories, Pelt.skin_weights, k=1)[0]
        )

        if self.length != 'long':
            self.cat_sprites['adult'] = random.randint(6, 8)
            self.cat_sprites['para_adult'] = 16
        else:
            self.cat_sprites['adult'] = random.randint(9, 11)
            self.cat_sprites['para_adult'] = 15
        self.cat_sprites['young adult'] = self.cat_sprites['adult']
        self.cat_sprites['senior adult'] = self.cat_sprites['adult']

    def init_scars(self, age):
        if age == "newborn":
            return

        if age in ['kitten', 'adolescent']:
            scar_choice = random.randint(0, 50)  # 2%
        elif age in ['young adult', 'adult']:
            scar_choice = random.randint(0, 20)  # 5%
        else:
            scar_choice = random.randint(0, 15)  # 6.67%

        mutilation_scars = [
            "CUTOPEN",
            "BESIEGED",
            "VIVISECTION", 
            "LABRATCHEST", 
            "LABRATLIMBS", 
            "RESTITCHEDUPPER", 
            "RESTITCHEDLOWER", 
            "STITCHEDHEAD",
            "EXTRACTIONTWO", 
            "MESSIAH", 
            "ENVOYCHEST",
            "PATCHWORK"
        ]

        if scar_choice == 1:
            self.scars.append(choice([
                choice(Pelt.scars1),
                choice(Pelt.scars3)
            ]))

        if age in ['kitten', 'adolescent']:
            for i in self.scars:
                if i in mutilation_scars:
                    self.scars.remove(i)

        if 'NOTAIL' in self.scars and 'HALFTAIL' in self.scars:
            self.scars.remove('HALFTAIL')
        if 'ROTRIDDEN' in self.scars and 'ROTMARKED' in self.scars:
            self.scars.remove('ROTMARKED')

    def init_accessories(self, age):
        if age == "newborn":
            self.accessory = None
            return

        acc_display_choice = random.randint(0, 50)
        if age in ['kitten', 'adolescent']:
            acc_display_choice = random.randint(0, 150)
        elif age in ['young adult', 'adult']:
            acc_display_choice = random.randint(0, 70)

        if acc_display_choice == 1:
            self.accessories.append(choice([
                choice(Pelt.plant_accessories),
                choice(Pelt.wild_accessories),
                choice(Pelt.collars),
                choice(Pelt.lizards),
                choice(Pelt.insectwings),
                choice(Pelt.herbs2),
                choice(Pelt.buddies),
                choice(Pelt.newaccs),
                choice(Pelt.bodypaint),
                choice(Pelt.necklaces),
                choice(Pelt.larsaccs),
                choice(Pelt.scarves),
                choice(Pelt.neckbandanas),
                choice(Pelt.morespears),
                choice(Pelt.drapery),
                choice(Pelt.pridedrapery),
                choice(Pelt.featherboas),
                choice(Pelt.chains),
                choice(Pelt.floatyeyes),
                choice(Pelt.flagaccs),
                choice(Pelt.ponchoaccs),
                choice(Pelt.glassesaccs),
                choice(Pelt.orbitals),
                choice(Pelt.vulturemasks)
            ]))
        else:
            self.accessories = []

    def init_pattern(self):
        if self.name in Pelt.torties:
            if not self.tortiebase:
                self.tortiebase = choice(Pelt.tortiebases)
            if not self.pattern:
                self.pattern = choice(Pelt.tortiepatterns)

            wildcard_chance = game.config["cat_generation"]["wildcard_tortie"]
            if self.colour:
                # The "not wildcard_chance" allows users to set wildcard_tortie to 0
                # and always get wildcard torties.
                if not wildcard_chance or random.getrandbits(wildcard_chance) == 1:
                    # This is the "wildcard" chance, where you can get funky combinations.
                    # people are fans of the print message, so I'm putting it back
                    print("Wildcard tortie!")

                    # Allow any pattern:
                    self.tortiepattern = choice(Pelt.tortiebases)

                    # Allow any colors that aren't the base color.
                    possible_colors = Pelt.pelt_colours.copy()
                    possible_colors.remove(self.colour)
                    self.tortiecolour = choice(possible_colors)

                else:
                    # Normal generation
                    if self.tortiebase in ["singlestripe", "smoke", "single"]:
                        self.tortiepattern = choice(['tabby', 'mackerel', 'classic', 'single', 'smoke', 'agouti',
                                                     'ticked'])
                    else:
                        self.tortiepattern = random.choices([self.tortiebase, 'single'], weights=[97, 3], k=1)[0]

                    if self.colour == "WHITE":
                        possible_colors = Pelt.white_colours.copy()
                        possible_colors.remove("WHITE")
                        self.colour = choice(possible_colors)

                    # Ginger is often duplicated to increase its chances
                    if (self.colour in Pelt.black_colours) or (self.colour in Pelt.white_colours):
                        self.tortiecolour = choice((Pelt.warm_colours * 2) + Pelt.cool_colours)
                    elif self.colour in Pelt.warm_colours:
                        self.tortiecolour = choice(Pelt.warm_colours + Pelt.black_colours * 2)
                    elif self.colour in Pelt.cool_colours:
                        possible_colors = Pelt.cool_colours.copy()
                        possible_colors.remove(self.colour)
                        possible_colors.extend(Pelt.black_colours + (Pelt.warm_colours * 2))
                        self.tortiecolour = choice(possible_colors)
                    else:
                        self.tortiecolour = "ORANGE"

            else:
                self.tortiecolour = "ORANGE"
        else:
            self.tortiebase = None
            self.tortiepattern = None
            self.tortiecolour = None
            self.pattern = None

    def white_patches_inheritance(self, parents: tuple):

        par_whitepatches = set()
        par_points = []
        for p in parents:
            if p:
                if p.pelt.white_patches:
                    par_whitepatches.add(p.pelt.white_patches)
                if p.pelt.points:
                    par_points.append(p.pelt.points)

        if not parents:
            print("Error - no parents. Randomizing white patches.")
            self.randomize_white_patches()
            return

        # Direct inheritance. Will only work if at least one parent has white patches, otherwise continue on.
        if par_whitepatches and not random.randint(0, game.config["cat_generation"]["direct_inheritance"]):
            # This ensures Torties and Calicos won't get direct inheritance of incorrect white patch types
            _temp = par_whitepatches.copy()
            if self.name == "Tortie":
                for p in _temp.copy():
                    if p in Pelt.high_white + Pelt.mostly_white + ["FULLWHITE"]:
                        _temp.remove(p)
            elif self.name == "Calico":
                for p in _temp.copy():
                    if p in Pelt.little_white + Pelt.mid_white:
                        _temp.remove(p)

            # Only proceed with the direct inheritance if there are white patches that match the pelt.
            if _temp:
                self.white_patches = choice(list(_temp))

                # Direct inheritance also effect the point marking.
                if par_points and self.name != "Tortie":
                    self.points = choice(par_points)
                else:
                    self.points = None

                return

        # dealing with points
        if par_points:
            chance = 10 - len(par_points)
        else:
            chance = 40
        # Chance of point is 1 / chance.
        if self.name != "Tortie" and not int(random.random() * chance):
            self.points = choice(Pelt.point_markings)
        else:
            self.points = None

        white_list = [Pelt.little_white, Pelt.mid_white, Pelt.high_white, Pelt.mostly_white, ['FULLWHITE']]

        weights = [0, 0, 0, 0, 0]  # Same order as white_list
        for p_ in par_whitepatches:
            if p_ in Pelt.little_white:
                add_weights = (40, 20, 15, 5, 0)
            elif p_ in Pelt.mid_white:
                add_weights = (10, 40, 15, 10, 0)
            elif p_ in Pelt.high_white:
                add_weights = (15, 20, 40, 10, 1)
            elif p_ in Pelt.mostly_white:
                add_weights = (5, 15, 20, 40, 5)
            elif p_ == "FULLWHITE":
                add_weights = (0, 5, 15, 40, 10)
            else:
                add_weights = (0, 0, 0, 0, 0)

            for x in range(0, len(weights)):
                weights[x] += add_weights[x]

        # If all the weights are still 0, that means none of the parents have white patches.
        if not any(weights):
            if not all(parents):  # If any of the parents are None (unknown), use the following distribution:
                weights = [20, 10, 10, 5, 0]
            else:
                # Otherwise, all parents are known and don't have any white patches. Focus distribution on little_white.
                weights = [50, 5, 0, 0, 0]

        # Adjust weights for torties, since they can't have anything greater than mid_white:
        if self.name == "Tortie":
            weights = weights[:2] + [0, 0, 0]
            # Another check to make sure not all the values are zero. This should never happen, but better
            # safe than sorry.
            if not any(weights):
                weights = [2, 1, 0, 0, 0]
        elif self.name == "Calico":
            weights = [0, 0, 0] + weights[3:]
            # Another check to make sure not all the values are zero. This should never happen, but better
            # safe than sorry.
            if not any(weights):
                weights = [2, 1, 0, 0, 0]

        chosen_white_patches = choice(
            random.choices(white_list, weights=weights, k=1)[0]
        )

        self.white_patches = chosen_white_patches
        if self.points and self.white_patches in [Pelt.high_white, Pelt.mostly_white, 'FULLWHITE']:
            self.points = None

    def randomize_white_patches(self):

        # Points determination. Tortie can't be pointed
        if self.name != "Tortie" and not random.getrandbits(game.config["cat_generation"]["random_point_chance"]):
            # Cat has colorpoint!
            self.points = choice(Pelt.point_markings)
        else:
            self.points = None

        # Adjust weights for torties, since they can't have anything greater than mid_white:
        if self.name == "Tortie":
            weights = (2, 1, 0, 0, 0)
        elif self.name == "Calico":
            weights = (0, 0, 20, 15, 1)
        else:
            weights = (10, 10, 10, 10, 1)

        white_list = [Pelt.little_white, Pelt.mid_white, Pelt.high_white, Pelt.mostly_white, ['FULLWHITE']]
        chosen_white_patches = choice(
            random.choices(white_list, weights=weights, k=1)[0]
        )

        self.white_patches = chosen_white_patches
        if self.points and self.white_patches in [Pelt.high_white, Pelt.mostly_white, 'FULLWHITE']:
            self.points = None

    def init_white_patches(self, pelt_white, parents: tuple):
        # Vit can roll for anyone, not just cats who rolled to have white in their pelt. 
        par_vit = []
        for p in parents:
            if p:
                if p.pelt.vitiligo:
                    par_vit.append(p.pelt.vitiligo)

        vit_chance = max(game.config["cat_generation"]["vit_chance"] - len(par_vit), 0)
        if not random.getrandbits(vit_chance):
            self.vitiligo = choice(Pelt.vit)

        # If the cat was rolled previously to have white patches, then determine the patch they will have
        # these functions also handle points. 
        if pelt_white:
            if parents:
                self.white_patches_inheritance(parents)
            else:
                self.randomize_white_patches()
        else:
            self.white_patches = None
            self.points = None

    def init_tint(self):
        """Sets tint for pelt and white patches"""

        # PELT TINT
        # Basic tints as possible for all colors.
        base_tints = sprites.cat_tints["possible_tints"]["basic"]
        if self.colour in sprites.cat_tints["colour_groups"]:
            color_group = sprites.cat_tints["colour_groups"].get(self.colour, "warm")
            color_tints = sprites.cat_tints["possible_tints"][color_group]
        else:
            color_tints = []

        if base_tints or color_tints:
            self.tint = choice(base_tints + color_tints)
        else:
            self.tint = "none"

        # WHITE PATCHES TINT
        if self.white_patches or self.points:
            # Now for white patches
            base_tints = sprites.white_patches_tints["possible_tints"]["basic"]
            if self.colour in sprites.cat_tints["colour_groups"]:
                color_group = sprites.white_patches_tints["colour_groups"].get(self.colour, "white")
                color_tints = sprites.white_patches_tints["possible_tints"][color_group]
            else:
                color_tints = []

            if base_tints or color_tints:
                self.white_patches_tint = choice(base_tints + color_tints)
            else:
                self.white_patches_tint = "none"
        else:
            self.white_patches_tint = "none"

    def common_combinations(self):
        if int(game.config["cat_generation"]["common_combinations"]) and random.randint(1, game.config["cat_generation"]["common_combinations"]) == 1: #1/5 default

            if self.eye_colour in Pelt.riveye_colours:
                fishy_features = [Pelt.gills, Pelt.lizardfins, Pelt.catfishwhiskers, Pelt.dragonwhiskers, Pelt.anglerfish]
                fishy_weights = [50, 30, 15, 10, 1]
                self.skin = choice(random.choices(fishy_features, fishy_weights, k=1)[0])
                print("fish spotted!!")

            if self.eye_colour in Pelt.geckoeyes_colors:
                reptile_features = [Pelt.tailfrills, Pelt.cyanfeatures, Pelt.cyanwings, Pelt.spikes]
                reptile_weights = [50, 30, 15, 10]
                self.skin = choice(random.choices(reptile_features, reptile_weights, k=1)[0])
                self.name = "Scaled"
                print("reptile spotted!!")

            if self.skin in Pelt.centipedegrowths and self.tortiepattern == None:
                self.name = "Centipede"
                print("centipede spotted!!")

            if self.skin in Pelt.overseertenna and self.tortiepattern == None:
                self.name = "Iggy"
                print("overseer spotted!!")

            if self.skin in Pelt.manes and self.tortiepattern == None:
                self.name = "Maned"
                print("maned slugcat spotted!!")

            if self.name == "Leafy" or self.tortiebase == "Leafy" and self.tortiepattern == "Leafy":
                wing_options = [Pelt.wings, Pelt.whitefadewings, Pelt.colorwings]
                wing_weights = [50, 40, 10]
                self.skin = choice(random.choices(wing_options, wing_weights, k=1)[0])
                print("winged slugcat spotted!!")

            if self.name == "Fluffy" or self.tortiebase == "Fluffy" and self.tortiepattern == "Fluffy":
                self.skin = choice(Pelt.tongues + Pelt.claws + Pelt.whiskers)
                print("cat spotted!!")

            if self.name == "Seaslug" or self.tortiebase == "Seaslug" and self.tortiepattern == "Seaslug":
                self.skin = choice(Pelt.glowspots + Pelt.seaslugpapillae)
                print("sea slug spotted!!")

            if self.name == "Pidgeon" or self.tortiebase == "Pidgeon" and self.tortiepattern == "Pidgeon":
                self.skin = choice(Pelt.pidgeonwings)
                print("Pidgeon spotted!!")

            if self.name == "Conure" or self.tortiebase == "Conure" and self.tortiepattern == "Conure":
                self.skin = choice(Pelt.conurewings)
                print("Conure spotted!!")

            if self.name == "Lovebird" or self.tortiebase == "Lovebird" and self.tortiepattern == "Lovebird":
                self.skin = choice(Pelt.lovebirdwings)
                print("Lovebird spotted!!")

            if self.name == "Budgie" or self.tortiebase == "Budgie" and self.tortiepattern == "Budgie":
                self.skin = choice(Pelt.budgiewings)
                print("Budgie spotted!!")

            if self.name == "Plated" or self.tortiebase == "Plated" and self.tortiepattern == "Plated":
                self.skin = choice(Pelt.mechanical)
                print("Mecha scug spotted!!")
        
            if self.skin in Pelt.familiar:
                self.colour = "PURPLE"
                print("FAMILIAR??!?!?")

        if int(game.config["cat_generation"]["most_common_combinations"]) and random.randint(1, game.config["cat_generation"]["most_common_combinations"]) == 1: #1/10 default

            if self.eye_colour in Pelt.buttoneye_colours and self.tortiepattern == None:
                self.name = "Patchwork"
                print("someone got turned into a marketable plushie...")

            if self.name == "Fizzy" or self.name == "Boba" or self.name == "Amoeba" or self.name == "Seaslug":
                self.white_patches = None
                self.vitiligo = None
                self.points = None
                print("clear pelt")
                
    @property
    def white(self):
        return self.white_patches or self.points

    @white.setter
    def white(self, val):
        print("Can't set pelt.white")
        return

    @staticmethod
    def describe_appearance(cat, short=False):
        """Return a description of a cat

        :param Cat cat: The cat to describe
        :param bool short: Whether to return a heavily-truncated description, default False
        :return str: The cat's description
        """
        
        with open("sprites/dicts/descriptions.json", "f") as f:
            descriptions_dict = json.load(f)
            
        # Define look-up dictionaries
        if short:
            renamed_colors = descriptions_dict['short_renamed_colors']
        else:
            renamed_colors = descriptions_dict['renamed_colors']

        # Pelt pattern descriptions
        pattern_des = descriptions_dict['pattern_des']

        # Start with determining the base color name
        color_name = str(cat.pelt.colour).lower()
        if color_name in renamed_colors:
            color_name = renamed_colors[color_name]

        # Replace "white" with "pale" if the cat is white
        if cat.pelt.name not in ["SingleColour", "TwoColour", "Tortie", "Calico"] and color_name == "white":
            color_name = "pale"

        # Time to describe the pattern and any additional colors
        if cat.pelt.name in pattern_des:
            color_name = pattern_des[cat.pelt.name].replace("c_n", color_name)
        elif cat.pelt.name in Pelt.torties:
            # Calicos and Torties need their own desciptions
            if short:
                # If using short, don't describe the colors of calicos and torties.
                # Just call them calico, tortie, or mottled
                if cat.pelt.colour in Pelt.black_colours + Pelt.cool_colours + Pelt.white_colours and \
                        cat.pelt.tortiecolour in Pelt.black_colours + Pelt.cool_colours + Pelt.white_colours:
                    color_name = "mottled"
                else:
                    color_name = cat.pelt.name.lower()
            else:
                base = cat.pelt.tortiebase.lower()
                if base in [tabby.lower() for tabby in Pelt.tabbies] + ['bengal', 'rosette', 'speckled']:
                    base = ' tabby'  # the extra space is intentional
                else:
                    base = ''

                patches_color = cat.pelt.tortiecolour.lower()
                if patches_color in renamed_colors:
                    patches_color = renamed_colors[patches_color]
                color_name = f"{color_name}/{patches_color}"

                if cat.pelt.colour in Pelt.black_colours + Pelt.cool_colours + Pelt.white_colours and \
                        cat.pelt.tortiecolour in Pelt.black_colours + Pelt.cool_colours + Pelt.white_colours:
                    color_name = f"{color_name} mottled{base}"
                else:
                    color_name = f"{color_name} {cat.pelt.name.lower()}{base}"
                    
        # Grabs tint name for more description
        white_patches_tint_name = str(cat.pelt.white_patches_tint).lower() 
        
        if cat.pelt.white_patches:
            if cat.pelt.white_patches == "FULLWHITE":
                # If the cat is fullwhite, discard all other information. They are just whatever white patch tint color they have
                color_name = f"{white_patches_tint_name}"
            if cat.pelt.white_patches in Pelt.mostly_white and cat.pelt.name != "Calico":
                color_name = f"{white_patches_tint_name} and {color_name}"
            elif cat.pelt.name != "Calico":
                color_name = f"{color_name} and {white_patches_tint_name}"

        if cat.pelt.points:
            color_name = f"{color_name} point"
            if "scarlet point" in color_name:
                color_name.replace("scarlet point", "flame point")

        # Remove none from white patch description
        if "none" in color_name:
            color_name = color_name.replace("none", "white")
        
        # Remove same color descriptors
        if "white and white" in color_name:
            color_name = color_name.replace("white and white", "white")

        if "black and black" in color_name:
            color_name = color_name.replace("black and black", "black")

        if "cream and cream" in color_name:
            color_name = color_name.replace("cream and cream", "cream")

        if "purple and purple" in color_name:
            color_name = color_name.replace("purple and purple", "purple")

        if "mint and mint" in color_name:
            color_name = color_name.replace("mint and mint", "mint")

        # Now it's time for gender
        if cat.genderalign in ["female", "trans female"]:
            color_name = f"{color_name} female"
        elif cat.genderalign in ["male", "trans male"]:
            color_name = f"{color_name} male"
        else:
            color_name = f"{color_name} slugcat"

        # Here is the place where we can add some additional details about the cat, for the full non-short one
        # These include notable missing limbs, vitiligo, long-furred-ness, features, and 3 or more scars
        if not short:
            feature_details = descriptions_dict['feature_details']

            scar_details = descriptions_dict['scar_details']

            additional_details = []
            if cat.pelt.vitiligo:
                additional_details.append("vitiligo")
            for scar in cat.pelt.scars:
                if scar in scar_details and scar_details[scar] not in additional_details:
                    additional_details.append(scar_details[scar])

            if len(additional_details) > 2:
                color_name = f"{color_name} with {', '.join(additional_details[:-1])}, and {additional_details[-1]}"
            elif len(additional_details) == 2:
                color_name = f"{color_name} with {' and '.join(additional_details)}"
            elif additional_details:
                color_name = f"{color_name} with {additional_details[0]}"

            if len(cat.pelt.scars) >= 3:
                color_name = f"scarred {color_name}"
            if cat.pelt.length == "long":
                color_name = f"bulky {color_name}"

        return color_name

    def get_sprites_name(self):
        return Pelt.sprites_names[self.name]
