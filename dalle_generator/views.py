from django.shortcuts import render
import openai

def generate_image(request):
    api_key = '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'
    prompt = request.GET.get('prompt', 'Generate an image')
    size = request.GET.get('size', '512x512')
    num_images = 4

    openai.api_key = api_key

    try:
        response = openai.Image.create(
            prompt=prompt,
            n=num_images,
            size=size
        )

        images = []
        for image_data in response['data']:
            image_url = image_data['url']
            images.append(image_url)

        return render(request, 'dalle_generator/generate_image.html', {'images': images})

    except Exception as e:
        error_message = str(e)
        return render(request, 'dalle_generator/error.html', {'error_message': error_message})
