import io
import boto3
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
from datetime import datetime
from dotenv import load_dotenv
from reportlab.lib import colors
from statistics import mean, stdev
import numpy as np
from apps.ST.models import Temperatura
from apps.SIL.models import IntensidadDeLuz
from apps.SHA.models import HumedadDeAmbiente
from apps.SHS.models import HumedadDeSuelo
from apps.plants.models import Planta
# Carga las variables de entorno desde el archivo .env
load_dotenv()

class GenerarReporteTemperaturaView(APIView):
    def post(self, request):
        planta_id = request.data.get('planta_id')

        # Obtener el objeto Planta correspondiente al planta_id proporcionado
        try:
            planta = Planta.objects.get(pk=planta_id)
        except Planta.DoesNotExist:
            return Response({'error': f'La planta con ID {planta_id} no existe.'}, status=status.HTTP_404_NOT_FOUND)


        if not planta_id:
            return Response({'error': 'Se requiere el parámetro planta_id en el cuerpo de la solicitud.'}, status=status.HTTP_400_BAD_REQUEST)

        # Obtener todos los registros de la tabla Temperatura con el planta_id especificado
        
        registros = Temperatura.objects.filter(planta_id=planta_id)

        # Obtener los valores de temperatura de los registros
        valores_temperatura = [registro.valor for registro in registros]

        # Calcular el promedio, desviación estándar y correlación de los valores de temperatura
        promedio = mean(valores_temperatura)
        desviacion_estandar = stdev(valores_temperatura)
        correlacion = np.corrcoef(valores_temperatura, valores_temperatura)[0, 1]

        # Generar el PDF con texto predeterminado y tabla
        response = HttpResponse(content_type='application/pdf')
        # Utilizar la fecha formateada en el nombre del archivo PDF
        fecha_actual = datetime.now()
        fecha_formateada = fecha_actual.strftime('%Y%m%d_%H%M%S')
        response['Content-Disposition'] = f'attachment; filename="reporte_semanal_Temperatura_{fecha_formateada}.pdf"'
        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []

        # Obtener los estilos de muestra proporcionados por reportlab
        styles = getSampleStyleSheet()

        # Agregar texto predeterminado al PDF
        elements.append(Paragraph(f"Reporte semanal de registro de temperatura para planta: {planta.nombre}", styles['Title']))
        elements.append(Spacer(1, 12))  # Espacio en blanco
        elements.append(Paragraph(f"Promedio de temperatura: {promedio:.2f}", styles['Normal']))
        elements.append(Paragraph(f"Desviación estándar de temperatura: {desviacion_estandar:.2f}", styles['Normal']))
        elements.append(Paragraph(f"Correlación de temperatura: {correlacion:.2f}", styles['Normal']))
        elements.append(Spacer(1, 12))  # Espacio en blanco

        # Generar una tabla con los registros de Temperatura
        data = [
            ["ID", "Planta ID", "Fecha/Hora", "Valor"]
        ]
        for registro in registros:
            data.append([registro.id, registro.planta_id, registro.fecha_hora, registro.valor])

        tabla = Table(data)
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Encabezado de la tabla
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Color de texto en el encabezado
            # ... (otros estilos de tabla según tus necesidades)
        ]))

        elements.append(tabla)
        doc.build(elements)

        # Subir el PDF generado al bucket de S3
        s3 = boto3.client('s3', 
        aws_access_key_id=os.environ.get('ACCESS_KEY'), 
        aws_secret_access_key=os.environ.get('SECRET_KEY'))
        bucket_name = os.environ.get('BUCKET_NAME')
        # Utilizar la fecha formateada en el nombre del archivo PDF
        pdf_filename = f'reporte_semanal_temperatura_{fecha_formateada}.pdf'
        pdf_data = response.content

        try:
            s3.upload_fileobj(io.BytesIO(pdf_data), bucket_name, pdf_filename)
        except Exception as e:
            # Manejar errores si algo sale mal durante la carga
            return Response({'error': 'Error al cargar el archivo PDF a S3'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Establecer la política de acceso para hacer el archivo público
        s3.put_object_acl(Bucket=bucket_name, Key=pdf_filename, ACL='public-read')

        # Obtener la URL del PDF recién generado
        url_reporte = f'https://{bucket_name}.s3.amazonaws.com/{pdf_filename}'

        # Devolver el enlace de descarga del PDF
        return Response({'url_reporte': url_reporte}, status=status.HTTP_200_OK)

class GenerarReporteIntensidadView(APIView):
    def post(self, request):
        planta_id = request.data.get('planta_id')

        # Obtener el objeto Planta correspondiente al planta_id proporcionado
        try:
            planta = Planta.objects.get(pk=planta_id)
        except Planta.DoesNotExist:
            return Response({'error': f'La planta con ID {planta_id} no existe.'}, status=status.HTTP_404_NOT_FOUND)


        if not planta_id:
            return Response({'error': 'Se requiere el parámetro planta_id en el cuerpo de la solicitud.'}, status=status.HTTP_400_BAD_REQUEST)

        # Obtener todos los registros de la tabla Temperatura con el planta_id especificado
        
        registros = IntensidadDeLuz.objects.filter(planta_id=planta_id)

        # Obtener los valores de temperatura de los registros
        valores_intensidad = [registro.valor for registro in registros]

        # Calcular el promedio, desviación estándar y correlación de los valores de temperatura
        promedio = mean(valores_intensidad)
        desviacion_estandar = stdev(valores_intensidad)
        correlacion = np.corrcoef(valores_intensidad, valores_intensidad)[0, 1]

        # Generar el PDF con texto predeterminado y tabla
        response = HttpResponse(content_type='application/pdf')
        # Utilizar la fecha formateada en el nombre del archivo PDF
        fecha_actual = datetime.now()
        fecha_formateada = fecha_actual.strftime('%Y%m%d_%H%M%S')
        response['Content-Disposition'] = f'attachment; filename="reporte_semanal_Intensidad_luz_{fecha_formateada}.pdf"'
        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []

        # Obtener los estilos de muestra proporcionados por reportlab
        styles = getSampleStyleSheet()

        # Agregar texto predeterminado al PDF
        elements.append(Paragraph(f"Reporte semanal de registro de Intensidad de luz para planta: {planta.nombre}", styles['Title']))
        elements.append(Spacer(1, 12))  # Espacio en blanco
        elements.append(Paragraph(f"Promedio de Intensidad de luz: {promedio:.2f}", styles['Normal']))
        elements.append(Paragraph(f"Desviación estándar de Intensidad de Luz: {desviacion_estandar:.2f}", styles['Normal']))
        elements.append(Paragraph(f"Correlación de Intensidad de luz: {correlacion:.2f}", styles['Normal']))
        elements.append(Spacer(1, 12))  # Espacio en blanco

        # Generar una tabla con los registros de Temperatura
        data = [
            ["ID", "Planta ID", "Fecha/Hora", "Valor"]
        ]
        for registro in registros:
            data.append([registro.id, registro.planta_id, registro.fecha_hora, registro.valor])

        tabla = Table(data)
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Encabezado de la tabla
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Color de texto en el encabezado
            # ... (otros estilos de tabla según tus necesidades)
        ]))

        elements.append(tabla)
        doc.build(elements)

        # Subir el PDF generado al bucket de S3
        s3 = boto3.client('s3', 
        aws_access_key_id=os.environ.get('ACCESS_KEY'), 
        aws_secret_access_key=os.environ.get('SECRET_KEY'))
        bucket_name = os.environ.get('BUCKET_NAME')
        # Utilizar la fecha formateada en el nombre del archivo PDF
        pdf_filename = f'reporte_semanal_Intensidad_luz_{fecha_formateada}.pdf'
        pdf_data = response.content

        try:
            s3.upload_fileobj(io.BytesIO(pdf_data), bucket_name, pdf_filename)
        except Exception as e:
            # Manejar errores si algo sale mal durante la carga
            return Response({'error': 'Error al cargar el archivo PDF a S3'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Establecer la política de acceso para hacer el archivo público
        s3.put_object_acl(Bucket=bucket_name, Key=pdf_filename, ACL='public-read')

        # Obtener la URL del PDF recién generado
        url_reporte = f'https://{bucket_name}.s3.amazonaws.com/{pdf_filename}'

        # Devolver el enlace de descarga del PDF
        return Response({'url_reporte': url_reporte}, status=status.HTTP_200_OK)

class GenerarReporteHumedadAmbienteView(APIView):
    def post(self, request):
        planta_id = request.data.get('planta_id')

        # Obtener el objeto Planta correspondiente al planta_id proporcionado
        try:
            planta = Planta.objects.get(pk=planta_id)
        except Planta.DoesNotExist:
            return Response({'error': f'La planta con ID {planta_id} no existe.'}, status=status.HTTP_404_NOT_FOUND)


        if not planta_id:
            return Response({'error': 'Se requiere el parámetro planta_id en el cuerpo de la solicitud.'}, status=status.HTTP_400_BAD_REQUEST)

        # Obtener todos los registros de la tabla Temperatura con el planta_id especificado
        
        registros = HumedadDeAmbiente.objects.filter(planta_id=planta_id)

        # Obtener los valores de temperatura de los registros
        valores_humedad_ambiente = [registro.valor for registro in registros]

        # Calcular el promedio, desviación estándar y correlación de los valores de temperatura
        promedio = mean(valores_humedad_ambiente)
        desviacion_estandar = stdev(valores_humedad_ambiente)
        correlacion = np.corrcoef(valores_humedad_ambiente, valores_humedad_ambiente)[0, 1]

        # Generar el PDF con texto predeterminado y tabla
        response = HttpResponse(content_type='application/pdf')
        # Utilizar la fecha formateada en el nombre del archivo PDF
        fecha_actual = datetime.now()
        fecha_formateada = fecha_actual.strftime('%Y%m%d_%H%M%S')
        response['Content-Disposition'] = f'attachment; filename="reporte_semanal_Humedad_ambiente_{fecha_formateada}.pdf"'
        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []

        # Obtener los estilos de muestra proporcionados por reportlab
        styles = getSampleStyleSheet()

        # Agregar texto predeterminado al PDF
        elements.append(Paragraph(f"Reporte semanal de registro de Humedad del ambiente para planta: {planta.nombre}", styles['Title']))
        elements.append(Spacer(1, 12))  # Espacio en blanco
        elements.append(Paragraph(f"Promedio de Humedad del ambiente: {promedio:.2f}", styles['Normal']))
        elements.append(Paragraph(f"Desviación estándar de Humedad del ambiente: {desviacion_estandar:.2f}", styles['Normal']))
        elements.append(Paragraph(f"Correlación de Humedad del ambiente: {correlacion:.2f}", styles['Normal']))
        elements.append(Spacer(1, 12))  # Espacio en blanco

        # Generar una tabla con los registros de Temperatura
        data = [
            ["ID", "Planta ID", "Fecha/Hora", "Valor"]
        ]
        for registro in registros:
            data.append([registro.id, registro.planta_id, registro.fecha_hora, registro.valor])

        tabla = Table(data)
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Encabezado de la tabla
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Color de texto en el encabezado
            # ... (otros estilos de tabla según tus necesidades)
        ]))

        elements.append(tabla)
        doc.build(elements)

        # Subir el PDF generado al bucket de S3
        s3 = boto3.client('s3', 
        aws_access_key_id=os.environ.get('ACCESS_KEY'), 
        aws_secret_access_key=os.environ.get('SECRET_KEY'))
        bucket_name = os.environ.get('BUCKET_NAME')
        # Utilizar la fecha formateada en el nombre del archivo PDF
        pdf_filename = f'reporte_semanal_Humedad_ambiente_{fecha_formateada}.pdf'
        pdf_data = response.content

        try:
            s3.upload_fileobj(io.BytesIO(pdf_data), bucket_name, pdf_filename)
        except Exception as e:
            # Manejar errores si algo sale mal durante la carga
            return Response({'error': 'Error al cargar el archivo PDF a S3'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Establecer la política de acceso para hacer el archivo público
        s3.put_object_acl(Bucket=bucket_name, Key=pdf_filename, ACL='public-read')

        # Obtener la URL del PDF recién generado
        url_reporte = f'https://{bucket_name}.s3.amazonaws.com/{pdf_filename}'

        # Devolver el enlace de descarga del PDF
        return Response({'url_reporte': url_reporte}, status=status.HTTP_200_OK)

class GenerarReporteHumedadSueloView(APIView):
    def post(self, request):
        planta_id = request.data.get('planta_id')

        # Obtener el objeto Planta correspondiente al planta_id proporcionado
        try:
            planta = Planta.objects.get(pk=planta_id)
        except Planta.DoesNotExist:
            return Response({'error': f'La planta con ID {planta_id} no existe.'}, status=status.HTTP_404_NOT_FOUND)


        if not planta_id:
            return Response({'error': 'Se requiere el parámetro planta_id en el cuerpo de la solicitud.'}, status=status.HTTP_400_BAD_REQUEST)

        # Obtener todos los registros de la tabla Temperatura con el planta_id especificado
        
        registros = HumedadDeSuelo.objects.filter(planta_id=planta_id)

        # Obtener los valores de temperatura de los registros
        valores_humedad_suelo = [registro.valor for registro in registros]

        # Calcular el promedio, desviación estándar y correlación de los valores de temperatura
        promedio = mean(valores_humedad_suelo)
        desviacion_estandar = stdev(valores_humedad_suelo)
        correlacion = np.corrcoef(valores_humedad_suelo, valores_humedad_suelo)[0, 1]

        # Generar el PDF con texto predeterminado y tabla
        response = HttpResponse(content_type='application/pdf')
        # Utilizar la fecha formateada en el nombre del archivo PDF
        fecha_actual = datetime.now()
        fecha_formateada = fecha_actual.strftime('%Y%m%d_%H%M%S')
        response['Content-Disposition'] = f'attachment; filename="reporte_semanal_Humedad_suelo{fecha_formateada}.pdf"'
        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []

        # Obtener los estilos de muestra proporcionados por reportlab
        styles = getSampleStyleSheet()

        # Agregar texto predeterminado al PDF
        elements.append(Paragraph(f"Reporte semanal de registro de Humedad de suelo para planta: {planta.nombre}", styles['Title']))
        elements.append(Spacer(1, 12))  # Espacio en blanco
        elements.append(Paragraph(f"Promedio de Humedad de suelo: {promedio:.2f}", styles['Normal']))
        elements.append(Paragraph(f"Desviación estándar de Humedad de suelo: {desviacion_estandar:.2f}", styles['Normal']))
        elements.append(Paragraph(f"Correlación de Humedad de suelo: {correlacion:.2f}", styles['Normal']))
        elements.append(Spacer(1, 12))  # Espacio en blanco

        # Generar una tabla con los registros de Temperatura
        data = [
            ["ID", "Planta ID", "Fecha/Hora", "Valor"]
        ]
        for registro in registros:
            data.append([registro.id, registro.planta_id, registro.fecha_hora, registro.valor])

        tabla = Table(data)
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Encabezado de la tabla
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Color de texto en el encabezado
            # ... (otros estilos de tabla según tus necesidades)
        ]))

        elements.append(tabla)
        doc.build(elements)

        # Subir el PDF generado al bucket de S3
        s3 = boto3.client('s3', 
        aws_access_key_id=os.environ.get('ACCESS_KEY'), 
        aws_secret_access_key=os.environ.get('SECRET_KEY'))
        bucket_name = os.environ.get('BUCKET_NAME')
        # Utilizar la fecha formateada en el nombre del archivo PDF
        pdf_filename = f'reporte_semanal_Humedad_suelo_{fecha_formateada}.pdf'
        pdf_data = response.content

        try:
            s3.upload_fileobj(io.BytesIO(pdf_data), bucket_name, pdf_filename)
        except Exception as e:
            # Manejar errores si algo sale mal durante la carga
            return Response({'error': 'Error al cargar el archivo PDF a S3'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Establecer la política de acceso para hacer el archivo público
        s3.put_object_acl(Bucket=bucket_name, Key=pdf_filename, ACL='public-read')

        # Obtener la URL del PDF recién generado
        url_reporte = f'https://{bucket_name}.s3.amazonaws.com/{pdf_filename}'

        # Devolver el enlace de descarga del PDF
        return Response({'url_reporte': url_reporte}, status=status.HTTP_200_OK)