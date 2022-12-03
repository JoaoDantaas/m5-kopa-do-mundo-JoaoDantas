from django.shortcuts import render
from rest_framework.views import APIView, Response, Request
from teams.models import Team
from django.forms.models import model_to_dict

class TeamsView(APIView):
    def post(self, request: Request) -> Response:
        team_data = request.data

        team = Team.objects.create(**team_data)

        return Response(model_to_dict(team), 201)

    def get(self, request: Request) -> Response:
        teams = Team.objects.all()

        teams_dict = []

        for team in teams:
            teams_dict.append(model_to_dict(team))
        
        return Response(teams_dict)

class TeamViewId(APIView):
    def get(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(pk=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, 404)

        team_dict = model_to_dict(team)

        return Response(team_dict)

    def patch(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(pk=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, 404)

        for key, value in request.data.items():
            setattr(team, key, value)
        
        team.save()

        team_dict = model_to_dict(team)

        return Response(team_dict, 200)

    def delete(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(pk=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, 404)

        team.delete()

        return Response(status=204)