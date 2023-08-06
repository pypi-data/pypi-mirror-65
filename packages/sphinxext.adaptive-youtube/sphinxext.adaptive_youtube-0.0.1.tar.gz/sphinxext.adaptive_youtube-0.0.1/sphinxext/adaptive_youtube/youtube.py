#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

import re
from docutils import nodes
from docutils.parsers.rst import directives, Directive
import urllib.parse as urlparse

def get_id(argument):
    if argument.startswith('http://') or argument.startswith('https://'):
        return urlparse.parse_qs(urlparse.urlparse(argument).query)['v'][0]
    return argument

def get_size(d, key):
    if key not in d:
        return None
    m = re.match("(\d+)(|%|px)$", d[key])
    if not m:
        raise ValueError("invalid size %r" % d[key])
    return int(m.group(1)), m.group(2) or "px"

def css(d):
    return "; ".join(sorted("%s: %s" % kv for kv in d.items()))

class youtube(nodes.General, nodes.Element): pass

def visit_youtube_node(self, node):
    aspect = node["aspect"]
    width = node["width"]
    height = node["height"]

    if aspect is None:
        aspect = 16, 9

    if width is None:
        if height is None:
            width = 100, "%"
            height = 100, "%"
        elif height[1] == "px":
            width = height[0] * aspect[0] / aspect[1], "px"
        else:
            raise ValueError("Specify the width in px if you specify the height in %.")
    else:
        if height is None:
            if width[1] == "px":
                height = width[0] * aspect[1] / aspect[0], "px"
            else:
                height = 100, "%"
        elif height is not None and height[1] == width[1]:
            aspect = width[0], height[0]
        elif width[1] == "px" and height[1] == "%":
            height = width[0]*height[0]/100, "px"
        else:
            raise ValueError("Specify the width in px if you use height in %.")
    
    absolute_wrapper_style = {
        "width": "100%",
        "height": "100%",
        "max-width": f"{width[0]}px" if width[1] == "px" else "100%",
        "max-height": f"{height[0]}px" if height[1] == "px" else "100%",
        "margin-bottom": "25px",
    }

    aspect_wrapper_style = {
        "position": "relative",
        "padding-bottom": f"{aspect[1]/aspect[0]*100}%",
        "padding-top": "0",
        "height": "0",
        "overflow": "hidden",
    }

    iframe_style = {
        "position": "absolute",
        "top": "0",
        "left": "0",
        "width": f"{width[0]}%" if width[1] == "%" else "100%",
        "height": "100%",
    }

    abs_wrap_attrs = {
        "CLASS": "absolute_wrapper",
        "style": css(absolute_wrapper_style),
    }

    aspect_wrap_attrs = {
        "CLASS": "aspect_wrapper",
        "style": css(aspect_wrapper_style),
    }

    iframe_attrs = {
        "src": "https://www.youtube.com/embed/%s" % node["id"],
        "style": css(iframe_style),
        "allowfullscreen": "true",
    }

    self.body.append(self.starttag(node, "div", **abs_wrap_attrs))
    self.body.append(self.starttag(node, "div", **aspect_wrap_attrs))
    self.body.append(self.starttag(node, "iframe", **iframe_attrs))
    self.body.append("</iframe></div></div>")

def depart_youtube_node(self, node):
    pass

def visit_youtube_node_latex(self,node):
    self.body.append(r'\begin{quote}\begin{center}\fbox{\url{https://youtu.be/%s}}\end{center}\end{quote}'%node['id'])


class YouTube(Directive):
    has_content = True
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "width": directives.unchanged,
        "height": directives.unchanged,
        "aspect": directives.unchanged,
    }

    def run(self):
        if "aspect" in self.options:
            aspect = self.options.get("aspect")
            m = re.match("(\d+):(\d+)", aspect)
            if m is None:
                raise ValueError("invalid aspect ratio %r" % aspect)
            aspect = tuple(int(x) for x in m.groups())
        else:
            aspect = None

        width = get_size(self.options, "width")
        height = get_size(self.options, "height")
        return [youtube(id=get_id(self.arguments[0]), aspect=aspect, width=width, height=height)]


def unsupported_visit_youtube(self, node):
    self.builder.warn('youtube: unsupported output format (node skipped)')
    raise nodes.SkipNode

_NODE_VISITORS = {
      'html': (visit_youtube_node, depart_youtube_node),
      'latex': (visit_youtube_node_latex, depart_youtube_node),
      'man': (unsupported_visit_youtube, None),
      'texinfo': (unsupported_visit_youtube, None),
      'text': (unsupported_visit_youtube, None)
}