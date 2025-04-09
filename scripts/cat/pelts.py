import random
from random import choice
from re import sub

from scripts.cat.sprites import sprites
from scripts.game_structure.game_essentials import game


class Pelt:
    sprites_names = {
        "SingleColour": 'single',
        'TwoColour': 'single',
        'Tabby': 'tabby',
        'Marbled': 'marbled',
        'Rosette': 'rosette',
        'Smoke': 'smoke',
        'Ticked': 'ticked',
        'Speckled': 'speckled',
        'Bengal': 'bengal',
        'Mackerel': 'mackerel',
        'Classic': 'classic',
        'Sokoke': 'sokoke',
        'Agouti': 'agouti',
        'Singlestripe': 'singlestripe',
        'Masked': 'masked',
        'Gravel': 'gravel',
        'Collared': 'collared',
        'Slimemold': 'slimemold',
        'Cyanlizard': 'cyanlizard',
        'Vulture': 'vulture',
        'Banana': 'banana',
        'Centipede': 'centipede',
        'Con': 'con',
        'Lizard': 'lizard',
        'Lantern': 'lantern',
        'Leviathan': 'leviathan',
        'Fluffy': 'fluffy',
        'Amoeba': 'amoeba',
        'Seaslug': 'seaslug',
        'Yeek': 'yeek',
        'Rusted': 'rusted',
        'Envoy': 'envoy',
        'Drizzle': 'drizzle',
        'Solace': 'solace',
        'Leafy': 'leafy',
        'Scaled': 'scaled',
        'Dragonfruit': 'dragonfruit',
        'Necklace': 'necklace',
        'Dreamer': 'dreamer',
        'Duskdawn': 'duskdawn',
        'Seer': 'seer',
        'Rotten': 'rotten',
        'Fire': 'fire',
        'Countershaded': 'countershaded',
        'Sunset': 'sunset',
        'Oldgrowth': 'oldgrowth',
        'Sparklecat': 'sparklecat',
        'Wolf': 'wolf',
        'Cherry': 'cherry',
        'Hypnotist': 'hypnotist',
        'Ringed': 'ringed',
        'Skinny': 'skinny',
        'Sparse': 'sparse',
        'Impish': 'impish',
        'Sporty': 'sporty',
        'Fizzy': 'fizzy',
        'Skeleton': 'skeleton',
        'Shred': 'shred',
        'Glowing': 'glowing',
        'Mold': 'mold',
        'Swing': 'swing',
        'Lovebird': 'lovebird',
        'Budgie': 'budgie',
        'Amazon': 'amazon',
        'Apple': 'apple',
        'Boba': 'boba',
        'Glitter': 'glitter',
        'Ice': 'ice',
        'Iggy': 'iggy',
        'Maned': 'maned',
        'Patchwork': 'patchwork',
        'Robot': 'robot',
        'Sunken': 'sunken',
        'Tomo': 'tomo',
        'Whale': 'whale',
        'Pidgeon': 'pidgeon',
        'Tortie': None,
        'Calico': None,
    }

    # ATTRIBUTES, including non-pelt related
    pelt_colours = [
        'WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK', 'CREAM', 'PALEGINGER',
        'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA', 'LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN',
        'CHOCOLATE'
    ]
    pelt_c_no_white = [
        'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK', 'CREAM', 'PALEGINGER',
        'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA', 'LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN',
        'CHOCOLATE'
    ]
    pelt_c_no_bw = [
        'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'CREAM', 'PALEGINGER',
        'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA', 'LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN',
        'CHOCOLATE'
    ]

    tortiepatterns = ['ONE', 'TWO', 'THREE', 'FOUR', 'REDTAIL', 'DELILAH', 'MINIMALONE', 'MINIMALTWO', 'MINIMALTHREE',
                      'MINIMALFOUR', 'HALF',
                      'OREO', 'SWOOP', 'MOTTLED', 'SIDEMASK', 'EYEDOT', 'BANDANA', 'PACMAN', 'STREAMSTRIKE', 'ORIOLE',
                      'CHIMERA', 'DAUB', 'EMBER', 'BLANKET',
                      'ROBIN', 'BRINDLE', 'PAIGE', 'ROSETAIL', 'SAFI', 'SMUDGED', 'DAPPLENIGHT', 'STREAK', 'MASK',
                      'CHEST', 'ARMTAIL', 'SMOKE', 'GRUMPYFACE',
                      'BRIE', 'BELOVED', 'BODY', 'SHILOH', 'FRECKLED', 'HEARTBEAT', 'SPECKLES', 'TIGER']
    tortiebases = ['single', 'tabby', 'bengal', 'marbled', 'ticked', 'smoke', 'rosette', 'speckled', 'mackerel',
                'classic', 'sokoke', 'agouti', 'singlestripe', 'masked', 'gravel', 'collared', 'slimemold',
                'cyanlizard', 'vulture', 'banana', 'centipede', 'con', 'lizard', 'lantern', 'leviathan',
                'fluffy', 'amoeba', 'yeek', 'rusted', 'envoy', 'drizzle', 'solace', 'leafy', 'scaled', 'dragonfruit', 
                'necklace', 'dreamer', 'duskdawn', 'seer', 'rotten', 'fire', 'countershaded', 'sunset', 'oldgrowth', 
                'sparklecat', 'wolf', 'cherry', 'hypnotist', 'ringed', 'skinny', 'sparse', 'impish', 'sporty', 
                'skeleton', 'shred', 'glowing', 'mold', 'swing', 'lovebird', 'budgie', 'amazon', 'apple', 'boba',
                'glitter', 'ice', 'iggy', 'maned', 'patchwork', 'robot', 'sunken', 'tomo', 'whale', 'pidgeon']

    pelt_length = ["short", "medium", "long"]
    eye_colours = ['YELLOW', 'AMBER', 'HAZEL', 'PALEGREEN', 'GREEN', 'BLUE', 'DARKBLUE', 'GREY', 'CYAN', 'EMERALD', 'PALEBLUE', 
        'PALEYELLOW', 'GOLD', 'HEATHERBLUE', 'COPPER', 'SAGE', 'COBALT', 'SUNLITICE', 'GREENYELLOW', 'BRONZE', 'SILVER', 'RED', 'PURPLE', 'MAUVE',
        'ELECTRICBLUE', 'VIOLET', 'PINK', 'SNOW', 'ORANGE', 'CREAM', 'SEAFOAM', 'CRIMSON', 'NAVY', 'VOIDGOLD', 'COOLBROWN', 'PLUM',
        'INDIGO', 'LILAC', 
        'ALBA', 'ALBINO', 'ANGEL', 'APPLE', 'AQUA', 'ARID', 'BANANA', 'BLOOD', 'CARNI', 'CHAIN', 
        'CREAMY', 'DAWN', 'ESES', 'EXILE', 'FAE', 'FALLSTAR', 'FIELD', 'FOAM', 'HOT', 'IRID', 
        'KARMA', 'KIND', 'MARTI', 'MEISTALT', 'MEISTER', 'MELON', 'MESS', 'MHUNT', 'MINT', 'MINV', 
        'MOON', 'MRIV', 'PEACH', 'PEBB', 'PELA', 'PEPPER', 'RETRO', 'RUNT', 'RUST', 'SIG', 
        'SIXER', 'SPLIT', 'SUN', 'SWEET', 'TIDE', 'VIVID', 'WAVE', 'WINKS', 'ZENI', 'BEAST',
        'BROWNTBOI', 'ORANGETBOI', 'BREDTBOI', 'REDTBOI'
        ]
    yellow_eyes = ['YELLOW', 'AMBER', 'PALEYELLOW', 'GOLD', 'COPPER', 'GREENYELLOW', 'BRONZE', 'SILVER', 'ORANGE', 'CREAM', 'VOIDGOLD',
                   'BROWNTBOI', 'ORANGETBOI']
    blue_eyes = ['BLUE', 'DARKBLUE', 'CYAN', 'PALEBLUE', 'HEATHERBLUE', 'COBALT', 'SUNLITICE', 'GREY', 'ELECTRICBLUE', 'SNOW', 'INDIGO',
                 'ANGEL']
    green_eyes = ['PALEGREEN', 'GREEN', 'EMERALD', 'SAGE', 'HAZEL', 'SEAFOAM', 'NAVY',
                  'MESS']
    red_eyes = ['RED', 'PURPLE', 'MAUVE', 'VIOLET', 'PINK', 'CRIMSON', 'COOLBROWN', 'PLUM', 'LILAC', 
                'MINT', 'PEACH', 'ALBINO', 'DAWN', 'BREDTBOI', 'REDTBOI']
    
    riveye_colours = ['RIVYELLOW', 'RIVAMBER', 'RIVHAZEL', 'RIVPALEGREEN', 'RIVGREEN', 'RIVBLUE', 'RIVDARKBLUE', 'RIVGREY', 'RIVCYAN', 'RIVEMERALD', 'RIVPALEBLUE', 
               'RIVPALEYELLOW', 'RIVGOLD', 'RIVHEATHERBLUE', 'RIVCOPPER', 'RIVSAGE', 'RIVCOBALT', 'RIVSUNLITICE', 'RIVGREENYELLOW', 'RIVBRONZE', 'RIVSILVER']
    yellow_riv_eyes = ['RIVYELLOW', 'RIVAMBER', 'RIVPALEYELLOW', 'RIVGOLD', 'RIVCOPPER', 'RIVGREENYELLOW', 'RIVBRONZE', 'RIVSILVER']
    blue_riv_eyes = ['RIVBLUE', 'RIVDARKBLUE', 'RIVCYAN', 'RIVPALEBLUE', 'RIVHEATHERBLUE', 'RIVCOBALT', 'RIVSUNLITICE']
    green_riv_eyes = ['RIVPALEGREEN', 'RIVGREEN', 'RIVEMERALD', 'RIVSAGE']
    
    buttoneye_colours = ['BUTTONYELLOW', 'BUTTONAMBER', 'BUTTONHAZEL', 'BUTTONPALEGREEN', 'BUTTONGREEN', 'BUTTONBLUE', 
                'BUTTONDARKBLUE', 'BUTTONGREY', 'BUTTONCYAN', 'BUTTONEMERALD', 'BUTTONHEATHERBLUE', 'BUTTONSUNLITICE', 
                'BUTTONCOPPER', 'BUTTONSAGE', 'BUTTONCOBALT', 'BUTTONPALEBLUE', 'BUTTONBRONZE', 'BUTTONSILVER', 'BUTTONPALEYELLOW',
                'BUTTONGOLD', 'BUTTONGREENYELLOW', 'BUTTONIRED', 'BUTTONPURPLE', 'BUTTONMAUVE', 'BUTTONINDIGO', 'BUTTONLILAC']
    yellow_button_eyes = ['BUTTONYELLOW', 'BUTTONAMBER', 'BUTTONPALEYELLOW', 'BUTTONGOLD', 'BUTTONCOPPER', 'BUTTONGREENYELLOW', 'BUTTONBRONZE', 'BUTTONSILVER']
    blue_button_eyes = ['BUTTONBLUE', 'BUTTONDARKBLUE', 'BUTTONCYAN', 'BUTTONPALEBLUE', 'BUTTONHEATHERBLUE', 'BUTTONCOBALT', 'BUTTONSUNLITICE', 'BUTTONINDIGO']
    green_button_eyes = ['BUTTONPALEGREEN', 'BUTTONGREEN', 'BUTTONEMERALD', 'BUTTONSAGE']
    red_button_eyes = ['BUTTONIRED', 'BUTTONPURPLE', 'BUTTONMAUVE', 'BUTTONLILAC']
    
    pupil_eyes = ['ALBA', 'BANANA', 'CREAMY', 'KARMA', 'MHUNT', 'PEPPER', 'SPLIT', 'WINKS', 'ZENI', 'BEAST',
                'CARNI', 'CHAIN', 'FOAM', 'MEISTALT', 'MELON', 'MINV', 'MOON', 'MRIV', 'PEBB', 'RUST', 'SIG', 
                'TIDE', 'VIVID', 'WAVE', 'APPLE', 'AQUA', 'FAE', 'FIELD', 'IRID', 'RUNT', 
                'ARID', 'BLOOD', 'ESES', 'EXILE', 'FALLSTAR', 'HOT', 'KIND', 'MARTI', 'MEISTER', 
                'PELA', 'RETRO', 'SIXER', 'SUN', 'SWEET']
    yellow_pupil_eyes = ['ALBA', 'BANANA', 'CREAMY', 'KARMA', 'MHUNT', 'PEPPER', 'SPLIT', 'WINKS', 'ZENI', 'BEAST']
    blue_pupil_eyes = ['CARNI', 'CHAIN', 'FOAM', 'MEISTALT', 'MELON', 'MINV', 'MOON', 'MRIV', 'PEBB', 'RUST', 'SIG', 
                 'TIDE', 'VIVID', 'WAVE']
    green_pupil_eyes = ['APPLE', 'AQUA', 'FAE', 'FIELD', 'IRID', 'RUNT']
    red_pupil_eyes = ['ARID', 'BLOOD', 'ESES', 'EXILE', 'FALLSTAR', 'HOT', 'KIND', 'MARTI', 'MEISTER', 
                'PELA', 'RETRO', 'SIXER', 'SUN', 'SWEET']

    multi_eyes = ['MULTIYELLOW', 'MULTIAMBER', 'MULTIHAZEL', 'MULTIPALEGREEN', 'MULTIGREEN', 'MULTIBLUE', 
                'MULTIDARKBLUE', 'MULTIGREY', 'MULTICYAN', 'MULTIEMERALD', 'MULTIHEATHERBLUE', 'MULTISUNLITICE',
                'MULTICOPPER', 'MULTISAGE', 'MULTICOBALT', 'MULTIPALEBLUE', 'MULTIBRONZE', 'MULTISILVER',
                'MULTIPALEYELLOW', 'MULTIGOLD', 'MULTIGREENYELLOW', 'MULTIRED', 'MULTIPURPLE', 'MULTIMAUVE',
                'MULTIELECTRICBLUE', 'MULTIVIOLET', 'MULTIPINK', 'MULTISNOW',
                'MULTIORANGE', 'MULTICREAM', 'MULTISEAFOAM', 'MULTICRIMSON', 'MULTINAVY',
                'MULTIVOIDGOLD', 'MULTICOOLBROWN', 'MULTIPLUM', 'MULTIINDIGO', 'MULTILILAC',
                'MULTIALBA', 'MULTIALBINO', 'MULTIANGEL', 'MULTIAPPLE', 'MULTIAQUA', 
                'MULTIARID', 'MULTIBANANA', 'MULTIBLOOD', 'MULTICARNI', 'MULTICHAIN',
                'MULTICREAMY', 'MULTIDAWN', 'MULTIESES', 'MULTIEXILE', 'MULTIFAE', 
                'MULTIFALLSTAR', 'MULTIFIELD', 'MULTIFOAM', 'MULTIHOT', 'MULTIIRID',
                'MULTIKARMA', 'MULTIKIND', 'MULTIMARTI', 'MULTIMEISTALT', 'MULTIMEISTER', 
                'MULTIMELON', 'MULTIMESS', 'MULTIMHUNT', 'MULTIMINT', 'MULTIMINV',
                'MULTIMOON', 'MULTIMRIV', 'MULTIPEACH', 'MULTIPEBB', 'MULTIPELA', 
                'MULTIPEPPER', 'MULTIRETRO', 'MULTIRUNT', 'MULTIRUST', 'MULTISIG',
                'MULTISIXER', 'MULTISPLIT', 'MULTISUN', 'MULTISWEET', 'MULTITIDE', 
                'MULTIVIVID', 'MULTIWAVE', 'MULTIWINKS', 'MULTIZENI', 'MULTIBEAST',
                'MULTIBROWNTBOI', 'MULTIORANGETBOI', 'MULTIBREDTBOI', 'MULTIREDTBOI'
                ]

    # bite scars by @wood pank on discord

    # scars from other cats, other animals
    scars1 = ["ONE", "TWO", "THREE", "FOUR", "TAILSCAR", "SNOUT", "CHEEK", "SIDE", "THROAT", "TAILBASE", "BELLY",
              "LEGBITE", "NECKBITE", "FACE", "MANLEG", "BRIGHTHEART", "MANTAIL", "BRIDGE", "RIGHTBLIND", "LEFTBLIND",
              "BOTHBLIND", "BEAKCHEEK", "BEAKLOWER", "CATBITE", "RATBITE", "QUILLCHUNK", "QUILLSCRATCH", "HINDLEG",
              "BACK", "QUILLSIDE", "SCRATCHSIDE", "BEAKSIDE", "CATBITETWO", "LABRATFACE", "LABRATCHEST", 
              "NEUTRINO", "MANGLEDARM", "DOUBLEBITE", "DANGEROUS", "X-FACE", "VULTURESHOULDER", "CHEEKCUT", "MIROSNOM",
              "SPEARWOUND"]

    # missing parts
    scars2 = ["LEFTEAR", "RIGHTEAR", "NOTAIL", "HALFTAIL", "NOPAW", "NOLEFTEAR", "NORIGHTEAR", "NOEAR"]

    # "special" scars that could only happen in a special event
    scars3 = ["SNAKE", "TOETRAP", "BURNPAWS", "BURNTAIL", "BURNBELLY", "BURNRUMP", "FROSTFACE", "FROSTTAIL",
              "FROSTMITT", "FROSTSOCK", "TOE", "SNAKETWO", "ROTMARKED", "ROTRIDDEN", "TOPSURGERY", "CUTOPEN", 
              "VIVISECTION", "LABRATLIMBS", "HALFFACELEFT", "FULLBODYBURNS", "BESIEGED", "HALFFACERIGHT", 
              "STARBURN", "ARMBURN", "ENVOYCHEST", "EXTRACTIONTWO", "RESTITCHEDUPPER", 
              "RESTITCHEDLOWER", "STITCHEDHEAD", "MESSIAH", "SMOKINGFACE", "BURNTLEG", "BURNTARM", 
              "ARTIRIGHT", "ARTIGLOWRIGHT", "ARTILEFT", "ARTIGLOWLEFT", "PATCHWORK"]

    # make sure to add plural and singular forms of new accs to acc_display.json so that they will display nicely
    plant_accessories = ["MAPLE LEAF", "HOLLY", "BLUE BERRIES", "FORGET ME NOTS", "RYE STALK", "LAUREL",
                         "BLUEBELLS", "NETTLE", "POPPY", "LAVENDER", "HERBS", "PETALS", "DRY HERBS",
                         "OAK LEAVES", "SCUGMINT", "MAPLE SEED", "JUNIPER", "SAKURA"]

    wild_accessories = ["RED FEATHERS", "BLUE FEATHERS", "JAY FEATHERS", "MOTH WINGS", "CICADA WINGS"]
    tail_accessories = ["RED FEATHERS", "BLUE FEATHERS", "JAY FEATHERS"]
    collars = [
        "CRIMSON", "BLUE", "YELLOW", "CYAN", "RED", "LIME", "GREEN", "RAINBOW",
        "BLACK", "SPIKES", "WHITE", "PINK", "PURPLE", "MULTI", "INDIGO", "CRIMSONBELL", "BLUEBELL",
        "YELLOWBELL", "CYANBELL", "REDBELL", "LIMEBELL", "GREENBELL",
        "RAINBOWBELL", "BLACKBELL", "SPIKESBELL", "WHITEBELL", "PINKBELL", "PURPLEBELL",
        "MULTIBELL", "INDIGOBELL", "CRIMSONBOW", "BLUEBOW", "YELLOWBOW", "CYANBOW", "REDBOW",
        "LIMEBOW", "GREENBOW", "RAINBOWBOW", "BLACKBOW", "SPIKESBOW", "WHITEBOW", "PINKBOW",
        "PURPLEBOW", "MULTIBOW", "INDIGOBOW", "CRIMSONNYLON", "BLUENYLON", "YELLOWNYLON", "CYANNYLON",
        "REDNYLON", "LIMENYLON", "GREENNYLON", "RAINBOWNYLON",
        "BLACKNYLON", "SPIKESNYLON", "WHITENYLON", "PINKNYLON", "PURPLENYLON", "MULTINYLON", "INDIGONYLON",
        "CRIMSONDRONE", "BLUEDRONE", "YELLOWDRONE", "CYANDRONE", "REDDRONE", "LIMEDRONE", "GREENDRONE",
        "RAINBOWDRONE", "BLACKDRONE", "SPIKESDRONE", "WHITEDRONE", "PINKDRONE", "PURPLEDRONE", "MULTIDRONE", "INDIGODRONE"]
    #Lex's RW Lizards
    lizards = [
        "BLUESKY", "BLUESEA", "PINKMAGENTA", "PINKPURPLE", "GREENEMERALD", "GREENLIME", "WHITEHIDDEN", "WHITEREVEALED", 
        "BLACKNEUTRAL", "BLACKALERT", "YELLOWORANGE", "YELLOWLEMON", "REDTOMATO", "CYANBLUE", "CYANGREEN", 
        "ALBISALAFUSHIA", "ALBISALARED", "MELASALARED", "MELASALAFUSHIA", "MELASALAPURPLE"
    ]
    #sey's accessories
    muddypaws = [
        "MUDDYPAWS"
    ]
    insectwings = [
        "DEATHSHEAD", "BLUEBORDERED", "BLOODVEIN", "LARGEEMERALD", "CINNABAR", "LUNA", "ROSYMAPLE",
        "ATLAS", "HERCULES", "SUNSET", "PURPLEEMPEROR", "WHITEADMIRAL", "SWALLOWTAIL"
    ]
    #other
    herbs2 = [
        "SPEAR", "PEARLEAR", "KARMAFLOWER", "LILCENTI", "PEARLNECK", "REDBATNIP", 
        "LILFLY", "BATNIP", "FLASHFRUIT", "REDFLASHFRUIT", "GREENKELP", "REDKELP", 
        "VULTMASK", "KINGMASK", "SCAVMASK", "TREESEED", "GLOWSTONE", "BROWNKELP", 
        "LILBEETLE", "EXPLOSPEAR", "GREENDRAGFLY", "BLUEDRAGFLY", "ELESPEAR"
    ]
    buddies = [
        "MOUSEBLUE", "MOUSEYEL", "MOUSEPINK", "MOUSERED", "YEEKRED", "YEEKBLUE",
        "VULTGRUB", "GRAPPLE", "SNAILGREEN", "SNAILBLUE", "SNAILRED", "SNAILPURPLE",
        "NOODLERED", "NOODLEPURPLE", "NOODLEGREY", "NOODLEBLUE", "NOODLEWHITE", "NOODLEPINK",
        "IGGYYELLOW", "IGGYPURPLE", "IGGYWHITE", "IGGYGREEN", "IGGYRED", "IGGYBLUE",
        "SQUIDBLACK", "SQUIDWHITE", "BUBBLE", "WORMGRASSPOT", "POLEPLANTPOT"
    ]
    newaccs = [
        "BATFLY", "BLUEFRUIT", "EMPTYBAG", "HERBSBAG", "INVEGG", "VOIDSPAWN",
        "REDARMOR", "OVERSEEREYE", "SPIDEREAR", "NEURONBLUE", "NEURONRED", "NEURONGREEN",
        "NEURONWHITE", "KARMAONE", "KARMATWO", "KARMATHREE", "KARMAFOUR", "SCROLL",
        "NECKLACESILVER", "NECKLACEGOLD", "TAILWRAP", "RAINCOAT", "LACESCARF", "TOLLMASK",
        "FLOWEREDMOSS", "MOSS", "MUSHROOMS", "MUSHROOMHAT", "GRENADE", "SANTAHAT",
        "EYEPATCH", 'INVMOUTH', "MOUSEYELPLUSH", "MOUSEREDPLUSH", "MOUSEBLUEPLUSH", "MOUSEPINKPLUSH"
    ]
    newaccs2 = [
        "GLITCHING", "ROBOTARM", "ROBOTLEG", "SCRAPARMOR", "BLINDFOLD",
        "BRONZEPOCKETWATCH", "SILVERPOCKETWATCH", "GOLDPOCKETWATCH", "MURDERPAINT", "BOGMOSSBLUE",
        "BOGMOSSGREEN", "BOGMOSSLIME",
        "ORANGEPLANTPELT", "LIMEPLANTPELT", "GREENPLANTPELT", "YELLOWPLANTPELT", "BLUEPLANTPELT"
    ]
    bodypaint = [
        "REDPAINT", "PINKPAINT", "VOIDPAINT", "YELLOWPAINT", "GREENPAINT", "PALEPAINT",
        "CYANPAINT", "BLUEPAINT", "PURPLEPAINT", "MAGENTAPAINT", "BLACKPAINT", "WHITEPAINT"
    ]
    implant = [
        "IMPLANTWHITE", "IMPLANTPURPLE", "IMPLANTGREEN", "IMPLANTYELLOW", "IMPLANTBLUE",
        "EYEIMPLANTWHITE", "EYEIMPLANTRED", "EYEIMPLANTGREEN", "EYEIMPLANTYELLOW", "EYEIMPLANTBLUE",
        "GLOWWHITE", "GLOWPURPLE", "GLOWGREEN", "GLOWYELLOW", "GLOWBLUE",
        "CELLIMPLANT"
    ]
    magic = [
        "ORANGEFIRE", "GREENFIRE", "BLUEFIRE", "YELLOWFIRE", "WHITEFIRE", "PINKFIRE", "REDFIRE",
        "GREENRING", "CYANRING", "SILVERRING", "WHITERING", "YELLOWRING", "VOIDRING", "GOLDRING",
        "PETPEBBLE", "PETCLAY", "PETLAPIS", "PETAMETHYST", "PETJADE", "PETGRANITE", "PETSANDSTONE"
    ]
    necklaces = [
        "NECKLACEWHITE", "NECKLACEPINK", "NECKLACEPURPLE", "NECKLACEYELLOW", "NECKLACECYAN",
        "NECKLACEGREEN", "NECKLACERED", "NECKLACEORANGE", "NECKLACEBLUE", "NECKLACEBLACK"
    ]
    drapery = [
        "DRAPERYWHITE", "DRAPERYORANGE", "DRAPERYTAN", "DRAPERYPALEYELLOW", "DRAPERYYELLOW", "DRAPERYMINT", "DRAPERYGREEN", "DRAPERYLIGHTAQUA",
        "DRAPERYAQUA", "DRAPERYCYAN", "DRAPERYLIGHTGRAY", "DRAPERYPURPLE", "DRAPERYLIGHTINDIGO", "DRAPERYBLUE", "DRAPERYLAVENDER", "DRAPERYLIGHTPINK", "DRAPERYPINK",
        "DRAPERYHOTPINK", "DRAPERYGRAY", "DRAPERYDARKGRAY", "DRAPERYLIGHTRED", "DRAPERYRED", "DRAPERYPEACH", "DRAPERYLIGHTORANGE"
    ]
    pridedrapery = [
        "ORIGINALGAYDRAPERY", "TRANSDRAPERY", "GENDERQUEERDRAPERY", "AGENDERDRAPERY", "NONBINARYDRAPERY", "POLYAMDRAPERY", "GENDERFLUIDDRAPERY",
        "GENDERFLUXDRAPERY", "GAYDRAPERY", "OMNISEXUALDRAPERY", "OBJECTUMDRAPERY", "RAINBOWDRAPERY", "PHILIDRAPERY", "BISEXUALDRAPERY",
        "PANSEXUALDRAPERY", "POLYSEXUALDRAPERY", "ASEXUALDRAPERY", "LESBIANDRAPERY", "INTERSEXDRAPERY", "AROACEDRAPERY", "DEMIGIRLDRAPERY",
        "DEMIBOYDRAPERY", "DEMIGENDERDRAPERY", "DEMIFLUIDDRAPERY", "DEMIFLUXDRAPERY", "ABRODRAPERY", "ARODRAPERY", "DEMISEXDRAPERY",
        "DEMIRODRAPERY", "ACHILLEANDRAPERY", "SAPPHICDRAPERY", "DIAMORICDRAPERY", "UNLABELEDDRAPERY", "TRANSFEMDRAPERY", "TRANSMASCDRAPERY",
        "BIGENDERDRAPERY", "MULTISEXDRAPERY", "ACESPECDRAPERY", "AROSPECDRAPERY"
    ]
    eyepatches = [
        "EYEPATCHWHITE", "EYEPATCHGREEN", "EYEPATCHAQUA", "EYEPATCHTURQUOISE", "EYEPATCHCYAN", "EYEPATCHBLUE", "EYEPATCHINDIGO",
        "EYEPATCHPURPLE", "EYEPATCHMAGENTA", "EYEPATCHPINK", "EYEPATCHROSE", "EYEPATCHLIGHTGRAY", "EYEPATCHDARKGRAY", "EYEPATCHBLACK",
        "EYEPATCHRED", "EYEPATCHORANGE", "EYEPATCHAMBER", "EYEPATCHYELLOW", "EYEPATCHLIME"
    ]
    #Lars's accessories 
    larsaccs = [
        "ALLSEEINGGOLD", "ALLSEEINGSILVER", "BESIEGEDMASKOG", "BESIEGEDMASKBLUE", "BESIEGEDMASKCYAN",
        "BESIEGEDMASKGRAY", "BESIEGEDMASKGREEN", "BESIEGEDMASKINDIGO", "BESIEGEDMASKORANGE", "BESIEGEDMASKPINK",
        "BESIEGEDMASKPURPLE", "BESIEGEDMASKRED", "BESIEGEDMASKROSE", "BESIEGEDMASKAQUA", "BESIEGEDMASKYELLOW",
        "HANDPEARLBLANK", "HANDPEARLBLUE", "HANDPEARLGREEN", "HANDPEARLORANGE", "HANDPEARLPURPLE",
        "HANDPEARLRED", "HANDPEARLYELLOW", "PEARLDRAPERY", "STRAIGHTGOLD", "STRAIGHTSILVER"
    ]
    #Harley's accessories, could be merged with other files
    harleyaccs = [
        "FALLENSTARMASK", "TORNCLOAKFALL", "FALLENSTARPAWS", "TORNCLOAKWINTER",
        "TORNCLOAKNIGHT", "TORNCLOAKSHADOW", "TORNCLOAKSILVER", "FAUXMANE"
    ]
    featherboas = [
        "DPINKFEATHERBOA", "DREDFEATHERBOA", "DGREENFEATHERBOA", "DBLUEFEATHERBOA", "DGREENERFEATHERBOA",
        "DORANGEFEATHERBOA", "LWHITEFEATHERBOA", "LPURPLEFEATHERBOA", "LBLUEFEATHERBOA", "LPINKFEATHERBOA",
        "DMAGENTAFEATHERBOA", "DCRIMSONFEATHERBOA", "DPURPLEFEATHERBOA"
    ]
    scarves = [
        "REDSCARF", "ORANGESCARF", "YELLOWSCARF", "LIMESCARF", "GREENSCARF", "CYANSCARF", "WHITESCARF",
        "BLUESCARF", "DARKBLUESCARF", "PURPLESCARF", "MAGENTASCARF", "BLACKSCARF", "GRAYSCARF", "BROWNSCARF",
        "NSHSCARF", "SAWYERSCARF"
    ]
    neckbandanas = [
        "DICEYNBANDANA", "EOUSNBANDANA", "FLUIDNBANDANA", "GUILDNBANDANA", "SKULLNBANDANA", "SKYNBANDANA", "SPACENBANDANA", "SWEETIENBANDANA",
        "TCYANNBANDANA", "TIEDYEMUDDYNBANDANA", "TIEDYENBANDANA", "TSAVNBANDANA", "BLUEGRADNBANDANA", "ORANGEGRADNBANDANA",  "YELLOWGRADNBANDANA", "LIMEGRADNBANDANA",
        "TEALGRADNBANDANA", "MAGENTAGRADNBANDANA", "REDGRADNBANDANA", "WHITENBANDANA", "LIGHTGRAYNBANDANA", "DARKGRAYNBANDANA", "BLACKNBANDANA", "PEACHNBANDANA",
        "PALEREDNBANDANA", "REDNBANDANA", "MAROONNBANDANA", "PALEORANGENBANDANA", "LIGHTORANGENBANDANA", "ORANGENBANDANA", "BROWNNBANDANA", "PALEYELLOWNBANDANA",
        "LIGHTYELLOWNBANDANA", "YELLOWNBANDANA", "PALEGREENNBANDANA", "LIGHTGREENNBANDANA", "GREENNBANDANA", "DARKGREENNBANDANA", "PALETEALNBANDANA", "LIGHTTEALNBANDANA",
        "TEALNBANDANA", "DARKTEALNBANDANA", "PALEBLUENBANDANA", "LIGHTBLUENBANDANA", "DARKBLUENBANDANA", "BLUENBANDANA", "LAVENDERNBANDANA", "PURPLENBANDANA",
        "DARKPURPLENBANDANA", "PALEPINKNBANDANA", "LIGHTPINKNBANDANA", "PINKNBANDANA", "DARKPINKNBANDANA", "PATCHWORKREDNBANDANA", "PATCHWORKORANGENBANDANA", "PATCHWORKYELLOWNBANDANA",
        "PATCHWORKGREENNBANDANA", "PATCHWORKTEALNBANDANA", "PATCHWORKBLUENBANDANA", "PATCHWORKINDIGONBANDANA", "PATCHWORKPURPLENBANDANA", "PATCHWORKPINKNBANDANA"
    ]
    chains = [
        "AMBERCHAIN", "PINKCHAIN", "PURPLECHAIN", "YELLOWCHAIN", "TEALCHAIN",
        "GREENCHAIN", "REDCHAIN", "ORANGECHAIN", "BLUECHAIN", "BLACKCHAIN"
    ]
    newaccs3 = [
        "FALLMPAINT", "SCAVMPAINT", "SPEARMPAINT", "BLUECLOUDS",
        "YELLOWCLOUDS", "PURPLECLOUDS", "PINKCLOUDS", "GOGGLES",
        "PINKPOLEPLANTBUDDY", "ORANGEPOLEPLANTBUDDY", "REDPOLEPLANTBUDDY"
    ]
    floatyeyes = [
        "YELLOWFLOATYEYES", "REDFLOATYEYES", "ORANGEFLOATYEYES",
        "LIMEFLOATYEYES", "GREENFLOATYEYES", "BLUEFLOATYEYES",
        "INDIGOFLOATYEYES"
        ]
    closest_accs = [
        "CRIMSON", "BLUE", "YELLOW", "CYAN", "RED", "LIME", "GREEN", "RAINBOW",
        "BLACK", "SPIKES", "WHITE", "PINK", "PURPLE", "MULTI", "INDIGO", "CRIMSONBELL", "BLUEBELL",
        "YELLOWBELL", "CYANBELL", "REDBELL", "LIMEBELL", "GREENBELL",
        "RAINBOWBELL", "BLACKBELL", "SPIKESBELL", "WHITEBELL", "PINKBELL", "PURPLEBELL",
        "MULTIBELL", "INDIGOBELL", "CRIMSONBOW", "BLUEBOW", "YELLOWBOW", "CYANBOW", "REDBOW",
        "LIMEBOW", "GREENBOW", "RAINBOWBOW", "BLACKBOW", "SPIKESBOW", "WHITEBOW", "PINKBOW",
        "PURPLEBOW", "MULTIBOW", "INDIGOBOW", "CRIMSONNYLON", "BLUENYLON", "YELLOWNYLON", "CYANNYLON",
        "REDNYLON", "LIMENYLON", "GREENNYLON", "RAINBOWNYLON",
        "BLACKNYLON", "SPIKESNYLON", "WHITENYLON", "PINKNYLON", "PURPLENYLON", "MULTINYLON", "INDIGONYLON",
        "MUDDYPAWS", 
        "REDPAINT", "PINKPAINT", "VOIDPAINT", "YELLOWPAINT", "GREENPAINT", "PALEPAINT",
        "CYANPAINT", "BLUEPAINT", "PURPLEPAINT", "MAGENTAPAINT", "BLACKPAINT", "WHITEPAINT",
        "IMPLANTWHITE", "IMPLANTPURPLE", "IMPLANTGREEN", "IMPLANTYELLOW", "IMPLANTBLUE",
        "EYEIMPLANTWHITE", "EYEIMPLANTRED", "EYEIMPLANTGREEN", "EYEIMPLANTYELLOW", "EYEIMPLANTBLUE",
        "GLOWWHITE", "GLOWPURPLE", "GLOWGREEN", "GLOWYELLOW", "GLOWBLUE",
        "CELLIMPLANT",
        "ORIGINALGAYDRAPERY", "TRANSDRAPERY", "GENDERQUEERDRAPERY", "AGENDERDRAPERY", "NONBINARYDRAPERY", "POLYAMDRAPERY", "GENDERFLUIDDRAPERY",
        "GENDERFLUXDRAPERY", "GAYDRAPERY", "OMNISEXUALDRAPERY", "OBJECTUMDRAPERY", "RAINBOWDRAPERY", "PHILIDRAPERY", "BISEXUALDRAPERY",
        "PANSEXUALDRAPERY", "POLYSEXUALDRAPERY", "ASEXUALDRAPERY", "LESBIANDRAPERY", "INTERSEXDRAPERY", "AROACEDRAPERY", "DEMIGIRLDRAPERY",
        "DEMIBOYDRAPERY", "DEMIGENDERDRAPERY", "DEMIFLUIDDRAPERY", "DEMIFLUXDRAPERY", "ABRODRAPERY", "ARODRAPERY", "DEMISEXDRAPERY",
        "DEMIRODRAPERY", "ACHILLEANDRAPERY", "SAPPHICDRAPERY", "DIAMORICDRAPERY", "UNLABELEDDRAPERY", "TRANSFEMDRAPERY", "TRANSMASCDRAPERY",
        "BIGENDERDRAPERY", "MULTISEXDRAPERY", "ACESPECDRAPERY", "AROSPECDRAPERY"
        "TORNCLOAKFALL", "TORNCLOAKWINTER", "TORNCLOAKNIGHT", "TORNCLOAKSHADOW", "TORNCLOAKSILVER", "FALLENSTARMASK",
        "DPINKFEATHERBOA", "DREDFEATHERBOA", "DGREENFEATHERBOA", "DBLUEFEATHERBOA", "DGREENERFEATHERBOA",
        "DORANGEFEATHERBOA", "LWHITEFEATHERBOA", "LPURPLEFEATHERBOA", "LBLUEFEATHERBOA", "LPINKFEATHERBOA",
        "DMAGENTAFEATHERBOA", "DCRIMSONFEATHERBOA", "DPURPLEFEATHERBOA",
        "REDSCARF", "ORANGESCARF", "YELLOWSCARF", "LIMESCARF", "GREENSCARF", "CYANSCARF", "WHITESCARF",
        "BLUESCARF", "DARKBLUESCARF", "PURPLESCARF", "MAGENTASCARF", "BLACKSCARF", "GRAYSCARF", "BROWNSCARF",
        "NSHSCARF", "SAWYERSCARF", 
        "DICEYNBANDANA", "EOUSNBANDANA", "FLUIDNBANDANA", "GUILDNBANDANA", "SKULLNBANDANA", "SKYNBANDANA", "SPACENBANDANA", "SWEETIENBANDANA",
        "TCYANNBANDANA", "TIEDYEMUDDYNBANDANA", "TIEDYENBANDANA", "TSAVNBANDANA", "BLUEGRADNBANDANA", "ORANGEGRADNBANDANA",  "YELLOWGRADNBANDANA", "LIMEGRADNBANDANA",
        "TEALGRADNBANDANA", "MAGENTAGRADNBANDANA", "REDGRADNBANDANA", "WHITENBANDANA", "LIGHTGRAYNBANDANA", "DARKGRAYNBANDANA", "BLACKNBANDANA", "PEACHNBANDANA",
        "PALEREDNBANDANA", "REDNBANDANA", "MAROONNBANDANA", "PALEORANGENBANDANA", "LIGHTORANGENBANDANA", "ORANGENBANDANA", "BROWNNBANDANA", "PALEYELLOWNBANDANA",
        "LIGHTYELLOWNBANDANA", "YELLOWNBANDANA", "PALEGREENNBANDANA", "LIGHTGREENNBANDANA", "GREENNBANDANA", "DARKGREENNBANDANA", "PALETEALNBANDANA", "LIGHTTEALNBANDANA",
        "TEALNBANDANA", "DARKTEALNBANDANA", "PALEBLUENBANDANA", "LIGHTBLUENBANDANA", "DARKBLUENBANDANA", "BLUENBANDANA", "LAVENDERNBANDANA", "PURPLENBANDANA",
        "DARKPURPLENBANDANA", "PALEPINKNBANDANA", "LIGHTPINKNBANDANA", "PINKNBANDANA", "DARKPINKNBANDANA", "PATCHWORKREDNBANDANA", "PATCHWORKORANGENBANDANA", "PATCHWORKYELLOWNBANDANA",
        "PATCHWORKGREENNBANDANA", "PATCHWORKTEALNBANDANA", "PATCHWORKBLUENBANDANA", "PATCHWORKINDIGONBANDANA", "PATCHWORKPURPLENBANDANA", "PATCHWORKPINKNBANDANA",
        "AMBERCHAIN", "PINKCHAIN", "PURPLECHAIN", "YELLOWCHAIN", "TEALCHAIN",
        "GREENCHAIN", "REDCHAIN", "ORANGECHAIN", "BLUECHAIN", "BLACKCHAIN",
        "FALLMPAINT", "SCAVMPAINT", "SPEARMPAINT", "GOGGLES"
    ]

    tabbies = [
        "Tabby", "Ticked", "Classic", "Sokoke", "Agouti", "Masked", "Vulture", "Envoy", "Drizzle",
        "Necklace", "Leviathan", "Rotten", "Fire", "Solace", "Swing", "Ice", "Maned", "Sunken"
    ]
    spotted = [
        "Speckled", "Rosette", "Gravel", "Banana", "Con", "Bengal", "Dreamer", "Oldgrowth", "Cherry",
        "Sparse", "Impish", "Ringed", "Mold", "Apple", "Glitter", "Patchwork", "Whale", "Pidgeon"
    ]
    plain = [
        "SingleColour", "TwoColour", "Smoke", "Singlestripe", "Collared", "Lizard", "Slimemold",
        "Fluffy", "Yeek", "Rusted", "Leafy", "Scaled", "Countershaded", "Sunset", "Skinny", 
        "Sporty", "Skeleton", "Shred", "Robot"
    ]
    exotic = [
        "Mackerel", "Marbled", "Cyanlizard", "Centipede", "Lantern", "Amoeba", "Seaslug", "Dragonfruit",
        "Duskdawn", "Seer", "Wolf", "Sparklecat", "Hypnotist", "Fizzy", "Glowing", "Budgie", "Lovebird",
        "Amazon", "Boba", "Iggy", "Tomo"
    ]
    torties = ["Tortie", "Calico"]
    pelt_categories = [tabbies, spotted, plain, exotic, torties]

    # SPRITE NAMES
    single_colours = [
        'WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK', 'CREAM', 'PALEGINGER',
        'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA', 'LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN',
        'CHOCOLATE'
    ]
    ginger_colours = ['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']
    black_colours = ['GREY', 'DARKGREY', 'GHOST', 'BLACK']
    white_colours = ['WHITE', 'PALEGREY', 'SILVER']
    brown_colours = ['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']
    colour_categories = [ginger_colours, black_colours, white_colours, brown_colours]
    eye_sprites = [
        'YELLOW', 'AMBER', 'HAZEL', 'PALEGREEN', 'GREEN', 'BLUE', 'DARKBLUE', 'BLUEYELLOW', 'BLUEGREEN',
        'GREY', 'CYAN', 'EMERALD', 'PALEBLUE', 'PALEYELLOW', 'GOLD', 'HEATHERBLUE', 'COPPER', 'SAGE', 'COBALT',
        'SUNLITICE', 'GREENYELLOW', 'BRONZE', 'SILVER', 'RED', 'PURPLE', 'MAUVE',
        'ELECTRICBLUE', 'VIOLET', 'PINK', 'SNOW', 'ORANGE', 'CREAM', 'SEAFOAM', 'CRIMSON', 'NAVY', 'VOIDGOLD', 'COOLBROWN', 'PLUM',
        'INDIGO', 'LILAC', 
        'ALBA', 'ALBINO', 'ANGEL', 'APPLE', 'AQUA', 'ARID', 'BANANA', 'BLOOD', 'CARNI', 'CHAIN', 
        'CREAMY', 'DAWN', 'ESES', 'EXILE', 'FAE', 'FALLSTAR', 'FIELD', 'FOAM', 'HOT', 'IRID', 
        'KARMA', 'KIND', 'MARTI', 'MEISTALT', 'MEISTER', 'MELON', 'MESS', 'MHUNT', 'MINT', 'MINV', 
        'MOON', 'MRIV', 'PEACH', 'PEBB', 'PELA', 'PEPPER', 'RETRO', 'RUNT', 'RUST', 'SIG', 
        'SIXER', 'SPLIT', 'SUN', 'SWEET', 'TIDE', 'VIVID', 'WAVE', 'WINKS', 'ZENI', 'BEAST',
        'BROWNTBOI', 'ORANGETBOI', 'BREDTBOI', 'REDTBOI'
    ]
    little_white = ['LITTLE', 'LIGHTTUXEDO', 'BUZZARDFANG', 'TIP', 'BLAZE', 'BIB', 'VEE', 'PAWS',
                    'BELLY', 'TAILTIP', 'TOES', 'BROKENBLAZE', 'LILTWO', 'SCOURGE', 'TOESTAIL', 'RAVENPAW', 'HONEY',
                    'LUNA',
                    'EXTRA', 'MUSTACHE', 'REVERSEHEART', 'SPARKLE', 'RIGHTEAR', 'LEFTEAR', 'ESTRELLA', 'REVERSEEYE',
                    'BACKSPOT',
                    'EYEBAGS', 'LOCKET', 'BLAZEMASK', 'TEARS', 'GLOVE', 'NECK'
                    'DOTS', 'FIVEPEBBLE', 'SIAMESE', 'SNOWBELLY',
                    'GLOWSTAR', 'STAR', 'DEADPIXEL', 'INSPECTOR', 'FACEDOTS', 'WPTEARS', 'ONEEARTIP', 'NOSETIP']
    mid_white = ['TUXEDO', 'FANCY', 'UNDERS', 'DAMIEN', 'SKUNK', 'MITAINE', 'SQUEAKS', 'STAR', 'WINGS',
                 'DIVA', 'SAVANNAH', 'FADESPOTS', 'BEARD', 'DAPPLEPAW', 'TOPCOVER', 'WOODPECKER', 'MISS', 'BOWTIE',
                 'VEST',
                 'FADEBELLY', 'DIGIT', 'FCTWO', 'FCONE', 'MIA', 'ROSINA', 'PRINCESS', 'BALLER', 'TREFOIL', 'MANUL',
                 'HEAD', 'SPARSE', 'BADGER', 'BELLY', 'MASK', 'LIGHTNING', 'FROSTBITTEN',
                 'LIMBS', 'STRIPES', 'SLICE', 'TOONY', 'ACROBAT']
    high_white = ['ANY', 'ANYTWO', 'BROKEN', 'FRECKLES', 'RINGTAIL', 'HALFFACE', 'PANTSTWO',
                  'GOATEE', 'PRINCE', 'FAROFA', 'MISTER', 'PANTS', 'REVERSEPANTS', 'HALFWHITE', 'APPALOOSA', 'PIEBALD',
                  'CURVED', 'GLASS', 'MASKMANTLE', 'MAO', 'PAINTED', 'SHIBAINU', 'OWL', 'BUB', 'SPARROW', 'TRIXIE',
                  'SAMMY', 'FRONT', 'BLOSSOMSTEP', 'BULLSEYE', 'FINN', 'SCAR', 'BUSTER', 'HAWKBLAZE', 'CAKE',
                  'PAINTSPLAT', 'ELDER',
                  'REVERSEHEAD', 'HEX']
    mostly_white = ['VAN', 'ONEEAR', 'LIGHTSONG', 'TAIL', 'HEART', 'MOORISH', 'APRON', 'CAPSADDLE',
                    'CHESTSPECK', 'BLACKSTAR', 'PETAL', 'HEARTTWO', 'PEBBLESHINE', 'BOOTS', 'COW', 'COWTWO', 'LOVEBUG',
                    'SHOOTINGSTAR', 'EYESPOT', 'PEBBLE', 'TAILTWO', 'BUDDY', 'KROPKA',
                    'DOUGIE', 'REVERSETEARS', 'REVERSETEARSTWO', 'REVERSENECK', 'ESCAPEE']
    point_markings = ['COLOURPOINT', 'RAGDOLL', 'SEPIAPOINT', 'MINKPOINT', 'SEALPOINT']
    vit = ['VITILIGO', 'VITILIGOTWO', 'MOON', 'PHANTOM', 'KARPATI', 'POWDER', 'BLEACHED', 'SMOKEY', 'CHARCOAL']
    white_sprites = [
        little_white, mid_white, high_white, mostly_white, point_markings, vit, 'FULLWHITE']

    empty = ['BLACK',  'PINK', 'DARKBROWN', 'BROWN', 'LIGHTBROWN', 'DARK', 'DARKGREY', 'GREY', 'DARKSALMON',
            'SALMON', 'PEACH', 'DARKMARBLED', 'MARBLED', 'LIGHTMARBLED', 'DARKBLUE', 'BLUE', 'LIGHTBLUE', 'RED']
    gills = ['PINKGILLS', 'BLUEGILLS', 'REDGILLS', 'LIMEGILLS', 'YELLOWGILLS', 'WHITEGILLS', 'RAINBOWGILLS', 'GRAYGILLS', 'HOTGILLS', 'COLDGILLS']
    tongues = ['FUCHSIATONGUE', 'PASTELTONGUE', 'KOBITONGUE', 'REDTONGUE', 'GREYTONGUE', 'ORANGETONGUE']
    spearholes = ['WHITESPOTS', 'BLACKSPOTS', 'MIXSPOTS', 'RAINBOWSPOTS']
    claws = ['BLACKCLAWS']
    antennae = ['WHITETENNA', 'REDTENNA', 'PINKTENNA', 'ORANGETENNA', 'YELLOWTENNA', 'BLUETENNA', 'GREENTENNA']
    glowspots = ['WHITEGLOWSPOTS', 'REDGLOWSPOTS', 'PINKGLOWSPOTS', 'ORANGEGLOWSPOTS', 'YELLOWGLOWSPOTS', 'BLUEGLOWSPOTS', 'GREENGLOWSPOTS']
    ramhorns = ['WHITEHORNSRAM', 'BLACKHORNSRAM', 'REDHORNSRAM', 'YELLOWHORNSRAM', 'GREENHORNSRAM', 'BLUEHORNSRAM', 'ORANGEHORNSRAM', 'BROWNHORNSRAM']
    scavhorns = ['WHITEHORNSSCAV', 'BLACKHORNSSCAV', 'REDHORNSSCAV', 'YELLOWHORNSSCAV', 'GREENHORNSSCAV', 'BLUEHORNSSCAV', 'ORANGEHORNSSCAV', 'BROWNHORNSSCAV']
    elitehorns = ['WHITEHORNSELITE', 'BLACKHORNSELITE', 'REDHORNSELITE', 'YELLOWHORNSELITE', 'GREENHORNSELITE', 'BLUEHORNSELITE', 'ORANGEHORNSELITE', 'BROWNHORNSELITE']
    sharphorns = ['WHITEHORNSSHARP', 'BLACKHORNSSHARP', 'REDHORNSSHARP', 'YELLOWHORNSSHARP', 'GREENHORNSSHARP', 'BLUEHORNSSHARP', 'ORANGEHORNSSHARP', 'BROWNHORNSSHARP']
    dragonhorns = ['WHITEHORNSDRAGON', 'BLACKHORNSDRAGON', 'REDHORNSDRAGON', 'YELLOWHORNSDRAGON', 'GREENHORNSDRAGON', 'BLUEHORNSDRAGON', 'ORANGEHORNSDRAGON', 'BROWNHORNSDRAGON']
    unihorns = ['WHITEHORNSLANCER', 'BLACKHORNSLANCER', 'REDHORNSLANCER', 'YELLOWHORNSLANCER', 'GREENHORNSLANCER', 'BLUEHORNSLANCER', 'ORANGEHORNSLANCER', 'BROWNHORNSLANCER']
    moth = ['WHITEMOTH', 'BLACKMOTH', 'REDMOTH', 'YELLOWMOTH', 'GREENMOTH', 'BLUEMOTH', 'ORANGEMOTH', 'BROWNMOTH']
    whiskers = ['WHITEWHISKERS', 'BLACKWHISKERS', 'REDWHISKERS', 'YELLOWWHISKERS', 'GREENWHISKERS', 'BLUEWHISKERS', 'ORANGEWHISKERS', 'BROWNWHISKERS']
    lizardfins = ['PINKFINS', 'BLUEFINS', 'REDFINS', 'GREENFINS', 'YELLOWFINS', 'WHITEFINS']
    lizardneedles = ['BLACKNEEDLES', 'WHITENEEDLES', 'RAINBOWNEEDLES']
    cyanwings = ['CYANWINGS']
    cyanfeatures = ['WHITECYAN', 'ORANGECYAN', 'BROWNCYAN', 'PINKCYAN', 'PINKERCYAN', 'TEALCYAN', 'GREENCYAN', 'BLOODYCYAN', 'LAVENDERCYAN', 'PURPLECYAN', 'CYANCYAN', 'BLUECYAN', 'DARKBLUECYAN', 'DARKPURPLECYAN', 'BLACKCYAN', 'EGGCYAN', 'YELLOWCYAN']
    anglerfish = ['ANGLERFISH']
    patterns = ['FIREBUGPART', 'TEARS', 'BLACKTHORNS', 'WHITETHORNS', 'GLASSBACK', 'SEASLUGPAPILLAE', 'GRASSSHEEPBACK', 'SEANGLEWINGS', 'ACROTAIL']
    catfish_whiskers = ['WHITECATFISHWHISKERS', 'PINKCATFISHWHISKERS', 'REDCATFISHWHISKERS', 'YELLOWCATFISHWHISKERS', 'GREENCATFISHWHISKERS', 'REDYELLOWCATFISHWHISKERS', 'BLUECATFISHWHISKERS', 'PURPLECATFISHWHISKERS', 'BLACKCATFISHWHISKERS', 'BLUEGREENCATFISHWHISKERS', 'BLUEPINKCATFISHWHISKERS', 'BROWNCATFISHWHISKERS']
    dragon_whiskers = ['WHITEDRAGONWHISKERS', 'PINKDRAGONWHISKERS', 'REDDRAGONWHISKERS', 'YELLOWDRAGONWHISKERS', 'GREENDRAGONWHISKERS', 'REDYELLOWDRAGONWHISKERS', 'BLUEDRAGONWHISKERS', 'PURPLEDRAGONWHISKERS', 'BLACKDRAGONWHISKERS', 'BLUEGREENDRAGONWHISKERS', 'BLUEPINKDRAGONWHISKERS', 'BROWNDRAGONWHISKERS']
    orbitals = ['ORANGEORBITAL', 'YELLOWORBITAL', 'EARTHORBITAL', 'EARTHTWOORBITAL', 'PURPLEORBITAL', 'PINKORBITAL', 'REDORBITAL']
    skin_categories = [empty, gills, tongues, spearholes, claws, antennae, glowspots, ramhorns, scavhorns, elitehorns, sharphorns, dragonhorns, unihorns, moth, whiskers, lizardfins, lizardneedles, cyanwings, cyanfeatures, anglerfish, patterns, catfish_whiskers, dragon_whiskers, orbitals]
    #list for stuff that should logically be below a cloak
    closest_skin = [
        'WHITESPOTS', 'BLACKSPOTS', 'MIXSPOTS', 'RAINBOWSPOTS',
        'WHITEGLOWSPOTS', 'REDGLOWSPOTS', 'PINKGLOWSPOTS', 'ORANGEGLOWSPOTS', 'YELLOWGLOWSPOTS', 'BLUEGLOWSPOTS', 'GREENGLOWSPOTS',
        'WHITECYAN', 'ORANGECYAN', 'BROWNCYAN', 'PINKCYAN', 'PINKERCYAN', 'TEALCYAN', 'GREENCYAN', 'BLOODYCYAN', 'LAVENDERCYAN', 
        'PURPLECYAN', 'CYANCYAN', 'BLUECYAN', 'DARKBLUECYAN', 'DARKPURPLECYAN', 'BLACKCYAN', 'EGGCYAN', 'YELLOWCYAN',
        'PINKFINS', 'BLUEFINS', 'REDFINS', 'GREENFINS', 'YELLOWFINS', 'WHITEFINS',
        'BLACKNEEDLES', 'WHITENEEDLES', 'RAINBOWNEEDLES',
        'TEARS', 'SEANGLEWINGS', 'GLASSBACK', 'GRASSSHEEPBACK'
    ]
    #skin_weights = [40, 10, 10, 6, 4, 10, 8, 2, 3, 2, 2, 1, 2, 3, 2]
    skin_weights = game.config["feature_generation"]["feature_chances"]

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
                 inventory:list=None
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

        # White patches must be initalized before eye color.
        num = game.config["cat_generation"]["base_heterochromia"]
        if self.white_patches in [Pelt.high_white, Pelt.mostly_white, 'FULLWHITE'] or self.colour == 'WHITE':
            num = num - 30
        if self.white_patches == 'FULLWHITE' or self.colour == 'WHITE':
            num -= 10
        for _par in parents:
            if _par.pelt.eye_colour2:
                num -= 10

        if num < 0:
            num = 1
            
        multieyenum = game.config["cat_generation"]["base_multieyes"]
        riveyenum = game.config["cat_generation"]["base_riveyes"]
        buttoneyenum = game.config["cat_generation"]["base_buttoneyes"]

        if not random.randint(0, riveyenum):
            self.eye_colour = choice(Pelt.riveye_colours)
        elif not random.randint(0, buttoneyenum):
            self.eye_colour = choice(Pelt.buttoneye_colours)

        if not random.randint(0, num):
            if self.eye_colour in Pelt.pupil_eyes:
                colour_wheel = [Pelt.yellow_pupil_eyes, Pelt.blue_pupil_eyes, Pelt.green_pupil_eyes, Pelt.red_pupil_eyes]
            elif self.eye_colour in Pelt.riveye_colours:
                colour_wheel = [Pelt.yellow_riv_eyes, Pelt.blue_riv_eyes, Pelt.green_riv_eyes]
            else:
                colour_wheel = [Pelt.yellow_eyes, Pelt.blue_eyes, Pelt.green_eyes, Pelt.red_eyes]
            for colour in colour_wheel[:]:
                if self.eye_colour in colour:
                    colour_wheel.remove(colour) # removes the selected list from the options
                    self.eye_colour2 = choice(choice(colour_wheel)) # choose from the remaining two lists
                    break

        elif self.eye_colour not in Pelt.riveye_colours and self.eye_colour not in Pelt.buttoneye_colours and not random.randint(0, multieyenum):
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
            if p_ in Pelt.ginger_colours:
                add_weight = (40, 0, 0, 10)
            elif p_ in Pelt.black_colours:
                add_weight = (0, 40, 2, 5)
            elif p_ in Pelt.white_colours:
                add_weight = (0, 5, 40, 0)
            elif p_ in Pelt.brown_colours:
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
                choice(Pelt.muddypaws),
                choice(Pelt.lizards),
                choice(Pelt.insectwings),
                choice(Pelt.herbs2),
                choice(Pelt.buddies),
                choice(Pelt.newaccs),
                choice(Pelt.bodypaint),
                choice(Pelt.necklaces),
                choice(Pelt.larsaccs),
                choice(Pelt.harleyaccs),
                choice(Pelt.featherboas),
                choice(Pelt.scarves),
                choice(Pelt.neckbandanas),
                choice(Pelt.chains),
                choice(Pelt.newaccs3),
                choice(Pelt.floatyeyes)
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
                        self.tortiecolour = choice((Pelt.ginger_colours * 2) + Pelt.brown_colours)
                    elif self.colour in Pelt.ginger_colours:
                        self.tortiecolour = choice(Pelt.brown_colours + Pelt.black_colours * 2)
                    elif self.colour in Pelt.brown_colours:
                        possible_colors = Pelt.brown_colours.copy()
                        possible_colors.remove(self.colour)
                        possible_colors.extend(Pelt.black_colours + (Pelt.ginger_colours * 2))
                        self.tortiecolour = choice(possible_colors)
                    else:
                        self.tortiecolour = "GOLDEN"

            else:
                self.tortiecolour = "GOLDEN"
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

        # Define look-up dictionaries
        if short:
            renamed_colors = {
                "white": "pale",
                "palegrey": "gray",
                "darkgrey": "gray",
                "grey": "gray",
                "paleginger": "ginger",
                "darkginger": "ginger",
                "sienna": "ginger",
                "lightbrown": "brown",
                "lilac": "brown",
                "golden-brown": "brown",
                "darkbrown": "brown",
                "chocolate": "brown",
                "ghost": "black"
            }
        else:
            renamed_colors = {
                "white": "pale",
                "palegrey": "pale gray",
                "grey": "gray",
                "darkgrey": "dark gray",
                "paleginger": "pale ginger",
                "darkginger": "dark ginger",
                "sienna": "dark ginger",
                "lightbrown": "light brown",
                "lilac": "light brown",
                "golden-brown": "golden brown",
                "darkbrown": "dark brown",
                "chocolate": "dark brown",
                "ghost": "black"
            }

        pattern_des = {
            "Tabby": "c_n tabby",
            "Speckled": "speckled c_n",
            "Bengal": "unusually dappled c_n",
            "Marbled": "c_n tabby",
            "Ticked": "c_n ticked",
            "Smoke": "c_n smoke",
            "Mackerel": "c_n tabby",
            "Classic": "c_n tabby",
            "Agouti": "c_n tabby",
            "Singlestripe": "dorsal-striped c_n",
            "Rosette": "unusually spotted c_n",
            "Sokoke": "c_n tabby",
            "Masked": "masked c_n tabby"
        }

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
                if cat.pelt.colour in Pelt.black_colours + Pelt.brown_colours + Pelt.white_colours and \
                        cat.pelt.tortiecolour in Pelt.black_colours + Pelt.brown_colours + Pelt.white_colours:
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

                if cat.pelt.colour in Pelt.black_colours + Pelt.brown_colours + Pelt.white_colours and \
                        cat.pelt.tortiecolour in Pelt.black_colours + Pelt.brown_colours + Pelt.white_colours:
                    color_name = f"{color_name} mottled{base}"
                else:
                    color_name = f"{color_name} {cat.pelt.name.lower()}{base}"

        if cat.pelt.white_patches:
            if cat.pelt.white_patches == "FULLWHITE":
                # If the cat is fullwhite, discard all other information. They are just white
                color_name = "white"
            if cat.pelt.white_patches in Pelt.mostly_white and cat.pelt.name != "Calico":
                color_name = f"white and {color_name}"
            elif cat.pelt.name != "Calico":
                color_name = f"{color_name} and white"

        if cat.pelt.points:
            color_name = f"{color_name} point"
            if "ginger point" in color_name:
                color_name.replace("ginger point", "flame point")

        if "white and white" in color_name:
            color_name = color_name.replace("white and white", "white")

        # Now it's time for gender
        if cat.genderalign in ["female", "trans female"]:
            color_name = f"{color_name} female"
        elif cat.genderalign in ["male", "trans male"]:
            color_name = f"{color_name} male"
        else:
            color_name = f"{color_name} slugcat"

        # Here is the place where we can add some additional details about the cat, for the full non-short one
        # These include notable missing limbs, vitiligo, long-furred-ness, and 3 or more scars
        if not short:

            scar_details = {
                "NOTAIL": "no tail",
                "HALFTAIL": "half a tail",
                "NOPAW": "three legs",
                "NOLEFTEAR": "a missing ear",
                "NORIGHTEAR": "a missing ear",
                "NOEAR": "no ears",
                "ROTRIDDEN": "the rot"
            }

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
