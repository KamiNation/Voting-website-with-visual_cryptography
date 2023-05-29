from django.shortcuts import render, redirect, reverse
from .email_backend import EmailBackend
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
from .forms import CustomUserForm
from .forms import PhotoForm
from . import forms
from django.template import RequestContext
from . import models
from voting.forms import VoterForm
from django.contrib.auth import login, logout
from captcha.image import ImageCaptcha
from django.db import models
import string
import random
import argparse
import random
from datetime import *
import sys
import smtplib
# import the corresponding modules
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from PIL import Image
import matplotlib.pyplot as plt
# Create your views here.


def account_login(request):
    if request.user.is_authenticated:
        if request.user.user_type == '1':
            return redirect(reverse("adminDashboard"))
        else:
            return redirect(reverse("voterDashboard"))

    context = {}
    if request.method == 'POST':
        user = EmailBackend.authenticate(request, username=request.POST.get(
            'email'), password=request.POST.get('password'))
        if user != None:
            login(request, user)
            if user.user_type == '1':
                return redirect(reverse("adminDashboard"))
            else:
                return redirect(reverse("voterDashboard"))
        else:
            messages.error(request, "Invalid details")
            return redirect("/")

    return render(request, "voting/login.html", context)


def account_register(request):
    userForm = CustomUserForm(request.POST or None)
    voterForm = VoterForm(request.POST or None)
    context = {
        'form1': userForm,
        'form2': voterForm
    }
    if request.method == 'POST':
        if userForm.is_valid() and voterForm.is_valid():
            user = userForm.save(commit=False)
            voter = voterForm.save(commit=False)
            voter.admin = user
            # Creating the recaptcha for the user
            captcha()
            # Saving the users data
            user.save()
            voter.save()
            messages.success(request, "Account created. You can login now!")
            return redirect(reverse('account_login'))
        else:
            messages.error(request, "Provided data failed validation")
            # return account_login(request)
    return render(request, "voting/reg.html", context)


def account_logout(request):
    user = request.user
    if user.is_authenticated:
        logout(request)
        messages.success(request, "Thank you for visiting us!")
    else:
        messages.error(
            request, "You need to be logged in to perform this action")

    return redirect(reverse("account_login"))


#VIews to handle image uploads
def members(request):
     if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('account_login')
        else:
            form = PhotoForm()
            return render(request, '/home/kami/Desktop/votebyvisual/vote/account/template/photo_upload.html', {'form': form})

#return render(request, "voting/photo_upload.html", context={'form': form})
            #return redirect('account_login')


#VisualCryptographySchemeCode from Captcha Generation to Captcha Splitting
#to Captcha mailing to user to Captcha Merging and finally Captcha Display.


# function to create recaptch
def captcha():
# Create an image instance of the given size
    image = ImageCaptcha(width = 280, height = 90)
# initializing size of string
    N = 7
# using random.choices()
# generating random strings
    res = ''.join(random.choices(string.ascii_uppercase +string.digits, k=N))
# print result
    print("The generated random string : " + str(res))
# Image captcha text
    captcha_text = res
# generate the image of the given text
    data = image.generate(captcha_text)
# write the image on the given file and save it
    filename1 = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    image.write(captcha_text, "/home/kami/Desktop/votebyvisual/vote/captcha/"+filename1 + '.png')
    two_of_two("/home/kami/Desktop/votebyvisual/vote/captcha/"+filename1+".png")



#VisualCryptographySchemeCode
# The MIT License (MIT)
# Copyright (c) 2016 Philipp Trommler
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT
# OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



def two_of_two(filename):
    """Generates a (2,2) visual cryptography scheme."""
    original = Image.open(filename)

    original = original.convert("1")
    o_pixels = original.load()

    first = Image.new("1", (original.size[0], original.size[1] * 2))
    f_pixels = first.load()

    second = Image.new("1", (original.size[0], original.size[1] * 2))
    s_pixels = second.load()

    for i in range(original.size[0]):
        for j in range(original.size[1]):
            if o_pixels[i,j] == 0:
                if random.randint(0, 1):
                    f_pixels[i,j * 2    ] = 1
                    f_pixels[i,j * 2 + 1] = 0
                    s_pixels[i,j * 2    ] = 0
                    s_pixels[i,j * 2 + 1] = 1
                else:
                    f_pixels[i,j * 2    ] = 0
                    f_pixels[i,j * 2 + 1] = 1
                    s_pixels[i,j * 2    ] = 1
                    s_pixels[i,j * 2 + 1] = 0
            else:
                if random.randint(0, 1):
                    f_pixels[i,j * 2    ] = 0
                    f_pixels[i,j * 2 + 1] = 1
                    s_pixels[i,j * 2    ] = 0
                    s_pixels[i,j * 2 + 1] = 1
                else:
                    f_pixels[i,j * 2    ] = 1
                    f_pixels[i,j * 2 + 1] = 0
                    s_pixels[i,j * 2    ] = 1
                    s_pixels[i,j * 2 + 1] = 0

    first.save(filename + "_img1.png")
    second.save(filename + "_img2.png")
    mergeCaptcha(filename + "_img1.png", filename + "_img2.png")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("IMAGE", help="The image to encrypt")
    args = parser.parse_args()

    two_of_two(args.IMAGE)

#Python code to mail a part of the share to user tested using mailtrap.io
    port = 2525
    smtp_server = "smtp.mailtrap.io"
    login = "1a2b3c4d5e6f7g" # paste your login generated by Mailtrap
    password = "1a2b3c4d5e6f7g" # paste your password generated by Mailtrap

    subject = "An example of boarding pass"
    sender_email = "mailtrap@example.com"
    receiver_email = "new@example.com"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Add body to email
    body = "This is an example of how you can send a boarding pass in attachment with Python"
    message.attach(MIMEText(body, "plain"))

    # Name of the split being sent to user
    filename = filename + "_img2.png"


    # Open PDF file in binary mode

    # We assume that the file is in the directory where you run your Python script from
    with open(filename, "rb") as attachment:
        # The content type "application/octet-stream" means that a MIME attachment is a binary file
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode to base64
    encoders.encode_base64(part)

    # Add header
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to your message and convert it to string
    message.attach(part)
    text = message.as_string()

    # send your email
    with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
        server.login("a40cc048b4b386", "7e676c786fa0dd")
        server.sendmail(sender_email, receiver_email, text)

    print('Sent')

#Python code to merge using bitwise xor operation
# Open images and store them in a list
def mergeCaptcha(file1, file2):
    share1 = Image.open(file1)
    share2 = Image.open(file2)


    output = Image.new("1", share1.size)
    output.paste(share1)
    output.paste(share2, mask=share2)

    output.save("/home/kami/Desktop/votebyvisual/vote/captcha/"+"output.png")
