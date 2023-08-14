import nltk
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

with open('[ANK-Raws&TD] Nekomonogatari - 02 (BD 1080p x264 FLACx2 Hi10P).Audio commentary.ass', encoding="utf8") as f:
    inp = f.readlines()

##with open('[ANK-Raws&TD] Nekomonogatari - 02 (BD 1080p x264 FLACx2 Hi10P).Audio commentary.ass', encoding="utf16") as f:
##    inp = f.readlines()

token = word_tokenize(str(list(str(inp))))

fdist = FreqDist(token).most_common(20000)

bl = ('0','1','2','3','4','5','6','7','8','9',
      'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
      'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
      '\'a','\'b','\'c','\'d','\'e','\'f','\'g','\'h','\'i','\'j','\'k','\'l','\'m',
      '\'n','\'o','\'p','\'q','\'r','\'s','\'t','\'u','\'v','\'w','\'x','\'y','\'z',
      '\'A','\'B','\'C','\'D','\'E','\'F','\'G','\'H','\'I','\'J','\'K','\'L','\'M',
      '\'N','\'O','\'P','\'Q','\'R','\'S','\'T','\'U','\'V','\'W','\'X','\'Y','\'Z',
      '\'',',',':','.','(',')','[',']','{','}','&',';','``','?','!','-','*','%','@',
      '，','。','、','·','…','（','）','「','」','『','』','《','》','；',
      '\'\'','\',','\':','\'.','\'(','\')','\'[','\']','\'{','\'}','\'&','\';','\'?','\'!','\'\\\\','\'-','\'*','\'%','\'@',
      '\'，','\'。','\'、','\'·','\'…','\'（','\'）','\'「','\'」','\'『','\'』','\'《','\'》','\'；')

for char,val in fdist:
    if char in bl:
        pass
    elif val >= 2:
        pass
    else:
        print(char,val)

f.close()
