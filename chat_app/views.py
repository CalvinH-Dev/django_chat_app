from json import dumps, loads

from django.forms import ValidationError
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views import View

from .models import Chat


class ChatView(View):
    def get(self, request: HttpRequest):
        return HttpResponse("ok get")

    def post(self, request: HttpRequest):
        try:
            data = loads(request.body)
            name = data["name"]
            message = data["message"]

        except ValueError:
            return HttpResponse(status=204)
        except KeyError as ke:
            field = ke.args[0]
            return HttpResponse(
                f"No field '{field}' found.",
                status=422,
            )

        name_max_length: int = Chat.name.field.max_length  # type: ignore
        mesage_max_length: int = Chat.message.field.max_length  # type: ignore

        if len(name) > name_max_length:
            return HttpResponse(
                f"Field 'name' too long (max {name_max_length}).", status=422
            )

        if len(message) > mesage_max_length:
            return HttpResponse(
                f"Field 'message' too long (max {mesage_max_length}).",
                status=422,
            )

        chat_message = Chat(name=name, message=message)

        try:
            chat_message.clean_fields()
        except ValidationError as ve:
            print(ve)
            return JsonResponse(ve.message_dict, status=422, safe=False)

        chat_message.save()
        print(chat_message)

        response_object = {"name": name, "message": message}

        return JsonResponse(response_object, status=201)
