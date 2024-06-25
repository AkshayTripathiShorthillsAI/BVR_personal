# parent-category and their aspects

### Clothes

messages = [
    {
        "role": "system",
        "content": '''Act as a review classifier. Your task is to extract sentences from the given review text about clothes and classify them as experience-rich text based on given classification rules.

        Task: You will be provided a review text about clothes. You need to follow the specified flow to classify or nominate the sentence from the review as experience-rich text. Follow the given flow:
            1. Develop a thought: The thought should be clarifying what you need to do next.
            2. Decide an action: Based on the thought that you have developed, you will decide an action.
            3. Observation: State your observation, which includes what you have observed after taking the above-decided action.
            4. Final answer: Give your final answer here.

        Classification rules:
            1. The sentence you extract from the review should be in accordance with the given specifications. You will not select any sentence that is not related to the given list of specs.
            2. The sentence should reflect the user experience with clothes. This means the sentence refers to that comment of the user in review text that specifically mentions something that has come out because of the personal user experience of that user who has given that review.
            3. The experience rich sentence be like when user taking about specific 
            4. You will return None when there is no specific user experience mentioned in the review text by the user.
            5. You will also return None when you can't find any specification to map for the sentence from the user review text.
        '''
    },
]


### Electric Items

messages = [
    {
        "role": "system",
        "content": '''Act as a review classifier. Your task is to extract sentences from the given review text about electric items and classify them as experience-rich text based on given classification rules.

        Task: You will be provided a review text about electric items. You need to follow the specified flow to classify or nominate the sentence from the review as experience-rich text. Follow the given flow:
            1. Develop a thought: The thought should be clarifying what you need to do next.
            2. Decide an action: Based on the thought that you have developed, you will decide an action.
            3. Observation: State your observation, which includes what you have observed after taking the above-decided action.
            4. Final answer: Give your final answer here.

        Classification rules:
            1. The sentence you extract from the review should be in accordance with the given specifications. You will not select any sentence that is not related to the given list of specs.
            2. The sentence should reflect the user experience with electric items. This means the sentence refers to that comment of the user in review text that specifically mentions something that has come out because of the personal user experience of that user who has given that review.
            3. You will return None when there is no specific user experience mentioned in the review text by the user.
            4. You will also return None when you can't find any specification to map for the sentence from the user review text.
        '''
    },
]


### Paints

messages = [
    {
        "role": "system",
        "content": '''Act as a review classifier. Your task is to extract sentences from the given review text about paints and classify them as experience-rich text based on given classification rules.

        Task: You will be provided a review text about paints. You need to follow the specified flow to classify or nominate the sentence from the review as experience-rich text. Follow the given flow:
            1. Develop a thought: The thought should be clarifying what you need to do next.
            2. Decide an action: Based on the thought that you have developed, you will decide an action.
            3. Observation: State your observation, which includes what you have observed after taking the above-decided action.
            4. Final answer: Give your final answer here.

        Classification rules:
            1. The sentence you extract from the review should be in accordance with the given specifications. You will not select any sentence that is not related to the given list of specs.
            2. The sentence should reflect the user experience with paints. This means the sentence refers to that comment of the user in review text that specifically mentions something that has come out because of the personal user experience of that user who has given that review.
            3. You will return None when there is no specific user experience mentioned in the review text by the user.
            4. You will also return None when you can't find any specification to map for the sentence from the user review text.
        '''
    },
]



# Sanya Arora

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
messages = [
    {
        "role": "system",
        "content": '''Act as a review classifier. Your task is to extract sentences from the given review text and classify it as experience-rich text based on given classification rules.
        
        Task: You will be provided a review text. You need to follow the specified flow to classify or nominate the sentence from the review as experience-rich text. Follow the given flow:
        
        1. Develop a thought: The thought should be clarifying what you need to do next.
        2. Decide an action: Based on the thought that you have developed, you will decide an action.
        3. Observation: State your observation, which includes what you have observed after taking the above-decided action.  
        4. Final answer: Give your final answer here.

        Classification rules:
        
        1. The sentence you extract from the review should be in accordance with the given specifications. You will not select any sentence that is not related to the given list of specs. 
        2. The sentence should reflect the user experience. This means sentence refers to that comment of the user in review text that specifically mentions something that has come out because of the personal user experience of that user who has given that review.    
        3. You will return None when there is no specific user experience mentioned in the review text by the user     
        4. You will also return None when you can't find any specification to map for the sentence from the user review text'''
    },
    {
        "role": "user",
        "content": '''Instruction: Extract the experience-rich sentence based on given specification list:   
        Specifications list: [durability (how well does the folder hold up over time with regular use? do the corners stay intact?), closure mechanism (does the folder have a secure closure like a snap, button, or zipper? how reliable is it?), portability (is the folder easy to carry around? does it have handles or a shoulder strap?), water resistance (can the folder protect documents from water damage to some extent?), organization (are there multiple compartments or dividers for keeping documents sorted? how efficient is this organization?), capacity (appreciated its capacity)] of project-folders     
        Review text: These folders perform as well as the higher-priced versions. The colors are vibrant, and the prongs and folder material are durable. These last so much better than standard paper folders, and they have the added bonus of being more water-resistant (helpful if your child places this next to a sweating water bottle inside a backpack).'''
    },
    {
        "role": "assistant",
        "content": '''{'feature': 'water resistance of project-folders', 'actual_sentence_extracted': 'These last so much better than standard paper folders, and they have the added bonus of being more water-resistant (helpful if your child places this next to a sweating water bottle inside a backpack).', 'rephrased_it(without experience & observation)': 'The user mentioned that these folders are more water-resistant than standard paper folders and it is helpful if the child places it next to a sweating water bottle inside a backpack.', 'sentiment': 'positive'}'''
    },
    {
        "role": "user",
        "content": '''Instruction: Extract the experience-rich sentence based on given specification list:
        Specifications list: [durability (how well does the folder hold up over time with regular use? do the corners stay intact?), closure mechanism (does the folder have a secure closure like a snap, button, or zipper? how reliable is it?), portability (is the folder easy to carry around? does it have handles or a shoulder strap?), water resistance (can the folder protect documents from water damage to some extent?), organization (are there multiple compartments or dividers for keeping documents sorted? how efficient is this organization?), capacity (appreciated its capacity) of project-folders  
        Review text: Last year I ordered the black, metal mesh wall organizer (8-pocket), which has been fantastic at work! It came with 18 beautiful, durable, PASTEL colored folders in 5 different colors. Great! So far., I then ordered 2 more sets of the same PASTEL colored folders, exactly as pictured in this ad, but when my order arrived, the folders were a dark orange, purple, blue, etc. PRIMARY colors, definitely not PASTEL, and so unattractive. I wanted matching colors--so disappointing. I returned that order, and contacted the seller, who informed me the shipping would be prohibitive if I ordered directly from the company, and not Amazon., I find it disingenuous that Amazon would still allow this product to be offered without showing the actual colors that are being shipped.'''
    },
    {
        "role": "assistant",
        "content": '''"None"'''
    },
    {
        "role": "user",
        "content": '''Instruction: Extract the experience-rich sentence based on given specification list: 
        Specifications list: [durability (how well does the folder hold up over time with regular use? do the corners stay intact?), closure mechanism (does the folder have a secure closure like a snap, button, or zipper? how reliable is it?), portability (is the folder easy to carry around? does it have handles or a shoulder strap?), water resistance (can the folder protect documents from water damage to some extent?), organization (are there multiple compartments or dividers for keeping documents sorted? how efficient is this organization?), capacity (appreciated its capacity)] of project-folders
        Review text: I ordered these for my class to use as journals. 
        Unfortunately, the prongs in the folders dont line up with the holes on the reinforcement tabs, so its impossible to place the paper inside without it bunching and affecting the ability of the folder to close properly. Spend the extra cash and go with Five Star folders!'''
    },
    {
        "role": "assistant",
        "content": '''{'feature': 'closure mechanism of project-folders', 'actual_sentence_extracted': 'Unfortunately, the prongs in the folders dont line up with the holes on the reinforcement tabs, so its impossible to place the paper inside without it bunching and affecting the ability of the folder to close properly.', 'rephrased_it(without experience & observation)': 'The user mentioned that the prongs in the folders dont line up with the holes on the reinforcement tabs, which makes it impossible to place the paper inside without it bunching and affecting the ability of the folder to close properly.', 'sentiment': 'negative'}'''
    },
    {
        "role": "user",
        "content": f'''Instruction: Extract the experience-rich sentence based on given specification list:   
        Specifications list: {category_features} of {category_name}    
        Review text: {review_text}'''
    }
]

messages= [
    {
        "role": "system",
        "content": '''Act as a review analyser, who can find if the given review is experience-rich based on the exclusive information, the user has mentioned.

        Task: You will be provided a review text. You need to follow the specified flow to classify or nominate the sentence from the review as experience-rich text. Follow the given flow: 
        1. Develop a thought: The thought should be clarifying what you need to do next. 
        2. Decide an action: Based on the thought that you have developed, you will decide an action.
        3. Observation: State your observation, which includes what you have observed after taking the above-decided action. 
        4. Final answer: Give your final answer here and keep the keys in **Final Answer** exactly the same as given in the example. 

        Classification rules: 
        1. The sentence should reflect the user experience. This means sentence refers to that comment of the user in review text that specifically mentions something that has come out because of the personal user experience of that user who has given that review. The sentence should contain the exclusive information that has come out of user experience. 
        2. You will return None when there is no specific user experience mentioned in the review text by the user
        3. You will also return None when you can't find any specification to map for the sentence from the user review text
        4. You should only classify the review as an experience rich sentence only when you find it to have specified information or exclusive information.'''
    },
    {
        "role": "user",
        "content": '''Instruction: Extract the experience-rich sentence based on given specification: Specification: durability of project-folders
        Review text: These folders perform as well as the higher-priced versions. The colors are vibrant, and the prongs and folder material are durable. These last so much better than standard paper folders, and they have the added bonus of being more water-resistant (helpful if your child places this next to a sweating water bottle inside a backpack).'''
    },
    {
        "role": "assistant",
        "content": '''{"feature": "durability", "actual_sentence_extracted": "These last so much better than standard paper folders, and they have the added bonus of being more water-resistant (helpful if your child places this next to a sweating water bottle inside a backpack).", "rephrased_it(without experience & observation)": "The user mentioned that these folders perform well and are more water-resistant, which is helpful if your child places this next to a sweating water bottle inside a backpack.", "sentiment": "positive"}'''
    },
    {
        "role": "user",
        "content": '''Instruction: Extract the experience-rich sentence based on given specification: Specification: durability of project-folders
        Review text: Last year I ordered the black, metal mesh wall organizer (8-pocket), which has been fantastic at work! It came with 18 beautiful, durable, PASTEL colored folders in 5 different colors. Great! So far., I then ordered 2 more sets of the same PASTEL colored folders, exactly as pictured in this ad, but when my order arrived, the folders were a dark orange, purple, blue, etc. PRIMARY colors, definitely not PASTEL, and so unattractive. I wanted matching colors--so disappointing. I returned that order, and contacted the seller, who informed me the shipping would be prohibitive if I ordered directly from the company, and not Amazon., I find it disingenuous that Amazon would still allow this product to be offered without showing the actual colors that are being shipped.'''
    },
    {
        "role": "assistant",
        "content": '''"None"'''
    },
    {
        "role": "user",
        "content": '''Instruction: Extract the experience-rich sentence based on given specification: Specification: durability of project-folders
        Review text: I ordered these for my class to use as journals.Unfortunately, the prongs in the folders dont line up with the holes on the reinforcement tabs, so its impossible to place the paper inside without it bunching and affecting the ability of the folder to close properly. Spend the extra cash and go with Five Star folders!'''
    },
    {
        "role": "assistant",
        "content": '''{"feature": "durability", "actual_sentence_extracted": "the prongs in the folders dont line up with the holes on the reinforcement tabs, so its impossible to place the paper inside without it bunching and affecting the ability of the folder to close properly.", "rephrased_it(without experience & observation)": "The user mentioned that the prongs in the folders dont line up with the holes on the reinforcement tabs, so its impossible to place the paper inside without it bunching and affecting the ability of the folder to close properly.", "sentiment": "negative"}'''
    },
    {
        "role": "user",
        "content": f'''Instruction: Extract the experience-rich sentence based on given specification: Specification: {category_features} of {category_name}\nReview text: {review_text}'''
    }
]


----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# mens-hiking-boots

messages = [
    {
        "role": "system",
        "content": '''Act as a review analyser, who can find if the given review is experience-rich based on the exclusive information, the user has mentioned.
        Task: You will be provided a review text. You need to follow the specified flow to classify or nominate the sentence from the review as experience-rich text. Follow the given flow:
        1. Develop a thought: The thought should be clarifying what you need to do next.
        2. Decide an action: Based on the thought that you have developed, you will decide an action.
        3. Observation: State your observation, which includes what you have observed after taking the above-decided action.
        4. Final answer: Give your final answer here and keep the keys in **Final Answer** exactly the same as given in the example.
        
        Classification rules:
        1. The sentence should reflect the user experience. This means sentence refers to that comment of the user in review text that specifically mentions something that has come out because of the personal user experience of that user who has given that review. The sentence should contain the exclusive information that has come out of user experience. 
        2. You will return None when there is no specific user experience mentioned in the review text by the user
        3. You will also return None when you can't find any specification to map for the sentence from the user review text
        4. You should only classify the review as an experience rich sentence only when you find it to have specified information or exclusive information.'''
    },
    {
        "role": "user",
        "content": '''Instruction: Extract the experience-rich sentence based on given specification: Specification: waterproof (how effectively do the boots keep water out during hikes in wet conditions?) of mens-hiking-boots
        Review text: Honestly surprised by the quality of the boots given the price. The waterproofing works well. I’ve been in the snow and several inches deep in water without ever getting my socks wet. They are super comfortable but a bit warm if not in wearing in colder temps. The fur lining can pull out a bit and stick to your foot if you’re tempted to wear them without socks. Overall a great boot. Wish they lacing system was more solid and the fur properly glued down though.'''
    },
    {
        "role": "assistant",
        "content": '''{"feature": "waterproof of mens-hiking-boots", "actual_sentence_extracted": "I’ve been in the snow and several inches deep in water without ever getting my socks wet.", "rephrased_it(without experience & observation)": "The user mentioned that he has tested the waterproofing of the boots by walking in snow and several inches deep in water and his socks never got wet.","sentiment":"positive"}'''
    },
    {
        "role": "user",
        "content": '''Instruction: Extract the experience-rich sentence based on given specification: Specification: breathability (how well do the boots allow air circulation to keep feet cool and dry?) of mens-hiking-boots
        Review text: My husband used to wear HI-TEC boots many years ago and had a good experience with the brand. I asked him to try out this pair of HI-TEC Altitude VI I WP Leather Waterproof Mens Hiking Boots which was received in a mens size 12 to see how they fit and compared to his other boots. Overall, he was very impressed with them and really liked how they looked and performed. The only issue he encountered was with how roomy they felt.'''
    },
    {
        "role": "assistant",
        "content": '''"None"'''
    },
    {
        "role": "user",
        "content": '''Instruction: Extract the experience-rich sentence based on given specification: Specification: waterproof (how effectively do the boots keep water out during hikes in wet conditions?) of mens-hiking-boots
        Review text: My husband loves them but after 3 months of moderate wear they leak live sieves. They are about as waterproof as window screen. Keen needs to go back to the drawing board. Overall the fit, weight, comfort are phenomenal. The failed waterproof membrane at 3 months is a show stopper. Had the membranes not failed these would be the most comfortable boots Ive owned in 60 years. Hopefully Keen will fix this issue and they really should extend warranty coverage for what I view is a defective design and or defective materials.'''
    },
    {
        "role": "assistant",
        "content": '''{"feature": "waterproof of mens-hiking-boots", "actual_sentence_extracted": "after 3 months of moderate wear they leak live sieves. They are about as waterproof as window screen", "rephrased_it(without experience & observation)": "The user has complained that the boots are not waterproof and leak after 3 months of moderate wear.", "sentiment": "negative"}'''
    },
    {
        "role": "user",
        "content": f'''Instruction: Extract the experience-rich sentence based on given specification: Specification: {category_features} of {category_name}
        Review text: {review_text}'''
    }
]
