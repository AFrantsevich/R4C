import json
from datetime import datetime, timedelta
from http import HTTPStatus

from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_list_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .forms import RobotForm
from .models import Robot
from .tools import export_to_excel, prepare_data_for_ex

PERIOD_TO_REPORT = 1
FILENAME = f"Perort_by_%s.xlsx"


@csrf_exempt
def add_robot_in_db(request):
    if request.method == "POST":
        try:
            json_data = json.loads(request.body)
        except ValueError:
            return JsonResponse(
                {"error": "Wrong data request"}, status=HTTPStatus.BAD_REQUEST
            )
        data = RobotForm(json_data)
        data.is_valid()
        if data.errors:
            return JsonResponse(
                json.loads(data.errors.as_json()), status=HTTPStatus.BAD_REQUEST
            )
        data.save()
        return JsonResponse(data.cleaned_data, status=HTTPStatus.CREATED)

    return JsonResponse(
        {"error": "Wrong request, only POST"}, status=HTTPStatus.BAD_REQUEST
    )


def get_report(request):
    time_now = datetime.now(tz=timezone.utc)
    data_to = time_now - timedelta(days=PERIOD_TO_REPORT)

    if request.method == "GET":
        try:
            data = get_list_or_404(
                Robot.objects.exclude(created__lt=data_to).order_by("model")
            )
        except Http404:
            return JsonResponse(
                {"error": "No data for export"}, status=HTTPStatus.NOT_FOUND
            )
        date_to_wr = prepare_data_for_ex(data)
        output = export_to_excel(date_to_wr)
        response = HttpResponse(
            output,
            content_type="application/"
            "vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet",
            status=HTTPStatus.OK,
        )
        response["Content-Disposition"] = (
            "attachment; filename=%s" % FILENAME % (time_now.strftime("%d-%m-%y %H-%M"))
        )
        return response

    return JsonResponse(
        {"error": "Wrong request, only GET"}, status=HTTPStatus.BAD_REQUEST
    )
