# README

This repository is a small project of a kata with a simple goal: write a secret santa list generator

## Rules

1. Each person must gift 1 and only 1 gift
2. Each person must receive 1 and only 1 gift
3. There can't be any reciprocity: If A gift to B, B can't gift to A
4. There can't be gift between couples: If A and B are together, A can't gift to B and B can't gift to A

## The project

The project has been developed in python. With a pretty simple algorithm with some optimization to avoid dead-end
(when not everyone has been gifted but there is no option to gift).
It will take as input list of people and list of couples like so

``` python
PEOPLE = ["Florent", "Jessica", "Coline", "Emilien", "Ambroise", "Bastien"]
COUPLES = [("Florent", "Jessica"), ("Coline", "Emilien")]
```

### Implementation

The main logic is held by a dict. Its keys are people and its value are set of people to which the key can't gift
(for example its couple or itself)

Below is an explanation of a first dummy version that works most of the time 

``` python
def generate(self):
        # prep work
        
        people_set = set(self.people)
        # s is the dict mentionned above
        s = dict()
        # is the set of gifted person, I prefered to use an other set over updating s each time
        gifted = set()
        
        for person in self.people:
            # at first I put the key person in its value since you don't want to gift to ourselves
            s[person] = {person}
            
        # add couple to it 
        for a, b in self.couples:
            s[a].add(b)
            s[b].add(a)
            
        
        for p in self.people:
            # This weird computation gives the list of available gift receiver
            # people_set is all the person 
            # ^ is the operator for symmetric_difference of set => inverse of an intersection
            # s[p] gives the set of person to which p can't gift too (like its SO)
            # | is the union operator for set
            # gifted is the list of person who already received a gift
            # So the available for p = all person - (impossible perso for p + already gifted person)
            available = people_set ^ (s[p] | gifted)
            
            # take a random person in this set
            receivers = random.sample(available, 1)

            # update my data structure
            # self.pairs is the result list
            self.pairs.append((p, receivers[0]))
            gifted.add(receivers[0])
            s[receivers[0]].add(p)
```

As stated above this version works most of the time, but can go to a dead end where not 
everyone got their gifts but there is nothing in `available` set. To fight that I made a couple of improvement


### Pick the most painful gifters first

As you see, I simply iterate over my list of person without second thought. Whereas I could
already do a small optimization:
- Start by the person with the most constraint
  - Or following my implementation, the person with the biggest `s[p]`
  - And iterate over this new list of person

``` python

# I played a bit with the lambda but it's quite easy
# Basically I sort the s by size of their set 
# I use the parameter reverse=True to have the descending order
# Then create a list of these people 
most_painfull_gifters = [x[0] for x in sorted(s.items(), key=lambda x: len(x[1]), reverse=True)]
```

So now the code will look like

``` python
... 
for p in most_painfull_gifters:
...
```

This code is still not dead-end proof but a bit more robust against it

### If no one is available go back

Another optimization to make the code more robust is too simply go back if `available` is
empty when there is still people missing their gift 

``` python 
if len(available) <= 0:
    # I've stopped using a for loop and no I do it by end with the class "i" parameter
    if i <= 0:
        # if I'm here it means that the secret santa is not possible because no one is available
        # for the first gifters
        print("Secret santa not possible")
        return
    # my line to "go back in time"
    i -=1
    
    # undo all my work in my structure
    removed_pair = self.pairs.pop()
    gifted.remove(removed_pair[1])
    s[removed_pair[1]].remove(removed_pair[0])
    continue
```

This change makes the code a bit more robust but it's possible to go in a 2 steps dead-end.
To resolves this problem I can take my change above and make it repeatable n times 

``` python
# same state as before
if len(available) <= 0:
    if i <= 0:
        print("Secret santa not possible")
        return

    # tmp is my precendent value of "i", it serves as history
    if tmp == i:
        # nb_try is init at 0 and count the number of time I've been stuck at "i" level
        nb_try += 1
    else:
        tmp = i

    # I've defined a TRY_ALLOWED to know how many times I can stay stuck at the same value
    # If I'm stuck too long, let's go back 1 more level 
    if nb_try >= self.TRY_ALLOWED:
        nb_try = 0
        call_back_santa()

    call_back_santa()
    continue
```

With this change, the code is even more robust and shouldn't be able to get stuck in dead-end


### How to run it

It comes with some test and secret santa tester. To launch the test you just have to write
``` bash
python SecretSantaGenerator.Test.py 

# or for one specified test
python SecretSantaGenerator.Test.py Test.test_generate_secret_santa_2
```

There is also a `main` with nothing really important in it that you can launch with
``` bash
 python main.py
```

## Possible amelioration

- Recursive call implementation
  - So it can test all the possibility and confirm if the secret santa is possible
- Graph usage instead of set?
  - I'm not sure it can be done but I had the idea
- Better test
  - Write automatically generated test with bigger data


# Random things

I was curious and after finishing my development, I asked ChatGPT for its implementation. My prompt:
```
Write me a secret santa list generator in python that takes as input a list of people and list of couple (formated as a
list of tuples) where couples can't be put together and each person gives and receives only gift
```

### The result

Certainly! Here's a Python code that generates Secret Santa pairings while ensuring that couples are not paired together and each person gives and receives only one gift:

```python
import random

def generate_secret_santa(people, couples):
    # Copy the list of people
    available_people = people.copy()

    # Shuffle the available people list
    random.shuffle(available_people)

    # Create a dictionary to store the pairings
    pairings = {}

    # Iterate through the available people
    for i, person in enumerate(available_people):
        # Get the couple associated with the current person (if any)
        couple = get_couple(person, couples)

        # If a couple is associated with the person, remove the couple from the available people
        if couple:
            available_people.remove(couple)

        # Find a recipient for the current person
        recipient = find_recipient(person, available_people)

        # If no recipient is found, restart the pairing process
        if recipient is None:
            return generate_secret_santa(people, couples)

        # Assign the recipient to the current person
        pairings[person] = recipient

    return pairings

def get_couple(person, couples):
    # Find the couple associated with the person
    for couple in couples:
        if person in couple:
            return couple

    return None

def find_recipient(person, available_people):
    # Shuffle the available people list
    random.shuffle(available_people)

    # Iterate through the available people to find a valid recipient
    for recipient in available_people:
        if recipient != person:
            return recipient

    return None

# Example usage
people = ['Alice', 'Bob', 'Charlie', 'David', 'Eve']
couples = [('Alice', 'Bob'), ('Charlie', 'David')]

pairings = generate_secret_santa(people, couples)

for giver, receiver in pairings.items():
    print(f"{giver} is giving a gift to {receiver}")
```

In this code, the `generate_secret_santa` function takes two parameters: `people` (a list of names) and `couples` (a list of tuples representing couples). It returns a dictionary `pairings` where the keys are the people and the values are their assigned recipients.

The `get_couple` function is a helper function that checks if a person is part of any couple. The `find_recipient` function selects a valid recipient from the available people list, excluding the person itself.

You can customize the `people` and `couples` lists to match your Secret Santa participants and their relationships. The code will ensure that each person is paired with a valid recipient, taking into account the specified constraints.