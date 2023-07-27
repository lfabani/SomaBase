import nlu
import pyspark
pipe = nlu.load('biobert')
pipe.predict("he was surprised by a whole the fact that there was IL-6 in the product, maybe its time to look for something else")