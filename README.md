[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

# Computational Reading Test
This demo code is meant to accompany my [Medium post](https://medium.com/@kazarazat/testing-if-machines-can-read-b15bcbaeae51) article outlining a formula and method to test basic reading comprehension in a computational system. This code demonstrates computational recognition of the words in an inputted sentence including: sentence typology, presence of the sentence words in the dictionary and definitions of the words. 

# How it Works
* Input a sentence as a string
* Uses NLTK to POS Tag the sentence
* Checks for Stop Words
* Checks each word that's not a Stop Word in Webster's Dictionary
* Defines all dictionary words using the Oxford API
* Identifies the Typology of the Sentence
* Calculates the time taken to recognize and define the words
* Outputs a JSON for verification

# Modules
**Install the requirements with pip**

    pip install -r requirements.txt
	
**Oxford Word Definitions API**
Get API credentials [Oxford Dictionaries](https://developer.oxforddictionaries.com)

    app_id = '********'
    app_key = '***********************'
    address = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/'


**The Input**

	my_sentence = 'the quick brown fox jumped over the lazy dog'

**The Output**
```sh
{"defined_words": ["brown", "lazy", "jump", "fox", "dog", "quick"], "stopwords_found": ["the", "over", "the"],<br/> 
"sentence_typology": ["subject", "verb", "object"], "definitions": ["of a colour produced by mixing red, yellow,<br/> 
and blue, as of dark wood or rich soil", "unwilling to work or use energy", "push oneself off a surface and into<br/>
the air by using the muscles in one's legs and feet", "a carnivorous mammal of the dog family with a pointed muzzle and bushy tail, proverbial for its cunning.", "a domesticated carnivorous mammal that typically has a long snout, an acute sense of smell, non-retractable claws, and a barking, howling, or whining voice.", "moving fast or doing something in a short time"], "total_words_read": 9, "reading_rate": "0.3587 per word", "comprehension_time": 3.22831, "comprehension_rate": 100.0}
```
