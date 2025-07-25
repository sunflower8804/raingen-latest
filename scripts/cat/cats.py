"""
Contains the Cat and Personality classes
"""

from __future__ import annotations

import bisect
import itertools
import os.path
import sys
from random import choice, randint, sample, random, getrandbits, randrange
from typing import Dict, List, Any

import ujson  # type: ignore

from scripts.cat.history import History
from scripts.cat.names import Name
from scripts.cat.pelts import Pelt
from scripts.cat.personality import Personality
from scripts.cat.skills import CatSkills
from scripts.cat.thoughts import Thoughts
from scripts.cat_relations.inheritance import Inheritance
from scripts.cat_relations.relationship import Relationship
from scripts.conditions import (
    Illness,
    Injury,
    PermanentCondition,
    get_amount_cat_for_one_medic,
    medical_cats_condition_fulfilled,
)
from scripts.event_class import Single_Event
from scripts.events_module.generate_events import GenerateEvents
from scripts.game_structure import image_cache
from scripts.game_structure.game_essentials import game
from scripts.game_structure.screen_settings import screen
from scripts.housekeeping.datadir import get_save_dir
from scripts.utility import (
    get_alive_status_cats,
    get_personality_compatibility,
    event_text_adjust,
    update_sprite,
    leader_ceremony_text_adjust,
)


class Cat:
    """The cat class."""

    dead_cats = []
    used_screen = screen

    ages = [
        "newborn",
        "kitten",
        "adolescent",
        "young adult",
        "adult",
        "senior adult",
        "senior",
    ]

    age_moons = {
        "newborn": game.config["cat_ages"]["newborn"],
        "kitten": game.config["cat_ages"]["kitten"],
        "adolescent": game.config["cat_ages"]["adolescent"],
        "young adult": game.config["cat_ages"]["young adult"],
        "adult": game.config["cat_ages"]["adult"],
        "senior adult": game.config["cat_ages"]["senior adult"],
        "senior": game.config["cat_ages"]["senior"],
    }

    # This in is in reverse order: top of the list at the bottom
    rank_sort_order = [
        "newborn",
        "kitten",
        "elder",
        "apprentice",
        "warrior",
        "mediator apprentice",
        "mediator",
        "cleric apprentice",
        "cleric",
        "deputy",
        "leader",
    ]

    gender_tags = {"female": "F", "male": "M"}

    # EX levels and ranges.
    # Ranges are inclusive to both bounds
    experience_levels_range = {
        "untrained": (0, 0),
        "trainee": (1, 50),
        "prepared": (51, 110),
        "competent": (110, 170),
        "proficient": (171, 240),
        "expert": (241, 320),
        "master": (321, 321),
    }

    default_pronouns = [
        {
            "subject": "they",
            "object": "them",
            "poss": "their",
            "inposs": "theirs",
            "self": "themself",
            "conju": 1,
        },
        {
            "subject": "she",
            "object": "her",
            "poss": "her",
            "inposs": "hers",
            "self": "herself",
            "conju": 2,
        },
        {
            "subject": "he",
            "object": "him",
            "poss": "his",
            "inposs": "his",
            "self": "himself",
            "conju": 2,
        },
    ]

    all_cats: Dict[str, Cat] = {}  # ID: object
    outside_cats: Dict[str, Cat] = {}  # cats outside the clan
    id_iter = itertools.count()

    all_cats_list: List[Cat] = []
    ordered_cat_list: List[Cat] = []

    grief_strings = {}

    def __init__(
        self,
        prefix=None,
        gender=None,
        status="newborn",
        backstory="clanborn",
        parent1=None,
        parent2=None,
        adoptive_parents=None,
        suffix=None,
        specsuffix_hidden=False,
        ID=None,
        moons=None,
        example=False,
        faded=False,
        skill_dict=None,
        pelt: Pelt = None,
        loading_cat=False,  # Set to true if you are loading a cat at start-up.
        **kwargs,
    ):
        """Initialise the cat.

        :param prefix: Cat's prefix (e.g. Fire- for Fireheart)
        :param gender: Cat's gender, default None
        :param status: Cat's age range, default "newborn"
        :param backstory: Cat's origin, default "clanborn"
        :param parent1: ID of parent 1, default None
        :param parent2: ID of parent 2, default None
        :param suffix: Cat's suffix (e.g. -heart for Fireheart)
        :param specsuffix_hidden: Whether cat has a special suffix (-kit, -paw, etc.), default False
        :param ID: Cat's unique ID, default None
        :param moons: Cat's age, default None
        :param example: If cat is an example cat, default False
        :param faded: If cat is faded, default False
        :param skill_dict: TODO find a good definition for this
        :param pelt: Body details, default None
        :param loading_cat: If loading a cat rather than generating a new one, default False
        :param kwargs: TODO what are the possible args here? ["biome", ]
        """

        self.history = None

        if (
            faded
        ):  # This must be at the top. It's a smaller list of things to init, which is only for faded cats
            self.init_faded(ID, status, prefix, suffix, moons, **kwargs)
            return

        self.generate_events = GenerateEvents()

        # Private attributes
        self._mentor = None  # plz
        self._experience = None
        self._moons = None

        # Public attributes
        self.gender = gender
        self.status = status
        self.backstory = backstory
        self.age = None
        self.skills = CatSkills(skill_dict=skill_dict)
        self.personality = Personality(
            trait="troublesome", lawful=0, aggress=0, stable=0, social=0
        )
        self.parent1 = parent1
        self.parent2 = parent2
        self.adoptive_parents = adoptive_parents if adoptive_parents else []
        self.pelt = pelt if pelt else Pelt()
        self.former_mentor = []
        self.patrol_with_mentor = 0
        self.apprentice = []
        self.former_apprentices = []
        self.relationships = {}
        self.mate = []
        self.previous_mates = []
        self.pronouns = [self.default_pronouns[0].copy()]
        self.placement = None
        self.example = example
        self.dead = False
        self.exiled = False
        self.outside = False
        self.driven_out = False
        self.dead_for = 0  # moons
        self.thought = ""
        self.genderalign = None
        self.birth_cooldown = 0
        self.illnesses = {}
        self.injuries = {}
        self.healed_condition = None
        self.leader_death_heal = None
        self.also_got = False
        self.permanent_condition = {}
        self.df = False
        self.experience_level = None
        self.inventory = []

        # Various behavior toggles
        self.no_kits = False
        self.no_mates = False
        self.no_retire = False

        self.prevent_fading = False  # Prevents a cat from fading

        self.faded_offspring = (
            []
        )  # Stores of a list of faded offspring, for relation tracking purposes

        self.faded = faded  # This is only used to flag cats that are faded, but won't be added to the faded list until
        # the next save.

        self.favourite = False

        self.specsuffix_hidden = specsuffix_hidden
        self.inheritance = None

        self.history = None

        # setting ID
        if ID is None:
            potential_id = str(next(Cat.id_iter))

            if game.clan:
                faded_cats = game.clan.faded_ids
            else:
                faded_cats = []

            while potential_id in self.all_cats or potential_id in faded_cats:
                potential_id = str(next(Cat.id_iter))
            self.ID = potential_id
        else:
            self.ID = ID

        # age and status
        if status is None and moons is None:
            self.age = choice(self.ages)
        elif moons is not None:
            self.moons = moons
            if moons > 300:
                # Out of range, always elder
                self.age = "senior"
            elif moons == 0:
                self.age = "newborn"
            else:
                # In range
                for key_age in self.age_moons.keys():
                    if moons in range(
                        self.age_moons[key_age][0], self.age_moons[key_age][1] + 1
                    ):
                        self.age = key_age
        else:
            if status == "newborn":
                self.age = "newborn"
            elif status == "kitten":
                self.age = "kitten"
            elif status == "elder":
                self.age = "senior"
            elif status in [
                "apprentice",
                "mediator apprentice",
                "cleric apprentice",
            ]:
                self.age = "adolescent"
            else:
                self.age = choice(["young adult", "adult", "adult", "senior adult"])
            self.moons = randint(
                self.age_moons[self.age][0], self.age_moons[self.age][1]
            )

        # backstory
        if self.backstory is None:
            self.backstory = "clanborn"
        else:
            self.backstory = self.backstory

        # sex!?!??!?!?!??!?!?!?!??
        if self.gender is None:
            self.gender = choice(["female", "male"])
        self.g_tag = self.gender_tags[self.gender]

        """if self.genderalign == "":
            self.genderalign = self.gender"""

        # These things should only run when generating a new cat, rather than loading one in.
        if not loading_cat:
            self.init_generate_cat(skill_dict)

        # In camp status
        self.in_camp = 1
        if "biome" in kwargs:
            biome = kwargs["biome"]
        elif game.clan is not None:
            biome = game.clan.biome
        else:
            biome = None
        # NAME
        # load_existing_name is needed so existing cats don't get their names changed/fixed for no reason
        if self.pelt is not None:
            self.name = Name(
                prefix,
                suffix,
                biome=biome,
                specsuffix_hidden=self.specsuffix_hidden,
                load_existing_name=loading_cat,
                cat=self,
            )
        else:
            self.name = Name(
                status,
                prefix,
                suffix,
                specsuffix_hidden=self.specsuffix_hidden,
                load_existing_name=loading_cat,
                cat=self,
            )

        # Private Sprite
        self._sprite = None

        # SAVE CAT INTO ALL_CATS DICTIONARY IN CATS-CLASS
        self.all_cats[self.ID] = self

        if self.ID not in ["0", None]:
            Cat.insert_cat(self)

    def init_faded(self, ID, status, prefix, suffix, moons, **kwargs):
        """Perform faded-specific initialization

        :param ID: Cat ID
        :param status: Cat status
        :param prefix: Cat's prefix
        :param suffix: Cat's suffix
        :param moons: Age in moons
        :param kwargs:

        :return: None
        """
        self.ID = ID
        self.parent1 = None
        self.parent2 = None
        self.adoptive_parents = []
        self.mate = []
        self.status = status
        self.pronouns = []  # Needs to be set as a list
        self.moons = moons
        self.dead_for = 0
        self.dead = True
        self.outside = False
        self.exiled = False
        self.inheritance = None  # This should never be used, but just for safety
        self.name = Name(prefix=prefix, suffix=suffix, cat=self)
        if "df" in kwargs:
            self.df = kwargs["df"]
        else:
            self.df = False

        self.init_moons_age(moons)

        self.set_faded()  # Sets the faded sprite and faded tag (self.faded = True)
        return True

    def init_moons_age(self, moons):
        """
        Gets the correct life stage for associated moons

        :param moons: Age in moons
        :return: None
        """
        if moons > 300:
            # Out of range, always elder
            self.age = "senior"
        elif moons == 0:
            self.age = "newborn"
        else:
            # In range
            for key_age in self.age_moons.keys():
                if moons in range(
                    self.age_moons[key_age][0], self.age_moons[key_age][1] + 1
                ):
                    self.age = key_age

    def init_generate_cat(self, skill_dict):
        """
        Used to roll a new cat
        :param skill_dict: TODO what is a skill dict exactly
        :return: None
        """
        # trans cat chances
        theythemdefault = game.settings["they them default"]
        self.genderalign = self.gender
        trans_chance = randint(0, 50)
        nb_chance = randint(0, 75)

        # GENDER IDENTITY
        if self.age in ["kitten", "newborn"]:
            # newborns can't be trans, sorry babies
            pass
        elif nb_chance == 1:
            self.genderalign = "nonbinary"
        elif trans_chance == 1:
            if self.gender == "female":
                self.genderalign = "trans male"
            else:
                self.genderalign = "trans female"

        # PRONOUNS
        if theythemdefault is True:
            self.pronouns = [self.default_pronouns[0].copy()]
        else:
            # Assigning pronouns based on gender
            if self.genderalign in ["female", "trans female"]:
                self.pronouns = [self.default_pronouns[1].copy()]
            elif self.genderalign in ["male", "trans male"]:
                self.pronouns = [self.default_pronouns[2].copy()]
            else:
                self.genderalign = "nonbinary"
                self.pronouns = [self.default_pronouns[0].copy()]

        # APPEARANCE
        self.pelt = Pelt.generate_new_pelt(
            self.gender,
            [Cat.fetch_cat(i) for i in (self.parent1, self.parent2) if i],
            self.age,
        )

        # Personality
        self.personality = Personality(kit_trait=self.is_baby())

        # experience and current patrol status
        if self.age in ["young", "newborn"]:
            self.experience = 0
        elif self.age in ["adolescent"]:
            m = self.moons
            self.experience = 0
            while m > Cat.age_moons["adolescent"][0]:
                ran = game.config["graduation"]["base_app_timeskip_ex"]
                exp = choice(
                    list(range(ran[0][0], ran[0][1] + 1))
                    + list(range(ran[1][0], ran[1][1] + 1))
                )
                self.experience += exp + 3
                m -= 1
        elif self.age in ["young adult", "adult"]:
            self.experience = randint(
                Cat.experience_levels_range["prepared"][0],
                Cat.experience_levels_range["proficient"][1],
            )
        elif self.age in ["senior adult"]:
            self.experience = randint(
                Cat.experience_levels_range["competent"][0],
                Cat.experience_levels_range["expert"][1],
            )
        elif self.age in ["senior"]:
            self.experience = randint(
                Cat.experience_levels_range["competent"][0],
                Cat.experience_levels_range["master"][1],
            )
        else:
            self.experience = 0

        if not skill_dict:
            self.skills = CatSkills.generate_new_catskills(self.status, self.moons)

    def __repr__(self):
        return "CAT OBJECT:" + self.ID

    def __eq__(self, other):
        return False if not isinstance(other, Cat) else self.ID == other.ID

    def __hash__(self):
        return hash(self.ID)

    @property
    def mentor(self):
        """Return managed attribute '_mentor', which is the ID of the cat's mentor."""
        return self._mentor

    @mentor.setter
    def mentor(self, mentor_id: Any):
        """Makes sure `Cat.mentor` can only be None (no mentor) or a string (mentor ID)."""
        if mentor_id is None or isinstance(mentor_id, str):
            self._mentor = mentor_id
        else:
            print(
                f"Mentor ID {mentor_id} of type {type(mentor_id)} isn't valid :("
                "\nCat.mentor has to be either None (no mentor) or the mentor's ID as a string."
            )

    def is_alive(self):
        """Check if this cat is alive

        :return: True if alive, False if dead
        """
        return not self.dead

    def die(self, body: bool = True):
        """Kills cat.

        body - defaults to True, use this to mark if the body was recovered so
        that grief messages will align with body status
        - if it is None, a lost cat died and therefore not trigger grief, since the clan does not know
        """
        if (
            self.status == "leader"
            and "pregnant" in self.injuries
            and game.clan.leader_lives > 0
        ):
            self.illnesses.clear()

            self.injuries = {
                key: value
                for (key, value) in self.injuries.items()
                if key == "pregnant"
            }
        else:
            self.injuries.clear()
            self.illnesses.clear()

        # Deal with leader death
        text = ""
        darkforest = game.clan.instructor.df
        isoutside = self.outside
        if self.status == "leader":
            if game.clan.leader_lives > 0:
                lives_left = game.clan.leader_lives
                death_thought = Thoughts.leader_death_thought(
                    self, lives_left, darkforest
                )
                final_thought = event_text_adjust(self, death_thought, main_cat=self)
                self.thought = final_thought
                return ""
            elif game.clan.leader_lives <= 0:
                self.dead = True
                game.just_died.append(self.ID)
                game.clan.leader_lives = 0
                death_thought = Thoughts.leader_death_thought(self, 0, darkforest)
                final_thought = event_text_adjust(self, death_thought, main_cat=self)
                self.thought = final_thought
                if game.clan.instructor.df is False:
                    text = (
                        "They've lost their last life and have travelled to the Void."
                    )
                else:
                    text = "They've lost their last life and have travelled to the RotWound."
        else:
            self.dead = True
            game.just_died.append(self.ID)
            death_thought = Thoughts.new_death_thought(self, darkforest, isoutside)
            final_thought = event_text_adjust(self, death_thought, main_cat=self)
            self.thought = final_thought

        for app in self.apprentice.copy():
            fetched_cat = Cat.fetch_cat(app)
            if fetched_cat:
                fetched_cat.update_mentor()
        self.update_mentor()

        # if game.clan and game.clan.game_mode != 'classic' and not (self.outside or self.exiled) and body is not None:
        if game.clan and not self.outside and not self.exiled:
            self.grief(body)

        if not self.outside:
            Cat.dead_cats.append(self)
            if game.clan.instructor.df is False:
                self.df = False
                game.clan.add_to_starclan(self)
            elif game.clan.instructor.df is True:
                self.df = True
                game.clan.add_to_darkforest(self)
        else:
            game.clan.add_to_unknown(self)

        return

    def exile(self):
        """This is used to send a cat into exile. This removes the cat's status and gives them a special 'exiled'
        status."""
        self.exiled = True
        self.outside = True
        self.status = "exiled"
        if self.personality.trait == "vengeful":
            self.thought = "Swears their revenge for being exiled"
        else:
            self.thought = "Is shocked that they have been exiled"
        for app in self.apprentice:
            fetched_cat = Cat.fetch_cat(app)
            if fetched_cat:
                fetched_cat.update_mentor()
        self.update_mentor()

    def grief(self, body: bool):
        """
        compiles grief moon event text
        """
        if body:
            body_status = "body"
        else:
            body_status = "no_body"

        # Keep track is the body was treated with rosemary.
        body_treated = False
        text = None

        # apply grief to cats with high positive relationships to dead cat
        for cat in Cat.all_cats.values():
            if cat.dead or cat.outside or cat.moons < 1:
                continue

            to_self = cat.relationships.get(self.ID)
            if not isinstance(to_self, Relationship):
                continue

            family_relation = self.familial_grief(living_cat=cat)
            very_high_values = []
            high_values = []

            if to_self.romantic_love > 55:
                very_high_values.append("romantic")
            if to_self.romantic_love > 40:
                high_values.append("romantic")

            if to_self.platonic_like > 50:
                very_high_values.append("platonic")
            if to_self.platonic_like > 30:
                high_values.append("platonic")

            if to_self.admiration > 70:
                very_high_values.append("admiration")
            if to_self.admiration > 50:
                high_values.append("admiration")

            if to_self.comfortable > 60:
                very_high_values.append("comfort")
            if to_self.comfortable > 40:
                high_values.append("comfort")

            if to_self.trust > 70:
                very_high_values.append("trust")
            if to_self.trust > 50:
                high_values.append("trust")

            major_chance = 0
            if very_high_values:
                # major grief eligible cats.

                major_chance = 3
                if cat.personality.stability < 5:
                    major_chance -= 1

                # decrease major grief chance if grave herbs are used
                if body and not body_treated and "rosemary" in game.clan.herbs:
                    body_treated = True
                    game.clan.herbs["rosemary"] -= 1
                    if game.clan.herbs["rosemary"] <= 0:
                        game.clan.herbs.pop("rosemary")
                    game.herb_events_list.append(
                        f"Rosemary was used for {self.name}'s body."
                    )

                if body_treated:
                    major_chance -= 1

            # If major_chance is not 0, there is a chance for major grief
            grief_type = None
            if major_chance and not int(random() * major_chance):
                grief_type = "major"

                possible_strings = []
                for x in very_high_values:
                    possible_strings.extend(
                        self.generate_events.possible_death_reactions(
                            family_relation, x, cat.personality.trait, body_status
                        )
                    )

                if not possible_strings:
                    print("No grief strings")
                    continue

                text = choice(possible_strings)
                text += " " + choice(MINOR_MAJOR_REACTION["major"])
                text = event_text_adjust(Cat, text=text, main_cat=self, random_cat=cat)

                cat.get_ill("grief stricken", event_triggered=True, severity="major")

            # If major grief fails, but there are still very_high or high values,
            # it can fail to to minor grief. If they have a family relation, bypass the roll.
            elif (very_high_values or high_values) and (
                family_relation != "general" or not int(random() * 5)
            ):
                grief_type = "minor"

                # These minor grief message will be applied as thoughts.
                minor_grief_messages = (
                    "Told a fond story at r_c's vigil",
                    "Bargains with the Ascended, begging them to send r_c back",
                    "Sat all night at r_c's vigil",
                    "Will never forget r_c",
                    "Prays that r_c is safe in the Void",
                    "Misses the warmth that r_c brought to {PRONOUN/m_c/poss} life",
                    "Is mourning r_c",
                    "Can't stop coming to tears each time r_c is mentioned",
                    "Stayed the longest at r_c's vigil",
                    "Left r_c's vigil early due to grief",
                    "Lashes out at any slugcat who checks on {PRONOUN/m_c/object} after r_c's death",
                    "Took a long walk on {PRONOUN/m_c/poss} own to mourn r_c in private",
                    "Is busying {PRONOUN/m_c/self} with too much work to forget about r_c's death",
                    "Does {PRONOUN/m_c/poss} best to console {PRONOUN/m_c/poss} clanmates about r_c's death",
                    "Takes a part of r_c's nest to put with {PRONOUN/m_c/poss} own, clinging to the fading scent",
                    "Sleeps in r_c's nest tonight",
                    "Defensively states that {PRONOUN/m_c/subject} {VERB/m_c/don't/doesn't} need any comfort about r_c's death",
                    "Wonders why the Void had to take r_c so soon",
                    "Still needs r_c even though they're gone",
                    "Doesn't think {PRONOUN/m_c/subject} will ever be the same without r_c",
                    "Was seen crying in {PRONOUN/m_c/poss} nest after r_c's vigil",
                    "Is hiding {PRONOUN/m_c/poss} tears as {PRONOUN/m_c/subject} {VERB/m_c/comfort/comforts} the others about r_c's passing",
                )

                if body:
                    minor_grief_messages += (
                        "Helped bury r_c, leaving {PRONOUN/r_c/poss} favorite prey at the grave",
                        "Slips out of camp to visit r_c's grave",
                        "Clung so desperately to r_c's body that {PRONOUN/m_c/subject} had to be dragged away",
                        "Hides a scrap of r_c's fur under {PRONOUN/m_c/poss} nest to cling to",
                        "Can't stand the sight of r_c's body in camp",
                        "Hissed at anyone who got too close to r_c's body, refusing to let go",
                        "Spent a long time grooming r_c's fur for their vigil",
                        "Arranged the flowers for r_c's vigil",
                        "Picked the best spot in the burial grounds for r_c",
                        "Keeps thinking that r_c is only sleeping",
                        "Is in denial of r_c's death, despite the ongoing vigil",
                        "Insists that r_c isn't gone",
                        "Begs r_c not to leave them all",
                        "Sleeps next to r_c for the entire vigil one last time",
                        "Ran out of camp the moment {PRONOUN/m_c/subject} saw r_c's body",
                        "Sang a song in memory of r_c at the vigil",
                        "Stares at r_c's vigil longingly, but doesn't feel the right to join in",
                    )

                text = choice(minor_grief_messages)

            if grief_type:
                # Generate the event:
                if cat.ID not in Cat.grief_strings:
                    Cat.grief_strings[cat.ID] = []

                Cat.grief_strings[cat.ID].append((text, (self.ID, cat.ID), grief_type))
                continue

            # Negative "grief" messages are just for flavor.
            high_values = []
            very_high_values = []
            if to_self.dislike > 50:
                high_values.append("dislike")

            if to_self.jealousy > 50:
                high_values.append("jealousy")

            if high_values:
                # Generate the event:
                possible_strings = []
                for x in high_values:
                    possible_strings.extend(
                        self.generate_events.possible_death_reactions(
                            family_relation, x, cat.personality.trait, body_status
                        )
                    )

                text = event_text_adjust(
                    Cat, choice(possible_strings), main_cat=self, random_cat=cat
                )
                if cat.ID not in Cat.grief_strings:
                    Cat.grief_strings[cat.ID] = []

                Cat.grief_strings[cat.ID].append((text, (self.ID, cat.ID), "negative"))

    def familial_grief(self, living_cat: Cat):
        """
        returns relevant grief strings for family members, if no relevant strings then returns None
        """
        dead_cat = self

        if dead_cat.is_parent(living_cat):
            return "child"
        elif living_cat.is_parent(dead_cat):
            return "parent"
        elif dead_cat.is_sibling(living_cat):
            return "sibling"
        else:
            return "general"

    def gone(self):
        """Makes a Clan cat an "outside" cat. Handles removing them from special positions, and removing
        mentors and apprentices."""
        self.outside = True

        if self.status in ["leader", "warrior"]:
            self.status_change("warrior")

        for app in self.apprentice.copy():
            app_ob = Cat.fetch_cat(app)
            if app_ob:
                app_ob.update_mentor()
        self.update_mentor()
        for x in self.apprentice:
            Cat.fetch_cat(x).update_mentor()
        game.clan.add_to_outside(self)

    def add_to_clan(self) -> list:
        """Makes an "outside cat" a Clan cat. Returns a list of IDs for any additional cats that
        are coming with them."""
        self.outside = False
        if not self.exiled:
            History.add_beginning(self)
        self.exiled = False
        game.clan.add_to_clan(self)

        # check if there are kits under 12 moons with this cat and also add them to the clan
        children = self.get_children()
        ids = []
        for child_id in children:
            child = Cat.all_cats[child_id]
            if (
                child.outside
                and not child.exiled
                and not child.dead
                and child.moons < 12
            ):
                child.add_to_clan()
                History.add_beginning(child)
                ids.append(child_id)

        return ids

    def status_change(self, new_status, resort=False):
        """Changes the status of a cat. Additional functions are needed if you want to make a cat a leader or deputy.
        new_status = The new status of a cat. Can be 'apprentice', 'cleric apprentice', 'warrior'
                    'cleric', 'elder'.
        resort = If sorting type is 'rank', and resort is True, it will resort the cat list. This should
                only be true for non-timeskip status changes."""
        old_status = self.status
        self.status = new_status
        self.name.status = new_status

        self.update_mentor()
        for app in self.apprentice.copy():
            fetched_cat = Cat.fetch_cat(app)
            if isinstance(fetched_cat, Cat):
                fetched_cat.update_mentor()

        # If they have any apprentices, make sure they are still valid:
        if old_status == "cleric":
            game.clan.remove_med_cat(self)

        # updates mentors
        if self.status == "apprentice":
            pass

        elif self.status == "cleric apprentice":
            pass

        elif self.status == "warrior":
            if old_status == "leader" and (
                game.clan.leader and game.clan.leader.ID == self.ID
            ):
                game.clan.leader = None
                game.clan.leader_predecessors += 1
            if game.clan and game.clan.deputy and game.clan.deputy.ID == self.ID:
                game.clan.deputy = None
                game.clan.deputy_predecessors += 1

        elif self.status == "cleric":
            if game.clan is not None:
                game.clan.new_medicine_cat(self)

        elif self.status == "elder":
            if (
                old_status == "leader"
                and game.clan.leader
                and game.clan.leader.ID == self.ID
            ):
                game.clan.leader = None
                game.clan.leader_predecessors += 1

            if game.clan.deputy and game.clan.deputy.ID == self.ID:
                game.clan.deputy = None
                game.clan.deputy_predecessors += 1

        elif self.status == "mediator":
            pass

        elif self.status == "mediator apprentice":
            pass

        # update class dictionary
        self.all_cats[self.ID] = self

        # If we have it sorted by rank, we also need to re-sort
        if game.sort_type == "rank" and resort:
            Cat.sort_cats()

    def rank_change_traits_skill(self, mentor):
        """Updates trait and skill upon ceremony"""

        if self.status in ["warrior", "cleric", "mediator"]:
            # Give a couple doses of mentor influence:
            if mentor:
                max_influence = randint(0, 2)
                i = 0
                while max_influence > i:
                    i += 1
                    affect_personality = self.personality.mentor_influence(
                        Cat.fetch_cat(mentor).personality
                    )
                    affect_skills = self.skills.mentor_influence(Cat.fetch_cat(mentor))
                    if affect_personality:
                        History.add_facet_mentor_influence(
                            self,
                            mentor.ID,
                            affect_personality[0],
                            affect_personality[1],
                        )
                    if affect_skills:
                        History.add_skill_mentor_influence(
                            self, affect_skills[0], affect_skills[1], affect_skills[2]
                        )

            History.add_mentor_skill_influence_strings(self)
            History.add_mentor_facet_influence_strings(self)
        return

    def manage_outside_trait(self):
        """To be run every moon on outside cats
        to keep trait and skills making sense."""
        if not (self.outside or self.exiled):
            return

        self.personality.set_kit(self.is_baby())  # Update kit trait stuff

    def describe_cat(self, short=False):
        """Generates a string describing the cat's appearance and gender.

        :param short: Whether to truncate the output, default False
        :type short: bool
        """
        output = Pelt.describe_appearance(self, short)
        # Add "a" or "an"
        output = f"an {output}" if output[0].lower() in "aeiou" else f"a {output}"
        return output

    def describe_eyes(self):
        """Get a human-readable description of this cat's eye colour"""
        colour = str(self.pelt.eye_colour).lower()
        colour2 = str(self.pelt.eye_colour2).lower()

        if colour == "palegreen":
            colour = "pale green"
        elif colour == "darkblue":
            colour = "dark blue"
        elif colour == "paleblue":
            colour = "pale blue"
        elif colour == "paleyellow":
            colour = "pale yellow"
        elif colour == "heatherblue":
            colour = "heather blue"
        elif colour == "blue2":
            colour = "blue"
        elif colour == "sunlitice":
            colour = "sunlit ice"
        elif colour == "greenyellow":
            colour = "green-yellow"

        if self.pelt.eye_colour in Pelt.riveye_colours:
            colour = colour.replace("riv", "")
        if self.pelt.eye_colour in Pelt.buttoneye_colours:
            colour = colour.replace("button", "")
        if self.pelt.eye_colour in Pelt.bobaeye_colours:
            colour = colour.replace("boba", "")
            
        if self.pelt.eye_colour2:
            if self.pelt.eye_colour2 in Pelt.multi_eyes:
                colour = colour + ", multi-eyed"
            else:
                if self.pelt.eye_colour2 in Pelt.riveye_colours:
                    colour2 = colour2.replace("riv", "")
                if self.pelt.eye_colour2 in Pelt.buttoneye_colours:
                    colour2 = colour2.replace("button", "")
                if self.pelt.eye_colour2 in Pelt.bobaeye_colours:
                    colour2 = colour2.replace("boba", "")
                if colour2 == "palegreen":
                    colour2 = "pale green"
                if colour2 == "darkblue":
                    colour2 = "dark blue"
                if colour2 == "paleblue":
                    colour2 = "pale blue"
                if colour2 == "paleyellow":
                    colour2 = "pale yellow"
                if colour2 == "heatherblue":
                    colour2 = "heather blue"
                if colour2 == "sunlitice":
                    colour2 = "sunlit ice"
                if colour2 == "greenyellow":
                    colour2 = "green-yellow"
                colour = f"{colour} and {colour2}"

        if self.pelt.eye_colour in Pelt.riveye_colours:
            colour = colour + ", huge"
        if self.pelt.eye_colour in Pelt.buttoneye_colours:
            colour = colour + " buttons"
        if self.pelt.eye_colour in Pelt.bobaeye_colours:
            colour = colour + ", large"

        return colour

    def convert_history(self, died_by, scar_events):
        """
        Handle old history save conversions
        """
        deaths = []
        if died_by:
            deaths.extend(
                {"involved": None, "text": death, "moon": "?"} for death in died_by
            )
        scars = []
        if scar_events:
            scars.extend(
                {"involved": None, "text": scar, "moon": "?"} for scar in scar_events
            )
        self.history = History(
            died_by=deaths,
            scar_events=scars,
        )

    def load_history(self):
        """Load this cat's history"""
        try:
            if game.switches["clan_name"] != "":
                clanname = game.switches["clan_name"]
            else:
                clanname = game.switches["clan_list"][0]
        except IndexError:
            print("WARNING: History failed to load, no Clan in game.switches?")
            return

        history_directory = f"{get_save_dir()}/{clanname}/history/"
        cat_history_directory = history_directory + self.ID + "_history.json"

        if not os.path.exists(cat_history_directory):
            self.history = History(
                beginning={},
                mentor_influence={},
                app_ceremony={},
                lead_ceremony=None,
                possible_history={},
                died_by=[],
                scar_events=[],
                murder={},
            )
            return
        try:
            with open(cat_history_directory, "r", encoding="utf-8") as read_file:
                history_data = ujson.loads(read_file.read())
                self.history = History(
                    beginning=(
                        history_data["beginning"] if "beginning" in history_data else {}
                    ),
                    mentor_influence=(
                        history_data["mentor_influence"]
                        if "mentor_influence" in history_data
                        else {}
                    ),
                    app_ceremony=(
                        history_data["app_ceremony"]
                        if "app_ceremony" in history_data
                        else {}
                    ),
                    lead_ceremony=(
                        history_data["lead_ceremony"]
                        if "lead_ceremony" in history_data
                        else None
                    ),
                    possible_history=(
                        history_data["possible_history"]
                        if "possible_history" in history_data
                        else {}
                    ),
                    died_by=(
                        history_data["died_by"] if "died_by" in history_data else []
                    ),
                    scar_events=(
                        history_data["scar_events"]
                        if "scar_events" in history_data
                        else []
                    ),
                    murder=history_data["murder"] if "murder" in history_data else {},
                )
        except Exception:
            self.history = None
            print(
                f"WARNING: There was an error reading the history file of cat #{self} or their history file was "
                f"empty. Default history info was given. Close game without saving if you have save information "
                f"you'd like to preserve!"
            )

    def save_history(self, history_dir):
        """Save this cat's history.

        :param history_dir: Directory to save cat's history to
        :type history_dir: str
        """
        if not os.path.exists(history_dir):
            os.makedirs(history_dir)

        history_dict = History.make_dict(self)
        try:
            game.safe_save(f"{history_dir}/{self.ID}_history.json", history_dict)
        except:
            self.history = History(
                beginning={},
                mentor_influence={},
                app_ceremony={},
                lead_ceremony=None,
                possible_history={},
                died_by=[],
                scar_events=[],
                murder={},
            )

            print(f"WARNING: saving history of cat #{self.ID} didn't work")

    def generate_lead_ceremony(self):
        """Create a leader ceremony and add it to the history"""

        # determine which dict we're pulling from
        if game.clan.instructor.df:
            starclan = False
            ceremony_dict = LEAD_CEREMONY_DF
        else:
            starclan = True
            ceremony_dict = LEAD_CEREMONY_SC

        # ---------------------------------------------------------------------------- #
        #                                    INTRO                                     #
        # ---------------------------------------------------------------------------- #
        all_intros = ceremony_dict["intros"]

        # filter the intros
        possible_intros = []
        for intro in all_intros:
            tags = all_intros[intro]["tags"]

            if game.clan.age != 0 and "new_clan" in tags:
                continue
            elif game.clan.age == 0 and "new_clan" not in tags:
                continue

            if (
                all_intros[intro]["lead_trait"]
                and self.personality.trait not in all_intros[intro]["lead_trait"]
            ):
                continue
            possible_intros.append(all_intros[intro])

        if chosen_intro := choice(possible_intros):
            intro = choice(chosen_intro["text"])
            intro = leader_ceremony_text_adjust(
                Cat,
                intro,
                self,
            )
        else:
            intro = "this should not appear"

        # ---------------------------------------------------------------------------- #
        #                                 LIFE GIVING                                  #
        # ---------------------------------------------------------------------------- #
        life_givers = []
        dead_relations = []
        life_giving_leader = None

        # grab life givers that the cat actually knew in life and sort by amount of relationship!
        relationships = self.relationships.values()

        for rel in relationships:
            kitty = self.fetch_cat(rel.cat_to)
            if kitty and kitty.dead and kitty.status != "newborn":
                # check where they reside
                if starclan:
                    if kitty.ID not in game.clan.starclan_cats:
                        continue
                else:
                    if kitty.ID not in game.clan.darkforest_cats:
                        continue
                # guides aren't allowed here
                if kitty == game.clan.instructor:
                    continue
                else:
                    dead_relations.append(rel)

        # sort relations by the strength of their relationship
        dead_relations.sort(
            key=lambda rel: rel.romantic_love
            + rel.platonic_like
            + rel.admiration
            + rel.comfortable
            + rel.trust,
            reverse=True,
        )

        # if we have relations, then make sure we only take the top 8
        if dead_relations:
            i = 0
            for rel in dead_relations:
                if i == 8:
                    break
                if rel.cat_to.status == "leader":
                    life_giving_leader = rel.cat_to
                    continue
                life_givers.append(rel.cat_to.ID)
                i += 1
        # check amount of life givers, if we need more, then grab from the other dead cats
        if len(life_givers) < 8:
            amount = 8 - len(life_givers)

            if starclan:
                # this part just checks how many SC cats are available, if there aren't enough to fill all the slots,
                # then we just take however many are available

                possible_sc_cats = [
                    i
                    for i in game.clan.starclan_cats
                    if self.fetch_cat(i)
                    and i not in life_givers
                    and self.fetch_cat(i).status not in ["leader", "newborn"]
                ]

                if len(possible_sc_cats) - 1 < amount:
                    extra_givers = possible_sc_cats
                else:
                    extra_givers = sample(possible_sc_cats, k=amount)
            else:
                possible_df_cats = [
                    i
                    for i in game.clan.darkforest_cats
                    if self.fetch_cat(i)
                    and i not in life_givers
                    and self.fetch_cat(i).status not in ["leader", "newborn"]
                ]
                if len(possible_df_cats) - 1 < amount:
                    extra_givers = possible_df_cats
                else:
                    extra_givers = sample(possible_df_cats, k=amount)

            life_givers.extend(extra_givers)

        # making sure we have a leader at the end
        ancient_leader = False
        if not life_giving_leader:
            # choosing if the life giving leader will be the oldest leader or previous leader
            coin_flip = randint(1, 2)
            if coin_flip == 1:
                # pick the oldest leader in SC
                ancient_leader = True
                if starclan:
                    sc_cats = game.clan.starclan_cats.copy()
                    sc_cats.sort(key=lambda x: -1 * int(Cat.fetch_cat(x).dead_for))
                    for kitty in sc_cats:
                        if (
                            self.fetch_cat(kitty)
                            and self.fetch_cat(kitty).status == "leader"
                        ):
                            life_giving_leader = kitty
                            break
                else:
                    df_kitties = game.clan.darkforest_cats.copy()
                    df_kitties.sort(key=lambda x: -1 * int(Cat.fetch_cat(x).dead_for))
                    for kitty in df_kitties:
                        if (
                            self.fetch_cat(kitty)
                            and self.fetch_cat(kitty).status == "leader"
                        ):
                            life_giving_leader = kitty
                            break
            else:
                # pick previous leader
                if starclan:
                    sc_cats = game.clan.starclan_cats.copy()
                    sc_cats.sort(key=lambda x: int(Cat.fetch_cat(x).dead_for))
                    for kitty in sc_cats:
                        if (
                            self.fetch_cat(kitty)
                            and self.fetch_cat(kitty).status == "leader"
                        ):
                            life_giving_leader = kitty
                            break
                else:
                    df_kitties = game.clan.darkforest_cats.copy()
                    df_kitties.sort(key=lambda x: int(Cat.fetch_cat(x).dead_for))
                    for kitty in df_kitties:
                        if (
                            self.fetch_cat(kitty)
                            and self.fetch_cat(kitty).status == "leader"
                        ):
                            life_giving_leader = kitty
                            break

        if life_giving_leader:
            life_givers.append(life_giving_leader)

        # check amount again, if more are needed then we'll add the ghost-y cats at the end
        if len(life_givers) < 9:
            unknown_blessing = True
        else:
            unknown_blessing = False
        extra_lives = str(9 - len(life_givers))
        possible_lives = ceremony_dict["lives"]
        lives = []
        used_lives = []
        used_virtues = []
        for giver in life_givers:
            giver_cat = self.fetch_cat(giver)
            if not giver_cat:
                continue
            life_list = []
            for life in possible_lives:
                tags = possible_lives[life]["tags"]
                rank = giver_cat.status

                if "unknown_blessing" in tags:
                    continue

                if "guide" in tags and giver_cat != game.clan.instructor:
                    continue
                if game.clan.age != 0 and "new_clan" in tags:
                    continue
                elif game.clan.age == 0 and "new_clan" not in tags:
                    continue
                if "old_leader" in tags and not ancient_leader:
                    continue
                if "leader_parent" in tags and giver_cat.ID not in self.get_parents():
                    continue
                elif "leader_child" in tags and giver_cat.ID not in self.get_children():
                    continue
                elif (
                    "leader_sibling" in tags and giver_cat.ID not in self.get_siblings()
                ):
                    continue
                elif "leader_mate" in tags and giver_cat.ID not in self.mate:
                    continue
                elif (
                    "leader_former_mate" in tags
                    and giver_cat.ID not in self.previous_mates
                ):
                    continue
                if "leader_mentor" in tags and giver_cat.ID not in self.former_mentor:
                    continue
                if (
                    "leader_apprentice" in tags
                    and giver_cat.ID not in self.former_apprentices
                ):
                    continue
                if (
                    possible_lives[life]["rank"]
                    and rank not in possible_lives[life]["rank"]
                ):
                    continue
                if (
                    possible_lives[life]["lead_trait"]
                    and self.personality.trait not in possible_lives[life]["lead_trait"]
                ):
                    continue
                if possible_lives[life]["star_trait"] and (
                    giver_cat.personality.trait
                    not in possible_lives[life]["star_trait"]
                ):
                    continue
                life_list.extend(list(possible_lives[life]["life_giving"]))

            i = 0
            chosen_life = {}
            while i < 10:
                attempted = []
                if life_list:
                    chosen_life = choice(life_list)
                    if chosen_life not in used_lives and chosen_life not in attempted:
                        break
                    attempted.append(chosen_life)
                    i += 1
                else:
                    print(
                        f"WARNING: life list had no items for giver #{giver_cat.ID}. Using default life. "
                        f"If you are a beta tester, please report and ping scribble along with "
                        f"all the info you can about the giver cat mentioned in this warning."
                    )
                    chosen_life = ceremony_dict["default_life"]
                    break

            used_lives.append(chosen_life)
            if "virtue" in chosen_life:
                poss_virtues = [
                    i for i in chosen_life["virtue"] if i not in used_virtues
                ] or ["faith", "friendship", "love", "strength"]
                virtue = choice(poss_virtues)
                used_virtues.append(virtue)
            else:
                virtue = None

            lives.append(
                leader_ceremony_text_adjust(
                    Cat,
                    chosen_life["text"],
                    leader=self,
                    life_giver=giver,
                    virtue=virtue,
                )
            )
        if unknown_blessing:
            possible_blessing = []
            for life in possible_lives:
                tags = possible_lives[life]["tags"]

                if "unknown_blessing" not in tags:
                    continue

                if (
                    possible_lives[life]["lead_trait"]
                    and self.personality.trait not in possible_lives[life]["lead_trait"]
                ):
                    continue
                possible_blessing.append(possible_lives[life])
            chosen_blessing = choice(possible_blessing)
            chosen_text = choice(chosen_blessing["life_giving"])
            lives.append(
                leader_ceremony_text_adjust(
                    Cat,
                    chosen_text["text"],
                    leader=self,
                    virtue=chosen_text["virtue"],
                    extra_lives=extra_lives,
                )
            )
        all_lives = "<br><br>".join(lives)

        # ---------------------------------------------------------------------------- #
        #                                    OUTRO                                     #
        # ---------------------------------------------------------------------------- #

        # get the outro
        all_outros = ceremony_dict["outros"]

        possible_outros = []
        for outro in all_outros:
            tags = all_outros[outro]["tags"]

            if game.clan.age != 0 and "new_clan" in tags:
                continue
            elif game.clan.age == 0 and "new_clan" not in tags:
                continue

            if (
                all_outros[outro]["lead_trait"]
                and self.personality.trait not in all_outros[outro]["lead_trait"]
            ):
                continue
            possible_outros.append(all_outros[outro])

        chosen_outro = choice(possible_outros)

        if chosen_outro:
            if life_givers:
                giver = life_givers[-1]
            else:
                giver = None
            outro = choice(chosen_outro["text"])
            outro = leader_ceremony_text_adjust(
                Cat,
                outro,
                leader=self,
                life_giver=giver,
            )
        else:
            outro = "this should not appear"

        full_ceremony = "<br><br>".join([intro, all_lives, outro])
        return full_ceremony

    # ---------------------------------------------------------------------------- #
    #                              moon skip functions                             #
    # ---------------------------------------------------------------------------- #

    def one_moon(self):
        """Handles a moon skip for an alive cat."""
        old_age = self.age
        self.moons += 1
        if self.moons == 1 and self.status == "newborn":
            self.status = "kitten"
        self.in_camp = 1

        if self.exiled or self.outside:
            # this is handled in events.py
            self.personality.set_kit(self.is_baby())
            self.thoughts()
            return

        if self.dead:
            self.thoughts()
            return

        if old_age != self.age:
            # Things to do if the age changes
            self.personality.facet_wobble(facet_max=2)

        # Set personality to correct type
        self.personality.set_kit(self.is_baby())
        # Upon age-change

        if self.status in [
            "apprentice",
            "mediator apprentice",
            "cleric apprentice",
        ]:
            self.update_mentor()

    def thoughts(self):
        """Generates a thought for the cat, which displays on their profile."""
        all_cats = self.all_cats
        other_cat = choice(list(all_cats.keys()))
        game_mode = game.switches["game_mode"]
        biome = game.switches["biome"]
        camp = game.switches["camp_bg"]
        try:
            season = game.clan.current_season
        except Exception:
            season = None

        # this figures out where the cat is
        where_kitty = None
        if not self.dead and not self.outside:
            where_kitty = "inside"
        elif self.dead and not self.df and not self.outside:
            where_kitty = "starclan"
        elif self.dead and self.df:
            where_kitty = "hell"
        elif self.dead:
            where_kitty = "UR"
        else:
            where_kitty = "outside"
        # get other cat
        i = 0
        # for cats inside the clan
        if where_kitty == "inside":
            dead_chance = getrandbits(4)
            while (
                other_cat == self.ID
                and len(all_cats) > 1
                or (all_cats.get(other_cat).dead and dead_chance != 1)
                or (other_cat not in self.relationships)
            ):
                other_cat = choice(list(all_cats.keys()))
                i += 1
                if i > 100:
                    other_cat = None
                    break
        # for dead cats
        elif where_kitty in ["starclan", "hell", "UR"]:
            while other_cat == self.ID and len(all_cats) > 1:
                other_cat = choice(list(all_cats.keys()))
                i += 1
                if i > 100:
                    other_cat = None
                    break
        # for cats currently outside
        # it appears as for now, kittypets and loners can only think about outsider cats
        elif where_kitty == "outside":
            while (
                other_cat == self.ID
                and len(all_cats) > 1
                or (other_cat not in self.relationships)
            ):
                # or (self.status in ['kittypet', 'loner'] and not all_cats.get(other_cat).outside):
                other_cat = choice(list(all_cats.keys()))
                i += 1
                if i > 100:
                    other_cat = None
                    break

        other_cat = all_cats.get(other_cat)

        # get chosen thought
        chosen_thought = Thoughts.get_chosen_thought(
            self, other_cat, game_mode, biome, season, camp
        )

        chosen_thought = event_text_adjust(
            Cat, chosen_thought, main_cat=self, random_cat=other_cat, clan=game.clan
        )

        # insert thought
        self.thought = str(chosen_thought)

    def relationship_interaction(self):
        """Randomly choose a cat of the Clan and have an interaction with them."""
        cats_to_choose = [
            iter_cat
            for iter_cat in Cat.all_cats.values()
            if iter_cat.ID != self.ID
            and not iter_cat.outside
            and not iter_cat.exiled
            and not iter_cat.dead
        ]
        # if there are no cats to interact, stop
        if not cats_to_choose:
            return

        chosen_cat = choice(cats_to_choose)
        if chosen_cat.ID not in self.relationships:
            self.create_one_relationship(chosen_cat)
        relevant_relationship = self.relationships[chosen_cat.ID]
        relevant_relationship.start_interaction()

        # handle contact with ill cat if
        if self.is_ill():
            relevant_relationship.cat_to.contact_with_ill_cat(self)
        if relevant_relationship.cat_to.is_ill():
            self.contact_with_ill_cat(relevant_relationship.cat_to)

    def moon_skip_illness(self, illness):
        """handles the moon skip for illness"""
        if not self.is_ill():
            return True

        if self.illnesses[illness]["event_triggered"]:
            self.illnesses[illness]["event_triggered"] = False
            return True

        mortality = self.illnesses[illness]["mortality"]

        # leader should have a higher chance of death
        if self.status == "leader" and mortality != 0:
            mortality = int(mortality * 0.7)
            if mortality == 0:
                mortality = 1

        if mortality and not int(random() * mortality):
            if self.status == "leader":
                self.leader_death_heal = True
                game.clan.leader_lives -= 1

            self.die()
            return False

        moons_with = game.clan.age - self.illnesses[illness]["moon_start"]

        # focus buff
        moons_prior = game.config["focus"]["rest and recover"]["moons_earlier_healed"]

        if self.illnesses[illness]["duration"] - moons_with <= 0:
            self.healed_condition = True
            return False

        # CLAN FOCUS! - if the focus 'rest and recover' is selected
        elif (
            game.clan.clan_settings.get("rest and recover")
            and self.illnesses[illness]["duration"] + moons_prior - moons_with <= 0
        ):
            self.healed_condition = True
            return False

    def moon_skip_injury(self, injury):
        """handles the moon skip for injury"""
        if not self.is_injured():
            return True

        if self.injuries[injury]["event_triggered"] is True:
            self.injuries[injury]["event_triggered"] = False
            return True

        mortality = self.injuries[injury]["mortality"]

        # leader should have a higher chance of death
        if self.status == "leader" and mortality != 0:
            mortality = int(mortality * 0.7)
            if mortality == 0:
                mortality = 1

        if mortality and not int(random() * mortality):
            if self.status == "leader":
                game.clan.leader_lives -= 1
            self.die()
            return False

        moons_with = game.clan.age - self.injuries[injury]["moon_start"]

        # focus buff
        moons_prior = game.config["focus"]["rest and recover"]["moons_earlier_healed"]

        # if the cat has an infected wound, the wound shouldn't heal till the illness is cured
        if (
            not self.injuries[injury]["complication"]
            and self.injuries[injury]["duration"] - moons_with <= 0
        ):
            self.healed_condition = True
            return False

        # CLAN FOCUS! - if the focus 'rest and recover' is selected
        elif (
            not self.injuries[injury]["complication"]
            and game.clan.clan_settings.get("rest and recover")
            and self.injuries[injury]["duration"] + moons_prior - moons_with <= 0
        ):
            self.healed_condition = True
            return False

    def moon_skip_permanent_condition(self, condition):
        """handles the moon skip for permanent conditions"""
        if not self.is_disabled():
            return "skip"

        if self.permanent_condition[condition]["event_triggered"]:
            self.permanent_condition[condition]["event_triggered"] = False
            return "skip"

        mortality = self.permanent_condition[condition]["mortality"]
        moons_until = self.permanent_condition[condition]["moons_until"]
        born_with = self.permanent_condition[condition]["born_with"]

        # handling the countdown till a congenital condition is revealed
        if moons_until is not None and moons_until >= 0 and born_with is True:
            self.permanent_condition[condition]["moons_until"] = int(moons_until - 1)
            self.permanent_condition[condition]["moons_with"] = 0
            if self.permanent_condition[condition]["moons_until"] != -1:
                return "skip"
        if (
            self.permanent_condition[condition]["moons_until"] == -1
            and self.permanent_condition[condition]["born_with"] is True
        ):
            self.permanent_condition[condition]["moons_until"] = -2
            return "reveal"

        # leader should have a higher chance of death
        if self.status == "leader" and mortality != 0:
            mortality = int(mortality * 0.7)
            if mortality == 0:
                mortality = 1

        if mortality and not int(random() * mortality):
            if self.status == "leader":
                game.clan.leader_lives -= 1
            self.die()
            return "continue"

    # ---------------------------------------------------------------------------- #
    #                                   relative                                   #
    # ---------------------------------------------------------------------------- #
    def get_parents(self):
        """Returns list containing parents of cat(id)."""
        if not self.inheritance:
            self.inheritance = Inheritance(self)
        return self.inheritance.parents.keys()

    def get_siblings(self):
        """Returns list of the siblings(id)."""
        if not self.inheritance:
            self.inheritance = Inheritance(self)
        return self.inheritance.siblings.keys()

    def get_children(self):
        """Returns list of the children (ids)."""
        if not self.inheritance:
            self.inheritance = Inheritance(self)
        return self.inheritance.kits.keys()

    def is_grandparent(self, other_cat: Cat):
        """Check if the cat is the grandparent of the other cat."""
        if not self.inheritance:
            self.inheritance = Inheritance(self)
        return other_cat.ID in self.inheritance.grand_kits.keys()

    def is_parent(self, other_cat: Cat):
        """Check if the cat is the parent of the other cat."""
        if not self.inheritance:
            self.inheritance = Inheritance(self)
        return other_cat.ID in self.inheritance.kits.keys()

    def is_sibling(self, other_cat: Cat):
        """Check if the cats are siblings."""
        if not self.inheritance:
            self.inheritance = Inheritance(self)
        return other_cat.ID in self.inheritance.siblings.keys()

    def is_littermate(self, other_cat: Cat):
        """Check if the cats are littermates."""
        if other_cat.ID not in self.inheritance.siblings.keys():
            return False
        litter_mates = [
            key
            for key, value in self.inheritance.siblings.items()
            if "litter mates" in value["additional"]
        ]
        return other_cat.ID in litter_mates

    def is_uncle_aunt(self, other_cat: Cat):
        """Check if the cats are related as uncle/aunt and niece/nephew."""
        if not self.inheritance:
            self.inheritance = Inheritance(self)
        return other_cat.ID in self.inheritance.siblings_kits.keys()

    def is_cousin(self, other_cat: Cat):
        """Check if this cat and other_cat are cousins."""
        if not self.inheritance:
            self.inheritance = Inheritance(self)
        return other_cat.ID in self.inheritance.cousins.keys()

    def is_related(self, other_cat, cousin_allowed):
        """Checks if the given cat is related to the current cat, according to the inheritance."""
        if not self.inheritance:
            self.inheritance = Inheritance(self)
        if cousin_allowed:
            return other_cat.ID in self.inheritance.all_but_cousins
        return other_cat.ID in self.inheritance.all_involved

    def get_relatives(self, cousin_allowed=True) -> list:
        """Returns a list of ids of all nearly related ancestors."""
        if not self.inheritance:
            self.inheritance = Inheritance(self)
        if cousin_allowed:
            return self.inheritance.all_involved
        return self.inheritance.all_but_cousins

    # ---------------------------------------------------------------------------- #
    #                                  conditions                                  #
    # ---------------------------------------------------------------------------- #

    def get_ill(self, name, event_triggered=False, lethal=True, severity="default"):
        """Add an illness to this cat.

        :param name: name of the illness (str)
        :param event_triggered: Whether to have this illness skip `moon_skip_illness` for 1 moon, default `False` (bool)
        :param lethal: Allow lethality, default `True` (bool)
        :param severity: Override severity, default `'default'` (str, accepted values `'minor'`, `'major'`, `'severe'`)
        """
        if name not in ILLNESSES:
            print(f"WARNING: {name} is not in the illnesses collection.")
            return
        if name == "kittencough" and self.status != "kitten":
            return

        illness = ILLNESSES[name]
        mortality = illness["mortality"][self.age]
        med_mortality = illness["medicine_mortality"][self.age]
        illness_severity = illness["severity"] if severity == "default" else severity
        duration = illness["duration"]
        med_duration = illness["medicine_duration"]

        amount_per_med = get_amount_cat_for_one_medic(game.clan)

        if medical_cats_condition_fulfilled(Cat.all_cats.values(), amount_per_med):
            duration = med_duration
        if severity != "minor":
            duration += randrange(-1, 1)
        if duration == 0:
            duration = 1

        if game.clan and game.clan.game_mode == "cruel season" and mortality != 0:
            mortality = int(mortality * 0.5)
            med_mortality = int(med_mortality * 0.5)

            # to prevent an illness gets no mortality, check and set it to 1 if needed
            if mortality == 0 or med_mortality == 0:
                mortality = 1
                med_mortality = 1
        if lethal is False:
            mortality = 0

        new_illness = Illness(
            name=name,
            severity=illness_severity,
            mortality=mortality,
            infectiousness=illness["infectiousness"],
            duration=duration,
            medicine_duration=illness["medicine_duration"],
            medicine_mortality=med_mortality,
            risks=illness["risks"],
            event_triggered=event_triggered,
        )

        if new_illness.name not in self.illnesses:
            self.illnesses[new_illness.name] = {
                "severity": new_illness.severity,
                "mortality": new_illness.current_mortality,
                "infectiousness": new_illness.infectiousness,
                "duration": new_illness.duration,
                "moon_start": game.clan.age if game.clan else 0,
                "risks": new_illness.risks,
                "event_triggered": new_illness.new,
            }

    def get_injured(self, name, event_triggered=False, lethal=True, severity="default"):
        """Add an injury to this cat.

        :param name: The injury to add
        :type name: str
        :param event_triggered: Whether to process healing immediately, defaults to False
        :type event_triggered: bool, optional
        :param lethal: _description_, defaults to True
        :type lethal: bool, optional
        :param severity: _description_, defaults to 'default'
        :type severity: str, optional
        """
        if name not in INJURIES:
            print(f"WARNING: {name} is not in the injuries collection.")
            return

        if name == "mangled tail" and "NOTAIL" in self.pelt.scars:
            return
        if name == "torn ear" and "NOEAR" in self.pelt.scars:
            return
        if name == "the rot" and "ROTRIDDEN" in self.pelt.scars:
            return

        injury = INJURIES[name]
        mortality = injury["mortality"][self.age]
        duration = injury["duration"]
        med_duration = injury["medicine_duration"]

        injury_severity = injury["severity"] if severity == "default" else severity
        if medical_cats_condition_fulfilled(
            Cat.all_cats.values(), get_amount_cat_for_one_medic(game.clan)
        ):
            duration = med_duration
        if severity != "minor":
            duration += randrange(-1, 1)
        if duration == 0:
            duration = 1

        if mortality != 0 and (game.clan and game.clan.game_mode == "cruel season"):
            mortality = int(mortality * 0.5)

            if mortality == 0:
                mortality = 1
        if lethal is False:
            mortality = 0

        new_injury = Injury(
            name=name,
            severity=injury_severity,
            duration=injury["duration"],
            medicine_duration=duration,
            mortality=mortality,
            risks=injury["risks"],
            illness_infectiousness=injury["illness_infectiousness"],
            also_got=injury["also_got"],
            cause_permanent=injury["cause_permanent"],
            event_triggered=event_triggered,
        )

        if new_injury.name not in self.injuries:
            self.injuries[new_injury.name] = {
                "severity": new_injury.severity,
                "mortality": new_injury.current_mortality,
                "duration": new_injury.duration,
                "moon_start": game.clan.age if game.clan else 0,
                "illness_infectiousness": new_injury.illness_infectiousness,
                "risks": new_injury.risks,
                "complication": None,
                "cause_permanent": new_injury.cause_permanent,
                "event_triggered": new_injury.new,
            }

        if len(new_injury.also_got) > 0 and not int(random() * 5):
            avoided = False
            if (
                "blood loss" in new_injury.also_got
                and len(get_alive_status_cats(Cat, ["cleric"], working=True)) != 0
            ):
                clan_herbs = set()
                needed_herbs = {"horsetail", "raspberry", "marigold", "cobwebs"}
                clan_herbs.update(game.clan.herbs.keys())
                herb_set = needed_herbs.intersection(clan_herbs)
                usable_herbs = []
                usable_herbs.extend(herb_set)

                if usable_herbs:
                    # deplete the herb
                    herb_used = choice(usable_herbs)
                    game.clan.herbs[herb_used] -= 1
                    if game.clan.herbs[herb_used] <= 0:
                        game.clan.herbs.pop(herb_used)
                    avoided = True
                    text = f"{herb_used.capitalize()} was used to stop blood loss for {self.name}."
                    game.herb_events_list.append(text)

            if not avoided:
                self.also_got = True
                additional_injury = choice(new_injury.also_got)
                if additional_injury in INJURIES:
                    self.additional_injury(additional_injury)
                else:
                    self.get_ill(additional_injury, event_triggered=True)
        else:
            self.also_got = False

    def additional_injury(self, injury):
        self.get_injured(injury, event_triggered=True)

    def congenital_condition(self, cat):
        possible_conditions = []

        for condition in PERMANENT:
            possible = PERMANENT[condition]
            if possible["congenital"] in ["always", "sometimes"]:
                possible_conditions.append(condition)

        new_condition = choice(possible_conditions)

        if new_condition == "born without a leg":
            cat.pelt.scars.append("NOPAW")
        elif new_condition == "born without a tail":
            cat.pelt.scars.append("NOTAIL")
        elif new_condition == "the rot":
            cat.pelt.scars.append("ROTRIDDEN")

        self.get_permanent_condition(new_condition, born_with=True)

    def get_permanent_condition(self, name, born_with=False, event_triggered=False):
        if name not in PERMANENT:
            print(
                self.name,
                f"WARNING: {name} is not in the permanent conditions collection.",
            )
            return

        if "blind" in self.permanent_condition and name == "failing eyesight":
            return
        if "deaf" in self.permanent_condition and name == "partial hearing loss":
            return

        # remove accessories if need be
        if 'NOTAIL' in self.pelt.scars or 'HALFTAIL' in self.pelt.scars:
            for acc in [
                'RED FEATHERS', 'BLUE FEATHERS',
                'JAY FEATHERS', "SEAWEED",
                "DAISY CORSAGE", "GULL FEATHERS",
                "SPARROW FEATHERS", "CLOVER",
                "DAISY", "MUSHROOMS",
                "FLOWEREDMOSS", "MOSS",
                "ORANGEFIRE", "GREENFIRE",
                "BLUEFIRE", "YELLOWFIRE",
                "WHITEFIRE", "PINKFIRE",
                "REDFIRE"
                ]:
                if acc in self.pelt.accessories:
                    self.pelt.inventory.remove(acc)
                if acc in self.pelt.inventory:
                    self.pelt.inventory.remove(acc)

        if 'NOPAW' in self.pelt.scars:
            for acc in [
                "HANDPEARLBLANK", "HANDPEARLBLUE",
                "HANDPEARLGREEN", "HANDPEARLORANGE",
                "HANDPEARLPURPLE", "HANDPEARLRED",
                "HANDPEARLYELLOW", "REDPAINT",
                "PINKPAINT", "VOIDPAINT",
                "YELLOWPAINT", "GREENPAINT",
                "PALEPAINT", "CYANPAINT",
                "BLUEPAINT", "PURPLEPAINT",
                "MAGENTAPAINT", "BLACKPAINT",
                "WHITEPAINT", "FALLENSTARPAWS",
                "MUDDYPAWS"
                ]:
                if acc in self.pelt.accessories:
                    self.pelt.inventory.remove(acc)
                if acc in self.pelt.inventory:
                    self.pelt.inventory.remove(acc)

        if 'NOEAR' in self.pelt.scars or 'NOLEFTEAR' in self.pelt.scars or 'NORIGHTEAR' in self.pelt.scars:
            for acc in [
                "STRAIGHTGOLD", "STRAIGHTSILVER",
                "MAGNATEJEWLERY", "REDPAINT",
                "PINKPAINT", "VOIDPAINT",
                "YELLOWPAINT", "GREENPAINT",
                "PALEPAINT", "CYANPAINT",
                "BLUEPAINT", "PURPLEPAINT",
                "MAGENTAPAINT", "BLACKPAINT",
                "WHITEPAINT"
                ]:
                if acc in self.pelt.accessories:
                    self.pelt.inventory.remove(acc)
                if acc in self.pelt.inventory:
                    self.pelt.inventory.remove(acc)

        condition = PERMANENT[name]
        new_condition = False
        mortality = condition["mortality"][self.age]
        if mortality != 0 and (game.clan and game.clan.game_mode == "cruel season"):
            mortality = int(mortality * 0.65)

        if condition["congenital"] == "always":
            born_with = True
        moons_until = condition["moons_until"]
        if born_with and moons_until != 0:
            moons_until = randint(
                moons_until - 1, moons_until + 1
            )  # creating a range in which a condition can present
            moons_until = max(moons_until, 0)

        if born_with and self.status not in ["kitten", "newborn"]:
            moons_until = -2
        elif born_with is False:
            moons_until = 0

        if name == "paralyzed":
            self.pelt.paralyzed = True

        new_perm_condition = PermanentCondition(
            name=name,
            severity=condition["severity"],
            congenital=condition["congenital"],
            moons_until=moons_until,
            mortality=mortality,
            risks=condition["risks"],
            illness_infectiousness=condition["illness_infectiousness"],
            event_triggered=event_triggered,
        )

        if new_perm_condition.name not in self.permanent_condition:
            self.permanent_condition[new_perm_condition.name] = {
                "severity": new_perm_condition.severity,
                "born_with": born_with,
                "moons_until": new_perm_condition.moons_until,
                "moon_start": game.clan.age if game.clan else 0,
                "mortality": new_perm_condition.current_mortality,
                "illness_infectiousness": new_perm_condition.illness_infectiousness,
                "risks": new_perm_condition.risks,
                "complication": None,
                "event_triggered": new_perm_condition.new,
            }
            new_condition = True
        return new_condition

    def not_working(self):
        """returns True if the cat cannot work, False if the cat can work"""
        for illness in self.illnesses:
            if self.illnesses[illness]["severity"] != "minor":
                return True
        return any(
            self.injuries[injury]["severity"] != "minor" for injury in self.injuries
        )

    def not_work_because_hunger(self):
        """returns True if the only condition, why the cat cannot work is because of starvation"""
        non_minor_injuries = [
            injury
            for injury in self.injuries
            if self.injuries[injury]["severity"] != "minor"
        ]
        if len(non_minor_injuries) > 0:
            return False
        non_minor_illnesses = [
            illness
            for illness in self.illnesses
            if self.illnesses[illness]["severity"] != "minor"
        ]
        return "starving" in non_minor_illnesses and len(non_minor_illnesses) == 1

    def retire_cat(self):
        """This is only for cats that retire due to health condition"""

        # There are some special tasks we need to do for apprentice
        # Note that although you can un-retire cats, they will be a full warrior/med_cat/mediator
        if self.moons > 6 and self.status in [
            "apprentice",
            "cleric apprentice",
            "mediator apprentice",
        ]:
            _ment = Cat.fetch_cat(self.mentor) if self.mentor else None
            self.status_change(
                "warrior"
            )  # Temp switch them to warrior, so the following step will work
            self.rank_change_traits_skill(_ment)

        self.status_change("elder")
        return

    def is_ill(self):
        """Returns true if the cat is ill."""
        return len(self.illnesses) > 0

    def is_injured(self):
        """Returns true if the cat is injured."""
        return len(self.injuries) > 0

    def is_disabled(self):
        """Returns true if the cat have permanent condition"""
        return len(self.permanent_condition) > 0

    def contact_with_ill_cat(self, cat: Cat):
        """handles if one cat had contact with an ill cat"""

        infectious_illnesses = []
        if self.is_ill() or cat is None or not cat.is_ill():
            return
        elif cat.is_ill():
            for illness in cat.illnesses:
                if cat.illnesses[illness]["infectiousness"] != 0:
                    infectious_illnesses.append(illness)
            if len(infectious_illnesses) == 0:
                return

        for illness in infectious_illnesses:
            illness_name = illness
            rate = cat.illnesses[illness]["infectiousness"]
            if self.is_injured():
                for y in self.injuries:
                    illness_infect = list(
                        filter(
                            lambda ill: ill["name"] == illness_name,
                            self.injuries[y]["illness_infectiousness"],
                        )
                    )
                    if illness_infect is not None and len(illness_infect) > 0:
                        illness_infect = illness_infect[0]
                        rate -= illness_infect["lower_by"]

                    # prevent rate lower 0 and print warning message
                    if rate < 0:
                        print(
                            f"WARNING: injury {self.injuries[y]['name']} has lowered \
                            chance of {illness_name} infection to {rate}"
                        )
                        rate = 1

            if not random() * rate:
                text = f"{self.name} had contact with {cat.name} and now has {illness_name}."
                # game.health_events_list.append(text)
                game.cur_events_list.append(
                    Single_Event(text, "health", [self.ID, cat.ID])
                )
                self.get_ill(illness_name)

    def save_condition(self):
        # save conditions for each cat
        clanname = None
        if game.switches["clan_name"] != "":
            clanname = game.switches["clan_name"]
        elif len(game.switches["clan_name"]) > 0:
            clanname = game.switches["clan_list"][0]
        elif game.clan is not None:
            clanname = game.clan.name

        condition_directory = get_save_dir() + "/" + clanname + "/conditions"
        condition_file_path = condition_directory + "/" + self.ID + "_conditions.json"

        if (
            (not self.is_ill() and not self.is_injured() and not self.is_disabled())
            or self.dead
            or self.outside
        ):
            if os.path.exists(condition_file_path):
                os.remove(condition_file_path)
            return

        conditions = {}

        if self.is_ill():
            conditions["illnesses"] = self.illnesses

        if self.is_injured():
            conditions["injuries"] = self.injuries

        if self.is_disabled():
            conditions["permanent conditions"] = self.permanent_condition

        game.safe_save(condition_file_path, conditions)

    def load_conditions(self):
        if game.switches["clan_name"] != "":
            clanname = game.switches["clan_name"]
        else:
            clanname = game.switches["clan_list"][0]

        condition_directory = get_save_dir() + "/" + clanname + "/conditions/"
        condition_cat_directory = condition_directory + self.ID + "_conditions.json"
        if not os.path.exists(condition_cat_directory):
            return

        try:
            with open(condition_cat_directory, "r", encoding="utf-8") as read_file:
                rel_data = ujson.loads(read_file.read())
                self.illnesses = rel_data.get("illnesses", {})
                self.injuries = rel_data.get("injuries", {})
                self.permanent_condition = rel_data.get("permanent conditions", {})

            if "paralyzed" in self.permanent_condition and not self.pelt.paralyzed:
                self.pelt.paralyzed = True

        except Exception as e:
            print(
                f"WARNING: There was an error reading the condition file of cat #{self}.\n",
                e,
            )

    # ---------------------------------------------------------------------------- #
    #                                    mentor                                    #
    # ---------------------------------------------------------------------------- #

    def is_valid_mentor(self, potential_mentor: Cat):
        # Dead or outside cats can't be mentors
        if potential_mentor.dead or potential_mentor.outside:
            return False
        # Match jobs
        if (
            self.status == "cleric apprentice"
            and potential_mentor.status != "cleric"
        ):
            return False
        if self.status == "apprentice" and potential_mentor.status not in [
            "leader",
            "deputy",
            "warrior",
        ]:
            return False
        if (
            self.status == "mediator apprentice"
            and potential_mentor.status != "mediator"
        ):
            return False

        # If not an app, don't need a mentor
        if "apprentice" not in self.status:
            return False
        # Dead cats don't need mentors
        if self.dead or self.outside or self.exiled:
            return False
        return True

    def __remove_mentor(self):
        """Should only be called by update_mentor, also sets fields on mentor."""
        if not self.mentor:
            return
        mentor_cat = Cat.fetch_cat(self.mentor)
        if not mentor_cat:
            return
        if self.ID in mentor_cat.apprentice:
            mentor_cat.apprentice.remove(self.ID)
        if self.moons > 6 and self.ID not in mentor_cat.former_apprentices:
            mentor_cat.former_apprentices.append(self.ID)
        if self.moons > 6 and mentor_cat.ID not in self.former_mentor:
            self.former_mentor.append(mentor_cat.ID)
        self.mentor = None

    def __add_mentor(self, new_mentor_id: str):
        """Should only be called by update_mentor, also sets fields on mentor."""
        # reset patrol number
        self.patrol_with_mentor = 0
        self.mentor = new_mentor_id
        mentor_cat = Cat.fetch_cat(self.mentor)
        if not mentor_cat:
            return
        if self.ID not in mentor_cat.apprentice:
            mentor_cat.apprentice.append(self.ID)

    def update_mentor(self, new_mentor: Any = None):
        """Takes mentor's ID as argument, mentor could just be set via this function."""
        # No !!
        if isinstance(new_mentor, Cat):
            print("Everything is terrible!! (new_mentor {new_mentor} is a Cat D:)")
            return
        # Check if cat can have a mentor
        illegible_for_mentor = (
            self.dead
            or self.outside
            or self.exiled
            or self.status
            not in ["apprentice", "mediator apprentice", "cleric apprentice"]
        )
        if illegible_for_mentor:
            self.__remove_mentor()
            return
        # If eligible, cat should get a mentor.
        if new_mentor:
            self.__remove_mentor()
            self.__add_mentor(new_mentor)

        # Check if current mentor is valid
        if self.mentor:
            mentor_cat = Cat.fetch_cat(
                self.mentor
            )  # This will return None if there is no current mentor
            if mentor_cat and not self.is_valid_mentor(mentor_cat):
                self.__remove_mentor()

        # Need to pick a random mentor if not specified
        if not self.mentor:
            potential_mentors = []
            priority_mentors = []
            for cat in self.all_cats.values():
                if self.is_valid_mentor(cat):
                    potential_mentors.append(cat)
                    if not cat.apprentice and not cat.not_working():
                        priority_mentors.append(cat)
            # First try for a cat who currently has no apprentices and is working
            if priority_mentors:  # length of list > 0
                new_mentor = choice(priority_mentors)
            elif potential_mentors:  # length of list > 0
                new_mentor = choice(potential_mentors)
            if new_mentor:
                self.__add_mentor(new_mentor.ID)

    # ---------------------------------------------------------------------------- #
    #                                 relationships                                #
    # ---------------------------------------------------------------------------- #
    def is_potential_mate(
        self,
        other_cat: Cat,
        for_love_interest: bool = False,
        age_restriction: bool = True,
        first_cousin_mates: bool = False,
        ignore_no_mates: bool = False,
    ):
        """
        Checks if this cat is potential mate for the other cat.
        There are no restrictions if the current cat already has a mate or not (this allows poly-mates).
        """

        try:
            first_cousin_mates = game.clan.clan_settings["first cousin mates"]
        except:
            if "unittest" not in sys.modules:
                raise

        # just to be sure, check if it is not the same cat
        if self.ID == other_cat.ID:
            return False

        # No Mates Check
        if not ignore_no_mates and (self.no_mates or other_cat.no_mates):
            return False

        # Inheritance check
        if self.is_related(other_cat, first_cousin_mates):
            return False

        # check dead cats
        if self.dead != other_cat.dead:
            return False

        # check for age
        if age_restriction:
            if (self.moons < 14 or other_cat.moons < 14) and not for_love_interest:
                return False

            # the +1 is necessary because both might not already be aged up
            # if only one is aged up at this point, later they are more moons apart than the setting defined
            # game_config boolean "override_same_age_group" disables the same-age group check.
            if (
                game.config["mates"].get("override_same_age_group", False)
                or self.age != other_cat.age
            ) and (
                abs(self.moons - other_cat.moons)
                > game.config["mates"]["age_range"] + 1
            ):
                return False

        age_restricted_ages = ["newborn", "kitten", "adolescent"]
        if (
            self.age in age_restricted_ages or other_cat.age in age_restricted_ages
        ) and self.age != other_cat.age:
            return False

        # check for mentor

        # Current mentor
        if other_cat.ID in self.apprentice or self.ID in other_cat.apprentice:
            return False

        # Former mentor
        is_former_mentor = (
            other_cat.ID in self.former_apprentices
            or self.ID in other_cat.former_apprentices
        )
        return bool(
            not is_former_mentor
            or game.clan.clan_settings["romantic with former mentor"]
        )

    def unset_mate(self, other_cat: Cat, breakup: bool = False, fight: bool = False):
        """Unset the mate from both self and other_cat"""
        if not other_cat:
            return

        # Both cats must have mates for this to work
        if len(self.mate) < 1 or len(other_cat.mate) < 1:
            return

        # AND they must be mates with each other.
        if self.ID not in other_cat.mate or other_cat.ID not in self.mate:
            print(
                f"Unsetting mates: These {self.name} and {other_cat.name} are not mates!"
            )
            return

        # If only deal with relationships if this is a breakup.
        if breakup:
            self_relationship = None
            if not self.dead:
                if other_cat.ID not in self.relationships:
                    self.create_one_relationship(other_cat)
                    self.relationships[other_cat.ID].mate = True
                self_relationship = self.relationships[other_cat.ID]
                self_relationship.romantic_love -= randint(20, 60)
                self_relationship.comfortable -= randint(10, 30)
                self_relationship.trust -= randint(5, 15)
                self_relationship.mate = False
                if fight:
                    self_relationship.romantic_love -= randint(10, 30)
                    self_relationship.platonic_like -= randint(15, 45)

            if not other_cat.dead:
                if self.ID not in other_cat.relationships:
                    other_cat.create_one_relationship(self)
                    other_cat.relationships[self.ID].mate = True
                other_relationship = other_cat.relationships[self.ID]
                other_relationship.romantic_love -= 40
                other_relationship.comfortable -= 20
                other_relationship.trust -= 10
                other_relationship.mate = False
                if fight:
                    self_relationship.romantic_love -= 20
                    other_relationship.platonic_like -= 30

        self.mate.remove(other_cat.ID)
        other_cat.mate.remove(self.ID)

        # Handle previous mates:
        if other_cat.ID not in self.previous_mates:
            self.previous_mates.append(other_cat.ID)
        if self.ID not in other_cat.previous_mates:
            other_cat.previous_mates.append(self.ID)

        if other_cat.inheritance:
            other_cat.inheritance.update_all_mates()
        if self.inheritance:
            self.inheritance.update_all_mates()

    def set_mate(self, other_cat: Cat):
        """Sets up a mate relationship between self and other_cat."""
        if other_cat.ID not in self.mate:
            self.mate.append(other_cat.ID)
        if self.ID not in other_cat.mate:
            other_cat.mate.append(self.ID)

        # If the current mate was in the previous mate list, remove them.
        if other_cat.ID in self.previous_mates:
            self.previous_mates.remove(other_cat.ID)
        if self.ID in other_cat.previous_mates:
            other_cat.previous_mates.remove(self.ID)

        if other_cat.inheritance:
            other_cat.inheritance.update_all_mates()
        if self.inheritance:
            self.inheritance.update_all_mates()

        # Set starting relationship values
        if not self.dead:
            if other_cat.ID not in self.relationships:
                self.create_one_relationship(other_cat)
                self.relationships[other_cat.ID].mate = True
            self_relationship = self.relationships[other_cat.ID]
            self_relationship.romantic_love += 20
            self_relationship.comfortable += 20
            self_relationship.trust += 10
            self_relationship.mate = True

        if not other_cat.dead:
            if self.ID not in other_cat.relationships:
                other_cat.create_one_relationship(self)
                other_cat.relationships[self.ID].mate = True
            other_relationship = other_cat.relationships[self.ID]
            other_relationship.romantic_love += 20
            other_relationship.comfortable += 20
            other_relationship.trust += 10
            other_relationship.mate = True

    def unset_adoptive_parent(self, other_cat: Cat):
        """Unset the adoptive parent from self"""
        self.adoptive_parents.remove(other_cat.ID)
        self.create_inheritance_new_cat()
        other_cat.create_inheritance_new_cat()
        if not self.dead:
            if other_cat.ID not in self.relationships:
                self.create_one_relationship(other_cat)
            self_relationship = self.relationships[other_cat.ID]
            self_relationship.platonic_like -= randint(10, 30)
            self_relationship.comfortable -= randint(10, 30)
            self_relationship.trust -= randint(5, 15)

        if not other_cat.dead:
            if self.ID not in other_cat.relationships:
                other_cat.create_one_relationship(self)
            other_relationship = other_cat.relationships[self.ID]
            other_relationship.platonic_like -= 20
            other_relationship.comfortable -= 20
            other_relationship.trust -= 10

    def set_adoptive_parent(self, other_cat: Cat):
        """Sets up a parent-child relationship between self and other_cat."""
        self.adoptive_parents.append(other_cat.ID)
        self.create_inheritance_new_cat()

        # Set starting relationship values
        if not self.dead:
            if other_cat.ID not in self.relationships:
                self.create_one_relationship(other_cat)
            self_relationship = self.relationships[other_cat.ID]
            self_relationship.platonic_like += 20
            self_relationship.comfortable += 20
            self_relationship.trust += 10

        if not other_cat.dead:
            if self.ID not in other_cat.relationships:
                other_cat.create_one_relationship(self)
            other_relationship = other_cat.relationships[self.ID]
            other_relationship.platonic_like += 20
            other_relationship.comfortable += 20
            other_relationship.trust += 10

    def create_inheritance_new_cat(self):
        """Creates the inheritance class for a new cat."""
        # set the born status to true, just for safety
        self.inheritance = Inheritance(self, True)

    def create_one_relationship(self, other_cat: Cat):
        """Create a new relationship between current cat and other cat. Returns: Relationship"""
        if other_cat.ID in self.relationships:
            return self.relationships[other_cat.ID]

        if other_cat.ID == self.ID:
            print(
                f"Attempted to create a relationship with self: {self.name}. Please report as a bug!"
            )
            return None

        self.relationships[other_cat.ID] = Relationship(self, other_cat)
        return self.relationships[other_cat.ID]

    def create_relationships_new_cat(self):
        """Create relationships for a new generated cat."""
        for inter_cat in Cat.all_cats.values():
            # the inter_cat is the same as the current cat
            if inter_cat.ID == self.ID:
                continue
            # if the cat already has (somehow) a relationship with the inter cat
            if inter_cat.ID in self.relationships:
                continue
            # if they dead (dead cats have no relationships)
            if self.dead or inter_cat.dead:
                continue
            # if they are not outside of the Clan at the same time
            if (
                self.outside
                and not inter_cat.outside
                or not self.outside
                and inter_cat.outside
            ):
                continue
            inter_cat.relationships[self.ID] = Relationship(inter_cat, self)
            self.relationships[inter_cat.ID] = Relationship(self, inter_cat)

    def init_all_relationships(self):
        """Create Relationships to all current Clancats."""
        for ID in self.all_cats:
            the_cat = self.all_cats.get(ID)
            if the_cat.ID is not self.ID:
                mates = the_cat.ID in self.mate
                are_parents = False
                parents = False
                siblings = False

                if (
                    self.parent1 is not None
                    and self.parent2 is not None
                    and the_cat.parent1 is not None
                    and the_cat.parent2 is not None
                ):
                    are_parents = the_cat.ID in [self.parent1, self.parent2]
                    parents = are_parents or self.ID in [
                        the_cat.parent1,
                        the_cat.parent2,
                    ]
                    siblings = self.parent1 in [
                        the_cat.parent1,
                        the_cat.parent2,
                    ] or self.parent2 in [the_cat.parent1, the_cat.parent2]

                related = parents or siblings

                # set the different stats
                romantic_love = 0
                like = 0
                dislike = 0
                admiration = 0
                comfortable = 0
                jealousy = 0
                trust = 0
                if game.settings["random relation"]:
                    if game.clan:
                        if (
                            the_cat == game.clan.instructor
                            and game.clan.instructor.dead_for >= self.moons
                        ):
                            pass
                        elif randint(1, 20) == 1 and romantic_love < 1:
                            dislike = randint(10, 25)
                            jealousy = randint(5, 15)
                            if randint(1, 30) == 1:
                                trust = randint(1, 10)
                        else:
                            like = randint(0, 35)
                            comfortable = randint(0, 25)
                            trust = randint(0, 15)
                            admiration = randint(0, 20)
                            if (
                                randint(1, 100 - like) == 1
                                and self.moons > 11
                                and the_cat.moons > 11
                                and self.age == the_cat.age
                            ):
                                romantic_love = randint(15, 30)
                                comfortable = int(comfortable * 1.3)
                                trust = int(trust * 1.2)
                    else:
                        if randint(1, 20) == 1 and romantic_love < 1:
                            dislike = randint(10, 25)
                            jealousy = randint(5, 15)
                            if randint(1, 30) == 1:
                                trust = randint(1, 10)
                        else:
                            like = randint(0, 35)
                            comfortable = randint(0, 25)
                            trust = randint(0, 15)
                            admiration = randint(0, 20)
                            if (
                                randint(1, 100 - like) == 1
                                and self.moons > 11
                                and the_cat.moons > 11
                                and self.age == the_cat.age
                            ):
                                romantic_love = randint(15, 30)
                                comfortable = int(comfortable * 1.3)
                                trust = int(trust * 1.2)

                if are_parents and like < 60:
                    like = 60
                if siblings and like < 30:
                    like = 30

                rel = Relationship(
                    cat_from=self,
                    cat_to=the_cat,
                    mates=mates,
                    family=related,
                    romantic_love=romantic_love,
                    platonic_like=like,
                    dislike=dislike,
                    admiration=admiration,
                    comfortable=comfortable,
                    jealousy=jealousy,
                    trust=trust,
                )
                self.relationships[the_cat.ID] = rel

    def save_relationship_of_cat(self, relationship_dir):
        # save relationships for each cat

        rel = []
        for r in self.relationships.values():
            r_data = {
                "cat_from_id": r.cat_from.ID,
                "cat_to_id": r.cat_to.ID,
                "mates": r.mates,
                "family": r.family,
                "romantic_love": r.romantic_love,
                "platonic_like": r.platonic_like,
                "dislike": r.dislike,
                "admiration": r.admiration,
                "comfortable": r.comfortable,
                "jealousy": r.jealousy,
                "trust": r.trust,
                "log": r.log,
            }
            rel.append(r_data)

        game.safe_save(f"{relationship_dir}/{self.ID}_relations.json", rel)

    def load_relationship_of_cat(self):
        if game.switches["clan_name"] != "":
            clanname = game.switches["clan_name"]
        else:
            clanname = game.switches["clan_list"][0]

        relation_directory = get_save_dir() + "/" + clanname + "/relationships/"
        relation_cat_directory = relation_directory + self.ID + "_relations.json"

        self.relationships = {}
        if os.path.exists(relation_directory):
            if not os.path.exists(relation_cat_directory):
                self.init_all_relationships()
                for cat in Cat.all_cats.values():
                    cat.create_one_relationship(self)
                return
            try:
                with open(relation_cat_directory, "r", encoding="utf-8") as read_file:
                    rel_data = ujson.loads(read_file.read())
                    for rel in rel_data:
                        cat_to = self.all_cats.get(rel["cat_to_id"])
                        if cat_to is None or rel["cat_to_id"] == self.ID:
                            continue
                        new_rel = Relationship(
                            cat_from=self,
                            cat_to=cat_to,
                            mates=rel["mates"] or False,
                            family=rel["family"] or False,
                            romantic_love=(rel["romantic_love"] or 0),
                            platonic_like=(rel["platonic_like"] or 0),
                            dislike=rel["dislike"] or 0,
                            admiration=rel["admiration"] or 0,
                            comfortable=rel["comfortable"] or 0,
                            jealousy=rel["jealousy"] or 0,
                            trust=rel["trust"] or 0,
                            log=rel["log"],
                        )
                        self.relationships[rel["cat_to_id"]] = new_rel
            except:
                print(
                    f"WARNING: There was an error reading the relationship file of cat #{self}."
                )

    @staticmethod
    def mediate_relationship(mediator, cat1, cat2, allow_romantic, sabotage=False):
        # Gather some important info

        # Gathering the relationships.
        if cat1.ID in cat2.relationships:
            rel1 = cat1.relationships[cat2.ID]
        else:
            rel1 = cat1.create_one_relationship(cat2)

        if cat2.ID in cat1.relationships:
            rel2 = cat2.relationships[cat1.ID]
        else:
            rel2 = cat2.create_one_relationship(cat1)

        # Output string.
        output = ""

        # Determine the chance of failure.
        if mediator.experience_level == "untrained":
            chance = 15
        elif mediator.experience_level == "trainee":
            # Negative bonus for very low.
            chance = 20
        elif mediator.experience_level == "prepared":
            chance = 35
        elif mediator.experience_level == "proficient":
            chance = 55
        elif mediator.experience_level == "expert":
            chance = 70
        elif mediator.experience_level == "master":
            chance = 100
        else:
            chance = 40

        compat = get_personality_compatibility(cat1, cat2)
        if compat is True:
            chance += 10
        elif compat is False:
            chance -= 5

        # Cat's compatibility with mediator also has an effect on success chance.
        for cat in [cat1, cat2]:
            if get_personality_compatibility(cat, mediator) is True:
                chance += 5
            elif get_personality_compatibility(cat, mediator) is False:
                chance -= 5

        # Determine chance to fail, turning sabotage into mediate and mediate into sabotage
        if not int(random() * chance):
            apply_bonus = False
            if sabotage:
                output += "Sabotage Failed!\n"
                sabotage = False
            else:
                output += "Mediate Failed!\n"
                sabotage = True
        else:
            apply_bonus = True
            # EX gain on success
            if mediator.status != "mediator apprentice":
                exp_gain = randint(10, 24)

                gm_modifier = 1
                if game.clan and game.clan.game_mode == "expanded":
                    gm_modifier = 3
                elif game.clan and game.clan.game_mode == "cruel season":
                    gm_modifier = 6

                if mediator.experience_level == "average":
                    lvl_modifier = 1.25
                elif mediator.experience_level == "high":
                    lvl_modifier = 1.75
                elif mediator.experience_level == "master":
                    lvl_modifier = 2
                else:
                    lvl_modifier = 1
                mediator.experience += exp_gain / lvl_modifier / gm_modifier

        if mediator.status == "mediator apprentice":
            mediator.experience += max(randint(1, 6), 1)

        # determine the traits to effect
        # Are they mates?
        mates = rel1.cat_from.ID in rel1.cat_to.mate

        pos_traits = ["platonic", "respect", "comfortable", "trust"]
        if allow_romantic and (mates or cat1.is_potential_mate(cat2)):
            pos_traits.append("romantic")

        neg_traits = ["dislike", "jealousy"]

        # Determine the number of positive traits to effect, and choose the traits
        chosen_pos = sample(pos_traits, k=randint(2, len(pos_traits)))

        # Determine negative trains effected
        neg_traits = sample(neg_traits, k=randint(1, 2))

        if compat is True:
            personality_bonus = 2
        elif compat is False:
            personality_bonus = -2
        else:
            personality_bonus = 0

        # Effects on traits
        for trait in chosen_pos + neg_traits:
            # The EX bonus in not applied upon a fail.
            if apply_bonus:
                if mediator.experience_level == "very low":
                    # Negative bonus for very low.
                    bonus = randint(-2, -1)
                elif mediator.experience_level == "low":
                    bonus = randint(-2, 0)
                elif mediator.experience_level == "high":
                    bonus = randint(1, 3)
                elif mediator.experience_level == "master":
                    bonus = randint(3, 4)
                elif mediator.experience_level == "max":
                    bonus = randint(4, 5)
                else:
                    bonus = 0  # Average gets no bonus.
            else:
                bonus = 0

            if trait == "romantic":
                if mates:
                    ran = (5, 10)
                else:
                    ran = (4, 6)

                if sabotage:
                    rel1.romantic_love = Cat.effect_relation(
                        rel1.romantic_love,
                        -(randint(ran[0], ran[1]) + bonus) + personality_bonus,
                    )
                    rel2.romantic_love = Cat.effect_relation(
                        rel1.romantic_love,
                        -(randint(ran[0], ran[1]) + bonus) + personality_bonus,
                    )
                    output += "Romantic interest decreased. "
                else:
                    rel1.romantic_love = Cat.effect_relation(
                        rel1.romantic_love,
                        (randint(ran[0], ran[1]) + bonus) + personality_bonus,
                    )
                    rel2.romantic_love = Cat.effect_relation(
                        rel2.romantic_love,
                        (randint(ran[0], ran[1]) + bonus) + personality_bonus,
                    )
                    output += "Romantic interest increased. "

            elif trait == "platonic":
                ran = (4, 6)

                if sabotage:
                    rel1.platonic_like = Cat.effect_relation(
                        rel1.platonic_like,
                        -(randint(ran[0], ran[1]) + bonus) + personality_bonus,
                    )
                    rel2.platonic_like = Cat.effect_relation(
                        rel2.platonic_like,
                        -(randint(ran[0], ran[1]) + bonus) + personality_bonus,
                    )
                    output += "Platonic like decreased. "
                else:
                    rel1.platonic_like = Cat.effect_relation(
                        rel1.platonic_like,
                        (randint(ran[0], ran[1]) + bonus) + personality_bonus,
                    )
                    rel2.platonic_like = Cat.effect_relation(
                        rel2.platonic_like,
                        (randint(ran[0], ran[1]) + bonus) + personality_bonus,
                    )
                    output += "Platonic like increased. "

            elif trait == "respect":
                ran = (4, 6)

                if sabotage:
                    rel1.admiration = Cat.effect_relation(
                        rel1.admiration,
                        -(randint(ran[0], ran[1]) + bonus) + personality_bonus,
                    )
                    rel2.admiration = Cat.effect_relation(
                        rel2.admiration,
                        -(randint(ran[0], ran[1]) + bonus) + personality_bonus,
                    )
                    output += "Respect decreased. "
                else:
                    rel1.admiration = Cat.effect_relation(
                        rel1.admiration,
                        (randint(ran[0], ran[1]) + bonus) + personality_bonus,
                    )
                    rel2.admiration = Cat.effect_relation(
                        rel2.admiration,
                        (randint(ran[0], ran[1]) + bonus) + personality_bonus,
                    )
                    output += "Respect increased. "

            elif trait == "comfortable":
                ran = (4, 6)

                if sabotage:
                    rel1.comfortable = Cat.effect_relation(
                        rel1.comfortable,
                        -(randint(ran[0], ran[1]) + bonus) + personality_bonus,
                    )
                    rel2.comfortable = Cat.effect_relation(
                        rel2.comfortable,
                        -(randint(ran[0], ran[1]) + bonus) + personality_bonus,
                    )
                    output += "Comfort decreased. "
                else:
                    rel1.comfortable = Cat.effect_relation(
                        rel1.comfortable,
                        (randint(ran[0], ran[1]) + bonus) + personality_bonus,
                    )
                    rel2.comfortable = Cat.effect_relation(
                        rel2.comfortable,
                        (randint(ran[0], ran[1]) + bonus) + personality_bonus,
                    )
                    output += "Comfort increased. "

            elif trait == "trust":
                ran = (4, 6)

                if sabotage:
                    rel1.trust = Cat.effect_relation(
                        rel1.trust,
                        -(randint(ran[0], ran[1]) + bonus) + personality_bonus,
                    )
                    rel2.trust = Cat.effect_relation(
                        rel2.trust,
                        -(randint(ran[0], ran[1]) + bonus) + personality_bonus,
                    )
                    output += "Trust decreased. "
                else:
                    rel1.trust = Cat.effect_relation(
                        rel1.trust,
                        (randint(ran[0], ran[1]) + bonus) + personality_bonus,
                    )
                    rel2.trust = Cat.effect_relation(
                        rel2.trust,
                        (randint(ran[0], ran[1]) + bonus) + personality_bonus,
                    )
                    output += "Trust increased. "

            elif trait == "dislike":
                ran = (4, 9)
                if sabotage:
                    rel1.dislike = Cat.effect_relation(
                        rel1.dislike,
                        (randint(ran[0], ran[1]) + bonus) - personality_bonus,
                    )
                    rel2.dislike = Cat.effect_relation(
                        rel2.dislike,
                        (randint(ran[0], ran[1]) + bonus) - personality_bonus,
                    )
                    output += "Dislike increased. "
                else:
                    rel1.dislike = Cat.effect_relation(
                        rel1.dislike,
                        -(randint(ran[0], ran[1]) + bonus) - personality_bonus,
                    )
                    rel2.dislike = Cat.effect_relation(
                        rel2.dislike,
                        -(randint(ran[0], ran[1]) + bonus) - personality_bonus,
                    )
                    output += "Dislike decreased. "

            elif trait == "jealousy":
                ran = (4, 6)

                if sabotage:
                    rel1.jealousy = Cat.effect_relation(
                        rel1.jealousy,
                        (randint(ran[0], ran[1]) + bonus) - personality_bonus,
                    )
                    rel2.jealousy = Cat.effect_relation(
                        rel2.jealousy,
                        (randint(ran[0], ran[1]) + bonus) - personality_bonus,
                    )
                    output += "Jealousy increased. "
                else:
                    rel1.jealousy = Cat.effect_relation(
                        rel1.jealousy,
                        -(randint(ran[0], ran[1]) + bonus) - personality_bonus,
                    )
                    rel2.jealousy = Cat.effect_relation(
                        rel2.jealousy,
                        -(randint(ran[0], ran[1]) + bonus) - personality_bonus,
                    )
                    output += "Jealousy decreased . "

        return output

    @staticmethod
    def effect_relation(current_value, effect):
        if effect < 0 and abs(effect) >= current_value:
            return 0

        if effect > 0 and current_value + effect >= 100:
            return 100

        return current_value + effect

    def set_faded(self):
        """This function is for cats that are faded. It will set the sprite and the faded tag"""
        self.faded = True

        # Silhouette sprite
        if self.age == "newborn":
            file_name = "faded_newborn"
        elif self.age == "kitten":
            file_name = "faded_kitten"
        elif self.age in ["adult", "young adult", "senior adult"]:
            file_name = "faded_adult"
        elif self.age == "adolescent":
            file_name = "faded_adol"
        else:
            file_name = "faded_senior"

        if self.df:
            file_name += "_df"

        file_name += ".png"

        self.sprite = image_cache.load_image(
            f"sprites/faded/{file_name}"
        ).convert_alpha()

    @staticmethod
    def fetch_cat(ID: str):
        """Fetches a cat object. Works for both faded and non-faded cats. Returns none if no cat was found."""
        if not ID or isinstance(ID, Cat):  # Check if argument is None or Cat.
            return ID
        elif not isinstance(ID, str):  # Invalid type
            return None
        if ID in Cat.all_cats:
            return Cat.all_cats[ID]
        else:
            return ob if (ob := Cat.load_faded_cat(ID)) else None

    @staticmethod
    def load_faded_cat(cat: str):
        """Loads a faded cat, returning the cat object. This object is saved nowhere else."""

        # just preventing any attempts to load something that isn't a cat ID
        if not cat.isdigit():
            return

        try:
            clan = (
                game.switches["clan_list"][0] if game.clan is None else game.clan.name
            )

            with open(
                get_save_dir() + "/" + clan + "/faded_cats/" + cat + ".json",
                "r",
                encoding="utf-8",
            ) as read_file:
                cat_info = ujson.loads(read_file.read())
                # If loading cats is attempted before the Clan is loaded, we would need to use this.

        except (
            AttributeError
        ):  # NOPE, cats are always loaded before the Clan, so doesn't make sense to throw an error
            with open(
                get_save_dir()
                + "/"
                + game.switches["clan_list"][0]
                + "/faded_cats/"
                + cat
                + ".json",
                "r",
                encoding="utf-8",
            ) as read_file:
                cat_info = ujson.loads(read_file.read())
        except:
            print("ERROR: in loading faded cat")
            return False

        cat_ob = Cat(
            ID=cat_info["ID"],
            prefix=cat_info["name_prefix"],
            suffix=cat_info["name_suffix"],
            status=cat_info["status"],
            moons=cat_info["moons"],
            faded=True,
            df=cat_info["df"] if "df" in cat_info else False,
        )
        if cat_info["parent1"]:
            cat_ob.parent1 = cat_info["parent1"]
        if cat_info["parent2"]:
            cat_ob.parent2 = cat_info["parent2"]
        cat_ob.faded_offspring = cat_info["faded_offspring"]
        cat_ob.adoptive_parents = (
            cat_info["adoptive_parents"] if "adoptive_parents" in cat_info else []
        )
        cat_ob.faded = True
        cat_ob.dead_for = cat_info["dead_for"] if "dead_for" in cat_info else 1

        return cat_ob

    # ---------------------------------------------------------------------------- #
    #                                  Sorting                                     #
    # ---------------------------------------------------------------------------- #

    @staticmethod
    def sort_cats(given_list=None):
        # disable unnecessary lambda in this function
        # pylint: disable=unnecessary-lambda
        if given_list is None:
            given_list = []
        if not given_list:
            given_list = Cat.all_cats_list
        if game.sort_type == "age":
            given_list.sort(key=lambda x: Cat.get_adjusted_age(x))
        elif game.sort_type == "reverse_age":
            given_list.sort(key=lambda x: Cat.get_adjusted_age(x), reverse=True)
        elif game.sort_type == "id":
            given_list.sort(key=lambda x: int(x.ID))
        elif game.sort_type == "reverse_id":
            given_list.sort(key=lambda x: int(x.ID), reverse=True)
        elif game.sort_type == "rank":
            given_list.sort(
                key=lambda x: (Cat.rank_order(x), Cat.get_adjusted_age(x)), reverse=True
            )
        elif game.sort_type == "exp":
            given_list.sort(key=lambda x: x.experience, reverse=True)
        elif game.sort_type == "death":
            given_list.sort(key=lambda x: -1 * int(x.dead_for))

        return

    @staticmethod
    def insert_cat(c: Cat):
        try:
            if game.sort_type == "age":
                bisect.insort(
                    Cat.all_cats_list, c, key=lambda x: Cat.get_adjusted_age(x)
                )
            elif game.sort_type == "reverse_age":
                bisect.insort(
                    Cat.all_cats_list, c, key=lambda x: -1 * Cat.get_adjusted_age(x)
                )
            elif game.sort_type == "rank":
                bisect.insort(
                    Cat.all_cats_list,
                    c,
                    key=lambda x: (
                        -1 * Cat.rank_order(x),
                        -1 * Cat.get_adjusted_age(x),
                    ),
                )
            elif game.sort_type == "exp":
                bisect.insort(Cat.all_cats_list, c, key=lambda x: x.experience)
            elif game.sort_type == "id":
                bisect.insort(Cat.all_cats_list, c, key=lambda x: int(x.ID))
            elif game.sort_type == "reverse_id":
                bisect.insort(Cat.all_cats_list, c, key=lambda x: -1 * int(x.ID))
            elif game.sort_type == "death":
                bisect.insort(Cat.all_cats_list, c, key=lambda x: -1 * int(x.dead_for))
        except (TypeError, NameError):
            # If you are using python 3.8, key is not a supported parameter into insort. Therefore, we'll need to
            # do the slower option of adding the cat, then resorting
            Cat.all_cats_list.append(c)
            Cat.sort_cats()

    @staticmethod
    def rank_order(cat: Cat):
        if cat.status in Cat.rank_sort_order:
            return Cat.rank_sort_order.index(cat.status)
        else:
            return 0

    @staticmethod
    def get_adjusted_age(cat: Cat):
        """Returns the moons + dead_for moons rather than the moons at death for dead cats, so dead cats are sorted by
        total age, rather than age at death"""
        if cat.dead:
            if game.config["sorting"]["sort_rank_by_death"]:
                if game.sort_type == "rank":
                    return cat.dead_for
                else:
                    if game.config["sorting"]["sort_dead_by_total_age"]:
                        return cat.dead_for + cat.moons
                    else:
                        return cat.moons
            else:
                if game.config["sorting"]["sort_dead_by_total_age"]:
                    return cat.dead_for + cat.moons
                else:
                    return cat.moons
        else:
            return cat.moons

    # ---------------------------------------------------------------------------- #
    #                                  properties                                  #
    # ---------------------------------------------------------------------------- #

    @property
    def experience(self):
        return self._experience

    @experience.setter
    def experience(self, exp: int):
        exp = min(exp, self.experience_levels_range["master"][1])
        self._experience = int(exp)

        for x in self.experience_levels_range:
            if (
                self.experience_levels_range[x][0]
                <= exp
                <= self.experience_levels_range[x][1]
            ):
                self.experience_level = x
                break

    @property
    def moons(self):
        return self._moons

    @moons.setter
    def moons(self, value: int):
        self._moons = value

        updated_age = False
        for key_age in self.age_moons.keys():
            if self._moons in range(
                self.age_moons[key_age][0], self.age_moons[key_age][1] + 1
            ):
                updated_age = True
                self.age = key_age
        try:
            if not updated_age and self.age is not None:
                self.age = "senior"
        except AttributeError:
            print(f"ERROR: cat has no age attribute! Cat ID: {self.ID}")

    @property
    def sprite(self):
        # Update the sprite
        update_sprite(self)
        return self._sprite

    @sprite.setter
    def sprite(self, new_sprite):
        self._sprite = new_sprite

    # ---------------------------------------------------------------------------- #
    #                                  other                                       #
    # ---------------------------------------------------------------------------- #

    def is_baby(self):
        return self.age in ["kitten", "newborn"]

    def get_save_dict(self, faded=False):
        if faded:
            return {
                "ID": self.ID,
                "name_prefix": self.name.prefix,
                "name_suffix": self.name.suffix,
                "status": self.status,
                "moons": self.moons,
                "dead_for": self.dead_for,
                "parent1": self.parent1,
                "parent2": self.parent2,
                "adoptive_parents": self.adoptive_parents,
                "df": self.df,
                "faded_offspring": self.faded_offspring,
            }
        else:
            return {
                "ID": self.ID,
                "name_prefix": self.name.prefix,
                "name_suffix": self.name.suffix,
                "specsuffix_hidden": self.name.specsuffix_hidden,
                "gender": self.gender,
                "gender_align": self.genderalign,
                "pronouns": self.pronouns,
                "birth_cooldown": self.birth_cooldown,
                "status": self.status,
                "backstory": self.backstory or None,
                "moons": self.moons,
                "trait": self.personality.trait,
                "facets": self.personality.get_facet_string(),
                "parent1": self.parent1,
                "parent2": self.parent2,
                "adoptive_parents": self.adoptive_parents,
                "mentor": self.mentor or None,
                "former_mentor": (
                    list(self.former_mentor) if self.former_mentor else []
                ),
                "patrol_with_mentor": (self.patrol_with_mentor or 0),
                "mate": self.mate,
                "previous_mates": self.previous_mates,
                "dead": self.dead,
                "paralyzed": self.pelt.paralyzed,
                "no_kits": self.no_kits,
                "no_retire": self.no_retire,
                "no_mates": self.no_mates,
                "exiled": self.exiled,
                "driven_out": self.driven_out,
                "pelt_name": self.pelt.name,
                "pelt_color": self.pelt.colour,
                "pelt_length": self.pelt.length,
                "sprite_kitten": self.pelt.cat_sprites["kitten"],
                "sprite_adolescent": self.pelt.cat_sprites["adolescent"],
                "sprite_adult": self.pelt.cat_sprites["adult"],
                "sprite_senior": self.pelt.cat_sprites["senior"],
                "sprite_para_adult": self.pelt.cat_sprites["para_adult"],
                "eye_colour": self.pelt.eye_colour,
                "eye_colour2": (self.pelt.eye_colour2 or None),
                "reverse": self.pelt.reverse,
                "white_patches": self.pelt.white_patches,
                "vitiligo": self.pelt.vitiligo,
                "points": self.pelt.points,
                "white_patches_tint": self.pelt.white_patches_tint,
                "pattern": self.pelt.pattern,
                "tortie_base": self.pelt.tortiebase,
                "tortie_color": self.pelt.tortiecolour,
                "tortie_pattern": self.pelt.tortiepattern,
                "skin": self.pelt.skin,
                "tint": self.pelt.tint,
                'accessories': self.pelt.accessories if self.pelt.accessories else [],
                "inventory": self.pelt.inventory if self.pelt.inventory else [],
                "skill_dict": self.skills.get_skill_dict(),
                "scars": self.pelt.scars or [],
                "accessory": self.pelt.accessory,
                "experience": self.experience,
                "dead_moons": self.dead_for,
                "current_apprentice": list(self.apprentice),
                "former_apprentices": list(self.former_apprentices),
                "df": self.df,
                "outside": self.outside,
                "faded_offspring": self.faded_offspring,
                "opacity": self.pelt.opacity,
                "prevent_fading": self.prevent_fading,
                "favourite": self.favourite,
            }

    def determine_next_and_previous_cats(self, status: List[str] = None, exclude_status: List[str] = None):
        """Determines where the next and previous buttons point to, relative to this cat.

        :param status: Allows you to constrain the list by status
        """
        sorted_specific_list = [
            check_cat
            for check_cat in Cat.all_cats_list
            if check_cat.dead == self.dead
            and check_cat.outside == self.outside
            and check_cat.df == self.df
            and not check_cat.faded
        ]

        if status is not None:
            sorted_specific_list = [
                check_cat
                for check_cat in sorted_specific_list
                if check_cat.status in status
            ]

        if exclude_status is not None:
            sorted_specific_list = [
                check_cat
                for check_cat in sorted_specific_list
                if check_cat.status not in exclude_status
            ]

        idx = sorted_specific_list.index(self)

        return (
            (
                sorted_specific_list[idx + 1].ID
                if len(sorted_specific_list) > idx + 1
                else 0
            ),
            sorted_specific_list[idx - 1].ID if idx - 1 >= 0 else 0,
        )


# ---------------------------------------------------------------------------- #
#                               END OF CAT CLASS                               #
# ---------------------------------------------------------------------------- #


# Creates a random cat
def create_cat(status, moons=None, biome=None):
    new_cat = Cat(status=status, biome=biome)

    if moons is not None:
        new_cat.moons = moons
    elif new_cat.moons >= 160:
        new_cat.moons = randint(120, 155)
    elif new_cat.moons == 0:
        new_cat.moons = randint(1, 5)

    not_allowed_scars = [
        "NOPAW",
        "NOTAIL",
        "HALFTAIL",
        "NOEAR",
        "BOTHBLIND",
        "RIGHTBLIND",
        "LEFTBLIND",
        "BRIGHTHEART",
        "NOLEFTEAR",
        "NORIGHTEAR",
        "MANLEG",
        "ROTRIDDEN", 
        "ROTMARKED", 
        "FULLBODYBURNS",
        "HALFFACELEFT", 
        "HALFFACERIGHT"
    ]

    for scar in new_cat.pelt.scars:
        if scar in not_allowed_scars:
            new_cat.pelt.scars.remove(scar)

    return new_cat


# Twelve example cats
def create_example_cats():
    warrior_indices = sample(range(12), 3)

    for cat_index in range(12):
        if cat_index in warrior_indices:
            game.choose_cats[cat_index] = create_cat(status="warrior")
        else:
            random_status = choice(
                ["kitten", "apprentice", "warrior", "warrior", "elder"]
            )
            game.choose_cats[cat_index] = create_cat(status=random_status)


# CAT CLASS ITEMS
cat_class = Cat(example=True)
game.cat_class = cat_class

# ---------------------------------------------------------------------------- #
#                                load json files                               #
# ---------------------------------------------------------------------------- #

resource_directory = "resources/dicts/conditions/"

with open(f"{resource_directory}illnesses.json", "r", encoding="utf-8") as read_file:
    ILLNESSES = ujson.loads(read_file.read())

with open(f"{resource_directory}injuries.json", "r", encoding="utf-8") as read_file:
    INJURIES = ujson.loads(read_file.read())

with open(
    f"{resource_directory}permanent_conditions.json", "r", encoding="utf-8"
) as read_file:
    PERMANENT = ujson.loads(read_file.read())

resource_directory = "resources/dicts/events/death/death_reactions/"

with open(f"{resource_directory}minor_major.json", "r", encoding="utf-8") as read_file:
    MINOR_MAJOR_REACTION = ujson.loads(read_file.read())

with open("resources/dicts/lead_ceremony_sc.json", "r", encoding="utf-8") as read_file:
    LEAD_CEREMONY_SC = ujson.loads(read_file.read())

with open("resources/dicts/lead_ceremony_df.json", "r", encoding="utf-8") as read_file:
    LEAD_CEREMONY_DF = ujson.loads(read_file.read())

with open("resources/dicts/backstories.json", "r", encoding="utf-8") as read_file:
    BACKSTORIES = ujson.loads(read_file.read())
