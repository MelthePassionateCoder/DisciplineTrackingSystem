from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Student, Violation, OffenseSummary
from .forms import ViolationForm, StudentRegisterForm, ChangePasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages

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
    violations = Violation.objects.filter(student=student).order_by('violation_number')
    context = {'student': student, 'violations': violations}
    pdf = render_to_pdf('disciplinetracking/pdf_template.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="student_violations.pdf"'
        return response
    return HttpResponse("Error generating PDF", status=500)

class PostListView(ListView):
	model = Student
	template_name ='disciplinetracking/list_view.html'
	context_object_name = 'students'
	ordering = ['-date_posted']
	paginate_by = 10
	
	def get_queryset(self):
		query = self.request.GET.get('q')
		if query:
			if query.isdigit():
				return Student.objects.filter(lrn__icontains=query).order_by('-date_posted')
			else:
				return Student.objects.filter(name__icontains=query).order_by('-date_posted')
		return Student.objects.all().order_by('-date_posted')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['search_query'] = self.request.GET.get('q', '')
		return context
	
class StudentViolationsView(DetailView):
	model = Student
	template_name = 'disciplinetracking/list_violation_view.html'
	context_object_name = 'student'
	paginate_by = 5
	

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['violations'] = Violation.objects.filter(
			student=self.kwargs['pk']
		).order_by('-violation_number')
		return context

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Student
	form_class= StudentRegisterForm
	template_name = 'disciplinetracking/create_student_view.html'

	def form_valid(self, form):
		form.instance.created_by = self.request.user
		return super().form_valid(form)

class PostCreateViolationView(LoginRequiredMixin, CreateView):
	template_name = 'disciplinetracking/create_violation_view.html'

	def get(self, request, pk):
		student = Student.objects.get(pk=pk)
		form = ViolationForm()
		return render(request, "disciplinetracking/create_violation_view.html", {'student': student, 'form': form})
	
	def post(self, request, pk):
		student = Student.objects.get(pk=pk)
		form = ViolationForm(request.POST, request.FILES)
		if form.is_valid():
			form.instance.student = student
			form.instance.created_by = self.request.user
			last_violation = Violation.objects.filter(student=student).order_by('-violation_number').first()
			if last_violation:
				if Violation.objects.filter(student=student, violation_number=last_violation.violation_number).exists():
					form.instance.violation_number = last_violation.violation_number + 1
				else:
					form.instance.violation_number =1
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
	form_class = ViolationForm
	template_name = "disciplinetracking/update_violation_view.html"

	def get_queryset(self):
		student_id = self.kwargs['pk']
		return Violation.objects.filter(student__id=student_id)

	def get_object(self, queryset=None):
		violation_id = self.kwargs['pk']
		return get_object_or_404(Violation, id=violation_id)

	def form_valid(self, form):
		return super().form_valid(form)

	def form_invalid(self, form):
		return super().form_invalid(form)


class DeleteViolationView(LoginRequiredMixin, DeleteView):
    model = Violation
    template_name = 'disciplinetracking/delete_violation.html'
	
    def get_success_url(self):
        return reverse_lazy('disciplinetracking-list', kwargs={'pk': self.object.student.pk})

class DeleteStudentView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = 'disciplinetracking/delete_student.html'
    success_url = reverse_lazy('disciplinetracking-home') 

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return super().delete(request, *args, **kwargs)

class ChangePassword(PasswordChangeView):
	form_class = ChangePasswordForm
	success_url = reverse_lazy('disciplinetracking-home')
	template_name = 'disciplinetracking/change_password.html'
	
	def form_valid(self, form):
		response = super().form_valid(form)
		messages.success(self.request, 'Your password was successfully changed.')
		return response

	def form_invalid(self, form):
		response = super().form_vinvalid(form)
		messages.error(self.request, 'There was an error changing your password. Please try again.')
		return response
		
  
def offense_summary(request):
    school_years = ['2025-2026','2024-2025','2023-2024','2022-2023','2021-2022', '2020-2021', '2019-2020'] 
    selected_year = request.GET.get('school_year', None)

    if selected_year:
        summaries = OffenseSummary.objects.filter(school_year=selected_year).order_by("-school_year")
    else:
        summaries = OffenseSummary.objects.all().order_by("-school_year")

    return render(request, 'disciplinetracking/summary_report.html', {'summaries': summaries, 'school_years': school_years, 'selected_year': selected_year})
