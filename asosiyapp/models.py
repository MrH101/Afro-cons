from django.db import models

class Bolim(models.Model):
    nom=models.CharField(max_length=100)
    rasm=models.FileField(upload_to='bolimlar')
    def __str__(self): return self.nom

class Ichki(models.Model):
    nom=models.CharField(max_length=100)
    rasm=models.FileField(upload_to='ichki_bolimlar')
    bolim=models.ForeignKey(Bolim, on_delete=models.CASCADE, related_name='ichkilari')
    def __str__(self): return self.nom

class Mahsulot(models.Model):
    nom=models.CharField(max_length=50)
    brend=models.CharField(max_length=50)
    narx=models.IntegerField()
    batafsil=models.TextField()
    kafolat=models.CharField(max_length=50)
    yetkazish=models.CharField(max_length=50)
    mavjud=models.BooleanField()
    chegirma=models.FloatField()
    ichki=models.ForeignKey(Ichki, on_delete=models.CASCADE)

    def __str__(self): return self.nom

class Rasm(models.Model):
    rasm=models.FileField()
    mahsulot=models.ForeignKey(Mahsulot, on_delete=models.CASCADE, related_name='rasmlari')
    def __str__(self): return self.mahsulot.nom

