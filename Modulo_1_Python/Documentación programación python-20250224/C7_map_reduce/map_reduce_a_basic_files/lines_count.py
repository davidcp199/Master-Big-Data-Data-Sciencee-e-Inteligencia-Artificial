from mrjob.job import MRJob

class MRLinesCount(MRJob):

    def mapper(self, _, linea):
            yield "lineas", 1
                
    def reducer(self, key, valores):
        yield key, sum(valores)

if __name__ == '__main__':
    MRLinesCount.run()
