"""
This module provides methods to deal with
simple form identification.
"""

from tg import flash, redirect, request

def post_login(self, came_from='/'):
    """
    Redirect the user to the initially requested page on successful
    authentication or redirect her back to the login page if login failed.
    
    """
    if not request.identity:
        login_counter = request.environ['repoze.who.logins'] + 1
        redirect(url('/login', came_from=came_from, __logins=login_counter))
    userid = request.identity['repoze.who.userid']
    flash(_('Welcome back, %s!') % userid)
    redirect(came_from)

def post_logout(self, came_from='/'):
    """
    Redirect the user to the initially requested page on logout and say
    goodbye as well.
    
    """
    flash(_('We hope to see you soon!'))
    redirect(came_from)
