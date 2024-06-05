from django.shortcuts import render, redirect
from django.views import View
from bot.forms import InputForm

from bot.langchain import askbot

class Home(View):
    def get(self, request):
        ai_response = request.session.get('ai_response','')

        form = InputForm()
        return render(request, "bot/home.html", {
            'form': form,
            'ai_response':ai_response
        })
    
  
    def post(self, request):
        form = InputForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            # print(message)

            response = askbot(message)
            request.session['ai_response'] = response

        form = InputForm()
        return redirect('/')  # Redirect to the named URL pattern
    



