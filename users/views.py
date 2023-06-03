from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ImageUploadForm
from food.models import Post
import requests

def register(request):
    if request.method  == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in, {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']

            # Upload the image to Azure and get the prediction
            headers = {
                'Prediction-Key': '8ee198d954d64cd1bf84138c0054cd17',
                'Content-Type': 'application/octet-stream'
            }
            response = requests.post(
                'https://foodprediction-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/455e7c4f-3111-43ca-91e5-45cdb1f75c47/classify/iterations/Iteration1/image',
                headers=headers,
                data=image.read(),
            )

            if response.status_code != 200:
                messages.error(request, 'There was an error processing the image. Please try again.')
                return redirect('profile')

            # Extract the prediction results
            result = response.json()
            print("Response status code: ", response.status_code)
            print("Full response content: ", result)
            predictions = result['predictions']

            # Find the prediction with the highest probability
            best_prediction = max(predictions, key=lambda x: x['probability'])

            # The tagName field contains whether the fruit is fresh or rotten
            fruit_status = best_prediction['tagName']

            # Save the post
            post = Post(image=image, prediction=fruit_status, author=request.user)
            post.save()

            messages.success(request, f'Your post has been created. The fruit is predicted to be: {fruit_status}.')
            return redirect('profile')
    else:
        form = ImageUploadForm()

    # Get the user's posts for display on the profile page
    posts = Post.objects.filter(author=request.user)

    context = {
        'form': form,
        'posts': posts,
    }

    return render(request, 'users/profile.html', context)

@login_required
def past_results(request):
    # Get the user's posts for display on the past results page
    posts = Post.objects.filter(author=request.user).order_by('-date_posted')

    context = {
        'posts': posts,
    }

    return render(request, 'users/past_results.html', context)

