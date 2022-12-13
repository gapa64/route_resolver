IPv4_PATTERN = (r'(\b25[0-5]|\b2[0-4][0-9]|\b[01]?[0-9][0-9]?)'
                r'(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}')
IPv6_PATTERN = (r'(?!^(?:(?:.*(?:::.*::|:::).*)'
                r'|::|[0:]+[01]|.*[^:]:|[0-9a-fA-F](?:.*:.*){8}'
                r'[0-9a-fA-F]|(?:[0-9a-fA-F]:){1,6}'
                r'[0-9a-fA-F])$)^(?:(::|[0-9a-fA-F]{1,4}:{1,2})'
                r'([0-9a-fA-F]{1,4}:{1,2}){0,6}([0-9a-fA-F]{1,4}|::)?)$')
IPv4_PREFIX_LEN = r'(\d|[1-2][0-9]|3[0-2])\b'
IPv6_PREFIX_LEN = r'(\d|[1-9][0-9]|1([0-1][1-9]|2[1-8]))\b'
IPv4_PREFIX_PATTERN = rf'{IPv4_PATTERN}/{IPv4_PREFIX_LEN}'
IPv6_PREFIX_PATTERN = rf'{IPv6_PATTERN}/{IPv6_PREFIX_LEN}'
IPv4_WEB_PREFIX_PATTERN = rf'{IPv4_PATTERN}%2F{IPv4_PREFIX_LEN}'
IPv6_WEB_PREFIX_PATTERN = rf'{IPv6_PATTERN}%2F{IPv6_PREFIX_LEN}'

#/prefix/<prefix>/nh/<next-hop>/metric/<metric>/match/<classifier>
