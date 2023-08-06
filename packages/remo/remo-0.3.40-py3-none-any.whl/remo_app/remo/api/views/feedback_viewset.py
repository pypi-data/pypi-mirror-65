from django.conf import settings

from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from remo_app.remo.api.serializers import FeedbackSerializer
from remo_app.remo.models import Feedback
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import json


class FeedbackViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = FeedbackSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        self.send_email(serializer.data)

    def send_email(self, data):
        user = self.request.user

        user_fullname = f'{user.first_name} {user.last_name}'

        text = json.loads(data['text'])

        html_msg = f"""
        <h5>Feedback from user</h5>
        <p>
            <b>Name:</b> {user_fullname} </br>
            <b>Email:</b> {user.username} </br>
            <b>Page:</b> {data['page_url']} </br>
            <b>Type:</b> {text['type']} </br>
            <b>Message:</b> {text['message']} </br>
        </p>
        </br>
        <img src="{data['screenshot']}" alt="screenshot" />
        """
        message = Mail(
            from_email='noreply@remo.ai',
            to_emails=settings.EMAIL_LIST,
            subject=f'Remo feedback from {user_fullname}',
            html_content=html_msg
        )

        try:
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            sg.send(message)
        except Exception as e:
            print(e)


class Feedbacks(GenericAPIView):
    serializer_class = FeedbackSerializer
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        key = request.query_params.get('access-key')
        if key != settings.FEEDBACKS_ACCESS_KEY:
            return Response(status=403)

        queryset = Feedback.objects.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

