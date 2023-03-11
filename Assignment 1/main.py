'''This module acts like the controller program. To run this code, 
simply write 'python3 main.py' (for linux users) or 'python main.py' 
(for windows users). The commented code is for testing purposes. 
If you wish to remove it, you can, but let it be xD'''


# import Dictionary
# dictionaryObject=Dictionary.Dictionary()

# dictionaryObject.documentProcessing()
# dictionaryObject.printPostingList()
# dictionaryObject.writeToFile()


# import Queries
# QueryObj=Queries.Queries()
# QueryObj.printPositionalIndex()
# QueryObj.loadPositionalIndex()


import SearchGUI

guiObj = SearchGUI
guiObj.triggerGUI()
