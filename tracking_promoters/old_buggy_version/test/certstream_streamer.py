from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def find_similar_url(slugs,url):
    for i in slugs:
        if i in url:
            score=similar(i,url)
            if score>0.2:
                print(f"{url} similar to {i}")

import logging
import sys
import datetime
import certstream
import ssl

def print_callback(message, context):

    slugs=['ens.domains', 'dopeapeclub.xyz', 'godhatesnftees.com', 'www.boredapeyachtclub.com', None, 'www.larvalabs.comcryptopunks', 'otherside.xyz', 'fsm.cool', 'www.larvalabs.comautoglyphs', 'nouns.wtf', 'moonrunners.io', 'moonbirds.xyz', 'pssssd.xyz', 'mekarhinos.io', 'xoxonft.io', 'www.azuki.com', 'goblintown.wtf', 'memeland.com', 'doodles.app', 'www.rtfkt.com', 'doodles.app', None, 'bapes.xyz', 'thegoda.io', 'www.renga.app', 'www.sandbox.game', 'emblem.pro', 'boredapeyachtclub.com#kennel-club', 'doadz.io', 'collective.proof.xyz', None, 'impostors.gg', 'onchainmonkey.com', 'app.rarible.comcollection0x211838a8a587b02de8a02a6edafbfd7277c317d4', 'imaginaryones.com', 'cryptoskulls.com', 'miladymaker.net', 'gossamer.world', 'www.illuminatinft.com', 'doodles.appdooplicator', 'bapes.xyz', 'solo.tosupernormal', 'lonelypop.com', 'cyberkongz.com', 'boki.art', 'www.v1punks.io', 'tasties.io', 'www.tenset.ioen', 'www.gala.games', 'mypethooligan.com', 'www.los-muertos.io', None, 'metaherouniverse.com', 'nftsensei.xyz', 'fluf.world', None, 'decentraland.org', 'twitter.comExplodedDegen', None, 'doodles.app', 'www.chimpers.xyz', 'toysterz.xyz', 'www.pjnen.com', 'spaceriders.xyz', 'killabears.com', 'treeverse.net', 'murakamiflowers.kaikaikiki.com', 'alphadogsnft.io', 'coolcatsnft.com', 'www.bullsandapesproject.com', 'immortalcat.io', 'osf.artrektguy', 'www.parallel.life', 'www.moonrabbits.art', 'www.treeverse.net', 'punkscomic.com', 'officialcryptocity.com', 'www.adidas.cominto_the_metaverse', 'zenacademy.io', 'mnlth.rtfkt.com', 'series2.veefriends.com', 'docs.nftworlds.com', 'rebels.art', 'www.rtfkt.com', 'flowerfam.earth', 'quirkies.io', 'rebels.art', 'notokay.art', 'fluf.world', 'aifa.football', 'metaherouniverse.com', 'www.moonbunnynft.xyz', 'pieceofshit.wtf', 'regular.world', 'themetakongz.com', 'lazylionsnft.com', 'quirkies.ioquirklings', 'onchainmonkey.com', 'drops.unxd.comdgfamily']
    logging.debug("Message -> {}".format(message))

    if message['message_type'] == "heartbeat":
        return

    if message['message_type'] == "certificate_update":
        all_domains = message['data']['leaf_cert']['all_domains']

        if len(all_domains) == 0:
            domain = "NULL"
        else:
            domain = all_domains[0]

        
        url_data=message['data']['leaf_cert']['all_domains'][1:]
        for i in range(10):
            try:
                url=message['data']['leaf_cert']['all_domains'][1:][i]
                find_similar_url(slugs,url)
                
            except:
                break
        # sys.stdout.write(u"[{}] {} (SAN: {})\n".format(datetime.datetime.now().strftime('%m/%d/%y %H:%M:%S'), domain, ", ".join(message['data']['leaf_cert']['all_domains'][1:])))
        # sys.stdout.flush()


logging.basicConfig(format='[%(levelname)s:%(name)s] %(asctime)s - %(message)s', level=logging.INFO)

certstream.listen_for_events(print_callback, url='wss://certstream.calidog.io/',sslopt={"cert_reqs":ssl.CERT_NONE})