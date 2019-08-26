import os
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify

from clubs.models import Club, Tag
from clubs.utils import clean


class Command(BaseCommand):
    help = 'Imports existing groups from Groups Online @ Penn.'
    START_URL = 'https://upenn-community.symplicity.com/index.php?s=student_group'

    def handle(self, *args, **kwargs):
        self.count = 1
        self.club_count = 0
        self.session = requests.Session()
        self.agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)' + \
                     ' Chrome/40.0.2214.85 Safari/537.36'
        self.session.headers = {
            'User-Agent': self.agent
        }
        self.process_url(self.START_URL)
        self.stdout.write('Imported {} clubs!'.format(self.club_count))

    def process_url(self, url):
        self.stdout.write('Processing Page {}'.format(self.count))
        self.count += 1
        resp = self.session.get(url)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.content, 'html.parser')
        grps = soup.select('.grpl .grpl-grp')
        for grp in grps:
            name = grp.select_one('h3 a').text.strip()
            image_url = urljoin(url, grp.select_one('img')['src']).strip()
            if image_url.endswith('/group_img.png'):
                image_url = None
            group_tag = grp.select_one('.grpl-type')
            if group_tag is not None:
                group_type = group_tag.text.strip()
            else:
                group_type = None
            description = grp.select_one('.grpl-purpose').text.replace('\r\n', '\n').strip()
            if description == 'This group has not written a purpose':
                description = ''
            else:
                description = clean(description)
            contact_tag = grp.select_one('.grpl-contact')
            if contact_tag is not None:
                contact_email = contact_tag.text.strip()
            else:
                contact_email = None

            if group_type is not None:
                tag = Tag.objects.get_or_create(name=group_type)[0]
            else:
                tag = None
            if Club.objects.filter(name=name).exists():
                club = Club.objects.get(name__iexact=name)
                flag = False
            else:
                cid = slugify(name)
                club, flag = Club.objects.get_or_create(id=cid)

            # only overwrite blank fields
            if not club.name:
                club.name = name
            if not club.description:
                club.description = description
            if not club.image and image_url:
                resp = requests.get(image_url, allow_redirects=True)
                resp.raise_for_status()
                club.image.save(os.path.basename(image_url), ContentFile(resp.content))
            if not club.email:
                club.email = contact_email

            # mark newly created clubs as inactive (has no owner)
            if flag:
                club.active = False
            club.save()
            if tag is not None and not club.tags.count():
                club.tags.set([tag])
            self.club_count += 1
            self.stdout.write("{} '{}'".format('Created' if flag else 'Updated', name))

        next_tag = soup.find(text='Next >')
        if next_tag is not None:
            next_link = next_tag.find_parent('a')['href']
            next_url = url.split('?', 1)[0] + next_link
            self.process_url(next_url)