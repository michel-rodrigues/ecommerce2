from django.db import models

class SignUp(models.Model):
    email = models.EmailField()
    full_name = models.CharField(max_length=120, blank=True, null=True)

    # 'auto_now_add' - Exibe o momento que foi adicionado pela 
    # primeira vez no banco de dados.
    # ' auto_now' - Exibe a última vez que foi atualizado no 
    # banco de dados
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    # Esse método vai fazer com que seja exibido uma string,
    # no caso o email, ao invés do objeto
    def __str__(self):
        return self.email
