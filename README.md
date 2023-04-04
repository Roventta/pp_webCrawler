# pp_webCrawler
a web crawler that parse data from two specific websites

dsl website's content list is not well constructed, each entry have various random fields, the feature of these field is entitled
by text, but neither HTML element id nor name.

Each field is seperated by <br/> solely.

dsl website's content list is ordered into clusters by alphabet characters, each cluser is leaded by one element, that have a id, which is a single character.
this program exploits this feature, that locates one cluster by searching elements with an id of "A", "B", etc., such operation is done
by function, dql_cluster_first_entry(guide_word, soup).

After locating one cluster, the program will route itself into the first element in the cluster, and start analysing the content,
since the first line of one element is always name, it does nothing but write it into the name field in pd.dataframe.

after writing the first entry, it will read through the following entries, first identify what field it belongs to (dql_identify_insert()), 
then insert them to relative field in pd frame.

Different schemes are applied for contact, since it is one line contain two different fields.
