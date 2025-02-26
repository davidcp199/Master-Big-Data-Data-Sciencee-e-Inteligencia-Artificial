from mrjob.job import MRJob

class MRWordCount(MRJob):

    def mapper(self, _, linea):
        for w in linea.split():
            yield w, 1
                
    def reducer(self, key, valores):
        yield key, sum(valores)

if __name__ == '__main__':
    MRWordCount.run()
