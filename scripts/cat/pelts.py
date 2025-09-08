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
        'Watermelon': 'watermelon',
        'Dragonet': 'dragonet',
        'Salmon': 'salmon',
        'Lightecho': 'lightecho',
        'Darkecho': 'darkecho',
        'Plantain': 'plantain',
        'Daenix': 'daenix',
        'Seltzer': 'seltzer',
        'Sworn': 'sworn',
        'Spooky': 'spooky',
        'Conure': 'conure',
        'Noble': 'noble',
        'Betta': 'betta',
        'Constellation': 'constellation',
        'Malibu': 'malibu',
        'Clay': 'clay',
        'Antethisis': 'antethisis',
        'Citadel': 'citadel',
        'Grave': 'grave',
        'Interloper': 'interloper',
        'Tortie': None,
        'Calico': None,
    }

    @staticmethod
    def with_suffix(colours, suffix):
        #Helper code for OPTIMIZATION WOOOO
        return [f"{c}{suffix}" for c in colours]

    # ATTRIBUTES, including non-pelt related
    pelt_colours = [
        'WHITE', 'SKY', 'BLUE', 'INDIGO', 'PURPLE', 'GHOST', 'BLACK', 'CREAM', 'YELLOW',
        'ORANGE', 'SCARLET', 'RED', 'PINK', 'MINT', 'LIME', 'GREEN', 'MAROON', 'PERIWINKLE',
        'LAVENDER'
    ]
    pelt_c_no_white = [
        'SKY', 'BLUE', 'INDIGO', 'PURPLE', 'GHOST', 'BLACK', 'CREAM', 'YELLOW',
        'ORANGE', 'SCARLET', 'RED', 'PINK', 'MINT', 'LIME', 'GREEN', 'MAROON', 'PERIWINKLE',
        'LAVENDER'
    ]
    pelt_c_no_bw = [
        'SKY', 'BLUE', 'INDIGO', 'PURPLE', 'CREAM', 'YELLOW',
        'ORANGE', 'SCARLET', 'RED', 'PINK', 'MINT', 'LIME', 'GREEN', 'MAROON', 'PERIWINKLE',
        'LAVENDER'
    ]

    tortiepatterns = ['ONE', 'TWO', 'THREE', 'FOUR', 'REDTAIL', 'DELILAH', 'HALF', 'STREAK', 'MASK', 'SMOKE',
                    'MINIMALONE', 'MINIMALTWO', 'MINIMALTHREE', 'MINIMALFOUR', 'OREO', 'SWOOP', 'CHIMERA', 'CHEST', 'ARMTAIL',
                    'GRUMPYFACE',
                    'MOTTLED', 'SIDEMASK', 'EYEDOT', 'BANDANA', 'PACMAN', 'STREAMSTRIKE', 'SMUDGED', 'DAUB', 'EMBER', 'BRIE',
                    'ORIOLE', 'ROBIN', 'BRINDLE', 'PAIGE', 'ROSETAIL', 'SAFI', 'DAPPLENIGHT', 'BLANKET', 'BELOVED', 'BODY',
                    'SHILOH', 'FRECKLED', 'HEARTBEAT', 'SPECKLES', 'TIGER', 'SHROOM', 'MAILBOX', 'GILAMONSTER', 'RINGEDMIMIC',
                    'NECKLACEMIMIC']
    tortiebases = ['single', 'tabby', 'bengal', 'marbled', 'ticked', 'smoke', 'rosette', 'speckled', 'mackerel',
                'classic', 'sokoke', 'agouti', 'singlestripe', 'masked', 'gravel', 'collared', 'slimemold',
                'cyanlizard', 'vulture', 'banana', 'centipede', 'con', 'lizard', 'lantern', 'leviathan',
                'fluffy', 'amoeba', 'yeek', 'rusted', 'envoy', 'drizzle', 'solace', 'leafy', 'scaled', 'dragonfruit', 
                'necklace', 'dreamer', 'duskdawn', 'seer', 'rotten', 'fire', 'countershaded', 'sunset', 'oldgrowth', 
                'sparklecat', 'wolf', 'cherry', 'hypnotist', 'ringed', 'skinny', 'sparse', 'impish', 'sporty', 
                'skeleton', 'shred', 'glowing', 'mold', 'swing', 'lovebird', 'budgie', 'amazon', 'apple', 'boba',
                'glitter', 'ice', 'iggy', 'maned', 'patchwork', 'robot', 'sunken', 'tomo', 'whale', 'pidgeon', 'watermelon',
                'dragonet', 'salmon', 'lightecho', 'darkecho', 'plantain', 'daenix', 'seltzer', 'sworn', 'spooky', 'conure', 
                'noble', 'betta', 'constellation', 'malibu', 'clay']

    pelt_length = ["short", "medium", "long"]
    eye_colours = ['YELLOW', 'AMBER', 'HAZEL', 'PALEGREEN', 'GREEN', 'BLUE', 'DARKBLUE', 'GREY', 'CYAN', 'EMERALD', 'PALEBLUE', 
        'PALEYELLOW', 'GOLD', 'HEATHERBLUE', 'COPPER', 'SAGE', 'COBALT', 'SUNLITICE', 'GREENYELLOW', 'BRONZE', 'SILVER', 'RED', 'PURPLE', 'MAUVE',
        'ELECTRICBLUE', 'VIOLET', 'PINK', 'SNOW', 'ORANGE', 'CREAM', 'SEAFOAM', 'CRIMSON', 'NAVY', 'VOIDGOLD', 'COOLBROWN', 'PLUM',
        'INDIGO', 'LILAC', 'ACROBLUE', 'ACROGREEN', 'ACROGREY', 'ACROINDIGO', 'ACROAMBER', 'ACROPINK', 'ACRORED', 'ACROTEAL',
        'ALBA', 'ALBINO', 'ANGEL', 'APPLE', 'AQUA', 'ARID', 'BANANA', 'BLOOD', 'CARNI', 'CHAIN', 
        'CREAMY', 'DAWN', 'ESES', 'EXILE', 'FAE', 'FALLSTAR', 'FIELD', 'FOAM', 'HOT', 'IRID', 
        'KARMA', 'KIND', 'MARTI', 'MEISTALT', 'MEISTER', 'MELON', 'MESS', 'MHUNT', 'MINT', 'MINV', 
        'MOON', 'MRIV', 'PEACH', 'PEBB', 'PELA', 'PEPPER', 'RETRO', 'RUNT', 'RUST', 'SIG', 
        'SIXER', 'SPLIT', 'SUN', 'SWEET', 'TIDE', 'VIVID', 'WAVE', 'WINKS', 'ZENI', 'BEAST',

        'BROWNTBOI', 'ORANGETBOI', 'BREDTBOI', 'REDTBOI', 'FIRE', 'RUBY', 'RUBYAGAIN', 'ESCAPEE',
        'REFORGED', 'FLORAVORE', 'REJECT', 'WAYFARER', 'PISTON', 'EXILED', 'THEIF', 'THEIFDOS', 'MORTICIAN',
        'SWAMPY', 'PORTALMAKER', 'PURIFIER', 'CORROSOL', 'SEVENSEVEN', 'ATLAN', 'BASIC', 'BELL', 'BIS', 'BIT',
        'CRITTER', 'CUBED', 'DIM', 'DOE', 'FREYR', 'GAMBLE', 'GORB', 'HERO', 'JANE', 'JOHN', 'MATT', 'MESS',
        'PE', 'POLE', 'RAT', 'RGB', 'ROT', 'SCRATCH', 'SHED', 'SIEGE', 'SPARK', 'SPARKLE', 'SUNSET', 'TELA',
        'USURP', 'WAR', 'XIII', 
        
        'BUTCHER', 'DREAMER', 'FAKEGOLD', 'GREENDREAM', 'HEATSTROKE', 'VIBRANCY', 'SIGNAL', 'PURPLEDREAM', 
        'NOVEMBER', 'LEADER']
    
    #do NOT add eyes with pupils here!!!! they go in yourcolour_pupil_eyes
    yellow_eyes = [
        'YELLOW', 'AMBER', 'PALEYELLOW', 'GOLD', 'COPPER', 'GREENYELLOW', 'BRONZE', 'SILVER', 'ORANGE', 'CREAM', 'VOIDGOLD',
        'BROWNTBOI', 'ORANGETBOI', 'ACROAMBER', 'ACROGREY', 'FIRE', 'PISTON', 'THEIFDOS', 'MORTICIAN', 'SWAMPY',
        'PURIFIER', 'CORROSOL',
        'BUTCHER', 'FAKEGOLD', 'HEATSTROKE', 'VIBRANCY'
        ]
    blue_eyes = [
        'BLUE', 'DARKBLUE', 'CYAN', 'PALEBLUE', 'HEATHERBLUE', 'COBALT', 'SUNLITICE', 'GREY', 'ELECTRICBLUE', 'SNOW', 'INDIGO',
        'ANGEL', 'ACROBLUE', 'ACROINDIGO', 'ESCAPEE', 'REJECT', 'WAYFARER', 'THEIF', 'GREENDREAM', 'SIGNAL', 'PURPLEDREAM',
        'NOVEMBER'
        ]
    green_eyes = [
        'PALEGREEN', 'GREEN', 'EMERALD', 'SAGE', 'HAZEL', 'SEAFOAM', 'NAVY', 'MESS', 'ACROGREEN', 'ACROTEAL', 'EXILED',
        'DREAMER', 'LEADER'
        ]
    red_eyes = [
        'RED', 'PURPLE', 'MAUVE', 'VIOLET', 'PINK', 'CRIMSON', 'COOLBROWN', 'PLUM', 'LILAC', 
        'MINT', 'PEACH', 'ALBINO', 'DAWN', 'BREDTBOI', 'REDTBOI', 'ACROPINK', 'ACRORED', 'RUBY', 'RUBYAGAIN', 'FLORAVORE',
        'HERO'
        ]
    
    #when a scug has one eye with a pupil and one without it looks bad so please list all eyes with pupils
    pupil_eyes = ['ALBA', 'BANANA', 'CREAMY', 'KARMA', 'MHUNT', 'PEPPER', 'SPLIT', 'WINKS', 'ZENI', 'BEAST',
                'CARNI', 'CHAIN', 'FOAM', 'MEISTALT', 'MELON', 'MINV', 'MOON', 'MRIV', 'PEBB', 'RUST', 'SIG', 
                'TIDE', 'VIVID', 'WAVE', 'APPLE', 'AQUA', 'FAE', 'FIELD', 'IRID', 'RUNT', 
                'ARID', 'BLOOD', 'ESES', 'EXILE', 'FALLSTAR', 'HOT', 'KIND', 'MARTI', 'MEISTER', 
                'PELA', 'RETRO', 'SIXER', 'SUN', 'SWEET',
                'REFORGED', 'PORTALMAKER', 'SEVENSEVEN', 'ATLAN', 'BASIC', 'BELL', 'BIS', 'BIT', 'CRITTER', 
                'CUBED', 'DOE', 'FREYR', 'GAMBLE', 'GORB', 'JANE', 'JOHN', 'MATT', 'MESS', 'PE', 'POLE', 
                'RAT', 'RGB', 'ROT', 'SCRATCH', 'SHED', 'SIEGE', 'SPARK', 'SPARKLE', 'SUNSET', 'TELA', 
                'USURP', 'WAR', 'XIII']
    yellow_pupil_eyes = ['ALBA', 'BANANA', 'CREAMY', 'KARMA', 'MHUNT', 'PEPPER', 'SPLIT', 'WINKS', 'ZENI', 'BEAST',
                        'REFORGED', 'ATLAN', 'BASIC', 'BELL', 'GAMBLE']
    blue_pupil_eyes = ['CARNI', 'CHAIN', 'FOAM', 'MEISTALT', 'MELON', 'MINV', 'MOON', 'MRIV', 'PEBB', 'RUST', 'SIG', 
                        'TIDE', 'VIVID', 'WAVE', 'PORTALMAKER', 'CRITTER', 'FREYR', 'RAT', 'ROT']
    green_pupil_eyes = ['APPLE', 'AQUA', 'FAE', 'FIELD', 'IRID', 'RUNT', 'CUBED',
                        'GORB', 'JOHN', 'PE', 'POLE', 'RGB', 'SHED', 'SPARKLE', 'USURP', 'XIII']
    red_pupil_eyes = ['ARID', 'BLOOD', 'ESES', 'EXILE', 'FALLSTAR', 'HOT', 'KIND', 'MARTI', 'MEISTER', 
                        'PELA', 'RETRO', 'SIXER', 'SUN', 'SWEET', 'SEVENSEVEN', 'BIS', 'BIT',
                        'DOE', 'JANE', 'MATT', 'MESS', 'SCRATCH', 'SIEGE', 'SPARK', 'SUNSET', 'TELA',
                        'DIM']

    riveye_colours = ['RIVYELLOW', 'RIVAMBER', 'RIVHAZEL', 'RIVPALEGREEN', 'RIVGREEN', 'RIVBLUE', 'RIVDARKBLUE', 'RIVGREY', 'RIVCYAN', 'RIVEMERALD', 'RIVPALEBLUE', 
               'RIVPALEYELLOW', 'RIVGOLD', 'RIVHEATHERBLUE', 'RIVCOPPER', 'RIVSAGE', 'RIVCOBALT', 'RIVSUNLITICE', 'RIVGREENYELLOW', 'RIVBRONZE', 'RIVSILVER',
               'ALTRIVYELLOW', 'ALTRIVAMBER', 'ALTRIVHAZEL', 'ALTRIVPALEGREEN', 'ALTRIVGREEN', 'ALTRIVBLUE', 'ALTRIVDARKBLUE', 'ALTRIVCYAN', 'ALTRIVEMERALD',
               'ALTRIVHEATHERBLUE', 'ALTRIVSUNLITICE', 'ALTRIVCOPPER', 'ALTRIVSILVER', 'ALTRIVPALEYELLOW', 'ALTRIVGOLD', 'ALTRIVGREENYELLOW', 'RIVRED', 'RIVPURPLE', 'RIVMAUVE','RIVELECTRICBLUE', 'RIVVIOLET',
               'RIVPINK', 'RIVSNOW', 'RIVORANGE', 'RIVCREAM', 'RIVSEAFOAM', 'RIVCRIMSON', 'RIVNAVY', 'RIVVOIDGOLD', 'RIVCOOLBROWN', 'RIVPLUM', 'RIVINDIGO', 'RIVLILAC',
               'RIVALBA', 'RIVALBINO', 'RIVANGEL', 'RIVAPPLE', 'RIVAQUA', 'RIVARID', 'RIVBANANA', 'RIVBLOOD', 'RIVCARNI', 'RIVCHAIN', 'RIVCREAMY', 'RIVDAWN',
               'RIVESES', 'RIVEXILE', 'RIVFAE', 'RIVFALLSTAR', 'RIVFIELD', 'RIVFOAM', 'RIVHOT', 'RIVIRID', 'RIVKARMA', 'RIVKIND', 'RIVMARTI', 'RIVMEISTALT',
               'RIVMHUNT', 'RIVMELON', 'RIVMESS', 'RIVMEISTER', 'RIVMINT', 'RIVMINV', 'RIVMOON', 'RIVMRIV', 'RIVPEACH', 'RIVPEBB', 'RIVPELA', 'RIVPEPPER',
               'RIVRETRO', 'RIVRUNT', 'RIVRUST', 'RIVSIG', 'RIVSIXER', 'RIVSPLIT', 'RIVSUN', 'RIVSWEET', 'RIVTIDE', 'RIVVIVID', 'RIVWAVE', 'RIVWINKS',
               'RIVZENI', 'RIVBROWNTBOI', 'RIVORANGETBOI', 'RIVBREDTBOI', 'RIVREDTBOI', 'RIVACROINDIGO', 'RIVACROAMBER', 'RIVACROTEAL', 'RIVACROGREY', 'RIVACROGREEN', 'RIVACROBLUE', 'RIVACRORED',
               'RIVACROPINK', 'RIVSPARKLE', 'RIVSUNSET', 'RIVSIEGE', 'RIVROT', 'RIVUSURP', 'RIVPE', 'RIVBIS', 'RIVCRITTER', 'RIVCUBED', 'RIVGAMBLE', 'RIVDIM', 'RIVBLUEORANGE', 'RIVMENACE',
               'RIVDEVIOUS', 'RIVGORB', 'RIVSTARSTRUCK', 'RIVAMBERHONEY', 'RIVSUNDOWN', 'RIVPARADISE', 'RIVMOLTENLAVA', 'RIVSILVERMOON', 'RIVSHADOWEDSILVER', 'RIVLACREATURA',
               'RIVAWAKENED', 'RIVASCENDED', 'RIVBLUERED', 'RIVWHITESILVER', 'RIVPINKLEMONADE', 'RIVHARVESTMOON', 'RIVPORTALGUN', 'RIVGASLIGHT', 'RIVBRONZEDIRT', 'RIVRBG', 'RIVRUBICON', 'RIVFIREGOLD', 'RIVBLOODRIVER',
               'RIVPARTYRGB', 'RIVMIDNIGHTGLOW', 'RIVRBGLIGHTS', 'RIVBUBBLEGUM', 'RIVCYN']
    yellow_riv_eyes = ['RIVYELLOW', 'RIVAMBER', 'RIVPALEYELLOW', 'RIVGOLD', 'RIVCOPPER', 'RIVGREENYELLOW', 'RIVBRONZE', 'RIVSILVER', 'ALTRIVYELLOW', 'ALTRIVAMBER', 'ALTRIVPALEYELLOW',
                      'ALTRIVGOLD', 'ALTRIVCOPPER', 'ALTRIVGREENYELLOW', 'ALTRIVBRONZE', 'ALTRIVSILVER', 'RIVORANGE', 'RIVCREAM', 'RIVVOIDGOLD', 'RIVBROWNTBOI', 'RIVORANGETBOI',
                      'RIVACROAMBER', 'RIVACROGREY', 'RIVSUNSET', 'RIVSIEGE', 'RIVAMBERHONEY', 'RIVPARADISE', 'RIVMOLTENLAVA', 'RIVAWAKENED', 'RIVASCENDED', 'RIVHARVESTMOON',
                      'RIVBRONZEDIRT', 'RIVRUBICON', 'RIVFIREGOLD', 'RIVCYN']
    blue_riv_eyes = ['RIVBLUE', 'RIVDARKBLUE', 'RIVCYAN', 'RIVPALEBLUE', 'RIVHEATHERBLUE', 'RIVCOBALT', 'RIVSUNLITICE', 'ALTRIVBLUE', 'ALTRIVDARKBLUE', 'ALTRIVCYAN', 'ALTRIVPALEBLUE', 'ALTRIVHEATHERBLUE',
                     'ALTRIVCOBALT', 'ALTRIVSUNLITICE', 'RIVELECTRICBLUE', 'RIVSNOW', 'RIVINDIGO', 'RIVANGEL', 'RIVACROBLUE', 'RIVACROINDIGO', 'RIVROT', 'RIVUSURP', 'RIVPE', 'RIVCRITTER', 'RIVBLUEORANGE',
                     'RIVSTARSTRUCK', 'RIVSILVERMOON', 'RIVSHADOWEDSILVER', 'RIVWHITESILVER', 'RIVPORTALGUN', 'RIVPARTYRGB', 'RIVMIDNIGHTGLOW']
    green_riv_eyes = ['RIVPALEGREEN', 'RIVGREEN', 'RIVEMERALD', 'RIVSAGE', 'RIVHAZEL', 'ALTRIVPALEGREEN', 'ALTRIVGREEN', 'ALTRIVEMERALD', 'ALTRIVSAGE', 'ALTRIVHAZEL', 'RIVSEAFOAM', 'RIVNAVY',
                     'RIVMESS', 'RIVACROGREEN', 'RIVACROTEAL', 'RIVCUBED', 'RIVGORB', 'RIVRGB', 'RIVRBGLIGHTS']
    red_riv_eyes = ['RIVRED', 'RIVPURPLE', 'RIVMAUVE', 'RIVVIOLET', 'RIVPINK', 'RIVCRIMSON', 'RIVCOOLBROWN', 'RIVPLUM', 'RIVLILAC', 'RIVMINT', 'RIVPEACH', 'RIVALBINO', 'RIVDAWN', 'RIVBREDTBOI',
                    'RIVREDTBOI', 'RIVACROPINK', 'RIVACRORED', 'RIVSPARKLE', 'RIVBIS', 'RIVGAMBLE', 'RIVDIM', 'RIVMENACE', 'RIVDEVIOUS', 'RIVSUNDOWN', 'RIVLACREATURA', 'RIVBLUERED',
                    'RIVPINKLEMONADE', 'RIVGASLIGHT', 'RIVBLOODRIVER', 'RIVBUBBLEGUM']
    
    buttoneye_colours = ['BUTTONYELLOW', 'BUTTONAMBER', 'BUTTONHAZEL', 'BUTTONPALEGREEN', 'BUTTONGREEN', 'BUTTONBLUE', 
                'BUTTONDARKBLUE', 'BUTTONGREY', 'BUTTONCYAN', 'BUTTONEMERALD', 'BUTTONHEATHERBLUE', 'BUTTONSUNLITICE', 
                'BUTTONCOPPER', 'BUTTONSAGE', 'BUTTONCOBALT', 'BUTTONPALEBLUE', 'BUTTONBRONZE', 'BUTTONSILVER', 'BUTTONPALEYELLOW',
                'BUTTONGOLD', 'BUTTONGREENYELLOW', 'BUTTONIRED', 'BUTTONPURPLE', 'BUTTONMAUVE', 'BUTTONINDIGO', 'BUTTONLILAC']
    yellow_button_eyes = ['BUTTONYELLOW', 'BUTTONAMBER', 'BUTTONPALEYELLOW', 'BUTTONGOLD', 'BUTTONCOPPER', 'BUTTONGREENYELLOW', 'BUTTONBRONZE', 'BUTTONSILVER']
    blue_button_eyes = ['BUTTONBLUE', 'BUTTONDARKBLUE', 'BUTTONCYAN', 'BUTTONPALEBLUE', 'BUTTONHEATHERBLUE', 'BUTTONCOBALT', 'BUTTONSUNLITICE', 'BUTTONINDIGO']
    green_button_eyes = ['BUTTONPALEGREEN', 'BUTTONGREEN', 'BUTTONEMERALD', 'BUTTONSAGE']
    red_button_eyes = ['BUTTONIRED', 'BUTTONPURPLE', 'BUTTONMAUVE', 'BUTTONLILAC']

    bobaeye_colours = ['BOBAYELLOW', 'BOBAAMBER', 'BOBAHAZEL', 'BOBAPALEGREEN', 'BOBAGREEN', 'BOBABLUE', 'BOBADARKBLUE', 'BOBAGREY', 'BOBACYAN',
                       'BOBAEMERALD', 'BOBAHEATHERBLUE', 'BOBASUNLITICE', 'BOBACOPPER', 'BOBASAGE', 'BOBACOBALT', 'BOBAPALEBLUE', 'BOBABRONZE', 'BOBASILVER',
                       'BOBAPALEYELLOW', 'BOBAGOLD', 'BOBAGREENYELLOW', 'BOBARED', 'BOBAPURPLE', 'BOBAMAUVE', 'BOBAALBA', 'BOBAALBINO', 'BOBAANGEL', 'BOBAAPPLE',
                       'BOBAAQUA', 'BOBAARID', 'BOBABANANA', 'BOBABLOOD', 'BOBACARNI', 'BOBACHAIN', 'BOBACREAMY', 'BOBADAWN', 'BOBAESES', 'BOBAEXILE', 'BOBAFAE',
                       'BOBAFALLSTAR', 'BOBAFIELD', 'BOBAFOAM', 'BOBAHOT', 'BOBAIRID', 'BOBAKARMA', 'BOBAKIND', 'BOBAMARTI', 'BOBAMEISTALT', 'BOBAMHUNT', 'BOBAMELON',
                       'BOBAMESS', 'BOBAMEISTER', 'BOBAMINT', 'BOBAMINV', 'BOBAMOON', 'BOBAMRIV', 'BOBAPEACH', 'BOBAPEBB', 'BOBAPELA', 'BOBAPEPPER', 'BOBARETRO',
                       'BOBARUNT', 'BOBARUST', 'BOBASIG', 'BOBASIXER', 'BOBASPLIT', 'BOBASUN', 'BOBASWEET', 'BOBATIDE', 'BOBAVIVID', 'BOBAWAVE', 'BOBAWINKS', 'BOBAZENI',
                       'BOBABEAST']
    yellow_boba_eyes = ['BOBAYELLOW', 'BOBAAMBER', 'BOBAPALEYELLOW', 'BOBAGOLD', 'BOBACOPPER', 'BOBAGREENYELLOW', 'BOBABRONZE', 'BOBASILVER',
                       'BOBAALBA', 'BOBABANANA', 'BOBACREAMY', 'BOBAKARMA', 'BOBAMHUNT', 'BOBAPEPPER', 'BOBASPLIT', 'BOBAWINKS', 'BOBAZENI', 'BOBABEAST']
    blue_boba_eyes = ['BOBABLUE', 'BOBADARKBLUE', 'BOBACYAN', 'BOBAPALEBLUE', 'BOBAHEATHERBLUE', 'BOBACOBALT', 'BOBASUNLITICE', 'BOBAGREY',
                     'BOBACARNI', 'BOBACHAIN', 'BOBAFOAM', 'BOBAMEISTALT', 'BOBAMELON', 'BOBAMINV', 'BOBAMOON', 'BOBAMRIV', 'BOBAPEBB', 'BOBARUST',
                     'BOBASIG', 'BOBATIDE', 'BOBAVIVID', 'BOBAWAVE']
    green_boba_eyes = ['BOBAPALEGREEN', 'BOBAGREEN', 'BOBAEMERALD', 'BOBASAGE', 'BOBAHAZEL', 'BOBAAPPLE', 'BOBAAQUA', 'BOBAFAE', 'BOBAFIELD', 'BOBAIRID',
                     'BOBARUNT']
    red_boba_eyes = ['BOBARED', 'BOBAPURPLE', 'BOBAMAUVE', 'BOBAARID', 'BOBABLOOD', 'BOBAESES', 'BOBAEXILE', 'BOBAFALLSTAR', 'BOBAHOT', 'BOBAKIND',
                    'BOBAMARTI', 'BOBAMEISTER', 'BOBAPELA', 'BOBARETRO', 'BOBASIXER', 'BOBASUN', 'BOBASWEET']
    
    multi_eyes = ['MULTIYELLOW', 'MULTIAMBER', 'MULTIHAZEL', 'MULTIPALEGREEN', 'MULTIGREEN', 'MULTIBLUE', 
                'MULTIDARKBLUE', 'MULTIGREY', 'MULTICYAN', 'MULTIEMERALD', 'MULTIHEATHERBLUE', 'MULTISUNLITICE',
                'MULTICOPPER', 'MULTISAGE', 'MULTICOBALT', 'MULTIPALEBLUE', 'MULTIBRONZE', 'MULTISILVER',
                'MULTIPALEYELLOW', 'MULTIGOLD', 'MULTIGREENYELLOW', 'MULTIRED', 'MULTIPURPLE', 'MULTIMAUVE',
                'MULTIELECTRICBLUE', 'MULTIVIOLET', 'MULTIPINK', 'MULTISNOW',
                'MULTIORANGE', 'MULTICREAM', 'MULTISEAFOAM', 'MULTICRIMSON', 'MULTINAVY',
                'MULTIVOIDGOLD', 'MULTICOOLBROWN', 'MULTIPLUM', 'MULTIINDIGO', 'MULTILILAC',
                'MULTIACROBLUE', 'MULTIACROGREEN', 'MULTIACROGREY', 'MULTIACROINDIGO',
                'MULTIACROAMBER', 'MULTIACROPINK', 'MULTIACRORED', 'MULTIACROTEAL',
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
                'MULTIBROWNTBOI', 'MULTIORANGETBOI', 'MULTIBREDTBOI', 'MULTIREDTBOI',
                'MULTIFIRE', 'MULTIRUBY', 'MULTIRUBYAGAIN', 'MULTIESCAPEE', 'MULTIREFORGED',
                'MULTIFLORAVORE', 'MULTIREJECT', 'MULTIWAYFARER', 'MULTIPISTON',
                'MULTIEXILED', 'MULTITHEIF', 'MULTITHEIFDOS', 'MULTIMORTICIAN', 'MULTISWAMPY',
                'MULTIPORTALMAKER', 'MULTIPURIFIER', 'MULTICORROSOL', 'MULTISEVENSEVEN',
                'MULTIATLAN', 'MULTIBASIC', 'MULTIBELL', 'MULTIBIS', 'MULTIBIT',
                'MULTICRITTER', 'MULTICUBED', 'MULTIDIM', 'MULTIDOE', 'MULTIFREYR',
                'MULTIGAMBLE', 'MULTIGORB', 'MULTIHERO', 'MULTIJANE', 'MULTIJOHN',
                'MULTIMATT', 'MULTIMESS', 'MULTIPE', 'MULTIPOLE', 'MULTIRAT', 'MULTIRGB',
                'MULTIROT', 'MULTISCRATCH', 'MULTISHED', 'MULTISIEGE', 'MULTISPARK',
                'MULTISPARKLE', 'MULTISUNSET', 'MULTITELA', 'MULTIUSURP', 'MULTIWAR',
                'MULTIXIII'
                ]

    # bite scars by @wood pank on discord

    # scars from other cats, other animals
    scars1 = ["ONE", "TWO", "THREE", "FOUR", "TAILSCAR", "SNOUT", "CHEEK", "SIDE", "THROAT", "TAILBASE", "BELLY",
              "LEGBITE", "NECKBITE", "FACE", "MANLEG", "BRIGHTHEART", "MANTAIL", "BRIDGE", "RIGHTBLIND", "LEFTBLIND",
              "BOTHBLIND", "BEAKCHEEK", "BEAKLOWER", "CATBITE", "RATBITE", "QUILLCHUNK", "QUILLSCRATCH", "HINDLEG",
              "BACK", "QUILLSIDE", "SCRATCHSIDE", "BEAKSIDE", "CATBITETWO", "LABRATFACE", "LABRATCHEST", 
              "NEUTRINO", "MANGLEDARM", "DOUBLEBITE", "DANGEROUS", "X-FACE", "VULTURESHOULDER", "CHEEKCUT", "MIROSNOM",
              "SPEARWOUND", "TAIL", "SHOULDER", "EYE", "ARM"]

    # missing parts
    scars2 = ["LEFTEAR", "RIGHTEAR", "NOTAIL", "HALFTAIL", "NOPAW", "NOLEFTEAR", "NORIGHTEAR", "NOEAR"]

    # "special" scars that could only happen in a special event
    scars3 = ["SNAKE", "TOETRAP", "BURNPAWS", "BURNTAIL", "BURNBELLY", "BURNRUMP", "FROSTFACE", "FROSTTAIL",
              "FROSTMITT", "FROSTSOCK", "TOE", "SNAKETWO", "ROTMARKED", "ROTRIDDEN", "TOPSURGERY", "CUTOPEN", 
              "VIVISECTION", "LABRATLIMBS", "HALFFACELEFT", "FULLBODYBURNS", "BESIEGED", "HALFFACERIGHT", 
              "STARBURN", "ARMBURN", "ENVOYCHEST", "EXTRACTIONTWO", "RESTITCHEDUPPER", 
              "RESTITCHEDLOWER", "STITCHEDHEAD", "MESSIAH", "SMOKINGFACE", "BURNTLEG", "BURNTARM", 
              "ARTIRIGHT", "ARTIGLOWRIGHT", "ARTILEFT", "ARTIGLOWLEFT", "PATCHWORK", "BLIZZARDBLAST"]

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
    #sorry sey i was too lazy to make a new sprite sheet 
    muddypaws = [
        "MUDDYPAWS", "WHITECLAWS", "PINKCLAWS", "BLUECLAWS", "GREENCLAWS", "YELLOWCLAWS", "REDCLAWS", "GREYCLAWS"
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
        "EYEPATCH", "INVMOUTH", "MOUSEYELPLUSH", "MOUSEREDPLUSH", "MOUSEBLUEPLUSH", "MOUSEPINKPLUSH"
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
        "TORNCLOAKNIGHT", "TORNCLOAKSHADOW", "TORNCLOAKSILVER", "FAUXMANE",
        "SLEEPYROBEPURPLE", "SLEEPYROBEGREEN", "SLEEPYROBEBLACK", "SLEEPYROBERED",
        "SLEEPYROBEBLUE", "SLEEPYROBEFLOAH", "ITERATORPEARLNECKLACE", "AMBERJEWLERY"
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
        "FALLMPAINT", "SCAVMPAINT", "SPEARMPAINT", "BLUECLOUDS", "RIBS",
        "YELLOWCLOUDS", "PURPLECLOUDS", "PINKCLOUDS", "GOGGLES", "MODSPEAR",
        "PINKPOLEPLANTBUDDY", "ORANGEPOLEPLANTBUDDY", "REDPOLEPLANTBUDDY", "EYEBAGS",
        "MAGNATEJEWLERY", "YELLOWKARMAWREATH", "BLUEKARMAWREATH", "PURPLEKARMAWREATH",
        "MOTHBUDDY", "BOOMERANG", "MOTHBUDDYTWO", "MIST"
    ]
    floatyeyes = [
        "YELLOWFLOATYEYES", "REDFLOATYEYES", "ORANGEFLOATYEYES",
        "LIMEFLOATYEYES", "GREENFLOATYEYES", "BLUEFLOATYEYES",
        "INDIGOFLOATYEYES"
    ]
    morespears = [
        "PURPLEINDIGOPSPEAR", "INDIGOPSPEAR", "PURPLEPSPEAR", "CYANPSPEAR", "BLUEPSPEAR", "BLUECYANPSPEAR",
        "GAYPSPEAR", "TURQUOISEPSPEAR", "TURQUOISEGREENPSPEAR", "LIMEGREENPSPEAR", "LIMEPSPEAR", "GREYPSPEAR",
        "GREENPSPEAR", "ORANGEPSPEAR", "REDPSPEAR", "REDPINKPSPEAR", "PURPLEPINKPSPEAR", "PINKPSPEAR",
        "MAGENTAPINKPSPEAR", "REDPURPLEPSPEAR", "BLUEPURPLEPSPEAR", "ROSEPINKPSPEAR", "GREENYELLOWPSPEAR", "LIMEYELLOWPSPEAR",
        "YELLOWPSPEAR", "REDFIRESPEAR", "ORANGEFIRESPEAR", "YELLOWFIRESPEAR", "PINKFIRESPEAR", "PURPLEFIRESPEAR",
        "DARKREDFIRESPEAR", "DARKPINKFIRESPEAR", "DARKORANGEFIRESPEAR", "DARKYELLOWFIRESPEAR"
        ]
    flagaccs = [
        "BLUEFLAG", "COOLFLAG", "GREENFLAG", "GREYFLAG", "ORANGEFLAG",
        "PINKFLAG", "PURPLEFLAG", "RAINBOWFLAG", "REDFLAG", "SINFLAG",
        "TEALFLAG", "WARMFLAG", "WHITEFLAG", "YELLOWFLAG"
    ]
    haloaccs = [
        "REDHALO", "ORANGEHALO", "YELLOWHALO", "GREENHALO", "TEALHALO",
        "CYANHALO", "INDIGOHALO", "BLUEHALO", "PURPLEHALO", "MAGENTAHALO",
        "PINKHALO", "WHITEHALO", "BLACKHALO"
    ]
    ponchoaccs = [
        "ORANGEPONCHO", "YELLOWPONCHO", "GREENPONCHO", "TEALPONCHO", "CYANPONCHO",
        "BLUEPONCHO", "PURPLEPONCHO", "PINKPONCHO", "REDPONCHO", "WHITEPONCHO",
        "BROWNPONCHO", "SILVERPONCHO", "BLACKPONCHO", "MLOCPONCHO", "VSSCPONCHO",
        "FAMILIARPONCHO", "NSHPONCHO"
    ]
    glassesaccs = [
        "SUNGLASSESPINK", "SUNGLASSESRED", "SUNGLASSESORANGE", "SUNGLASSESAMBER", "SUNGLASSESYELLOW", "SUNGLASSESLIME",
        "SUNGLASSESGREEN", "SUNGLASSESTEAL", "SUNGLASSESCYAN", "SUNGLASSESBLUE", "SUNGLASSESINDIGO", "SUNGLASSESPURPLE",
        "SUNGLASSESWHITE", "SUNGLASSES", "GLASSESRED", "GLASSESORANGE", "GLASSESAMBER", "GLASSESYELLOW",
        "GLASSESLIME", "GLASSESGREEN", "GLASSESTEAL", "GLASSESCYAN", "GLASSESBLUE", "GLASSESINDIGO",
        "GLASSESPURPLE", "GLASSESPINK"
    ]
    orbitals = [
        "ORANGEORBITAL", "YELLOWORBITAL", "EARTHORBITAL",
        "EARTHTWOORBITAL", "PURPLEORBITAL", "PINKORBITAL", 
        "REDORBITAL"
    ]
    vulturemasks = [
        'VULTMASKONE', 'VULTMASKTWO', 'VULTMASK3', 'VULTMASK4', 'VULTMASK5', 'VULTMASK6', 'VULTMASK7', 'VULTMASK8',
        'VULTMASK9', 'VULTMASK10', 'VULTMASK11', 'VULTMASK12', 'VULTMASK13', 'VULTMASK14', 'VULTMASK15', 'VULTMASK16', 
        'VULTMASK17', 'VULTMASK18', 'VULTMASK19', 'VULTMASK20', 'VULTMASK21', 'VULTMASK22', 'VULTMASK23', 'VULTMASK24'
    ]
    iteratormasks = [
        'BLUEITERATOR', 'BLACKITERATOR', 'GREENITERATOR', 'ORANGEITERATOR', 'PINKITERATOR', 'CYANITERATOR',
        'PURPLEITERATOR', 'REDITERATOR', 'CREAMITERATOR', 'WHITEITERATOR', 'YELLOWITERATOR'
    ]
    
    #list for stuff that should logically be behind a long tongue   
    closest_accs = (
        lizards + bodypaint + collars + implant + drapery + 
        pridedrapery + scarves + featherboas + chains + ponchoaccs + morespears + floatyeyes +
        harleyaccs + neckbandanas +
        ["MUDDYPAWS", "CELLIMPLANT", "GOGGLES", "FALLMPAINT", "SCAVMPAINT", "SPEARMPAINT", "EYEBAGS", "MAGNATEJEWLERY", "YELLOWKARMAWREATH", "BLUEKARMAWREATH", "PURPLEKARMAWREATH",
        "MURDERPAINT", "BOGMOSSBLUE", "BOGMOSSGREEN", "BOGMOSSLIME", "ORANGEPLANTPELT", "LIMEPLANTPELT", "GREENPLANTPELT", "YELLOWPLANTPELT", "BLUEPLANTPELT"]
)

    tabbies = [
        "Tabby", "Ticked", "Classic", "Sokoke", "Agouti", "Masked", "Vulture", "Envoy", "Drizzle",
        "Necklace", "Leviathan", "Rotten", "Fire", "Solace", "Swing", "Ice", "Maned", "Sunken", "Daenix",
        "Spooky", "Sworn", "Noble", "Marbled"
    ]
    spotted = [
        "Speckled", "Rosette", "Gravel", "Banana", "Con", "Bengal", "Dreamer", "Oldgrowth", "Cherry",
        "Sparse", "Impish", "Ringed", "Mold", "Apple", "Glitter", "Whale", "Pidgeon", 
        "Watermelon", "Lightecho", "Darkecho", "Salmon", "Plantain", "Malibu", "Clay"
    ]
    plain = [
        "SingleColour", "TwoColour", "Smoke", "Singlestripe", "Collared", "Lizard", "Slimemold",
        "Fluffy", "Yeek", "Rusted", "Leafy", "Scaled", "Countershaded", "Sunset", "Skinny", 
        "Sporty", "Skeleton", "Shred", "Robot", "Lantern"
    ]
    exotic = [
        "Mackerel", "Cyanlizard", "Centipede", "Amoeba", "Seaslug", "Dragonfruit", "Duskdawn", 
        "Seer", "Wolf", "Sparklecat", "Hypnotist", "Fizzy", "Glowing", "Budgie", "Lovebird",
        "Seltzer", "Amazon", "Boba", "Iggy", "Tomo", "Dragonet", "Conure", "Betta", "Patchwork", 
        "Constellation"
    ]
    torties = ["Tortie", "Calico"]
    pelt_categories = [tabbies, spotted, plain, exotic, torties]

    # SPRITE NAMES
    single_colours = [
        'WHITE', 'SKY', 'BLUE', 'INDIGO', 'PURPLE', 'GHOST', 'BLACK', 'CREAM', 'YELLOW',
        'ORANGE', 'SCARLET', 'RED', 'PINK', 'MINT', 'LIME', 'GREEN', 'MAROON', 'PERIWINKLE',
        'LAVENDER'
    ]
    warm_colours = ['YELLOW', 'ORANGE', 'SCARLET', 'RED', 'MAROON']
    black_colours = ['GHOST', 'BLACK']
    white_colours = ['WHITE', 'SKY', 'CREAM', 'PERIWINKLE']
    cool_colours = ['BLUE', 'INDIGO', 'PURPLE', 'MINT', 'LIME', 'GREEN', 'LAVENDER']
    colour_categories = [warm_colours, black_colours, white_colours, cool_colours]
    little_white = [
        'LITTLE', 'LIGHTTUXEDO', 'BUZZARDFANG', 'TIP', 'BLAZE', 'BIB', 'VEE', 'PAWS',
        'BELLY', 'TAILTIP', 'TOES', 'BROKENBLAZE', 'LILTWO', 'SCOURGE', 'TOESTAIL', 'RAVENPAW', 'HONEY',
        'LUNA',
        'EXTRA', 'MUSTACHE', 'REVERSEHEART', 'SPARKLE', 'RIGHTEAR', 'LEFTEAR', 'ESTRELLA', 'REVERSEEYE',
        'BACKSPOT',
        'EYEBAGS', 'LOCKET', 'BLAZEMASK', 'TEARS', 'GLOVE', 'NECK',
        'DOTS', 'FIVEPEBBLE', 'SIAMESE', 'SNOWBELLY',
        'GLOWSTAR', 'STAR', 'DEADPIXEL', 'INSPECTOR', 'FACEDOTS', 'WPTEARS', 'ONEEARTIP', 'NOSETIP',
        'WOLFX', 'GLOWWOLFX', 'TICKEDSPOTS', 'SHREDPATCH', 'TICKEDSTRIPE', 'TICKEDONE', 'BROW',
        'TOPFIN', 'LOWFIN', 'LINE'
        ]
    mid_white = [
        'TUXEDO', 'FANCY', 'UNDERS', 'DAMIEN', 'SKUNK', 'MITAINE', 'SQUEAKS', 'STAR', 'WINGS',
        'DIVA', 'SAVANNAH', 'FADESPOTS', 'BEARD', 'DAPPLEPAW', 'TOPCOVER', 'WOODPECKER', 'MISS', 'BOWTIE',
        'VEST',
        'FADEBELLY', 'DIGIT', 'FCTWO', 'FCONE', 'MIA', 'ROSINA', 'PRINCESS', 'BALLER', 'TREFOIL', 'MANUL',
        'HEAD', 'SPARSE', 'BADGER', 'BELLY', 'MASK', 'LIGHTNING', 'FROSTBITTEN',
        'LIMBS', 'STRIPES', 'SLICE', 'TOONY', 'ACROBAT',
        'DEFIBULATOR', 'WOLFINSIDE', 'TICKEDSPOTSSTRIPE', 'WOLDOUTSIDEONE', 'WOLFFILLONE', 'ECHOBELLY', 'LURE',
        'WATERMELONSEEDS', 'DEEP', 'PLUSHIE', 'SCALETAIL', 'SPARKLING', 'POPPY', 'RISING'
                 ]
    high_white = [
        'ANY', 'ANYTWO', 'BROKEN', 'FRECKLES', 'RINGTAIL', 'HALFFACE', 'PANTSTWO',
        'GOATEE', 'PRINCE', 'FAROFA', 'MISTER', 'PANTS', 'REVERSEPANTS', 'HALFWHITE', 'APPALOOSA', 'PIEBALD',
        'CURVED', 'GLASS', 'MASKMANTLE', 'MAO', 'PAINTED', 'SHIBAINU', 'OWL', 'BUB', 'SPARROW', 'TRIXIE',
        'SAMMY', 'FRONT', 'BLOSSOMSTEP', 'BULLSEYE', 'FINN', 'SCAR', 'BUSTER', 'HAWKBLAZE', 'CAKE',
        'PAINTSPLAT', 'ELDER',
        'REVERSEHEAD', 'HEX', 'SHREDONE', 'SHREDTWO', 'WOLFOUTSIDETWO', 'TICKEDTWO',
        'TICKEDFILLONE', 'TICKEDFILLTWO','TICKEDFILLTHREE', 'SPOOKYBONES', 'WATERMELONWAVE', 'FACEMASK', 'STUFFED',
        'CARBON'
                  ]
    mostly_white = [
        'VAN', 'ONEEAR', 'LIGHTSONG', 'TAIL', 'HEART', 'MOORISH', 'APRON', 'CAPSADDLE',
        'CHESTSPECK', 'BLACKSTAR', 'PETAL', 'HEARTTWO', 'PEBBLESHINE', 'BOOTS', 'COW', 'COWTWO', 'LOVEBUG',
        'SHOOTINGSTAR', 'EYESPOT', 'PEBBLE', 'TAILTWO', 'BUDDY', 'KROPKA',
        'DOUGIE', 'REVERSETEARS', 'REVERSETEARSTWO', 'REVERSENECK', 'ESCAPEE',
        'WOLFFILLTWO', 'TREEFROG', 'RIPPLE'
                    ]
    point_markings = ['COLOURPOINT', 'RAGDOLL', 'SEPIAPOINT', 'MINKPOINT', 'SEALPOINT']
    vit = ['VITILIGO', 'VITILIGOTWO', 'MOON', 'PHANTOM', 'KARPATI', 'POWDER', 'BLEACHED', 'SMOKEY', 'CHARCOAL']
    white_sprites = [little_white, mid_white, high_white, mostly_white, point_markings, vit, 'FULLWHITE']
    
    # Colorized features using inline color lists with with_suffix
    empty = ['BLACK', 'PINK', 'DARKBROWN', 'BROWN', 'LIGHTBROWN', 'DARK', 'DARKGREY', 'GREY', 'DARKSALMON', 'SALMON', 'PEACH', 'DARKMARBLED', 'MARBLED', 'LIGHTMARBLED', 'DARKBLUE', 'BLUE', 'LIGHTBLUE', 'RED']
    claws = ['BLACKCLAWS']
    whiskers = with_suffix(['WHITE', 'BLACK', 'RED', 'YELLOW', 'GREEN', 'BLUE', 'ORANGE', 'BROWN'], 'WHISKERS')
    antennae = with_suffix(['WHITE', 'RED', 'PINK', 'ORANGE', 'YELLOW', 'BLUE', 'GREEN'], 'TENNA')
    sharphorns = with_suffix(['WHITE', 'BLACK', 'RED', 'YELLOW', 'GREEN', 'BLUE', 'ORANGE', 'BROWN'], 'HORNSSHARP')
    ramhorns = Pelt.with_suffix(['WHITE', 'BLACK', 'RED', 'YELLOW', 'GREEN', 'BLUE', 'ORANGE', 'BROWN'], 'HORNSRAM')
    scavhorns = Pelt.with_suffix(['WHITE', 'BLACK', 'RED', 'YELLOW', 'GREEN', 'BLUE', 'ORANGE', 'BROWN'], 'HORNSSCAV')
    elitehorns = Pelt.with_suffix(['WHITE', 'BLACK', 'RED', 'YELLOW', 'GREEN', 'BLUE', 'ORANGE', 'BROWN'], 'HORNSELITE')
    unihorns = Pelt.with_suffix(['WHITE', 'BLACK', 'RED', 'YELLOW', 'GREEN', 'BLUE', 'ORANGE', 'BROWN'], 'HORNSLANCER')
    antlers = ['ANTLERS']
    dragonhorns = Pelt.with_suffix(['WHITE', 'BLACK', 'RED', 'YELLOW', 'GREEN', 'BLUE', 'ORANGE', 'BROWN'], 'HORNSDRAGON')
    tailfrills = Pelt.with_suffix(['BLUE', 'ORANGE', 'GREEN', 'PURPLE', 'PINK', 'RED', 'YELLOW', 'CYAN'], 'TAILFRILLS')
    spikes = Pelt.with_suffix(['YELLOW', 'GREEN', 'AQUA', 'CYAN', 'BLUE', 'PURPLE', 'PINK', 'RED', 'ORANGE'], 'SPIKES')
    seaslugpapillae = ['SEASLUGPAPILLAE']
    thorns = Pelt.with_suffix(['BLACK', 'WHITE'], 'THORNS')
    gills = Pelt.with_suffix(['PINK', 'BLUE', 'RED', 'LIME', 'YELLOW', 'WHITE', 'RAINBOW', 'GRAY', 'HOT', 'COLD'], 'GILLS')
    tongues = Pelt.with_suffix(['FUCHSIA', 'PASTEL', 'KOBI', 'RED', 'GREY', 'ORANGE'], 'TONGUE')
    moth = Pelt.with_suffix(['WHITE', 'BLACK', 'RED', 'YELLOW', 'GREEN', 'BLUE', 'ORANGE', 'BROWN'], 'MOTH')
    glowspots = Pelt.with_suffix(['WHITE', 'RED', 'PINK', 'ORANGE', 'YELLOW', 'BLUE', 'GREEN'], 'GLOWSPOTS')
    lizardneedles = Pelt.with_suffix(['BLACK', 'WHITE', 'RAINBOW'], 'NEEDLES')
    catfishwhiskers = Pelt.with_suffix(['WHITE', 'PINK', 'RED', 'YELLOW', 'GREEN', 'REDYELLOW', 'BLUE', 'PURPLE', 'BLACK', 'BLUEGREEN', 'BLUEPINK', 'BROWN'], 'CATFISHWHISKERS')
    dragonwhiskers = Pelt.with_suffix(['WHITE', 'PINK', 'RED', 'YELLOW', 'GREEN', 'REDYELLOW', 'BLUE', 'PURPLE', 'BLACK', 'BLUEGREEN', 'BLUEPINK', 'BROWN'], 'DRAGONWHISKERS')
    lizardfins = Pelt.with_suffix(['PINK', 'BLUE', 'RED', 'GREEN', 'YELLOW', 'WHITE'], 'FINS')
    anglerfish = ['ANGLERFISH']
    quills = Pelt.with_suffix(['WHITE', 'BLACK'], 'QUILLS')
    centipedegrowths = ['CENTIPEDEGROWTHS']
    tears = ['TEARS']
    spearholes = Pelt.with_suffix(['WHITE', 'BLACK', 'MIX', 'RAINBOW'], 'SPOTS')
    cyanfeatures = Pelt.with_suffix(['WHITE', 'ORANGE', 'BROWN', 'PINK', 'PINKER', 'TEAL', 'GREEN', 'BLOODY', 'LAVENDER', 'PURPLE', 'CYAN', 'BLUE', 'DARKBLUE', 'DARKPURPLE', 'BLACK', 'EGG', 'YELLOW'], 'CYAN')
    cyanwings = ['CYANWINGS']
    firebugpart = ['FIREBUGPART']
    seaangelwings = ['SEAANGELWINGS']
    loach = ['LOACH']
    grasssheepback = ['GRASSSHEEPBACK']
    glassback = ['GLASSBACK']
    familiar = ['FAMILIARMARK']
    acrotail = ['ACROTAIL']
    stinger = Pelt.with_suffix(['BLACK', 'GREY', 'WHITE', 'GOLD'], 'STINGER')
    dropwig = Pelt.with_suffix(['PURPLE', 'GREEN', 'BLUE'], 'DROPWIG')
    manes = Pelt.with_suffix(['DARKBROWN', 'CHOCOLATE', 'GOLDEN', 'BLOND', 'GINGER', 'SILVER'], 'MANE')
    overseertenna = Pelt.with_suffix(['WHITE', 'SKY', 'BLUE', 'INDIGO', 'PURPLE', 'GHOST', 'BLACK', 'CREAM', 'YELLOW', 'ORANGE', 'SCARLET', 'RED', 'PINK', 'MINT', 'LIME', 'GREEN', 'MAROON', 'PERIWINKLE', 'LAVENDER'], 'OVERSEERTENNA')
    budgiewings = Pelt.with_suffix(['WHITE', 'SKY', 'BLUE', 'INDIGO', 'PURPLE', 'GHOST', 'BLACK', 'CREAM', 'YELLOW', 'ORANGE', 'SCARLET', 'RED', 'PINK', 'MINT', 'LIME', 'GREEN', 'MAROON', 'PERIWINKLE', 'LAVENDER'], 'BUDGIEWINGS')
    conurewings = Pelt.with_suffix(['WHITE', 'SKY', 'BLUE', 'INDIGO', 'PURPLE', 'GHOST', 'BLACK', 'CREAM', 'YELLOW', 'ORANGE', 'SCARLET', 'RED', 'PINK', 'MINT', 'LIME', 'GREEN', 'MAROON', 'PERIWINKLE', 'LAVENDER'], 'CONUREWINGS')
    lovebirdwings = Pelt.with_suffix(['WHITE', 'SKY', 'BLUE', 'INDIGO', 'PURPLE', 'GHOST', 'BLACK', 'CREAM', 'YELLOW', 'ORANGE', 'SCARLET', 'RED', 'PINK', 'MINT', 'LIME', 'GREEN', 'MAROON', 'PERIWINKLE', 'LAVENDER'], 'LOVEBIRDWINGS')
    pidgeonwings = Pelt.with_suffix(['WHITE', 'SKY', 'BLUE', 'INDIGO', 'PURPLE', 'GHOST', 'BLACK', 'CREAM', 'YELLOW', 'ORANGE', 'SCARLET', 'RED', 'PINK', 'MINT', 'LIME', 'GREEN', 'MAROON', 'PERIWINKLE', 'LAVENDER'], 'PIDGEONWINGS')
    vulturewings = Pelt.with_suffix(['WHITE', 'SKY', 'BLUE', 'INDIGO', 'PURPLE', 'GHOST', 'BLACK', 'CREAM', 'YELLOW', 'ORANGE', 'SCARLET', 'RED', 'PINK', 'MINT', 'LIME', 'GREEN', 'MAROON', 'PERIWINKLE', 'LAVENDER'], 'VULTUREWINGS')
    colorwings = Pelt.with_suffix(['WATCHER', 'ARTIFICER','HUNTER', 'SAINT', 'RIVULETWINGS', 'SPEARMASTER', 'GOURMAND'], 'WINGS')
    whitefadewings = Pelt.with_suffix(['WHITE','DARKCREAM','CREAM','OFFWHITE','GRAY','PINK','BLACK','POWDERBLUE','SPLASH','PURPLE','BLACKBERRY','SAND','CLAY','BRICK','SALMON','SEAFOAM','MINT','EVERGREEN','CRANBERRY','PEARL','ORCHID','RUBY','CORAL','TAN','LEMON','CLOVER','CYAN','VIOLET','GOLDEN'],'WINGSFADE')
    wings = Pelt.with_suffix(['WHITE','DARKCREAM','CREAM','OFFWHITE','GRAY','PINK','BLACK','POWDERBLUE','SPLASH','PURPLE','BLACKBERRY','SAND','CLAY','BRICK','SALMON','SEAFOAM','MINT','EVERGREEN','CRANBERRY','PEARL','ORCHID','RUBY','CORAL','TAN','LEMON','CLOVER','CYAN','VIOLET','GOLDEN'],'WINGS')
    skin_categories = [dragonhorns, moth, seaslugpapillae, tailfrills, thorns, glowspots, gills, tongues, lizardneedles, 
                       spikes, lizardfins, catfishwhiskers, dragonwhiskers, quills, centipedegrowths, stinger, anglerfish, 
                       spearholes, cyanfeatures, cyanwings, firebugpart, seaangelwings, loach, dropwig, glassback, grasssheepback, 
                       familiar, acrotail, tears, manes, overseertenna, budgiewings, conurewings, lovebirdwings, pidgeonwings, 
                       vulturewings, colorwings, whitefadewings, wings]
    
    #list for stuff that should logically be behind a cloak
    closest_skin = [
        'WHITESPOTS', 'BLACKSPOTS', 'MIXSPOTS', 'RAINBOWSPOTS',
        'WHITEGLOWSPOTS', 'REDGLOWSPOTS', 'PINKGLOWSPOTS', 'ORANGEGLOWSPOTS', 'YELLOWGLOWSPOTS', 'BLUEGLOWSPOTS', 'GREENGLOWSPOTS',
        'WHITECYAN', 'ORANGECYAN', 'BROWNCYAN', 'PINKCYAN', 'PINKERCYAN', 'TEALCYAN', 'GREENCYAN', 'BLOODYCYAN', 'LAVENDERCYAN', 
        'PURPLECYAN', 'CYANCYAN', 'BLUECYAN', 'DARKBLUECYAN', 'DARKPURPLECYAN', 'BLACKCYAN', 'EGGCYAN', 'YELLOWCYAN',
        'PINKFINS', 'BLUEFINS', 'REDFINS', 'GREENFINS', 'YELLOWFINS', 'WHITEFINS',
        'BLACKNEEDLES', 'WHITENEEDLES', 'RAINBOWNEEDLES', 'BLACKTHORNS', 'WHITETHORNS',
        'TEARS', 'SEAANGELWINGS', 'GLASSBACK', 'GRASSSHEEPBACK', 'LOACH', 'FAMILIARMARK'
    ]

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

        if not random.randint(0, riveyenum):
            self.eye_colour = choice(Pelt.riveye_colours)
        elif not random.randint(0, buttoneyenum):
            self.eye_colour = choice(Pelt.buttoneye_colours)
        elif not random.randint(0, bobaeyenum):
            self.eye_colour = choice(Pelt.bobaeye_colours)

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

        # Define look-up dictionaries
        if short:
            renamed_colors = {
                "white": "pale",
                "sky": "blue",
                "indigo": "blue",
                "mint": "green",
                "lime": "green",
                "maroon": "red",
                "periwinkle": "purple",
                "lavender": "purple",
                "ghost": "black"
            }
        else:
            renamed_colors = {
                "white": "pale",
                "sky": "sky",
                "indigo": "indigo",
                "mint": "mint",
                "lime": "lime",
                "maroon": "maroon",
                "periwinkle": "periwinkle",
                "lavender": "lavender",
                "ghost": "black"
            }

        pattern_des = {
            "Tabby": "c_n tabby",
            "Speckled": "speckled c_n",
            "Bengal": "unusually striped c_n",
            "Marbled": "c_n tabby",
            "Ticked": "vivid splotchy c_n",
            "Smoke": "c_n smoke",
            "Mackerel": "c_n tabby",
            "Classic": "c_n tabby",
            "Agouti": "speckled c_n",
            "Singlestripe": "dorsal-striped c_n",
            "Rosette": "unusually spotted c_n",
            "Sokoke": "unusually colored c_n tabby",
            "Masked": "masked c_n smoke",
            'Gravel': 'speckled c_n',
            'Collared': 'c_n collared',
            'Slimemold': 'c_n vivid smoke',
            'Cyanlizard': 'c_n cyan lizard patterned',
            'Vulture': 'masked c_n',
            'Banana': 'dotted c_n',
            'Centipede': 'centipede patterned',
            'Con': 'layered c_n',
            'Lizard': 'c_n lizard patterned',
            'Lantern': 'spotted c_n',
            'Leviathan': 'c_n tabby',
            'Fluffy': 'fluffy c_n',
            'Amoeba': 'c_n amoeba patterned',
            'Seaslug': 'vividly striped c_n',
            'Yeek': 'vividly banded c_n',
            'Rusted': 'c_n smoke',
            'Envoy': 'c_n patchy ticked',
            'Drizzle': 'c_n drizzled',
            'Solace': 'vivid dorsal-striped c_n',
            'Leafy': 'leafy c_n',
            'Scaled': 'scaley c_n',
            'Dragonfruit': 'dragonfruit hued and patterned',
            'Necklace': 'c_n collared',
            'Dreamer': 'c_n smoke',
            'Duskdawn': 'c_n dusky gradient',
            'Seer': 'vividly tipped patchy c_n',
            'Rotten': 'rotted c_n',
            'Fire': 'c_n blotchy tabby',
            'Countershaded': 'patchy c_n',
            'Sunset': 'vivid c_n smoke',
            'Oldgrowth': 'mossy c_n patched',
            'Sparklecat': 'inverted patchy c_n',
            'Wolf': 'rotten patchy c_n',
            'Cherry': 'c_n cyan lizard patterned',
            'Hypnotist': 'hypnotic c_n',
            'Ringed': 'vividly pawed patchy c_n',
            'Skinny': 'masked c_n smoke',
            'Sparse': 'unusually striped c_n collared',
            'Impish': 'c_n impish pattern',
            'Sporty': 'vividly patched c_n',
            'Fizzy': 'glass soda bottle patterned',
            'Skeleton': 'unusually spotted c_n',
            'Shred': 'patchy c_n',
            'Glowing': 'glowy c_n',
            'Mold': 'blotchy c_n',
            'Swing': 'blocky c_n smoke',
            'Lovebird': 'lovebird hued and patterned',
            'Budgie': 'budgie hued and patterned',
            'Amazon': 'neon striped',
            'Apple': 'apple hued and patterned',
            'Boba': 'c_n boba themed',
            'Glitter': 'c_n smoke',
            'Ice': 'c_n striped and speckled',
            'Iggy': 'c_n overseer patterned',
            'Maned': 'c_n striped',
            'Patchwork': 'c_n false calico',
            'Robot': 'robotic c_n',
            'Sunken': 'vibrantly ribbed c_n',
            'Tomo': 'glowy skeleton-patterned c_n',
            'Whale': 'vividly speckled and ticked c_n',
            'Pidgeon': 'speckled and ticked c_n',
            'Watermelon': 'watermelon hued and patterned',
            'Dragonet': 'vivid c_n tabby',
            'Salmon': 'salmon hued and patterned',
            'Lightecho': 'light c_n echo patterned',
            'Darkecho' : 'dark c_n echo patterned',
            'Plantain' : 'banana hued and patterned',
            'Daenix' : 'banded c_n',
            'Seltzer' : 'ticked c_n',
            'Sworn' : 'vividly thin-ringed c_n',
            'Spooky' : 'unusual c_n tabby',
            'Conure' : 'conure hued and patterned',
            'Noble' : 'c_n patchy tabby',
            'Betta' : 'c_n betta patterned',
            'Constellation' : 'c_n star patterned',
            'Malibu' : 'c_n speckled',
            'Clay' : 'patchy c_n smoke',
            'Antethisis': 'vibrant blotchy c_n',
            'Citadel': 'banded c_n',
            'Grave': 'patchily striped c_n',
            'Interloper': 'vibrantly patched c_n',
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
