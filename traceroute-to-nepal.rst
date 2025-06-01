Traceroute to Nepal
###################
:date: 2012-05-03 23:58
:author: sauravtuladhar
:category: Misc 
:slug: traceroute-to-nepal
:status: published

traceroute is a wonderful tool to analyse network structure. According to its man page,

   traceroute tracks the route packets taken from an IP network on their way to a given host. It utilizes the IP protocol's time to live (TTL) field and attempts to elicit an ICMP TIME_EXCEEDED response from each gateway along the path to the host.

From time to time, I like to run my traceroute to explore how I connect to different websites via my ISP's network. It is specially interesting for me to to traceroute tests from US to servers hosted in Nepal, as I have some idea about how internet traffic flows in/out of Nepal. Today I'll present results on traceroute test to Nepal Telecom's (NT) website. Since NT had optical fiber links through to India and beyond, it will be interesting to see which links are utilized for a packet to reach from US to NT.

[caption id="attachment_155" align="aligncenter" width="738"]\ |Traceroute result| Traceroute output for Nepal Telecom website.[/caption]

**Analysis:**

-  Hops 1 - 9 , the packets are still in US
-  The trace starts from my router and goes into Comcast network and  to BOS (Boston) in hop 4 and comes down to NYC ( New York City ) in hop 7 via routers at Woburn and Needham MA in hos 5 and 6 respectively
-  At NYC, the packet drops off from Comcast network to L3's  10 Gigabit ethernet links. Since NYC is the main landing site for Trans-Atlantic optical fiber cables coming ashore east coast in US,  it is expected that the packet going out to Nepal would also follow the same path.
-  From NYC , the next hop(9) is  to Airtel in India via L3's 10Gigabit link
-   Among several telecom operators in India, NT has bought the largest bandwidth with Airtel, so it makes sense that the route via Airtel's network is most viable one.
-  At hop 11, the packet reached India. This is evident from the jump in round trip delay to ~400ms which translates to ~ 11,000 km. The fiber landing site is most likely Mumbai, India.
-  From there on, the packet enters Nepal at hop 12.  The router IP 202.70.x.x belongs to NT. The router at hope 12 is a Border Gateway router, most probably at Bhairahawa  where most of NT connection goes through to India.
-  The the packet goes through Butwal to Pokhara (pkr.btw) in hope 13
-  From Pokhara, the packet reaches NT's Intn'l Exchange Bldg at Patan on hop 14. From there on the packet finally reaches the webserver at NT's central office at Bhadrakali.

This was a traceroute analysis through Comcast network. Next I'll do the same kind of analysis for trace through Verizon DSL network.

.. |Traceroute result| image:: http://sauravtuladhar.files.wordpress.com/2012/05/trace_nb_ktm.png?w=1024
   :class: wp-image-155
   :width: 738px
   :height: 194px
   :target: http://sauravtuladhar.files.wordpress.com/2012/05/trace_nb_ktm.png
