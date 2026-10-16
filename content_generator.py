import random

# Procedural generation engine to create 100+ unique interactive stories
STORY_LOCATIONS = [
    "at the grocery store", "at the playground", "in the classroom", 
    "in the school cafeteria", "at a birthday party", "in the library", 
    "on the school bus", "at the doctor's office", "in a busy restaurant",
    "at the movie theater"
]

STORY_TRIGGERS = [
    ("it gets very loud and crowded", "Sensory Overload"),
    ("the lights are too bright and buzzing", "Sensory Overload"),
    ("a fire alarm suddenly goes off", "Sensory Overload"),
    ("someone takes a toy you were playing with", "Conflict"),
    ("someone cuts in front of you in line", "Conflict"),
    ("a classmate says something unkind", "Conflict"),
    ("you don't know anyone and feel shy", "Social Anxiety"),
    ("you are asked to speak in front of everyone", "Social Anxiety"),
    ("you want to join a game but don't know how to ask", "Social Anxiety"),
    ("the daily schedule suddenly changes without warning", "Routine Disruption"),
    ("your favorite food is sold out", "Routine Disruption"),
    ("you drop your snack on the floor", "Accident"),
    ("someone bumps into you and makes you drop your book", "Accident")
]

def generate_stories(count=3):
    stories = []
    # Ensure we don't pick the exact same combo in one batch
    combos = random.sample(STORY_TRIGGERS, min(count, len(STORY_TRIGGERS)))
    
    for trigger, category in combos:
        loc = random.choice(STORY_LOCATIONS)
        scenario = f"You are **{loc}** and suddenly **{trigger}**. How should you handle this?"
        
        if category == "Sensory Overload":
            options = [
                ("Cover your ears, close your eyes, and take deep breaths 🧘", True, "Great choice! Deep breaths and blocking noise helps calm your nervous system."),
                ("Scream loudly and run away 🏃", False, "Running away might not be safe. Try finding a quiet corner with a trusted adult instead.")
            ]
        elif category == "Conflict":
            options = [
                ("Use your words and say 'Please don't do that, I don't like it' 🗣️", True, "Perfect! Using your words calmly is the best way to solve a problem and set boundaries."),
                ("Push them or yell at them 😠", False, "Physical actions or yelling can cause someone to get hurt. Always try using your words or asking an adult for help.")
            ]
        elif category == "Social Anxiety":
            options = [
                ("Take a deep breath and say 'Hi' or ask 'Can I play?' 👋", True, "Awesome! Starting small and asking to join is a brave and wonderful step."),
                ("Hide and refuse to talk to anyone 🙈", False, "Hiding won't help you feel better in the long run. Try finding a teacher or parent to help you say hi.")
            ]
        elif category == "Routine Disruption":
            options = [
                ("Look at your visual schedule or ask an adult what the new plan is 📅", True, "Excellent! Checking your schedule and asking for help makes sudden changes much easier."),
                ("Throw your things on the floor 😤", False, "Changes can be frustrating, but throwing things won't fix it. Take a breath and ask an adult for the new plan.")
            ]
        else: # Accident
            options = [
                ("Tell an adult what happened so they can help you clean it up or fix it 🧹", True, "Great job! Accidents happen to everyone, and adults are there to help."),
                ("Cry and run away so you don't get in trouble 😭", False, "It's okay to feel upset, but it's important to be honest. Adults will help you fix it, you won't be in trouble!")
            ]
            
        random.shuffle(options)
        stories.append({"scenario": scenario, "options": options})
    return stories

# Procedural generation for 100+ unique emotion scenarios
EMOTION_SUBJECTS = ["Your best friend", "Your classmate", "Your sibling", "Your teacher", "A new student"]
EMOTION_EVENTS = [
    ("drops their favorite ice cream on the ground", "Sad 😢"),
    ("loses their favorite book", "Sad 😢"),
    ("falls down and scrapes their knee", "Sad 😢"),
    ("wins a gold medal in the race", "Happy 😊"),
    ("gets a surprise birthday present", "Happy 😊"),
    ("is told they did an amazing job on their drawing", "Happy 😊"),
    ("cannot figure out a really hard math problem", "Frustrated 😤"),
    ("has to wait a very long time in line", "Frustrated 😤"),
    ("builds a tall tower and someone knocks it over accidentally", "Frustrated 😤"),
    ("hears a very loud scary noise outside", "Scared 😨"),
    ("sees a big spider crawling near their desk", "Scared 😨")
]

def generate_emotions(count=3):
    emotions = []
    combos = random.sample(EMOTION_EVENTS, min(count, len(EMOTION_EVENTS)))
    
    for event, answer in combos:
        sub = random.choice(EMOTION_SUBJECTS)
        scenario = f"{sub} **{event}**. How do they most likely feel?"
        
        options = ["Happy 😊", "Sad 😢", "Frustrated 😤", "Scared 😨"]
        emotions.append({"scenario": scenario, "options": options, "answer": answer})
    return emotions
