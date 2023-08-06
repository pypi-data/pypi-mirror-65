## Adaptive Youtube iFrames

This sphinx extension adds the directive `youtube`, to embed Youtube Videos into Sphinx Docs, using the Video-ID. (Observable from the Link)
This package contains code parts of https://github.com/shomah4a/sphinxcontrib.youtube and https://github.com/sphinx-contrib/youtube.

This extension embeds Youtube videos in a responsive way. With no options given it will fill 100% width and will display videos with an aspect ratio of 16:9.

`..  youtube:: sfjlksdfks`

With :width:, :height: and :aspect: specific dimensions or an aspect ratio for the video can be **optionally** specified. Examples:

```
..  youtube:: sfjlksdfks
    :width: 640px
    :height: 480px

..  youtube:: sfjlksdfks
    :aspect: 4:3

..  youtube:: sfjlksdfks
    :width: 80%
```

### Stay responsive:

Never destroy your UI with overflowing videos. Even if you set a large fix size for your Video, if the screen size reduces on mobile, the video will switch to width=100%.

Install:

```shell
pip3 install sphinxcontrib-adaptive_youtube
```