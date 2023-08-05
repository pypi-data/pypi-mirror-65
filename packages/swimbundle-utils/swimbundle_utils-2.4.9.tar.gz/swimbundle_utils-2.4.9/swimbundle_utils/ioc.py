from __future__ import unicode_literals
import re
import ipaddress
import iocextract
from builtins import str


class IOCParser(object):
    
    @staticmethod
    def unravel(value, wrap_chars):
        to_return = []
        for i in range(0, len(wrap_chars)):
            wrapping_char = wrap_chars[i]
            re_str = r"\{start}([^<>\[\]\(\)]*)\{end}".format(start=wrapping_char[0], end=wrapping_char[1])
            match = re.compile(re_str)
            match = match.findall(value)
            if match:
                to_return.extend(match)
            else:
                continue

        to_return.append(value)
        return to_return

    def possible_entries(self, entry):
        # Text that might wrap an IOC, in format <start txt>, <end txt>
        # So for example "(10.20.32.123)" -> "10.20.32.123"

        wrapping_chars = [  # Will be recursed on, so only add static regex
            ("(", ")"),
            ("<", ">"),
            (";", ";"),
            ("[", "]"),
            ("-", "-"),
            ('"', '"')
        ]

        sub_entries = self.unravel(entry, wrapping_chars)

        wrapping_txts = [
            (";", ";"),
            ("href=\"", "\""),
            ("alt=\"", "\""),
            ("<", ">,"),
        ]

        poss = []
        poss.extend(sub_entries)
        poss.append(entry)

        sub_strings = re.split("[<>]", entry)
        poss.extend(sub_strings)

        for start_txt, end_txt in wrapping_txts:
            starts_w = entry.startswith(start_txt)
            ends_w = entry.endswith(end_txt)

            if starts_w:
                poss.append(entry[len(start_txt):])

            if ends_w:
                poss.append(entry[:-len(end_txt)])

            if starts_w and ends_w:
                poss.insert(0, entry[len(start_txt):-len(end_txt)])  # Insert to beginning because of stripping

        return poss

    def parse_iocs(self, text, defang=False,  whitelist_regex=''):

        ioc_typer = IOCTyper()

        split_text = re.split(r"(\n| )", text)

        split_text = map(lambda x: x.strip("\r\t\n "), split_text)
        split_text = filter(lambda x: len(x) > 2, split_text)  # Strip out single chars

        entries = []

        for entry in split_text:
            # Each entry might not be split correctly, try some combinations
            for pos in self.possible_entries(entry):
                typ = ioc_typer.type_ioc(pos)

                if typ != "unknown":
                    entries.append((pos, typ))

        # iocextract can find iocs that have been defanged.  They are refanged and added to the correct type.
        iocs = set(iocextract.extract_iocs(text, refang=True))
        for ioc in iocs:
            typ = ioc_typer.type_ioc(ioc)
            entries.append((ioc, typ))
            for pos in self.possible_entries(ioc):
                typ = ioc_typer.type_ioc(pos)
                if typ != "unknown":
                    entries.append((pos, typ))

        result = IOCTyper.build_empty_ioc_dict()

        for entry, typ in entries:
            result[typ].append(entry)

        # Append domains from URLs to the domains result
        cleaned_urls = [re.sub("https?(://)?", "", u) for u in result["url"]]  # Strip schema
        cleaned_urls = [re.sub("[/?].*", "", u) for u in cleaned_urls]  # Strip excess /'s

        for cleaned_url in cleaned_urls:
            if ioc_typer.type_ioc(cleaned_url) == "domain":
                result["domain"].append(cleaned_url)

        # Add second level domains to domains (ie www.google.com -> google.com)
        sld_list = map(lambda x: x.group(), filter(lambda x: x, [re.search("\w+\.\w+$", dom) for dom in result["domain"]]))
        result["domain"].extend(sld_list)

        # Remove duplicates
        for k, v in result.items():
            result[k] = list(set(v))

        # Clear results based on whitelist
        if whitelist_regex:
            for ioc_typ in IOCTyper.IOC_TYPES:
                ioc_list = []
                for ioc in result[ioc_typ]:
                    if re.findall(whitelist_regex, ioc):
                        pass  # Found match, don't add to list
                    else:
                        ioc_list.append(ioc)
                result[ioc_typ] = ioc_list
        if defang:
            result = self.defang_results(result)
        return result

    @staticmethod
    def defang_results(results):
        defangable = ['domain', 'ipv4_private', 'ipv4_public', 'url']
        new_results = {}
        for key, value in results.items():
            if key in defangable:
                new_value = []
                for ioc in value:
                    new_value.append(iocextract.defang(ioc))
                new_results[key] = new_value
        results.update(new_results)
        return results

class IOCTyper(object):
    # Order of this list determnines the detection order, DO NOT CHANGE
    # Add new types to the top of this list
    IOC_TYPES = [
        'ssdeep',
        'sha256',
        'sha1',
        'md5',
        'email',
        'ipv4_public',
        'ipv4_private',
        'ipv6_public',
        'ipv6_private',
        'filename',
        'domain',
        'url',
        'unknown'
    ]

    COMMON_FILETYPES = ['3dm', '3ds', '3g2', '3gp', '7z', 'accdb', 'ai', 'aif', 'apk', 'app', 'asf', 'asp',
                        'aspx', 'avi', 'b', 'bak', 'bat', 'bin', 'bmp', 'c', 'cab', 'cbr', 'cer', 'cfg',
                        'cfm', 'cgi', 'class', 'cpl', 'cpp', 'crdownload', 'crx', 'cs', 'csr', 'css',
                        'csv', 'cue', 'cur', 'dat', 'db', 'dbf', 'dcr', 'dds', 'deb', 'dem', 'deskthemepack',
                        'dll', 'dmg', 'dmp', 'doc', 'docm', 'docx', 'download', 'drv', 'dtd', 'dwg', 'dxf',
                        'eps', 'exe', 'fla', 'flv', 'fnt', 'fon', 'gadget', 'gam', 'ged', 'gif', 'gpx', 'gz',
                        'h', 'hqx', 'htm', 'html', 'icns', 'ico', 'ics', 'iff', 'indd', 'ini', 'iso', 'jar',
                        'java', 'jpeg', 'jpg', 'js', 'json', 'jsp', 'key', 'keychain', 'kml', 'kmz', 'lnk',
                        'log', 'lua', 'm', 'm3u', 'm4a', 'm4v', 'max', 'mdb', 'mdf', 'mid', 'mim', 'mov',
                        'mp3', 'mp4', 'mpa', 'mpeg', 'mpg', 'msg', 'msi', 'nes', 'obj', 'odt', 'otf',
                        'pages', 'part', 'pct', 'pdb', 'pdf', 'php', 'pkg', 'pl', 'plugin', 'png', 'pps',
                        'ppt', 'pptx', 'prf', 'ps', 'psd', 'pspimage', 'py', 'rar', 'rm', 'rom', 'rpm',
                        'rss', 'rtf', 'sav', 'sdf', 'sh', 'sitx', 'sln', 'sql', 'srt', 'svg', 'swf', 'swift',
                        'sys', 'tar', 'tax2016', 'tax2017', 'tex', 'tga', 'thm', 'tif', 'tiff', 'tmp',
                        'toast', 'torrent', 'ttf', 'txt', 'uue', 'vb', 'vcd', 'vcf', 'vcxproj', 'vob', 'wav',
                        'wma', 'wmv', 'wpd', 'wps', 'wsf', 'xcodeproj', 'xhtml', 'xlr', 'xls', 'xlsx',
                        'xlsm', 'xml', 'yuv', 'zip', 'zipx', 'webm', 'flac', 'numbers']

    COMMON_TLDS = ['aaa', 'aarp', 'abarth', 'abb', 'abbott', 'abbvie', 'abc', 'able', 'abogado', 'abudhabi', 'ac',
                   'academy', 'accenture', 'accountant', 'accountants', 'aco', 'active', 'actor', 'ad', 'adac', 'ads',
                   'adult', 'ae', 'aeg', 'aero', 'aetna', 'af', 'afamilycompany', 'afl', 'africa', 'ag', 'agakhan',
                   'agency', 'ai', 'aig', 'aigo', 'airbus', 'airforce', 'airtel', 'akdn', 'al', 'alfaromeo', 'alibaba',
                   'alipay', 'allfinanz', 'allstate', 'ally', 'alsace', 'alstom', 'alwaysdata', 'am', 'americanexpress',
                   'americanfamily', 'amex', 'amfam', 'amica', 'amsterdam', 'analytics', 'android', 'anquan', 'anz',
                   'ao', 'aol', 'apartments', 'app', 'apple', 'aq', 'aquarelle', 'ar', 'arab', 'aramco', 'archi',
                   'army',
                   'arpa', 'art', 'arte', 'as', 'asda', 'asia', 'associates', 'at', 'athleta', 'attorney', 'au',
                   'auction', 'audi', 'audible', 'audio', 'auspost', 'author', 'auto', 'autos', 'avianca', 'aw', 'aws',
                   'ax', 'axa', 'az', 'azure', 'ba', 'baby', 'backplane', 'baidu', 'banamex', 'bananarepublic', 'band',
                   'bank', 'bar', 'barcelona', 'barclaycard', 'barclays', 'barefoot', 'bargains', 'baseball',
                   'basketball', 'bauhaus', 'bayern', 'bb', 'bbc', 'bbt', 'bbva', 'bcg', 'bcn', 'bd', 'be', 'beats',
                   'beauty', 'beer', 'bentley', 'berlin', 'best', 'bestbuy', 'bet', 'bf', 'bg', 'bh', 'bharti', 'bi',
                   'bible', 'bid', 'bike', 'bing', 'bingo', 'bio', 'biz', 'bj', 'black', 'blackfriday', 'blanco',
                   'blockbuster', 'blog', 'bloomberg', 'blue', 'bm', 'bms', 'bmw', 'bn', 'bnl', 'bnpparibas', 'bo',
                   'boats', 'boehringer', 'bofa', 'bom', 'bond', 'boo', 'book', 'booking', 'bosch', 'bostik', 'boston',
                   'bot', 'boutique', 'box', 'bplaced', 'br', 'bradesco', 'bridgestone', 'broadway', 'broker',
                   'brother',
                   'brussels', 'bs', 'bt', 'budapest', 'bugatti', 'build', 'builders', 'business', 'buy', 'buzz', 'bv',
                   'bw', 'by', 'bz', 'bzh', 'ca', 'cab', 'cafe', 'cal', 'call', 'callidomus', 'calvinklein', 'cam',
                   'camera', 'camp', 'cancerresearch', 'canon', 'capetown', 'capital', 'capitalone', 'car', 'caravan',
                   'cards', 'care', 'career', 'careers', 'cars', 'cartier', 'casa', 'case', 'caseih', 'cash', 'casino',
                   'cat', 'catering', 'catholic', 'cba', 'cbn', 'cbre', 'cbs', 'cc', 'cd', 'ceb', 'center', 'ceo',
                   'cern', 'cf', 'cfa', 'cfd', 'cg', 'ch', 'chanel', 'channel', 'charity', 'chase', 'chat', 'cheap',
                   'chintai', 'christmas', 'chrome', 'chrysler', 'church', 'ci', 'cipriani', 'circle', 'cisco',
                   'citadel', 'citi', 'citic', 'city', 'cityeats', 'ck', 'cl', 'claims', 'cleaning', 'click', 'clinic',
                   'clinique', 'clothing', 'cloud', 'club', 'clubmed', 'cm', 'cn', 'co', 'coach', 'codes', 'coffee',
                   'college', 'cologne', 'com', 'comcast', 'commbank', 'community', 'company', 'compare', 'computer',
                   'comsec', 'condos', 'construction', 'consulting', 'contact', 'contractors', 'cooking',
                   'cookingchannel', 'cool', 'coop', 'corsica', 'country', 'coupon', 'coupons', 'courses', 'cr',
                   'credit', 'creditcard', 'creditunion', 'cricket', 'crown', 'crs', 'cruise', 'cruises', 'csc', 'cu',
                   'cuisinella', 'cv', 'cw', 'cx', 'cy', 'cymru', 'cyou', 'cz', 'dabur', 'dad', 'dance', 'data', 'date',
                   'dating', 'datsun', 'day', 'dclk', 'dds', 'de', 'deal', 'dealer', 'deals', 'degree', 'delivery',
                   'dell', 'deloitte', 'delta', 'democrat', 'dental', 'dentist', 'desi', 'design', 'dev', 'dhl',
                   'diamonds', 'diet', 'digital', 'direct', 'directory', 'discount', 'discover', 'dish', 'diy', 'dj',
                   'dk', 'dm', 'dnp', 'do', 'docs', 'doctor', 'dodge', 'dog', 'doha', 'domains', 'dot', 'download',
                   'drive', 'dtv', 'dubai', 'duck', 'dunlop', 'duns', 'dupont', 'durban', 'dvag', 'dvr', 'dz', 'earth',
                   'eat', 'ec', 'eco', 'edeka', 'edu', 'education', 'ee', 'eg', 'email', 'emerck', 'energy', 'engineer',
                   'engineering', 'enterprises', 'epost', 'epson', 'equipment', 'er', 'ericsson', 'erni', 'es', 'esq',
                   'estate', 'esurance', 'et', 'etisalat', 'eu', 'eurovision', 'eus', 'events', 'everbank', 'exchange',
                   'expert', 'exposed', 'express', 'extraspace', 'fage', 'fail', 'fairwinds', 'faith', 'family', 'fan',
                   'fans', 'farm', 'farmers', 'fashion', 'fast', 'fedex', 'feedback', 'ferrari', 'ferrero', 'fi',
                   'fiat',
                   'fidelity', 'fido', 'film', 'final', 'finance', 'financial', 'fire', 'firestone', 'firmdale', 'fish',
                   'fishing', 'fit', 'fitness', 'fj', 'fk', 'flickr', 'flights', 'flir', 'florist', 'flowers', 'fly',
                   'fm', 'fo', 'foo', 'food', 'foodnetwork', 'football', 'ford', 'forex', 'forsale', 'forum',
                   'foundation', 'fox', 'fr', 'free', 'fresenius', 'frl', 'frogans', 'frontdoor', 'frontier', 'ftr',
                   'fujitsu', 'fujixerox', 'fun', 'fund', 'furniture', 'futbol', 'fyi', 'ga', 'gal', 'gallery', 'gallo',
                   'gallup', 'game', 'games', 'gap', 'garden', 'gb', 'gbiz', 'gd', 'gdn', 'ge', 'gea', 'gent',
                   'genting',
                   'george', 'gf', 'gg', 'ggee', 'gh', 'gi', 'gift', 'gifts', 'gives', 'giving', 'gl', 'glade', 'glass',
                   'gle', 'global', 'globo', 'gm', 'gmail', 'gmbh', 'gmo', 'gmx', 'gn', 'godaddy', 'gold', 'goldpoint',
                   'golf', 'goo', 'goodhands', 'goodyear', 'goog', 'google', 'gop', 'got', 'gov', 'gp', 'gq', 'gr',
                   'grainger', 'graphics', 'gratis', 'green', 'gripe', 'grocery', 'group', 'gs', 'gt', 'gu', 'guardian',
                   'gucci', 'guge', 'guide', 'guitars', 'guru', 'gw', 'gy', 'hair', 'hamburg', 'hangout', 'haus', 'hbo',
                   'hdfc', 'hdfcbank', 'health', 'healthcare', 'help', 'helsinki', 'here', 'hermes', 'hgtv', 'hiphop',
                   'hisamitsu', 'hitachi', 'hiv', 'hk', 'hkt', 'hm', 'hn', 'hockey', 'holdings', 'holiday', 'homedepot',
                   'homegoods', 'homes', 'homesense', 'honda', 'honeywell', 'horse', 'hospital', 'host', 'hosting',
                   'hot', 'hoteles', 'hotels', 'hotmail', 'house', 'how', 'hr', 'hsbc', 'ht', 'hu', 'hughes', 'hyatt',
                   'hyundai', 'ibm', 'icbc', 'ice', 'icu', 'id', 'ie', 'ieee', 'ifm', 'ikano', 'il', 'im', 'imamat',
                   'imdb', 'immo', 'immobilien', 'in', 'inc', 'industries', 'infiniti', 'info', 'ing', 'ink',
                   'institute', 'insurance', 'insure', 'int', 'intel', 'international', 'intuit', 'investments', 'io',
                   'ipiranga', 'iq', 'ir', 'irish', 'is', 'iselect', 'ismaili', 'ist', 'istanbul', 'it', 'itau', 'itv',
                   'iveco', 'iwc', 'jaguar', 'java', 'jcb', 'jcp', 'je', 'jeep', 'jetzt', 'jewelry', 'jio', 'jlc',
                   'jll',
                   'jm', 'jmp', 'jnj', 'jo', 'jobs', 'joburg', 'jot', 'joy', 'jp', 'jpmorgan', 'jprs', 'juegos',
                   'juniper', 'kaufen', 'kddi', 'ke', 'kerryhotels', 'kerrylogistics', 'kerryproperties', 'kfh', 'kg',
                   'kh', 'ki', 'kia', 'kim', 'kinder', 'kindle', 'kitchen', 'kiwi', 'km', 'kn', 'koeln', 'komatsu',
                   'kosher', 'kp', 'kpmg', 'kpn', 'kr', 'krd', 'kred', 'kuokgroup', 'kw', 'ky', 'kyoto', 'kz', 'la',
                   'lacaixa', 'ladbrokes', 'lamborghini', 'lamer', 'lancaster', 'lancia', 'lancome', 'land',
                   'landrover',
                   'lanxess', 'lasalle', 'lat', 'latino', 'latrobe', 'law', 'lawyer', 'lb', 'lc', 'lds', 'lease',
                   'leclerc', 'lefrak', 'legal', 'lego', 'lexus', 'lgbt', 'li', 'liaison', 'lidl', 'life',
                   'lifeinsurance', 'lifestyle', 'lighting', 'like', 'lilly', 'limited', 'limo', 'lincoln', 'linde',
                   'link', 'lipsy', 'live', 'living', 'lixil', 'lk', 'llc', 'loan', 'loans', 'locker', 'locus', 'loft',
                   'lol', 'london', 'lotte', 'lotto', 'love', 'lpl', 'lplfinancial', 'lr', 'ls', 'lt', 'ltd', 'ltda',
                   'lu', 'lundbeck', 'lupin', 'luxe', 'luxury', 'lv', 'ly', 'ma', 'macys', 'madrid', 'maif', 'maison',
                   'makeup', 'man', 'management', 'mango', 'map', 'market', 'marketing', 'markets', 'marriott',
                   'marshalls', 'maserati', 'mattel', 'mba', 'mc', 'mckinsey', 'md', 'me', 'med', 'media', 'meet',
                   'melbourne', 'meme', 'memorial', 'men', 'menu', 'meo', 'merckmsd', 'metlife', 'mg', 'mh', 'miami',
                   'microsoft', 'mil', 'mini', 'mint', 'mit', 'mitsubishi', 'mk', 'ml', 'mlb', 'mls', 'mm', 'mma', 'mn',
                   'mo', 'mobi', 'mobile', 'mobily', 'moda', 'moe', 'moi', 'mom', 'monash', 'money', 'monster', 'mopar',
                   'mormon', 'mortgage', 'moscow', 'moto', 'motorcycles', 'mov', 'movie', 'movistar', 'mp', 'mq', 'mr',
                   'ms', 'msd', 'mt', 'mtn', 'mtr', 'mu', 'museum', 'mutual', 'mv', 'mw', 'mx', 'my', 'mz', 'na', 'nab',
                   'nadex', 'nagoya', 'name', 'nationwide', 'natura', 'navy', 'nba', 'nc', 'ne', 'nec', 'net',
                   'netbank',
                   'netflix', 'network', 'neustar', 'new', 'newholland', 'news', 'next', 'nextdirect', 'nexus', 'nf',
                   'nfl', 'ng', 'ngo', 'ngrok', 'nhk', 'ni', 'nico', 'nike', 'nikon', 'ninja', 'nissan', 'nissay', 'nl',
                   'no', 'nokia', 'northwesternmutual', 'norton', 'now', 'nowruz', 'nowtv', 'np', 'nr', 'nra', 'nrw',
                   'ntt', 'nu', 'nyc', 'nz', 'obi', 'observer', 'off', 'office', 'okinawa', 'olayan', 'olayangroup',
                   'oldnavy', 'ollo', 'om', 'omega', 'one', 'ong', 'onion', 'onl', 'online', 'onyourside', 'ooo',
                   'open',
                   'oracle', 'orange', 'org', 'organic', 'origins', 'osaka', 'otsuka', 'ott', 'ovh', 'pa', 'page',
                   'panasonic', 'panerai', 'paris', 'pars', 'partners', 'parts', 'party', 'passagens', 'pay', 'pccw',
                   'pe', 'pet', 'pf', 'pfizer', 'pg', 'ph', 'pharmacy', 'phd', 'philips', 'phone', 'photo',
                   'photography', 'photos', 'physio', 'piaget', 'pics', 'pictet', 'pictures', 'pid', 'pin', 'ping',
                   'pink', 'pioneer', 'pizza', 'pk', 'place', 'play', 'playstation', 'plumbing', 'plus', 'pm', 'pn',
                   'pnc', 'pohl', 'poker', 'politie', 'porn', 'post', 'pr', 'pramerica', 'praxi', 'press', 'prime',
                   'pro', 'prod', 'productions', 'prof', 'progressive', 'promo', 'properties', 'property', 'protection',
                   'pru', 'prudential', 'ps', 'pt', 'pub', 'pw', 'pwc', 'py', 'qa', 'qpon', 'quebec', 'quest', 'qvc',
                   'racing', 'radio', 'raid', 're', 'read', 'realestate', 'realtor', 'realty', 'recipes', 'red',
                   'redstone', 'redumbrella', 'rehab', 'reise', 'reisen', 'reit', 'reliance', 'ren', 'rent', 'rentals',
                   'repair', 'report', 'republican', 'rest', 'restaurant', 'review', 'reviews', 'rexroth', 'rich',
                   'richardli', 'ricoh', 'rightathome', 'ril', 'rio', 'rip', 'rmit', 'ro', 'rocher', 'rocks', 'rodeo',
                   'rogers', 'room', 'rs', 'rsvp', 'ru', 'rugby', 'ruhr', 'run', 'rw', 'rwe', 'ryukyu', 'sa',
                   'saarland',
                   'safe', 'safety', 'sakura', 'sale', 'salon', 'samsclub', 'samsung', 'sandvik', 'sandvikcoromant',
                   'sanofi', 'sap', 'sapo', 'sarl', 'sas', 'save', 'saxo', 'sb', 'sbi', 'sbs', 'sc', 'sca', 'scb',
                   'schaeffler', 'schmidt', 'scholarships', 'school', 'schule', 'schwarz', 'science', 'scjohnson',
                   'scor', 'scot', 'sd', 'se', 'search', 'seat', 'secure', 'security', 'seek', 'select', 'sener',
                   'services', 'ses', 'seven', 'sew', 'sex', 'sexy', 'sfr', 'sg', 'sh', 'shangrila', 'sharp', 'shaw',
                   'shell', 'shia', 'shiksha', 'shoes', 'shop', 'shopping', 'shouji', 'show', 'showtime', 'shriram',
                   'si', 'silk', 'sina', 'singles', 'site', 'sj', 'sk', 'ski', 'skin', 'sky', 'skype', 'sl', 'sling',
                   'sm', 'smart', 'smile', 'sn', 'sncf', 'so', 'soccer', 'social', 'softbank', 'software', 'sohu',
                   'solar', 'solutions', 'song', 'sony', 'soy', 'space', 'spiegel', 'sport', 'spot', 'spreadbetting',
                   'sr', 'srl', 'srt', 'st', 'stada', 'staples', 'star', 'starhub', 'statebank', 'statefarm',
                   'staticland', 'statoil', 'stc', 'stcgroup', 'stockholm', 'storage', 'store', 'stream', 'studio',
                   'study', 'style', 'su', 'sucks', 'supplies', 'supply', 'support', 'surf', 'surgery', 'suzuki', 'sv',
                   'swatch', 'swiftcover', 'swiss', 'sx', 'sy', 'sydney', 'symantec', 'systems', 'sz', 'tab', 'taipei',
                   'talk', 'taobao', 'target', 'tatamotors', 'tatar', 'tattoo', 'tax', 'taxi', 'tc', 'tci', 'td', 'tdk',
                   'team', 'tech', 'technology', 'telecity', 'telefonica', 'temasek', 'tennis', 'teva', 'tf', 'tg',
                   'th',
                   'thd', 'theater', 'theatre', 'tiaa', 'tickets', 'tienda', 'tiffany', 'tips', 'tires', 'tirol', 'tj',
                   'tjmaxx', 'tjx', 'tk', 'tkmaxx', 'tl', 'tm', 'tmall', 'tn', 'to', 'today', 'tokyo', 'tools', 'top',
                   'toray', 'toshiba', 'total', 'tours', 'town', 'toyota', 'toys', 'trade', 'trading', 'training',
                   'travel', 'travelchannel', 'travelers', 'travelersinsurance', 'trust', 'trv', 'tt', 'tube', 'tui',
                   'tunes', 'tushu', 'tv', 'tvs', 'tw', 'tz', 'ua', 'ubank', 'ubs', 'uconnect', 'ug', 'uk', 'unicom',
                   'university', 'uno', 'uol', 'ups', 'us', 'uy', 'uz', 'va', 'vacations', 'vana', 'vanguard', 'vc',
                   've', 'vegas', 'ventures', 'verisign', 'versicherung', 'vet', 'vg', 'vi', 'viajes', 'video', 'vig',
                   'viking', 'villas', 'vin', 'vip', 'virgin', 'visa', 'vision', 'vista', 'vistaprint', 'viva', 'vivo',
                   'vlaanderen', 'vn', 'vodka', 'volkswagen', 'volvo', 'vote', 'voting', 'voto', 'voyage', 'vu',
                   'vuelos', 'wales', 'walmart', 'walter', 'wang', 'wanggou', 'warman', 'watch', 'watches', 'weather',
                   'weatherchannel', 'webcam', 'weber', 'website', 'wed', 'wedding', 'weibo', 'weir', 'wf', 'whoswho',
                   'wien', 'wiki', 'williamhill', 'win', 'windows', 'wine', 'winners', 'wme', 'wolterskluwer',
                   'woodside', 'work', 'works', 'world', 'wow', 'ws', 'wtc', 'wtf', 'xbox', 'xerox', 'xfinity',
                   'xihuan',
                   'xin', 'xperia', 'xxx', 'xyz', 'yachts', 'yahoo', 'yamaxun', 'yandex', 'ye', 'yodobashi', 'yoga',
                   'yokohama', 'you', 'youtube', 'yt', 'yun', 'za', 'zappos', 'zara', 'zero', 'zip', 'zippo', 'zm',
                   'zone', 'zuerich', 'zw']

    # Country Code TLDs
    CC_TLDS = ['uk', 'eu', 'su', 'ac', 'ax', 'af', 'al', 'dz', 'as', 'ad', 'ao', 'ai', 'aq', 'ag', 'ar', 'am',
               'aw', 'au', 'at', 'az', 'bs', 'bh', 'bd', 'bb', 'by', 'be', 'bz', 'bj', 'bm', 'bt', 'bo', 'ba',
               'bw', 'bv', 'br', 'io', 'bn', 'bg', 'bf', 'bi', 'kh', 'cm', 'ca', 'cv', 'ky', 'cf', 'td', 'cl',
               'cn', 'cx', 'cc', 'co', 'km', 'cd', 'cg', 'ck', 'cr', 'ci', 'hr', 'cu', 'cy', 'cz', 'dk', 'dj',
               'dm', 'do', 'ec', 'eg', 'sv', 'gq', 'er', 'ee', 'et', 'fk', 'fo', 'fj', 'fi', 'fr', 'gf', 'pf',
               'tf', 'ga', 'gm', 'ge', 'de', 'gh', 'gi', 'gr', 'gl', 'gd', 'gp', 'gu', 'gt', 'gn', 'gw', 'gy',
               'ht', 'hm', 'hn', 'hk', 'hu', 'is', 'in', 'id', 'ir', 'iq', 'ie', 'il', 'it', 'jm', 'jp', 'jo',
               'kz', 'ke', 'ki', 'kp', 'kr', 'kw', 'kg', 'la', 'lv', 'lb', 'ls', 'lr', 'ly', 'li', 'lt', 'lu',
               'mo', 'mk', 'mg', 'mw', 'my', 'mv', 'ml', 'mt', 'mh', 'mq', 'mr', 'mu', 'yt', 'mx', 'fm', 'md',
               'mc', 'mn', 'ms', 'ma', 'mz', 'mm', 'na', 'nr', 'np', 'nl', 'an', 'nc', 'nz', 'ni', 'ne', 'ng',
               'nu', 'nf', 'mp', 'no', 'om', 'pk', 'pw', 'ps', 'pa', 'pg', 'py', 'pe', 'ph', 'pn', 'pl', 'pt',
               'pr', 'qa', 're', 'ro', 'ru', 'rw', 'sh', 'kn', 'lc', 'pm', 'vc', 'ws', 'sm', 'st', 'sa', 'sn',
               'cs', 'sc', 'sl', 'sg', 'sk', 'si', 'sb', 'so', 'za', 'gs', 'es', 'lk', 'sd', 'sr', 'sj', 'sz',
               'se', 'ch', 'sy', 'tw', 'tj', 'tz', 'th', 'tl', 'tg', 'tk', 'to', 'tt', 'tn', 'tr', 'tm', 'tc',
               'tv', 'ug', 'ua', 'ae', 'gb', 'us', 'um', 'uy', 'uz', 'vu', 'va', 've', 'vn', 'vg', 'vi', 'wf',
               'eh', 'ye', 'zm', 'zw']

    URL_REGEX_COMPILED = re.compile(r"""^                                    #beginning of line	
(?P<proto>https?:\/\/)               #protocol                http://	
(	
(?P<domain>(([\u007E-\uFFFFFF\w-]+[.])+[\u007E-\uFFFFFF\w-]{2,}))	
|	
(?P<ipv4>(?:(?:\b|\.)(?:2(?:5[0-5]|[0-4]\d)|1?\d?\d)){4})	
|	
(\[?	
(?P<ipv6>(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])))	
\]?)	
)	
(?P<port>:\d{1,5})?	
\/?                                    #domain                    www.google.co.uk	
(?P<directory>(?<=\/)([{}%|~\/!?A-Za-z0-9_.-]+)(?=\/))?                    #directory    /var/www/html/apps	
\/?                                    #final directory slash    /	
(?P<filename>([^?<>"]+))?                #filename                index.php	
                                    #query marker            ?	
(?P<query>\?[^\s"<>]*)?                        #query text                cmd=login_submit&id=1#cnx=2.123	
$                                    #end of line""", re.VERBOSE | re.UNICODE)

    FILE_REGEX = r'^(?!.*[\\/:*"<>|])[\w !@#$%^&*()+=\[\]{}\'"-]+(\.[\w -]+)?$'

    def __init__(self):
        self.ioc_patterns = {
            'ipv4_public': IPv4PublicIOC(),
            'ipv4_private': IPv4PrivateIOC(),
            'ipv6_public': IPv6PublicIOC(),
            'ipv6_private': IPv6PrivateIOC(),

            'url': URLIOC(self),
            'email': RegexIOC(r'^[\w%+.-]+@[A-Za-z0-9.-]+\.[a-z]{2,}$'),
            'md5': RegexIOC(r'^[a-fA-F0-9]{32}$'),
            'sha1': RegexIOC(r'^[a-fA-F0-9]{40}$'),
            'sha256': RegexIOC(r'^[a-fA-F0-9]{64}$'),
            'ssdeep': RegexIOC(r'^([1-9]\d*)(?!:\d\d($|:)):([\w+0-9\/]+):([\w+0-9\/]+)$')
        }

        self.ioc_patterns.update({
            'filename': FilenameIOC(IOCTyper.FILE_REGEX),
            'domain': DomainIOC(),
            'unknown': AnyIOC()
        })

        self.tld_patterns = {
            'validSLD': re.compile(r'^[a-z0-9-]+$', re.IGNORECASE),
            'validTLD': re.compile(r'^[a-z]{2,64}$'),
            'tld': re.compile(r'^\.[a-z]{2,}$')
        }

    @staticmethod
    def build_empty_ioc_dict():
        iocs = {}
        for ioc in IOCTyper.IOC_TYPES:
            iocs[ioc] = []

        return iocs

    def is_ip(self, value):
        versions = ["4", "6"]
        p_levels = ["public", "private"]
        for v in versions:
            for p_level in p_levels:
                if self.ioc_patterns["ipv{}_{}".format(v, p_level)].run(value):
                    return True
        return False

    def split_domain(self, domain):
        if self.is_ip(domain):
            return {
                'tld': None,
                'sld': None,
                'subs': None,
                'ip': domain,
            }

        domain_parts = domain.split(".")
        domain_tld = domain_parts.pop()  # Top level domain

        if len(domain_parts) > 0:
            domain_sld = domain_parts.pop()  # Second level domain
        else:
            domain_sld = None

        if domain_tld in IOCTyper.CC_TLDS:  # for country code TLDs like .uk, .eu, etc.
            if domain_sld:
                if domain_sld == "co" or domain_sld in IOCTyper.COMMON_TLDS:  # find "com" "co", etc.
                    domain_tld = domain_sld + "." + domain_tld
                    if len(domain_parts) > 0:
                        domain_sld = domain_parts.pop()
                    else:
                        domain_sld = None

        if len(domain_parts) > 0:
            subs = ".".join(domain_parts)  # Sub-domains
        else:
            subs = None

        return {
            'tld': domain_tld,
            'sld': domain_sld,
            'subs': subs,
            'ip': None
        }

    def type_ioc(self, ioc):
        for pat_name in IOCTyper.IOC_TYPES:
            if self.ioc_patterns[pat_name].run(ioc):
                return pat_name


class IOCObj(object):
    def run(self, value):
        raise NotImplementedError


class AnyIOC(IOCObj):  # Always returns true
    def run(self, value):
        return True


class RegexIOC(object):
    def __init__(self, regex, re_flags=0):
        """
        :param regex: Regex String to match a value against
        """
        self.regex = re.compile(regex, re_flags)

    def run(self, value):
        return bool(self.regex.search(value))


class URLIOC(IOCObj):
    def __init__(self, typer):
        self.typer = typer

    def run(self, value):
        match = IOCTyper.URL_REGEX_COMPILED.search(value)
        if match and len(match.group()) == len(value):
            return True
        return False


class FilenameIOC(IOCObj):
    def __init__(self, regex):
        self.regex = re.compile(regex)

    def run(self, value):
        match = self.regex.search(value)
        if match and self.is_filename(match.group()):
            return True
        return False

    @staticmethod
    def is_filename(fn):

        extension = ".".join(fn.split(".")[-1:])
        if extension == fn:
            return False

        if extension in IOCTyper.COMMON_FILETYPES:
            return True
        else:
            return False


class DomainIOC(IOCObj):
    NUMERIC_NOT_A_DOMAIN = numeric_only = re.compile(r'^([0-9]+\.)+[0-9]+$')
    GENERAL_DOMAIN = re.compile(r'(([\u007E-\uFFFFFF\w-]+[.])+[\u007E-\uFFFFFF\w-]{2,})', re.UNICODE)

    def run(self, value):
        match = self.GENERAL_DOMAIN.search(value)
        if match and len(match.group()) == len(value):
            bad_match = self.NUMERIC_NOT_A_DOMAIN.search(value)
            if not bad_match or len(bad_match.group()) != len(value):
                return True

        return False


class IPIOC(IOCObj):
    def privacy_valid(self, value):
        # Return true if the value is private otherwise false if public
        ipaddr = ipaddress.ip_address(str(value))
        if ipaddr.is_private == self.is_private():
            return True
        else:
            return False

    def is_private(self):
        # Return true if the ioc typer is for private ips only else false for public
        raise NotImplementedError

    def ip_ver(self):
        # Return ip version, either 4 or 6
        raise NotImplementedError

    def ioc_name(self):
        # Returns one of ipv6_private, ipv6_public, ipv4_public, ipv4_private
        name = "ipv{}".format(self.ip_ver())
        name += "_{}".format("private" if self.is_private() else "public")
        return name

    def get_regex(self):
        raise NotImplementedError

    def __init__(self):
        self.regex = re.compile(self.get_regex())

    def run(self, value):
        match = self.regex.search(value)
        result = False

        try:
            ipaddress.ip_address(str(value))  # Try parsing IP
        except ValueError:
            return False

        if match:
            result = True and self.privacy_valid(value)

        return result


class IPv4PublicIOC(IPIOC):
    def get_regex(self):
        return r'^(?:(?:\b|\.)(?:2(?:5[0-5]|[0-4]\d)|1?\d?\d)){4}$'

    # Keeping regex in case it becomes useful
    #         # Class A
    #         r'^10\.(2([0-5]{2})|2[0-9]{1}|1?\d?\d)\.(2([0-5]{2})|2[0-9]{1}|1?\d?\d)\.(2([0-5]{2})|2[0-9]{1}|1?\d?\d)$',
    #         # Class B
    #         r'^172\.(3([01])|1[6-9]|2\d)\.(2([0-5]{2})|2[0-9]{1}|1?\d?\d)\.(2([0-5]{2})|2[0-9]{1}|1?\d?\d)$',
    #         # Class C
    #         r'^192\.168\.(2([0-5]{2})|2[0-9]{1}|1?\d?\d)\.(2([0-5]{2})|2[0-9]{1}|1?\d?\d)$',
    #     ]

    def is_private(self):
        return False

    def ip_ver(self):
        return "4"


class IPv4PrivateIOC(IPv4PublicIOC):
    def is_private(self):
        return True


class IPv6PublicIOC(IPIOC):
    def get_regex(self):
        return r'^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))$'

    def is_private(self):
        return False

    def ip_ver(self):
        return "6"


class IPv6PrivateIOC(IPv6PublicIOC):
    def is_private(self):
        return True
