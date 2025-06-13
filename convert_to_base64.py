import base64

def image_to_base64(image_path):
    with open(image_path, 'rb') as image_file:
        base64_string = base64.b64encode(image_file.read()).decode('utf-8')
    return base64_string

# Example usage
if __name__ == '__main__':
    base64_captcha = image_to_base64('captcha.jpg')
    print(base64_captcha)  # This prints the base64 string of the image
