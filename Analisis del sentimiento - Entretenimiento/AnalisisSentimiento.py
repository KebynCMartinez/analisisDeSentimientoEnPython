import sys,tweepy,csv,re
from textblob import TextBlob
import matplotlib.pyplot as plt


class SentimentAnalysis:

    def __init__(self):
        self.tweets = []
        self.tweetText = []

    def DownloadData(self):
        # Autenticación
        consumerKey = '07mM9kwHFOvI1qN5g17YHuynA'
        consumerSecret = 'fMEEXGuCaKaKK9uKhRMtIHDqiepXA9BDa8RNE6rBnvTaNnYZUk'
        accessToken = '785670640837681152-7cjRHdDeZDgiVhkm0EIhB8L82h7nh0Q'
        accessTokenSecret = 'j6hbNuZ6Z7Gwndn8X1fsznYiSqoOevNWYJ00PQYhTglUp'
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        #api = tweepy.API(auth)
        api = tweepy.API(auth, wait_on_rate_limit=True)

        # entrada para el término a buscar y cuántos tweets buscar
        searchTerm = input("Sobre que deseas analizar: ")
        NoOfTerms = int(input("Que cantidad de Tweets desea analizar: "))

        # buscando tweets
        self.tweets = tweepy.Cursor(api.search, q=searchTerm, lang = "en").items(NoOfTerms)

        # Abrir/crear un fichero para agregar los datos
        csvFile = open('result.csv', 'a')

        # Uso de escritura en archivo csv
        csvWriter = csv.writer(csvFile)


        # creando algunas variables para almacenar información
        polarity = 0
        positive = 0
        wpositive = 0
        spositive = 0
        negative = 0
        wnegative = 0
        snegative = 0
        neutral = 0


        # creando algunas variables para obtener información
        for tweet in self.tweets:
            #Agregue a temp para que podamos almacenar en csv más tarde. Yo uso codificar UTF-8
            self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
            # print (tweet.text.translate(non_bmp_map))    #print tweet's text
            analysis = TextBlob(tweet.text)
            # print(analysis.sentiment)  # print tweet's polarity
            polarity += analysis.sentiment.polarity  # adding up polarities to find the average later

            if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
                neutral += 1
            elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
                wpositive += 1
            elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
                positive += 1
            elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
                spositive += 1
            elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
                wnegative += 1
            elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
                negative += 1
            elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
                snegative += 1

        
        public_tweets = tweepy.Cursor(api.search, q=searchTerm, lang = "en").items(NoOfTerms)

        for tweet in public_tweets:
	        print(tweet.text)
	        analysis = TextBlob(tweet.text)
	        print(analysis.sentiment)
	        if analysis.sentiment [ 0 ] > 0 :
	        	print('Positivo')
	        elif analysis.sentiment [ 0 ] < 0 :
	    	    print('Negativo')
	        print("")

        # Escribir en csv y cerrar archivo csv
        csvWriter.writerow(self.tweetText)
        csvFile.close()

        # encontrar el promedio de cómo están reaccionando las personas
        positive = self.percentage(positive, NoOfTerms)
        wpositive = self.percentage(wpositive, NoOfTerms)
        spositive = self.percentage(spositive, NoOfTerms)
        negative = self.percentage(negative, NoOfTerms)
        wnegative = self.percentage(wnegative, NoOfTerms)
        snegative = self.percentage(snegative, NoOfTerms)
        neutral = self.percentage(neutral, NoOfTerms)

        # Encontrar la reacción promedio
        polarity = polarity / NoOfTerms

        # Imprime los datos recabados
        print("Cómo reacciona la gente de " + searchTerm + " analizando " + str(NoOfTerms) + " tweets.")
        print()
        print("Reporte General: ")

        if (polarity == 0):
            print("Neutral")
        elif (polarity > 0 and polarity <= 0.3):
            print("Débilmente positivo")
        elif (polarity > 0.3 and polarity <= 0.6):
            print("Positivo")
        elif (polarity > 0.6 and polarity <= 1):
            print("Fuertemente Positivo")
        elif (polarity > -0.3 and polarity <= 0):
            print("Debilmente Negativo")
        elif (polarity > -0.6 and polarity <= -0.3):
            print("Negativo")
        elif (polarity > -1 and polarity <= -0.6):
            print("Fuertemente Negativo")

        print()
        print("Reporte Detallado: ")
        print(str(positive) + " porciento de la gente pensaba que era positivo")
        print(str(wpositive) + " porciento de la gente pensaba que era débilmente positivo")
        print(str(spositive) + " porciento de la gente pensaba que era fuertemente positivo")
        print(str(negative) + " porciento de la gente pensaba que era negativo")
        print(str(wnegative) + " porciento de la gente pensaba que era débilmente negativo")
        print(str(snegative) + " porciento de la gente pensaba que era fuertemente negativo")
        print(str(neutral) + " porciento de la gente pensaba que era neutral")

        self.plotPieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, NoOfTerms)


    def cleanTweet(self, tweet):
        # Quita los Links, Caracteres especiales, etc del tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    # Función que calcula el porcentaje
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

    def plotPieChart(self, positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, noOfSearchTerms):
        labels = ['Positivo [' + str(positive) + '%]', 'Débilmente Positivo [' + str(wpositive) + '%]','Fuertemente Positivo [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
                  'Negativo [' + str(negative) + '%]', 'Débilmente Negativo [' + str(wnegative) + '%]', 'Fuertemente Negativo [' + str(snegative) + '%]']
        sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
        colors = ['yellowgreen','lightgreen','darkgreen', 'gold', 'red','lightsalmon','darkred']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('Cómo reacciona la gente de ' + searchTerm + ' analizando ' + str(noOfSearchTerms) + ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()



if __name__== "__main__":
    sa = SentimentAnalysis()
    sa.DownloadData()