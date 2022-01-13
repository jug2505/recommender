from django.db import models

class Rating(models.Model):
    user_id = models.CharField(max_length=16)
    movie_id = models.CharField(max_length=16)
    rating = models.DecimalField(decimal_places=2, max_digits=4)
    rating_timestamp = models.DateTimeField()

    class Meta:
        db_table = 'rating'

    def __str__(self):
        return "user_id: {}, movie_id: {}, rating: {}".format(self.user_id, self.movie_id, self.rating)


class Genre(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        db_table = 'genre'

    def __str__(self):
        return self.name


class Movie(models.Model):
    movie_id = models.CharField(max_length=16, unique=True, primary_key=True)
    title = models.CharField(max_length=512)
    year = models.IntegerField(null=True)
    genres = models.ManyToManyField(Genre, related_name='movies', db_table='movie_genre')

    class Meta:
        db_table = 'movie'

    def __str__(self):
        return self.title


class Similarity(models.Model):
    source = models.CharField(max_length=16, db_index=True)
    target = models.CharField(max_length=16)
    similarity = models.DecimalField(max_digits=8, decimal_places=7)

    class Meta:
        db_table = 'similarity'

    def __str__(self):
        return "[({} => {}) sim = {}]".format(self.source, self.target, self.similarity)


class SeededRecs(models.Model):
    source = models.CharField(max_length=16)
    target = models.CharField(max_length=16)
    support = models.DecimalField(max_digits=10, decimal_places=8)
    confidence = models.DecimalField(max_digits=10, decimal_places=8)

    class Meta:
        db_table = 'seeded_recs'

    def __str__(self):
        return "[({} => {}) support = {}, confidence = {}]".format(self.source, self.target, self.support, self.confidence)
