"""
sentry_wechat.models
~~~~~~~~~~~~~~~~~~~~~
:copyright: (c) 2020 by cxt, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from __future__ import absolute_import

import time
import json
import requests
import logging
import six
import sentry
from datetime import datetime
from pytz import timezone

from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from sentry.exceptions import PluginError
from sentry.plugins.bases import notify
from sentry.http import is_valid_url, safe_urlopen
from sentry.utils.safe import safe_execute

from sentry.utils.http import absolute_uri
from django.core.urlresolvers import reverse


def validate_urls(value, **kwargs):
    output = []
    for url in value.split('\n'):
        url = url.strip()
        if not url:
            continue
        if not url.startswith(('http://', 'https://')):
            raise PluginError('Not a valid URL.')
        if not is_valid_url(url):
            raise PluginError('Not a valid URL.')
        output.append(url)
    return '\n'.join(output)


class WechatForm(notify.NotificationConfigurationForm):
    urls = forms.CharField(
        label=_('Wechat robot url'),
        widget=forms.Textarea(attrs={
            'class': 'span6', 'placeholder': 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx-xxx-xxx-xxx-xxx'}),
        help_text=_('Enter wechat robot url.'))

    def clean_url(self):
        value = self.cleaned_data.get('url')
        return validate_urls(value)


class WechatPlugin(notify.NotificationPlugin):
    author = 'cxt'
    author_url = 'https://github.com/susujs/sentry-wechat-plugin'
    version = sentry.VERSION
    description = "Integrates wechat robot."
    resource_links = [
        ('Bug Tracker', 'https://github.com/susujs/sentry-wechat-plugin/issues'),
        ('Source', 'https://github.com/susujs/sentry-wechat-plugin'),
    ]

    slug = 'wechat'
    title = 'wechat'
    conf_title = title
    conf_key = 'wechat'

    project_conf_form = WechatForm
    timeout = getattr(settings, 'SENTRY_WECHAT_TIMEOUT', 3)
    logger = logging.getLogger('sentry.plugins.wechat')

    def is_configured(self, project, **kwargs):
        return bool(self.get_option('urls', project))

    def get_config(self, project, **kwargs):
        return [{
            'name': 'urls',
            'label': 'wechat robot url',
            'type': 'textarea',
            'help': 'Enter wechat robot url.',
            'placeholder': 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx-xxx-xxx-xxx-xxx',
            'validators': [validate_urls],
            'required': False
        }]

    def get_webhook_urls(self, project):
        url = self.get_option('urls', project)
        if not url:
            return ''
        return url

    def send_webhook(self, url, payload):
        return safe_urlopen(
            url=url,
            json=payload,
            timeout=self.timeout,
            verify_ssl=False,
        )

    def get_group_url(self, group):
        '''
        return absolute_uri(reverse('sentry-group', args=[
            group.organization.slug,
            group.project.slug,
            group.id,
        ]))
        '''
        return absolute_uri(group.get_absolute_url())

    def notify_users(self, group, event, *args, **kwargs):
        url = self.get_webhook_urls(group.project)
        project = event.project
        host = self.get_option("host", project) or ''
        safe = self.get_option("safe", project)
        data = {
            "msgtype": "text",
            'safe': '1' if safe else '0',
            "text": {
                    "content": '[标题] {}\n[时间] {}\n[{}] {}\n[href]({})'.format(
                        "Sentry {} 项目告警".format(project.slug),
                        datetime.now(timezone('Asia/Shanghai')
                                     ).strftime("%Y-%m-%d %H:%M:%S"),
                        event.get_tag('level').capitalize(
                        ), event.message.encode('utf8'),
                        "{}{}events/{}/".format(host,
                                                group.get_absolute_url())
                    )
            }
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
