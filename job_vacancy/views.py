from django.shortcuts import render, redirect
from .forms import VacancyForm
from django.conf import settings
from .models import Applicant
from datetime import datetime
import os
import json


def apply(request):
    form = VacancyForm()

    if request.method == 'POST':
        form = VacancyForm(request.POST, request.FILES)

        if form.is_valid():

            # save to database
            applicant = Applicant.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                address=form.cleaned_data['address'],
                cv=request.FILES['cv'],
            )

            # save to json file using the DB id
            record = {
                "id": applicant.id,
                "name": applicant.name,
                "submitted_at": datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                "address": applicant.address,
                "email": applicant.email,
                "cv_filename": applicant.cv.name,
            }

            submissions_dir = os.path.join(
                settings.BASE_DIR, 'job_vacancy', 'submissions')
            os.makedirs(submissions_dir, exist_ok=True)

            json_file = os.path.join(submissions_dir, 'applications.json')

            records = []

            if os.path.exists(json_file):
                with open(json_file, 'r') as f:
                    try:
                        records = json.load(f)
                    except json.JSONDecodeError:
                        records = []

            records.append(record)

            with open(json_file, 'w') as f:
                json.dump(records, f)

            return redirect('success')

    return render(request, 'applicants/apply.html', {'form': form})


def success(request):
    return render(request, 'applicants/success.html')
