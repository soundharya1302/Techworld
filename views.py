from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages
from .models import Movie, Theatre, Seat, Ticket, Moviedetails
from .forms import SignUpForm, MovieForm, SeatSelectionForm, BookTicketForm
from django.http import Http404, JsonResponse


def home(request):
    return render(request, 'home.html')

def movie_list(request):
    # Fetch all movies from the database
    movies = Movie.objects.all()
    return render(request, 'movie_list.html', {'movies': movies})

def movie_details(request, id):
    try:
        movie_1 = Moviedetails.objects.get(id=id)
    except Moviedetails.DoesNotExist:
        raise Http404("Movie not found")
    return render(request, 'movie_detail.html', {'movie': movie_1})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Log the user in
            auth_login(request, user)
            
            # Get the first available movie (or customize the logic as needed)
            latest_movie = Movie.objects.first()  # Adjust this logic if necessary
            
            if latest_movie:
                # Redirect to theatre list with movie_id
                return redirect('theatres', movie_id=latest_movie.id)
            else:
                # Handle the case where no movie is found
                messages.error(request, 'No movies available.')
                return redirect('home')  # Redirect to home or any other page as fallback
        
        else:
            messages.error(request, 'Invalid username or password.')
    
    # Render the login page if GET request or login fails
    return render(request, 'login.html')


def theatre_list(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    theatres = Theatre.objects.filter(movie=movie)
    
    if request.method == 'POST':
        selected_theatre_id = request.POST.get('theatre')
        # Redirect to seat selection page with selected theatre
        return redirect('seat_selection', theatre_id=selected_theatre_id, movie_id=movie.id)

    return render(request, 'theatre_list.html',  {'theatres': theatres, 'movie_id': movie_id})


def seat_selection(request, movie_id, theatre_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    theatre = get_object_or_404(Theatre, pk=theatre_id)
    seats = Seat.objects.filter(theatre=theatre)  # Fetching the seats for the selected theatre

    return render(request, 'seat_selection.html', {
        'movie': movie,
        'theatre': theatre,
        'seats': seats,  # Pass the seats to the template
    })

def select_seat(request):
    if request.method == 'POST':
        seat_id = request.POST.get('seat_id')
        action = request.POST.get('action')  # 'select' or 'deselect'

        if not seat_id or action not in ['select', 'deselect']:
            return JsonResponse({'status': 'error', 'message': 'Invalid parameters'}, status=400)

        seat = get_object_or_404(Seat, id=seat_id)

        if action == 'select':
            if not seat.is_booked:
                seat.is_booked = True
                seat.save()
                return JsonResponse({'status': 'success', 'message': f'Seat {seat_id} has been selected.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Seat is already booked'}, status=400)
        elif action == 'deselect':
            if seat.is_booked:
                seat.is_booked = False
                seat.save()
                return JsonResponse({'status': 'success', 'message': f'Seat {seat_id} has been deselected.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Seat is not booked'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)



def book_ticket(request, movie_id, theatre_id, seat_id):
    # Fetch the relevant Movie, Theatre, and Seat instances
    movie = get_object_or_404(Movie, id=movie_id)
    theatre = get_object_or_404(Theatre, id=theatre_id)
    seat = get_object_or_404(Seat, seat_number=seat_id, theatre=theatre)
    
    user_name = request.user.username
    show_time = "11:00 AM"

    context = {
        'user': {'name': user_name},
        'movie': movie,
        'theatre': theatre,
        'seat': seat,
       'show': {'time': show_time},
    }

    
    return render(request, 'book_ticket.html', context)


def booking_confirmation(request):
   
    
    return render(request, 'booking_confirmation.html')