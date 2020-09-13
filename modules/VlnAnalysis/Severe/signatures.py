#!/usr/bin/env python3
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This file is a part of TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework
#Added some of my own :)

searchinfo = ""
info = ""
properties = {}

services = {

        'AWS/S3'          : {'code':'[300-499]','error':r'The specified bucket does not exit'},
        'BitBucket'       : {'code':'[300-499]','error':r'Repository not found'},
        'CloudFront'      : {'code':'[300-499]','error':r'ERROR\: The request could not be satisfied'},
        'Github'          : {'code':'[300-499]','error':r'There isn\'t a Github Pages site here\.'},
        'Shopify'         : {'code':'[300-499]','error':r'Sorry\, this shop is currently unavailable\.'},
        'Desk'            : {'code':'[300-499]','error':r'Sorry\, We Couldn\'t Find That Page'},
        'Fastly'          : {'code':'[300-499]','error':r'Fastly error\: unknown domain\:'},
        'FeedPress'       : {'code':'[300-499]','error':r'The feed has not been found\.'},
        'Ghost'           : {'code':'[300-499]','error':r'The thing you were looking for is no longer here\, or never was'},
        'Heroku'          : {'code':'[300-499]','error':r'no-such-app.html|<title>no such app</title>|herokucdn.com/error-pages/no-such-app.html'},
        'Pantheon'        : {'code':'[300-499]','error':r'The gods are wise, but do not know of the site which you seek.'},
        'Tumbler'         : {'code':'[300-499]','error':r'Whatever you were looking for doesn\'t currently exist at this address.'},
        'Wordpress'       : {'code':'[300-499]','error':r'Do you want to register'},
        'Desk'            : {'code':'[300-499]','error':r'Sorry, We Couldn\'t Find That Page'},
        'ZenDesk'         : {'code':'[300-499]','error':r'Help Center Closed'},
        'TeamWork'        : {'code':'[300-499]','error':r'Oops - We didn\'t find your site.'},
        'Helpjuice'       : {'code':'[300-499]','error':r'We could not find what you\'re looking for.'},
        'Helpscout'       : {'code':'[300-499]','error':r'No settings were found for this company:'},
        'S3Bucket'        : {'code':'[300-499]','error':r'The specified bucket does not exist'},
        'Cargo'           : {'code':'[300-499]','error':r'<title>404 &mdash; File not found</title>'},
        'Zeus'            : {'code':'[300-499]','error':r'Phew, Nothing\'s here'},
        'StatuPage'       : {'code':'[300-499]','error':r'You are being <a href=\"https://www.statuspage.io\">redirected'},
        'Uservoice'       : {'code':'[300-499]','error':r'This UserVoice subdomain is currently available!'},
        'Surge'           : {'code':'[300-499]','error':r'project not found'},
        'Intercom'        : {'code':'[300-499]','error':r'This page is reserved for artistic dogs\.|Uh oh\. That page doesn\'t exist</h1>'},
        'Webflow'         : {'code':'[300-499]','error':r'<p class=\"description\">The page you are looking for doesn\'t exist or has been moved.</p>'},
        'Kajabi'          : {'code':'[300-499]','error':r'<h1>The page you were looking for doesn\'t exist.</h1>'},
        'Thinkific'       : {'code':'[300-499]','error':r'You may have mistyped the address or the page may have moved.'},
        'Tave'            : {'code':'[300-499]','error':r'<h1>Error 404: Page Not Found</h1>'},
        'Wishpond'        : {'code':'[300-499]','error':r'<h1>https://www.wishpond.com/404?campaign=true'},
        'Aftership'       : {'code':'[300-499]','error':r'Oops.</h2><p class=\"text-muted text-tight\">The page you\'re looking for doesn\'t exist.'},
        'Aha'             : {'code':'[300-499]','error':r'There is no portal here \.\.\. sending you back to Aha!'},
        'Tictail'         : {'code':'[300-499]','error':r'to target URL: <a href=\"https://tictail.com|Start selling on Tictail.'},
        'Brightcove'      : {'code':'[300-499]','error':r'<p class=\"bc-gallery-error-code\">Error Code: 404</p>'},
        'Bigcartel'       : {'code':'[300-499]','error':r'<h1>Oops! We couldn&#8217;t find that page.</h1>'},
        'ActiveCampaign'  : {'code':'[300-499]','error':r'alt=\"LIGHTTPD - fly light.\"'},
        'Campaignmonitor' : {'code':'[300-499]','error':r'Double check the URL or <a href=\"mailto:help@createsend.com'},
        'Acquia'          : {'code':'[300-499]','error':r'The site you are looking for could not be found.|If you are an Acquia Cloud customer and expect to see your site at this address'},
        'Proposify'       : {'code':'[300-499]','error':r'If you need immediate assistance, please contact <a href=\"mailto:support@proposify.biz'},
        'Simplebooklet'   : {'code':'[300-499]','error':r'We can\'t find this <a href=\"https://simplebooklet.com'},
        'GetResponse'     : {'code':'[300-499]','error':r'With GetResponse Landing Pages, lead generation has never been easier'},
        'Vend'            : {'code':'[300-499]','error':r'Looks like you\'ve traveled too far into cyberspace.'},
        'Jetbrains'       : {'code':'[300-499]','error':r'is not a registered InCloud YouTrack.'},
        'Unbounce'        : {'code':'[300-499]','error':r'The requested URL / was not found on this server|The requested URL was not found on this server'},
        'Tictail'         : {'code':'[300-499]','error':r'Building a brand of your own\?|to target URL: \<a href\=\\\"https://tictail.com|Start selling on Tictail.'},
        'Smartling'       : {'code':'[300-499]','error':r'Domain is not configured'},
        'Pingdom'         : {'code':'[300-499]','error':r'pingdom'},
        'Tilda'           : {'code':'[300-499]','error':r'Domain has been assigned'},
        'Surveygizmo'     : {'code':'[300-499]','error':r'data-html-name'},
        'Mashery'         : {'code':'[300-499]','error':r'Unrecognized domain <strong>'},
}
