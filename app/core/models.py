"""Database models."""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from utils.slug_generator import unique_slug_generator


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **kwargs):
        """Create, save and return a new user."""
        if not email:
            raise ValueError("User must have an email address.")
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)  # using=self._dbis for multiple database
        return user

    def create_superuser(self, email, password=None, **kwargs):
        """Create and return new super user"""
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""

    slug = models.SlugField(max_length=100, null=True, editable=False, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField(
        auto_now_add=False, auto_now=False, blank=True, null=True
    )

    objects = UserManager()  # Assign usermanager to User model

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = unique_slug_generator(self, variable=self.name)
        self.clean()
        super().save(*args, **kwargs)


class City(models.Model):
    """Storing city details."""

    name = models.CharField(max_length=255, null=False, blank=False)
    slug = models.SlugField(null=True, max_length=255, editable=False)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.slug = unique_slug_generator(self, variable=self.name)
        self.clean()
        super().save(*args, **kwargs)


class Movie(models.Model):
    """Storing movie details."""

    rating_choice = (
        ("U", "U"),
        ("UA", "UA"),
        ("A", "A"),
        ("R", "R"),
    )
    title = models.CharField(max_length=255, null=False, blank=False)
    slug = models.SlugField(max_length=255, null=True, editable=False)
    description = models.TextField(null=True, blank=True)
    duration = models.DurationField()
    release_date = models.DateField(auto_now=False, auto_now_add=False)
    language = models.CharField(max_length=255, null=True, blank=True)
    certificate = models.CharField(max_length=2, choices=rating_choice)

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        self.slug = unique_slug_generator(self, variable=self.title)
        self.clean()
        super().save(*args, **kwargs)


class Media(models.Model):
    """Storing Media(images) for each movies"""
    movie = models.ForeignKey(Movie, on_delete=models.PROTECT, related_name="media")
    image = models.ImageField(null=True, blank=True)
    alt_text = models.CharField(max_length=255)
    is_feature = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.movie}-{self.image}"


class Theater(models.Model):
    """Storing Theater deatails"""
    name = models.CharField(max_length=255, null=False, blank=False)
    slug = models.SlugField(max_length=255, null=True, editable=False)
    address = models.CharField(max_length=255, null=False, blank=False)
    city = models.ForeignKey(City, related_name="theater", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.slug = unique_slug_generator(self, variable=self.name)
        self.clean()
        super().save(*args, **kwargs)


class Screen(models.Model):
    """Storing screen for each theater."""
    name = models.CharField(max_length=255, null=False, blank=False)
    slug = models.SlugField(max_length=255, null=True, editable=False)
    theater = models.ForeignKey(
        Theater, on_delete=models.CASCADE, related_name="screen"
    )

    def __str__(self):
        return f"{self.name}-{self.theater.name}"

    def save(self, *args, **kwargs):
        self.slug = unique_slug_generator(self, variable=self.name)
        self.clean()
        super().save(*args, **kwargs)


class Show(models.Model):
    """Storing shows for each movies."""
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="show")
    slug = slug = models.SlugField(max_length=255, null=True, editable=False)
    start_date = models.DateField(
        auto_now=False, auto_now_add=False, null=True, blank=True
    )
    end_date = models.DateField(
        auto_now=False, auto_now_add=False, null=True, blank=True
    )
    start_time = models.TimeField(
        auto_now=False, auto_now_add=False, null=True, blank=True
    )
    end_time = models.TimeField(
        auto_now=False, auto_now_add=False, null=True, blank=True
    )

    def __str__(self):
        return f"{self.movie.title}:[{self.start_time}-{self.end_time}]"

    def save(self, *args, **kwargs):
        self.slug = unique_slug_generator(self, variable=self)
        self.clean()
        super().save(*args, **kwargs)

class ScreenShowMapper(models.Model):
    """Mapping screens with shows"""
    screen = models.ForeignKey(
        Screen, on_delete=models.CASCADE, related_name="screen_show"
    )
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name="screen_show")
    slug = slug = models.SlugField(max_length=255, null=True, editable=False)

    def __str__(self):
        return f"{self.screen} {self.show}"

    def save(self, *args, **kwargs):
        self.slug = unique_slug_generator(self, variable=self)
        self.clean()
        super().save(*args, **kwargs)


class SeatingClass(models.Model):
    """Storing seating class like Gold,Silver etc"""
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)
    slug = models.SlugField(max_length=255, null=True, editable=False)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.slug = unique_slug_generator(self, variable=self.name)
        self.clean()
        super().save(*args, **kwargs)


class Fare(models.Model):
    """storing fare details for each show,screen and seating class"""
    screen_show = models.ForeignKey(
        ScreenShowMapper, on_delete=models.CASCADE, related_name="fare"
    )
    seating_class = models.ForeignKey(
        SeatingClass, on_delete=models.CASCADE, related_name="fare"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2,null=False, blank=False)
    def __str__(self):
        return f"{self.screen_show} {self.seating_class}-{self.price}Rs"


class Seat(models.Model):
    """Storing no_seats and its deatils for each screen."""
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name="seats")
    fare = models.ForeignKey(Fare, on_delete=models.CASCADE, related_name="seats")
    row = models.IntegerField(null=False, blank=False)
    column = models.IntegerField(null=False, blank=False)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.screen} {self.fare.seating_class}:Row-{self.row},Column-{self.column}"


class Booking(models.Model):
    """Storing booking information."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="booking")
    screen_show = models.ForeignKey(
        ScreenShowMapper, on_delete=models.CASCADE, related_name="booking"
    )
    booking_date = models.DateField(auto_now_add=False, auto_now=False)

    def __str__(self):
        return f"{self.user} - {self.screen_show} - {self.booking_date}"


class BookingSeat(models.Model):
    """Storing seats selected for each booking."""
    seat = models.ForeignKey(
        Seat, on_delete=models.CASCADE, related_name="booking_seat"
    )
    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, related_name="booking_seat"
    )
    booking_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.booking} - {self.seat}"


class Payment(models.Model):
    """Storing payment."""
    pay_methods = (
        ("DEBIT CARD", "Debit card"),
        ("CREDIT CARD", "Credit card"),
        ("NET BANKING", "Net banking"),
        ("UPI", "UPI"),
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=pay_methods)
    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, related_name="payment"
    )
    coupon = models.CharField(null=True, blank=True, max_length=20)
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.booking} {self.payment_method} {self.payment_status}"

    def save(self, *args, **kwargs):
        booking_seats = BookingSeat.objects.filter(booking=self.booking)
        total_amount = sum(
            [booking_seat.seat.fare.price for booking_seat in booking_seats]
        )
        self.amount = total_amount

        super(Payment, self).save(*args, **kwargs)
