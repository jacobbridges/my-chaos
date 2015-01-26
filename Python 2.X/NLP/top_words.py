# usr/bin/env python

import re
from collections import Counter
 
SPEECH_TO_PROCESS = "US State of Union Address -- (01-20-2015).txt"
 
# Open speech document
with open("./speeches/" + SPEECH_TO_PROCESS, "r") as SPEECH_FILE:
  
  # Read speech text into variable, converting any pesky unicode characters
	speech = SPEECH_FILE.read().decode('utf8').encode("ascii", "ignore")
	
	# Remove all apostrophes from text (easier to handle contractions)
	speech = speech.replace("'", '')
	
	# Get all words from document with regex
	words = re.findall(r'\w+', speech.lower())
	
	# Load word list into Counter object
	c = Counter(words)
	
	# Calculate the progressive score
	progressive_score = 0 + (c["going"] + c["will"] + c["next"] + c["tomorrow"] + c["future"]) - (c["have"] + c["did"] + c["done"] + c["past"] + c["yesterday"] + c["last"])
	
	print "Progressive Score = " + str(progressive_score)