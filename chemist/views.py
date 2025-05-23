import pandas as pd
from io import BytesIO
from datetime import date
from chemist.restock import ReStcok
from django.http import HttpResponse
from chemist.pharmacy import MyPharmacy
from rest_framework.views import APIView
from rest_framework.response import Response

from chemist.models import Product, DailySales, IncomingOrder

today = date.today()

class ExcelProcessAPIView(APIView):

    def get(self, request, *args, **kwargs):
        output = BytesIO()
        update_result = ReStcok.renew_stock()
        if not update_result:
            print({"message" : "incoming stock up to date"})
        else:
            print({"message" : "incoming stock been updated"})

        products = Product.objects.all()

        p = MyPharmacy()
        if not products:
            result_df = p.init_pharmacy(today)
        else:
            result_df = p.non_order(today)
        
        result_df.to_excel(output, index=False)
        output.seek(0)

        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        file_name = f'{today}_order_suggestion.xlsx'
        response['Content-Disposition'] = f'attachment; filename={file_name}'

        return response

    def post(self, request, *args, **kwargs):
        output = BytesIO()
        excel_file = request.FILES.get('file')

        try:
            df = pd.read_excel(excel_file)
            if df.empty:
                return Response({"error": "Invaild data"}, status=400)
            update_result = ReStcok.renew_stock()
            if not update_result:
                print({"message" : "incoming stock up to date"})
            else:
                print({"message" : "incoming stock been updated"})
            p = MyPharmacy()
            result_df = p.with_new_order(df, today)
            result_df.to_excel(output, index=False)
            output.seek(0)
            response = HttpResponse(
                output.getvalue(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )

            file_name = f'{today}_order_suggestion.xlsx'
            response['Content-Disposition'] = f'attachment; filename={file_name}'

            return response
        
        except Exception as e:
            return Response({"error" : f"{str(e)}"}, status=400)

    def put(self, request, *args, **kwargs):
        try:
            Product.objects.all().delete()
            DailySales.objects.all().delete()
            IncomingOrder.objects.all().delete()
            return Response({"message": "Data has been clean up"})
        except:
            return Response({"message": "Fail to delete data"})