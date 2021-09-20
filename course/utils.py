from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.template.loader import get_template, render_to_string
from django.utils.html import strip_tags
from summerschool import settings
from PIL import Image, ImageDraw, ImageFont
from summerschool import settings
import textwrap

import io

import os


class Email():

    def send_submission_email(self, request, submission):
        context = {
            'category': submission.task.category.title,
            'person': submission.account.first_name + " "+submission.account.last_name,
            'domain': get_current_site(request)
        }

        html_message = render_to_string(
            'emails/submission_email.html', context)
        plain_message = strip_tags(html_message)
        from_email = settings.EMAIL_HOST_USER
        organisers = submission.task.category.organiser_set.all().values_list('account__email',
                                                                              flat=True).distinct()

        send_mail('New Submission update | Summer School Portal', plain_message,
                  from_email, organisers, html_message=html_message)

    def send_admin_commented_email(self, submission):
        context = {
            'category': submission.task.category.title,
            'first_name': submission.account.first_name,
            'last_name': submission.account.last_name,
            'organisers': submission.task.category.organiser_set.all()
        }

        html_message = render_to_string(
            'emails/admin_commented_email.html', context)
        plain_message = strip_tags(html_message)
        from_email = settings.EMAIL_HOST_USER
        to = submission.account.email

        send_mail('Submission Checked by Mentor | ISTE Summer School', plain_message,
                  from_email, [to], html_message=html_message)


class Certficate():

    # def make_certificate(self, account, course, duration):

    #     img = Image.open(os.path.join(settings.BASE_DIR,
    #                      'course/certificate/certificate.jpeg'))

    #     d1 = ImageDraw.Draw(img)

    #     myFont = ImageFont.truetype(os.path.join(
    #         settings.BASE_DIR, 'course/certificate/font.ttf'), 35)

    #     d1.text((410, 390), f"{account.first_name} {account.last_name}", fill=(
    #         194, 151, 72), font=myFont)
    #     d1.text((64.1277, 434.4681), account.registration_number,
    #             fill=(194, 151, 72), font=myFont)
    #     d1.text((975.4681, 434.4681), str(duration),
    #             fill=(194, 151, 72), font=myFont)
    #     d1.text((130.2979, 475.3191), course,
    #             fill=(194, 151, 72), font=myFont)

    #     certificate = io.BytesIO()
    #     img.save(certificate, format="jpeg")

    #     return certificate

    def make_certificate(self, account, course, duration):
        image_text = f"This is to certifiy that {account.first_name} {account.last_name} bearing Registration Number {account.registration_number}, a student of MIT Manipal, has successfully completed {duration} weeks of the {course} course, during the Summer School 2021, organised by Indian Society for Technical Education, Students Chapter Manipal."
        course_words = course.split()

        STOP_WORDS = [account.first_name, account.last_name,
                      account.registration_number+",", str(duration)] + course_words

        img = Image.open(os.path.join(settings.BASE_DIR,
                         'course/certificate/certificate2.png'))

        d1 = ImageDraw.Draw(img)

        myFont = ImageFont.truetype(os.path.join(
            settings.BASE_DIR, 'course/certificate/font.ttf'), 30)

        margin = 68
        offset = 290
        for line in textwrap.wrap(image_text, width=70):
            words = line.split()

            margin = 68

            for word in words:
                d1.text((margin, offset), word+" ", font=myFont, fill=(
                    194, 151, 72) if word in STOP_WORDS else (0, 0, 0))

                margin += myFont.getsize(word+" ")[0]

            offset += myFont.getsize(line)[1]
        certificate = io.BytesIO()
        img.save(certificate, format="png")

        return certificate

    def make_error_file(self, message: str):
        img = Image.new(mode="RGB", size=(200, 200),
                        color=(153, 153, 255))
        d1 = ImageDraw.Draw(img)

        myFont = ImageFont.truetype(os.path.join(
            settings.BASE_DIR, 'course/certificate/font.ttf'), 10)

        d1.text((100, 100), message, fill=(
            194, 151, 72), font=myFont)
        certificate = io.BytesIO()

        img.save(certificate, format="jpeg")

        return certificate
