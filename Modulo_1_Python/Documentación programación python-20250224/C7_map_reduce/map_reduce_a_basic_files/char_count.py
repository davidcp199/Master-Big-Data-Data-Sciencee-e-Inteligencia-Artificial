from mrjob.job import MRJob

class MRCharCount(MRJob):

    def mapper(self, _, linea):
        for caracter in linea:
            yield caracter, 1
                
    def reducer(self, key, valores):
        yield key, sum(valores)

if __name__ == '__main__':
    MRCharCount.run()
