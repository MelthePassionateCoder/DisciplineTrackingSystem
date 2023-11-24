from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Student, Violation
from .forms import ViolationForm, StudentRegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
# def add_violation(request):
#     if request.method == 'POST':
#         form = ViolationForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('success_page')  # Redirect to a success page or wherever you want
#     else:
#         form = ViolationForm()

#     return render(request, 'your_template.html', {'form': form}

# def add_violation(request):
#     if request.method == 'POST':
#         form = ViolationForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.instance.created_by = request.user  # Set the created_by field
#             form.save()
#             return redirect('success_page')  # Redirect to a success page or wherever you want
#     else:
#         form = ViolationForm()

#     return render(request, 'create_view.html', {'form': form})
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def download_pdf(request, pk):
    student = get_object_or_404(Student, pk=pk)
    violations = Violation.objects.filter(student=student)
    context = {'student': student, 'violations': violations}
    pdf = render_to_pdf('disciplinetracking/pdf_template.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="student_violations.pdf"'
        return response
    return HttpResponse("Error generating PDF", status=500)

class PostListView(LoginRequiredMixin,ListView):
	model = Student
	template_name ='disciplinetracking/list_view.html'
	# <app>/<model>_<viewtype>.html
	context_object_name = 'students'
	ordering = ['-date_posted']

	def get_queryset(self):
		query = self.request.GET.get('q')
		if query:
			return Student.objects.filter(name__icontains=query)
		return Student.objects.all()

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['search_query'] = self.request.GET.get('q', '')
		return context

# class ArticleListView(ListView):
#     template_name = 'article.html'
#     paginate_by = 25

#     def get_queryset(self):
#         return Article.objects..prefetch_related(
#             'author'
#         ).order_by('-created_at')

class StudentViolationsView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'disciplinetracking/list_violation_view.html'
    context_object_name = 'student'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['violations'] = Violation.objects.filter(
            student=self.kwargs['pk']
        ).order_by('-school_year')
        return context
	# def student_detail(request, pk):
	# 	# student = get_object_or_404(Student, pk=pk)
	# 	# violations = Violation.objects.filter(student=student)

	# 	# render(request, 'disciplinetracking/list_violation_view.html', {'student': student, 'violations': violations})
	# 	student = get_object_or_404(Student, pk=pk)
	# 	violations = Violation.objects.filter(student=student)
	# 	return render(request, 'disciplinetracking/list_violation_view.html', {'student': student, 'violations': violations})

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Student
	form_class= StudentRegisterForm
	template_name = 'disciplinetracking/create_student_view.html'

	def form_valid(self, form):
		form.instance.created_by = self.request.user
		return super().form_valid(form)

class PostCreateViolationView(LoginRequiredMixin, CreateView):
	# form_class=ViolationForm
	# template_name = 'disciplinetracking/create_violation_view.html'
	model= Violation
	fields = ['narrative_report','school_year','pictures','date_posted']
	template_name = 'disciplinetracking/create_violation_view.html'
	# def form_valid(self, form):
	# 	form.instance.created_by = self.request.user
	# 	return super().form_valid(form)
	def get(self, request, pk):
		student = Student.objects.get(pk=pk)
		form = ViolationForm()
		return render(request, "disciplinetracking/create_violation_view.html", {'student': student, 'form': form})
	
	def post(self, request, pk):
		student = Student.objects.get(pk=pk)
		form = ViolationForm(request.POST, request.FILES)
		if form.is_valid():
			form.save(commit=False)
			form.instance.student = student
			form.instance.created_by = self.request.user
			form.save()
			return redirect('disciplinetracking-list', pk=student.pk)
		else:
			print(form.errors)  # Check form errors in console
		return render(request, self.template_name, {'student': student, 'form': form})
	
class PostUpdateView(LoginRequiredMixin, UpdateView):
	model = Student
	form_class = StudentRegisterForm
	template_name = "disciplinetracking/update_student_view.html"
	
	
class PostUpdateViolationView(LoginRequiredMixin, UpdateView):
	model = Violation
	form_class = ViolationForm
	template_name = "disciplinetracking/update_violation_view.html"
	# def form_valid(self, form):
	# 	if form.is_valid():
	# 		form.save(commit=False)
	# 		form.instance.created_by = self.request.user
	# 		form.save()
	# 		return self.model.objects.filter(
    #         student=self.kwargs['pk']
    #     ).order_by('-date_posted').first()


	
	def form_valid(self, form):
		return super().form_valid(form)
	

class PostDetailView(LoginRequiredMixin, DetailView):
	model = Violation
	template_name = "disciplinetracking/detail_view.html"

class DeleteViolationView(LoginRequiredMixin, DeleteView):
    model = Violation
    template_name = 'disciplinetracking/delete_violation.html'

    def get_success_url(self):
        # Redirect to the student's violations page after successful deletion
        return reverse_lazy('disciplinetracking-list', kwargs={'pk': self.object.student.pk})

class DeleteStudentView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = 'disciplinetracking/delete_student.html'
    success_url = reverse_lazy('disciplinetracking-home')  # Redirect to the student list after successful deletion

    def delete(self, request, *args, **kwargs):
        # Call the overridden delete method in the Student model
        self.object = self.get_object()
        self.object.delete()
        return super().delete(request, *args, **kwargs)
		
  
    
	
