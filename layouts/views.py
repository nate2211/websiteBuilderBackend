from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from layouts.models import Layout, LayoutText, LayoutComponent, LayoutSetting, LayoutHeader, LayoutBody, LayoutFooter
from layouts.serializers import LayoutSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from .models import Layout
from .serializers import LayoutSerializer
from rest_framework import viewsets


@api_view(['POST'])
def create_layout(request):
    data = request.data
    source = data.get('source')

    # Create the layout
    layout = Layout.objects.create(title=source['title'])

    # Process components for each section
    for section_name in ('header', 'body', 'footer'):
        section_data = data.get(section_name)
        if section_data and section_data.get('component') is not None:
            # For simplicity, assuming component, images, texts, settings are all direct under section_data
            component_data = section_data['component']
            images_ids = [image['image_id'] for image in section_data.get('images', [])]
            texts = section_data.get('texts', [])
            settings = section_data.get('settings')

            # Create LayoutComponent
            component = LayoutComponent.objects.create(component=component_data)
            component.images.set(images_ids)
            component.save()

            # Create LayoutText instances
            for text_data in texts:
                LayoutText.objects.create(component=component, text=text_data['text'])

            # Create LayoutSetting instance if settings are provided
            if settings:
                LayoutSetting.objects.create(component=component, setting=settings)

            # Associate the component with the specific layout section
            if section_name == 'header':
                layout_header = LayoutHeader.objects.create(layout=layout)
                layout_header.components.add(component)
            elif section_name == 'body':
                layout_body = LayoutBody.objects.create(layout=layout)
                layout_body.components.add(component)
            elif section_name == 'footer':
                layout_footer = LayoutFooter.objects.create(layout=layout)
                layout_footer.components.add(component)

    return Response({"success": "Layout created successfully."}, status=status.HTTP_201_CREATED)