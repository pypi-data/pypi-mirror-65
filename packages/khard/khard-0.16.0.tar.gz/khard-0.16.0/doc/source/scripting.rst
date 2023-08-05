Scripting and integration with other programs
=============================================

Khard can be used together with email or SIP clients or a synchronisation
program like `vdirsyncer`_.

.. _vdirsyncer: https://github.com/pimutils/vdirsyncer/

mutt
----

Khard may be used as an external address book for the email client mutt. To
accomplish that, add the following to your mutt config file (mostly
``~/.mutt/muttrc``):

.. code-block:: muttrc

  set query_command= "khard email --parsable %s"
  bind editor <Tab> complete-query
  bind editor ^T    complete

Then you can complete email addresses by pressing the Tab-key in mutt's new
mail dialog. If your address books contain hundreds or even thousands of
contacts and the query process is very slow, you may try the
``--search-in-source-files`` option to speed up the search:

.. code-block:: muttrc

  set query_command= "khard email --parsable --search-in-source-files %s"

If you want to complete multi-word search strings like "john smith" then you
may try out the following instead:

.. code-block:: muttrc

  set query_command = "echo %s | xargs khard email --parsable --"

To add email addresses to khard's address book, you may also add the following
lines to your muttrc file:

.. code-block:: muttrc

  macro index,pager A \
    "<pipe-message>khard add-email<return>" \
    "add the sender email address to khard"

Then navigate to an email message in mutt's index view and press "A" to start
the address import dialog.


Alot
----

Add the following lines to your alot config file:

.. code-block:: ini

  [accounts]
      [[youraccount]]
          [[[abook]]]
              type = shellcommand
              command = khard email --parsable
              regexp = '^(?P<email>[^@]+@[^\t]+)\t+(?P<name>[^\t]+)'
              ignorecase = True



Twinkle
-------

For those who also use the SIP client twinkle to take phone calls, khard can be used to query
incoming numbers. The plugin tries to find the incoming caller id and speaks it together with the
phone's ring tone. But it is more or less a proof of concept - feel free to extend.

The plugin needs the following programs:

.. code-block:: shell

  sudo aptitude install ffmpeg espeak sox mpc

sox and ffmpeg are used to cut and convert the new ring tone and espeak speaks
the caller id.  mpc is a client for the music player daemon (mpd). It's
required to stop music during an incoming call. Skip the last, if you don't use
mpd. Don't forget to set the "stop_music"-parameter in the ``config.py`` file
to ``False``, too.

After the installation, copy the scripts and sounds folders to your twinkle
config folder:

.. code-block:: shell

  cp -R misc/twinkle/* ~/.twinkle/

Next convert the sound samples to wave:

.. code-block:: shell

  ffmpeg -i incoming_call.ogg incoming_call.wav
  ffmpeg -i outgoing_call.ogg outgoing_call.wav
  ffmpeg -i ringtone_segment.ogg ringtone_segment.wav

Then edit your twinkle config file (mostly ``~/.twinkle/twinkle.cfg``) like
this:

.. code-block:: ini

  # RING TONES
  # We need a default ring tone. Otherwise the phone would not ring at all, if
  # something with the custom ring tone creation goes wrong.
  ringtone_file=/home/USERNAME/.twinkle/sounds/incoming_call.wav
  ringback_file=/home/USERNAME/.twinkle/sounds/outgoing_call.wav

  # SCRIPTS
  script_incoming_call=/home/USERNAME/.twinkle/scripts/incoming_call.py
  script_in_call_answered=
  script_in_call_failed=/home/USERNAME/.twinkle/scripts/incoming_call_failed.py
  script_outgoing_call=
  script_out_call_answered=
  script_out_call_failed=
  script_local_release=/home/USERNAME/.twinkle/scripts/incoming_call_ended.py
  script_remote_release=/home/USERNAME/.twinkle/scripts/incoming_call_ended.py


Zsh
---

The file ``misc/zsh/_khard`` contains a khard cli completion function for the
zsh and ``misc/zsh/_email-khard`` completes email addresses.

Install by copying to a directory where zsh searches for completion functions
(the ``$fpath`` array). If you, for example, put all completion functions into
the folder ``~/.zsh/completions`` you must add the following to your zsh main
config file:

.. code-block:: zsh

  fpath=( $HOME/.zsh/completions $fpath )
  autoload -U compinit
  compinit


sdiff
-----

Use the wrapper script ``misc/sdiff/sdiff_khard_wrapper.sh`` if you want to use
sdiff as your contact merging tool. Just make the script executable and set it
as your merge editor in khard's config file:

.. code-block:: ini

  merge_editor = /path/to/sdiff_khard_wrapper.sh

.. include:: davcontroller.rst
