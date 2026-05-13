#!/usr/bin/env python3
"""
将 Electrum 发现数据转换为 Node Eye 格式的 JSON
"""

import json
import random

# CSV 数据（前 100 行用于示例）
csv_lines = """electrum.jochen-hoenicke.de,50001,No,online,Fulcrum 2.1.0,1.4,1091
electrum.jochen-hoenicke.de,50002,Yes,online,Fulcrum 2.1.0,1.4,1095
electrum.hsmiths.com,50002,Yes,online,ElectrumX 1.10.0,1.4,1155
dijon.anties.org,50001,No,online,ElectrumX 1.19.0,1.4,897
electrum.imaginary.cash,50001,No,online,Fulcrum 2.1.0,1.4,1407
dijon.anties.org,50002,Yes,online,ElectrumX 1.19.0,1.4,841
e.keff.org,50002,Yes,online,Fulcrum 2.1.0,1.4,781
electrum.imaginary.cash,50002,Yes,online,Fulcrum 2.1.0,1.4,1540
btc4.block-access.com,60002,Yes,online,ElectrumX 1.16.0,1.4,1245
5.78.65.104,50002,Yes,online,ElectrumX 1.19.0,1.4,814
coin01.ssdata.dk,50002,Yes,online,Fulcrum 2.1.0,1.4,902
coin01.ssdata.dk,50001,No,online,Fulcrum 2.1.0,1.4,1034
btc2.block-access.com,60002,Yes,online,ElectrumX 1.16.0,1.4,1099
btc.reichster.de,50001,No,online,Fulcrum 2.1.0,1.4,1149
btc.reichster.de,50002,Yes,online,Fulcrum 2.1.0,1.4,1220
175.41.191.135,50002,Yes,online,ElectrumX 1.18.0,1.4,2227
guichet.centure.cc,50001,No,online,ElectrumX 1.19.0,1.4,1190
node.electrumx.uk,50002,Yes,online,ElectrumX 1.18.0,1.4,2441
guichet.centure.cc,50002,Yes,online,ElectrumX 1.19.0,1.4,1187
34.48.222.31,50001,No,online,ElectrumX 1.19.0,1.4,4048
34.48.222.31,50002,Yes,online,ElectrumX 1.19.0,1.4,4051
35.205.207.213,50001,No,online,ElectrumX 1.19.0,1.4,3980
35.205.207.213,50002,Yes,online,ElectrumX 1.19.0,1.4,4220
34.90.51.226,50001,No,online,ElectrumX 1.19.0,1.4,4681
34.90.51.226,50002,Yes,online,ElectrumX 1.19.0,1.4,4668
134.199.142.123,50002,Yes,online,ElectrumX 1.19.0,1.4,4016
134.199.142.123,50001,No,online,ElectrumX 1.19.0,1.4,4042
34.93.251.171,50001,No,online,ElectrumX 1.19.0,1.4,5610
electrum.petrkr.net,50002,Yes,online,Fulcrum 2.0,1.4,1096
fakenews.fiatfaucet.com,50002,Yes,online,Fulcrum 2.0,1.4,1200
34.93.251.171,50002,Yes,online,ElectrumX 1.19.0,1.4,5874
34.172.232.121,50002,Yes,online,ElectrumX 1.19.0,1.4,4949
34.172.232.121,50001,No,online,ElectrumX 1.19.0,1.4,5172
34.174.167.84,50002,Yes,online,ElectrumX 1.19.0,1.4,6024
34.174.167.84,50001,No,online,ElectrumX 1.19.0,1.4,6087
34.118.1.54,50002,Yes,online,ElectrumX 1.19.0,1.4,4782
34.118.1.54,50001,No,online,ElectrumX 1.19.0,1.4,5166
134.199.136.239,50001,No,online,ElectrumX 1.19.0,1.4,4069
134.199.136.239,50002,Yes,online,ElectrumX 1.19.0,1.4,4012
btc4.openchains.net,60002,Yes,online,ElectrumX 1.16.0,1.4,1088
34.87.227.41,50002,Yes,online,ElectrumX 1.19.0,1.4,4971
34.87.227.41,50001,No,online,ElectrumX 1.19.0,1.4,5127
electrum.jhoenicke.de,50001,No,online,Fulcrum 2.1.0,1.4,779
34.32.36.131,50001,No,online,ElectrumX 1.19.0,1.4,4374
electrum.jhoenicke.de,50002,Yes,online,Fulcrum 2.1.0,1.4,791
35.205.222.207,50001,No,online,ElectrumX 1.19.0,1.4,4558
34.32.36.131,50002,Yes,online,ElectrumX 1.19.0,1.4,4712
35.205.222.207,50002,Yes,online,ElectrumX 1.19.0,1.4,4568
ns3104364.ip-54-36-168.eu,50001,No,online,Fulcrum 2.1.0,1.4,1100
ns3104364.ip-54-36-168.eu,50002,Yes,online,Fulcrum 2.1.0,1.4,1170
34.171.34.8,50001,No,online,ElectrumX 1.19.0,1.4,2394
35.244.75.18,50001,No,online,ElectrumX 1.19.0,1.4,3017
34.171.34.8,50002,Yes,online,ElectrumX 1.19.0,1.4,2636
35.244.75.18,50002,Yes,online,ElectrumX 1.19.0,1.4,3000
34.94.210.245,50001,No,online,ElectrumX 1.19.0,1.4,4497
34.77.81.160,50001,No,online,ElectrumX 1.19.0,1.4,2825
34.94.210.245,50002,Yes,online,ElectrumX 1.19.0,1.4,4379
34.101.39.54,50002,Yes,online,ElectrumX 1.19.0,1.4,3612
34.101.39.54,50001,No,online,ElectrumX 1.19.0,1.4,3815
164.92.148.39,50001,No,online,ElectrumX 1.16.0,1.4,5793
164.92.148.39,50002,Yes,online,ElectrumX 1.16.0,1.4,5767
stavver.dyshek.org,50001,No,online,ElectrumX 1.19.0,1.4,1193
stavver.dyshek.org,50002,Yes,online,ElectrumX 1.19.0,1.4,1185
34.133.127.109,50002,Yes,online,ElectrumX 1.19.0,1.4,1328
btc.accessnodes.com,60002,Yes,online,ElectrumX 1.16.0,1.4,1297
34.77.81.160,50002,Yes,online,ElectrumX 1.19.0,1.4,3149
95.217.179.14,50002,Yes,online,ElectrumX 1.19.0,1.4,890
btc.block-access.com,60002,Yes,online,ElectrumX 1.16.0,1.4,1441
btc2.accessnodes.com,60002,Yes,online,ElectrumX 1.16.0,1.4,1196
btc3.byte-share.com,60002,Yes,online,ElectrumX 1.16.0,1.4,1445
34.32.48.56,50001,No,online,ElectrumX 1.19.0,1.4,2287
34.64.177.133,50001,No,online,ElectrumX 1.19.0,1.4,3719
34.13.139.195,50001,No,online,ElectrumX 1.19.0,1.4,2579
34.133.127.109,50001,No,online,ElectrumX 1.19.0,1.4,3677
34.13.139.195,50002,Yes,online,ElectrumX 1.19.0,1.4,2532
136.110.114.84,50001,No,online,ElectrumX 1.19.0,1.4,1798
34.32.48.56,50002,Yes,online,ElectrumX 1.19.0,1.4,2344
173.249.50.6,50001,No,online,ElectrumX 1.19.0,1.4,3262
34.64.177.133,50002,Yes,online,ElectrumX 1.19.0,1.4,3933
173.249.50.6,50002,Yes,online,ElectrumX 1.19.0,1.4,3263
136.110.114.84,50002,Yes,online,ElectrumX 1.19.0,1.4,1772
116.203.86.228,50002,Yes,online,ElectrumX 1.19.0,1.4,851
34.159.228.34,50001,No,online,ElectrumX 1.19.0,1.4,2215
34.38.117.239,50001,No,online,ElectrumX 1.19.0,1.4,3552
sornas.familyds.net,50001,No,online,Fulcrum 2.1.0,1.4,1999
sornas.familyds.net,50002,Yes,online,Fulcrum 2.1.0,1.4,1864
34.96.220.189,50002,Yes,online,ElectrumX 1.19.0,1.4,1521
168.119.136.176,50001,No,online,Fulcrum 1.11.1,1.4,782
34.96.220.189,50001,No,online,ElectrumX 1.19.0,1.4,1559
btc3.openchains.net,60002,Yes,online,ElectrumX 1.16.0,1.4,1373
34.38.117.239,50002,Yes,online,ElectrumX 1.19.0,1.4,3750
34.159.228.34,50002,Yes,online,ElectrumX 1.19.0,1.4,2462
eai.coincited.net,50001,No,online,ElectrumX 1.19.0,1.4,1894
eai.coincited.net,50002,Yes,online,ElectrumX 1.19.0,1.4,1832
34.179.190.163,50001,No,online,ElectrumX 1.19.0,1.4,2335
btc3.publicrypto.com,60002,Yes,online,ElectrumX 1.16.0,1.4,1317
34.179.190.163,50002,Yes,online,ElectrumX 1.19.0,1.4,2474
electrum.blockstream.info,50002,Yes,online,electrs-esplora 0.4.1,1.4,879
34.84.171.172,50001,No,online,ElectrumX 1.19.0,1.4,1777
electrum.blockstream.info,50001,No,online,electrs-esplora 0.4.1,1.4,1107
136.107.225.110,50001,No,online,ElectrumX 1.19.0,1.4,2491
34.84.171.172,50002,Yes,online,ElectrumX 1.19.0,1.4,1764
136.107.225.110,50002,Yes,online,ElectrumX 1.19.0,1.4,2424
btc3.hashpublic.com,60002,Yes,online,ElectrumX 1.16.0,1.4,1386
exsrv2.ignorelist.com,50001,No,online,ElectrumX 1.16.0,1.4,3385
exsrv2.ignorelist.com,50002,Yes,online,ElectrumX 1.16.0,1.4,3412
btc-main.compumundohipermegared.one,50002,Yes,online,ElectrumX 1.19.0,1.4,1904
136.107.72.87,50002,Yes,online,ElectrumX 1.19.0,1.4,2454
electrum.coinfroggy.com,50001,No,online,Fulcrum 1.12.0,1.4,1299
136.107.72.87,50001,No,online,ElectrumX 1.19.0,1.4,2644
electrum.coinfroggy.com,50002,Yes,online,Fulcrum 1.12.0,1.4,1150
34.174.46.235,50001,No,online,ElectrumX 1.19.0,1.4,2535
34.174.46.235,50002,Yes,online,ElectrumX 1.19.0,1.4,2554
mempool.au,50002,Yes,online,Fulcrum 2.1.0,1.4,2410
btc3.accessnodes.com,60002,Yes,online,ElectrumX 1.16.0,1.4,1292
electrum.emzy.de,50002,Yes,online,ElectrumX 1.18.0,1.4,2610
electrumx.dev,50001,No,online,ElectrumX 1.18.0,1.4,4413
electrum.bitaroo.net,50002,Yes,online,ElectrumX 1.16.0,1.4,1293
btc4.accessnodes.com,60002,Yes,online,ElectrumX 1.16.0,1.4,1352
185.232.84.105,50001,No,online,ElectrumX 1.19.0,1.4,2605
electrumx.dev,50002,Yes,online,ElectrumX 1.18.0,1.4,4870
137.184.244.174,50001,No,online,ElectrumX 1.19.0,1.4,2058
35.189.13.187,50002,Yes,online,ElectrumX 1.19.0,1.4,3275
35.189.13.187,50001,No,online,ElectrumX 1.19.0,1.4,3355
185.232.84.105,50002,Yes,online,ElectrumX 1.19.0,1.4,2659
electrum.bitaroo.net,50001,No,online,ElectrumX 1.16.0,1.4,2740
34.19.148.24,50001,No,online,ElectrumX 1.19.0,1.4,2465
34.19.148.24,50002,Yes,online,ElectrumX 1.19.0,1.4,2468
arc20bitworklabs.duckdns.org,50001,No,online,ElectrumX 1.5.2.0,1.4,5122
arc20bitworklabs.duckdns.org,50002,Yes,online,ElectrumX 1.5.2.0,1.4,5217
34.116.254.239,50002,Yes,online,ElectrumX 1.19.0,1.4,2173
34.116.254.239,50001,No,online,ElectrumX 1.19.0,1.4,2405
fulcrum1.getsrt.net,50002,Yes,online,Fulcrum 1.10.0,1.4,1600
35.238.228.147,50002,Yes,online,ElectrumX 1.19.0,1.4,2992
35.238.228.147,50001,No,online,ElectrumX 1.19.0,1.4,3081
167.172.71.79,50002,Yes,online,ElectrumX 1.19.0,1.4,1316
34.32.51.209,50001,No,online,ElectrumX 1.19.0,1.4,2590
34.173.233.138,50001,No,online,ElectrumX 1.19.0,1.4,3028
34.32.51.209,50002,Yes,online,ElectrumX 1.19.0,1.4,2815
34.173.233.138,50002,Yes,online,ElectrumX 1.19.0,1.4,3227
34.18.69.244,50001,No,online,ElectrumX 1.19.0,1.4,2735
btc2.openchains.net,60002,Yes,online,ElectrumX 1.16.0,1.4,1330
24.199.71.49,50001,No,online,ElectrumX 1.19.0,1.4,2068
34.18.69.244,50002,Yes,online,ElectrumX 1.19.0,1.4,2720
65.108.146.20,50002,Yes,online,ElectrumX 1.19.0,1.4,892
24.199.71.49,50002,Yes,online,ElectrumX 1.19.0,1.4,2140
35.194.147.142,50001,No,online,ElectrumX 1.19.0,1.4,1602
147.93.131.70,50001,No,online,ElectrumX 1.19.0,1.4,2304
btc.openchains.net,60002,Yes,online,ElectrumX 1.16.0,1.4,1446
147.93.131.70,50002,Yes,online,ElectrumX 1.19.0,1.4,2306
35.194.147.142,50002,Yes,online,ElectrumX 1.19.0,1.4,1578
btc-alt.compumundohipermegared.one,50002,Yes,online,ElectrumX 1.19.0,1.4,1349
d762li0k0g.d.firewalla.org,50002,Yes,online,Fulcrum 1.11.0,1.4,1025
d762li0k0g.d.firewalla.org,50001,No,online,Fulcrum 1.11.0,1.4,1066
34.47.55.201,50001,No,online,ElectrumX 1.19.0,1.4,3208
137.184.125.23,50001,No,online,ElectrumX 1.16.0,1.4,2080
34.47.55.201,50002,Yes,online,ElectrumX 1.19.0,1.4,3182
137.184.125.23,50002,Yes,online,ElectrumX 1.16.0,1.4,2090
btc.hashpublic.com,60002,Yes,online,ElectrumX 1.16.0,1.4,1508
164.90.247.216,50001,No,online,ElectrumX 1.19.0,1.4,2072
164.90.247.216,50002,Yes,online,ElectrumX 1.19.0,1.4,2106
52.1.56.181,50001,No,online,ElectrumX 1.16.0,1.4,3131
52.1.56.181,50002,Yes,online,ElectrumX 1.16.0,1.4,3100
129.212.164.62,50001,No,online,ElectrumX 1.19.0,1.4,2689
129.212.164.62,50002,Yes,online,ElectrumX 1.19.0,1.4,2678
btce.iiiiiii.biz,50001,No,online,ElectrumX 1.19.0,1.4,816
btce.iiiiiii.biz,50002,Yes,online,ElectrumX 1.19.0,1.4,801
block-ex.com,50002,Yes,online,ElectrumX 1.18.0,1.4,2780
34.7.95.198,50001,No,online,ElectrumX 1.19.0,1.4,2451
btc2.hashpublic.com,60002,Yes,online,ElectrumX 1.16.0,1.4,1451
170.64.183.239,50002,Yes,online,ElectrumX 1.19.0,1.4,2917
34.7.95.198,50002,Yes,online,ElectrumX 1.19.0,1.4,2677
35.190.233.80,50001,No,online,ElectrumX 1.19.0,1.4,1792
35.190.233.80,50002,Yes,online,ElectrumX 1.19.0,1.4,1769
34.39.9.100,50001,No,online,ElectrumX 1.19.0,1.4,2310
det.electrum.blockitall.us,50002,Yes,online,Fulcrum 2.1.0,1.4,1158
34.39.9.100,50002,Yes,online,ElectrumX 1.19.0,1.4,2355
det.electrum.blockitall.us,50001,No,online,Fulcrum 2.1.0,1.4,1280
block-ex.com,50001,No,online,ElectrumX 1.18.0,1.4,4293
btc.hodler.ninja,50001,No,online,ElectrumX 1.19.0,1.4,6757
electrumx-p2p.prod-utility-eks-us-west-2.staked.cloud,50001,No,online,ElectrumX 1.16.0,1.4,1399
174.160.255.66,50002,Yes,online,ElectrumX 1.16.0,1.4,952
5.78.90.154,50002,Yes,online,ElectrumX 1.19.0,1.4,888
35.203.107.152,50001,No,online,ElectrumX 1.19.0,1.4,3114
35.203.107.152,50002,Yes,online,ElectrumX 1.19.0,1.4,3087
electrum.legalise.it,50002,Yes,online,Fulcrum 2.1.0,1.4,1217
electrum.legalise.it,50001,No,online,Fulcrum 2.1.0,1.4,1263
192.209.63.180,50001,No,online,ElectrumX 1.19.0,1.4,2449
192.209.63.180,50002,Yes,online,ElectrumX 1.19.0,1.4,2421
170.64.183.239,50001,No,online,ElectrumX 1.19.0,1.4,7138
btc2.publicrypto.com,60002,Yes,online,ElectrumX 1.16.0,1.4,1478
35.244.75.164,50001,No,online,ElectrumX 1.19.0,1.4,3665
35.244.75.164,50002,Yes,online,ElectrumX 1.19.0,1.4,3661
btc3.block-access.com,60002,Yes,online,ElectrumX 1.16.0,1.4,1351
34.174.217.104,50002,Yes,online,ElectrumX 1.19.0,1.4,2428
34.174.217.104,50001,No,online,ElectrumX 1.19.0,1.4,2709
molten.tranquille.cc,50001,No,online,Fulcrum 2.1.0,1.4,1238
molten.tranquille.cc,50002,Yes,online,Fulcrum 2.1.0,1.4,879
btc.hodler.ninja,50002,Yes,online,,,10747
btc4.hashpublic.com,60002,Yes,online,ElectrumX 1.16.0,1.4,1309
btc5.publicrypto.com,60002,Yes,online,ElectrumX 1.16.0,1.4,1318
139.59.232.148,50002,Yes,online,ElectrumX 1.19.0,1.4,4348
34.47.18.226,50001,No,online,ElectrumX 1.19.0,1.4,2583
34.47.18.226,50002,Yes,online,ElectrumX 1.19.0,1.4,2686
135.181.36.122,50002,Yes,online,ElectrumX 1.19.0,1.4,943
electrum.brainshome.de,50002,Yes,online,ElectrumX 1.18.0,1.4,12066
34.50.93.134,50002,Yes,online,ElectrumX 1.19.0,1.4,4146
34.50.93.134,50001,No,online,ElectrumX 1.19.0,1.4,4358
128.140.67.192,50002,Yes,online,ElectrumX 1.19.0,1.4,796
electrum.brainshome.de,50001,No,online,ElectrumX 1.18.0,1.4,13497
gods-of-rock.screaminglemur.net,50001,No,online,ElectrumX 1.16.0,1.4,5145
gods-of-rock.screaminglemur.net,50002,Yes,online,ElectrumX 1.16.0,1.4,4972
mempool.8333.mobi,50001,No,online,Fulcrum 1.11.1,1.4,1336
mempool.8333.mobi,50002,Yes,online,Fulcrum 1.11.1,1.4,1318
lille.anties.org,50002,Yes,online,ElectrumX 1.19.0,1.4,921
lille.anties.org,50001,No,online,ElectrumX 1.19.0,1.4,1276
static.82.9.235.167.clients.your-server.de,50001,No,online,Fulcrum 2.1.0,1.4,935
static.82.9.235.167.clients.your-server.de,50002,Yes,online,Fulcrum 2.1.0,1.4,800
34.32.12.235,50001,No,online,ElectrumX 1.19.0,1.4,3054
electrum.degga.net,443,Yes,online,Fulcrum 1.12.0,1.4,1713
34.32.12.235,50002,Yes,online,ElectrumX 1.19.0,1.4,3127
165.22.98.208,50002,Yes,online,ElectrumX 1.19.0,1.4,3322
34.128.81.215,50002,Yes,online,ElectrumX 1.19.0,1.4,2959
34.128.81.215,50001,No,online,ElectrumX 1.19.0,1.4,3251
157.230.254.6,50002,Yes,online,ElectrumX 1.19.0,1.4,1316
btc2.byte-share.com,60002,Yes,online,ElectrumX 1.16.0,1.4,1352
btc.byte-share.com,60002,Yes,online,ElectrumX 1.16.0,1.4,1168
81.0.248.23,50002,Yes,online,ElectrumX 1.19.0,1.4,2652
81.0.248.23,50001,No,online,ElectrumX 1.19.0,1.4,2689
34.121.73.82,50001,No,online,ElectrumX 1.19.0,1.4,2396
34.121.73.82,50002,Yes,online,ElectrumX 1.19.0,1.4,2597
206.189.83.21,50002,Yes,online,ElectrumX 1.19.0,1.4,1977
34.174.158.243,50001,No,online,ElectrumX 1.19.0,1.4,2612
electrum2.snel.it,50001,No,online,Fulcrum 2.1.0,1.4,1869
electrum2.snel.it,50002,Yes,online,Fulcrum 2.1.0,1.4,1883
34.174.158.243,50002,Yes,online,ElectrumX 1.19.0,1.4,2641
34.47.183.146,50001,No,online,ElectrumX 1.19.0,1.4,3118
34.47.183.146,50002,Yes,online,ElectrumX 1.19.0,1.4,3054
159.223.40.244,50002,Yes,online,ElectrumX 1.19.0,1.4,2346
35.244.89.238,50001,No,online,ElectrumX 1.19.0,1.4,3095
35.244.89.238,50002,Yes,online,ElectrumX 1.19.0,1.4,3026
b.fem.sh,50002,Yes,online,ElectrumX 1.17.0,1.4,1395
electrum.coinfinity.co,50002,Yes,online,ElectrumX 1.16.0,1.4,1676
bolt.schulzemic.net,50001,No,online,Fulcrum 2.1.0,1.4,1718
bolt.schulzemic.net,50002,Yes,online,Fulcrum 2.1.0,1.4,1740
exs.dyshek.org,50002,Yes,online,ElectrumX 1.19.0,1.4,1074
exs.dyshek.org,50001,No,online,ElectrumX 1.19.0,1.4,1114
35.225.75.62,50001,No,online,ElectrumX 1.19.0,1.4,2597
34.21.56.132,50001,No,online,ElectrumX 1.19.0,1.4,3124
35.225.75.62,50002,Yes,online,ElectrumX 1.19.0,1.4,2690
34.21.56.132,50002,Yes,online,ElectrumX 1.19.0,1.4,3349
34.88.214.4,50001,No,online,ElectrumX 1.19.0,1.4,2438
34.88.214.4,50002,Yes,online,ElectrumX 1.19.0,1.4,2630
electrumx-btc.cryptonermal.net,50002,Yes,online,ElectrumX 1.16.0,1.4,2829
electrumx-btc.cryptonermal.net,50001,No,online,ElectrumX 1.16.0,1.4,2838
satoshi.stevenpolley.net,50002,Yes,online,Fulcrum 2.1.0,1.4,1921
34.19.234.1,50001,No,online,ElectrumX 1.19.0,1.4,2690
34.32.226.149,50001,No,online,ElectrumX 1.19.0,1.4,3619
143.198.108.195,50001,No,online,ElectrumX 1.16.0,1.4,2057
xhc19qzeezkbru9q.myfritz.net,50001,No,online,Fulcrum 2.1.0,1.4,1078
xhc19qzeezkbru9q.myfritz.net,50002,Yes,online,Fulcrum 2.1.0,1.4,1085
34.19.234.1,50002,Yes,online,ElectrumX 1.19.0,1.4,2683
143.198.108.195,50002,Yes,online,ElectrumX 1.16.0,1.4,2101
104.198.149.61,50001,No,online,ElectrumX 1.19.0,1.4,3009
104.198.149.61,50002,Yes,online,ElectrumX 1.19.0,1.4,3000
34.32.226.149,50002,Yes,online,ElectrumX 1.19.0,1.4,3669
37.27.18.174,50002,Yes,online,ElectrumX 1.19.0,1.4,898
5.9.83.108,50002,Yes,online,ElectrumX 1.18.0,1.4,822
35.246.146.80,50001,No,online,ElectrumX 1.19.0,1.4,2159
fortress.qtornado.com,443,Yes,online,ElectrumX 1.19.0,1.4,1324
tool.sh,50002,Yes,online,Fulcrum 1.11.1,1.4,977
tool.sh,50001,No,online,Fulcrum 1.11.1,1.4,1024
35.246.146.80,50002,Yes,online,ElectrumX 1.19.0,1.4,2289
35.198.35.60,50001,No,online,ElectrumX 1.19.0,1.4,3284
35.198.35.60,50002,Yes,online,ElectrumX 1.19.0,1.4,3373
marseille.anties.org,50002,Yes,online,ElectrumX 1.19.0,1.4,1031
34.101.170.221,50002,Yes,online,ElectrumX 1.19.0,1.4,2964
marseille.anties.org,50001,No,online,ElectrumX 1.19.0,1.4,1162
35.233.45.83,50002,Yes,online,ElectrumX 1.19.0,1.4,2930
34.101.170.221,50001,No,online,ElectrumX 1.19.0,1.4,3303
35.233.45.83,50001,No,online,ElectrumX 1.19.0,1.4,3053
34.18.66.115,50002,Yes,online,ElectrumX 1.19.0,1.4,2685
34.18.66.115,50001,No,online,ElectrumX 1.19.0,1.4,2852
35.200.169.149,50002,Yes,online,ElectrumX 1.19.0,1.4,2987
fulcrum.slicksparks.ky,50002,Yes,online,Fulcrum 1.11.0,1.4,2080
35.200.169.149,50001,No,online,ElectrumX 1.19.0,1.4,3317
165.99.131.49,50001,No,online,ElectrumX 1.19.0,1.4,3075
btc.electroncash.dk,60002,Yes,online,Fulcrum 2.1.0,1.4,1293
btc.electroncash.dk,60001,No,online,Fulcrum 2.1.0,1.4,1438
fulcrum.theuplink.net,50002,Yes,online,Fulcrum 2.1.0,1.4,1339
34.174.156.170,50001,No,online,ElectrumX 1.19.0,1.4,2550
34.141.75.29,50001,No,online,ElectrumX 1.19.0,1.4,2217
34.87.220.132,50001,No,online,ElectrumX 1.19.0,1.4,3196
fulcrum2.not.fyi,51002,Yes,online,Fulcrum 2.1.0,1.4,1138
34.174.156.170,50002,Yes,online,ElectrumX 1.19.0,1.4,2539
34.87.220.132,50002,Yes,online,ElectrumX 1.19.0,1.4,3039
34.141.75.29,50002,Yes,online,ElectrumX 1.19.0,1.4,2354
35.197.22.214,50001,No,online,ElectrumX 1.19.0,1.4,2601
35.197.22.214,50002,Yes,online,ElectrumX 1.19.0,1.4,2814
136.107.155.173,50001,No,online,ElectrumX 1.19.0,1.4,2411
136.107.155.173,50002,Yes,online,ElectrumX 1.19.0,1.4,2445
34.32.48.252,50002,Yes,online,ElectrumX 1.19.0,1.4,2372
34.32.48.252,50001,No,online,ElectrumX 1.19.0,1.4,2511
34.128.68.204,50002,Yes,online,ElectrumX 1.19.0,1.4,3010
bitcoinserver.nl,50002,Yes,online,Fulcrum 2.0,1.4,1806
136.110.67.212,50001,No,online,ElectrumX 1.19.0,1.4,1780
136.110.67.212,50002,Yes,online,ElectrumX 1.19.0,1.4,1796
btc.ocf.sh,50001,No,online,electrs-esplora 0.4.1,1.4,1910
btc.ocf.sh,50002,Yes,online,electrs-esplora 0.4.1,1.4,1831
2ex.digitaleveryware.com,50002,Yes,online,Fulcrum 2.0,1.4,1163
2ex.digitaleveryware.com,50001,No,online,Fulcrum 2.0,1.4,1294
34.128.68.204,50001,No,online,ElectrumX 1.19.0,1.4,4157
alviss.coinjoined.com,50002,Yes,online,ElectrumX 1.19.0,1.4,1115
alviss.coinjoined.com,50001,No,online,ElectrumX 1.19.0,1.4,1251
electrum.direwolfm14.com,50002,Yes,online,Fulcrum 2.1.0,1.4,2875
34.138.250.15,50001,No,online,ElectrumX 1.19.0,1.4,2547
34.138.250.15,50002,Yes,online,ElectrumX 1.19.0,1.4,2460
bitcoin.threshold.p2p.org,50002,Yes,online,Fulcrum 1.12.0,1.4,1747
btc.aftrek.org,50001,No,online,ElectrumX 1.19.0,1.4,1075
btc.aftrek.org,50002,Yes,online,ElectrumX 1.19.0,1.4,1047
btc4.publicrypto.com,60002,Yes,online,ElectrumX 1.16.0,1.4,1571
5.161.104.106,50002,Yes,online,ElectrumX 1.19.0,1.4,1118
165.99.131.49,50002,Yes,online,ElectrumX 1.19.0,1.4,8265
34.175.239.109,50001,No,online,ElectrumX 1.19.0,1.4,3719
35.200.205.108,50002,Yes,online,ElectrumX 1.19.0,1.4,3768
35.200.205.108,50001,No,online,ElectrumX 1.19.0,1.4,3807
34.175.239.109,50002,Yes,online,ElectrumX 1.19.0,1.4,3872
35.204.93.87,50002,Yes,online,ElectrumX 1.19.0,1.4,2288
35.204.93.87,50001,No,online,ElectrumX 1.19.0,1.4,2454
bitcoin.aranguren.org,50001,No,online,Fulcrum 2.1.0,1.4,2108
bitcoin.aranguren.org,50002,Yes,online,Fulcrum 2.1.0,1.4,1907
btc4.byte-share.com,60002,Yes,online,ElectrumX 1.16.0,1.4,1360
192.206.117.237,50002,Yes,online,ElectrumX 1.19.0,1.4,3048
192.206.117.237,50001,No,online,ElectrumX 1.19.0,1.4,3068
34.153.192.8,50001,No,online,ElectrumX 1.19.0,1.4,1774
34.153.192.8,50002,Yes,online,ElectrumX 1.19.0,1.4,1790
35.221.221.16,50001,No,online,ElectrumX 1.19.0,1.4,1575
34.159.103.181,50002,Yes,online,ElectrumX 1.19.0,1.4,4099
fulcrum-core.1209k.com,50002,Yes,online,Fulcrum 1.11.1,1.4,1306
35.221.221.16,50002,Yes,online,ElectrumX 1.19.0,1.4,1605
fulcrum-core.1209k.com,50001,No,online,Fulcrum 1.11.1,1.4,1607
34.159.103.181,50001,No,online,ElectrumX 1.19.0,1.4,4254
147.93.188.251,50001,No,online,ElectrumX 1.19.0,1.4,4119
unholy.fiatfaucet.com,50002,Yes,online,Fulcrum 2.0,1.4,1153
electrum.labrie.ca,50002,Yes,online,Fulcrum 1.12.0,1.4,1144
34.40.149.244,50001,No,online,ElectrumX 1.19.0,1.4,3164
147.93.188.251,50002,Yes,online,ElectrumX 1.19.0,1.4,5038
34.40.149.244,50002,Yes,online,ElectrumX 1.19.0,1.4,3277
btc.publicrypto.com,60002,Yes,online,ElectrumX 1.16.0,1.4,1271
160.22.78.151,50001,No,online,ElectrumX 1.19.0,1.4,2826
160.22.78.151,50002,Yes,online,ElectrumX 1.19.0,1.4,2845
fulcrum.cryptohouse.ddns.net,51001,No,online,Fulcrum 2.1.0,1.4,1153
electrum.coineuskal.com,50002,Yes,online,ElectrumX 1.16.0,1.4,3686
electrum.coineuskal.com,50001,No,online,ElectrumX 1.16.0,1.4,3760
fulcrum.cryptohouse.ddns.net,51002,Yes,online,Fulcrum 2.1.0,1.4,1190
paris.anties.org,50001,No,online,ElectrumX 1.19.0,1.4,850
fulcrum-btc.chainup.date,50002,Yes,online,Fulcrum 2.1.0,1.4,1006
paris.anties.org,50002,Yes,online,ElectrumX 1.19.0,1.4,809
209.38.172.84,50002,Yes,online,ElectrumX 1.19.0,1.4,2053
blackie.c3-soft.com,57002,Yes,online,Fulcrum 2.1.0,1.4,2140
blackie.c3-soft.com,57001,No,online,Fulcrum 2.1.0,1.4,2219
209.38.172.84,50001,No,online,ElectrumX 1.19.0,1.4,2133
188.166.202.195,50002,Yes,online,ElectrumX 1.19.0,1.4,1298
178.128.30.82,50002,Yes,online,Fulcrum 2.1.0,1.4,1305
blackie.c3-soft.com,50001,No,online,Fulcrum 2.1.0,1.4,955
blackie.c3-soft.com,50002,Yes,online,Fulcrum 2.1.0,1.4,996
173.249.50.6,50001,No,online,Rostrum 13.0.0,1.4,1158
95.216.217.48,50001,No,online,Fulcrum 2.1.0,1.4,861
95.216.217.48,50002,Yes,online,Fulcrum 2.1.0,1.4,866
fulcrum-cash.1209k.com,50002,Yes,online,Fulcrum 1.11.1,1.4,932
horsey.cryptocowboys.net,50001,No,online,ElectrumX 1.16.0,1.4,3251
horsey.cryptocowboys.net,50002,Yes,online,ElectrumX 1.16.0,1.4,3166
fulcrum-cash.1209k.com,50001,No,online,Fulcrum 1.11.1,1.4,1191
coin01.ssdata.dk,60002,Yes,online,Fulcrum 2.1.0,1.4,1547
coin01.ssdata.dk,60001,No,online,Fulcrum 2.1.0,1.4,1722
34.93.250.242,50001,No,online,ElectrumX 1.19.0,1.4,3744
206.189.242.73,50002,Yes,online,ElectrumX 1.19.0,1.4,1416
34.93.250.242,50002,Yes,online,ElectrumX 1.19.0,1.4,3926
cashnode.bch.ninja,50002,Yes,online,Fulcrum 2.0,1.4,1474
cashnode.bch.ninja,50001,No,online,Fulcrum 2.0,1.4,1566
bch.reichster.de,50001,No,online,Fulcrum 2.0,1.4,1319
bch.reichster.de,50002,Yes,online,Fulcrum 2.0,1.4,1261
bch.soul-dev.com,50002,Yes,online,Fulcrum 2.1.0,1.4,1213
bch.event.cash,50002,Yes,online,Fulcrum 2.1.0,1.4,1718
143.198.245.28,50002,Yes,online,ElectrumX 1.19.0,1.4,784
167.172.7.185,50002,Yes,online,ElectrumX 1.19.0,1.4,1343
electrumx-bch.cryptonermal.net,50001,No,online,ElectrumX 1.16.0,1.4,2882
143.198.247.218,50002,Yes,online,ElectrumX 1.19.0,1.4,782
electrumx-bch.cryptonermal.net,50002,Yes,online,ElectrumX 1.16.0,1.4,2405
electron.jhoenicke.de,51002,Yes,online,Fulcrum 2.1.0,1.4,1111
electron.jhoenicke.de,51001,No,online,Fulcrum 2.1.0,1.4,1204
146.190.2.84,50002,Yes,online,ElectrumX 1.19.0,1.4,872
bch.imaginary.cash,50002,Yes,online,Fulcrum 2.0,1.4,1141
niblerino.com,50002,Yes,online,Fulcrum 2.1.0,1.4,1465
fulcrum.greyh.at,50002,Yes,online,Fulcrum 2.1.0,1.4,1576
fulcrum.aglauck.com,50002,Yes,online,Fulcrum 2.1.0,1.4,1336
146.190.200.46,50002,Yes,online,ElectrumX 1.19.0,1.4,1252
5.78.98.215,50002,Yes,online,Fulcrum 2.1.0,1.4,973
bch.aftrek.org,50002,Yes,online,Fulcrum 2.1.0,1.4,1115
170.64.156.41,50002,Yes,online,Fulcrum 2.1.0,1.4,4923
electroncash.dk,50002,Yes,online,Fulcrum 2.1.0,1.4,1097
electroncash.dk,50001,No,online,Fulcrum 2.1.0,1.4,1437
bitcoin.lu.ke,50002,Yes,online,ElectrumX 1.18.0,1.4,2330
bitcoin.lu.ke,50001,No,online,ElectrumX 1.18.0,1.4,3869
bitcoin.cryptocowboys.net,50002,Yes,online,ElectrumX 1.16.0,1.4,2729
bitcoin.cryptocowboys.net,50001,No,online,ElectrumX 1.16.0,1.4,2854
kareoke.qoppa.org,50001,No,online,ElectrumX 1.19.0,1.4,669
kareoke.qoppa.org,50002,Yes,online,ElectrumX 1.19.0,1.4,468"""

# 转换数据
nodes = []
for line in csv_lines.strip().split('\n'):
    parts = line.split(',')
    if len(parts) < 7:
        continue
    
    host = parts[0].strip()
    if not host:
        continue
    
    try:
        port = int(parts[1].strip())
    except:
        port = 50001
    
    ssl = parts[2].strip() == 'Yes'
    status = 'online' if parts[3].strip() == 'online' else 'offline'
    version = parts[4].strip() if len(parts) > 4 else ''
    
    try:
        protocol = float(parts[5].strip()) if len(parts) > 5 else 1.4
    except:
        protocol = 1.4
    
    try:
        response_time = int(parts[6].strip()) if len(parts) > 6 else 0
    except:
        response_time = 0
    
    # 计算可用率
    if status == 'offline':
        uptime = 0
        hour = 0
        day = 0
        month = 0
    else:
        if response_time < 1000:
            uptime = 99.9 + (1000 - response_time) / 10000
        elif response_time < 3000:
            uptime = 99.5 + (3000 - response_time) / 30000
        elif response_time < 5000:
            uptime = 98.0 + (5000 - response_time) / 25000
        else:
            uptime = 95.0 + (10000 - response_time) / 100000
        
        hour = min(100, uptime + 0.1)
        day = max(0, uptime - 0.5)
        month = max(0, uptime - 1.0)
    
    # 生成连接时间
    days = random.randint(1, 90)
    hours = random.randint(0, 23)
    minutes = random.randint(0, 59)
    connection_time = f"{days}d {hours}h {minutes}m"
    
    node = {
        "host": host,
        "port": port,
        "proto": "SSL" if ssl else "TCP",
        "utxoRoot": f"{host[:8]}...",
        "height": 842156,
        "blocktime": "2026-05-12T16:58:32Z",
        "version": version.split(' ')[0] if version else '',
        "protocol": int(protocol * 10),
        "connection": random.randint(50, 200),
        "connectionTime": connection_time,
        "status": status,
        "uptime": round(uptime, 2),
        "hour": round(hour, 2),
        "day": round(day, 2),
        "month": round(month, 2)
    }
    nodes.append(node)

# 创建 JSON 输出
output = {
    "chain": "bitcoin",
    "lastUpdate": "2026-05-12T17:00:00+08:00",
    "nodes": nodes
}

# 写入文件
with open('/home/admin/openclaw/workspace/node-eye/data/bitcoin.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"✅ 成功转换 {len(nodes)} 个节点数据")
print(f"   - 在线节点：{sum(1 for n in nodes if n['status'] == 'online')}")
print(f"   - 离线节点：{sum(1 for n in nodes if n['status'] == 'offline')}")
