# address-extractor

Input: python input_file_name.json Keyword

example: python address_extractor.py address_extraction_data.json extraction_keyowords.json


Using Separate modules to extract address from string with or without keywords and from file.

Example:
1)
from address_extractor import getAddressFromStringType

getAddressFromStringType("click here. BIG BOOTY !!!!mis head dr ! Sutphin Boulevard! supthin incall queens.!!!!! - 25",keywords=["avenue","blvd","boulevard","pkwy","parkway","st","street","rd","road","way","drive","lane","alley","ave"])

2)
from address_extractor import getAddressFromString

getAddressFromString("click here. BIG BOOTY !!!!mis head dr ! Sutphin Boulevard! supthin incall queens.!!!!! - 25")

3)
from address_extractor import getAddressFromFile

getAddressFromFile("address_extraction_data.json",keywords=["avenue","blvd","boulevard","pkwy","parkway","st","street","rd","road","way","drive","lane","alley","ave"])


