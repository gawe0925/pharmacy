import pandas as pd
from pharmacy import MyPharmacy
from rest_framework import status
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response


class ExcelProcessAPIView(APIView):
    def post(self, request, *args, **kwargs):
        excel_file = request.FILES.get('file')

        if not excel_file:
            return Response({"error" : "excel_file not provided"}, status=400)
        
        try:
            df = pd.read_excel(excel_file)

            result = MyPharmacy.pharmacy(df)

            return Response({"message" : "The amount of Incoming_Stock has been updated"}, status=200)

        except Exception as e:
            return Response()