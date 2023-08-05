"""
Created on 12/dic/2013

@author: Marco Pompili
"""

import logging

from django import template
from django.conf import settings as user_settings

from sorl.thumbnail import get_thumbnail, delete

from django_easy_instagram import settings
from django_easy_instagram.scraper import instagram_profile_obj

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

handler.setFormatter(formatter)
logger.addHandler(handler)

register = template.Library()


def get_profile_media(profile, page=0):
    """
    Parse a generated media object
    :param profile:
    :param page:
    :return:
    """
    try:
        edges = profile['entry_data']['ProfilePage'][page]['graphql']['user']['edge_owner_to_timeline_media']['edges']
        return [edge['node'] for edge in edges]
    except KeyError:
        logger.exception("path to profile media not found")


class InstagramUserRecentMediaNode(template.Node):
    """
    Template node for showing recent media from an user.
    """

    def __init__(self, var_name):
        self.var_name = var_name
        self.username = template.Variable(var_name)

    def render(self, context):
        try:
            profile = instagram_profile_obj(self.username.resolve(context))
        except template.base.VariableDoesNotExist:
            logger.warning(
                " variable name \"{}\" not found in context!"
                " Using a raw string as input is DEPRECATED."
                " Please use a template variable instead!".format(self.var_name)
            )

            profile = instagram_profile_obj(username=self.var_name)

        if profile:
            context['profile'] = profile
            context['recent_media'] = get_profile_media(profile)

        return ''


@register.tag
def instagram_user_recent_media(parser, token):
    """
    Tag for getting data about recent media of an user.
    :param parser:
    :param token:
    :return:
    """
    try:
        tagname, username = token.split_contents()

        return InstagramUserRecentMediaNode(username)
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires a single argument" % token.contents.split()[0]
        )


@register.filter(name='local_cache')
def local_cache(value, size="600x600"):
    im = get_thumbnail(value, size, crop='center', quality=settings.INSTAGRAM_QUALITY)
    return im.url
