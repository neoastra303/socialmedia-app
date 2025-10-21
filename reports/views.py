from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from .models import Report
from .forms import ReportForm
from django.contrib.auth.models import User
from posts.models import Post, Comment

@login_required
def report_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.reported_post = post
            report.save()
            messages.success(request, 'تم إرسال التقرير بنجاح.')
            return redirect('posts:post_detail', post_id=post.id)
    else:
        form = ReportForm()
    return render(request, 'reports/report_form.html', {'object': post, 'type': 'post', 'form': form})

@login_required
def report_user(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.reported_user = user
            report.save()
            messages.success(request, 'تم إرسال التقرير بنجاح.')
            return redirect('users:profile', username=username)
    else:
        form = ReportForm()
    return render(request, 'reports/report_form.html', {'object': user, 'type': 'user', 'form': form})

@user_passes_test(lambda u: u.is_staff)
def admin_reports(request):
    reports = Report.objects.all().order_by('-created_at')
    return render(request, 'reports/admin_reports.html', {'reports': reports})

@user_passes_test(lambda u: u.is_staff)
def resolve_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        report.status = action
        report.resolved_at = timezone.now()
        report.resolved_by = request.user
        report.save()
        messages.success(request, f'تم {action} التقرير.')
        return redirect('reports:admin_reports')
    return render(request, 'reports/resolve_report.html', {'report': report})
