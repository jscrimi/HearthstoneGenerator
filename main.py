import tracery
from tracery.modifiers import base_english
import random

#card parts
#name (string)

#cost (integer 1-10)
#attack (integer)
#health (integer)
#cardClass (NEUTRAL, ROGUE, MAGE, PRIEST, WARLOCK, WARRIOR, DRUID, SHAMAN, HUNTER, PALADIN)
#rarity (COMMON, RARE, EPIC, LEGENDARY)
#tribe ('', ELEMENTAL, BEAST, PIRATE, DEMON, DRAGON, MURLOC, MECH, TOTEM

#text (string, <b>Charge</b> for bolding

#add delimited values to the text fields, go through string, remove those numbers, and add that value to the cost
#delimiter .#add/.#sub
def main():
    print("Creating Hearthstone Card")

    cardTextRules = {
        'origin': ['',
                   '#oneEffect#',
                   '#oneEffect#',
                   '#twoEffect#',
                   '#threeEffect#',
                   '#oneEffect#',
                   '#twoEffect#',
                   '#oneEffect#',
                   '#twoEffect#',
                   '#threeEffect#',
                   '#fourEffect#'],

        'oneEffect': ['#costReduction#',
                      '#battlecry#',
                      '#deathrattle#',
                      '#ability#'],
        'twoEffect': '#ability#, #oneEffect#',
        'threeEffect': '#ability#, #twoEffect#',
        'fourEffect': '#ability#, #ability#, #ability#, #ability#,',


        #standalone effects
        'costModOneOrNone': ['.1add',''],
        'costModOneOrTwo' : ['.1add','.2add'],
        'ability': ['#charge#',
                    '#rush#',
                    '#divineShield#',
                    '#taunt#',
                    '#poisonous#',
                    '#windfury#',
                    '#adapt#',
                    '#lifesteal#',
                    '#stealth#',
                    '#spelldamage#',
                    '#overload#'],
        'charge': '<b>Charge</b>.2add',
        'rush': '<b>Rush</b>.1add',
        'divineShield': '<b>Divine Shield</b>#costModOneOrNone#',
        'taunt': '<b>Taunt</b>#costModOneOrNone#',
        'discover': '<b>Discover</b>',
        'poisonous': '<b>Poisonous</b>.1add',
        'windfury': '<b>Windfury</b>#costModOneOrTwo#',
        'overload': '<b>Overload:</b> (#cNumber#)',
        'adapt': '<b>Adapt</b>',
        'lifesteal': '<b>Lifesteal</b>.1add',
        'stealth': '<b>Stealth</b>#costModOneOrNone#',
        'freeze': '<b>Freeze</b>',
        'spelldamage': ['<b>Spell Damage +1</b>#costModOneOrNone#',
                        '<b>Spell Damage +1</b>#costModOneOrNone#',
                        '<b>Spell Damage +2</b>.2add',
                        '<b>Spell Damage +1</b>#costModOneOrNone#',
                        '<b>Spell Damage +2</b>.2add',
                        '<b>Spell Damage +3</b>.3add'],

        #battlecry logic
        'battlecry': ['<b>Battlecry:</b> #bConditional# #bEffect#..1add',
                      '<b>Battlecry:</b> #bConditional# #bEffect# and #bEffect#..2add',
                      '<b>Battlecry:</b> #bConditional# #bEffect#..1add',
                      '<b>Battlecry:</b> #bConditional# #bEffect# and #bEffect#..2add',
                      '<b>Combo</b> #bEffect#.#costModOneOrTwo#'],
        'bConditional': ['If #who#,','','',''],
        'who': ['you #yWhat#', 'your opponent #oWhat#'],
        'yWhat': ['control #minionControl#',
                  'are holding #minionControl#',
                  'played #minionControl# this turn',
                  'have 10 mana crystals',
                  'played #minionControl# last turn',
                  'only have even-Cost cards in your deck.2sub',
                  'only have odd-Cost cards in your deck.2sub',
                  'have no (#cNumber#) Cost cards in your deck.2sub',
                  'have at least one (#cNumber#) Cost card in your deck.1sub'],
        'oWhat': ['controls #minionControl#',
                  'is holding #minionControl#.1sub',
                  'played #minionControl# last turn.1sub'],
        'minionControl': ['two minions.1sub',
                          'three minions.2sub',
                          'four minions.3sub',
                          'a damaged minion',
                          'an undamaged minion',
                          'a #minionType#',
                          'a #minionType#',
                          'a #minionType#',
                          'a #minionType#',
                          'a #minionType#',
                          'a #minionType# and a #minionType#.1sub',
                          'a #minionType#, a #minionType#, and a #minionType#.1sub'],
        'minionType': ['Beast#mWith#',
                       'Totem#mWith#',
                       'Elemental#mWith#',
                       'Demon#mWith#',
                       'Mech#mWith#',
                       'Pirate#mWith#',
                       'Dragon#mWith#',
                       'Murloc#mWith#',
                       'Treant#mWith#',
                       'Ooze#mWith#',
                       'Legendary Minion',
                       'minion#mWith#',
                       'minion#mWith#',
                       'minion#mWith#',
                       'minion#mWith#',
                       'minion#mWith#'],
        'mWith': ['','','','','','',
                  ' with #number# #stat#.1sub',
                  ' with cost (#cNumber#).1sub',
                  ' with #taunt#',
                  ' with #divineShield#',
                  ' with #rush#.1sub',
                  ' with <b>Deathrattle</b>'],
        'bEffect': ['Deal #dNumber# damage #target#',
                    'Destroy a #minionType#.2add',
                    'Freeze #fTarget#',
                    'Restore #dNumber# Health #target#',
                    'Silence a minion',
                    'Gain #dNumber# Armor',
                    'Gain +#number# #stat#',
                    'Gain #ability#',
                    'Give a friendly #minionType# +#number# #stat#',
                    'Give a friendly #minionType# +#aBNumber#/+#aBNumber#',
                    'Give a friendly #minionType# #ability#',
                    'Give a #minionType# #ability#',
                    'Summon a #aNumber#/#hNumber# #minionType#.1add',
                    'Summon a #aNumber#/#hNumber# #minionType# for your opponent.2sub',
                    '<b>Recruit</b> a #minionType#.2add',
                    'Shuffle #copyOf# into #whoseDeck#',
                    'Add a #aNumber#/#hNumber# #minionType# that costs (#cNumber#) to your hand',
                    'Add a random spell (from your opponents class) to your hand',
                    'Add a random #class# spell to your hand',
                    '#discover# a #minionType#',
                    '#discover# a spell',
                    'Draw a card',
                    'Draw two cards.1add',
                    'Draw three cards.3add',
                    'Discard a card.2sub',
                    'Discard two cards.3sub'],
        'fTarget': ['an enemy',
                    'a random enemy',
                    'a random enemy minion',
                    'a random friendly character,',
                    'an enemy minion',
                    'all minions',
                    'all your other minions',
                    'all enemy minions',
                    'all enemies'],
        'dNumber': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15'],
        'target': ['to your hero',
                   'to a friendly minion',
                   'to the enemy hero',
                   'to an enemy minion',
                   'to a friendly character',
                   'to an enemy',
                   'to a minion',
                   'to a hero',
                   'to both heroes',
                   'to all minions',
                   'to all enemies',
                   'to all friendly characters',
                   'to all enemy minions',
                   'to all friendly minions',
                   'randomly split between all friendly minions',
                   'randomly split between all minions',
                   'randomly split between all enemy minions',
                   'randomly split between all characters',
                   'randomly split between all enemies',
                   'randomly split between all friendly characters',
                   'to #minionControl#',
                   'to a #minionType#'],
        'aNumber': ['0','1', '2', '3', '4', '0','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
        'number': ['1', '2', '3', '4', '0','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
        'hNumber': ['1', '2', '3', '4', '5', '1', '2', '3', '4', '5', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15'],
        'aBNumber': ['1', '2', '3', '4', '5','1', '2', '3', '4', '5','1', '2', '3', '4', '5', '10'],
        'cNumber': ['0','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
        'stat': ['Attack','Health','Cost'],

        'copyOf': ['a copy of a friendly minion',
                   'a copy of an enemy minion',
                   'a friendly minion',
                   'an enemy minion',
                   'a #minionType# that costs (#cNumber#)',
                   'a Scroll of Wonder',
                   'an Ancient Curse',
                   'a Bomb',
                   'a Mine',
                   'an Ambush',
                   'your hand',
                   'a golden copy of a friendly minion',
                   'a golden copy of an enemy minion',
                   '#minionControl#',
                   'your deck',
                   'your opponents deck',
                   'your minions',
                   'all minions'],
        'whoseDeck': ['your deck', 'your opponents deck', 'your hand', 'your opponents hand'],


        # deathrattle logic
        'deathrattle': ['<b>Deathrattle:</b> #dConditional# #dEffect#..1add',
                        '<b>Deathrattle:</b> #dConditional# #dEffect# and #dEffect#..2add'],
        'dConditional': ['If #dwho#.1sub,', '', '', '', '', ''],
        'dwho': ['you #yWhat#', 'your opponent #oWhat#', 'this minion was killed by a #minionType#'],
        'dEffect': ['Deal #dNumber# #dTarget#',
                    'Destroy a random #minionType#',
                    'Freeze #fDTarget#',
                    'Restore #dNumber# Health #dTarget#',
                    'Silence a random minion',
                    'Give your hero #dNumber# Armor',
                    'Give a random friendly #minionType# +#number# #stat#',
                    'Give a random friendly #minionType# +#aBNumber#/+#aBNumber#',
                    'Give a random friendly #minionType# #ability#',
                    'Give a random #minionType# #ability#',
                    'Summon a #aNumber#/#hNumber# #minionType#.1add',
                    'Summon a #aNumber#/#hNumber# #minionType# for your opponent.1sub',
                    '<b>Recruit</b> a #minionType#.2add',
                    'Shuffle #dCopyOf# into #whoseDeck#',
                    'Add a #aNumber#/#hNumber# #minionType# that costs (#cNumber#) to your hand',
                    'Add a random spell (from your opponents class) to your hand',
                    'Add a random #class# spell to your hand',
                    'Draw a card',
                    'Draw two cards.1add',
                    'Draw three cards.3add',
                    'Discard a card.1sub',
                    'Discard two cards.2sub'],
        'fDTarget': ['a random enemy',
                     'a random enemy minion',
                     'a random friendly character,',
                     'a random minion',
                     'all minions',
                     'all your other minions',
                     'all enemy minions',
                     'all enemies'],
        'dTarget': ['to your hero',
                    'to a random friendly minion',
                    'to the enemy hero',
                    'to a random enemy minion',
                    'to a random friendly character',
                    'to a random enemy',
                    'to a random minion',
                    'to a random hero',
                    'to both heroes',
                    'to all minions',
                    'to all enemies',
                    'to all friendly characters',
                    'to all enemy minions',
                    'to all friendly minions',
                    'randomly split between all friendly minions',
                    'randomly split between all minions',
                    'randomly split between all enemy minions',
                    'randomly split between all characters',
                    'randomly split between all enemies',
                    'randomly split between all friendly characters',
                    'to #minionControl#',
                    'to a random #minionType#'],

        'dCopyOf': ['a copy of a random friendly minion',
                    'a copy of an random enemy minion',
                    'a random friendly minion',
                    'a random enemy minion',
                    'a #minionType# that costs (#cNumber#)',
                    'a Scroll of Wonder',
                    'an Ancient Curse',
                    'a Bomb',
                    'a Mine',
                    'an Ambush',
                    'your hand',
                    'a golden copy of a random friendly minion',
                    'a golden copy of a random enemy minion',
                    'your minions',
                    'all minions'],

        #Cost Reduction
        'costReduction': ['Costs (1) less for each #minionType# you played this game.8add.CR',
                          'Costs (1) less for each #minionType# your opponent played this game.6add.CR',
                          'Costs (1) less for each minion your opponent controls.5add.CR',
                          'Costs (1) less for each minion you control.6add.CR',
                          'Costs (1) less for each spell you played this game.10add.CR',
                          'Costs (1) less for each spell your opponent played this game.8add.CR',
                          'Costs (1) less for each card in your hand.7add.CR',
                          'Costs (1) less for each card your opponent has in their hand.6add.CR',
                          'Costs (0) less, improved by <b>Spell Damage</b> twice.8add.CR',
                          'Costs (2) less for each spell you cast this game with cost over (5).10add.CR',
                          'Costs (1) less for each minion that died this turn.7add.CR',
                          'Costs (2) less for each damage your hero has taken this turn.5add.CR',
                          'Costs (1) less for each damage you dealt to the enemy hero this turn.10add.CR',
                          'Costs (1) less for each point of your missing health.10add.CR',
                          'Costs (1) less for each point of health missing from your opponent.10add.CR',
                          'Costs (3) less for each spell you played this turn.9add.CR',
                          'Costs (2) less for each #minionType# on the board.4add.CR',
                          'Controlling a #minionType#, a #minionType#, and a #minionType# reduces the cost of this card by (2) each.3add.CR',
                          'Costs (3) less for each #minionType# that died this game.10add.10add.CR',
                          'This costs (0) if you played #minionControl# this turn.5add.CR',
                          'This costs (10) if it is not the first card you play this turn.3sub.CR',
                          'Costs (2) less for each card you played this turn.5add.CR'],
        'baseStatAttack': ['0','1','2','3','4','5','6','7','8','9','10','12'],
        'baseStatHealth': ['1','2','3','4','5','6','7','8','9','10','12'],
        'baseCardRarity': ['Common','Common','Rare','Common','Rare','Epic','Common','Rare','Epic','Legendary'],
        'baseCardTribe':  ['Minion', 'Minion', 'Minion', 'Minion',
                           'Elemental', 'Beast', 'Pirate', 'Demon', 'Dragon', 'Murloc', 'Mech', 'Totem'],
        'class': ['Mage', 'Priest', 'Shaman', 'Warrior', 'Paladin', 'Rogue', 'Hunter', 'Druid', 'Warlock'],


        #Name Generation Logic
            #All cards will be at least 2 words long
            #Rarity determines adjectives, Tribe determines noun

        'ADJCommon' : ["","","","","Simple", "Faceless", "Giant", "Northern", "Sleepy", "Bone", "Cauldron", "Deranged", "Eldritch",
                       "Fossilized","Violet","Red","Orange", "Faerie", "Yellow","Green","Blue","Purple", "Bog","Captured","Darkmire",
                       "Fearsome", "Furious","Grotesque", "Jade", "Obsidian", "Sated", "Silver", "Gold", "Bronze", "Storm",
                       "Tar", "Wyrm", "Ancient of", "Damaged", "Dark", "Frost", "Gemstudded", "Necrotic", "Ornery",
                       "Priestess of", "Stalking", "Patient", "Spellweaver", "Temple", "Volcanic", "Wind", "Antique",
                       "Blood", "Clockwork", "Cobalt", "Corrosive", "Crazed", "Cryo", "Cult", "Druid of the",
                       "Ethereal", "Fen", "Floating", "Fungal", "Jelly", "Guild", "Kabal", "Mechano", "Nesting", "Pit",
                       "Quartz", "Rotten", "Rusty", "Salty", "Spectral", "Sunborne", "Veno", "Verdant", "Vile"],
        'ADJRare' : ["#ADJCommon#","","", "Doom", "Gilnean", "Grizzled", "Ancient", "Giggling", "Grimestreet", "Knight of the",
                     "Nightscale", "Volcano", "Arcane", "Argent", "Bone", "Book", "Coffin", "Corrupted", "Cruel", "Dino",
                     "Crystal", "Cursed", "Frozen", "Hungry", "Ivory", "Ebony", "Master", "Mechanical", "Metero",
                     "Missile", "Moat", "Possessed", "Security", "Seeping", "Spark", "Tending", "Void", "Wobbling",
                     "Abominable", "Avian", "Azure", "Bewitched", "Bomb", "Bonfire", "Carrion", "Chief", "Corpse",
                     "Collecting","Glacial", "Crystalline", "Volatile", "Dark Iron", "Death", "Despicable", "Direhorn", "Draconic", "Festering", "Grim",
                     "King of", "Lotus", "Onyx", "Second-Rate", "Servant", "Siege", "Sludge", "Spiked", "Stampeding",
                     "Summoning", "Thunder", "Twilight", "Upgraded", "Voodoo", "Ancient", "Animated"],
        'ADJEpic' : ["#ADJCommon#","", "#ADJRare", "Molten", "Arcane", "Clockwork", "Mountain", "Snowfury", "Frost", "Sea",
                     "Blade of the", "Blood", "Hatching", "Obsidian", "Void", "Charged", "Giant", "Sand", "Grand",
                     "Primodial", "Splitting", "Abominable", "Ancient of the", "Astro", "Beryllium", "Blaze", "Bog",
                     "Corridor", "Dreampetal", "Giant", "Midnight", "Twilight", "Spiteful", "Star", "Stone", "Worgen", "Ancient", "Anima", "Black",
                     "Shadow", "Coldarra", "Fight", "Furnacefire", "Glowstone", "Grand", "Leatherclad", "Mossy", "Mysterious",
                     "Nerubian", "Piloted", "Radiant", "Scaled", "Nightmarish", "Reaving", "Skulking", "Spectral", "Big Game",
                     "Bittertide", "Carnivorous", "Crazed", "Dark", "Deathweb", "Earth", "Sky", "Water", "Fire", "Fate",
                     "Fel", "Light", "Glitter", "Gloom", "Holo", "Junk", "Lotus", "Muck", "Necro", "Omega", "Reckless", "Tomb",
                     "Validated", "Vilespine", "Windshear", "Astral", "Crowding", "Cyclopian", "Dread", "Faceless", "Primal"],
        'ADJLegendary' : ["#ADJEpic#", "#ADJEpic#", "#ADJRare#"],

        'NMinion' : ["#NElemental#","#NBeast#","#NPirate#","#NDemon#","#NDragon#","#NMurloc#","#NMech#","#NTotem#"],
        'NElemental' : ["Giant", "Windlord", "Anomaly", "Elemental", "Primal Lord", "Firelord", "Lightlord", "Blazecaller",
                        "Blazecaller", "Caller", "Shaper", "Water Lord", "Sentinel", "Watcher", "Lord", "Crusher", "Worldshaker",
                        "Tyrant", "Ascendent", "Sunshard", "Lurker", "Phoenix", "Destroyer", "Shambler", "Spirit", "Manipulator",
                        "Lightspawn", "Surger", "Chaser", "Thunderhead", "Djinn", "Guardian", "Rager", "Creeper", "Emissary",
                        "Harbinger", "Walker", "Nimbus", "Geode", "Tempest", "Artificer", "Oracle", "Devil", "Fly", "Shard",
                        ""],
        'NBeast' : ["Dinosaur", "Mooneater", "Mastodon", "Kraken", "Devilsaur", "Sand Worm", "Guadian", "Wurm", "Maw",
                    "Jormungar", "Hound", "Creeper", "Anaconda", "Hawk", "Threshadon", "Swamp King", "-saur", "Direhorn"
                    "Stalker", "Highmane", "Hyrda", "Worm", "Widow", "Spider", "Hatchling", "Moth", "Stag", "Beast", "Specimen",
                    "Roc", "Kodo", "Buzzard", "Tiger", "Rhino", "Longneck", "Skitterer", "Grizzly", "Warhorse", "Rager",
                    "Bloatbat", "Megasaur", "Wolf", "Stegodon", "Tallstrider", "Prowler", "Snapjaw", "Pterrordax", "Savage",
                    "Courser", "Cruncher", "Crow", "Elekk", "Bear", "Shark", "Cat", "Fox", "Grub", "Tunneler", "Camel",
                    "Scale", "Bat", "Cobra", "Monkey", "Wasp", "Owl", "Panther", "Raptor", "Patriarch", "Basilisk", "Lizard",
                    "Fledgling", "Parrot", "King"],
        'NPirate' : ["Captain", "Crewman", "Castaway", "Buccaneer", "Dog", "Pirate", "Corsair", "Freebooter", "Squidface",
                     "Lad", "Cultist", "Bloodsail", "Raider", "Cheat", "First Mate", "Deckhand", "Swashbuckler"],
        'NDemon' : ["Lord", "Enforcer", "Abyssal", "Doomguard", "Infernal", "Crusher", "Dreadlord", "Guard", "Watcher",
                    "Prince","Cultist", "Menace","King", "Steed", "Queen", "Inquisitor", "Soul", "Reaver", "Felhound", "Devil", "Demon",
                    "Voidcaller", "Caller", "Piper", "Imp", "Fiend", "Gang Boss", "Nethersoul", "Trickster", "Ripper",
                    "Terror", "Mistress", "Succubus", "Knight of Evil", "Analyst", "Homonculus", "Wrathguard", "Voidwalker",
                    "Walker", "Manipulator", "Descendant", "Darkspawn"],
        'NDragon' : ["Wing", "Dragonlord", "Dragon", "Aspect", "Essence", "Drake", "Dreamweaver", "Maw", "Matriarch", "Wrym",
                     "Crusher", "Darkonid", "Nightmare", "Scalebane", "Scale", "Consort", "Operative", "Sorcerer", "Breaker",
                     "Dragonsmith", "Guardian", "Whelp", "Harbinger"],
        'NMurloc' : ["Seer", "Knight", "Murk-Eye", "Murloc", "Stinger", "Spiritwalker", "Oracle", "Warleader", "Lookout",
                     "Primalfin", "Bilefin", "Blowgill", "Sniper", "Warrior", "Bluegill", "Fish", "Angler", "Tidehunter",
                     "Champion", "Puddlestomper", "Chum", "Raider", "Tidecaller", "Inquisitor", "Tinyfin"],
        'NMech' : ["Giant", "Muncher", "Dozer", "Tank", "Shredder", "Nullifier", "Leviathan", "Curator", "Golem", "Stegotron",
                   "Tron", "Robot", "Mech", "Machine", "Juggernaut", "Launcher", "Sky Golem", "Rover", "Drill", "Burglebot",
                   "Healbot", "3000", "4000", "2000","1000","5000", "Automaton", "Guardian", "Reaver", "Mechano-Egg", "-o-Tron",
                   "Recylcer", "Engine", "Repair Bot", "Wargear", "Gear", "Module", "Crawler", "Cannon", "Wagon", "Reaper",
                   "Menace", "Clunker", "Rager", "Steambot", "Pinata", "Bot", "Gatekeeper", "Demolisher", "Golem", "Leaper",
                   "Spewer", "Bomb", "Rocket", "Robo", "Warper", "Hopper", "Minibot", "Mauler"],
        'NTotem' : ["Totem", "Golem", "Totem", "Totem", "Totem", "Totem", "Golem"]
    }

    grammar = tracery.Grammar(cardTextRules)
    grammar.add_modifiers(base_english)


    cardAttack = int(grammar.flatten("#baseStatAttack#"))
    cardHealth = int(grammar.flatten("#baseStatHealth#"))
    cardBaseCost = ((cardAttack + cardHealth) / 2)
    cardClass = grammar.flatten("#class#")
    cardRarity = grammar.flatten("#baseCardRarity#")
    cardTribe = grammar.flatten("#baseCardTribe#")
    cardText = grammar.flatten("#origin#")

    if (cardRarity == "Common"):
        adjective = grammar.flatten("#ADJCommon#")
    elif (cardRarity == "Rare"):
        adjective = grammar.flatten("#ADJRare#")
    elif (cardRarity == "Epic"):
        adjective = grammar.flatten("#ADJEpic#")
    elif (cardRarity == "Legendary"):
        adjective = grammar.flatten("#ADJLegendary#")
    else:
        adjective = "error"

    changeTribe = random.randint(0,100)
    if(adjective == "void" and changeTribe > 45):
        cardTribe = "Demon"

    if(cardTribe == "Minion"):
        noun = grammar.flatten("#NMinion#")
    elif (cardTribe == "Elemental"):
        noun = grammar.flatten("#NElemental#")
    elif (cardTribe == "Beast"):
        noun = grammar.flatten("#NBeast#")
    elif (cardTribe == "Pirate"):
        noun = grammar.flatten("#NPirate#")
    elif (cardTribe == "Demon"):
        noun = grammar.flatten("#NDemon#")
    elif (cardTribe == "Dragon"):
        noun = grammar.flatten("#NDragon#")
    elif (cardTribe == "Murloc"):
        noun = grammar.flatten("#NMurloc#")
    elif (cardTribe == "Mech"):
        noun = grammar.flatten("#NMech#")
    elif (cardTribe == "Totem"):
        noun = grammar.flatten("#NTotem#")
    else:
        noun = "error"

    cardName = adjective + " " + noun

    if (cardTribe == "Totem"):
        cardClass = "Shaman"
    if (cardTribe == "Dragon"):
        cardBaseCost -= 1
    if (cardClass == "Neutral"):
        cardBaseCost += random.randint(0,1)
    if (cardText.find("Treant") != -1):
        cardClass = "Druid"
    if (cardText.find("Overload") != -1):
        cardClass = "Shaman"
    if (cardText.find("Discard") != -1):
        cardClass = "Warlock"
    if (cardText.find("Combo") != -1):
        cardClass = "Rogue"
    if (cardRarity == "Legendary"):
        cardBaseCost -= 1
    if (cardRarity == "Epic"):
        cardAttack += random.randint(0,1)
        cardHealth += random.randint(0,1)



    cardTextCostAdjustment = 0 \
                             + (cardText.count('.1add') * 1) \
                             + (cardText.count('.2add') * 2) \
                             + (cardText.count('.3add') * 3) \
                             + (cardText.count('.4add') * 4) \
                             + (cardText.count('.5add') * 5) \
                             + (cardText.count('.6add') * 6) \
                             + (cardText.count('.7add') * 7) \
                             + (cardText.count('.8add') * 8) \
                             + (cardText.count('.9add') * 9) \
                             + (cardText.count('.10add') * 10) \
                             - (cardText.count('.1sub') * 1) \
                             - (cardText.count('.2sub') * 2) \
                             - (cardText.count('.3sub') * 3) \
                             - (cardText.count('.4sub') * 4) \
                             - (cardText.count('.5sub') * 5) \
                             - (cardText.count('.6sub') * 6) \
                             - (cardText.count('.7sub') * 7) \
                             - (cardText.count('.8sub') * 8) \
                             - (cardText.count('.9sub') * 9) \
                             - (cardText.count('.10sub') * 10)\
                             - (cardText.count('with') * 1)
    cardText = cardText.replace('.1add', '')
    cardText = cardText.replace('.2add', '')
    cardText = cardText.replace('.3add', '')
    cardText = cardText.replace('.4add', '')
    cardText = cardText.replace('.5add', '')
    cardText = cardText.replace('.6add', '')
    cardText = cardText.replace('.7add', '')
    cardText = cardText.replace('.8add', '')
    cardText = cardText.replace('.9add', '')
    cardText = cardText.replace('.10add', '')
    cardText = cardText.replace('.1sub', '')
    cardText = cardText.replace('.2sub', '')
    cardText = cardText.replace('.3sub', '')
    cardText = cardText.replace('.4sub', '')
    cardText = cardText.replace('.5sub', '')
    cardText = cardText.replace('.6sub', '')
    cardText = cardText.replace('.7sub', '')
    cardText = cardText.replace('.8sub', '')
    cardText = cardText.replace('.9sub', '')
    cardText = cardText.replace('.10sub', '')


    cardCost = cardBaseCost + cardTextCostAdjustment

    if(cardCost > 10 and cardText.find(".CR") == -1):
        cardCost = 10
    if(cardCost < 0):
        cardCost = random.randint(0,1)

    cardText = cardText.replace(".CR","")

    print("Hearthstone Card Created:\n")
    print(cardName)
    print(str(cardCost) + "-Cost " + str(cardAttack) + "/" + str(cardHealth) + " " + cardRarity + " " + cardClass + " " + cardTribe + ".")
    print(cardText)


##End Main##


#Run the main function
if __name__ == "__main__":
    main()