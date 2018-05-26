# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from mako.template import Template
from scrapy.exceptions import DropItem
from scrapy_scout import settings
from scrapy_scout.models import create_tables
from scrapy_scout.models import db_connect
from scrapy_scout.models import Priglasitev
from sendgrid.helpers.mail import Content
from sendgrid.helpers.mail import Email
from sendgrid.helpers.mail import Mail
from sqlalchemy.orm import sessionmaker

import logging
import os
import sendgrid

logger = logging.getLogger()


def send_message():
    email_template = Template(filename='scrapy_scout/email.mako')

    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email('app97716152@heroku.com')
    subject = 'Nova priglasena koncentracija'
    to_email = Email(settings.RECEIVERS)
    content = Content('text/plain', email_template.render())
    mail = Mail(from_email, subject, to_email, content)
    sg.client.mail.send.post(request_body=mail.get())


class ScrapyScoutPipeline(object):
    def __init__(self):
        """Initializes database connection and sessionmaker."""
        engine = db_connect()
        create_tables(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save priglasitev in the database.

        This method is called for every item pipeline component.
        """
        session = self.Session()

        if item['date']:
            priglasitev_exists = session.query(Priglasitev).filter_by(
                date=item['date'].date(), st_zadeve=item['st_zadeve'])
        else:
            raise DropItem('Missing date in %s' % item)

        if not priglasitev_exists.count():
            priglasitev = Priglasitev(**item)
            try:
                session.add(priglasitev)
                session.commit()
            except Exception as e:
                logger.error(e)
                session.rollback()
                raise
            finally:
                session.close()

            if hasattr(spider, 'mode') and spider.mode == 'production':
                send_message()

        return item
