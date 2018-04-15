from django.shortcuts import render_to_response
from ceasar_cipher.forms import InputForm
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse


def encrypt(plaintext, key):
    L2I = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", range(26)))
    I2L = dict(zip(range(26), "ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
    encrypted_text = ''

    for c in plaintext.upper():
        if c.isalpha():
            encrypted_text += I2L[(L2I[c] + key) % 26]
        else:
            encrypted_text += c
    return encrypted_text


def decrypt(encrypted_text, key):
    L2I = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", range(26)))
    I2L = dict(zip(range(26), "ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
    decrypted_text = ''

    for c in encrypted_text.upper():
        if c.isalpha():
            decrypted_text += I2L[(L2I[c] - key) % 26]
        else:
            decrypted_text += c
    return decrypted_text


def frequency_analysis(text):
    normalized_text = text.upper()

    analysis_2 = {
        "analysis": [
            {"letter": "A", "frequency": 0}, {"letter": "B", "frequency": 0}, {"letter": "C", "frequency": 0},
            {"letter": "D", "frequency": 0}, {"letter": "E", "frequency": 0}, {"letter": "F", "frequency": 0},
            {"letter": "G", "frequency": 0}, {"letter": "H", "frequency": 0}, {"letter": "I", "frequency": 0},
            {"letter": "J", "frequency": 0}, {"letter": "K", "frequency": 0}, {"letter": "L", "frequency": 0},
            {"letter": "M", "frequency": 0}, {"letter": "N", "frequency": 0}, {"letter": "O", "frequency": 0},
            {"letter": "P", "frequency": 0}, {"letter": "Q", "frequency": 0}, {"letter": "R", "frequency": 0},
            {"letter": "S", "frequency": 0}, {"letter": "T", "frequency": 0}, {"letter": "U", "frequency": 0},
            {"letter": "V", "frequency": 0}, {"letter": "W", "frequency": 0}, {"letter": "X", "frequency": 0},
            {"letter": "Y", "frequency": 0}, {"letter": "Z", "frequency": 0}
        ]
    }

    for letter in normalized_text:
        if letter.isalpha():
            for j in range(0, 26):
                if analysis_2['analysis'][j]['letter'] == letter:
                    analysis_2['analysis'][j]['frequency'] += 1
                    j += 1

    return analysis_2


def try_keys(frequency_analysis_results):

    # key prediction based on frequency analysis

    approximate_keys = []
    i = 1
    for k, v in frequency_analysis_results.items():
        if v == max(frequency_analysis_results.values()):
            approximate_keys.append(abs(5 - i))           # 5 is index of letter 'E' - the most frequent letter
        i += 1
    return approximate_keys


def index(request):
    if request.method == 'POST':
        received_data = request.POST
        print('----OK----')

        data = {}

        if received_data.get('action') == 'encode':
            encrypted = encrypt(received_data.get('plaintext'), int(received_data.get('key')))
            data['text'] = encrypted
            fa = frequency_analysis(received_data.get('plaintext'))
            data['frequency_analysis'] = fa
            data['try_keys'] = try_keys(fa)
            return JsonResponse(data)

        if received_data.get('action') == 'decode':
            decrypted = decrypt(received_data.get('plaintext'), int(received_data.get('key')))
            data['text'] = decrypted
            return JsonResponse(data)

        if received_data.get('action') == 'f_a':
            data['frequency_analysis'] = frequency_analysis(received_data.get('plaintext'))
            return JsonResponse(data)

    return render(request, 'index.html')
