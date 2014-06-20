# Copyright 2011, Google Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#     * Neither the name of Google Inc. nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import json
from Holodeck.holodeck import create_deck, classname_to_id
from Holodeck.effects import get_all_effects

# This creates the holodeck once, making it global for all
# future connections.
deck = create_deck() 
deck.daemon = True
deck.start()
print "Started holodeck thread"

def web_socket_do_extra_handshake(request):
    # This example handler accepts any request. See origin_check_wsh.py for how
    # to reject access from untrusted scripts based on origin value.
    pass  # Always accept.



def web_socket_transfer_data(request):
    global deck
    
    effect_list = get_all_effects()
    
    icon_meta = {}
    for (ename, eclass) in effect_list.items():
      meta = eclass.META

      if not meta.get('id'):
        meta['id'] = classname_to_id(ename)

      if not meta.get('img'):
        meta['img'] = meta['id']+".png"

      meta['active'] = deck.is_active(meta['id'])

      # Create this tab if not already made
      if not icon_meta.get(meta['tab'], None):
        icon_meta[meta['tab']] = {}

      icon_meta[meta['tab']][meta['id']] = meta 

    print "Sending meta:"
    for tab in icon_meta:
      print tab
      for icon in icon_meta[tab]:
        print "-", icon

    request.ws_stream.send_message(json.dumps(
      {"type": "init", "data": icon_meta}
    ), binary=False)

    while True:
        msg = request.ws_stream.receive_message()
        if msg is None:
            print "Client connection aborted"
            return

        msg = json.loads(msg)
        cmd = json.loads(msg['data'])

        result = deck.handle(cmd)
        print "Response:", result
        response = json.dumps({"type": "delta", "data": result})
        request.ws_stream.send_message(response, binary=False)

        deck.update()
