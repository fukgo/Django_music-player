from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from .forms import ContactForm
class ContactView(View):
    def get(self,request):
        return render(request, 'other/contact_us.html')
    def post(self,request):
        form = ContactForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            return JsonResponse({'status':'success','message':'感谢您的反馈，我们会尽快处理'})
        else:
            return JsonResponse({'status':'fail','message':'请检查您的输入是否正确'})

