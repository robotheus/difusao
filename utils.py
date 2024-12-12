from ndlib.models.epidemics.IndependentCascadesModel import IndependentCascadesModel

class ModifiedIC(IndependentCascadesModel):
    def __init__(self, graph):
        super().__init__(graph)
        self.available_statuses = {"suscetível": 0, "ativo": 1}
