import pytest
from django.test import Client


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def post_list():
    posts = [
        {
            "title": "It's All About The Priorities",
            "text": "Life is full of wonderful surprises and so \
                is work. As a developer, it's easy to burn out \
                when you have more tasks than you can handle. \
                In this article, I will share a simple tip \
                that can make the process smooth while \
                achieving the goals. Picture this, it's July 16, 1969.\
                Apollo 11 is landing on the Moon with a 0.043 MHz\
                processor. At the time of landing, the instructions\
                for the CPU far exceeded than what it could manage.\
                Luckily, it didn't crash, made it to the moon safely.",
            "tags": ["Motivation"],
        },
        {
            "title": "Side Projects for Professional Growth",
            "text": "Side hustles are great, so great that they can \
                speak for you at job interviews, give you hands-on experience \
                on new tools and programming languages, bring you extra income \
                and define you professionally in every possible way. \
                For this article, I have selected my top four side projects and \
                their impact on my professional growth.",
            "tags": ["IT"],
        },
        {
            "title": "Book Review: Living by The Code",
            "text": "I strongly recommend reading the book yourself. \
                In case you can't, here are my top three takeaways from the book.\
                People who prefer working in the morning than a late-night tend \
                to achieve more in the long run and stay motivated.\
                Communication is a critical part of the developer's job. \
                Always communicate and ask for help.\
                Choosing one thing at a time. For those who's been struggling \
                to choose one area of development, choose one. After mastering \
                one, you can move on to others.",
            "tags": ["Book"],
        },
        {
            "title": "Nega Kitoblardan O'rganish Foydaliroq",
            "text": "Sizda hech imtihonga qattiq tayyorlanib, \
                imtihondan so'ng hamma narsa esingizdan chiqib ketganmi? \
                Ingliz tilida bu haqida zo'r maqol bor: <<Easy come - Easy go>>. \
                Oson kelgan bilim oson ketadi.\
                Bilimlarni eslab qolish uchun, kerakli payt qo'llay olish uchun \
                uni tushunish kerak. Maqsad qisqa vaqt ichida ko'p narsani o'rganish, \
                yodlash emas, balki o'rgangan bilimni miya qabul qilishga, tushunishga \
                imkon yaratish, ustida ko'proq o'ylashdir.",
            "tags": ["Book"],
        },
    ]
    return posts
