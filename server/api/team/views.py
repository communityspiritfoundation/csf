from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Team
from ..users.models import User
from ..event.models import Event
from .serializers import TeamSerialiser
from django.core.exceptions import ObjectDoesNotExist

from django.http import HttpResponse


@api_view(["POST"])
def create_team(request):
    if request.user.is_authenticated is False:
        return Response("User not authenticated", status=403)
    else:
        serialiser = TeamSerialiser(data=request.data)
        if serialiser.is_valid():
            serialiser.save()
            return Response(serialiser.data, status=200)
        else:
            return Response(serialiser.errors, status=400)


@api_view(["GET"])
def get_team(request, team_id):
    users = User.objects.filter(team_id=team_id)
    users_events = []
    for users in users:
        for event in users.users_events.all():
            new_event = Event.objects.get(name=event)
            if new_event.name not in users_events:
                users_events.append(new_event.name)
    try:
        team = Team.objects.get(team_id=team_id)
    except ObjectDoesNotExist:
        return Response("Team does not exist", status=500)
    team.users_events = users_events
    serializer = TeamSerialiser(team)
    return Response(serializer.data, status=200)


@api_view(["GET"])
def get_teams(request):
    teams = Team.objects.all()
    serializer = TeamSerialiser(teams, many=True)
    return Response(serializer.data, status=200)


@api_view(["PUT"])
def update_team(request, team_id):
    if request.user.is_authenticated is False:
        return Response("User not authenticated", status=403)
    else:
        team = Team.objects.get(team_id=team_id)
        team_name_formatted = f"{team.name} - {team.join_code}"
        if str(request.user.team_id) != str(team_name_formatted):
            return HttpResponse(
                "User isn't authenticated to make changes to this team", status=403
            )
        else:
            if request.user.team_admin is False:
                return HttpResponse("User isn't an admin of this team", status=403)
            else:
                serializer = TeamSerialiser(instance=team, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=200)
                else:
                    return Response(serializer.errors, status=400)


@api_view(["DELETE"])
def delete_team(request, team_id):
    if request.user.is_authenticated is False:
        return Response("User is not authenticated", status=403)
    else:
        team = Team.objects.get(team_id=team_id)
        team_name_formatted = f"{team.name} - {team.join_code}"
        if (
            str(request.user.team_id) != str(team_name_formatted)
            and request.user.team_admin is False
        ):
            return Response("User is not authorised to delete this team", status=403)
        else:
            team.delete()
            request.user.team_admin = False
            request.user.team_id = None
            request.user.save()
            return Response("Team successfully deleted", status=200)
