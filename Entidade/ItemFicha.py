Entidade/Instrutor.py

class ItemFicha:
    def __init__(self, exercicio=None, series: int = 0, repeticoes: int = 0):
        self.exercicio = exercicio
        self.series = series
        self.repeticoes = repeticoes

    def __str__(self) -> str:
        return f"{self.exercicio}: {self.series} séries x {self.repeticoes} repetições"