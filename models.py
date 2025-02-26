from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=200)
    poster_url = models.URLField()
    class Meta:
        db_table = 'movie'

class Moviedetails(models.Model):
    title = models.CharField(max_length=255)
    poster_url = models.URLField()
    director = models.CharField(max_length=255)
    screenplay = models.CharField(max_length=255)
    dialogues = models.CharField(max_length=255)
    production = models.CharField(max_length=255)
    cast = models.TextField()
    cinematography = models.CharField(max_length=255)
    editor = models.CharField(max_length=255)
    music = models.CharField(max_length=255)
    production_companies = models.TextField()
    release_date = models.DateField()
    running_time = models.IntegerField()
    country = models.CharField(max_length=100)
    language = models.CharField(max_length=100)

    class Meta:
        db_table = 'moviedetails'


class Theatre(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True)
    location = models.CharField(max_length=255)
    theatre_id = models.IntegerField()
    show_time = models.DateTimeField()
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    class Meta:
        db_table = 'theater'


class Seat(models.Model):
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=10)
    row = models.CharField(max_length=10)
    is_booked = models.BooleanField(default=False or True)

    class Meta:
        unique_together = ('theatre', 'seat_number', 'row')
        db_table = 'seat'

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    show_time = models.CharField(max_length=100)
    # other fields
    class Meta:
        db_table = 'ticket'

       

     





