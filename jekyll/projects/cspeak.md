---
layout: project-page
title: CSpeak
---

CSpeak is a very simple speech synthesis library written in C. It consists of only ~140 lines of code, half of which is a formant lookup table. The table of formants and the Daisy Bell demo are adapted from [Cantarino][4].

 - [Source code][1]

### Demo

The synthesiser singing [Daisy Bell][3] (visualisation provided by [sndpeek][2]):

{% assign youtube_video_id = "6nqzVnYm_SU" %}
{% include youtube-embed.html %}

Below is the original artificial rendition of the song by the IBM 7094:

{% assign youtube_video_id = "41U78QP8nBk" %}
{% include youtube-embed.html %}

 [1]: http://github.com/davidar/cspeak
 [2]: http://soundlab.cs.princeton.edu/software/sndpeek/
 [3]: http://en.wikipedia.org/wiki/Daisy_Bell
 [4]: http://code.google.com/p/tinkerit/wiki/Cantarino
