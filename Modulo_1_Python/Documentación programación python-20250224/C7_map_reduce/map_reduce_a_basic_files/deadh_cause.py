from mrjob.job import MRJob

def to_int(cadena):
    try:
        return int(cadena)
    except:
        return 0

class MRCauseOfDeadth(MRJob):

    def mapper(self, _, linea):
        campos = linea.split(";")
        passcodigo = campos[1]
        num_ejecs = to_int(campos[3])
        if passcodigo == "USA":
            yield "ejecs", num_ejecs
               
    def reducer(self, key, valores):
        yield key, sum(valores)

if __name__ == '__main__':
    MRCauseOfDeadth.run()
