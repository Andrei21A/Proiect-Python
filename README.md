# Find-command

In urmatorul proiect am realizat comanda find din linux 

Codul imita comanda "find" si foloseste o serie diferita de argumente cum ar fi -name, -iname, .(extensii) pentru a optimiza cautarea. In plus se poate folosi si comanda -exec pentru folosirea comenzilor bash asupra fisierelor gasite.

Am incercat sa am un cod cat mai concis si am folosit comprehensiuni de liste impreuna cu o logica cat mai buna pentru if uri. De asemenea, folosind functia "matches_pattern" trec prin toate cazurile posibile pt find -name/iname "...".

Cea mai importanta comanda a fost os.walk ce mi-a permis sa pot sa ma plimb prin directory-uri si fisiere folosindu-ma de tuplul root,dirs,files 

Toata logica si varietatea de combinatii de argumente are loc in main, iar la final este apelata functia find cu toate argumente ce au fost setate
