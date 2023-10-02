import json
from http import HTTPStatus

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .forms import RobotForm

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
