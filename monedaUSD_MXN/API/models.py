from django.db import models

class CambioMoneda(models.Model):
    
    proveedor=models.CharField(max_length=50)
    fecha_actualizacion=models.CharField(max_length=50)
    valorUSD=models.CharField(max_length=50)
    

    class Meta:
        verbose_name = ("CambioMoneda")
        verbose_name_plural = ("CambioMonedas")

    def __str__(self):
        return self.proveedor

