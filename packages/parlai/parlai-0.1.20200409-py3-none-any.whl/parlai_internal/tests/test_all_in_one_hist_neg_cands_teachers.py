#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import unittest

import parlai.utils.testing as testing_utils
from parlai.core.worlds import _create_task_agents
from parlai.scripts.train_model import setup_args


@testing_utils.skipIfCircleCI
class TestAllInOneHistNegCandsTeachers(unittest.TestCase):
    """
    Test the outputs of the first example of many teachers used for all-in-one training,
    including ones trained with history strings as negative candidates.
    """

    def test_check_examples(self):

        # Define all pairs of task strings and examples
        no_header_hist_neg_cands = [
            (
                'internal:neg_hist:control_task=empathetic_dialogues;EmpatheticDialogues',
                {
                    'id': 'neg_hist',
                    'text': 'I remember going to see the fireworks with my best friend. It was the first time we ever spent time alone together. Although there was a lot of people, we felt like the only people in the world.',
                    'labels': [
                        'Was this a friend you were in love with, or just a best friend?'
                    ],
                    'episode_done': False,
                    'hist_labels': [
                        'I remember going to see the fireworks with my best friend. It was the first time we ever spent time alone together. Although there was a lot of people, we felt like the only people in the world.'
                    ],
                    'label_candidates': [
                        'For sure! And always check for the wreckless drivers and the ones who cut you off- Thats really bad in bigger cities. Can never be too careful.',
                        'I do not watch a lot of TV.',
                        "Yeah, it's going to be my first year there, but I'm a junior technically, but yeah I hope I do!",
                        "Wow, that's absurd.. Of course it's the ONE that's impotrant.",
                        'Literally never have been the sane,  But its a life lesson.',
                        'Probably they just fell bad for you, thank god it was not worse.',
                        "Hey there bud, how's it goig?",
                        'not today but last week. Its funny but embarrassing ',
                        'Yeah, it is weird. Your son must be really talented.',
                        'Yeah it is crazy to see things we used to have in our lives every day years later.  Makes you wish you could go back to those days when everything was so easy.',
                        'I do not know if it is stupid to do but i handed my things to a stranger to look out for it',
                        'I am hurting so bad right now.',
                        'Yeah i was really nervous',
                        'I am here now thankfully, it was a learning experience for sure.',
                        'Ha, that is funny',
                        'Was this a friend you were in love with, or just a best friend?',
                        'Man that does sound like a handful!',
                        'One looked jsut a few years older.',
                        'I remember going to see the fireworks with my best friend. It was the first time we ever spent time alone together. Although there was a lot of people, we felt like the only people in the world.',
                        'Saw a person who seemed very sick and unhealthy..spit intheir hands..sneeze in them..sling it everywhere..then touch the doorhandle to the store',
                    ],
                },
            ),
            (
                'internal:neg_hist:control_task=wizard_of_wikipedia;BasicApprenticeDialog:add_topic=False',
                {
                    'id': 'neg_hist',
                    'text': "I think science fiction is an amazing genre for anything. Future science, technology, time travel, FTL travel, they're all such interesting concepts.",
                    'labels': ["I'm a huge fan of science fiction myself! "],
                    'episode_done': False,
                    'hist_labels': [
                        "I think science fiction is an amazing genre for anything. Future science, technology, time travel, FTL travel, they're all such interesting concepts."
                    ],
                    'label_candidates': [
                        'I more so need to choose the right dog breed for my lifestyle.',
                        'Nicholas Sparks was born on December 31, 1965 in Omaha, Nebraska ',
                        'Oh nice. I love mountains. Its not something I am used to. Has it been around for a while?',
                        'Are red heads the only people that have that recessive allele on chromosome 16?',
                        "I think science fiction is an amazing genre for anything. Future science, technology, time travel, FTL travel, they're all such interestingconcepts.",
                        'I believe the phrase was coined when animals or stray livestock would have to be penned or "impounded" until claimed by whoever owned them.',
                        "Ever watched Grey's Anatomy. It is a pretty good show.",
                        'Oh, so it was named after him? Is there any specific features a bowie knife has?',
                        'Baked goods are very popular and have been throughout history',
                        'I have to come to camp because of Summer School, but we try to make it fun anyways. I meet new people. ',
                        'Sausage, I got it from a street fair!',
                        'another thing i love about Barbershop music is that it consists of four-part chords for every melody note in a predominantly .',
                        'I like all the different colors I can use',
                        'Thats what I have heard as well',
                        "Ah! I wasn't sure. And that's a *lot* of fender-benders!",
                        'I never realized that. What do lizards usually eat?',
                        'I think I am somewhat familiar with him and his art',
                        "I'm a huge fan of science fiction myself! ",
                        'My favourite colour is blue.  Is is one of the three primary colours.  What about you?',
                        'What other categories of plant can be grown in a garden,especially the scented ones?',
                    ],
                },
            ),
            (
                'internal:neg_hist:control_task=wizard_of_wikipedia;BasicWizardDialog:add_topic=False',
                {
                    'id': 'neg_hist',
                    'text': "I'm a huge fan of science fiction myself! ",
                    'labels': [
                        'Awesome! I really love how sci-fi storytellers focus on political/social/philosophical issues that would still be around even in the future. Makes them relatable.'
                    ],
                    'episode_done': False,
                    'hist_labels': ["I'm a huge fan of science fiction myself! "],
                    'label_candidates': [
                        'I have not heard of that before. tell me more about Iguanas please',
                        'Try traveling with red hair on airline flights ! lol. Some cultures ridicule us, some admire us. ',
                        'That actually sounds awful! I have had so many cats since childhood I lost count. But once I got a dog I feel in love!',
                        'I also love biscuits! You can beat a good soft biscuit!',
                        'Perfection! Any particular reason you chose that weapon? I\'ve actually used that in defense, ha! Or "was" going to',
                        'I am planning to move to London once I retire!',
                        'Yes, I believe his son took over at some point,',
                        "I think I read it in my Intro to Philosophy course in college. I can't remember a damn thing about it, though.",
                        "Honestly, no. The closest I've been is one built in an airport to attract tourists and travelers in Vegas.",
                        'Is it popular only in the United States or in other countries as well?',
                        'Oh yeah. I love to use a tub and justsit down there for minutes ',
                        'It is superficial. I notice that most models are tall.',
                        'Who makes the Honda Civic?',
                        "I think they're founders  Steve Jobs, Steve Wozniak, and Ronald Wayne would beg to differ!",
                        "Yes! The comedy of the writing lies in the depiction of manners, education, marriage, and money during the British Regency period; so it's interesting",
                        "If you haven't seen many Broadway shows, I recommend taking a trip to New York and going to their theatre district. If you can get Hamilton tickets, it's a must!",
                        'Interesting.  What kind of law are you interested in?',
                        'Awesome! I really love how sci-fi storytellers focus on political/social/philosophical issues that would still be around even in the future. Makes them relatable.',
                        "I'm a huge fan of science fiction myself! ",
                        'can you use eaving to make a scarf?',
                    ],
                },
            ),
        ]
        no_header_normal = [
            (
                'empathetic_dialogues',
                {
                    'situation': 'I remember going to the fireworks with my best friend. There was a lot of people, but it only felt like us in the world.',
                    'emotion': 'sentimental',
                    'text': 'I remember going to see the fireworks with my best friend. It was the first time we ever spent time alone together. Although there was a lot of people, we felt like the only people in the world.',
                    'labels': [
                        'Was this a friend you were in love with, or just a best friend?'
                    ],
                    'prepend_ctx': None,
                    'prepend_cand': None,
                    'deepmoji_ctx': None,
                    'deepmoji_cand': None,
                    'episode_done': False,
                    'label_candidates': [],
                },
            ),
            (
                'wizard_of_wikipedia',
                {
                    'id': 'WizardDialogKnowledgeTeacher',
                    'text': 'Science fiction',
                    'labels': [
                        "I think science fiction is an amazing genre for anything. Future science, technology, time travel, FTL travel, they're all such interesting concepts."
                    ],
                    'chosen_topic': 'Science fiction',
                    'episode_done': False,
                    'label_candidates': [],
                    'knowledge': 'Science fiction Science fiction (often shortened to SF or sci-fi) is a genre of speculative fiction, typically dealing with imaginative concepts such as futuristic science and technology, space travel, time travel, faster than light travel, parallel universes, and extraterrestrial life.\nScience fiction Science fiction often explores the potential consequences of scientific and other innovations, and has been called a "literature of ideas".\nScience fiction It usually avoids the supernatural, unlike the related genre of fantasy.\nScience fiction Historically, science-fiction stories have had a grounding in actual science, but now this is only expected of hard science fiction.\nScience fiction Science fiction is difficult to define, as it includes a wide range of subgenres and themes.\nScience fiction Hugo Gernsback, who suggested the term "scientifiction" for his "Amazing Stories" magazine, wrote: "By \'scientifiction\' I mean the Jules Verne, H. G. Wells and Edgar Allan Poe type of story—a charming romance intermingled with scientific fact and prophetic vision... Not only do these amazing tales make tremendously interesting reading—they are always instructive.\nScience fiction They supply knowledge... in a very palatable form... New adventures pictured for us in the scientifiction of today are not at all impossible of realization tomorrow...\n',
                    'title': 'Science fiction',
                    'checked_sentence': 'Science fiction (often shortened to SF or sci-fi) is a genre of speculative fiction, typically dealing with imaginative concepts such as futuristic science and technology, space travel, time travel, faster than light travel, parallel universes, and extraterrestrial life.',
                },
            ),
            (
                'wizard_of_wikipedia:BasicApprenticeDialog:add_topic=False',
                {
                    'id': 'WizardBasicDialog',
                    'text': "I think science fiction is an amazing genre for anything. Future science, technology, time travel, FTL travel, they're all such interesting concepts.",
                    'labels': ["I'm a huge fan of science fiction myself! "],
                    'episode_done': False,
                },
            ),
            (
                'wizard_of_wikipedia:BasicWizardDialog:add_topic=False',
                {
                    'id': 'WizardBasicDialog',
                    'text': "I'm a huge fan of science fiction myself! ",
                    'labels': [
                        'Awesome! I really love how sci-fi storytellers focus on political/social/philosophical issues that would still be around even in the future. Makes them relatable.'
                    ],
                    'episode_done': False,
                    'chosen_topic': 'Science fiction',
                },
            ),
        ]
        persona_and_topic_hist_neg_cands = [
            (
                "internal:neg_hist:control_task=parlai.tasks.convai2.agents;PersonaTopicifierTeacher",
                {
                    'id': 'neg_hist',
                    'text': "your persona: i like to remodel homes.\nyour persona: i like to go hunting.\nyour persona: i like to shoot a bow.\nyour persona: my favorite holiday is halloween.\nNicholas Sparks\nhi , how are you doing ? i'm getting ready to do some cheetah chasing to stay in shape .",
                    'labels': (
                        'you must be very fast . hunting is one of my favorite hobbies .',
                    ),
                    'episode_done': False,
                    'hist_labels': [
                        "hi , how are you doing ? i'm getting ready to do some cheetah chasing to stay in shape ."
                    ],
                    'label_candidates': [
                        'can you buy iron in the mail ?',
                        'no . i just watch tv . the godfather , mostly .',
                        'you have some pretty bad luck there .',
                        'you must be very fast . hunting is one of my favorite hobbies .',
                        "as long as there are no flowers i don't like them",
                        'oh , okay . i am a dr . what are you going to go to college for ?',
                        'so do you like fish do you eat those',
                        "yeah i've been hanging out with a girl from work . she's cute",
                        'i am currently engaged and am a little bit crazy with wedding planning lol',
                        "i don't watch much tv . being a nurse takes up all ofmy free time .",
                        'i do not have a favorite .',
                        'he is always playing over our mcdonalds speaker .',
                        'thanks though . where are you from ?',
                        "hi , how are you doing ? i'm getting ready to do some cheetah chasing to stay in shape .",
                        "i try to go as much as possible as of today i've been to 40",
                        'yum , love seafood , too . could eat salmon , shrimp , all the time',
                        'thanks . what are your hobbies ?',
                        'cool ! i work with marketing stuff . i love it .',
                        "oh no . i'm sorry to hear that . that is sad",
                        'i do ! we have a kevin at the church mydad preached at !',
                    ],
                },
            ),
            (
                "internal:neg_hist:control_task=parlai_internal.tasks.empathetic_dialogues.agents;PersonaTopicifierTeacher",
                {
                    'id': 'neg_hist',
                    'text': 'your persona: people hate that i obsess about the poor.\nyour persona: i like to make cellphone apps that would help heal our world.\nyour persona: i like to watch people pray together.\nyour persona: people don t like me too much but i like them anyways.\nAndroid (operating system)#Applications\nI remember going to see the fireworks with my best friend. It was the first time we ever spent time alone together. Although there was a lot of people, we felt like the only people in the world.',
                    'labels': [
                        'Was this a friend you were in love with, or just a best friend?'
                    ],
                    'episode_done': False,
                    'hist_labels': [
                        'I remember going to see the fireworks with my best friend. It was the first time we ever spent time alone together. Although there was a lot of people, we felt like the only people in the world.'
                    ],
                    'label_candidates': [
                        'It was only his second competition.  He did a lot better than I expected',
                        'I felt bad for firing her',
                        'That sounds awesome! Have you guys been friends long?',
                        'Have you made a formal complaint against them yet?',
                        'shame on him. How did you find out?',
                        "Every year I'm so excited about Christmas and have all these plans.",
                        "I just don't understand why they let themselves go.",
                        "Yes. I hope so! It's one little step but it's a big one for him to do on his own.",
                        'I tried following a recipe for vegan cookies and they turned out horribly.',
                        'I budgeted for a year to make sure I could afford it. Well worth it!',
                        "Ghost in the graveyard was a blast! I can't believe I forgot that one. It sounds like we both had great childhoods.",
                        'I am so glad that I wake up every day!',
                        'i went to a new restaurant that has been getting bad reviews, it was actually really good.',
                        'No!!! gross... did you flip? ',
                        'I really am, I had bad teeth my entire lifebecause of genetic reasons.',
                        'Was this a friend you were in love with, or just a best friend?',
                        'The perfect person for you will come soon enough',
                        'I remember going to see the fireworks with my best friend. It was the first time we ever spent time alone together. Although there was a lot of people, we felt like the only people in the world.',
                        'thats no goodat all! you may feel better after you sleep yeah?',
                        'She left me. I believed she would never cheat on me until she told me she was dating another guy',
                    ],
                },
            ),
            (
                "internal:neg_hist:control_task=parlai.tasks.wizard_of_wikipedia.agents;BasicPersonaTopicifierTeacher:speaker_label=apprentice:add_topic=True",
                {
                    'id': 'neg_hist',
                    'text': "your persona: not a day goes by that i don't drink four mountain dews.\nyour persona: i enjoy movies about aliens invading the earth.\nyour persona: my favorite hobby is chess.\nyour persona: i just dyed my hair hot pink with purple highlights.\nScience fiction\nI think science fiction is an amazing genre for anything. Future science, technology, time travel, FTL travel, they're all such interesting concepts.",
                    'labels': ["I'm a huge fan of science fiction myself! "],
                    'episode_done': False,
                    'hist_labels': [
                        "I think science fiction is an amazing genre for anything. Future science, technology, time travel, FTL travel, they're all such interesting concepts."
                    ],
                    'label_candidates': [
                        'Sorry about that, I should have said his first name. Mick Taylor who was born 17 January 1949 was the lead bassist for the rolling stones from 1969-1974.',
                        'Sometimes that happens to a lotof people.',
                        "Wow that's so long ago for such a relatively unknown university.",
                        'There are also differences as for the obligation, liabilities  and powers between an estate agent in the UK and a real estate broker in the US.  ',
                        'Yes, I could probably get into it if I tried.',
                        'I love Electronic Music! It uses instruments and mechanical elements while missing in others standard instruments! Its usually called "EDM". What kind of music do you listen to?',
                        'Interesting, I did not know that! Every wedding I have been to has had an edible cake. I wonder why only the grooms get to eat the cake at some weddings!',
                        "I think science fiction is an amazing genre for anything. Future science, technology, time travel, FTL travel, they're all such interesting concepts.",
                        'I am not sure, but what is your favorite shade of green? What hue do you prefer?',
                        "That's so amazing. What's the farthest distance in space that humans have explored?",
                        'Oh for sure, those Doritos flavored nacho cheese tacos are the best!',
                        'what kind of puzzles do you like? word search? crossword? logic or number puzzles?',
                        'Interesting. My favorite book series as a kid was The Magic Treehouse series.',
                        'are they paid well?',
                        'I work at a memorial hospital.  Have you watched the show general hospital?',
                        'Alright, so what would you say is your favourite keto meal?',
                        "I'm a huge fan of science fiction myself! ",
                        'Beer has been brewed on a domestic level for years now too',
                        'It is the third least popular state in the US, and the most sparsely populated. ',
                        'I enjoy some of it, yes.',
                    ],
                },
            ),
            (
                "internal:neg_hist:control_task=parlai.tasks.wizard_of_wikipedia.agents;BasicPersonaTopicifierTeacher:speaker_label=wizard:add_topic=True",
                {
                    'id': 'neg_hist',
                    'text': "your persona: not a day goes by that i don't drink four mountain dews.\nyour persona: i enjoy movies about aliens invading the earth.\nyour persona: my favorite hobby is chess.\nyour persona: i just dyed my hair hot pink with purple highlights.\nScience fiction\nI'm a huge fan of science fiction myself!",
                    'labels': [
                        'Awesome! I really love how sci-fi storytellers focus on political/social/philosophical issues that would still be around even in the future. Makes them relatable.'
                    ],
                    'episode_done': False,
                    'hist_labels': ["I'm a huge fan of science fiction myself!"],
                    'label_candidates': [
                        "Sounds delicious!  I'm getting hungry.  One of the placed I would like to visit in Mexico are the pyramids, do you know anything about them?",
                        'Yes the team of engineers who work at IBM are very smart.  Steve Jobs had a lot of vision as well. ',
                        'Have you ever cooked professionally as a chef, or mainly just in your own home?',
                        'When did Spider-Man first come out?',
                        'That makes sense, finding a good balance is always a key to a good diet. Too much of one type offood can be unhealthy for anyone.',
                        "That's a good choice! You know, Steve jobs instructed his employees to investigate touch screen devices and later they invented iphone",
                        'I dont know much about either of those sports.',
                        'I am not sure, but they are eaten raw, and in sauces',
                        'Did he put it together himself?',
                        'For sure and the interest and penalties accumulate over time. I cut all my cards up lol.',
                        'What kind of music do you actually like?',
                        'Oh wait I just made a decision, I want to be a dietary vegan because  I wont be consuming animal products, not only meat but also eggs, dairy products and other animal-derived substances',
                        "I'm a huge fan of science fiction myself!",
                        'Yes, that was a great one. They evenhad a tv series based of it, Bates Motel. Did you watch any of it?',
                        'How do you like Donald Trump currently as our president?',
                        'That is just awful. I have definitely seen some horses in dire situations and reached out to my local chapter',
                        'What exactly is The Royal Ballet?',
                        'Awesome! I really love how sci-fi storytellers focus on political/social/philosophical issues that would still be around even in the future. Makes them relatable.',
                        'I never really understood why swimming was relatively short compared to running and bicycling.',
                        'yea even two jobs isnt enough these days',
                    ],
                },
            ),
        ]
        persona_and_topic_normal = [
            (
                "parlai.tasks.convai2.agents:PersonaTopicifierTeacher",
                {
                    'text': "your persona: i like to remodel homes.\nyour persona: i like to go hunting.\nyour persona: i like to shoot a bow.\nyour persona: my favorite holiday is halloween.\nNicholas Sparks\nhi , how are you doing ? i'm getting ready to do some cheetah chasing to stay in shape .",
                    'labels': (
                        'you must be very fast . hunting is one of my favorite hobbies .',
                    ),
                    'reward': 0,
                    'label_candidates': (
                        'my mom was single with 3 boys , so we never left the projects .',
                        'i try to wear all black every day . it makes me feel comfortable .',
                        'well nursing stresses you out so i wish luck with sister',
                        'yeah just want to pick up nba nfl getting old',
                        'i really like celine dion . what about you ?',
                        'no . i live near farms .',
                        "i wish i had a daughter , i'm a boy mom . they're beautiful boys though still lucky",
                        'yeah when i get bored i play gone with the wind my favorite movie .',
                        "hi how are you ? i'm eatingdinner with my hubby and 2 kids .",
                        'were you married to your high school sweetheart ? i was .',
                        'that is great to hear ! are you a competitive rider ?',
                        "hi , i'm doing ok . i'm abanker . how about you ?",
                        "i'm 5 years old",
                        'hi there . how are you today ?',
                        'i totally understand how stressful that can be .',
                        'yeah sometimes you do not know what you are actually watching',
                        'mother taught me to cook ! we are looking for an exterminator .',
                        'i enjoy romantic movie . what is your favorite season ? mine is summer .',
                        'editing photos takesa lot of work .',
                        'you must be very fast . hunting is one of my favorite hobbies .',
                    ),
                    'episode_done': False,
                },
            ),
            (
                "parlai_internal.tasks.empathetic_dialogues.agents:PersonaTopicifierTeacher",
                {
                    'situation': 'I remember going to the fireworks with my best friend. There was a lot of people, but it only felt like us in the world.',
                    'emotion': 'sentimental',
                    'text': 'your persona: people hate that i obsess about the poor.\nyour persona: i like to make cellphone apps that would help heal our world.\nyour persona: i like to watch people pray together.\nyour persona: people don t like me too much but i like them anyways.\nAndroid (operating system)#Applications\nI remember going to see the fireworks with my best friend. It was the first time we ever spent time alone together. Although there was a lot of people, we felt like the only people in the world.',
                    'labels': [
                        'Was this a friend you were in love with, or just a best friend?'
                    ],
                    'prepend_ctx': None,
                    'prepend_cand': None,
                    'deepmoji_ctx': None,
                    'deepmoji_cand': None,
                    'episode_done': False,
                    'label_candidates': [],
                },
            ),
            (
                "parlai.tasks.wizard_of_wikipedia.agents:PersonaTopicifierTeacher",
                {
                    'id': 'WizardDialogKnowledgeTeacher',
                    'text': "your persona: not a day goes by that i don't drink four mountain dews.\nyour persona: i enjoy movies about aliens invading the earth.\nyour persona: my favorite hobby is chess.\nyour persona: i just dyed my hair hot pink with purple highlights.\nScience fiction\n",
                    'labels': [
                        "I think science fiction is an amazing genre for anything. Future science, technology, time travel, FTL travel, they're all such interesting concepts."
                    ],
                    'chosen_topic': 'Science fiction',
                    'episode_done': False,
                    'label_candidates': [],
                    'knowledge': 'Science fiction Science fiction (often shortened to SF or sci-fi) is a genre of speculative fiction, typically dealing with imaginative concepts such as futuristic science and technology, space travel, time travel, faster than light travel, parallel universes, and extraterrestrial life.\nScience fiction Science fiction often explores the potential consequences of scientific and other innovations, and has been called a "literature of ideas".\nScience fiction It usually avoids the supernatural, unlike the related genre of fantasy.\nScience fiction Historically, science-fiction stories have had a grounding in actual science, but now this is only expected of hard science fiction.\nScience fiction Science fiction is difficult to define, as it includes a wide range of subgenres and themes.\nScience fiction Hugo Gernsback, who suggested the term "scientifiction" for his "Amazing Stories" magazine, wrote: "By \'scientifiction\' I mean the Jules Verne, H. G. Wells and Edgar Allan Poe type of story—a charming romance intermingled with scientific fact and prophetic vision... Not only do these amazing tales make tremendously interesting reading—they are always instructive.\nScience fiction They supply knowledge... in a very palatable form... New adventures pictured for us in the scientifiction of today are not at all impossible of realization tomorrow...\n',
                    'title': 'Science fiction',
                    'checked_sentence': 'Science fiction (often shortened to SF or sci-fi) is a genre of speculative fiction, typically dealing with imaginative concepts such as futuristic science and technology, space travel, time travel, faster than light travel, parallel universes, and extraterrestrial life.',
                },
            ),
            (
                "parlai.tasks.wizard_of_wikipedia.agents:BasicPersonaTopicifierTeacher:speaker_label=apprentice:add_topic=True",
                {
                    'id': 'WizardBasicDialog',
                    'text': "your persona: not a day goes by that i don't drink four mountain dews.\nyour persona: i enjoy movies about aliens invading the earth.\nyour persona: my favorite hobby is chess.\nyour persona: i just dyed my hair hot pink with purple highlights.\nScience fiction\nI think science fiction is an amazing genre for anything. Future science, technology, time travel, FTL travel, they're all such interesting concepts.",
                    'labels': ["I'm a huge fan of science fiction myself! "],
                    'episode_done': False,
                },
            ),
            (
                "parlai.tasks.wizard_of_wikipedia.agents:BasicPersonaTopicifierTeacher:speaker_label=wizard:add_topic=True",
                {
                    'id': 'WizardBasicDialog',
                    'text': "your persona: not a day goes by that i don't drink four mountain dews.\nyour persona: i enjoy movies about aliens invading the earth.\nyour persona: my favorite hobby is chess.\nyour persona: i just dyed my hair hot pink with purple highlights.\nScience fiction\nI'm a huge fan of science fiction myself!",
                    'labels': [
                        'Awesome! I really love how sci-fi storytellers focus on political/social/philosophical issues that would still be around even in the future. Makes them relatable.'
                    ],
                    'episode_done': False,
                    'chosen_topic': 'Science fiction',
                },
            ),
        ]
        all_tasks_and_messages = (
            no_header_hist_neg_cands
            + no_header_normal
            + persona_and_topic_hist_neg_cands
            + persona_and_topic_normal
        )

        for task_string, desired_message in all_tasks_and_messages:

            # Get message
            parser = setup_args()
            opt = parser.parse_args(['-t', task_string, '-dt', 'train:ordered'])
            teacher = _create_task_agents(opt)[0]
            # We use this function because that's what's called in train_model.py
            actual_message = teacher.get(episode_idx=0, entry_idx=0)

            print(f'\nChecking {task_string}:')
            for key in desired_message.keys():
                if key in ['label_candidates']:
                    # These are often created randomly and thus will vary
                    continue
                print(key)
                self.assertEqual(desired_message[key], actual_message[key])
            print('')


if __name__ == '__main__':
    unittest.main()
