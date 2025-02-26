from mrjob.job import MRJob

class MRWordCount(MRJob):

    def mapper(self, _, linea):
        for caracter in linea:
            if caracter.isalpha():
                yield "letra", 1
            else:
                yield "otros", 1
                
    def reducer(self, key, valores):
        yield key, sum(valores)

if __name__ == '__main__':
    MRWordCount.run()
