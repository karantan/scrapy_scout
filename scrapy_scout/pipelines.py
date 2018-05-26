# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from scrapy_scout import settings
from scrapy_scout.models import Priglasitev
from scrapy_scout.models import create_tables
from scrapy_scout.models import db_connect
from mako.template import Template
from sqlalchemy.orm import sessionmaker

import logging
import requests

logger = logging.getLogger()


def send_message():
    email_template = Template(filename='scrapy_scout/email.mako')
    resp = requests.post(
        'https://api.mailgun.net/v3/{}/messages'.format(
            settings.MAILGUN_DOMAIN),
        auth=('api', settings.MAILGUN_API_KEY),
        data={
            'from': 'varstvo-konkurence.si <mailgun@{}>'.format(
                settings.MAILGUN_DOMAIN),
            'to': [email.strip() for email in settings.RECEIVERS.split(',')],
            'subject': 'Nova priglasena koncentracija',
            'text': 'Nova priglasena koncentracija',
            'html': email_template.render(),
        })
    try:
        resp.raise_for_status()
    except Exception as e:
        logger.error(e)


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
                date=item['date'])
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
