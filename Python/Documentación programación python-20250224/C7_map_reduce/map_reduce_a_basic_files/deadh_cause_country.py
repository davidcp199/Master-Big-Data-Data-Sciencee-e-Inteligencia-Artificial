from mrjob.job import MRJob

def to_int(cadena):
    try:
        return int(cadena)
    except:
        return 0
        
class MRCauseOfDeadth(MRJob):

    def configure_args(self):
        super(MRCauseOfDeadth, self).configure_args()
        self.add_passthru_arg(
            '--country', default='Spain',
            help="Indica el código del país.")

    def mapper(self, _, linea):
        campos = linea.split(";")
        cod_pais= campos[1]
        if cod_pais == self.options.country:
                num_ejecs = to_int(campos[3])
                yield cod_pais, num_ejecs
               
    def reducer(self, key, valores):
        yield key, sum(valores)

if __name__ == '__main__':
    MRCauseOfDeadth.run()
