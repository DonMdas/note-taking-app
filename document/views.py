from django.shortcuts import render, redirect
from .models import Note
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .gemini_utils import generate_summary
from datetime import datetime, timedelta

 

# create dashboard page
@login_required(login_url='/login/')
def dashboard(request):
    # Get all notes for the current user
    notes = Note.objects.filter(user=request.user)
    
    # Get count of notes created in the last 7 days
    one_week_ago = datetime.now() - timedelta(days=7)
    recent_note_count = Note.objects.filter(user=request.user, created_at__gte=one_week_ago).count()
    
    # Get count of notes edited in the last 3 days
    three_days_ago = datetime.now() - timedelta(days=3)
    recently_edited_count = Note.objects.filter(user=request.user, modified_at__gte=three_days_ago).count()
    
    context = {
        'notes': notes,
        'recent_note_count': recent_note_count,
        'recently_edited_count': recently_edited_count
    }
    
    return render(request, 'dashboard.html', context)


# create editor page
@login_required(login_url='/login/')
def editor(request):
    docid = int(request.GET.get('docid', 0))
    notes = Note.objects.filter(user=request.user)  # show only user's notes

    if request.method == 'POST':
        docid = int(request.POST.get('docid', 0))
        title = request.POST.get('title')
        content = request.POST.get('content', '')
        summary = request.POST.get('summary', '')  # Get summary from form

        if docid > 0:
            note = Note.objects.get(pk=docid, user=request.user)
            note.title = title
            note.content = content
            note.summary = summary  # Save the summary
            note.save()
            return redirect('/?docid=%i' % docid)
        else:
            note = Note.objects.create(
                title=title, content=content, summary=summary, user=request.user
            )
            return redirect('/?docid=%i' % note.id)

    if docid > 0:
        try:
            note = Note.objects.get(pk=docid, user=request.user)
        except Note.DoesNotExist:
            note = ''
    else:
        note = ''

    context = {
        'docid': docid,
        'notes': notes,
        'note': note
    }

    return render(request, 'editor.html', context)

 
# create delete notes page
 
 
@login_required(login_url='/login/')
def delete_note(request, docid):
    try:
        note = Note.objects.get(pk=docid, user=request.user)
        note.delete()
    except Note.DoesNotExist:
        pass
    return redirect('/?docid=0')

 
 
# login page for user
def login_page(request):
    # If user is already authenticated, redirect to dashboard page
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username)
            if not user_obj.exists():
                messages.error(request, "Username not found")
                return redirect('/login/')
            user_obj = authenticate(username=username, password=password)
            if user_obj:
                login(request, user_obj)
                return redirect('dashboard')  # Changed to redirect to dashboard
            messages.error(request, "Wrong Password")
            return redirect('/login/')
        except Exception as e:
            messages.error(request, "Something went wrong")
            return redirect('/register/')
    return render(request, "login.html")
 
 
# register page for user
def register_page(request):
    # If user is already authenticated, redirect to dashboard page
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username)
            if user_obj.exists():
                messages.error(request, "Username is taken")
                return redirect('/register/')
            user_obj = User.objects.create(username=username)
            user_obj.set_password(password)
            user_obj.save()
            messages.success(request, "Account created")
            return redirect('/login')
        except Exception as e:
            messages.error(request, "Something went wrong")
            return redirect('/register')
    return render(request, "register.html")
 
 
# logout function
def custom_logout(request):
    logout(request)
    return redirect('login')

# Add this new view
@login_required(login_url='/login/')
def summarize_note(request):
    """API endpoint to summarize note content"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
    
    try:
        content = request.POST.get('content', '')
        docid = request.POST.get('docid', 0)
        
        # Generate summary
        summary = generate_summary(content)
        
        # If docid is provided, save the summary to the note
        if int(docid) > 0:
            try:
                note = Note.objects.get(pk=int(docid), user=request.user)
                note.summary = summary
                note.save()
            except Note.DoesNotExist:
                pass
        
        return JsonResponse({'summary': summary})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
